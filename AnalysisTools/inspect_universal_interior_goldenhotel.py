#!/usr/bin/env python3
"""GoldenHotel exact-original-byte static graph capture. Never loads game/managed code.

The existing C3 owner-matching COHORT, PACKAGE_LOCK, provenance and captured siblings
are historical records: do not modify them to add this separately-scoped target.
A successful output proves serialized UnityFS links only, NOT generation/runtime.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import sys

import inspect_universal_interior_owner_matching as owner
import inspect_universal_interior_c3f7 as c7

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "BLB_Thunderstore_Mods_LOL-Lead_Interiors"
VERSION = "0.0.7"
FLOW = "GoldenHotel"
DUNGEON_NAME = "Goldstay Hotel"
MEMBER = "BepInEx/plugins/boomsinterior.lethalbundle"
ZIP_BYTES = 208890187
ZIP_SHA256 = "0e605a7280b3c14d52049c5b42c7a85d3001dc98a7fa61f5822364686d13e16b"
MEMBER_BYTES = 208728335
MEMBER_SHA256 = "bf3ddb70d42084c5847a1038abffb759956fe3e9cb4cfc1bbb657b746a14895b"
AUTHORITY_HASHES = {
    owner.AUTHORITY: "80f7b57c09defa48ab99444dfd8d0e1091fa32781e3dc5e44df225d440471fe0",
    owner.EXPORT: "19935c1afc98de1562fda8b299d7d23d09c3555eac88f9de7992eb3d6e2b46b8",
}
HISTORICAL_FLOWS = ["BellevilleApp", "CrimsonKeep"]
EXPECTED_TYPES = [
    ("dungeon_flow", "DungeonFlow", "DunGen.Graph"),
    ("extended_dungeon_flow", "ExtendedDungeonFlow", "LethalLevelLoader"),
    ("level_matching_properties", "LevelMatchingProperties", "LethalLevelLoader"),
]


def require(condition, message):
    if not condition:
        raise c7.CaptureError(message)


def check_locked_package(lock, authority, observed):
    """Check the full unmodified C3 lock, plus independently pinned byte hashes."""
    require(c7.COHORT is owner.COHORT, "Shared C3 cohort identity changed")
    require(owner.COHORT.get(PACKAGE) == (VERSION, HISTORICAL_FLOWS),
            "Historical C3 owner target set must remain two flows")
    require(authority == AUTHORITY_HASHES, "Accepted source authority drift")
    owner.verify_lock(lock, authority, PACKAGE, observed)
    require(observed.get("package") == PACKAGE and observed.get("version") == VERSION,
            "Exact source package identity/version drift")
    require(observed.get("flows") == HISTORICAL_FLOWS, "Historical flow scope drift")
    require(observed.get("zip_bytes") == ZIP_BYTES
            and observed.get("zip_sha256") == ZIP_SHA256, "Original ZIP byte drift")
    require(observed.get("unityfs_members") == [{
        "member": MEMBER, "bytes": MEMBER_BYTES, "sha256": MEMBER_SHA256, "unityfs": True
    }], "Original UnityFS byte/member identity drift")
    require(isinstance(observed.get("archive_members"), list)
            and len(observed["archive_members"]) == 5, "Original full ZIP inventory drift")


def checked_descriptor(idx, obj, class_name, namespace):
    key = (obj["bundle_member"], obj["serialized_file"], obj["path_id"])
    require(obj["bundle_member"] == MEMBER and isinstance(obj["serialized_file"], str)
            and bool(obj["serialized_file"]), "Incorrect target bundle/file identity")
    require(type(obj["path_id"]) is int and obj["path_id"] != 0,
            "Invalid original path ID")
    require(obj.get("type") == "MonoBehaviour", "Original object type mismatch")
    require(isinstance(obj.get("raw_object_sha256"), str)
            and re.fullmatch("[0-9a-f]{64}", obj["raw_object_sha256"]) is not None,
            "Missing original raw object SHA256")
    require(key in idx.objects and idx.objects[key].get("raw_sha256") == obj["raw_object_sha256"],
            "Original raw object identity mismatch")
    require(owner.script_is(idx, key, class_name, namespace),
            "Original MonoScript class or namespace drift: " + class_name)
    require(idx.descriptor(key) == {
        k: obj[k] for k in ("bundle_member", "serialized_file", "path_id",
                            "type", "raw_object_sha256", "script")
    }, "Original serialized descriptor mismatch")
    return key


def checked_single_pointer(idx, parent, field_names, target):
    require(isinstance(field_names, list) and len(field_names) == 1
            and isinstance(field_names[0], str), "Missing/ambiguous mandatory owner pointer")
    fields = dict(c7.pointers(idx.objects[parent]["tree"]))
    require(field_names[0] in fields, "Missing actual serialized owner pointer")
    resolved = idx.resolve(parent, fields[field_names[0]], required=True, expected={"MonoBehaviour"})
    require(resolved == target, "Cross-object/cross-file mandatory pointer mismatch")


def check_matching_fields(value):
    require(isinstance(value, dict), "Missing serialized matching fields")
    for name in ("levelTags", "currentRoutePrice", "currentWeather", "planetNames"):
        require(isinstance(value.get(name), list), "Missing original matching list: " + name)
    for list_name in ("levelTags", "planetNames"):
        for item in value[list_name]:
            require(isinstance(item, dict) and isinstance(item.get("_name"), str)
                    and type(item.get("_rarity")) is int,
                    "Invalid matching tag/name rarity: " + list_name)
    for item in value["currentRoutePrice"]:
        require(isinstance(item, dict) and type(item.get("_rarity")) is int
                and isinstance(item.get("_minMax"), dict),
                "Invalid original currentRoutePrice entry")


def validated_target(idx):
    """Return one exact, pointer-linked original object graph or fail closed."""
    result = owner.capture_target(idx, FLOW)
    require(result.get("flow_name") == FLOW, "GoldenHotel name drift")
    flow = checked_descriptor(idx, result["dungeon_flow"], "DungeonFlow", "DunGen.Graph")
    ext = result["extended_dungeon_flow"]
    owner_key = checked_descriptor(idx, ext, "ExtendedDungeonFlow", "LethalLevelLoader")
    require(ext.get("dungeon_name") == DUNGEON_NAME, "Owner display DungeonName drift")
    checked_single_pointer(idx, owner_key, ext.get("fields_referencing_exact_flow"), flow)
    matching = result.get("level_matching_properties")
    require(isinstance(matching, dict), "Missing original LevelMatchingProperties")
    matching_key = checked_descriptor(idx, matching, "LevelMatchingProperties", "LethalLevelLoader")
    checked_single_pointer(idx, owner_key, ext.get("fields_referencing_level_matching_properties"),
                           matching_key)
    require(matching.get("serialized_fields") == idx.objects[matching_key]["tree"],
            "Original matching type-tree contents drift")
    check_matching_fields(matching["serialized_fields"])
    require(isinstance(matching.get("direct_references"), list),
            "Missing matching pointer inventory")
    actual = list(c7.pointers(matching["serialized_fields"]))
    require(len(actual) == len(matching["direct_references"]),
            "Matching direct-reference inventory incomplete")
    for row in matching["direct_references"]:
        require(isinstance(row, dict), "Malformed matching pointer inventory")
        ptr = row.get("pointer")
        require(any(field == row.get("field") and pointer == ptr for field, pointer in actual),
                "Matching pointer record not in original fields")
        resolved = idx.resolve(matching_key, ptr)
        require(row.get("resolution_error") is None, "Unresolved matching reference")
        if resolved is None:
            require(row.get("resolved") is None, "False non-null original pointer")
        else:
            require(row.get("resolved") is not None, "Non-null reference not recorded")
            expected = idx.descriptor(resolved)
            require(all(row["resolved"].get(k) == v for k, v in expected.items()),
                    "Original matching reference descriptor drift")
    return result


def capture(cache, lock_path, out):
    # Do not change owner.COHORT or c7.COHORT: equality with legacy lock includes flows.
    authority = owner.verify_authority()
    path = c7.download(PACKAGE, cache)
    observed = c7.inventory(PACKAGE, path)  # Verifies manifest + every ZIP member.
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    check_locked_package(lock, authority, observed)
    require(importlib.metadata.version("UnityPy") == c7.UNITYPY_VERSION == "1.25.3",
            "UnityPy version mismatch")
    require(importlib.metadata.version("PyYAML") == "6.0.2", "PyYAML version mismatch")
    idx = c7.AssetIndex()
    idx.load(path, observed)  # Re-hashes each UnityFS member before type-tree load.
    target = validated_target(idx)
    source_rel = Path(__file__).relative_to(ROOT)
    source_bytes = (ROOT / source_rel).read_bytes()
    expected_head = os.environ.get("EXPECTED_HEAD", "")
    require(not expected_head or re.fullmatch("[0-9a-f]{40}", expected_head) is not None,
            "Invalid pinned checkout SHA")
    owner.write_json(out / "GOLDENHOTEL_CAPTURE.json", {
        "schema_version": 1,
        "classification": "STATIC_SERIALIZED_ORIGINAL_ASSET_ONLY / NOT_GENERATION_PASS",
        "source_code": {
            "path": source_rel.as_posix(),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "checked_out_head": expected_head or None,
            "python": platform.python_version(),
            "unitypy": importlib.metadata.version("UnityPy"),
            "pyyaml": importlib.metadata.version("PyYAML"),
        },
        "legacy_lock_path": owner.LOCK.relative_to(ROOT).as_posix(),
        "authority": authority,
        "package": observed,
        "target": target,
        "proof_limit": "Static original serialized DungeonFlow/ExtendedDungeonFlow/LevelMatchingProperties identities only; no generation, CullFactory, entrances, NavMesh, traversal, live managed-object identity or runtime PASS.",
    })


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("goldenhotel-package-cache"))
    parser.add_argument("--lock", type=Path, default=owner.LOCK)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("GOLDENHOTEL_CAPTURE.json", "GOLDENHOTEL_FAILURE.json"):
        (args.out / name).unlink(missing_ok=True)
    try:
        capture(args.cache, args.lock, args.out)
    except Exception as exc:
        owner.write_json(args.out / "GOLDENHOTEL_FAILURE.json", {
            "schema_version": 1,
            "classification": "CAPTURE_FAILED / NO_STATIC_OR_RUNTIME_PASS",
            "package": PACKAGE,
            "flow": FLOW,
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
        raise
    return 0


if __name__ == "__main__":
    sys.exit(main())
