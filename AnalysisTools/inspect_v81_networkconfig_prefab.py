#!/usr/bin/env python3
"""Fail-closed static V81 NetworkConfig prefab capture for EntranceTeleportB.

This helper never starts Unity or managed game/mod code. It parses only the exact
installed base-game serialized assets plus the exact installed Assembly-CSharp.dll
and Unity.Netcode.Runtime.dll. Output is compact JSON suitable for repository evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import importlib.metadata
import json
from pathlib import Path
import struct
import sys

UNITYPY_VERSION = "1.25.3"
DNFILE_VERSION = "0.18.0"
DNCIL_VERSION = "1.0.2"
TTGEN_VERSION = "0.0.10"
TARGET_NAME = "EntranceTeleportB"
NETWORK_MANAGER_SCRIPT = ("NetworkManager", "Unity.Netcode", "unity.netcode.runtime")
NETWORK_MANAGER_FULL_NAME = "Unity.Netcode.NetworkManager"
GAME_ASSEMBLY_NAME = "Assembly-CSharp"
REQUIRED_SURFACE = (
    ("EntranceTeleport", "", "assembly-csharp"),
    ("InteractTrigger", "", "assembly-csharp"),
    ("NetworkObject", "Unity.Netcode", "unity.netcode.runtime"),
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _rol32(value: int, shift: int) -> int:
    value &= 0xFFFFFFFF
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def md4_digest(data: bytes) -> bytes:
    """Small deterministic MD4 implementation used only for Unity serialized scriptID recovery."""
    message = bytearray(data)
    bit_length = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message.extend(bit_length.to_bytes(8, "little"))

    a0, b0, c0, d0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    def f(x, y, z):
        return (x & y) | ((~x) & z)

    def g(x, y, z):
        return (x & y) | (x & z) | (y & z)

    def h(x, y, z):
        return x ^ y ^ z

    for offset in range(0, len(message), 64):
        x = struct.unpack("<16I", message[offset:offset + 64])
        a, b, c, d = a0, b0, c0, d0

        for i in range(16):
            if i % 4 == 0:
                a = _rol32(a + f(b, c, d) + x[i], 3)
            elif i % 4 == 1:
                d = _rol32(d + f(a, b, c) + x[i], 7)
            elif i % 4 == 2:
                c = _rol32(c + f(d, a, b) + x[i], 11)
            else:
                b = _rol32(b + f(c, d, a) + x[i], 19)

        for i, k in enumerate((0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15)):
            if i % 4 == 0:
                a = _rol32(a + g(b, c, d) + x[k] + 0x5A827999, 3)
            elif i % 4 == 1:
                d = _rol32(d + g(a, b, c) + x[k] + 0x5A827999, 5)
            elif i % 4 == 2:
                c = _rol32(c + g(d, a, b) + x[k] + 0x5A827999, 9)
            else:
                b = _rol32(b + g(c, d, a) + x[k] + 0x5A827999, 13)

        for i, k in enumerate((0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15)):
            if i % 4 == 0:
                a = _rol32(a + h(b, c, d) + x[k] + 0x6ED9EBA1, 3)
            elif i % 4 == 1:
                d = _rol32(d + h(a, b, c) + x[k] + 0x6ED9EBA1, 9)
            elif i % 4 == 2:
                c = _rol32(c + h(d, a, b) + x[k] + 0x6ED9EBA1, 11)
            else:
                b = _rol32(b + h(c, d, a) + x[k] + 0x6ED9EBA1, 15)

        a0 = (a0 + a) & 0xFFFFFFFF
        b0 = (b0 + b) & 0xFFFFFFFF
        c0 = (c0 + c) & 0xFFFFFFFF
        d0 = (d0 + d) & 0xFFFFFFFF

    return struct.pack("<4I", a0, b0, c0, d0)


def normalize_assembly(value) -> str:
    text = "" if value is None else str(value).strip().lower()
    return text[:-4] if text.endswith(".dll") else text


def script_id_digest(desc, convention: str) -> bytes:
    class_name = str(desc.get("class") or "")
    namespace = str(desc.get("namespace") or "")
    assembly = str(desc.get("assembly") or "")
    if convention == "CLASS_NAMESPACE_ASSEMBLY_NO_DLL":
        assembly = assembly[:-4] if assembly.lower().endswith(".dll") else assembly
    elif convention != "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL":
        raise ValueError("Unknown serialized scriptID convention: " + convention)
    payload = class_name + namespace + assembly
    return md4_digest(payload.encode("utf-8"))


def is_pptr(value) -> bool:
    return isinstance(value, dict) and "m_FileID" in value and "m_PathID" in value


def walk(value, path=()):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, path + (f"[{index}]",))


def path_text(path) -> str:
    out = ""
    for part in path:
        if part.startswith("["):
            out += part
        else:
            out += ("." if out else "") + part
    return out


def script_identity(desc):
    if not desc:
        return None
    return (
        str(desc.get("class") or ""),
        str(desc.get("namespace") or ""),
        normalize_assembly(desc.get("assembly")),
    )


def hash128_bytes(value):
    if isinstance(value, memoryview):
        raw = value.tobytes()
        return raw if len(raw) == 16 else None
    if isinstance(value, (bytes, bytearray)):
        raw = bytes(value)
        return raw if len(raw) == 16 else None
    if isinstance(value, (list, tuple)) and len(value) == 16:
        try:
            return bytes(int(x) & 0xFF for x in value)
        except (TypeError, ValueError):
            return None
    if isinstance(value, dict):
        bracket = [f"bytes[{i}]" for i in range(16)]
        underscored = [f"bytes_{i}_" for i in range(16)]
        keys = bracket if all(k in value for k in bracket) else underscored
        if all(k in value for k in keys):
            try:
                return bytes(int(value[k]) & 0xFF for k in keys)
            except (TypeError, ValueError):
                return None
    attrs = [f"bytes_{i}_" for i in range(16)]
    if all(hasattr(value, a) for a in attrs):
        try:
            return bytes(int(getattr(value, a)) & 0xFF for a in attrs)
        except (TypeError, ValueError):
            return None
    return None


def hash128_state(value) -> str:
    if value is None:
        return "MISSING"
    raw = hash128_bytes(value)
    if raw is None:
        return "UNSUPPORTED:" + type(value).__name__
    return "NONZERO" if any(raw) else "ZERO"


def metadata_type_name(row) -> str:
    if not hasattr(row, "TypeName"):
        return type(row).__name__
    name = str(row.TypeName)
    namespace = str(row.TypeNamespace)
    return f"{namespace}.{name}" if namespace else name


def inspect_game_network_manager_inheritance(dll_path: Path):
    import dnfile

    version = importlib.metadata.version("dnfile")
    if version != DNFILE_VERSION:
        raise ValueError(f"Expected dnfile {DNFILE_VERSION}, got {version}")
    if not dll_path.is_file():
        raise ValueError("Exact installed Assembly-CSharp.dll is missing below the supplied data root")

    pe = dnfile.dnPE(str(dll_path))
    if pe.net is None or pe.net.mdtables is None:
        raise ValueError("Assembly-CSharp.dll is not a readable managed assembly")

    assembly_rows = pe.net.mdtables.Assembly or []
    if not assembly_rows:
        raise ValueError("Assembly-CSharp.dll has no Assembly row")
    assembly_row = assembly_rows.rows[0]
    assembly_name = str(assembly_row.Name)
    if assembly_name != GAME_ASSEMBLY_NAME:
        raise ValueError("Unexpected game assembly identity: " + assembly_name)

    bases = {}
    for t in pe.net.mdtables.TypeDef:
        own = metadata_type_name(t)
        if own == "<Module>":
            continue
        ext = getattr(t, "Extends", None)
        ext_row = None if ext is None else getattr(ext, "row", None)
        bases[own] = None if ext_row is None else metadata_type_name(ext_row)

    derived = []
    for own in sorted(bases):
        chain = []
        cursor = own
        seen = set()
        while True:
            base = bases.get(cursor)
            if not base:
                break
            chain.append(base)
            if base == NETWORK_MANAGER_FULL_NAME:
                namespace, _, class_name = own.rpartition(".")
                derived.append({
                    "type": own,
                    "class": class_name,
                    "namespace": namespace,
                    "assembly": GAME_ASSEMBLY_NAME,
                    "base_chain_to_network_manager": chain,
                })
                break
            if base not in bases:
                break
            if base in seen:
                raise ValueError("Cycle in Assembly-CSharp TypeDef inheritance while resolving " + own)
            seen.add(base)
            cursor = base

    return {
        "dll_bytes": dll_path.stat().st_size,
        "dll_sha256": sha256_file(dll_path),
        "assembly": {
            "name": assembly_name,
            "version": (
                f"{assembly_row.MajorVersion}.{assembly_row.MinorVersion}."
                f"{assembly_row.BuildNumber}.{assembly_row.RevisionNumber}"
            ),
        },
        "network_manager_base_type": NETWORK_MANAGER_FULL_NAME,
        "derived_serialized_owner_types": derived,
        "derived_serialized_owner_type_count": len(derived),
    }


def candidate_asset_files(data_root: Path):
    raw = []
    for name in ("globalgamemanagers", "globalgamemanagers.assets", "resources.assets"):
        p = data_root / name
        if p.is_file():
            raw.append(p)
    raw.extend(p for p in data_root.glob("sharedassets*.assets") if p.is_file())
    raw.extend(p for p in data_root.glob("level*") if p.is_file())
    files = []
    seen = set()
    for p in raw:
        low = p.name.lower()
        if low.endswith((".ress", ".resource", ".assets.ress")):
            continue
        resolved = p.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        files.append(resolved)
    return sorted(files, key=lambda p: p.name.lower())


def inspect_assets(data_root: Path, game_owner_proof, netcode_proof):
    import UnityPy

    version = importlib.metadata.version("UnityPy")
    if version != UNITYPY_VERSION:
        raise ValueError(f"Expected UnityPy {UNITYPY_VERSION}, got {version}")
    ttgen_version = importlib.metadata.version("TypeTreeGeneratorAPI")
    if ttgen_version != TTGEN_VERSION:
        raise ValueError(f"Expected TypeTreeGeneratorAPI {TTGEN_VERSION}, got {ttgen_version}")

    files_on_disk = candidate_asset_files(data_root)
    if not files_on_disk:
        raise ValueError("No supported base-game serialized asset files found")

    file_inventory = [
        {
            "logical_path": str(p.relative_to(data_root)).replace("\\", "/"),
            "bytes": p.stat().st_size,
            "sha256": sha256_file(p),
        }
        for p in files_on_disk
    ]

    env = UnityPy.load(*[str(p) for p in files_on_disk])
    objects = list(env.objects)
    if not objects:
        raise ValueError("UnityPy loaded zero serialized objects")

    serialized_files = {}
    duplicate_names = set()
    for obj in objects:
        name = obj.assets_file.name
        prior = serialized_files.get(name)
        if prior is not None and id(prior) != id(obj.assets_file):
            duplicate_names.add(name)
        serialized_files[name] = obj.assets_file
    if duplicate_names:
        raise ValueError("Ambiguous serialized-file names: " + ", ".join(sorted(duplicate_names)))

    unity_versions = sorted({
        str(getattr(sf, "unity_version", "") or "").strip()
        for sf in serialized_files.values()
        if str(getattr(sf, "unity_version", "") or "").strip()
    })
    if len(unity_versions) != 1:
        raise ValueError("Expected exactly one Unity serialized-file version, found: " + json.dumps(unity_versions))
    unity_version = unity_versions[0]

    from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
    generator = TypeTreeGenerator(unity_version)
    managed_dir = data_root / "Managed"
    generator_inputs = []
    for dll_name in ("Assembly-CSharp.dll", "Unity.Netcode.Runtime.dll"):
        dll_path = managed_dir / dll_name
        if not dll_path.is_file():
            raise ValueError("TypeTree recovery input missing: " + dll_name)
        dll_bytes = dll_path.read_bytes()
        generator.load_dll(dll_bytes)
        generator_inputs.append({
            "logical_path": "Managed/" + dll_name,
            "bytes": len(dll_bytes),
            "sha256": hashlib.sha256(dll_bytes).hexdigest(),
        })

    by_id = {(o.assets_file.name, o.path_id): o for o in objects}
    raw_cache = {}
    full_cache = {}
    descriptor_cache = {}

    def ident(obj):
        return {
            "serialized_file": obj.assets_file.name,
            "path_id": obj.path_id,
            "type": obj.type.name,
        }

    def read_raw(obj):
        key = (obj.assets_file.name, obj.path_id)
        if key not in raw_cache:
            raw_cache[key] = obj.read_typetree()
        return raw_cache[key]

    def resolve(owner, ptr):
        if not is_pptr(ptr):
            return None, "MALFORMED_POINTER"
        if ptr["m_PathID"] == 0:
            return None, "NULL"
        fid = ptr["m_FileID"]
        if fid == 0:
            filename = owner.assets_file.name
        else:
            externals = owner.assets_file.externals
            if fid < 1 or fid > len(externals):
                return None, "INVALID_EXTERNAL_INDEX"
            ext = str(externals[fid - 1].path)
            filename = ext.replace("\\", "/").rsplit("/", 1)[-1]
            if filename not in serialized_files:
                return None, "EXTERNAL_NOT_LOADED:" + ext
        target = by_id.get((filename, ptr["m_PathID"]))
        return (target, "RESOLVED") if target else (None, "PATH_ID_NOT_FOUND:" + filename)

    script_map = {}
    script_errors = []
    for obj in objects:
        if obj.type.name != "MonoScript":
            continue
        try:
            tree = read_raw(obj)
        except Exception as exc:
            script_errors.append({**ident(obj), "error": f"{type(exc).__name__}: {exc}"})
            continue
        properties_hash = hash128_bytes(tree.get("m_PropertiesHash"))
        script_map[(obj.assets_file.name, obj.path_id)] = {
            **ident(obj),
            "class": tree.get("m_ClassName"),
            "namespace": tree.get("m_Namespace"),
            "assembly": tree.get("m_AssemblyName"),
            "properties_hash": None if properties_hash is None else properties_hash.hex(),
        }

    def serialized_script_id(obj):
        st = getattr(obj, "serialized_type", None)
        value = None if st is None else getattr(st, "script_id", None)
        raw = hash128_bytes(value)
        return raw if raw is not None and any(raw) else None

    def serialized_old_type_hash(obj):
        st = getattr(obj, "serialized_type", None)
        value = None if st is None else getattr(st, "old_type_hash", None)
        raw = hash128_bytes(value)
        return raw if raw is not None and any(raw) else None

    convention_matches = Counter()
    convention_samples = 0
    for obj in objects:
        if obj.type.name != "MonoBehaviour":
            continue
        sid = serialized_script_id(obj)
        if sid is None:
            continue
        try:
            head = read_raw(obj)
        except Exception:
            continue
        script, direct_status = resolve(obj, head.get("m_Script"))
        if direct_status != "RESOLVED":
            continue
        rec = script_map.get((script.assets_file.name, script.path_id))
        if rec is None:
            continue
        convention_samples += 1
        for convention in (
            "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL",
            "CLASS_NAMESPACE_ASSEMBLY_NO_DLL",
        ):
            if script_id_digest(rec, convention) == sid:
                convention_matches[convention] += 1

    if convention_samples == 0:
        raise ValueError("Could not calibrate serialized scriptID hashing against any resolved installed MonoScript reference")
    valid_conventions = [
        name
        for name in (
            "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL",
            "CLASS_NAMESPACE_ASSEMBLY_NO_DLL",
        )
        if convention_matches[name] == convention_samples
    ]
    if not valid_conventions:
        raise ValueError(
            "Serialized scriptID hash convention did not validate against all resolved installed MonoScript references: "
            + json.dumps({"samples": convention_samples, "matches": dict(convention_matches)}, sort_keys=True)
        )
    script_id_convention = (
        "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL"
        if "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL" in valid_conventions
        else valid_conventions[0]
    )

    def metadata_type_descriptors(dll_path: Path):
        import dnfile
        pe = dnfile.dnPE(str(dll_path))
        if pe.net is None or pe.net.mdtables is None:
            raise ValueError("Managed scriptID catalog input is not a readable assembly: " + dll_path.name)
        assembly_rows = pe.net.mdtables.Assembly or []
        if not assembly_rows:
            raise ValueError("Managed scriptID catalog input has no Assembly row: " + dll_path.name)
        assembly_name = str(assembly_rows.rows[0].Name)
        if assembly_name != dll_path.stem:
            raise ValueError(f"Managed scriptID catalog assembly identity mismatch for {dll_path.name}: {assembly_name}")
        return [
            {
                "class": str(t.TypeName),
                "namespace": str(t.TypeNamespace),
                "assembly": dll_path.name,
                "metadata_source": "EXACT_INSTALLED_TYPEDEF",
            }
            for t in pe.net.mdtables.TypeDef
            if str(t.TypeName) != "<Module>"
        ]

    descriptor_catalog = {}
    for rec in script_map.values():
        key = script_identity(rec)
        if key is not None:
            descriptor_catalog[key] = dict(rec)
    for dll_name in ("Assembly-CSharp.dll", "Unity.Netcode.Runtime.dll"):
        for rec in metadata_type_descriptors(managed_dir / dll_name):
            key = script_identity(rec)
            if key not in descriptor_catalog:
                descriptor_catalog[key] = rec

    script_id_index = {}
    for rec in descriptor_catalog.values():
        digest = script_id_digest(rec, script_id_convention).hex()
        script_id_index.setdefault(digest, []).append(rec)
    script_id_collisions = {
        digest: rows
        for digest, rows in script_id_index.items()
        if len({script_identity(row) for row in rows}) > 1
    }

    old_type_hash_samples = 0
    old_type_hash_matches = 0
    for obj in objects:
        if obj.type.name != "MonoBehaviour":
            continue
        old_hash = serialized_old_type_hash(obj)
        if old_hash is None:
            continue
        try:
            head = read_raw(obj)
        except Exception:
            continue
        script, direct_status = resolve(obj, head.get("m_Script"))
        if direct_status != "RESOLVED":
            continue
        rec = script_map.get((script.assets_file.name, script.path_id))
        if rec is None or not rec.get("properties_hash"):
            continue
        old_type_hash_samples += 1
        if rec["properties_hash"] == old_hash.hex():
            old_type_hash_matches += 1

    if old_type_hash_samples == 0:
        raise ValueError(
            "Could not calibrate SerializedType.old_type_hash against any resolved installed MonoScript m_PropertiesHash"
        )
    if old_type_hash_matches != old_type_hash_samples:
        raise ValueError(
            "SerializedType.old_type_hash did not validate against all comparable resolved installed MonoScript "
            f"m_PropertiesHash values: matches={old_type_hash_matches}, samples={old_type_hash_samples}"
        )

    properties_hash_index = {}
    for rec in script_map.values():
        digest = rec.get("properties_hash")
        if digest:
            properties_hash_index.setdefault(digest, []).append(rec)
    properties_hash_collisions = {
        digest: rows
        for digest, rows in properties_hash_index.items()
        if len({script_identity(row) for row in rows}) > 1
    }

    def script_descriptor(mb_obj, mb_tree=None):
        key = (mb_obj.assets_file.name, mb_obj.path_id)
        if key in descriptor_cache:
            return descriptor_cache[key]
        if mb_tree is None:
            mb_tree = read_raw(mb_obj)

        script, direct_status = resolve(mb_obj, mb_tree.get("m_Script"))
        if direct_status == "RESOLVED":
            rec = script_map.get((script.assets_file.name, script.path_id))
            if rec is not None:
                result = (rec, "RESOLVED", "OBJECT_M_SCRIPT")
                descriptor_cache[key] = result
                return result

        serialized_type = getattr(mb_obj, "serialized_type", None)
        script_type_index = -1 if serialized_type is None else getattr(serialized_type, "script_type_index", -1)
        try:
            script_type_index = int(script_type_index)
        except (TypeError, ValueError):
            script_type_index = -1
        script_types = getattr(mb_obj.assets_file, "script_types", None) or []
        if script_type_index >= 0:
            if script_type_index >= len(script_types):
                result = (None, "INVALID_SCRIPT_TYPE_INDEX", "SERIALIZED_TYPE_INDEX")
                descriptor_cache[key] = result
                return result
            script_type = script_types[script_type_index]
            ptr = {
                "m_FileID": int(script_type.local_serialized_file_index),
                "m_PathID": int(script_type.local_identifier_in_file),
            }
            script, type_status = resolve(mb_obj, ptr)
            if type_status != "RESOLVED":
                result = (None, "SCRIPT_TYPE_" + type_status, "SERIALIZED_TYPE_INDEX")
                descriptor_cache[key] = result
                return result
            rec = script_map.get((script.assets_file.name, script.path_id))
            if rec is None:
                result = (None, "SCRIPT_TYPE_RESOLVED_NOT_MONOSCRIPT", "SERIALIZED_TYPE_INDEX")
                descriptor_cache[key] = result
                return result
            result = (rec, "RESOLVED", "SERIALIZED_TYPE_INDEX")
            descriptor_cache[key] = result
            return result

        sid = serialized_script_id(mb_obj)
        if sid is not None:
            candidates = script_id_index.get(sid.hex(), [])
            unique_candidates = {}
            for rec in candidates:
                unique_candidates[script_identity(rec)] = rec
            rows = list(unique_candidates.values())
            if len(rows) == 1:
                result = (rows[0], "RESOLVED", "SERIALIZED_TYPE_SCRIPT_ID")
                descriptor_cache[key] = result
                return result
            if len(rows) > 1:
                result = (None, "AMBIGUOUS_SCRIPT_ID", "SERIALIZED_TYPE_SCRIPT_ID")
                descriptor_cache[key] = result
                return result

        old_hash = serialized_old_type_hash(mb_obj)
        if old_hash is not None:
            candidates = properties_hash_index.get(old_hash.hex(), [])
            unique_candidates = {}
            for rec in candidates:
                unique_candidates[script_identity(rec)] = rec
            rows = list(unique_candidates.values())
            if len(rows) == 1:
                result = (rows[0], "RESOLVED", "SERIALIZED_TYPE_OLD_TYPE_HASH")
                descriptor_cache[key] = result
                return result
            if len(rows) > 1:
                result = (None, "AMBIGUOUS_OLD_TYPE_HASH", "SERIALIZED_TYPE_OLD_TYPE_HASH")
                descriptor_cache[key] = result
                return result
            result = (None, "OLD_TYPE_HASH_NO_EXACT_MONOSCRIPT_MATCH", "SERIALIZED_TYPE_OLD_TYPE_HASH")
            descriptor_cache[key] = result
            return result

        result = (None, direct_status, "OBJECT_M_SCRIPT")
        descriptor_cache[key] = result
        return result

    def read(obj):
        key = (obj.assets_file.name, obj.path_id)
        if key in full_cache:
            return full_cache[key]
        if obj.type.name != "MonoBehaviour":
            tree = read_raw(obj)
            full_cache[key] = tree
            return tree

        head = read_raw(obj)
        desc, status, source = script_descriptor(obj, head)
        if status != "RESOLVED" or desc is None:
            raise ValueError(
                "Cannot recover exact MonoBehaviour identity for "
                + json.dumps({**ident(obj), "script_status": status, "script_source": source})
            )
        namespace = str(desc.get("namespace") or "")
        class_name = str(desc.get("class") or "")
        assembly = str(desc.get("assembly") or "")
        if not class_name or not assembly:
            raise ValueError("Resolved MonoScript descriptor is incomplete: " + json.dumps(desc))
        fullname = f"{namespace}.{class_name}" if namespace else class_name
        try:
            nodes = generator.get_nodes_up(assembly, fullname)
            tree = obj.read_typetree(nodes=nodes)
        except Exception as exc:
            raise ValueError(
                "Exact TypeTree recovery failed for "
                + json.dumps({
                    **ident(obj),
                    "script": desc,
                    "script_source": source,
                    "error": f"{type(exc).__name__}: {exc}",
                })
            ) from exc
        full_cache[key] = tree
        return tree

    allowed_derived_scripts = {
        (
            rec["class"],
            rec["namespace"],
            normalize_assembly(rec["assembly"]),
        )
        for rec in game_owner_proof["derived_serialized_owner_types"]
    }

    if not netcode_proof["summary"].get("network_manager_type_identity_unique"):
        raise ValueError("Netcode metadata did not prove a unique Unity.Netcode.NetworkManager TypeDef")

    def editor_identifier_identity(value):
        text = str(value or "").strip()
        if "::" not in text:
            return None
        assembly, full_type = text.split("::", 1)
        namespace, sep, class_name = full_type.rpartition(".")
        if not sep:
            namespace, class_name = "", full_type
        return class_name, namespace, normalize_assembly(assembly)

    def manager_owner_proof(desc, tree):
        ident_tuple = script_identity(desc)
        if ident_tuple == NETWORK_MANAGER_SCRIPT:
            return "EXACT_MONOSCRIPT_IDENTITY"
        if (
            desc
            and str(desc.get("class") or "") == NETWORK_MANAGER_SCRIPT[0]
            and normalize_assembly(desc.get("assembly")) == NETWORK_MANAGER_SCRIPT[2]
        ):
            return "MONOSCRIPT_CLASS_ASSEMBLY_CANONICALIZED_BY_NETCODE_METADATA"
        if ident_tuple in allowed_derived_scripts:
            return "ASSEMBLY_CSHARP_DERIVED_NETWORK_MANAGER"
        if editor_identifier_identity(tree.get("m_EditorClassIdentifier")) == NETWORK_MANAGER_SCRIPT:
            return "EXACT_EDITOR_CLASS_IDENTIFIER"
        return None

    def serialized_type_diagnostic(obj):
        st = getattr(obj, "serialized_type", None)
        if st is None:
            return None
        out = {}
        for attr in ("class_id", "script_type_index", "is_stripped_type"):
            if hasattr(st, attr):
                value = getattr(st, attr)
                if isinstance(value, (str, int, float, bool)) or value is None:
                    out[attr] = value
        for attr in ("script_id", "old_type_hash"):
            value = getattr(st, attr, None)
            raw = hash128_bytes(value)
            out[attr + "_state"] = hash128_state(value)
            if raw is not None:
                out[attr] = raw.hex()
            elif value is not None:
                out[attr + "_python_type"] = type(value).__name__
        return out

    manager_candidates = []
    structural_config_candidates = []
    unresolved_script_count = 0
    null_script_count = 0
    descriptor_source_counts = Counter()
    unresolved_serialized_type_state_counts = Counter()
    for obj in objects:
        if obj.type.name != "MonoBehaviour":
            continue
        try:
            head = read_raw(obj)
        except Exception:
            continue
        desc, status, descriptor_source = script_descriptor(obj, head)
        descriptor_source_counts[f"{descriptor_source}:{status}"] += 1
        script_ptr = head.get("m_Script")
        if is_pptr(script_ptr) and script_ptr.get("m_PathID") == 0:
            null_script_count += 1
        if status != "RESOLVED":
            unresolved_script_count += 1
            st = getattr(obj, "serialized_type", None)
            class_id = None if st is None else getattr(st, "class_id", None)
            script_type_index = None if st is None else getattr(st, "script_type_index", None)
            script_id_value = None if st is None else getattr(st, "script_id", None)
            old_type_hash_value = None if st is None else getattr(st, "old_type_hash", None)
            state_key = (
                f"class_id={class_id};script_type_index={script_type_index};"
                f"script_id={hash128_state(script_id_value)};"
                f"old_type_hash={hash128_state(old_type_hash_value)}"
            )
            unresolved_serialized_type_state_counts[state_key] += 1

        proof_kind = manager_owner_proof(desc, head)
        if not proof_kind:
            continue

        tree = read(obj)
        config_hits = [
            (path, value)
            for path, value in walk(tree)
            if path and path[-1].casefold() == "networkconfig"
        ]
        if config_hits:
            structural_config_candidates.append({
                **ident(obj),
                "script_status": status,
                "script_source": descriptor_source,
                "script": desc,
                "manager_owner_proof": proof_kind,
                "editor_class_identifier": tree.get("m_EditorClassIdentifier"),
                "serialized_type": serialized_type_diagnostic(obj),
                "top_level_fields": sorted(str(k) for k in tree.keys())[:80],
                "network_config_paths": [path_text(path) for path, _ in config_hits],
                "network_config_top_level_fields": [
                    sorted(str(k) for k in value.keys())[:80] if isinstance(value, dict) else ["<list>"]
                    for _, value in config_hits
                ],
                "network_config_hit_count": len(config_hits),
                "structured_network_config_hits": sum(
                    1 for _, value in config_hits if isinstance(value, (dict, list))
                ),
            })
        manager_candidates.append((obj, tree, desc, config_hits, status, descriptor_source, proof_kind))

    exact_manager_candidates = [
        row
        for row in manager_candidates
        if len(row[3]) == 1 and isinstance(row[3][0][1], (dict, list))
    ]
    if len(exact_manager_candidates) != 1:
        diagnostics = [
            {
                **ident(obj),
                "script": desc,
                "network_config_hit_count": len(config_hits),
                "structured_network_config_hits": sum(
                    1 for _, value in config_hits if isinstance(value, (dict, list))
                ),
            }
            for obj, _, desc, config_hits, script_status, descriptor_source, proof_kind in manager_candidates
        ]
        raise ValueError(
            "Expected exactly one serialized NetworkManager owner with one structured NetworkConfig subtree after "
            "exact SerializedType/MonoScript identity recovery; "
            f"found {len(exact_manager_candidates)} qualifying of {len(manager_candidates)} proven owner candidate(s); "
            f"unresolved MonoBehaviour identities={unresolved_script_count}; object-level null m_Script pointers={null_script_count}; "
            f"descriptor sources={json.dumps(dict(sorted(descriptor_source_counts.items())))}; "
            f"unresolved serialized type states={json.dumps(dict(sorted(unresolved_serialized_type_state_counts.items())))}; "
            f"proven candidates={json.dumps(diagnostics)}; "
            f"structural NetworkConfig candidates={json.dumps(structural_config_candidates)}"
        )

    manager_obj, manager_tree, manager_script, config_hits, manager_script_status, manager_descriptor_source, manager_proof_kind = exact_manager_candidates[0]
    if len(config_hits) != 1:
        raise ValueError(f"Expected exactly one NetworkConfig subtree on Unity.Netcode.NetworkManager, found {len(config_hits)}")
    config_path, config_tree = config_hits[0]
    if not isinstance(config_tree, (dict, list)):
        raise ValueError("NetworkConfig subtree is not structured")

    registry_edges = []
    registry_gameobjects = {}
    visited_objects = set()
    unresolved_registry = []
    prefab_field_paths = set()

    def object_has_prefab_fields(tree):
        return any(path and "prefab" in path[-1].casefold() for path, _ in walk(tree))

    def scan_prefab_tree(owner_obj, node, base_path, prefab_context=False, chain=()):
        if is_pptr(node):
            if not prefab_context:
                return
            leaf = base_path[-1].casefold() if base_path else ""
            if leaf in {"m_script", "m_gameobject", "m_prefabparentobject", "m_correspondingsourceobject"}:
                return
            target, status = resolve(owner_obj, node)
            edge = {
                "field_path": path_text(base_path),
                "source": ident(owner_obj),
                "pointer": node,
                "status": status,
                "chain": list(chain),
            }
            if target is not None:
                edge["target"] = ident(target)
            registry_edges.append(edge)
            if status == "NULL":
                return
            if status != "RESOLVED":
                unresolved_registry.append(edge)
                return
            if target.type.name == "GameObject":
                registry_gameobjects[(target.assets_file.name, target.path_id)] = {
                    "object": target,
                    "chains": [list(chain) + [path_text(base_path)]],
                }
                return
            if target.type.name == "MonoBehaviour":
                try:
                    target_head = read_raw(target)
                    desc, desc_status, desc_source = script_descriptor(target, target_head)
                    target_tree = read(target)
                except Exception as exc:
                    unresolved_registry.append({**edge, "status": "TARGET_PARSE_ERROR", "error": f"{type(exc).__name__}: {exc}"})
                    return
                edge["target_script"] = desc
                edge["target_script_status"] = desc_status
                edge["target_script_source"] = desc_source
                key = (target.assets_file.name, target.path_id)
                if key in visited_objects:
                    return
                class_name = "" if not desc else str(desc.get("class") or "")
                if "prefab" in class_name.casefold() or object_has_prefab_fields(target_tree):
                    visited_objects.add(key)
                    scan_prefab_tree(
                        target,
                        target_tree,
                        base_path + ("->" + (class_name or "MonoBehaviour"),),
                        prefab_context=True,
                        chain=chain + (path_text(base_path),),
                    )
            return

        if isinstance(node, dict):
            for key, child in node.items():
                child_context = prefab_context or ("prefab" in str(key).casefold())
                if child_context:
                    prefab_field_paths.add(path_text(base_path + (str(key),)))
                scan_prefab_tree(owner_obj, child, base_path + (str(key),), child_context, chain)
        elif isinstance(node, list):
            for i, child in enumerate(node):
                scan_prefab_tree(owner_obj, child, base_path + (f"[{i}]",), prefab_context, chain)

    scan_prefab_tree(manager_obj, config_tree, config_path)

    if unresolved_registry:
        raise ValueError("Unresolved non-null NetworkConfig prefab pointer(s): " + json.dumps(unresolved_registry[:8]))
    if not prefab_field_paths:
        raise ValueError("No prefab-related serialized field path found under Unity.Netcode.NetworkManager.NetworkConfig")
    if not registry_gameobjects:
        raise ValueError("NetworkConfig prefab traversal resolved zero GameObject candidates")

    registered = []
    exact = []
    for key, rec in sorted(registry_gameobjects.items()):
        obj = rec["object"]
        tree = read(obj)
        name = tree.get("m_Name")
        row = {**ident(obj), "name": name, "chains": rec["chains"]}
        registered.append(row)
        if name == TARGET_NAME:
            exact.append(obj)

    def component_records(go_obj):
        go_tree = read(go_obj)
        components = []
        transform_obj = None
        for idx, entry in enumerate(go_tree.get("m_Component") or []):
            ptr = entry.get("component") if isinstance(entry, dict) and "component" in entry else entry
            target, status = resolve(go_obj, ptr)
            if status != "RESOLVED":
                raise ValueError(f"Unresolved component pointer on target hierarchy: {status}")
            if target.type.name == "Transform":
                transform_obj = target
                components.append({**ident(target), "component_kind": "Transform"})
                continue
            if target.type.name != "MonoBehaviour":
                components.append({**ident(target), "component_kind": target.type.name})
                continue
            head = read_raw(target)
            desc, desc_status, desc_source = script_descriptor(target, head)
            if desc_status != "RESOLVED" or desc is None:
                raise ValueError(f"Unresolved MonoBehaviour script on target hierarchy: {desc_status}")
            tree = read(target)
            comp = {
                **ident(target),
                "component_kind": "MonoBehaviour",
                "script": desc,
                "script_source": desc_source,
            }
            if desc.get("class") == "EntranceTeleport":
                comp["entrance_fields"] = {
                    "entranceId": tree.get("entranceId"),
                    "isEntranceToBuilding": tree.get("isEntranceToBuilding"),
                }
            components.append(comp)
        if transform_obj is None:
            raise ValueError("Target GameObject has no Transform component")
        return components, transform_obj

    def child_gameobjects(transform_obj):
        tree = read(transform_obj)
        out = []
        for ptr in tree.get("m_Children") or []:
            child_transform, status = resolve(transform_obj, ptr)
            if status != "RESOLVED" or child_transform.type.name != "Transform":
                raise ValueError(f"Unresolved/non-Transform child pointer on target hierarchy: {status}")
            child_tree = read(child_transform)
            child_go, go_status = resolve(child_transform, child_tree.get("m_GameObject"))
            if go_status != "RESOLVED" or child_go.type.name != "GameObject":
                raise ValueError(f"Unresolved/non-GameObject child Transform owner: {go_status}")
            out.append(child_go)
        return out

    target_surface = None
    status = None
    if len(exact) == 0:
        status = "EXACT_NAME_NOT_REGISTERED"
    elif len(exact) > 1:
        status = "AMBIGUOUS_MULTIPLE_EXACT_MATCHES"
        target_surface = {"exact_match_count": len(exact), "matches": [ident(x) for x in exact]}
    else:
        root = exact[0]
        queue = deque([(root, "")])
        seen = set()
        hierarchy = []
        all_scripts = []
        root_scripts = []
        while queue:
            go_obj, rel = queue.popleft()
            key = (go_obj.assets_file.name, go_obj.path_id)
            if key in seen:
                raise ValueError("Cycle/duplicate GameObject encountered in target Transform hierarchy")
            seen.add(key)
            go_tree = read(go_obj)
            name = go_tree.get("m_Name")
            components, transform_obj = component_records(go_obj)
            scripts = [c["script"] for c in components if c.get("script")]
            all_scripts.extend(scripts)
            if rel == "":
                root_scripts.extend(scripts)
            hierarchy.append({
                **ident(go_obj),
                "relative_path": rel or ".",
                "name": name,
                "components": components,
            })
            for child in child_gameobjects(transform_obj):
                child_name = read(child).get("m_Name") or "<unnamed>"
                child_rel = child_name if not rel else rel + "/" + child_name
                queue.append((child, child_rel))

        def has_required(scripts, required):
            cls, ns, assembly = required
            return any(
                s.get("class") == cls
                and str(s.get("namespace") or "") == ns
                and normalize_assembly(s.get("assembly")) == assembly
                for s in scripts
            )

        root_missing = [r[0] for r in REQUIRED_SURFACE if not has_required(root_scripts, r)]
        hierarchy_missing = [r[0] for r in REQUIRED_SURFACE if not has_required(all_scripts, r)]
        target_surface = {
            "exact_match": ident(root),
            "root_required_components_missing": root_missing,
            "hierarchy_required_components_missing": hierarchy_missing,
            "root_surface_proven": not root_missing,
            "hierarchy_surface_proven": not hierarchy_missing,
            "hierarchy": hierarchy,
        }
        status = "REGISTERED_SURFACE_PROVEN" if not hierarchy_missing else "REGISTERED_SURFACE_INCOMPLETE"

    owner_kind = manager_proof_kind

    return {
        "unitypy_version": version,
        "asset_files": file_inventory,
        "serialized_file_count": len(serialized_files),
        "object_count": len(objects),
        "type_counts": dict(sorted(Counter(o.type.name for o in objects).items())),
        "script_parse_errors": script_errors,
        "network_manager": {
            **ident(manager_obj),
            "script_status": manager_script_status,
            "script_source": manager_descriptor_source,
            "script": manager_script,
            "owner_kind": owner_kind,
            "editor_class_identifier": manager_tree.get("m_EditorClassIdentifier"),
            "network_config_path": path_text(config_path),
        },
        "network_manager_owner_proof": game_owner_proof,
        "typetree_recovery": {
            "unity_version": unity_version,
            "TypeTreeGeneratorAPI": ttgen_version,
            "generator_inputs": generator_inputs,
            "descriptor_source_counts": dict(sorted(descriptor_source_counts.items())),
            "script_id_recovery": {
                "convention": script_id_convention,
                "calibration_samples": convention_samples,
                "calibration_matches": dict(sorted(convention_matches.items())),
                "catalog_type_count": len(descriptor_catalog),
                "hash_entry_count": len(script_id_index),
                "ambiguous_hash_count": len(script_id_collisions),
            },
            "old_type_hash_recovery": {
                "calibration_samples": old_type_hash_samples,
                "calibration_matches": old_type_hash_matches,
                "serialized_monoscript_hash_count": len(properties_hash_index),
                "ambiguous_hash_count": len(properties_hash_collisions),
            },
            "unresolved_serialized_type_state_counts": dict(sorted(unresolved_serialized_type_state_counts.items())),
        },
        "network_config_prefab_field_paths": sorted(prefab_field_paths),
        "network_config_prefab_edges": registry_edges,
        "registered_gameobject_count": len(registered),
        "registered_gameobjects": registered,
        "target_name": TARGET_NAME,
        "target_status": status,
        "target_surface": target_surface,
    }


def inspect_netcode(dll_path: Path):
    import dnfile
    from dncil.cil.body.reader import read_method_body_from_bytes

    versions = {
        "dnfile": importlib.metadata.version("dnfile"),
        "dncil": importlib.metadata.version("dncil"),
    }
    if versions != {"dnfile": DNFILE_VERSION, "dncil": DNCIL_VERSION}:
        raise ValueError(f"Managed parser version mismatch: {versions}")

    pe = dnfile.dnPE(str(dll_path))
    if pe.net is None or pe.net.mdtables is None:
        raise ValueError("Unity.Netcode.Runtime.dll is not a readable managed assembly")

    nested = {id(row.NestedClass.row): row.EnclosingClass.row for row in (pe.net.mdtables.NestedClass or [])}

    def defined_type_name(row):
        name, ns = str(row.TypeName), str(row.TypeNamespace)
        own = f"{ns}.{name}" if ns else name
        return defined_type_name(nested[id(row)]) + "+" + name if id(row) in nested else own

    method_owners = {}
    field_owners = {}
    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        method_owners.update({id(m.row): owner for m in t.MethodList})
        field_owners.update({id(f.row): owner for f in t.FieldList})

    def type_name(row):
        if hasattr(row, "TypeName"):
            ns, name = str(row.TypeNamespace), str(row.TypeName)
            return f"{ns}.{name}" if ns else name
        if hasattr(row, "Signature"):
            return "TypeSpec[" + row.Signature.value.hex() + "]"
        return type(row).__name__

    tables = {1: "TypeRef", 2: "TypeDef", 4: "Field", 6: "MethodDef", 10: "MemberRef", 27: "TypeSpec", 43: "MethodSpec"}

    def resolve_token(token):
        table_id = token >> 24
        idx = token & 0xFFFFFF
        if table_id == 0x70:
            entry = pe.net.user_strings.get(idx)
            return repr(entry.value) if entry is not None else f"user_string(0x{idx:x})"
        table_name = tables.get(table_id)
        if not table_name:
            return f"token(0x{token:08x})"
        table = getattr(pe.net.mdtables, table_name)
        if idx <= 0 or idx > len(table.rows):
            return f"invalid_token(0x{token:08x})"
        row = table.rows[idx - 1]
        if table_id == 43:
            inner = (row.Method.table.number << 24) | row.Method.row_index
            return "MethodSpec(" + resolve_token(inner) + "; " + row.Instantiation.value.hex() + ")"
        if table_id in (1, 2, 27):
            return type_name(row)
        if table_id == 6:
            return method_owners[id(row)] + "::" + str(row.Name)
        if table_id == 4:
            return field_owners[id(row)] + "::" + str(row.Name)
        return type_name(row.Class.row) + "::" + str(row.Name)

    assembly_rows = pe.net.mdtables.Assembly or []
    if not assembly_rows:
        raise ValueError("Netcode assembly has no Assembly row")
    a = assembly_rows.rows[0]
    assembly = {
        "name": str(a.Name),
        "version": f"{a.MajorVersion}.{a.MinorVersion}.{a.BuildNumber}.{a.RevisionNumber}",
    }
    if assembly["name"] != "Unity.Netcode.Runtime":
        raise ValueError("Unexpected Netcode assembly identity: " + assembly["name"])

    core_types = {
        "Unity.Netcode.NetworkConfig",
        "Unity.Netcode.NetworkPrefabs",
        "Unity.Netcode.NetworkPrefab",
        "Unity.Netcode.NetworkPrefabsList",
        "Unity.Netcode.NetworkManager",
    }
    type_rows = {defined_type_name(t): t for t in pe.net.mdtables.TypeDef}
    manager_named_types = sorted(
        name for name in type_rows if name.rsplit(".", 1)[-1] == "NetworkManager"
    )
    if manager_named_types != [NETWORK_MANAGER_FULL_NAME]:
        raise ValueError(
            "Expected exactly one NetworkManager TypeDef identity in Netcode metadata: "
            + json.dumps(manager_named_types)
        )
    for required in ("Unity.Netcode.NetworkConfig", "Unity.Netcode.NetworkPrefabs", "Unity.Netcode.NetworkPrefab"):
        if required not in type_rows:
            raise ValueError("Required Netcode type missing: " + required)

    fields = []
    for name in sorted(core_types & set(type_rows)):
        t = type_rows[name]
        for fr in t.FieldList:
            fields.append({
                "type": name,
                "field": str(fr.row.Name),
                "signature_hex": fr.row.Signature.value.hex(),
            })
    if not any(x["type"] == "Unity.Netcode.NetworkManager" and x["field"] == "NetworkConfig" for x in fields):
        raise ValueError("Exact Netcode NetworkManager.NetworkConfig field missing")
    if not any(x["type"] == "Unity.Netcode.NetworkPrefabs" and x["field"] == "m_Prefabs" for x in fields):
        raise ValueError("Exact Netcode NetworkPrefabs.m_Prefabs field missing")

    signals = ("m_Prefabs", "NetworkPrefabsList", "NetworkPrefab", "PrefabList", "AddNetworkPrefab", "Prefabs")
    methods = []
    parse_errors = []
    for name in sorted(core_types & set(type_rows)):
        t = type_rows[name]
        for mr in t.MethodList:
            m = mr.row
            if not m.Rva:
                continue
            try:
                body = read_method_body_from_bytes(pe.get_data(m.Rva, 250000))
            except Exception as exc:
                parse_errors.append({"type": name, "method": str(m.Name), "error": f"{type(exc).__name__}: {exc}"})
                continue
            instructions = []
            resolved_values = []
            for ins in body.instructions:
                operand = ins.operand
                value = operand.value if hasattr(operand, "value") else None
                resolved = resolve_token(value) if isinstance(value, int) else None
                if resolved is not None:
                    resolved_values.append(resolved)
                instructions.append({
                    "offset": ins.offset,
                    "opcode": ins.opcode.name,
                    "operand": None if operand is None else str(operand),
                    "resolved": resolved,
                })
            blob = "\n".join(resolved_values) + "\n" + str(m.Name)
            if any(s in blob for s in signals):
                methods.append({
                    "type": name,
                    "method": str(m.Name),
                    "token": f"0x{0x06000000 | mr.row_index:08x}",
                    "rva": int(m.Rva),
                    "signature_hex": m.Signature.value.hex(),
                    "resolved_references": resolved_values,
                    "instructions": instructions,
                })
    if parse_errors:
        raise ValueError("Netcode core-type IL parse errors: " + json.dumps(parse_errors))
    if not methods:
        raise ValueError("No focused Netcode prefab-registration IL methods found")
    if sum(len(m["instructions"]) for m in methods) > 20000:
        raise ValueError("Focused Netcode IL exceeds 20,000 instructions")

    return {
        "dll_bytes": dll_path.stat().st_size,
        "dll_sha256": sha256_file(dll_path),
        "assembly": assembly,
        "field_inventory": fields,
        "focused_methods": methods,
        "summary": {
            "core_types_present": sorted(core_types & set(type_rows)),
            "focused_method_count": len(methods),
            "focused_instruction_count": sum(len(m["instructions"]) for m in methods),
            "network_manager_network_config_field_present": True,
            "network_manager_type_identity_unique": True,
            "network_manager_type_identity": NETWORK_MANAGER_FULL_NAME,
            "m_prefabs_field_present": True,
            "parse_errors": 0,
        },
    }


def self_test():
    assert normalize_assembly("Assembly-CSharp.dll") == "assembly-csharp"
    assert normalize_assembly("Unity.Netcode.Runtime") == "unity.netcode.runtime"
    assert is_pptr({"m_FileID": 0, "m_PathID": 1})
    tree = {"NetworkConfig": {"NetworkPrefabsLists": [{"m_FileID": 0, "m_PathID": 7}]}}
    paths = [path_text(p) for p, _ in walk(tree) if p and "prefab" in p[-1].casefold()]
    assert "NetworkConfig.NetworkPrefabsLists" in paths
    required = {(x[0], x[1], x[2]) for x in REQUIRED_SURFACE}
    assert ("EntranceTeleport", "", "assembly-csharp") in required
    assert TARGET_NAME == "EntranceTeleportB"
    assert NETWORK_MANAGER_SCRIPT == ("NetworkManager", "Unity.Netcode", "unity.netcode.runtime")
    assert script_identity({"class": "GameNetworkManager", "namespace": "", "assembly": "Assembly-CSharp.dll"}) == (
        "GameNetworkManager", "", "assembly-csharp"
    )
    assert normalize_assembly("Unity.Netcode.Runtime.dll") == "unity.netcode.runtime"
    assert md4_digest(b"").hex() == "31d6cfe0d16ae931b73c59d7e0c089c0"
    assert md4_digest(b"abc").hex() == "a448017aaf21d8525fc10ae87aa6729d"
    assert hash128_bytes({"bytes[%d]" % i: i for i in range(16)}) == bytes(range(16))
    assert hash128_bytes(memoryview(bytes(range(16)))) == bytes(range(16))
    assert hash128_state(memoryview(bytes(16))) == "ZERO"
    assert hash128_state(memoryview(bytes(range(16)))) == "NONZERO"
    sample = {"assembly": "Assembly-CSharp.dll", "namespace": "", "class": "EntranceTeleport"}
    expected_script_id = md4_digest(b"EntranceTeleportAssembly-CSharp.dll")
    assert script_id_digest(sample, "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL") == expected_script_id
    assert script_id_digest(sample, "CLASS_NAMESPACE_MONOSCRIPT_ASSEMBLY_LITERAL") != script_id_digest(
        sample, "CLASS_NAMESPACE_ASSEMBLY_NO_DLL"
    )
    assert importlib.metadata.version("TypeTreeGeneratorAPI") == TTGEN_VERSION
    print("V81 NetworkConfig EntranceTeleportB scanner self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-root", type=Path)
    p.add_argument("--netcode-dll", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.data_root or not args.data_root.is_dir():
        raise ValueError("--data-root must be the exact installed Lethal Company_Data directory")
    if not args.netcode_dll or not args.netcode_dll.is_file():
        raise ValueError("--netcode-dll must be the exact installed Unity.Netcode.Runtime.dll")
    if not args.out:
        raise ValueError("--out is required")

    result = {
        "schema_version": "v81-networkconfig-entranceteleportb-7",
        "target_name": TARGET_NAME,
        "proof_boundary": (
            "Static installed-V81 base-game serialized assets plus exact installed Assembly-CSharp.dll and "
            "Unity.Netcode.Runtime.dll metadata only. Managed code is never loaded or executed. Stripped/null object-level "
            "m_Script references may be recovered through the serialized file's exact SerializedType script_type_index "
            "to MonoScript mapping or, when that index is absent, through the SerializedType 128-bit script_id matched "
            "against exact installed managed TypeDefs. Unity serialized script_id recovery uses MD4(className + namespace + "
            "assemblyName); the exact assembly-name convention must first validate against all comparable resolved installed "
            "MonoScript references. When script_id is null, SerializedType.old_type_hash may be matched only to a unique "
            "MonoScript.m_PropertiesHash after that relation validates against every comparable resolved installed reference. "
            "Missing TypeTrees are generated statically from those exact installed assemblies. "
            "GameObject name alone is never registration proof; the target must be reached from the proven serialized "
            "Unity.Netcode.NetworkManager.NetworkConfig prefab-list path."
        ),
        "toolchain": {
            "python": sys.version.split()[0],
            "UnityPy": importlib.metadata.version("UnityPy"),
            "dnfile": importlib.metadata.version("dnfile"),
            "dncil": importlib.metadata.version("dncil"),
            "TypeTreeGeneratorAPI": importlib.metadata.version("TypeTreeGeneratorAPI"),
        },
        "netcode": None,
        "assets": None,
    }
    netcode_result = inspect_netcode(args.netcode_dll)
    game_owner_proof = inspect_game_network_manager_inheritance(
        args.data_root / "Managed" / "Assembly-CSharp.dll"
    )
    result["netcode"] = netcode_result
    result["assets"] = inspect_assets(args.data_root, game_owner_proof, netcode_result)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "target_status": result["assets"]["target_status"],
        "registered_gameobject_count": result["assets"]["registered_gameobject_count"],
        "netcode_dll_sha256": result["netcode"]["dll_sha256"],
        "netcode_focused_methods": result["netcode"]["summary"]["focused_method_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
