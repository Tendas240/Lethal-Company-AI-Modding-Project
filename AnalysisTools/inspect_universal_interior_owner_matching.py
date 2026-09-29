#!/usr/bin/env python3
"""Bounded static capture for the final three unresolved C3 owner matching assets.

The probe reuses the reviewed C3F7 Thunderstore acquisition and UnityPy pathway.
It never loads Unity, the game, or managed mod code. A first invocation with
--record-provenance only records exact package/member bytes. Normal capture is
refused until those bytes are pinned in PACKAGE_LOCK.json.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

import inspect_universal_interior_c3f7 as c7

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3OwnerMatching"
LOCK = EVIDENCE / "PACKAGE_LOCK.json"
AUTHORITY = "Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md"
EXPORT = "ProfileSources/S1.42AK/export.r2x"
COHORT = {
    "Piggy-LC_Office": ("2.3.4", ["OfficeDungeonFlow"]),
    "BLB_Thunderstore_Mods_LOL-Lead_Interiors": ("0.0.7", ["BellevilleApp", "CrimsonKeep"]),
}

# Reuse only the already-reviewed static acquisition/parser implementation.
c7.COHORT = COHORT


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(c7.json_safe(value), indent=2, allow_nan=False) + "\n", encoding="utf-8")


def verify_authority():
    return c7.verify_authority()


def script_is(idx, key, class_name, namespace=None):
    script = idx.scripts.get(key)
    if not script or script.get("m_ClassName") != class_name:
        return False
    if namespace is not None and script.get("m_Namespace") != namespace:
        return False
    return True


def resolved_pointer_fields(idx, owner):
    result = []
    tree = idx.objects[owner]["tree"]
    for field, ptr in c7.pointers(tree):
        if field == "m_Script":
            continue
        entry = {"field": field, "pointer": ptr, "resolved": None, "resolution_error": None}
        try:
            target = idx.resolve(owner, ptr)
        except c7.CaptureError as exc:
            entry["resolution_error"] = str(exc)
            result.append(entry)
            continue
        if target is not None:
            rec = idx.objects[target]
            target_tree = rec.get("tree", {})
            entry["resolved"] = {
                **idx.descriptor(target),
                "name": target_tree.get("m_Name"),
            }
        result.append(entry)
    return result


def exact_flow(idx, flow_name):
    matches = [
        key for key in idx.scripts
        if c7.class_is(key, "DungeonFlow", "DunGen.Graph", "DunGen.dll")
        and idx.objects[key]["tree"].get("m_Name") == flow_name
    ]
    if len(matches) != 1:
        raise c7.CaptureError(f"Expected one exact DungeonFlow {flow_name}, found {len(matches)}")
    return matches[0]


def owner_for_flow(idx, flow):
    candidates = []
    for key in idx.scripts:
        if not script_is(idx, key, "ExtendedDungeonFlow", "LethalLevelLoader"):
            continue
        fields = []
        for field, ptr in c7.pointers(idx.objects[key]["tree"]):
            if field == "m_Script":
                continue
            try:
                target = idx.resolve(key, ptr)
            except c7.CaptureError:
                continue
            if target == flow:
                fields.append(field)
        if fields:
            candidates.append((key, sorted(fields)))
    if len(candidates) != 1:
        raise c7.CaptureError(f"Expected one ExtendedDungeonFlow owner, found {len(candidates)}")
    return candidates[0]


def matching_asset(idx, owner):
    matches = []
    for field, ptr in c7.pointers(idx.objects[owner]["tree"]):
        if field == "m_Script":
            continue
        try:
            target = idx.resolve(owner, ptr)
        except c7.CaptureError:
            continue
        if target is not None and script_is(idx, target, "LevelMatchingProperties", "LethalLevelLoader"):
            matches.append((field, target))
    unique = {}
    for field, target in matches:
        unique.setdefault(target, []).append(field)
    if len(unique) > 1:
        raise c7.CaptureError("ExtendedDungeonFlow refers to multiple LevelMatchingProperties assets")
    if not unique:
        return None, []
    target, fields = next(iter(unique.items()))
    return target, sorted(fields)


def legacy_matching_fields(tree):
    names = {
        "dynamicLevelTagsList",
        "dynamicRoutePricesList",
        "dynamicCurrentWeatherList",
        "manualPlanetNameReferenceList",
        "manualContentSourceNameReferenceList",
        "generateAutomaticConfigurationOptions",
    }
    return {key: tree[key] for key in sorted(tree) if key in names}


def describe_matching(idx, matching):
    if matching is None:
        return None
    tree = idx.objects[matching]["tree"]
    refs = []
    for row in resolved_pointer_fields(idx, matching):
        target = row.get("resolved")
        if target is None:
            refs.append(row)
            continue
        key = (target["bundle_member"], target["serialized_file"], target["path_id"])
        ttree = idx.objects[key].get("tree", {})
        row["resolved"]["script"] = idx.scripts.get(key)
        # ContentTag assets are tiny and their exact serialized identity matters
        # for Custom/Vanilla/All applicability; retain their complete fields.
        if script_is(idx, key, "ContentTag", "LethalLevelLoader"):
            row["resolved"]["serialized_fields"] = ttree
        refs.append(row)
    return {
        **idx.descriptor(matching),
        "serialized_fields": tree,
        "direct_references": refs,
    }


def capture_target(idx, flow_name):
    flow = exact_flow(idx, flow_name)
    owner, owner_flow_fields = owner_for_flow(idx, flow)
    owner_tree = idx.objects[owner]["tree"]
    matching, matching_fields = matching_asset(idx, owner)
    return {
        "flow_name": flow_name,
        "dungeon_flow": idx.descriptor(flow),
        "extended_dungeon_flow": {
            **idx.descriptor(owner),
            "name": owner_tree.get("m_Name"),
            "dungeon_name": owner_tree.get("<DungeonName>k__BackingField", owner_tree.get("DungeonName", owner_tree.get("dungeonDisplayName"))),
            "fields_referencing_exact_flow": owner_flow_fields,
            "fields_referencing_level_matching_properties": matching_fields,
            "legacy_matching_fields": legacy_matching_fields(owner_tree),
        },
        "level_matching_properties": describe_matching(idx, matching),
    }


def verify_lock(lock, authority, key, observed):
    if lock.get("schema_version") != 1:
        raise c7.CaptureError("Owner-matching lock schema drift")
    if lock.get("authority") != authority:
        raise c7.CaptureError("Owner-matching authority hash drift")
    packages = lock.get("packages")
    if not isinstance(packages, dict) or set(packages) != set(COHORT):
        raise c7.CaptureError("Owner-matching lock must contain exactly the two target packages")
    if packages.get(key) != observed:
        raise c7.CaptureError("ZIP/member provenance drift: " + key)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--package", choices=COHORT)
    p.add_argument("--cache", type=Path, default=Path("c3-owner-packages"))
    p.add_argument("--out", type=Path)
    p.add_argument("--lock", type=Path, default=LOCK)
    p.add_argument("--record-provenance", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()

    if args.self_test:
        assert set(COHORT) == {"Piggy-LC_Office", "BLB_Thunderstore_Mods_LOL-Lead_Interiors"}
        assert COHORT["Piggy-LC_Office"] == ("2.3.4", ["OfficeDungeonFlow"])
        assert COHORT["BLB_Thunderstore_Mods_LOL-Lead_Interiors"] == ("0.0.7", ["BellevilleApp", "CrimsonKeep"])
        print("owner-matching self-test passed")
        return 0
    if not args.package or not args.out:
        p.error("--package and --out are required outside --self-test")

    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("PROVENANCE_CANDIDATE.json", "CAPTURE.json", "CAPTURE_FAILURE.json"):
        (args.out / name).unlink(missing_ok=True)

    key = args.package
    try:
        authority = verify_authority()
        path = c7.download(key, args.cache)
        observed = c7.inventory(key, path)
        if args.record_provenance:
            write_json(args.out / "PROVENANCE_CANDIDATE.json", {
                "schema_version": 1,
                "authority": authority,
                "package": observed,
                "qualification": "Candidate byte provenance only; no asset clearance until exact bytes are pinned in PACKAGE_LOCK.json.",
            })
            return 0

        lock = json.loads(args.lock.read_text(encoding="utf-8"))
        verify_lock(lock, authority, key, observed)
        if importlib.metadata.version("UnityPy") != c7.UNITYPY_VERSION:
            raise c7.CaptureError("UnityPy version drift")
        idx = c7.AssetIndex()
        idx.load(path, observed)
        captures = {flow: capture_target(idx, flow) for flow in COHORT[key][1]}
        write_json(args.out / "CAPTURE.json", {
            "schema_version": 1,
            "authority": authority,
            "package": observed,
            "unitypy_version": importlib.metadata.version("UnityPy"),
            "targets": captures,
            "proof_boundary": "Exact static package/object-graph serialization only. No Unity/game/mod managed code execution and no Phase-C3 applicability conclusion in this capture.",
        })
        return 0
    except Exception as exc:
        write_json(args.out / "CAPTURE_FAILURE.json", {
            "schema_version": 1,
            "package": key,
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
        raise


if __name__ == "__main__":
    sys.exit(main())
