#!/usr/bin/env python3
"""Bounded static capture for the final three unresolved C3 owner matching assets.

The probe reuses the reviewed C3F7 Thunderstore acquisition and UnityPy pathway.
It never loads Unity, the game, or managed mod code. A first invocation with
--record-provenance only records exact package/member bytes. Normal capture is
refused until those bytes are pinned in PACKAGE_LOCK.json.
"""
import argparse
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

# Original byte-lock cohort is immutable: the historical two-flow lock and
# existing BellevilleApp/CrimsonKeep JSON remain untouched. LeadFactory is an
# additional capture target, not a rewrite of historical PACKAGE_LOCK metadata.
ADDITIONAL_TARGETS = {
    "BLB_Thunderstore_Mods_LOL-Lead_Interiors": ("LeadFactory",),
}
LEAD_BUNDLE = "BepInEx/plugins/boomsinterior.lethalbundle"
LEAD_CAB = "CAB-38a1e9912a4e0bf00320c85779ae5f69"
# Previously handed-over candidate object pins, NOT new independently observed bytes.
# Every pin MUST be independently verified on a later, separately authorized capture.
LEAD_FACTORY_PINS = {
    "extended_mod": ("LeadInteriors", "ExtendedMod", -5675661616573147864, "b7bbafab52d59bfd3b5ac0f342db7250dcaf6c63e53112f1448fc93754f738e1"),
    "extended_flow": ("LFExtended", "ExtendedDungeonFlow", -3701692716072040616, "6d02f4b61c8e0e380e1267d32c7f972da37280dbb4843792be6b5e17af9f8ecd"),
    "dungeon_flow": ("LeadFactory", "DungeonFlow", 6083446938328665743, "3e248637eea8633ccd9934276343d57bed62c6ac551970e07cac401b51fa0406"),
    "matching": ("LFMatchingProperties", "LevelMatchingProperties", 7848904247385245749, "f5aa37562c665a6018548a7df248f7a9c4683cd28149010e96338202d0624b49"),
}

# Reuse only the already-reviewed static acquisition/parser implementation.
c7.COHORT = COHORT


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(c7.json_safe(value), indent=2, allow_nan=False) + "\n", encoding="utf-8")


def verify_leadfactory_registration():
    rows = (ROOT / AUTHORITY).read_text(encoding="utf-8").splitlines()
    # The existing hash in PACKAGE_LOCK already covers this exact inventory.
    qualified = [
        line for line in rows
        if "| `LeadFactory` |" in line
        and "| `leadinteriors:leadfactory` |" in line
        and "| BLB_Thunderstore_Mods_LOL-Lead_Interiors 0.0.7 |" in line
        and "| Custom #24 |" in line
    ]
    if len(qualified) != 1:
        raise c7.CaptureError("LeadFactory authoritative package/LLL registration drift")


def verify_authority():
    existing = c7.verify_authority()
    verify_leadfactory_registration()
    return existing


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
            target_tree = idx.objects[target].get("tree", {})
            entry["resolved"] = {
                **idx.descriptor(target),
                "name": target_tree.get("m_Name"),
            }
        result.append(entry)
    return result


def exact_flow(idx, flow_name):
    matches = [
        key for key in idx.scripts
        if idx.class_is(key, "DungeonFlow", "DunGen.Graph", "DunGen.dll")
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



def require_lead_pin(idx, key, label):
    name, cls, path_id, raw_sha = LEAD_FACTORY_PINS[label]
    if not script_is(idx, key, cls, "DunGen.Graph" if cls == "DungeonFlow" else "LethalLevelLoader"):
        raise c7.CaptureError("LeadFactory serialized class drift: " + label)
    d = idx.descriptor(key)
    if (d.get("bundle_member"), d.get("serialized_file"), d.get("path_id"), d.get("raw_object_sha256")) != (
        LEAD_BUNDLE, LEAD_CAB, path_id, raw_sha
    ):
        raise c7.CaptureError("LeadFactory historical candidate object pin mismatch: " + label)
    if idx.objects[key]["tree"].get("m_Name") != name:
        raise c7.CaptureError("LeadFactory serialized name mismatch: " + label)


def leadfactory_owner_provenance(idx, flow, owner, matching):
    if matching is None:
        raise c7.CaptureError("LeadFactory requires exact LevelMatchingProperties reference")
    require_lead_pin(idx, flow, "dungeon_flow")
    require_lead_pin(idx, owner, "extended_flow")
    require_lead_pin(idx, matching, "matching")
    mods = [
        key for key in idx.scripts
        if script_is(idx, key, "ExtendedMod", "LethalLevelLoader")
        and idx.objects[key]["tree"].get("m_Name") == "LeadInteriors"
    ]
    if len(mods) != 1:
        raise c7.CaptureError("LeadFactory requires exactly one LeadInteriors ExtendedMod")
    mod = mods[0]
    require_lead_pin(idx, mod, "extended_mod")
    owner_fields = []
    for field, ptr in c7.pointers(idx.objects[mod]["tree"]):
        if field == "m_Script":
            continue
        # Unresolved non-null references cannot be silently interpreted as safe.
        target = idx.resolve(mod, ptr)
        if target == owner:
            owner_fields.append(field)
    if not owner_fields:
        raise c7.CaptureError("LeadInteriors ExtendedMod has no exact LFExtended reference")
    return {
        **idx.descriptor(mod),
        "name": "LeadInteriors",
        "fields_referencing_exact_extended_flow": sorted(owner_fields),
        "historical_pins_status": "CANDIDATE_ONLY_UNTIL_EXACT_AUTHORIZED_ORIGINAL_RECAPTURE",
        "proof_boundary": "Serialized ExtendedMod-to-ExtendedDungeonFlow-to-DungeonFlow and matching-asset links only; not managed registration, Offense applicability, normalization, generation, selector safety or runtime PASS.",
    }

def capture_target(idx, flow_name):
    flow = exact_flow(idx, flow_name)
    owner, owner_flow_fields = owner_for_flow(idx, flow)
    owner_tree = idx.objects[owner]["tree"]
    matching, matching_fields = matching_asset(idx, owner)
    extra = {"extended_mod": leadfactory_owner_provenance(idx, flow, owner, matching)} if flow_name == "LeadFactory" else {}
    return {
        **extra,
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
        raise c7.CaptureError("Owner-matching lock must contain exactly the two originally locked packages")
    if packages.get(key) != observed:
        raise c7.CaptureError("ZIP/member provenance drift: " + key)



def self_test_leadfactory():
    # No network, UnityPy import, original bytes, game load or managed code.
    assert ADDITIONAL_TARGETS == {"BLB_Thunderstore_Mods_LOL-Lead_Interiors": ("LeadFactory",)}
    assert COHORT["BLB_Thunderstore_Mods_LOL-Lead_Interiors"][1] == ["BellevilleApp", "CrimsonKeep"]
    pins = LEAD_FACTORY_PINS
    keys = {n: (LEAD_BUNDLE, LEAD_CAB, p[2]) for n, p in pins.items()}
    def ptr(label):
        return {"m_FileID": 0, "m_PathID": keys[label][2]}
    class FakeIndex:
        def __init__(self):
            self.scripts = {}
            self.objects = {}
            for label, key in keys.items():
                name, cls, _, raw = pins[label]
                ns = "DunGen.Graph" if cls == "DungeonFlow" else "LethalLevelLoader"
                assembly = "DunGen.dll" if cls == "DungeonFlow" else "LethalLevelLoader.dll"
                self.scripts[key] = {"m_ClassName": cls, "m_Namespace": ns, "m_AssemblyName": assembly}
                tree = {"m_Name": name}
                if label == "extended_mod":
                    tree["m_ExtendedDungeonFlows"] = [ptr("extended_flow")]
                if label == "extended_flow":
                    tree["<DungeonFlow>k__BackingField"] = ptr("dungeon_flow")
                    tree["<LevelMatchingProperties>k__BackingField"] = ptr("matching")
                self.objects[key] = {"tree": tree, "type": "MonoBehaviour", "raw_sha256": raw}
        def resolve(self, origin, pointer):
            if pointer["m_PathID"] == 0:
                return None
            key = (origin[0], origin[1], pointer["m_PathID"])
            if key not in self.objects:
                raise c7.CaptureError("Unresolved synthetic pointer")
            return key
        def class_is(self, key, cls, ns, assembly):
            row = self.scripts.get(key, {})
            return (row.get("m_ClassName"), row.get("m_Namespace"), row.get("m_AssemblyName")) == (cls, ns, assembly)
        def descriptor(self, key):
            rec = self.objects[key]
            return {"bundle_member": key[0], "serialized_file": key[1], "path_id": key[2],
                    "type": rec["type"], "raw_object_sha256": rec["raw_sha256"], "script": self.scripts[key]}
    good = capture_target(FakeIndex(), "LeadFactory")
    assert good["extended_mod"]["fields_referencing_exact_extended_flow"] == ["m_ExtendedDungeonFlows[0]"]
    assert good["extended_dungeon_flow"]["fields_referencing_exact_flow"] == ["<DungeonFlow>k__BackingField"]
    assert good["extended_dungeon_flow"]["fields_referencing_level_matching_properties"] == ["<LevelMatchingProperties>k__BackingField"]
    for label in ("extended_mod", "extended_flow", "dungeon_flow", "matching"):
        bad = FakeIndex()
        bad.objects[keys[label]]["raw_sha256"] = "0" * 64
        try:
            capture_target(bad, "LeadFactory")
        except c7.CaptureError:
            pass
        else:
            raise AssertionError("Unpinned " + label + " silently passed")
    bad = FakeIndex()
    bad.objects[keys["extended_mod"]]["tree"]["m_ExtendedDungeonFlows"] = []
    try:
        capture_target(bad, "LeadFactory")
    except c7.CaptureError:
        pass
    else:
        raise AssertionError("Missing ExtendedMod edge silently passed")
    bad = FakeIndex()
    bad.objects[keys["extended_flow"]]["tree"]["<LevelMatchingProperties>k__BackingField"] = {"m_FileID": 0, "m_PathID": 0}
    try:
        capture_target(bad, "LeadFactory")
    except c7.CaptureError:
        pass
    else:
        raise AssertionError("Missing matching-asset edge silently passed")
    # This full self-test uses only existing checked-in source/lock bytes.
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["packages"]["BLB_Thunderstore_Mods_LOL-Lead_Interiors"]["flows"] == ["BellevilleApp", "CrimsonKeep"]
    assert lock["packages"]["BLB_Thunderstore_Mods_LOL-Lead_Interiors"]["zip_sha256"] == "0e605a7280b3c14d52049c5b42c7a85d3001dc98a7fa61f5822364686d13e16b"
    assert lock["packages"]["BLB_Thunderstore_Mods_LOL-Lead_Interiors"]["unityfs_members"][0]["sha256"] == "bf3ddb70d42084c5847a1038abffb759956fe3e9cb4cfc1bbb657b746a14895b"
    verify_leadfactory_registration()

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
        self_test_leadfactory()
        print("owner-matching source-only LeadFactory self-test passed")
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
        capture_names = list(COHORT[key][1]) + list(ADDITIONAL_TARGETS.get(key, ()))
        captures = {flow: capture_target(idx, flow) for flow in capture_names}
        write_json(args.out / "CAPTURE.json", {
            "schema_version": 1,
            "authority": authority,
            "package": observed,
            "unitypy_version": importlib.metadata.version("UnityPy"),
            "capture_target_names": capture_names,
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
