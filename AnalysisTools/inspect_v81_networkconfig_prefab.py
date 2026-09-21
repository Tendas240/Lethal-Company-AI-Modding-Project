#!/usr/bin/env python3
"""Fail-closed static V81 NetworkConfig prefab capture for EntranceTeleportB.

This helper never starts Unity or managed game/mod code. It parses only the exact
installed base-game serialized assets plus Unity.Netcode.Runtime.dll supplied by
its PowerShell wrapper. Output is compact JSON suitable for repository evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

UNITYPY_VERSION = "1.25.3"
DNFILE_VERSION = "0.18.0"
DNCIL_VERSION = "1.0.2"
TARGET_NAME = "EntranceTeleportB"
NETWORK_MANAGER_SCRIPT = ("NetworkManager", "Unity.Netcode", "unity.netcode.runtime")
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


def normalize_assembly(value) -> str:
    text = "" if value is None else str(value).strip().lower()
    return text[:-4] if text.endswith(".dll") else text


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


def inspect_assets(data_root: Path):
    import UnityPy

    version = importlib.metadata.version("UnityPy")
    if version != UNITYPY_VERSION:
        raise ValueError(f"Expected UnityPy {UNITYPY_VERSION}, got {version}")

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

    by_id = {(o.assets_file.name, o.path_id): o for o in objects}
    cache = {}

    def ident(obj):
        return {
            "serialized_file": obj.assets_file.name,
            "path_id": obj.path_id,
            "type": obj.type.name,
        }

    def read(obj):
        key = (obj.assets_file.name, obj.path_id)
        if key not in cache:
            cache[key] = obj.read_typetree()
        return cache[key]

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
            tree = read(obj)
        except Exception as exc:
            script_errors.append({**ident(obj), "error": f"{type(exc).__name__}: {exc}"})
            continue
        script_map[(obj.assets_file.name, obj.path_id)] = {
            **ident(obj),
            "class": tree.get("m_ClassName"),
            "namespace": tree.get("m_Namespace"),
            "assembly": tree.get("m_AssemblyName"),
        }

    def script_descriptor(mb_obj, mb_tree):
        script, status = resolve(mb_obj, mb_tree.get("m_Script"))
        if status == "NULL":
            return None, status
        if status != "RESOLVED":
            return None, status
        rec = script_map.get((script.assets_file.name, script.path_id))
        return (rec, "RESOLVED") if rec else (None, "RESOLVED_NOT_MONOSCRIPT")

    manager_candidates = []
    unresolved_script_count = 0
    for obj in objects:
        if obj.type.name != "MonoBehaviour":
            continue
        try:
            tree = read(obj)
        except Exception:
            continue
        desc, status = script_descriptor(obj, tree)
        if status not in ("RESOLVED", "NULL"):
            unresolved_script_count += 1
        if not desc:
            continue
        if (
            desc.get("class") == NETWORK_MANAGER_SCRIPT[0]
            and str(desc.get("namespace") or "") == NETWORK_MANAGER_SCRIPT[1]
            and normalize_assembly(desc.get("assembly")) == NETWORK_MANAGER_SCRIPT[2]
        ):
            config_hits = [
                (path, value)
                for path, value in walk(tree)
                if path and path[-1].casefold() == "networkconfig"
            ]
            manager_candidates.append((obj, tree, desc, config_hits))

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
            for obj, _, desc, config_hits in manager_candidates
        ]
        raise ValueError(
            "Expected exactly one exact serialized Unity.Netcode.NetworkManager with one structured NetworkConfig subtree, "
            f"found {len(exact_manager_candidates)} qualifying of {len(manager_candidates)} exact script candidate(s); "
            f"unresolved non-null script pointers={unresolved_script_count}; candidates={json.dumps(diagnostics)}"
        )

    manager_obj, manager_tree, manager_script, config_hits = exact_manager_candidates[0]
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
                    target_tree = read(target)
                except Exception as exc:
                    unresolved_registry.append({**edge, "status": "TARGET_PARSE_ERROR", "error": f"{type(exc).__name__}: {exc}"})
                    return
                desc, desc_status = script_descriptor(target, target_tree)
                edge["target_script"] = desc
                edge["target_script_status"] = desc_status
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
            tree = read(target)
            desc, desc_status = script_descriptor(target, tree)
            if desc_status != "RESOLVED" or desc is None:
                raise ValueError(f"Unresolved MonoBehaviour script on target hierarchy: {desc_status}")
            comp = {
                **ident(target),
                "component_kind": "MonoBehaviour",
                "script": desc,
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

    return {
        "unitypy_version": version,
        "asset_files": file_inventory,
        "serialized_file_count": len(serialized_files),
        "object_count": len(objects),
        "type_counts": dict(sorted(Counter(o.type.name for o in objects).items())),
        "script_parse_errors": script_errors,
        "network_manager": {**ident(manager_obj), "script": manager_script, "network_config_path": path_text(config_path)},
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
        "schema_version": "v81-networkconfig-entranceteleportb-2",
        "target_name": TARGET_NAME,
        "proof_boundary": (
            "Static installed-V81 base-game asset plus Unity.Netcode.Runtime.dll evidence only. "
            "No game/mod assembly is loaded or executed. GameObject name alone is never treated as registration proof; "
            "the target must be reached from the exact serialized Unity.Netcode.NetworkManager.NetworkConfig prefab path."
        ),
        "toolchain": {
            "python": sys.version.split()[0],
            "UnityPy": importlib.metadata.version("UnityPy"),
            "dnfile": importlib.metadata.version("dnfile"),
            "dncil": importlib.metadata.version("dncil"),
        },
        "netcode": inspect_netcode(args.netcode_dll),
        "assets": inspect_assets(args.data_root),
    }
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
