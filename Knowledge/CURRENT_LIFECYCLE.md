<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`, `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1 — ShyGuy Isolation Diagnostic — RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1 ShyGuy Isolation.r2z`  
SHA-256: `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`  
Parent: `S1.42AI`  
Candidate: `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`  
Runtime failure decision: `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`

The build/static/materialization stage passed, but the first runtime diagnostic did not arm successfully. Exact owner prevalidation could not resolve the hardcoded type name `LethalMin.PikminType`; DIAG1 marked itself invalid and then removed all Harmony hooks owned by its diagnostic Harmony instance. The fail-closed rollback was correct, but the gameplay portion of that run therefore cannot validate the intended isolation contract.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1**, failed diagnostic evidence.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1_RUNTIME_FAILURE_AWAITING_REPAIR` and guards the accepted **S1.42AH** profile/SHA while no runtime candidate is active.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1` remains the last runtime-evidence attribution pointer only; it does not make DIAG1 active or accepted.

## Diagnostic runtime result

The runtime log records the exact failed owner prevalidation, `[DIAG1_INVALID]`, and `[DIAG1_INSTALL_ROLLED_BACK]`. The analyzer also records non-ShyGuy enemy activity after rollback. Operator observation from the run was: additional enemies spawned; two Shy Guys were observed inside; no Shy Guy was observed outside; the two observed interior Shy Guys did not come outside during the observed period.

Those observations are useful evidence, but they cannot prove the S1.42AI interior-only correction because DIAG1 was no longer armed. Use `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` for the bounded decision and repair contract.

## Required repair

`Patches/S142AIDiag1Isolation/PackageOwnerGuards.cs` currently hardcodes `ResolveRequiredType("LethalMin.PikminType")`. The successor repair must derive the exact `List<T>` generic argument from the declared `LethalMin.Onion.WithdrawPikminFromOnion` metadata and retain fail-closed exactness instead of replacing the string with another guessed namespace.

`AnalysisTools/validate_s142ai_diag1_static.py` must be strengthened in the same repair so it proves the CLR generic-argument contract against the materialized LethalMin DLL, not merely the decompiled short spelling `List<PikminType>`.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**.

## Canonical Gale workflow

Whenever a future repaired successor becomes ready for runtime testing, use the repository-driven **Gale v2.4** replacement/import workflow in `Knowledge/GALE_PROFILE_WORKFLOW.md`, implemented by `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The ready-to-test response must supply that repository-driven import one-liner together with the exact successor-build-specific one-line PowerShell runtime-log uploader. No Gale import or new gameplay run is required while the DIAG1 repair is still pending.

## Exact next project action

Repair the DIAG1 owner type-resolution contract and the static gate, validate the repair repository-native, then build a successor diagnostic candidate. Do **not** rerun the current S1.42AI-DIAG1 profile unchanged. A new gameplay test is requested only after a repaired successor candidate exists and all static/materialized gates are green.
