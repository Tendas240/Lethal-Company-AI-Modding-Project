#!/usr/bin/env python3
"""Validate the completed repository against the original pre-overhaul contract.

This is deliberately stricter than the day-to-day knowledge validator. It checks
one-time migration obligations that were specified in the frozen pre-overhaul
repository: backup ordering, visible historical classification, semantic topic
coverage, accepted/current controller consistency, readable evidence/source
availability, bounded bootstrap routing, and final completion records.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_COMMIT = "5dbd0e637a480d8591773e422bbca4b0654cad20"
FROZEN_TREE = "0e17aac410cf600a164396b5586b5b50f084df22"
BACKUP_GATE_COMMIT = "2c1ab3be7db5474b0e08ff8a80c063a2c50224a4"
BACKUP_REPOSITORY = "Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904"
ACCEPTED_BUILD = "S1.42AB"
ACCEPTED_SHA = "3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca"
LATEST_BUILD = "S1.42AC"

errors: list[str] = []
warnings: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def path_exists(value: str) -> bool:
    return (ROOT / value).exists()


def require_path(value: str, context: str = "required path") -> None:
    if not path_exists(value):
        err(f"{context} missing: {value}")


def read_json(value: str) -> dict:
    p = ROOT / value
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        err(f"invalid JSON {value}: {exc}")
        return {}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if check and cp.returncode != 0:
        err(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp


def git_object_exists(spec: str) -> bool:
    return git("cat-file", "-e", spec, check=False).returncode == 0


def check_required_artifacts() -> None:
    req = read_json("Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json")
    status = str(req.get("status", ""))
    if "VALIDATED" not in status or not ("EXECUTED" in status or "IMPLEMENTED" in status):
        err(f"requirements status is not executed/implemented + validated: {status!r}")
    for item in req.get("required_artifacts", []):
        if isinstance(item, str):
            require_path(item, "requirements artifact")
        else:
            err(f"non-string required_artifacts entry: {item!r}")


def check_backup_and_ordering() -> None:
    manifest = read_json("Current/PRE_OVERHAUL_BACKUP_MANIFEST.json")
    if manifest.get("verification_result") != "PASS":
        err("standalone backup manifest verification_result is not PASS")
    if manifest.get("source_repository") != "Tendas240/Lethal-Company-AI-Modding-Project":
        err("backup manifest source repository drift")
    if manifest.get("frozen_source_commit_sha") != FROZEN_COMMIT:
        err("backup manifest frozen source commit drift")
    if manifest.get("source_tree_sha") != FROZEN_TREE:
        err("backup manifest frozen source tree drift")
    if manifest.get("backup_repository") != BACKUP_REPOSITORY:
        err("backup manifest standalone repository drift")

    if not git_object_exists(f"{FROZEN_COMMIT}^{{commit}}"):
        err("frozen pre-overhaul source commit is not present in repository history")
    else:
        tree = git("rev-parse", f"{FROZEN_COMMIT}^{{tree}}").stdout.strip()
        if tree != FROZEN_TREE:
            err(f"frozen source tree mismatch: {tree} != {FROZEN_TREE}")

    if not git_object_exists(f"{BACKUP_GATE_COMMIT}^{{commit}}"):
        err("backup-manifest gate commit is not present in repository history")
        return
    if git("merge-base", "--is-ancestor", BACKUP_GATE_COMMIT, "HEAD", check=False).returncode != 0:
        err("backup gate commit is not an ancestor of current HEAD")
    if not git_object_exists(f"{BACKUP_GATE_COMMIT}:Current/PRE_OVERHAUL_BACKUP_MANIFEST.json"):
        err("backup gate commit does not contain PRE_OVERHAUL_BACKUP_MANIFEST.json")

    # Structural IA artifacts must not already exist at the gate commit. This
    # proves the mandatory external-backup checkpoint preceded the migration.
    structural_at_gate = [
        "Knowledge",
        "Current/PROJECT_KNOWLEDGE_MAP.json",
        "Current/BUILD_LINEAGE.json",
        "Current/DOCUMENT_AUTHORITY.json",
        "RepositoryTools/knowledge_architecture_validator.py",
    ]
    for item in structural_at_gate:
        if git_object_exists(f"{BACKUP_GATE_COMMIT}:{item}"):
            err(f"structural overhaul artifact already existed at backup gate: {item}")


def check_visible_historical_classification() -> None:
    expected = {
        "Current/02_TECHNICAL_BASELINE.md": "HISTORICAL MIXED SNAPSHOT — NOT GLOBAL CURRENT AUTHORITY",
        "Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md": "HISTORICAL ROADMAP SNAPSHOT — NOT CURRENT AUTHORITY",
        "OVERHAUL_START_HERE_ChatGPT.txt": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
        "Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
        "Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
    }
    for path, marker in expected.items():
        require_path(path, "historical-classification target")
        p = ROOT / path
        if p.exists():
            head = p.read_text(encoding="utf-8")[:1800]
            if marker not in head:
                err(f"missing conspicuous historical/completion banner in {path}")

    authority = read_json("Current/DOCUMENT_AUTHORITY.json")
    history = {
        x.get("path"): x for x in authority.get("historical_or_superseded", [])
        if isinstance(x, dict) and x.get("path")
    }
    for path in expected:
        if path not in history:
            err(f"document authority registry does not classify {path}")

    plugin = "Patches/S139CompatibilityFixes/Plugin.cs"
    drift = authority.get("code_comment_drift")
    if not isinstance(drift, dict) or drift.get("path") != plugin:
        err("accepted Plugin.cs stale-comment drift is not explicitly classified")
    else:
        invariants = " ".join(map(str, drift.get("current_invariants", []))).lower()
        for needle in ("crawler", "bite limit 3", "puffer", "native cleanup"):
            if needle not in invariants:
                err(f"Plugin.cs comment-drift authority lacks current invariant: {needle}")
        if not drift.get("provenance_rule"):
            err("Plugin.cs comment-drift authority lacks provenance rule for accepted source/binary alignment")


def check_current_state_and_controllers() -> None:
    state = read_json("Current/CURRENT_STATE.json")
    accepted = state.get("accepted_baseline", {})
    latest = state.get("latest_built_artifact", {})
    controllers = state.get("controllers", {})
    if accepted.get("build_id") != ACCEPTED_BUILD:
        err("CURRENT_STATE accepted build is not S1.42AB")
    if accepted.get("sha256") != ACCEPTED_SHA:
        err("CURRENT_STATE accepted SHA drift")
    if latest.get("build_id") != LATEST_BUILD:
        err("CURRENT_STATE latest built artifact is not S1.42AC")
    if latest.get("status") != "FORMALLY_REJECTED_NOT_PROMOTED":
        err("S1.42AC status drift: it must remain formally rejected/not promoted")
    if state.get("active_candidate") is not None:
        err("CURRENT_STATE unexpectedly has an active candidate")
    if state.get("runtime_test_outstanding") is not False:
        err("CURRENT_STATE unexpectedly has a runtime test outstanding")

    spec = read_json("BuildSpecs/current.json")
    if spec.get("enabled") is not False:
        err("BuildSpecs/current.json must remain disabled")
    if spec.get("base_profile") != accepted.get("profile"):
        err("build controller base profile does not match accepted baseline")
    if spec.get("base_sha256") != ACCEPTED_SHA:
        err("build controller base SHA does not match accepted baseline")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    if active != ACCEPTED_BUILD:
        err(f"RuntimeInbox/ACTIVE_BUILD.txt drift: {active!r}")
    if controllers.get("build_enabled") is not False:
        err("CURRENT_STATE controllers.build_enabled must be false")
    if controllers.get("runtime_active_build") != ACCEPTED_BUILD:
        err("CURRENT_STATE runtime_active_build drift")

    for key in ("profile", "acceptance", "project_status", "runtime_evidence", "profile_sources", "file_index"):
        value = accepted.get(key)
        if not isinstance(value, str) or not path_exists(value):
            err(f"accepted baseline readable source/evidence missing for {key}: {value!r}")
    require_path("ProfileSources/S1.42AB/export.r2x", "accepted readable profile export")


def check_knowledge_map() -> None:
    km = read_json("Current/PROJECT_KNOWLEDGE_MAP.json")
    topics = {t.get("id"): t for t in km.get("topics", []) if isinstance(t, dict)}
    required_ids = {
        "accepted_baseline",
        "active_candidate_and_next_test",
        "build_pipeline",
        "gale_import",
        "runtime_upload_and_ingest",
        "bcmer",
        "interiors_and_lll",
        "enemy_spawn_baseline",
        "pikmin_enemy_compatibility",
        "jetpack",
        "coderebirth",
        "functional_microwave",
        "immortal_snail",
        "monitor_only_errors",
        "black_mesa_pikmin_routing",
        "roadmap_and_deferred_scopes",
        "patch_safety_policy",
        "repository_overhaul",
        "pre_overhaul_backup_and_recovery",
    }
    missing = sorted(required_ids - set(topics))
    if missing:
        err(f"knowledge map missing required major topics: {missing}")
    for topic_id, topic in topics.items():
        canonical = topic.get("canonical")
        if not isinstance(canonical, str) or not path_exists(canonical):
            err(f"knowledge topic {topic_id} has missing canonical target: {canonical!r}")
        if not topic.get("aliases"):
            err(f"knowledge topic {topic_id} has no semantic aliases")
        for field in ("machine_state", "evidence", "config_paths", "code_paths", "historical_sources"):
            for value in topic.get(field, []):
                if isinstance(value, str) and not path_exists(value):
                    err(f"knowledge topic {topic_id}.{field} references missing path: {value}")

    roadmap = topics.get("roadmap_and_deferred_scopes", {})
    if roadmap.get("canonical") != "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md":
        err("live roadmap does not route to Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md")

    bootstrap = (ROOT / "START_HERE_ChatGPT_Masterprompt.txt").read_text(encoding="utf-8")
    if "Current/PROJECT_KNOWLEDGE_MAP.md" not in bootstrap:
        err("bootstrap does not route directly to PROJECT_KNOWLEDGE_MAP")
    if len(bootstrap.encode("utf-8")) > 16000:
        err("bootstrap exceeds 16 KiB bounded-context guard")
    # Bootstrap -> map -> canonical topic is at most two retrieval hops.
    for topic_id in required_ids & set(topics):
        if not topics[topic_id].get("canonical"):
            err(f"topic {topic_id} cannot be reached within <=3 hops")


def check_build_lineage_and_final_records() -> None:
    lineage = read_json("Current/BUILD_LINEAGE.json")
    if lineage.get("current_accepted_build_id") != ACCEPTED_BUILD:
        err("BUILD_LINEAGE current accepted build drift")
    if lineage.get("active_candidate_build_id") is not None:
        err("BUILD_LINEAGE unexpectedly has active candidate")
    for build in lineage.get("builds", []):
        if not isinstance(build, dict):
            continue
        bid = build.get("id", "?")
        for field in ("profile", "build_plan", "candidate_record", "decision_record", "runtime_evidence", "post_decision_analysis"):
            value = build.get(field)
            if isinstance(value, str) and value and not path_exists(value):
                err(f"BUILD_LINEAGE {bid}.{field} missing: {value}")
    z = next((b for b in lineage.get("builds", []) if isinstance(b, dict) and b.get("id") == "S1.42Z"), None)
    if not z:
        err("BUILD_LINEAGE lacks S1.42Z")
    else:
        if z.get("profile") != "Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z":
            err("S1.42Z lineage profile provenance regressed")
        if z.get("sha256") != "a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4":
            err("S1.42Z lineage SHA provenance regressed")

    execution = read_json("Current/OVERHAUL_EXECUTION_STATE.json")
    if execution.get("status") != "OVERHAUL_COMPLETE_VALIDATED":
        err("OVERHAUL_EXECUTION_STATE not complete/validated")
    if execution.get("last_completed_phase") != 11:
        err("OVERHAUL_EXECUTION_STATE last_completed_phase is not 11")
    validation = read_json("Current/OVERHAUL_VALIDATION_RESULTS.json")
    if validation.get("status") not in {"FINAL_VALIDATION_PASS", "POST_ACCEPTANCE_REAUDIT_PASS"}:
        err(f"OVERHAUL_VALIDATION_RESULTS status not PASS: {validation.get('status')!r}")
    final = (ROOT / "Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md").read_text(encoding="utf-8")
    if "PASS / COMPLETE / VALIDATED" not in final:
        err("final acceptance record is not marked PASS / COMPLETE / VALIDATED")

    migration = read_json("Current/REPOSITORY_MIGRATION_MANIFEST.json")
    if "moved_paths" not in migration or "deleted_paths" not in migration:
        err("migration manifest lacks moved/deleted path accounting")
    if not migration.get("deletion_decision"):
        err("migration manifest lacks deletion rationale")


def check_canonical_backtick_paths() -> None:
    docs = [
        "README.md", "START_HERE_ChatGPT_Masterprompt.txt",
        "Current/00_CURRENT_STATE.md", "Current/01_HANDOVER_CORE.md",
        "Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md",
        "Current/PROJECT_KNOWLEDGE_MAP.md", "Current/BUILD_LINEAGE.md",
        "Current/DOCUMENT_AUTHORITY.md", "Current/REPOSITORY_MIGRATION_MANIFEST.md",
        "Current/CURRENT_STATE_TRANSITION_POLICY.md",
        "Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md",
    ]
    docs.extend(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "Knowledge").glob("*.md"))
    audit = ROOT / "Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md"
    if audit.exists():
        docs.append("Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md")

    prefixes = (
        "Current/", "Knowledge/", "BuildSpecs/", "RuntimeInbox/", "RuntimeEvidence/",
        "ProfileSources/", "Profiles/", "Patches/", "BuildSystem/", "RuntimeTools/",
        "RepositoryTools/", ".github/",
    )
    for doc in docs:
        require_path(doc, "canonical document")
        p = ROOT / doc
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for raw in re.findall(r"`([^`\n]+)`", text):
            value = raw.strip().rstrip(".,;:")
            if not value.startswith(prefixes):
                continue
            if any(x in value for x in ("*", "?", "=", " -> ", ".md/.json")):
                continue
            if not path_exists(value):
                err(f"broken internal backtick path in {doc}: {value}")


def main() -> int:
    check_required_artifacts()
    check_backup_and_ordering()
    check_visible_historical_classification()
    check_current_state_and_controllers()
    check_knowledge_map()
    check_build_lineage_and_final_records()
    check_canonical_backtick_paths()

    print("Original overhaul-contract validation")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for message in warnings:
        print("WARNING:", message)
    for message in errors:
        print("ERROR:", message)
    if errors:
        return 1
    print("PASS: completed repository satisfies the frozen pre-overhaul contract checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
