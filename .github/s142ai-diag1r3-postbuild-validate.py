#!/usr/bin/env python3
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

BUILD_COMMIT = "19914cff25cb768cffe22694e93df150e45bdd2f"
PROFILE = Path("Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z")
PROFILE_SHA = "13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768"
PLUGIN_SHA = "98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a"
PLUGIN = "BepInEx/plugins/Tendas-S142AIDiag1Isolation/S142AIDiag1Isolation.dll"
CONFIG = "BepInEx/config/tendas.s142ai.diag1.isolation.cfg"
WORKFLOW = ".github/workflows/s142ai-diag1r3-postbuild-validation.yml"
SCRIPT = ".github/s142ai-diag1r3-postbuild-validate.py"
VALIDATION_PROFILE = Path("ValidationArtifacts/S1.42AI-DIAG1R3.sdk8.validation.r2z")
STATIC_OUT = Path("ValidationArtifacts/diag1r3-static-out")
APPLICABILITY_OUT = Path("ValidationArtifacts/diag1r3-materialized-applicability.json")
REPORT_DIR = Path("ValidationArtifacts/diag1r3-materialized")


def fail(message):
    raise RuntimeError(message)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_text(args):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if p.returncode != 0:
        fail(f"{args[0]} failed ({p.returncode}) for {' '.join(args[1:])}: " + p.stderr.decode("utf-8", errors="replace")[-3000:])
    return p.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def normalize_il(text):
    text = re.sub(r"(?mi)^\s*//\s*MVID\s*:.*$", "// MVID: <NORMALIZED>", text)
    text = re.sub(r"(?mi)^\s*//\s*(?:PE|COFF)?\s*Timestamp\s*:.*$", "// Timestamp: <NORMALIZED>", text)
    text = re.sub(r"(?mi)^\s*//\s*Checksum\s*:.*$", "// Checksum: <NORMALIZED>", text)
    text = re.sub(r"(?mi)^\s*//\s*PDB.*$", "// PDB: <NORMALIZED>", text)
    return text


def zip_files(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        if len(names) != len(set(names)):
            fail(f"Duplicate ZIP members in {path}")
        return {n: z.read(n) for n in names}


def precheck():
    subprocess.run(["git", "merge-base", "--is-ancestor", BUILD_COMMIT, "HEAD"], check=True)
    changed = set(subprocess.check_output(["git", "diff", "--name-only", BUILD_COMMIT, "HEAD"], text=True).splitlines())
    if changed != {WORKFLOW, SCRIPT}:
        fail(f"Unexpected repository drift since R3 build commit: {sorted(changed)}")

    state = json.loads(Path("Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    if state.get("accepted_baseline", {}).get("build_id") != "S1.42AH":
        fail("Accepted baseline drifted before R3 post-build validation")
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        fail("R3 validation requires no active candidate and no outstanding runtime test")
    revision = state.get("selected_scope", {}).get("diagnostic_revision", {})
    if revision.get("build_id") != "S1.42AI-DIAG1R3":
        fail("CURRENT_STATE no longer identifies R3 as prepared successor")

    controller = json.loads(Path("BuildSpecs/current.json").read_text(encoding="utf-8"))
    expected_controller = {
        "enabled": True,
        "build_id": "S1.42AI-DIAG1R3",
        "base_profile": "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z",
        "base_sha256": "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2",
        "output_profile": str(PROFILE),
        "profile_name": "LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair",
    }
    for key, expected in expected_controller.items():
        if controller.get(key) != expected:
            fail(f"R3 controller drift for {key}: {controller.get(key)!r} != {expected!r}")

    active = Path("RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    if active != "S1.42AI-DIAG1R2":
        fail(f"Runtime attribution moved before R3 validation: {active!r}")

    result = json.loads(Path("Current/AUTO_BUILD_RESULT.json").read_text(encoding="utf-8"))
    expected_result = {
        "build_id": "S1.42AI-DIAG1R3",
        "base_profile": "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z",
        "base_sha256": "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2",
        "output_profile": str(PROFILE),
        "output_sha256": PROFILE_SHA,
        "snapshot_dir": "ProfileSources/S1.42AI-DIAG1R3",
    }
    for key, expected in expected_result.items():
        if result.get(key) != expected:
            fail(f"AUTO_BUILD_RESULT drift for {key}: {result.get(key)!r} != {expected!r}")
    if result.get("zip_members") != 337 or result.get("snapshot", {}).get("entries") != 337 or result.get("snapshot", {}).get("text_entries") != 331:
        fail("Unexpected R3 archive/snapshot counts")
    if any(result.get(k) != [] for k in ("mod_state_changes", "mod_additions", "mod_removals")):
        fail("R3 unexpectedly changes package state")

    if not PROFILE.is_file() or sha256_file(PROFILE) != PROFILE_SHA:
        fail("Canonical R3 profile missing or SHA mismatch")
    index = json.loads(Path("ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json").read_text(encoding="utf-8"))
    matches = [x for x in index if x.get("path") == PLUGIN]
    if len(matches) != 1 or matches[0].get("sha256") != PLUGIN_SHA or matches[0].get("text_snapshot") is not False:
        fail(f"R3 diagnostic DLL FILE_INDEX binding mismatch: {matches!r}")
    if Path("AnalysisEvidence/S1.42AI-DIAG1R3").exists():
        fail("R3 validation evidence already exists; refusing overwrite/reuse")
    print("PASS_PRECHECK_R3_POSTBUILD")


def compare():
    result = json.loads(Path("Current/AUTO_BUILD_RESULT.json").read_text(encoding="utf-8"))
    static = json.loads((STATIC_OUT / "STATIC_VALIDATION.json").read_text(encoding="utf-8"))
    applicability = json.loads(APPLICABILITY_OUT.read_text(encoding="utf-8"))
    if sha256_file(PROFILE) != PROFILE_SHA or result.get("output_sha256") != PROFILE_SHA or result.get("build_id") != "S1.42AI-DIAG1R3":
        fail("Canonical R3 profile/result binding mismatch")
    if static.get("status") != "PASS_PREBUILD_STATIC_GATE":
        fail(f"Exact SDK8 static gate not green: {static.get('status')}")
    expected_identity = {
        "asset": "ShyGuyDef",
        "enemyName": "Shy guy",
        "aiType": "ShyGuy.AI.ShyGuyAI",
        "comparison": "StringComparison.Ordinal",
    }
    identity = static.get("checks", {}).get("plugin_source", {}).get("shyguy_identity_contract")
    if identity != expected_identity:
        fail(f"Unexpected exact ShyGuy identity contract: {identity!r}")
    if applicability.get("status") != "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY" or applicability.get("materialized_profile_sha256") != PROFILE_SHA:
        fail("Canonical materialized applicability is not exact-profile green")

    c = zip_files(PROFILE)
    e = zip_files(VALIDATION_PROFILE)
    if set(c) != set(e) or len(c) != 337:
        fail("Canonical/green-gate archive member inventory mismatch")
    differing = [n for n in sorted(c) if c[n] != e[n]]
    unexpected = sorted(set(differing) - {"export.r2x", PLUGIN})
    if unexpected:
        fail(f"Unexpected canonical/green-gate byte differences: {unexpected}")

    def normalize_export(data):
        text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        hits = [line for line in text.split("\n") if re.match(r"^\s*profileName\s*:", line)]
        if len(hits) != 1:
            fail(f"Expected exactly one profileName, found {len(hits)}")
        return re.sub(r"(?m)^(\s*)profileName\s*:.*$", r"\1profileName: <NORMALIZED>", text), hits[0].strip()

    cn, cname = normalize_export(c["export.r2x"])
    en, ename = normalize_export(e["export.r2x"])
    if cn != en:
        fail("export.r2x differs by more than profileName")
    if cname != "profileName: LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair" or ename != "profileName: LC V1 S1.42AI-DIAG1 ShyGuy Isolation":
        fail(f"Unexpected profileName pair: canonical={cname!r}, green={ename!r}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    canonical_dll = REPORT_DIR / "canonical.dll"
    green_dll = REPORT_DIR / "green-gate.dll"
    canonical_dll.write_bytes(c[PLUGIN])
    green_dll.write_bytes(e[PLUGIN])
    canonical_plugin_sha = hashlib.sha256(c[PLUGIN]).hexdigest()
    green_plugin_sha = hashlib.sha256(e[PLUGIN]).hexdigest()
    if canonical_plugin_sha != PLUGIN_SHA:
        fail(f"Canonical plugin SHA mismatch: {canonical_plugin_sha} != {PLUGIN_SHA}")
    if green_plugin_sha != static["checks"]["ephemeral_profile"]["plugin_sha256"]:
        fail("Green-gate plugin/result SHA mismatch")

    canonical_types = run_text(["ilspycmd", "-l", "c", str(canonical_dll)])
    green_types = run_text(["ilspycmd", "-l", "c", str(green_dll)])
    if canonical_types != green_types:
        fail("Canonical/green-gate diagnostic DLL class inventories differ")
    type_names = [line.strip()[6:].strip() for line in canonical_types.splitlines() if line.strip().startswith("Class ")]
    if not type_names:
        fail("Diagnostic DLL class inventory is empty")

    semantic_type_hashes = {}
    decompiled_sources = []
    for type_name in type_names:
        canonical_cs = run_text(["ilspycmd", "-t", type_name, str(canonical_dll)])
        green_cs = run_text(["ilspycmd", "-t", type_name, str(green_dll)])
        if canonical_cs != green_cs:
            diff = "".join(difflib.unified_diff(green_cs.splitlines(True), canonical_cs.splitlines(True), fromfile="green-gate.cs", tofile="canonical.cs", n=3))[:12000]
            fail(f"Decompiled C# semantic mismatch for {type_name}:\n{diff}")
        decompiled_sources.append(canonical_cs)
        canonical_il = normalize_il(run_text(["ilspycmd", "--ilcode", "-t", type_name, str(canonical_dll)]))
        green_il = normalize_il(run_text(["ilspycmd", "--ilcode", "-t", type_name, str(green_dll)]))
        if canonical_il != green_il:
            diff = "".join(difflib.unified_diff(green_il.splitlines(True), canonical_il.splitlines(True), fromfile="green-gate.il", tofile="canonical.il", n=3))[:12000]
            fail(f"Normalized IL semantic mismatch for {type_name}:\n{diff}")
        semantic_type_hashes[type_name] = hashlib.sha256(canonical_il.encode("utf-8")).hexdigest()

    all_source = "\n".join(decompiled_sources)
    for marker in ('ResolveRequiredType("LethalMin.PikminType")', 'ResolveRequiredType("ElevatorMod.Patches.EndlessElevator")'):
        if marker in all_source:
            fail(f"Canonical DLL decompiles with known-bad resolver: {marker}")
    for marker in ("[DIAG1_OWNER_TYPE_DERIVED]", "[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]", "[DIAG1_COMPLEX_TARGET_APPLICABLE]", "kite.ZelevatorCode", "ShyGuyDef", "Shy guy", "ShyGuy.AI.ShyGuyAI", "StringComparison.Ordinal"):
        if marker not in all_source:
            fail(f"Canonical DLL missing repaired runtime marker/binding: {marker}")

    # Do not reject unrelated diagnostic prose containing "Shy Guy". The regression contract is the
    # exact enemyName comparator. Source static validation proves the exact constant/comparator, and
    # per-type C#/normalized-IL identity above binds the canonical DLL semantically to that source build.
    if 'string.Equals(candidate.enemyName, "Shy Guy", StringComparison.Ordinal)' in all_source:
        fail("Canonical DLL contains known-bad ordinal enemyName comparator for 'Shy Guy'")
    exact_materialized_comparator = 'string.Equals(candidate.enemyName, "Shy guy", StringComparison.Ordinal)' in all_source

    cfg = c[CONFIG].decode("utf-8-sig")
    if "S1.42AI-DIAG1 Enabled = true" not in cfg:
        fail("Canonical DIAG1 config is not enabled")
    owner = static["checks"]["lethalmin_withdraw_clr_contract"]
    if owner.get("parameter_0_generic_argument") != "LethalMin.Pikmin.PikminType" or owner.get("parameter_0_generic_argument_same_assembly") is not True:
        fail("Metadata-derived LethalMin PikminType proof missing")
    compat = static["checks"]["endless_elevator_applicability"]
    expected_compat = {
        "applicability": "NOT_APPLICABLE_DEPENDENCY_ABSENT",
        "dependency_guid": "kite.ZelevatorCode",
        "provider_assembly": "kite.ZelevatorCode",
        "provider_type": "ElevatorMod.Patches.EndlessElevator",
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
    }
    for key, expected in expected_compat.items():
        if compat.get(key) != expected:
            fail(f"Unexpected applicability contract for {key}: {compat.get(key)!r}")

    report = {
        "schema_version": 1,
        "status": "PASS_CANONICAL_DIAG1R3_MATERIALIZED_IDENTITY_APPLICABILITY_EQUIVALENCE",
        "build_id": "S1.42AI-DIAG1R3",
        "canonical_profile": str(PROFILE),
        "canonical_profile_sha256": PROFILE_SHA,
        "canonical_build_commit": BUILD_COMMIT,
        "validation_head_sha": os.environ.get("GITHUB_SHA"),
        "validation_workflow_run": int(os.environ["GITHUB_RUN_ID"]),
        "static_gate_status": static["status"],
        "materialized_applicability_status": applicability["status"],
        "shyguy_identity_contract": expected_identity,
        "known_bad_source_identity_literal_absent": True,
        "known_bad_materialized_enemyname_comparator_absent": True,
        "exact_materialized_enemyname_comparator_rendered_by_ilspy": exact_materialized_comparator,
        "canonical_plugin_sha256": canonical_plugin_sha,
        "green_gate_plugin_sha256": green_plugin_sha,
        "plugin_byte_identical": canonical_plugin_sha == green_plugin_sha,
        "plugin_class_inventory_identical": True,
        "plugin_decompiled_csharp_identical_per_type": True,
        "plugin_normalized_il_identical_per_type": True,
        "plugin_semantic_type_hashes": semantic_type_hashes,
        "zip_members": len(c),
        "byte_identical_members_excluding_plugin_and_export": len(c) - 2,
        "allowed_nonidentical_members": sorted(set(differing)),
        "export_difference": "profileName only",
        "metadata_derived_pikmin_type": owner["parameter_0_generic_argument"],
        "metadata_derived_pikmin_type_same_assembly": True,
        "endless_elevator_applicability": expected_compat,
        "runtime_state_modified": False,
    }
    (REPORT_DIR / "MATERIALIZED_VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (REPORT_DIR / "MATERIALIZED_VALIDATION.md").write_text(
        "# S1.42AI-DIAG1R3 materialized validation\n\n"
        f"- Status: **{report['status']}**\n"
        f"- Canonical profile SHA-256: `{PROFILE_SHA}`\n"
        f"- Canonical diagnostic DLL SHA-256: `{canonical_plugin_sha}`\n"
        f"- Green-gate diagnostic DLL SHA-256: `{green_plugin_sha}`\n"
        "- Exact ShyGuy identity: `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` / `StringComparison.Ordinal`\n"
        f"- Static gate: **{static['status']}**\n"
        f"- Materialized EndlessElevator applicability: **{applicability['status']}**\n"
        f"- Plugin decompiled C# identical for all {len(type_names)} classes: **true**\n"
        f"- Plugin normalized IL identical for all {len(type_names)} classes: **true**\n"
        f"- ZIP members: **{len(c)}**\n"
        "- All non-plugin members except `export.r2x`: byte-identical to the repaired SDK8 green-gate materialization\n"
        "- `export.r2x`: profileName-only difference\n"
        f"- Metadata-derived PikminType: `{owner['parameter_0_generic_argument']}`\n"
        f"- EndlessElevator dependency GUID: `{expected_compat['dependency_guid']}`\n",
        encoding="utf-8",
    )
    canonical_dll.unlink()
    green_dll.unlink()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"precheck", "compare"}:
        raise SystemExit("usage: s142ai-diag1r3-postbuild-validate.py {precheck|compare}")
    precheck() if sys.argv[1] == "precheck" else compare()
