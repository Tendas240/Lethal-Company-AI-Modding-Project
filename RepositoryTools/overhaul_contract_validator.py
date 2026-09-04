#!/usr/bin/env python3
"""Strict post-overhaul validation against the frozen pre-overhaul contract."""
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
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def exists(value: str) -> bool:
    return (ROOT / value).exists()


def require(value: str, label: str = "required path") -> None:
    if not exists(value):
        error(f"{label} missing: {value}")


def load(path: str) -> dict:
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"invalid JSON {path}: {exc}")
        return {}


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )


def git_has(spec: str) -> bool:
    return git("cat-file", "-e", spec).returncode == 0


def concrete_path(value: str) -> bool:
    """True only for references intended to identify a currently existing path.

    The knowledge map also contains globs, placeholders and lifecycle destinations;
    those are search/process notation rather than broken file references.
    """
    if not value:
        return False
    if any(mark in value for mark in ("*", "?", "<", ">", "...")):
        return False
    if re.fullmatch(r"Current/\d+", value):
        return False
    if re.search(r"\.json\.[A-Za-z_][A-Za-z0-9_]*$", value):
        return False
    if value in {"Profiles/DO_NOT_BUILD.r2z", "RuntimeInbox/Current/LogOutput.log"}:
        return False
    return True


def check_requirements() -> None:
    req = load("Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json")
    status = str(req.get("status", ""))
    if "VALIDATED" not in status or not ({"EXECUTED", "IMPLEMENTED"} & set(status.split("_"))):
        error(f"requirements status is not executed/implemented + validated: {status!r}")
    for path in req.get("required_artifacts", []):
        if isinstance(path, str):
            require(path, "requirements artifact")
        else:
            error(f"invalid required_artifacts entry: {path!r}")


def check_backup_ordering() -> None:
    m = load("Current/PRE_OVERHAUL_BACKUP_MANIFEST.json")
    checks = {
        "verification_result": "PASS",
        "source_repository": "Tendas240/Lethal-Company-AI-Modding-Project",
        "frozen_source_commit_sha": FROZEN_COMMIT,
        "frozen_source_tree_sha": FROZEN_TREE,
        "backup_repository": BACKUP_REPOSITORY,
        "backup_is_historical_read_only": True,
        "backup_is_current_source_of_truth": False,
        "standalone_backup_gate_passed": True,
    }
    for key, wanted in checks.items():
        if m.get(key) != wanted:
            error(f"backup manifest {key} drift: {m.get(key)!r} != {wanted!r}")
    if not git_has(f"{FROZEN_COMMIT}^{{commit}}"):
        error("frozen pre-overhaul commit absent from Git history")
    else:
        got = git("rev-parse", f"{FROZEN_COMMIT}^{{tree}}").stdout.strip()
        if got != FROZEN_TREE:
            error(f"frozen tree mismatch: {got}")
    if not git_has(f"{BACKUP_GATE_COMMIT}^{{commit}}"):
        error("backup-gate commit absent from history")
        return
    if git("merge-base", "--is-ancestor", BACKUP_GATE_COMMIT, "HEAD").returncode != 0:
        error("backup-gate commit is not an ancestor of HEAD")
    if not git_has(f"{BACKUP_GATE_COMMIT}:Current/PRE_OVERHAUL_BACKUP_MANIFEST.json"):
        error("backup-gate commit lacks backup manifest")
    for path in (
        "Knowledge",
        "Current/PROJECT_KNOWLEDGE_MAP.json",
        "Current/BUILD_LINEAGE.json",
        "Current/DOCUMENT_AUTHORITY.json",
        "RepositoryTools/knowledge_architecture_validator.py",
    ):
        if git_has(f"{BACKUP_GATE_COMMIT}:{path}"):
            error(f"structural IA artifact existed before/at backup gate: {path}")


def check_history_authority() -> None:
    banners = {
        "Current/02_TECHNICAL_BASELINE.md": "HISTORICAL MIXED SNAPSHOT — NOT GLOBAL CURRENT AUTHORITY",
        "Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md": "HISTORICAL ROADMAP SNAPSHOT — NOT CURRENT AUTHORITY",
        "OVERHAUL_START_HERE_ChatGPT.txt": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
        "Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
        "Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md": "EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED",
    }
    for path, marker in banners.items():
        require(path, "historical authority target")
        if exists(path) and marker not in (ROOT / path).read_text(encoding="utf-8")[:1800]:
            error(f"missing conspicuous historical/completion banner: {path}")
    authority = load("Current/DOCUMENT_AUTHORITY.json")
    classified = {
        x.get("path") for x in authority.get("historical_or_superseded", [])
        if isinstance(x, dict)
    }
    for path in banners:
        if path not in classified:
            error(f"authority registry does not classify {path}")
    drift = authority.get("code_comment_drift")
    if not isinstance(drift, dict) or drift.get("path") != "Patches/S139CompatibilityFixes/Plugin.cs":
        error("Plugin.cs historical comment drift is not explicitly classified")
    else:
        text = " ".join(map(str, drift.get("current_invariants", []))).lower()
        for needle in ("crawler", "bite limit 3", "puffer", "native cleanup"):
            if needle not in text:
                error(f"Plugin.cs comment-drift metadata lacks invariant: {needle}")
        if not drift.get("provenance_rule"):
            error("Plugin.cs comment-drift metadata lacks accepted-source provenance rule")


def check_live_state() -> None:
    state = load("Current/CURRENT_STATE.json")
    a = state.get("accepted_baseline", {})
    latest = state.get("latest_built_artifact", {})
    controllers = state.get("controllers", {})
    if a.get("build_id") != ACCEPTED_BUILD or a.get("sha256") != ACCEPTED_SHA:
        error("accepted baseline/SHA drift from S1.42AB")
    if latest.get("build_id") != LATEST_BUILD or latest.get("status") != "FORMALLY_REJECTED_NOT_PROMOTED":
        error("latest artifact drift: S1.42AC must remain formally rejected/not promoted")
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        error("unexpected active candidate or runtime test")
    spec = load("BuildSpecs/current.json")
    if spec.get("enabled") is not False:
        error("BuildSpecs/current.json unexpectedly enabled")
    if spec.get("base_profile") != a.get("profile") or spec.get("base_sha256") != ACCEPTED_SHA:
        error("BuildSpecs accepted-base guard drift")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    lineage = load("Current/BUILD_LINEAGE.json")
    known_builds = {b.get("id") for b in lineage.get("builds", []) if isinstance(b, dict) and b.get("id")}
    if active not in known_builds:
        error(f"runtime active-build controller points to unknown lineage build: {active!r}")
    if controllers.get("runtime_active_build") != active:
        error("runtime active-build controller disagrees with CURRENT_STATE")
    if controllers.get("build_enabled") is not False:
        error("CURRENT_STATE controllers.build_enabled unexpectedly true")
    for key in ("profile", "acceptance", "project_status", "runtime_evidence", "profile_sources", "file_index"):
        value = a.get(key)
        if not isinstance(value, str) or not exists(value):
            error(f"accepted baseline lacks readable {key}: {value!r}")
    require("ProfileSources/S1.42AB/export.r2x", "accepted readable profile export")


def check_map() -> None:
    km = load("Current/PROJECT_KNOWLEDGE_MAP.json")
    topics = {x.get("id"): x for x in km.get("topics", []) if isinstance(x, dict)}
    required_ids = {
        "accepted_baseline", "active_candidate_and_next_test", "build_pipeline",
        "gale_import", "runtime_upload_and_ingest", "bcmer", "interiors_and_lll",
        "enemy_spawn_baseline", "pikmin_enemy_compatibility", "jetpack", "coderebirth",
        "functional_microwave", "immortal_snail", "monitor_only_errors",
        "black_mesa_pikmin_routing", "roadmap_and_deferred_scopes", "patch_safety_policy",
        "repository_overhaul", "pre_overhaul_backup_and_recovery",
    }
    missing = sorted(required_ids - set(topics))
    if missing:
        error(f"knowledge map missing mandatory topics: {missing}")
    for tid, topic in topics.items():
        canonical = topic.get("canonical")
        if not isinstance(canonical, str) or not exists(canonical):
            error(f"topic {tid} canonical target missing: {canonical!r}")
        if not topic.get("aliases"):
            error(f"topic {tid} has no aliases")
        for field in ("machine_state", "evidence", "config_paths", "code_paths", "historical_sources"):
            for value in topic.get(field, []):
                if isinstance(value, str) and concrete_path(value) and not exists(value):
                    error(f"topic {tid}.{field} missing concrete path: {value}")
    if topics.get("roadmap_and_deferred_scopes", {}).get("canonical") != "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md":
        error("live roadmap routes to a superseded source")
    bootstrap = (ROOT / "START_HERE_ChatGPT_Masterprompt.txt").read_text(encoding="utf-8")
    if "Current/PROJECT_KNOWLEDGE_MAP.md" not in bootstrap:
        error("bootstrap does not directly route to the knowledge map")
    if len(bootstrap.encode("utf-8")) > 16000:
        error("bootstrap exceeds 16 KiB context guard")


def check_lineage_and_completion() -> None:
    lineage = load("Current/BUILD_LINEAGE.json")
    if lineage.get("current_accepted_build_id") != ACCEPTED_BUILD or lineage.get("active_candidate_build_id") is not None:
        error("BUILD_LINEAGE current lifecycle drift")
    for build in lineage.get("builds", []):
        if not isinstance(build, dict):
            continue
        for field in ("profile", "build_plan", "candidate_record", "decision_record", "runtime_evidence", "post_decision_analysis"):
            value = build.get(field)
            if isinstance(value, str) and concrete_path(value) and not exists(value):
                error(f"BUILD_LINEAGE {build.get('id')}.{field} missing: {value}")
    z = next((x for x in lineage.get("builds", []) if isinstance(x, dict) and x.get("id") == "S1.42Z"), {})
    if z.get("profile") != "Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z" or z.get("sha256") != "a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4":
        error("S1.42Z accepted provenance regression in BUILD_LINEAGE")
    execution = load("Current/OVERHAUL_EXECUTION_STATE.json")
    if execution.get("status") != "OVERHAUL_COMPLETE_VALIDATED" or execution.get("last_completed_phase") != 11:
        error("OVERHAUL_EXECUTION_STATE is not complete through phase 11")
    validation = load("Current/OVERHAUL_VALIDATION_RESULTS.json")
    if validation.get("status") not in {"FINAL_VALIDATION_PASS", "POST_ACCEPTANCE_REAUDIT_PASS"}:
        error("OVERHAUL_VALIDATION_RESULTS is not a PASS state")
    require("Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md", "final acceptance")
    if exists("Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md") and "PASS / COMPLETE / VALIDATED" not in (ROOT / "Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md").read_text(encoding="utf-8"):
        error("final acceptance is not marked PASS / COMPLETE / VALIDATED")
    migration = load("Current/REPOSITORY_MIGRATION_MANIFEST.json")
    if "moved_paths" not in migration or "deleted_paths" not in migration or not migration.get("deletion_decision"):
        error("migration manifest lacks move/delete accounting or rationale")


def check_canonical_paths() -> None:
    docs = [
        "README.md", "START_HERE_ChatGPT_Masterprompt.txt", "Current/00_CURRENT_STATE.md",
        "Current/01_HANDOVER_CORE.md", "Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md",
        "Current/PROJECT_KNOWLEDGE_MAP.md", "Current/BUILD_LINEAGE.md",
        "Current/DOCUMENT_AUTHORITY.md", "Current/REPOSITORY_MIGRATION_MANIFEST.md",
        "Current/CURRENT_STATE_TRANSITION_POLICY.md", "Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md",
    ]
    docs += [str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "Knowledge").glob("*.md")]
    if exists("Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md"):
        docs.append("Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md")
    prefixes = ("Current/", "Knowledge/", "BuildSpecs/", "RuntimeInbox/", "RuntimeEvidence/", "ProfileSources/", "Profiles/", "Patches/", "BuildSystem/", "RuntimeTools/", "RepositoryTools/", ".github/")
    for doc in docs:
        require(doc, "canonical document")
        if not exists(doc):
            continue
        for raw in re.findall(r"`([^`\n]+)`", (ROOT / doc).read_text(encoding="utf-8")):
            value = raw.strip().rstrip(".,;:")
            if not value.startswith(prefixes) or not concrete_path(value):
                continue
            if any(mark in value for mark in ("=", " -> ", ".md/.json")):
                continue
            if not exists(value):
                error(f"broken concrete internal path in {doc}: {value}")


def main() -> int:
    check_requirements()
    check_backup_ordering()
    check_history_authority()
    check_live_state()
    check_map()
    check_lineage_and_completion()
    check_canonical_paths()
    print("Frozen original overhaul-contract validation")
    print(f"errors={len(ERRORS)} warnings={len(WARNINGS)}")
    for item in WARNINGS:
        print("WARNING:", item)
    for item in ERRORS:
        print("ERROR:", item)
    if ERRORS:
        return 1
    print("PASS: completed repository satisfies frozen pre-overhaul contract checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())