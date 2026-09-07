from __future__ import annotations

import hashlib
import json
import os
import subprocess
import zipfile
from pathlib import Path

BUILD_ID = "S1.42AH"
TITLE = "Mouth Dog Pikmin Dual Prevention"
BASE_PROFILE = Path("Profiles/LC V1 S1.42AF Microwave Fix.r2z")
BASE_SHA = "6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0"
PROFILE = Path("Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z")
PROFILE_NAME = "LC V1 S1.42AH Mouth Dog Fix"
DLL_ARCHIVE_PATH = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
PLAN = Path("BuildSpecs/S1.42AH_PLAN.md")
CANDIDATE = Path("Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md")
PROJECT_STATUS = Path("Current/Projektstatus_S1.42AH_CANDIDATE.json")
SOURCE_ROOT = "ProfileSources/S1.42AH/"
FILE_INDEX = Path("ProfileSources/S1.42AH/FILE_INDEX.json")
RUN_ID = int(os.environ["GITHUB_RUN_ID"])
BUILD_COMMIT_TOKEN = "__BUILD_COMMIT__"


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def validate_source_contract() -> None:
    source = Path("Patches/S139CompatibilityFixes/Plugin.cs").read_text(encoding="utf-8")
    required = [
        'AccessTools.TypeByName("LethalMin.MouthDogPikminEnemy")',
        'AccessTools.TypeByName("LethalMin.PikminAI")',
        'typeof(EnemyAI).IsAssignableFrom(pikminAiType)',
        'typeof(MouthDogAI).GetMethod(',
        '"OnCollideWithEnemy"',
        'BindingFlags.DeclaredOnly',
        'new Type[] { typeof(Collider), typeof(EnemyAI) }',
        'collisionParameters[0].ParameterType == typeof(Collider)',
        'collisionParameters[1].ParameterType == typeof(EnemyAI)',
        'onCollideWithEnemy.GetMethodBody() != null',
        'priority = Priority.First',
        '!pikminAiType.IsInstanceOfType(collidedEnemy)',
        'MaxCollisionBlockLogs = 8',
        'Harmony.GetPatchInfo(target)',
    ]
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise SystemExit(f"Missing reviewed source-contract markers: {missing}")

    forbidden = [
        'typeof(EnemyAI).GetMethod("OnCollideWithEnemy"',
        'AccessTools.Method(typeof(EnemyAI), "OnCollideWithEnemy"',
    ]
    found_forbidden = [marker for marker in forbidden if marker in source]
    if found_forbidden:
        raise SystemExit(f"Forbidden broad MouthDog collision target marker present: {found_forbidden}")

    review = Path("Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md").read_text(encoding="utf-8")
    review_required = [
        "PikminAI : EnemyAI",
        "MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)",
        "Do not patch the position-only `DetectNoise()` path",
    ]
    missing_review = [marker for marker in review_required if marker not in review]
    if missing_review:
        raise SystemExit(f"Missing reviewed evidence markers: {missing_review}")

    vanilla = Path("SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt").read_text(encoding="utf-8")
    for marker in [
        "public override void OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)",
        "collidedEnemy.HitEnemy(2, null, playHitSFX: true)",
        "public override void OnCollideWithPlayer(Collider other)",
    ]:
        if marker not in vanilla:
            raise SystemExit(f"Vanilla source proof marker missing: {marker}")


def write_transient_spec() -> Path:
    spec = {
        "enabled": True,
        "build_id": BUILD_ID,
        "base_profile": str(BASE_PROFILE).replace("\\", "/"),
        "base_sha256": BASE_SHA,
        "output_profile": str(PROFILE).replace("\\", "/"),
        "profile_name": PROFILE_NAME,
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": [],
        "local_plugin_builds": [
            {
                "project": "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj",
                "configuration": "Release",
                "built_file": "Patches/S139CompatibilityFixes/bin/Release/netstandard2.1/S139CompatibilityFixes.dll",
                "archive_path": DLL_ARCHIVE_PATH,
            }
        ],
        "text_assertions": [
            {"path": "BepInEx/config/CodeRebirth.cfg", "contains": "Functional Microwave | Allow Editing Config = true"},
            {"path": "BepInEx/config/CodeRebirth.cfg", "contains": "Functional Microwave | Volume = 0.15"},
            {"path": "BepInEx/config/NoteBoxz.LethalMin.cfg", "contains": "Eyeless Dog Bite Cooldown = 5.5"},
            {"path": "BepInEx/config/NoteBoxz.LethalMin.cfg", "contains": "Eyeless Dog Bite Limit = 7"},
        ],
    }
    path = Path("/tmp/S1.42AH.json")
    path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    return path


def validate_build() -> tuple[str, str]:
    result = json.loads(Path("Current/AUTO_BUILD_RESULT.json").read_text(encoding="utf-8"))
    if result.get("build_id") != BUILD_ID:
        raise SystemExit(f"Unexpected build id: {result.get('build_id')}")
    if result.get("base_sha256") != BASE_SHA:
        raise SystemExit(f"Unexpected base hash: {result.get('base_sha256')}")

    expected_changed = {"export.r2x", DLL_ARCHIVE_PATH}
    changed = set(result.get("changed_existing_members", []))
    if changed != expected_changed:
        raise SystemExit(f"Unexpected changed archive members: {sorted(changed)}")
    for key in ["added_members", "mod_state_changes", "mod_additions", "mod_removals"]:
        if result.get(key) not in ([], None):
            raise SystemExit(f"Unexpected {key}: {result.get(key)}")

    profile_sha = result["output_sha256"]
    if sha256(PROFILE) != profile_sha:
        raise SystemExit("Profile SHA mismatch between builder result and file bytes")

    index = json.loads(FILE_INDEX.read_text(encoding="utf-8"))
    matches = [entry for entry in index if entry.get("path") == DLL_ARCHIVE_PATH]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one injected compatibility DLL; got {len(matches)}")
    dll_sha = matches[0]["sha256"]

    # Independent byte-preservation proof: member set must match the accepted AF base,
    # and every member except export.r2x + the compatibility DLL must be byte-identical.
    with zipfile.ZipFile(BASE_PROFILE, "r") as base_zip, zipfile.ZipFile(PROFILE, "r") as new_zip:
        base_names = set(base_zip.namelist())
        new_names = set(new_zip.namelist())
        if base_names != new_names:
            raise SystemExit(
                f"Archive member-set drift: added={sorted(new_names-base_names)}, removed={sorted(base_names-new_names)}"
            )
        drift = []
        for name in sorted(base_names - expected_changed):
            if base_zip.read(name) != new_zip.read(name):
                drift.append(name)
        if drift:
            raise SystemExit(f"Unrelated archive members are not byte-preserved: {drift[:20]}")

        dll_bytes = new_zip.read(DLL_ARCHIVE_PATH)
        if hashlib.sha256(dll_bytes).hexdigest() != dll_sha:
            raise SystemExit("Injected DLL bytes do not match FILE_INDEX SHA")
        for marker in [
            "MouthDogPikminGuard",
            "MouthDogVanillaCollisionGuard",
            "OnCollideWithEnemy",
            "PikminAI",
            "Exact target co-patch ownership",
        ]:
            if marker.encode("utf-8") not in dll_bytes and marker.encode("utf-16le") not in dll_bytes:
                raise SystemExit(f"Expected diagnostic/contract marker absent from built DLL: {marker}")

    print(f"S1.42AH profile SHA-256: {profile_sha}")
    print(f"S1.42AH compatibility DLL SHA-256: {dll_sha}")
    print("Archive byte-preservation: PASS (all non-identity/non-DLL members byte-identical to S1.42AF)")
    return profile_sha, dll_sha


def update_state(profile_sha: str, dll_sha: str) -> None:
    profile = str(PROFILE).replace("\\", "/")
    candidate = str(CANDIDATE).replace("\\", "/")
    plan = str(PLAN).replace("\\", "/")
    project_status = str(PROJECT_STATUS).replace("\\", "/")
    disabled_id = "IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION"

    disabled = {
        "enabled": False,
        "build_id": disabled_id,
        "base_profile": profile,
        "base_sha256": profile_sha,
        "output_profile": "Profiles/DO_NOT_BUILD.r2z",
        "profile_name": "DO_NOT_BUILD",
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": [],
        "local_plugin_builds": [],
        "text_assertions": [],
    }
    Path("BuildSpecs/current.json").write_text(json.dumps(disabled, indent=2) + "\n", encoding="utf-8")
    Path("RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

    state_path = Path("Current/CURRENT_STATE.json")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    latest = {
        "build_id": BUILD_ID,
        "title": TITLE,
        "status": "BUILD_PASS_RUNTIME_VALIDATION_OUTSTANDING",
        "profile": profile,
        "sha256": profile_sha,
        "candidate_record": candidate,
        "project_status": project_status,
        "build_plan": plan,
        "profile_sources": SOURCE_ROOT,
        "file_index": str(FILE_INDEX).replace("\\", "/"),
        "workflow_run": RUN_ID,
        "build_commit": BUILD_COMMIT_TOKEN,
        "plugin_dll_sha256": dll_sha,
        "parent": "S1.42AF",
    }
    active = dict(latest)
    active["status"] = "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
    state["latest_built_artifact"] = latest
    state["active_candidate"] = active
    state["runtime_test_outstanding"] = True
    scope = state["selected_scope"]
    scope["status"] = "BUILT_ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
    scope["candidate_build_id"] = BUILD_ID
    scope["profile"] = profile
    scope["sha256"] = profile_sha
    scope["candidate_record"] = candidate
    scope["project_status"] = project_status
    scope["build_plan"] = plan
    scope["implementation_commit"] = "486678d311be9b63d5f4581a27714885cbe55310"
    scope["finding"] = (
        "S1.42AH implements the PASS-reviewed dual prevention-only MouthDog contract from exact accepted S1.42AF. "
        "The build changes only export.r2x profile identity and the cumulative S139CompatibilityFixes DLL; all other archive members are byte-preserved. "
        "Runtime acceptance is now outstanding and must prove both protected Dog -> Pikmin paths plus native reverse/player/neighbor lifecycle behavior."
    )
    state["next_action"] = (
        "Import S1.42AH with the canonical Gale v2.4 replacement helper and run the full-normal MouthDog/Pikmin regression gate from Current/139. "
        "Deliberately provoke MouthDog/Pikmin collision, explicitly command/throw Pikmin onto the MouthDog for reverse-direction latch/attack/death/unlatch/task cleanup, "
        "verify MouthDog -> player and non-Pikmin neighbor behavior, repeat protected collisions, then upload the complete fresh S1.42AH LogOutput.log with the build-specific uploader in Current/139. "
        "Do not accept S1.42AH from build/startup success alone."
    )
    state["controllers"]["build_enabled"] = False
    state["controllers"]["build_id"] = disabled_id
    state["controllers"]["build_base_profile"] = profile
    state["controllers"]["build_base_sha256"] = profile_sha
    state["controllers"]["runtime_active_build"] = BUILD_ID
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lineage_path = Path("Current/BUILD_LINEAGE.json")
    lineage = json.loads(lineage_path.read_text(encoding="utf-8"))
    lineage["active_candidate_build_id"] = BUILD_ID
    lineage["latest_built_artifact_id"] = BUILD_ID
    lineage["builds"] = [b for b in lineage.get("builds", []) if b.get("id") != BUILD_ID]
    lineage["builds"].append({
        "id": BUILD_ID,
        "title": TITLE,
        "status": "active-candidate",
        "parent": "S1.42AF",
        "profile": profile,
        "sha256": profile_sha,
        "build_plan": plan,
        "candidate_record": candidate,
        "project_status": project_status,
        "workflow_run": RUN_ID,
        "build_commit": BUILD_COMMIT_TOKEN,
        "safe_as_gameplay_base": False,
        "principal_feature": "dual prevention on exact LethalMin MouthDog adapter plus exact Vanilla MouthDogAI Pikmin collision path",
    })
    lineage.setdefault("feature_index", {})["MouthDog_to_Pikmin_dual_prevention_candidate"] = BUILD_ID
    invariant = (
        "S1.42AH is built directly from accepted S1.42AF, not rejected S1.42AG; only export.r2x identity and the cumulative compatibility DLL differ in the archive, "
        "and runtime acceptance is required before it can become a gameplay base."
    )
    if invariant not in lineage.setdefault("lineage_invariants", []):
        lineage["lineage_invariants"].append(invariant)
    lineage_path.write_text(json.dumps(lineage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    gale = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
    uploader = "$src=Join-Path $env:APPDATA 'com.kesomannen.gale\\lethal-company\\profiles\\LC V1 S1.42AH Mouth Dog Fix\\BepInEx\\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw \"Log not found: $src\"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@(\"$env:ProgramFiles\\GitHub CLI\\gh.exe\",\"$env:LOCALAPPDATA\\Programs\\GitHub CLI\\gh.exe\",\"${env:ProgramFiles(x86)}\\GitHub CLI\\gh.exe\")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@(\"$env:ProgramFiles\\GitHub CLI\\gh.exe\",\"$env:LOCALAPPDATA\\Programs\\GitHub CLI\\gh.exe\",\"${env:ProgramFiles(x86)}\\GitHub CLI\\gh.exe\")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api \"repos/$repo/contents/$dst\" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AH runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT \"repos/$repo/contents/$dst\" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}"

    PLAN.write_text(f"""# S1.42AH — Mouth Dog Pikmin Dual Prevention

**Status:** BUILT / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED  
**Parent:** exact accepted S1.42AF — Path-Length-Safe Microwave Packaging  
**Parent SHA-256:** `{BASE_SHA}`  
**Safety authority:** `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`

## Implemented risky-patch delta

`Patches/S139CompatibilityFixes/Plugin.cs` retains the exact `Priority.First` prevention Prefix on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and adds the reviewed exact `Priority.First` Prefix on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`.

The Vanilla override is skipped only when the actual `collidedEnemy` is identified by the validated runtime `LethalMin.PikminAI` type. Null and non-Pikmin `EnemyAI` collisions pass through unchanged. `DetectNoise`, `OnCollideWithPlayer`, base `EnemyAI.OnCollideWithEnemy`, and native Pikmin lifecycle are not patched.

## Built candidate identity

- Profile: `{profile}`
- Gale profile name: `{PROFILE_NAME}`
- Profile SHA-256: `{profile_sha}`
- Compatibility DLL SHA-256: `{dll_sha}`
- Atomic build workflow run: `{RUN_ID}`
- Build commit: `{BUILD_COMMIT_TOKEN}`
- Candidate record: `{candidate}`
- Exact archive delta vs S1.42AF: `export.r2x` plus `{DLL_ARCHIVE_PATH}` only.
- Added/removed archive members: none.
- Package/config changes: none.
- Independent byte-preservation check: every other archive member is byte-identical to S1.42AF.

Runtime acceptance remains outstanding.
""", encoding="utf-8")

    CANDIDATE.write_text(f"""# S1.42AH Build Candidate — Mouth Dog Pikmin Dual Prevention

**Date:** 2026-09-07  
**Status:** ACTIVE RUNTIME CANDIDATE / BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED  
**Accepted baseline:** S1.42AF — Path-Length-Safe Microwave Packaging

## Candidate identity

- Profile: `{profile}`
- Gale profile name: `{PROFILE_NAME}`
- Profile SHA-256: `{profile_sha}`
- Compatibility DLL: `{DLL_ARCHIVE_PATH}`
- Compatibility DLL SHA-256: `{dll_sha}`
- Atomic build workflow run: `{RUN_ID}`
- Build commit: `{BUILD_COMMIT_TOKEN}`
- Plan: `{plan}`
- Snapshot: `{SOURCE_ROOT}`

## Exact build delta

S1.42AH is built directly from accepted S1.42AF, never from rejected S1.42AG. Automated plus independent ZIP verification proves:

- changed existing members: `export.r2x` and `{DLL_ARCHIVE_PATH}` only;
- added members: none;
- removed members: none;
- package enable/version/add/remove changes: none;
- config changes: none;
- every unrelated archive member is byte-identical to S1.42AF.

## Patch contract

The cumulative plugin validates exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and exact declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`, validates `LethalMin.PikminAI : EnemyAI` at runtime, and installs both Prefixes at `Priority.First` only after the complete contract validates. A failed dual installation rolls back any local partial hook and installs no guessed fallback.

The collision Prefix returns `false` only for the supplied validated runtime `LethalMin.PikminAI`. Null/non-Pikmin EnemyAI pass through. `DetectNoise`, MouthDog -> player, base EnemyAI collision handling, and native Pikmin attack/latch/death/unlatch/task ownership remain untouched.

Build-time DLL inspection confirms both diagnostic families and bounded exact-target Harmony PatchInfo ownership logging are present.

## Runtime acceptance gate

Runtime acceptance must deliberately cover all of the following under the full normal stack:

1. provoke real MouthDog/Pikmin collision and require the bounded Vanilla collision-block marker;
2. require no MouthDog adapter `Biting N Pikmin`, `EnemyAttackMouth`, 2.5-second `GrabPikmin`, or Pikmin `HitEnemy(2)` processing from the Dog collision path;
3. explicitly command/throw Pikmin onto a MouthDog — passive followers do not count;
4. prove Pikmin latch/attack, MouthDog death, native death -> unlatch -> task finish -> follow/idle cleanup;
5. prove MouthDog -> player remains functional;
6. repeat protected collision opportunities;
7. verify non-Pikmin neighbor behavior remains unfiltered;
8. preserve ordinary noise-position response and S1.42AF contracts;
9. require both patch-install markers, bounded collision marker(s), no new project-patch errors, no `Work state with no task assigned!` burst, no `Leader is null when following`, and no fatal/retry flood attributable to the patch.

A noise-driven lunge toward an audible Pikmin position is not itself a failure.

## Exact ready-to-test commands

Canonical Gale v2.4 replacement/import one-liner:

```powershell
{gale}
```

After the test, upload the complete fresh S1.42AH log with this exact self-contained one-liner:

```powershell
{uploader}
```

## Acceptance boundary

S1.42AH is build-safe only. S1.42AF remains the sole accepted gameplay base until the runtime gate above passes.
""", encoding="utf-8")

    project = {
        "schema_version": 4,
        "date": "2026-09-07",
        "repository_is_source_of_truth": True,
        "accepted_baseline": state["accepted_baseline"],
        "active_runtime_candidate": active,
        "runtime_gate": {
            "adapter_path_protection": "MUST_PASS",
            "vanilla_collision_block_marker": "MUST_APPEAR",
            "mouthdog_pikmin_bite_grab": "MUST_BE_0",
            "mouthdog_pikmin_hit_enemy_2": "MUST_BE_0",
            "reverse_direction_explicit_command_or_throw": "REQUIRED",
            "pikmin_latch_attack": "MUST_REMAIN_FUNCTIONAL",
            "mouthdog_death_unlatch_task_cleanup": "MUST_REMAIN_FUNCTIONAL",
            "mouthdog_to_player": "MUST_REMAIN_FUNCTIONAL",
            "non_pikmin_neighbor_behavior": "MUST_REMAIN_FUNCTIONAL",
            "repetition": "REQUIRED",
            "noise_position_pursuit": "ALLOWED_NOT_A_FAILURE_BY_ITSELF",
            "work_state_warning_burst": "MUST_BE_0",
            "leader_null_following": "MUST_BE_0",
            "project_patch_errors": "MUST_BE_0",
            "fatal": "MUST_BE_0",
        },
        "archive_gate": {
            "parent": "S1.42AF",
            "changed_existing_members": ["export.r2x", DLL_ARCHIVE_PATH],
            "added_members": [],
            "removed_members": [],
            "unrelated_members_byte_preserved": True,
            "profile_sha256": profile_sha,
            "plugin_dll_sha256": dll_sha,
        },
        "controllers": {
            "buildspec_current_enabled": False,
            "buildspec_current_id": disabled_id,
            "buildspec_base_profile": profile,
            "buildspec_base_sha256": profile_sha,
            "runtime_active_build": BUILD_ID,
            "successor_armed": False,
        },
        "exact_next_step": state["next_action"],
    }
    PROJECT_STATUS.write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lifecycle_path = Path("Knowledge/CURRENT_LIFECYCLE.md")
    lifecycle = lifecycle_path.read_text(encoding="utf-8")
    if str(CANDIDATE).replace("\\", "/") not in lifecycle.splitlines()[5]:
        lifecycle = lifecycle.replace(
            "`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`,",
            "`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`,",
            1,
        )
    replacement = f"""## Latest built artifact

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**

- Parent: accepted S1.42AF, not rejected S1.42AG.
- Profile: `{profile}`
- SHA-256: `{profile_sha}`
- Compatibility DLL SHA-256: `{dll_sha}`
- Candidate: `{candidate}`
- Build workflow run: `{RUN_ID}`
- Build commit: `{BUILD_COMMIT_TOKEN}`
- Exact archive delta: `export.r2x` + compatibility DLL only; every unrelated member byte-identical to S1.42AF.

S1.42AF remains the only accepted gameplay base until S1.42AH passes runtime validation.

## MouthDog successor Patch Safety Review

`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md` is implemented by S1.42AH. The candidate retains exact `DoCheckInterval()` prevention and adds the exact Pikmin-only Vanilla `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` prevention. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collisions and native Pikmin lifecycle remain outside the patch.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `{disabled_id}`.
- Guarded candidate: `{profile}` / `{profile_sha}`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.
- Runtime test outstanding: **yes**.
- No successor beyond S1.42AH is armed.

## Exact next project action

Import and runtime-test S1.42AH using `{candidate}`. Deliberately exercise both protected MouthDog -> Pikmin paths, explicitly command/throw Pikmin for the reverse-direction latch/attack/death/unlatch/task test, preserve MouthDog -> player/non-Pikmin/noise behavior, repeat the collision gate, and upload the complete fresh log using the build-specific uploader in the candidate record.

Do not accept S1.42AH from build/startup success alone.

"""
    lifecycle = replace_section(lifecycle, "## Latest built artifact", "## Future runtime acceptance", replacement)
    lifecycle_path.write_text(lifecycle, encoding="utf-8")

    pik_path = Path("Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md")
    pik = pik_path.read_text(encoding="utf-8")
    pik = pik.replace(
        "`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`,",
        "`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`,",
        1,
    )
    mouth = f"""## Mouth Dog / Eyeless Dog — S1.42AH active candidate

S1.42AF remains accepted. S1.42AG remains rejected partial-fix evidence. **S1.42AH is now the built active runtime candidate and is not accepted.**

S1.42AH implements the exact reviewed dual prevention architecture from `Current/138`: retain `Priority.First` prevention on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and add `Priority.First` prevention on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the supplied object is validated runtime `LethalMin.PikminAI`.

The complete target/signature/method-body/inheritance contract fails closed with no guessed fallback. The adapter stays enabled. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collision behavior and native Pikmin attack/latch/death/unlatch/task ownership remain unchanged.

Candidate: `{candidate}`  
Profile SHA-256: `{profile_sha}`  
DLL SHA-256: `{dll_sha}`

The archive was built directly from S1.42AF. Only `export.r2x` and the cumulative compatibility DLL differ; all unrelated members are byte-identical.

Runtime acceptance must deliberately prove the protected collision marker, absence of adapter/grab/HitEnemy mutation, explicit reverse-direction Pikmin command/throw latch/attack/death cleanup, MouthDog -> player, non-Pikmin neighbor behavior, repetition and clean logs. Noise-position pursuit alone is not failure evidence.

## Current lifecycle

- accepted: S1.42AF;
- latest built: S1.42AH, build pass / active candidate / not accepted;
- active candidate: S1.42AH;
- runtime test pending: yes;
- successor beyond S1.42AH: not armed.

"""
    pik = replace_section(pik, "## Mouth Dog / Eyeless Dog — current boundary", "## CodeRebirth utility kills", mouth)
    pik_path.write_text(pik, encoding="utf-8")

    lineage_md_path = Path("Current/BUILD_LINEAGE.md")
    lineage_md = lineage_md_path.read_text(encoding="utf-8")
    lineage_md = lineage_md.replace(
        "- **Latest built artifact:** S1.42AG — Mouth Dog Pikmin One-Way Protection — **runtime rejected / partial fix**.\n- **Active candidate:** none.\n- **Next build:** none armed; controller is idle on accepted S1.42AF while targeted analysis of the remaining Mouth Dog targeting/attack path is required.",
        f"- **Latest built artifact:** S1.42AH — {TITLE} — **build pass / active runtime candidate / not accepted**.\n- **Active candidate:** S1.42AH.\n- **Accepted gameplay baseline:** S1.42AF remains unchanged until runtime acceptance.\n- **Next build:** none armed; runtime validation of S1.42AH is outstanding.",
        1,
    )
    row = f"| S1.42AH | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** | Dual exact MouthDog adapter + Vanilla Pikmin collision prevention built directly from accepted S1.42AF; only profile identity and cumulative compatibility DLL differ. |\n"
    if "| S1.42AH |" not in lineage_md:
        anchor = "| S1.42AG | **RUNTIME REJECTED / PARTIAL FIX**"
        pos = lineage_md.index(anchor)
        line_end = lineage_md.index("\n", pos) + 1
        lineage_md = lineage_md[:line_end] + row + lineage_md[line_end:]
    section = f"""### S1.42AH — active Mouth Dog Pikmin dual prevention candidate

- Parent: accepted S1.42AF, never rejected S1.42AG.
- Profile: `{profile}`
- SHA-256: `{profile_sha}`
- DLL SHA-256: `{dll_sha}`
- Candidate: `{candidate}`
- Plan: `{plan}`
- Build workflow run: `{RUN_ID}`
- Build commit: `{BUILD_COMMIT_TOKEN}`
- Archive delta: `export.r2x` + compatibility DLL only; all other members byte-identical to S1.42AF.
- Status: build pass / runtime validation outstanding / not accepted.

"""
    if "### S1.42AH — active Mouth Dog Pikmin dual prevention candidate" not in lineage_md:
        insert = lineage_md.index("## Feature/fix lookup")
        lineage_md = lineage_md[:insert] + section + lineage_md[insert:]
    lineage_md_path.write_text(lineage_md, encoding="utf-8")

    run("python", "RepositoryTools/render_current_navigation.py")


def main() -> None:
    if sha256(BASE_PROFILE) != BASE_SHA:
        raise SystemExit("Accepted S1.42AF base profile hash mismatch; refusing build")
    validate_source_contract()
    run("python", "BuildSystem/test_profile_builder.py")
    spec = write_transient_spec()
    run("python", "BuildSystem/profile_builder.py", str(spec))
    profile_sha, dll_sha = validate_build()
    update_state(profile_sha, dll_sha)
    Path("/tmp/s142ah_meta.json").write_text(
        json.dumps({"profile_sha256": profile_sha, "plugin_sha256": dll_sha, "workflow_run": RUN_ID}),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
