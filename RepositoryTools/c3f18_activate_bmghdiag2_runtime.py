#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ID = "S1.42AK-BMGHDIAG2"
PROFILE = "Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z"
PROFILE_SHA = "56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2"
DLL_SHA = "51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
ACTIVATION = "Current/172_S1.42AK_BMGHDIAG2_RUNTIME_ACTIVATION.md"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/BUILD_RESULT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, data) -> None:
    (ROOT / rel).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one replacement target, found {count}")
    return text.replace(old, new, 1)


# Fail closed on the exact main-integrated pre-activation state.
state = load_json("Current/CURRENT_STATE.json")
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(state["latest_built_artifact"]["build_id"] == "S1.42AK", "Latest normal artifact drift")
require(state["active_candidate"] is None, "Gameplay candidate must remain null")
require(state["runtime_test_outstanding"] is False, "Runtime test was already armed")
require(state["selected_scope"]["status"] == "PHASE_C3F18_BMGHDIAG2_MAIN_INTEGRATION_PASS_RUNTIME_ACTIVATION_NEXT", "Unexpected lifecycle phase")
require(state["controllers"]["runtime_active_build"] == "S1.42AK", "Runtime controller drift")
require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == "S1.42AK", "ACTIVE_BUILD drift")
current_spec = load_json("BuildSpecs/current.json")
require(current_spec["enabled"] is False, "Build controller must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller identity drift")
require(sha256_file(PROFILE) == PROFILE_SHA, "Main-integrated BMGHDIAG2 profile SHA mismatch")
build_result = load_json(BUILD_RESULT)
require(build_result["build_id"] == BUILD_ID, "Build result ID drift")
require(build_result["output_profile"] == PROFILE, "Build result profile drift")
require(build_result["output_sha256"] == PROFILE_SHA, "Build result profile SHA drift")
require(build_result["base_sha256"] == BASE_SHA, "Build result base SHA drift")

scope = state["selected_scope"]
old_diag = copy.deepcopy(scope["diagnostic_revision"])
require(old_diag["build_id"] == "S1.42AK-BMGHDIAG1", "Expected failed BMGHDIAG1 predecessor")
review = copy.deepcopy(scope["diagnostic_successor_review"])
require(review["build_id"] == BUILD_ID, "Expected BMGHDIAG2 successor review")
require(review["status"] == "EXACT_BYTES_MAIN_INTEGRATED_NOT_ARMED_NOT_ACCEPTED", "BMGHDIAG2 pre-activation status drift")
require(review["profile"] == PROFILE and review["profile_sha256"] == PROFILE_SHA, "BMGHDIAG2 identity drift")
require(review["diagnostic_dll_sha256"] == DLL_SHA, "BMGHDIAG2 DLL identity drift")
require(review["main_integrated"] is True and review["runtime_armed"] is False, "BMGHDIAG2 integration/arming drift")

# Preserve the failed predecessor as evidence, and promote only the successor record to active diagnostic runtime target.
scope["diagnostic_predecessor_revision"] = old_diag
review["status"] = "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED"
review["sha256"] = PROFILE_SHA
review["runtime_armed"] = True
review["activation_record"] = ACTIVATION
review["runtime_role"] = "DIAGNOSTIC_ONLY_BLACK_MESA_GREENHOUSE_FORCE_SELECTION_AND_READ_ONLY_ENTRANCE_OBSERVATION"
review["runtime_validation_status"] = "RUNTIME_TEST_OUTSTANDING_NOT_ACCEPTED"
scope["diagnostic_revision"] = review
del scope["diagnostic_successor_review"]
scope["diagnostic_build_plan"] = "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md"
scope["diagnostic_static_evidence"] = "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
scope["diagnostic_publication_evidence"] = "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["status"] = "PHASE_C3F18_BMGHDIAG2_RUNTIME_ACTIVE_TEST_OUTSTANDING"
scope["finding"] = (
    "S1.42AK-BMGHDIAG2 exact reviewed bytes are published on main and are now the active diagnostic runtime target for the bounded Black Mesa x Greenhouse qualification. "
    "The active profile remains SHA-256 56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2 with diagnostic DLL SHA-256 51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775. "
    "This is a direct diagnostic overlay over exact accepted S1.42AK, not a descendant of BMGHDIAG1. S1.42AK remains accepted/latest, active_candidate remains null and BuildSpecs/current.json remains disabled. RuntimeInbox/ACTIVE_BUILD.txt now identifies S1.42AK-BMGHDIAG2 solely for Gale target resolution and runtime-evidence attribution. Black Mesa x Greenhouse remains NOT_YET_PROVEN until the runtime evidence is ingested and decided."
)
scope["analysis_contract"] = (
    "Treat S1.42AK-BMGHDIAG2 as the active diagnostic runtime target only. Preserve exact profile/DLL identities, accepted S1.42AK, S1.42AB normalization, Black Mesa Dawn/native ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope. "
    "Do not promote or accept the diagnostic merely because it is active. The runtime gate must establish BMGHDIAG2 arming, exact Black Mesa Greenhouse selection, generation/topology/traversal evidence and absence of invalidating refusal/inconclusive markers."
)
scope["next_action"] = (
    "Import the exact active S1.42AK-BMGHDIAG2 profile through the canonical repository-driven Gale v2.4 launcher, run the bounded Black Mesa x Greenhouse diagnostic, exercise the main entrance and alternate entrance IDs 1, 2 and 3 in both directions where practical, then upload that run's exact BepInEx/LogOutput.log with the build-specific one-line uploader. Do not alter profile/config/package bytes during the test."
)
state["runtime_test_outstanding"] = True
state["controllers"]["runtime_active_build"] = BUILD_ID
state["next_action"] = scope["next_action"]
write_json("Current/CURRENT_STATE.json", state)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

# Register the exact diagnostic profile for repository/Gale integrity checks.
expected = load_json("Profiles/EXPECTED_HASHES.json")
entry = expected.get(PROFILE)
require(entry is None, "BMGHDIAG2 expected-hash entry already exists unexpectedly")
expected[PROFILE] = {
    "build_id": BUILD_ID,
    "sha256": PROFILE_SHA,
    "note": "Diagnostic-only active runtime target directly over accepted S1.42AK; canonical readable snapshot is ProfileSources/S1.42AK-BMGHDIAG2/. Not a gameplay lineage entry or gameplay base."
}
write_json("Profiles/EXPECTED_HASHES.json", expected)

# Add the active diagnostic to the current byte-integrity pending set.
integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("profiles", [])), "BMGHDIAG2 already appears as completed evidence")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("pending_profiles", [])), "BMGHDIAG2 already appears as pending evidence")
integrity["updated"] = "2026-09-24"
integrity["last_validated"] = "2026-09-24"
integrity["pending_profiles"].append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": "ProfileSources/S1.42AK-BMGHDIAG2/",
    "file_index": "ProfileSources/S1.42AK-BMGHDIAG2/FILE_INDEX.json",
    "export": "ProfileSources/S1.42AK-BMGHDIAG2/export.r2x",
    "build_plan": "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md",
    "build_result": BUILD_RESULT,
    "static_evidence": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/STATIC_VERIFICATION.json",
    "publication_evidence": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md",
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": "Exact reviewed/main-integrated BMGHDIAG2 bytes are runtime-armed solely for Black Mesa x Greenhouse diagnostic qualification; not accepted and not a gameplay base."
})
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMGHDIAG2 exact reviewed/main-integrated profile SHA-256 56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2 is now the active diagnostic runtime target pending Black Mesa x Greenhouse evidence; it remains unaccepted."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

# Human integrity index.
path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->", "integrity live marker")
text = replace_once(text, "**Last-Validated:** 2026-09-23", "**Last-Validated:** 2026-09-24", "integrity date")
text = replace_once(text, "- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.", "- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.\n- **S1.42AK-BMGHDIAG2** — active diagnostic runtime target over accepted S1.42AK; exact profile SHA-256 `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`; runtime evidence outstanding; not accepted and not a gameplay base.", "integrity pending list")
path.write_text(text, encoding="utf-8")

# Knowledge Map current anchor.
path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->", "knowledge-map live marker")
old = "BMGHDIAG2 is **on main but not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is a separate atomic runtime-activation checkpoint; no gameplay run is yet authorized."
new = "BMGHDIAG2 is **on main and now runtime-armed as a diagnostic-only target**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2`, no gameplay active candidate exists and one bounded diagnostic runtime test is outstanding. S1.42AK remains accepted/latest. The next action is the exact Black Mesa x Greenhouse runtime qualification plus upload of that run's `LogOutput.log`; activation itself does not accept or promote the diagnostic."
text = replace_once(text, old, new, "knowledge-map activation anchor")
path.write_text(text, encoding="utf-8")

# Current lifecycle router.
path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->", "lifecycle live marker")
text = replace_once(text, "BMGHDIAG2 is **published on main but not runtime-armed and not accepted**. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until a later explicit diagnostic runtime run.", "BMGHDIAG2 is **published on main and runtime-armed as the active diagnostic target, but remains not accepted**. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2`, `active_candidate = null`, and `runtime_test_outstanding = true`. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until this exact run is ingested and decided. Activation authority: `Current/172_S1.42AK_BMGHDIAG2_RUNTIME_ACTIVATION.md`.", "lifecycle BMGHDIAG2 status")
old_live = "- Active diagnostic runtime target: **none**.\n- Runtime test outstanding: **no**.\n- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 exact bytes integrated on main; separate runtime activation next**.\n- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.\n- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.\n- No gameplay successor or universal override is armed."
new_live = "- Active diagnostic runtime target: **S1.42AK-BMGHDIAG2**.\n- Runtime test outstanding: **yes — exact Black Mesa x Greenhouse diagnostic only**.\n- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 runtime active; evidence outstanding**.\n- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.\n- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2`.\n- No gameplay successor or universal override is armed; S1.42AK remains accepted/latest."
text = replace_once(text, old_live, new_live, "lifecycle live execution state")
old_next = "Prepare a separate atomic runtime-activation checkpoint for the exact main-integrated S1.42AK-BMGHDIAG2 profile SHA-256 56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2 / diagnostic DLL SHA-256 51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775. That later activation may point RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK-BMGHDIAG2 and set runtime_test_outstanding=true only while preserving accepted/latest normal baseline S1.42AK and keeping BuildSpecs/current.json disabled. Do not change gameplay/config/package bytes. The activation response must provide the repository-derived Gale import command and exact build-specific one-line PowerShell runtime-log uploader."
new_next = "Run the exact active S1.42AK-BMGHDIAG2 diagnostic on Black Mesa after importing it through the canonical Gale v2.4 launcher. Require `[BMGHDIAG2] ARMED`, exact Greenhouse selection, successful generation, topology IDs 0..3 and direct player traversal of the main entrance plus alternate IDs 1, 2 and 3 where practical; fail closed on refusal/inconclusive evidence. Then upload that run's exact `BepInEx/LogOutput.log` with the build-specific uploader from `Current/172_S1.42AK_BMGHDIAG2_RUNTIME_ACTIVATION.md`."
text = replace_once(text, old_next, new_next, "lifecycle next action")
old_perm = "No diagnostic is currently runtime-armed. BMGHDIAG2 exact bytes are integrated on main but remain non-runtime until a later explicit atomic activation step; only that later activation may authorize another gameplay run."
new_perm = "BMGHDIAG2 is now the explicitly runtime-armed diagnostic target under the direct-diagnostic authority chain. The canonical v2.4 launcher must resolve only the exact main-integrated profile/DLL identities above; this authorization ends at diagnostic evidence collection and does not promote the build."
text = replace_once(text, old_perm, new_perm, "lifecycle Gale status")
path.write_text(text, encoding="utf-8")

# Interiors topic: replace the stale BMGHDIAG1-only next-step statement with the live successor activation.
path = ROOT / "Knowledge/INTERIORS_AND_LLL.md"
text = path.read_text(encoding="utf-8")
old = "No runtime test is currently armed. The next step is source/root-cause analysis of `ValidateAssemblyHash` / `ResolveObservationContract` and, only if justified, a separately versioned minimal diagnostic repair. Do not rerun the refused BMGHDIAG1 bytes, change Greenhouse availability, duplicate-register Black Mesa, alter S1.42AB normalization, modify the B3 matrix, or open the separate Black-Mesa/Pikmin routing scope."
new = "That startup-provenance root cause has since been repaired by separately versioned `S1.42AK-BMGHDIAG2`, whose exact reviewed bytes are published on main and are now the active diagnostic runtime target. The bounded runtime test is outstanding: require `[BMGHDIAG2] ARMED`, exact Black Mesa Greenhouse selection, generation/topology evidence and direct entrance traversal before changing the matrix classification. Do not rerun BMGHDIAG1, change Greenhouse availability, duplicate-register Black Mesa, alter S1.42AB normalization, modify the B3 matrix, or open the separate Black-Mesa/Pikmin routing scope. Activation authority: `Current/172_S1.42AK_BMGHDIAG2_RUNTIME_ACTIVATION.md`."
text = replace_once(text, old, new, "interiors diagnostic status")
path.write_text(text, encoding="utf-8")

# Canonical activation evidence, including the exact user-facing command pair required by project policy.
gale_cmd = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
uploader_cmd = "$ErrorActionPreference='Stop';$build='S1.42AK-BMGHDIAG2';$log='C:\\Users\\Milan\\AppData\\Roaming\\com.kesomannen.gale\\lethal-company\\profiles\\LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic\\BepInEx\\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){throw \"Expected runtime log not found: $log\"};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){throw 'Runtime log is empty'};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMGHDIAG2]',[StringComparison]::Ordinal) -lt 0){throw 'Refusing upload: exact local LogOutput.log contains no [BMGHDIAG2] marker'};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback}};if(!$gh){throw 'GitHub CLI (gh) could not be resolved or bootstrapped'};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{$existing=(& $gh api \"repos/$repo/contents/$dest?ref=main\" --jq '.sha' 2>$null)}catch{};$payload=@{message=\"Upload $build runtime log ($localSha)\";content=[Convert]::ToBase64String($bytes);branch='main'};if($existing){$payload.sha=$existing};$json=$payload|ConvertTo-Json -Compress;$json|& $gh api --method PUT \"repos/$repo/contents/$dest\" --input -;if($LASTEXITCODE -ne 0){throw 'GitHub runtime-log upload failed'};Write-Host \"Uploaded exact $build LogOutput.log SHA-256 $localSha\" -ForegroundColor Green"
activation_text = f'''# S1.42AK-BMGHDIAG2 Runtime Activation\n\n**Date:** 2026-09-24  \n**Status:** PUBLISHED ON MAIN / ACTIVE DIAGNOSTIC RUNTIME TARGET / TEST OUTSTANDING / NOT ACCEPTED  \n**Accepted gameplay baseline:** S1.42AK — unchanged  \n**Diagnostic:** S1.42AK-BMGHDIAG2  \n**Diagnostic profile:** `{PROFILE}`  \n**Diagnostic SHA-256:** `{PROFILE_SHA}`  \n**Diagnostic DLL SHA-256:** `{DLL_SHA}`  \n**Exact parent:** accepted S1.42AK / `{BASE_SHA}`  \n**Main integration:** PR #144 / exact head `984feb61d9a23296ec111f377639c090cf4f952b` / merge `1dc18d5a37b5560d282174e11460672b508382ba`\n\n## Activation decision\n\nThe exact reviewed, byte-published and main-integrated BMGHDIAG2 artifact is authorized as the active runtime-evidence target for the single Black Mesa x Greenhouse qualification required by Phase C3F18. This is diagnostic-only. S1.42AK remains accepted/latest, `active_candidate` remains null, and `BuildSpecs/current.json` remains disabled.\n\nBMGHDIAG2 derives directly from exact accepted S1.42AK. BMGHDIAG1 is failed predecessor evidence only and is never a parent. The canonical Gale direct-diagnostic chain therefore resolves `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2` -> `CURRENT_STATE.selected_scope.diagnostic_revision` -> `{BUILD_RESULT}` -> exact accepted S1.42AK / `Current/AUTO_BUILD_RESULT.json`.\n\n## Exact runtime identities\n\n- profile SHA-256: `{PROFILE_SHA}`;\n- diagnostic DLL SHA-256: `{DLL_SHA}`;\n- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;\n- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;\n- archive/index members: 337;\n- package/config drift: zero.\n\n## Runtime qualification contract\n\nRun the exact diagnostic on **Black Mesa**. A sufficient run must establish all of the following:\n\n1. `[BMGHDIAG2] ARMED` appears without startup refusal;\n2. `[BMGHDIAG2] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool=<N>->1` appears;\n3. DunGen completes without exhausted retries or fatal generation abort;\n4. `[BMGHDIAG2] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4` appears;\n5. the player normally enters and exits through the main entrance;\n6. alternate IDs 1, 2 and 3 are directly traversed by the player; bidirectional use should be obtained where practical;\n7. no severe clipping or inaccessible required entrance geometry is observed at exercised endpoints;\n8. no new severe/persistent target-attributable routing or NavMesh failure is present;\n9. no `[BMGHDIAG2] REFUSED` or `TOPOLOGY_INCONCLUSIVE` marker invalidates the run.\n\nSuccessful native teleport alone must not be overclaimed as visual geometry proof. The separate Black-Mesa/Pikmin routing-recovery scope remains closed during this diagnostic.\n\n## Exact Gale replacement/import one-liner\n\n```powershell\n{gale_cmd}\n```\n\nThe launcher must resolve the direct diagnostic chain above and verify the exact downloaded profile SHA before Gale import. Follow its numeric old-profile selection and explicit `y` deletion confirmation; do not manually substitute another profile.\n\n## Exact build-specific runtime-log uploader\n\nAfter the gameplay run is complete, run this single PowerShell line. It resolves/bootstrap `gh`, authenticates if required, verifies the exact BMGHDIAG2 local `LogOutput.log` by path/non-empty content/marker, computes its SHA-256, and creates or replaces `RuntimeInbox/Current/LogOutput.log` on `main` without a local repository clone.\n\n```powershell\n{uploader_cmd}\n```\n\nThe normal runtime-ingest workflow then attributes the evidence to BMGHDIAG2 through `RuntimeInbox/ACTIVE_BUILD.txt`. If the run has already completed, do not repeat gameplay merely because upload remains outstanding.\n\n## Preserved boundaries\n\n- S1.42AK remains accepted/latest;\n- S1.42AB InteriorWeightNormalization remains unchanged;\n- Black Mesa remains Dawn/native-owned and is not duplicate-registered;\n- Greenhouse availability remains unchanged;\n- the 30x53 B3 matrix remains unchanged until evidence justifies reclassification;\n- Shatteredrooms x Experimentation/Embrion remain untouched;\n- no universal interior override or Black-Mesa/Pikmin routing repair is authorized.\n\n## Evidence attribution and rollback\n\nRuntime evidence must be uploaded while `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2`. Runtime-active status never promotes the diagnostic. Rollback remains exact accepted S1.42AK through the same canonical Gale replacement workflow after the diagnostic gate is decided.\n'''
(ROOT / ACTIVATION).write_text(activation_text, encoding="utf-8")

print("PASS: staged exact BMGHDIAG2 runtime activation without changing gameplay/config/package/profile bytes")
