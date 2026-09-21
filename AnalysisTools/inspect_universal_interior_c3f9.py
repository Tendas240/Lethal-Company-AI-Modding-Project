#!/usr/bin/env python3
"""C3F9A static gap probe for the six unresolved C3F8 fire-exit surfaces.

Uses the exact C3F7 package lock/acquisition path and UnityPy 1.25.3. It does not
execute Unity, game binaries, or managed mod code. The probe is deliberately
bounded to BackroomsFlow, SHFlow, CircusFacilityFlow, SpookyManorFlow,
CastleFlow and StorageComplex.
"""
import argparse
from collections import defaultdict
import gc
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import zipfile

import inspect_universal_interior_c3f7 as c7

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F9"
LOCK = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F7/PACKAGE_LOCK.json"
TARGETS = {
    "Generic_GMD-Generic_Interiors": ["BackroomsFlow", "SHFlow"],
    "LethalMatt-Bozoros": ["CircusFacilityFlow"],
    "Magic_Wesley-WesleysInteriors": ["SpookyManorFlow"],
    "Tolian-Scoopy_Castle": ["CastleFlow"],
    "Beaniebe-Storage_Complex": ["StorageComplex"],
}
EXPECTED_RESULTS = {
    "BackroomsFlow": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
    "SHFlow": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
    "CircusFacilityFlow": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
    "SpookyManorFlow": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
    "CastleFlow": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
    "StorageComplex": "PROP_PRESENT_TEMPLATE_UNRESOLVED",
}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(c7.json_safe(data), indent=2, allow_nan=False) + "\n", encoding="utf-8")


def key_of(desc):
    return (desc["bundle_member"], desc["serialized_file"], desc["path_id"])


def describe(idx, key):
    rec = idx.descriptor(key)
    if idx.objects[key]["type"] == "GameObject":
        rec["name"] = idx.objects[key]["tree"].get("m_Name")
    return rec


def transform_for_go(idx, go):
    tree = idx.objects[go]["tree"]
    comps = tree.get("m_Component")
    if not isinstance(comps, list):
        raise c7.CaptureError("GameObject component table missing during ancestry probe")
    found = []
    for entry in comps:
        comp = idx.resolve(go, entry.get("component"), required=True)
        if idx.objects[comp]["type"] in ("Transform", "RectTransform"):
            found.append(comp)
    if len(found) != 1:
        raise c7.CaptureError("Expected exactly one Transform during ancestry probe")
    return found[0]


def ancestry(idx, go):
    chain = []
    seen = set()
    current = go
    while True:
        if current in seen:
            raise c7.CaptureError("Cycle in candidate parent ancestry")
        seen.add(current)
        tr = transform_for_go(idx, current)
        tt = idx.objects[tr]["tree"]
        parent_tr = idx.resolve(tr, tt.get("m_Father"), expected={"Transform", "RectTransform"})
        edge = {
            "gameobject": describe(idx, current),
            "transform": idx.descriptor(tr),
            "parent_lists_child": None,
        }
        chain.append(edge)
        if parent_tr is None:
            break
        parent_go = idx.resolve(
            parent_tr,
            idx.objects[parent_tr]["tree"].get("m_GameObject"),
            required=True,
            expected={"GameObject"},
        )
        children = idx.objects[parent_tr]["tree"].get("m_Children")
        if not isinstance(children, list):
            raise c7.CaptureError("Parent Transform children table missing")
        resolved_children = [idx.resolve(parent_tr, p, required=True, expected={"Transform", "RectTransform"}) for p in children]
        edge["parent_lists_child"] = tr in resolved_children
        current = parent_go
    return chain


def flow_roots(idx, flow):
    pending, visited, roots, edges = [flow], set(), set(), []
    while pending:
        key = pending.pop()
        if key in visited:
            continue
        visited.add(key)
        for field, ptr in c7.pointers(idx.objects[key]["tree"]):
            if field in ("m_Script", "m_GameObject"):
                continue
            target = idx.resolve(key, ptr)
            if target is None:
                continue
            edges.append({
                "owner": idx.descriptor(key),
                "field": field,
                "target": idx.descriptor(target),
            })
            if idx.objects[target]["type"] == "GameObject":
                roots.add(target)
            elif any(idx.class_is(target, cls, ns, "DunGen.dll") for cls, ns in (
                ("DungeonFlow", "DunGen.Graph"),
                ("DungeonArchetype", "DunGen"),
                ("TileSet", "DunGen"),
            )):
                if idx.class_is(target, "DungeonFlow", "DunGen.Graph", "DunGen.dll") and target != flow:
                    raise c7.CaptureError("Flow graph refers to a different DungeonFlow")
                pending.append(target)
            else:
                raise c7.CaptureError("Unsupported non-null flow-graph reference: " + field)
    if not roots:
        raise c7.CaptureError("No tile roots resolved for flow")
    return roots, edges


def all_flow_membership(idx):
    result = {}
    errors = {}
    for key in sorted(idx.scripts):
        if not idx.class_is(key, "DungeonFlow", "DunGen.Graph", "DunGen.dll"):
            continue
        name = idx.objects[key]["tree"].get("m_Name")
        if not isinstance(name, str) or not name:
            raise c7.CaptureError("DungeonFlow lacks stable m_Name")
        if name in result:
            raise c7.CaptureError("Duplicate DungeonFlow name in package: " + name)
        try:
            roots, _ = flow_roots(idx, key)
            gos = set()
            for root in roots:
                gos.update(idx.hierarchy(root))
            result[name] = {
                "flow": idx.descriptor(key),
                "roots": roots,
                "gameobjects": gos,
            }
        except Exception as exc:
            errors[name] = f"{type(exc).__name__}: {exc}"
    return result, errors


def structural_reference(owner_type, field):
    return (
        field == "m_GameObject"
        or field.startswith("m_Component[")
        or field == "m_Father"
        or field.startswith("m_Children[")
    )


def reverse_refs(idx, wanted):
    refs = defaultdict(list)
    for owner, rec in idx.objects.items():
        tree = rec.get("tree")
        if tree is None:
            continue
        for field, ptr in c7.pointers(tree):
            if field == "m_Script":
                continue
            try:
                target = idx.resolve(owner, ptr)
            except c7.CaptureError:
                continue
            if target not in wanted:
                continue
            refs[target].append({
                "owner": describe(idx, owner),
                "owner_script": idx.scripts.get(owner),
                "field": field,
                "structural": structural_reference(rec["type"], field),
            })
    return refs


def serialized_type_meta(obj):
    st = getattr(obj, "serialized_type", None)
    def hx(value):
        return None if value is None else bytes(value).hex()
    result = {
        "type_id": getattr(obj, "type_id", None),
        "class_id": getattr(obj, "class_id", None),
        "byte_size": getattr(obj, "byte_size", None),
        "script_type_index": getattr(st, "script_type_index", None) if st else None,
        "script_id": hx(getattr(st, "script_id", None)) if st else None,
        "old_type_hash": hx(getattr(st, "old_type_hash", None)) if st else None,
        "is_stripped_type": getattr(st, "is_stripped_type", None) if st else None,
    }
    sti = result["script_type_index"]
    asset = getattr(obj, "assets_file", None)
    script_types = getattr(asset, "script_types", None) if asset else None
    if isinstance(sti, int) and sti >= 0 and script_types is not None:
        if sti >= len(script_types):
            raise c7.CaptureError("SerializedType script_type_index out of range")
        binding = script_types[sti]
        result["script_type_binding"] = {
            "local_serialized_file_index": getattr(binding, "local_serialized_file_index", None),
            "local_identifier_in_file": getattr(binding, "local_identifier_in_file", None),
        }
    else:
        result["script_type_binding"] = None
    return result


def fingerprint(meta):
    return (meta.get("script_id"), meta.get("old_type_hash"))


def collect_backrooms_null_keys(flow):
    found = set()
    def visit(template):
        for go in template.get("gameobject_component_context", []):
            for comp in go.get("components", []):
                if comp.get("type") == "MonoBehaviour" and comp.get("script") is None:
                    found.add(key_of(comp))
        for child in template.get("spawn_prefab_templates", []):
            visit(child["template"])
    for template in flow.get("templates", []):
        visit(template)
    return found


def probe_backrooms_rebind(path, observed, idx, flow):
    import UnityPy
    null_keys = collect_backrooms_null_keys(flow)
    if len(null_keys) != 2:
        raise c7.CaptureError(f"Expected two unique Backrooms null-script components, found {len(null_keys)}")

    known_classes = {"EntranceTeleport", "InteractTrigger"}
    known_keys = {
        key: script["m_ClassName"]
        for key, script in idx.scripts.items()
        if script and script["m_ClassName"] in known_classes
        and script["m_Namespace"] == ""
        and script["m_AssemblyName"] in ("Assembly-CSharp", "Assembly-CSharp.dll")
    }
    if not any(cls == "EntranceTeleport" for cls in known_keys.values()):
        raise c7.CaptureError("No exact known EntranceTeleport control object in package")

    known_meta = {}
    nodes = defaultdict(list)
    target_meta = {}
    with zipfile.ZipFile(path) as archive:
        for member in observed["unityfs_members"]:
            data = archive.read(member["member"])
            env = UnityPy.load(data)
            for obj in env.objects:
                key = (member["member"], obj.assets_file.name, obj.path_id)
                if key in known_keys:
                    meta = serialized_type_meta(obj)
                    known_meta[key] = meta
                    node = getattr(getattr(obj, "serialized_type", None), "node", None)
                    if node is not None:
                        nodes[known_keys[key]].append((key, meta, node))
                if key in null_keys:
                    target_meta[key] = serialized_type_meta(obj)
            del env, data
            gc.collect()

    if set(target_meta) != null_keys:
        raise c7.CaptureError("Failed to reacquire all Backrooms null-script objects")

    known_fingerprints = defaultdict(set)
    for key, meta in known_meta.items():
        known_fingerprints[fingerprint(meta)].add(known_keys[key])

    probes = []
    with zipfile.ZipFile(path) as archive:
        target_members = sorted({key[0] for key in null_keys})
        for member_name in target_members:
            member_info = next(m for m in observed["unityfs_members"] if m["member"] == member_name)
            data = archive.read(member_name)
            if len(data) != member_info["bytes"] or hashlib.sha256(data).hexdigest() != member_info["sha256"]:
                raise c7.CaptureError("Backrooms rebind member provenance drift")
            env = UnityPy.load(data)
            objects = {(member_name, obj.assets_file.name, obj.path_id): obj for obj in env.objects}
            for key in sorted(null_keys):
                if key[0] != member_name:
                    continue
                obj = objects.get(key)
                if obj is None:
                    raise c7.CaptureError("Backrooms target object missing on second pass")
                meta = target_meta[key]
                matches = sorted(known_fingerprints.get(fingerprint(meta), set()))
                forced = []
                for cls in sorted(nodes):
                    seen_node_hashes = set()
                    for source_key, source_meta, node in nodes[cls]:
                        structure = node.dump_structure()
                        node_hash = hashlib.sha256(structure.encode("utf-8")).hexdigest()
                        if node_hash in seen_node_hashes:
                            continue
                        seen_node_hashes.add(node_hash)
                        attempt = {
                            "candidate_class": cls,
                            "source_control": idx.descriptor(source_key),
                            "source_serialized_type": source_meta,
                            "node_structure_sha256": node_hash,
                            "success": False,
                        }
                        try:
                            parsed = obj.read_typetree(nodes=node, check_read=True)
                            attempt["success"] = True
                            attempt["parsed_fields"] = parsed
                            if cls == "EntranceTeleport":
                                eid = parsed.get("entranceId")
                                side = parsed.get("isEntranceToBuilding")
                                attempt["entrance_predicate"] = (
                                    type(eid) is int and eid == 1
                                    and type(side) in (bool, int) and side == 0
                                )
                        except Exception as exc:
                            attempt["error"] = f"{type(exc).__name__}: {exc}"
                        forced.append(attempt)
                probes.append({
                    "component": idx.descriptor(key),
                    "serialized_type": meta,
                    "known_class_matches_by_script_id_and_old_type_hash": matches,
                    "forced_exact_typetree_probes": forced,
                })
            del env, data, objects
            gc.collect()

    exact_entrance = []
    for probe in probes:
        matches = set(probe["known_class_matches_by_script_id_and_old_type_hash"])
        for attempt in probe["forced_exact_typetree_probes"]:
            if (
                attempt["candidate_class"] == "EntranceTeleport"
                and attempt["success"]
                and attempt.get("entrance_predicate") is True
                and matches == {"EntranceTeleport"}
            ):
                exact_entrance.append((probe, attempt))

    return {
        "null_script_component_count": len(null_keys),
        "known_control_counts": {
            cls: sum(1 for value in known_keys.values() if value == cls)
            for cls in sorted(known_classes)
        },
        "probes": probes,
        "inside_id_1_rebind_proven": len(exact_entrance) == 1,
        "qualification": (
            "A positive rebound requires a unique serialized script-id/type-hash match to "
            "EntranceTeleport plus an exact-consumption parse under a known same-package "
            "EntranceTeleport typetree yielding inside-side entranceId 1. Object naming "
            "alone is never accepted."
        ),
    }


def candidate_analysis(idx, flow_name, flow, package_flows, flow_errors):
    import re
    target_roots = {key_of(x) for x in flow["tile_roots"]}
    target_members = {key_of(x["global_prop"]) for x in flow["prop_tile_membership"]}
    target_gos = package_flows[flow_name]["gameobjects"]
    bundle = flow["dungeon_flow"]["bundle_member"]
    candidates = [
        key for key in idx.scripts
        if idx.class_is(key, "GlobalProp", "DunGen", "DunGen.dll")
        and idx.objects[key]["tree"].get("PropGroupID") == 1231
        and key[0] == bundle
        and key not in target_members
    ]
    rows = []
    wanted = set()
    interim = []
    for prop in sorted(candidates):
        owner = idx.resolve(prop, idx.objects[prop]["tree"].get("m_GameObject"), required=True, expected={"GameObject"})
        chain = ancestry(idx, owner)
        chain_keys = [key_of(x["gameobject"]) for x in chain]
        flow_memberships = sorted(
            name for name, info in package_flows.items()
            if owner in info["gameobjects"]
        )
        root_memberships = sorted(
            name for name, info in package_flows.items()
            if chain_keys[-1] in info["roots"]
        )
        wanted.update({prop, owner, *chain_keys})
        interim.append((prop, owner, chain, flow_memberships, root_memberships))
    refs = reverse_refs(idx, wanted)

    relevant = []
    for prop, owner, chain, flow_memberships, root_memberships in interim:
        nonstructural = []
        exact_doorway_links = []
        for target in {prop, owner, *(key_of(x["gameobject"]) for x in chain)}:
            for ref in refs.get(target, []):
                if ref["structural"]:
                    continue
                owner_key = key_of(ref["owner"])
                enriched = dict(ref)
                owner_go = None
                if idx.objects[owner_key]["type"] == "MonoBehaviour":
                    ptr = idx.objects[owner_key]["tree"].get("m_GameObject")
                    if isinstance(ptr, dict):
                        owner_go = idx.resolve(owner_key, ptr, expected={"GameObject"})
                enriched["owner_gameobject"] = None if owner_go is None else describe(idx, owner_go)
                enriched["owner_in_target_flow_hierarchy"] = owner_go in target_gos if owner_go else False

                match = re.fullmatch(r"BlockerPrefabWeights\[(\d+)\]\.GameObject", ref["field"])
                entry = None
                positive_weight = False
                if match:
                    weights = idx.objects[owner_key]["tree"].get("BlockerPrefabWeights")
                    index = int(match.group(1))
                    if not isinstance(weights, list) or index >= len(weights) or not isinstance(weights[index], dict):
                        raise c7.CaptureError("Malformed Doorway BlockerPrefabWeights entry")
                    entry = weights[index]
                    weight = entry.get("Weight")
                    positive_weight = isinstance(weight, (int, float)) and not isinstance(weight, bool) and weight > 0
                    enriched["blocker_prefab_weight_entry"] = entry
                    enriched["positive_serialized_weight"] = positive_weight

                script = ref.get("owner_script")
                exact_dungen_doorway = bool(
                    script
                    and script.get("m_ClassName") == "Doorway"
                    and script.get("m_Namespace") == "DunGen"
                    and script.get("m_AssemblyName") in ("DunGen.dll", "Assembly-CSharp")
                )
                enriched["exact_dungen_doorway"] = exact_dungen_doorway
                nonstructural.append(enriched)
                if (
                    enriched["owner_in_target_flow_hierarchy"]
                    and exact_dungen_doorway
                    and match
                    and positive_weight
                ):
                    exact_doorway_links.append(enriched)

        template = c7.template_capture(idx, prop)
        row = {
            "global_prop": idx.record(prop),
            "owner_gameobject": describe(idx, owner),
            "ancestry": chain,
            "target_flow_downward_membership": owner in target_gos,
            "target_flow_root_match": key_of(chain[-1]["gameobject"]) in target_roots,
            "all_dungeonflow_downward_memberships": flow_memberships,
            "all_dungeonflow_root_memberships": root_memberships,
            "nonstructural_reverse_references": nonstructural,
            "target_flow_exact_dungen_doorway_blocker_links": exact_doorway_links,
            "template": template,
            "indirect_target_candidate": bool(exact_doorway_links),
            "indirect_standard_template": bool(exact_doorway_links) and template["standard_inside_id_1_template_proven"],
        }
        rows.append(row)
        if row["indirect_target_candidate"]:
            relevant.append(row)

    return {
        "flow_name": flow_name,
        "target_tile_root_count": len(target_roots),
        "target_reachable_prop_1231_count": len(target_members),
        "same_bundle_unreached_prop_1231_count": len(candidates),
        "target_indirect_candidate_count": len(relevant),
        "target_indirect_standard_template_count": sum(x["indirect_standard_template"] for x in relevant),
        "indirect_standard_template_proven": bool(relevant) and all(x["indirect_standard_template"] for x in relevant),
        "package_dungeonflow_names": sorted(package_flows),
        "package_dungeonflow_probe_errors": flow_errors,
        "candidates": rows,
        "qualification": (
            "Indirect membership is accepted only through a positive-weight serialized "
            "DunGen.Doorway.BlockerPrefabWeights[n].GameObject reference whose Doorway "
            "component belongs to the target flow's exact tile hierarchy. Package co-location, "
            "names, custom doorway classes and unrelated reverse references are not sufficient."
        ),
    }


def capture_package(key, out):
    if key not in TARGETS:
        raise ValueError("Package is outside C3F9A target set")
    if importlib.metadata.version("UnityPy") != c7.UNITYPY_VERSION:
        raise ValueError("UnityPy version drift")

    authority = c7.verify_authority()
    path = c7.download(key, out / "cache")
    observed = c7.inventory(key, path)
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    c7.verify_lock(lock, key, authority, observed)

    idx = c7.AssetIndex()
    idx.load(path, observed)
    package_flows, flow_errors = all_flow_membership(idx)

    results = []
    for flow_name in TARGETS[key]:
        flow = c7.capture_flow(idx, flow_name)
        if flow["fatal_ambiguities"]:
            raise c7.CaptureError(flow_name + " C3F7 replay became fatal: " + "; ".join(flow["fatal_ambiguities"]))
        if flow["result_class"] != EXPECTED_RESULTS[flow_name]:
            raise c7.CaptureError(
                f"{flow_name} result drift: {flow['result_class']} != {EXPECTED_RESULTS[flow_name]}"
            )
        item = {
            "flow_name": flow_name,
            "c3f7_result_class": flow["result_class"],
            "prop_1231_settings": flow["prop_1231_serialized_settings"],
        }
        if flow_name == "BackroomsFlow":
            item["backrooms_rebind"] = probe_backrooms_rebind(path, observed, idx, flow)
        else:
            item["candidate_attribution"] = candidate_analysis(
                idx, flow_name, flow, package_flows, flow_errors
            )
        results.append(item)

    result = {
        "schema_version": "c3f9a-static-gap-probe-1",
        "package": observed,
        "source_c3f7_lock_sha256": c7.sha256_file(LOCK),
        "helper_sha256": c7.sha256_file(Path(__file__)),
        "c3f7_helper_sha256": c7.sha256_file(Path(c7.__file__)),
        "authority_sha256": authority,
        "toolchain": {"python": sys.version.split()[0], "unitypy": c7.UNITYPY_VERSION},
        "results": results,
        "proof_boundary": (
            "Static exact-package object-graph and serialized-type evidence only. "
            "No managed package DLL is executed or interpreted here; runtime code "
            "indirection remains a separate obligation where a package contains a DLL."
        ),
    }
    write_json(out / "GAP_CAPTURE.json", result)
    print(json.dumps({
        "package": key,
        "flows": [
            {
                "flow": x["flow_name"],
                "backrooms_rebind": x.get("backrooms_rebind", {}).get("inside_id_1_rebind_proven"),
                "candidate_count": x.get("candidate_attribution", {}).get("same_bundle_unreached_prop_1231_count"),
                "indirect_standard_template_proven": x.get("candidate_attribution", {}).get("indirect_standard_template_proven"),
            }
            for x in results
        ],
    }))


def self_test():
    assert set(TARGETS) == {
        "Generic_GMD-Generic_Interiors",
        "LethalMatt-Bozoros",
        "Magic_Wesley-WesleysInteriors",
        "Tolian-Scoopy_Castle",
        "Beaniebe-Storage_Complex",
    }
    assert sum(len(x) for x in TARGETS.values()) == 6
    assert set(EXPECTED_RESULTS) == {x for values in TARGETS.values() for x in values}
    fake = {"script_id": "aa", "old_type_hash": "bb"}
    assert fingerprint(fake) == ("aa", "bb")
    assert structural_reference("Transform", "m_Father")
    assert structural_reference("GameObject", "m_Component[0].component")
    assert not structural_reference("MonoBehaviour", "spawnPrefab")
    print("C3F9A self-test passed")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--package", choices=TARGETS)
    p.add_argument("--out", type=Path, default=Path("c3f9-output"))
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.package:
        p.error("--package is required unless --self-test is used")
    args.out.mkdir(parents=True, exist_ok=True)
    capture_package(args.package, args.out)


if __name__ == "__main__":
    main()
