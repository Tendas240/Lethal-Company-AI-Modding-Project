#!/usr/bin/env python3
"""Minimal LeadFactory static provenance; no original/object-tree publication.

Capture requires an independent, authorized manual workflow_dispatch. A PR
runs only --self-test, which uses no original bytes, downloads or UnityPy.
The output is local to the short-lived runner: NO upload/artifact/publication.
It is a narrowly whitelisted technical fact record, not Offense or runtime PASS.
"""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

import inspect_universal_interior_owner_matching as owner

PACKAGE = "BLB_Thunderstore_Mods_LOL-Lead_Interiors"
TARGET = "LeadFactory"
AUTHORIZATION = "I_AUTHORIZE_ONE_PINNED_C3_OWNER_SOURCE_CAPTURE"
KEYS = ("extended_mod", "extended_flow", "dungeon_flow", "matching")
EDGE_NAMES = (
    "extended_mod_to_extended_flow",
    "extended_flow_to_dungeon_flow",
    "extended_flow_to_matching",
)
FIELD_RE = re.compile(r"^[A-Za-z_<>][A-Za-z0-9_<>\[\].-]{0,127}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_OUTPUT_BYTES = 8192


def fail(message):
    raise owner.c7.CaptureError("LeadFactory minimal-output gate: " + message)


def exact_keys(value, names):
    if type(value) is not dict or set(value) != set(names):
        fail("unexpected output fields")


def require_field_names(fields):
    if type(fields) is not list or not fields or len(fields) > 16:
        fail("invalid provenance edge count")
    if len(set(fields)) != len(fields):
        fail("duplicate provenance edge")
    if fields != sorted(fields):
        fail("unsorted provenance edges")
    for name in fields:
        if type(name) is not str or not FIELD_RE.fullmatch(name):
            fail("unsafe or nontechnical field name")


def verify_minimal(report, lock):
    """Whitelist the whole emitted JSON, including every nested member."""
    exact_keys(report, ("schema_version", "target", "result", "source", "objects", "edges", "proof_boundary"))
    if report["schema_version"] != 1 or report["target"] != TARGET or report["result"] != "PASS":
        fail("schema/target/outcome drift")
    if report["proof_boundary"] != "PINNED_SERIALIZED_REFERENCES_ONLY_NOT_OFFENSE_OR_RUNTIME_PASS":
        fail("proof-boundary drift")
    source = report["source"]
    exact_keys(source, (
        "package", "version", "zip_bytes", "zip_sha256",
        "unityfs_member", "unityfs_bytes", "unityfs_sha256",
        "authority_verified", "exact_package_lock_verified", "unitypy_version",
    ))
    locked = lock["packages"][PACKAGE]
    unityfs = locked["unityfs_members"]
    if len(unityfs) != 1:
        fail("ambiguous UnityFS member count")
    member = unityfs[0]
    expected_source = {
        "package": PACKAGE,
        "version": "0.0.7",
        "zip_bytes": locked["zip_bytes"],
        "zip_sha256": locked["zip_sha256"],
        "unityfs_member": owner.LEAD_BUNDLE,
        "unityfs_bytes": member["bytes"],
        "unityfs_sha256": member["sha256"],
        "authority_verified": True,
        "exact_package_lock_verified": True,
        "unitypy_version": owner.c7.UNITYPY_VERSION,
    }
    if source != expected_source:
        fail("package/provenance output mismatch")
    for key in ("zip_sha256", "unityfs_sha256"):
        if type(source[key]) is not str or not SHA_RE.fullmatch(source[key]):
            fail("invalid SHA-256")
    if type(source["zip_bytes"]) is not int or type(source["unityfs_bytes"]) is not int:
        fail("invalid source size")
    objects = report["objects"]
    exact_keys(objects, KEYS)
    for label in KEYS:
        pin_name, pin_class, pin_path, pin_hash = owner.LEAD_FACTORY_PINS[label]
        obj = objects[label]
        exact_keys(obj, ("name", "class", "bundle_member", "serialized_file", "path_id", "raw_object_sha256"))
        expected = {
            "name": pin_name,
            "class": pin_class,
            "bundle_member": owner.LEAD_BUNDLE,
            "serialized_file": owner.LEAD_CAB,
            "path_id": pin_path,
            "raw_object_sha256": pin_hash,
        }
        if obj != expected or type(obj["path_id"]) is not int or not SHA_RE.fullmatch(obj["raw_object_sha256"]):
            fail("candidate object identity not exactly reverified: " + label)
    edges = report["edges"]
    exact_keys(edges, EDGE_NAMES)
    for label in EDGE_NAMES:
        require_field_names(edges[label])
    encoded = json.dumps(report, ensure_ascii=True, allow_nan=False, sort_keys=True)
    if len(encoded.encode("utf-8")) > MAX_OUTPUT_BYTES:
        fail("output exceeds minimal technical size budget")
    # No serialized raw trees, dynamic asset content, tags, pricing, weather,
    # mod descriptions or source bytes may appear in the output.
    prohibited = (
        "serialized_fields", "legacy_matching_fields", "direct_references",
        "levelTags", "planetNames", "modNames", "authorNames",
        "currentRoutePrice", "currentWeather", "m_GameObject",
    )
    if any(value in encoded for value in prohibited):
        fail("protected serialized content in output")
    return True


def minimal_report(idx, lock):
    # Reuse the validated 4-node provenance chain but never call capture_target()
    # or describe_matching(), whose historical mode emits full object trees.
    flow = owner.exact_flow(idx, TARGET)
    extended_flow, flow_fields = owner.owner_for_flow(idx, flow)
    matching, matching_fields = owner.matching_asset(idx, extended_flow)
    provenance = owner.leadfactory_owner_provenance(idx, flow, extended_flow, matching)
    extended_mod = (owner.LEAD_BUNDLE, owner.LEAD_CAB, owner.LEAD_FACTORY_PINS["extended_mod"][2])
    objects = {}
    for label, key in (
        ("extended_mod", extended_mod),
        ("extended_flow", extended_flow),
        ("dungeon_flow", flow),
        ("matching", matching),
    ):
        owner.require_lead_pin(idx, key, label)
        name, class_name, path_id, sha = owner.LEAD_FACTORY_PINS[label]
        # Only pinned scalar identities, never idx.objects[key]["tree"].
        objects[label] = {
            "name": name, "class": class_name,
            "bundle_member": owner.LEAD_BUNDLE,
            "serialized_file": owner.LEAD_CAB,
            "path_id": path_id, "raw_object_sha256": sha,
        }
    locked = lock["packages"][PACKAGE]
    member = locked["unityfs_members"][0]
    result = {
        "schema_version": 1,
        "target": TARGET,
        "result": "PASS",
        "source": {
            "package": PACKAGE,
            "version": locked["version"],
            "zip_bytes": locked["zip_bytes"],
            "zip_sha256": locked["zip_sha256"],
            "unityfs_member": member["member"],
            "unityfs_bytes": member["bytes"],
            "unityfs_sha256": member["sha256"],
            "authority_verified": True,
            "exact_package_lock_verified": True,
            "unitypy_version": owner.c7.UNITYPY_VERSION,
        },
        "objects": objects,
        "edges": {
            "extended_mod_to_extended_flow": provenance["fields_referencing_exact_extended_flow"],
            "extended_flow_to_dungeon_flow": flow_fields,
            "extended_flow_to_matching": matching_fields,
        },
        "proof_boundary": "PINNED_SERIALIZED_REFERENCES_ONLY_NOT_OFFENSE_OR_RUNTIME_PASS",
    }
    verify_minimal(result, lock)
    return result


def verify_workflow_boundary():
    path = owner.ROOT / ".github/workflows/universal-interior-c3-owner-matching-evidence.yml"
    content = path.read_text(encoding="utf-8")
    if content.count("\n  capture:\n") != 1:
        fail("workflow capture job count drift")
    validate, capture = content.split("\n  capture:\n")
    if "  pull_request:\n" not in validate:
        fail("missing pull_request source validation")
    if any(x in validate for x in ("pip install", "urlopen", "Acquire exact package", "upload-artifact", "capture_leadfactory_minimal_provenance.py --target")):
        fail("PR-side network/capture/publishing risk")
    if "if: github.event_name == 'workflow_dispatch'" not in capture:
        fail("capture is not manual-dispatch gated")
    if "actions/upload-artifact" in content or "--record-provenance" in content:
        fail("unreviewed artifact publication or provenance fallback")
    if "options:\n          - LeadFactory" not in content:
        fail("workflow capture target is not exclusively LeadFactory")
    # The package is hardcoded in this source module, not a workflow input.
    if PACKAGE != "BLB_Thunderstore_Mods_LOL-Lead_Interiors":
        fail("source package pin drift")
    if "source_capture_authorization" not in content or "expected_head_sha" not in content:
        fail("missing independent capture authorization/commit pin")
    if capture.index("Fail closed on missing independent authorization") > capture.index("pip install"):
        fail("network step precedes authorization")
    if "python AnalysisTools/capture_leadfactory_minimal_provenance.py --target LeadFactory" not in capture:
        fail("workflow targets a nonminimal legacy capture path")


def self_test():
    # Original parser supplies synthetic positive/negative four-object tests.
    owner.self_test_leadfactory()
    lock = json.loads(owner.LOCK.read_text(encoding="utf-8"))
    locked = lock["packages"][PACKAGE]
    assert locked["flows"] == ["BellevilleApp", "CrimsonKeep"]
    assert locked["zip_sha256"] == "0e605a7280b3c14d52049c5b42c7a85d3001dc98a7fa61f5822364686d13e16b"
    assert locked["unityfs_members"][0]["sha256"] == "bf3ddb70d42084c5847a1038abffb759956fe3e9cb4cfc1bbb657b746a14895b"
    # Synthetic evidence construction (no original ZIP/asset bytes).
    obj = {
        label: {
            "name": p[0], "class": p[1],
            "bundle_member": owner.LEAD_BUNDLE,
            "serialized_file": owner.LEAD_CAB,
            "path_id": p[2], "raw_object_sha256": p[3],
        } for label, p in owner.LEAD_FACTORY_PINS.items()
    }
    member = locked["unityfs_members"][0]
    sample = {
        "schema_version": 1,
        "target": TARGET,
        "result": "PASS",
        "source": {
            "package": PACKAGE, "version": "0.0.7",
            "zip_bytes": locked["zip_bytes"], "zip_sha256": locked["zip_sha256"],
            "unityfs_member": owner.LEAD_BUNDLE, "unityfs_bytes": member["bytes"],
            "unityfs_sha256": member["sha256"],
            "authority_verified": True, "exact_package_lock_verified": True,
            "unitypy_version": owner.c7.UNITYPY_VERSION,
        },
        "objects": obj,
        "edges": {
            "extended_mod_to_extended_flow": ["m_ExtendedDungeonFlows[0]"],
            "extended_flow_to_dungeon_flow": ["<DungeonFlow>k__BackingField"],
            "extended_flow_to_matching": ["<LevelMatchingProperties>k__BackingField"],
        },
        "proof_boundary": "PINNED_SERIALIZED_REFERENCES_ONLY_NOT_OFFENSE_OR_RUNTIME_PASS",
    }
    assert verify_minimal(sample, lock)
    # Every extra or protected field, missing link, changed hash or inferred
    # Offense/runtime success must cause refusal, not a broader JSON export.
    import copy
    corruptions = (
        lambda x: x["objects"]["matching"].update({"serialized_fields": {"levelTags": [100]}}),
        lambda x: x["objects"]["matching"].update({"raw_object_sha256": "0" * 64}),
        lambda x: x["edges"].update({"extended_flow_to_matching": []}),
        lambda x: x["edges"].update({"extended_mod_to_extended_flow": ["some tag words with spaces"]}),
        lambda x: x.update({"Offense_generation_PASS": True}),
        lambda x: x.update({"result": "RUNTIME_PASS"}),
        lambda x: x["source"].update({"source_url": "https://example.invalid/repacked.zip"}),
    )
    for mutate in corruptions:
        wrong = copy.deepcopy(sample)
        mutate(wrong)
        try:
            verify_minimal(wrong, lock)
        except owner.c7.CaptureError:
            pass
        else:
            raise AssertionError("unsafe synthetic minimal-report mutation was accepted")
    verify_workflow_boundary()
    owner.verify_leadfactory_registration()
    print("LeadFactory minimal provenance source-only self-test PASS")


def run_capture(args):
    if args.target != TARGET or os.environ.get("LEADFACTORY_CAPTURE_AUTHORIZATION") != AUTHORIZATION:
        fail("independent manual authorization or exact target missing")
    authority = owner.verify_authority()
    lock = json.loads(owner.LOCK.read_text(encoding="utf-8"))
    if lock.get("schema_version") != 1 or lock.get("authority") != authority:
        fail("original byte/authority lock drift")
    if set(lock.get("packages", {})) != set(owner.COHORT):
        fail("original package set drift")
    locked = lock["packages"][PACKAGE]
    if (locked.get("version"), locked.get("zip_sha256")) != (
        "0.0.7", "0e605a7280b3c14d52049c5b42c7a85d3001dc98a7fa61f5822364686d13e16b"
    ):
        fail("original ZIP provenance drift before acquisition")
    if len(locked["unityfs_members"]) != 1 or locked["unityfs_members"][0].get("sha256") != "bf3ddb70d42084c5847a1038abffb759956fe3e9cb4cfc1bbb657b746a14895b":
        fail("original UnityFS provenance drift before acquisition")
    # This is the ONLY original-byte acquisition and requires a separately
    # authorized exact-head workflow_dispatch. Never called on --self-test/PR.
    path = owner.c7.download(PACKAGE, args.cache)
    observed = owner.c7.inventory(PACKAGE, path)
    owner.verify_lock(lock, authority, PACKAGE, observed)
    if importlib.metadata.version("UnityPy") != owner.c7.UNITYPY_VERSION:
        fail("UnityPy parser version drift")
    idx = owner.c7.AssetIndex()
    idx.load(path, observed)
    report = minimal_report(idx, lock)
    verify_minimal(report, lock)
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "LEADFACTORY_MINIMAL.json"
    if target.exists():
        target.unlink()
    owner.write_json(target, report)
    # Assert again against the exact bytes that would have been written.
    verify_minimal(json.loads(target.read_text(encoding="utf-8")), lock)
    print("LEADFACTORY_MINIMAL_CAPTURE_LOCAL_ONLY_PASS")
    print("No artifacts, ZIP, bundle, or JSON published; proof is not runtime PASS")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", choices=(TARGET,))
    p.add_argument("--cache", type=Path, default=Path("c3-owner-packages"))
    p.add_argument("--out", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.out or args.target != TARGET:
        p.error("an explicit --target LeadFactory and --out are required")
    try:
        run_capture(args)
        return 0
    except Exception as exc:
        # Do not print exception payloads originating in serialized objects.
        print("LEADFACTORY_MINIMAL_CAPTURE_BLOCKED: " + type(exc).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
