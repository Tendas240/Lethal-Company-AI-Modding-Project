#!/usr/bin/env python3
"""Fail-closed static capture for Black Mesa 3.4.4 Thunderstore package.

This helper never executes Unity, the game, or managed mod assemblies. It inventories
the exact downloaded ZIP, hashes DLL/UnityFS members, and statically scans serialized
Unity objects with UnityPy==1.25.3 for Dawn/Dusk moon-definition, scene and
EntranceTeleport evidence.

Usage:
  python inspect_universal_interior_c3f2.py --zip PACKAGE.zip --out OUTPUT --source-url URL
  python inspect_universal_interior_c3f2.py --self-test
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

PACKAGE_KEY = "Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior"
PACKAGE_VERSION = "3.4.4"
EXPECTED_SOURCE_URL = (
    "https://gcdn.thunderstore.io/live/repository/packages/"
    "Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior-3.4.4.zip"
)
UNITYPY_VERSION = "1.25.3"
ENTRANCE_FIELDS = {"entranceId", "isEntranceToBuilding", "entrancePoint", "exitPoint"}
DEFINITION_CLASS_RE = re.compile(r"(?:Dusk|Dawn)?.*MoonDefinition|MoonDefinition", re.I)
NAME_SIGNAL_RE = re.compile(r"black\s*mesa|entrance|fire.?exit|teleport|dungeon", re.I)
BLACK_MESA_RE = re.compile(r"black\s*mesa", re.I)
BLOCK = 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(BLOCK), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_member_name(name: str) -> str:
    if not name or "\\" in name or name.startswith("/"):
        raise ValueError("Unsafe ZIP member path: " + repr(name))
    p = PurePosixPath(name)
    if any(part in ("", ".", "..") for part in p.parts):
        raise ValueError("Unsafe ZIP member path: " + repr(name))
    return str(p)


def hash_member(archive: zipfile.ZipFile, info: zipfile.ZipInfo):
    h = hashlib.sha256()
    first = b""
    with archive.open(info, "r") as f:
        while True:
            chunk = f.read(BLOCK)
            if not chunk:
                break
            if not first:
                first = chunk[:16]
            h.update(chunk)
    return h.hexdigest(), first


def recursive_field_hits(value, wanted, prefix=""):
    hits = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = prefix + "." + key if prefix else key
            if key in wanted:
                hits.append({"field_path": path, "value": item})
            hits.extend(recursive_field_hits(item, wanted, path))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            hits.extend(recursive_field_hits(item, wanted, f"{prefix}[{i}]"))
    return hits


def recursive_strings(value, prefix=""):
    out = []
    if isinstance(value, str):
        out.append({"field_path": prefix, "value": value})
    elif isinstance(value, dict):
        for key, item in value.items():
            path = prefix + "." + key if prefix else key
            out.extend(recursive_strings(item, path))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            out.extend(recursive_strings(item, f"{prefix}[{i}]"))
    return out


def validate_manifest(data):
    if not isinstance(data, dict):
        raise ValueError("manifest.json must be a JSON object")
    if data.get("version_number") != PACKAGE_VERSION:
        raise ValueError(
            f"manifest version mismatch: expected {PACKAGE_VERSION}, got {data.get('version_number')!r}"
        )
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        raise ValueError("manifest name missing")
    return data


def self_test():
    assert safe_member_name("plugins/BlackMesa/file.dll") == "plugins/BlackMesa/file.dll"
    for bad in ("../x", "/x", "a\\b"):
        try:
            safe_member_name(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("unsafe path accepted: " + bad)
    validate_manifest({"name": "x", "version_number": PACKAGE_VERSION})
    try:
        validate_manifest({"name": "x", "version_number": "0.0.0"})
    except ValueError:
        pass
    else:
        raise AssertionError("wrong version accepted")
    tree = {"x": [{"entranceId": 2}], "nested": {"isEntranceToBuilding": False}}
    hits = recursive_field_hits(tree, ENTRANCE_FIELDS)
    assert {h["field_path"] for h in hits} == {"x[0].entranceId", "nested.isEntranceToBuilding"}
    print("C3F2 self-test passed")


def inspect_bundle(member_name, data, UnityPy):
    env = UnityPy.load(data)
    objects = list(env.objects)
    files = {}
    duplicate_files = []
    for obj in objects:
        name = obj.assets_file.name
        prior = files.get(name)
        if prior is not None and id(prior) != id(obj.assets_file):
            duplicate_files.append(name)
        files[name] = obj.assets_file
    if duplicate_files:
        raise ValueError("Ambiguous serialized-file names: " + ", ".join(sorted(set(duplicate_files))))

    by_id = {(o.assets_file.name, o.path_id): o for o in objects}
    cache = {}

    def identity(o):
        return {"serialized_file": o.assets_file.name, "path_id": o.path_id, "type": o.type.name}

    def read(o):
        key = (o.assets_file.name, o.path_id)
        if key not in cache:
            cache[key] = o.read_typetree()
        return cache[key]

    def resolve(owner, ptr):
        if not isinstance(ptr, dict) or "m_PathID" not in ptr or "m_FileID" not in ptr:
            return None, "MALFORMED_POINTER"
        if ptr["m_PathID"] == 0:
            return None, "NULL"
        fid = ptr["m_FileID"]
        if fid == 0:
            filename = owner.assets_file.name
        else:
            if fid < 1 or fid > len(owner.assets_file.externals):
                return None, "INVALID_EXTERNAL_INDEX"
            ext = str(owner.assets_file.externals[fid - 1].path)
            filename = ext.replace("\\", "/").rsplit("/", 1)[-1]
            if filename not in files:
                return None, "EXTERNAL_NOT_IN_BUNDLE:" + ext
        target = by_id.get((filename, ptr["m_PathID"]))
        return (target, "RESOLVED") if target else (None, "PATH_ID_NOT_FOUND:" + filename)

    scripts = []
    script_map = {}
    parse_errors = []
    for obj in objects:
        if obj.type.name != "MonoScript":
            continue
        try:
            tree = read(obj)
        except Exception as exc:
            parse_errors.append({**identity(obj), "stage": "MonoScript", "error_type": type(exc).__name__, "error": str(exc)})
            continue
        rec = {
            **identity(obj),
            "class": tree.get("m_ClassName"),
            "namespace": tree.get("m_Namespace"),
            "assembly": tree.get("m_AssemblyName"),
        }
        scripts.append(rec)
        script_map[(obj.assets_file.name, obj.path_id)] = rec

    entrance_matches = []
    definition_candidates = []
    script_status = Counter()
    mb_total = 0
    mb_parsed = 0
    unresolved_script_records = []
    for obj in objects:
        if obj.type.name != "MonoBehaviour":
            continue
        mb_total += 1
        try:
            tree = read(obj)
        except Exception as exc:
            parse_errors.append({**identity(obj), "stage": "MonoBehaviour", "error_type": type(exc).__name__, "error": str(exc)})
            continue
        mb_parsed += 1
        script, status = resolve(obj, tree.get("m_Script"))
        descriptor = script_map.get((script.assets_file.name, script.path_id)) if script else None
        if status == "RESOLVED" and descriptor is None:
            status = "RESOLVED_NOT_MONOSCRIPT"
        script_status[status] += 1
        if status not in ("RESOLVED", "NULL"):
            unresolved_script_records.append({
                **identity(obj), "status": status, "m_Script": tree.get("m_Script"),
                "raw_object_sha256": hashlib.sha256(obj.get_raw_data()).hexdigest(),
                "raw_object_bytes": obj.byte_size,
            })

        entrance_hits = recursive_field_hits(tree, ENTRANCE_FIELDS)
        exact_entrance = bool(descriptor and descriptor.get("class") == "EntranceTeleport")
        if exact_entrance or entrance_hits:
            entrance_matches.append({
                **identity(obj),
                "script": descriptor,
                "exact_entrance_class": exact_entrance,
                "field_hits": entrance_hits,
                "serialized_fields": tree,
            })

        strings = recursive_strings(tree)
        black_strings = [s for s in strings if BLACK_MESA_RE.search(s["value"])]
        class_name = descriptor.get("class") if descriptor else None
        if (class_name and DEFINITION_CLASS_RE.search(class_name)) or black_strings:
            definition_candidates.append({
                **identity(obj),
                "script": descriptor,
                "black_mesa_string_hits": black_strings,
                "serialized_fields": tree,
            })

    go_total = 0
    go_parse_errors = []
    go_name_matches = []
    for obj in objects:
        if obj.type.name != "GameObject":
            continue
        go_total += 1
        try:
            tree = read(obj)
        except Exception as exc:
            go_parse_errors.append({**identity(obj), "error_type": type(exc).__name__, "error": str(exc)})
            continue
        name = tree.get("m_Name", "")
        if isinstance(name, str) and NAME_SIGNAL_RE.search(name):
            go_name_matches.append({**identity(obj), "name": name, "active_self": tree.get("m_IsActive")})

    serialized_files = [
        {
            "name": asset.name,
            "unity_version": asset.unity_version,
            "externals": [str(x.path) for x in asset.externals],
            "type_tree_enabled": asset._enable_type_tree,
            "object_count": len(asset.objects),
        }
        for asset in files.values()
    ]
    fatal_ambiguities = []
    if parse_errors:
        fatal_ambiguities.append(f"{len(parse_errors)} MonoScript/MonoBehaviour parse errors")
    if go_parse_errors:
        fatal_ambiguities.append(f"{len(go_parse_errors)} GameObject parse errors")
    if unresolved_script_records:
        fatal_ambiguities.append(f"{len(unresolved_script_records)} unresolved non-null script pointers")

    return {
        "member": member_name,
        "object_count": len(objects),
        "type_counts": dict(sorted(Counter(o.type.name for o in objects).items())),
        "serialized_files": serialized_files,
        "coverage": {
            "monoscripts": len(scripts),
            "monobehaviours_total": mb_total,
            "monobehaviours_parsed": mb_parsed,
            "gameobjects_total": go_total,
            "script_pointer_status_counts": dict(script_status),
        },
        "monoscript_inventory": scripts,
        "entrance_class_or_field_matches": entrance_matches,
        "black_mesa_or_moon_definition_candidates": definition_candidates,
        "gameobject_name_matches": go_name_matches,
        "parse_errors": parse_errors,
        "gameobject_parse_errors": go_parse_errors,
        "unresolved_script_records": unresolved_script_records,
        "fatal_ambiguities": fatal_ambiguities,
    }


def capture(args):
    if args.source_url != EXPECTED_SOURCE_URL:
        raise ValueError("Unexpected package source URL; refusing capture")
    if not args.zip.is_file():
        raise FileNotFoundError(args.zip)

    import UnityPy
    version = importlib.metadata.version("UnityPy")
    if version != UNITYPY_VERSION:
        raise ValueError(f"Expected UnityPy {UNITYPY_VERSION}, got {version}")

    args.out.mkdir(parents=True, exist_ok=True)
    zip_sha = sha256_file(args.zip)
    zip_bytes = args.zip.stat().st_size
    inventory = []
    dlls = []
    bundle_members = []
    manifest = None
    seen_casefold = {}

    with zipfile.ZipFile(args.zip) as archive:
        infos = archive.infolist()
        for info in infos:
            name = safe_member_name(info.filename.rstrip("/")) if info.filename.endswith("/") else safe_member_name(info.filename)
            folded = name.casefold()
            if folded in seen_casefold:
                raise ValueError(f"Duplicate/case-colliding ZIP member: {name} vs {seen_casefold[folded]}")
            seen_casefold[folded] = name
            if info.flag_bits & 1:
                raise ValueError("Encrypted ZIP member not allowed: " + name)
            if info.is_dir():
                inventory.append({"member": name + "/", "directory": True})
                continue
            digest, prefix = hash_member(archive, info)
            unityfs = prefix.startswith(b"UnityFS\x00")
            rec = {
                "member": name,
                "bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "sha256": digest,
                "unityfs": unityfs,
            }
            inventory.append(rec)
            if name == "manifest.json":
                if manifest is not None:
                    raise ValueError("Multiple root manifest.json entries")
                manifest = validate_manifest(json.loads(archive.read(info).decode("utf-8-sig")))
            if name.lower().endswith(".dll"):
                dlls.append(rec.copy())
            if unityfs:
                bundle_members.append(rec.copy())

        if manifest is None:
            raise ValueError("Root manifest.json missing")
        if not dlls:
            raise ValueError("Unexpected package layout: no DLL members")
        if not bundle_members:
            raise ValueError("Unexpected package layout: no UnityFS members")

        bundle_reports = []
        for rec in bundle_members:
            data = archive.read(rec["member"])
            actual = hashlib.sha256(data).hexdigest()
            if actual != rec["sha256"] or len(data) != rec["bytes"]:
                raise ValueError("Bundle byte/hash changed during capture: " + rec["member"])
            try:
                report = inspect_bundle(rec["member"], data, UnityPy)
            except Exception as exc:
                report = {
                    "member": rec["member"],
                    "fatal_ambiguities": [f"bundle parse failure: {type(exc).__name__}: {exc}"],
                }
            bundle_reports.append(report)

    definitions = []
    entrances = []
    scene_signals = []
    fatal = []
    for report in bundle_reports:
        definitions.extend(
            [{"bundle_member": report["member"], **x}
             for x in report.get("black_mesa_or_moon_definition_candidates", [])]
        )
        entrances.extend(
            [{"bundle_member": report["member"], **x}
             for x in report.get("entrance_class_or_field_matches", [])]
        )
        if any(BLACK_MESA_RE.search(f.get("name", "")) for f in report.get("serialized_files", [])):
            scene_signals.append({"bundle_member": report["member"], "reason": "serialized_file_name"})
        if report.get("gameobject_name_matches"):
            scene_signals.append({"bundle_member": report["member"], "reason": "gameobject_name_signal"})
        fatal.extend([f"{report['member']}: {x}" for x in report.get("fatal_ambiguities", [])])

    if not definitions:
        fatal.append("No Black-Mesa or MoonDefinition serialized candidate found; package layout/definition mapping is unresolved")
    if not scene_signals and not entrances:
        fatal.append("No scene/entrance serialization signal found; scene-bundle mapping is unresolved")

    result = {
        "schema_version": "phase-c3f2-capture-1",
        "package": {
            "namespace": PACKAGE_KEY,
            "version": PACKAGE_VERSION,
            "source_url": args.source_url,
            "zip_bytes": zip_bytes,
            "zip_sha256": zip_sha,
            "manifest": manifest,
        },
        "toolchain": {"python": sys.version.split()[0], "unitypy": version},
        "archive_inventory": inventory,
        "implementation_dlls": dlls,
        "unityfs_bundles": bundle_members,
        "bundle_reports": bundle_reports,
        "summary": {
            "archive_members": len(inventory),
            "dll_members": len(dlls),
            "unityfs_members": len(bundle_members),
            "definition_candidates": len(definitions),
            "entrance_class_or_field_matches": len(entrances),
            "scene_signal_bundles": scene_signals,
            "fatal_ambiguities": fatal,
            "status": "CAPTURE_COMPLETE_FAIL_CLOSED_AMBIGUITY" if fatal else "CAPTURE_COMPLETE_STATIC_SURFACE_RESOLVED",
        },
        "proof_boundary": (
            "Static package serialization only. No Unity/game/mod managed code executes. "
            "Absence of serialized EntranceTeleport fields is not proof of zero runtime entrances; "
            "generation, traversal, routing, NavMesh and arbitrary-interior compatibility remain unproven."
        ),
    }
    output = args.out / "BLACK_MESA_344_PACKAGE_TOPOLOGY_CAPTURE.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    if fatal:
        raise RuntimeError("Fail-closed capture ambiguity: " + "; ".join(fatal))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--source-url")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if args.zip is None or args.out is None or args.source_url is None:
        p.error("--zip, --out and --source-url are required unless --self-test is used")
    try:
        capture(args)
    except Exception as exc:
        args.out.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema_version": "phase-c3f2-capture-failure-1",
            "package": PACKAGE_KEY,
            "version": PACKAGE_VERSION,
            "source_url": args.source_url,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "fail_closed": True,
        }
        (args.out / "CAPTURE_FAILURE.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
