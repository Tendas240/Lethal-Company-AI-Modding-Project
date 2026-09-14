<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`, `AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.md`, `AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.json`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R1 — ShyGuy Isolation Diagnostic Owner Type Resolution Repair — RUNTIME DIAGNOSTIC FAILED / ENDLESSELEVATOR APPLICABILITY REPAIR LANDED / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z`  
SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`  
Candidate: `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`  
Runtime failure: `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`

R1 successfully repaired the predecessor's owner type-resolution defect: runtime derived `LethalMin.Pikmin.PikminType` from the exact `WithdrawPikminFromOnion` metadata contract. The diagnostic then failed a later strict complex-owner prevalidation because `ElevatorMod.Patches.EndlessElevator` was absent at runtime. DIAG1 marked itself invalid and rolled back all Harmony hooks owned by its instance, so ShyGuy-only isolation was not active during gameplay.

## Landed EndlessElevator applicability repair

The R1 failure cause is now repository-native proven and repaired. Exact LethalMinNightly `1.1.108` evidence binds `LethalMin.Compats.EndlessElevatorPatch` to `CompatClass("kite.ZelevatorCode")`, with applicability controlled by `Chainloader.PluginInfos.ContainsKey(pluginGUID)`. The foreign CLR target is exactly `[kite.ZelevatorCode]ElevatorMod.Patches.EndlessElevator`.

The permanent runtime contract is therefore:

- `kite.ZelevatorCode` absent: only this compat target is `NOT_APPLICABLE`; do not resolve the foreign type and do not invalidate the complex-owner layer.
- `kite.ZelevatorCode` present: the target is REQUIRED; exact provider assembly/type, exact LethalMin owner/signature and patch installation remain fail-closed.
- There is no generic `missing target => ignore` fallback.

PR #91 landed this repair on `main` at merge commit `ef3842e5e1766afdd5db77c232b34c0e7c7d3105`. Permanent DIAG1 static/materialized run `34887087467` is green on repair commit `5582d83b9c5404bfdfa50cb24636e9661800b71f`; the two later PR-head commits only removed the temporary repair workflow/helper and did not change the permanent six-file repair.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R1**, failed diagnostic evidence; its applicability failure cause is repaired in source, but the artifact itself remains failed and unaccepted.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R1_APPLICABILITY_REPAIR_LANDED_AWAITING_SUCCESSOR_DETERMINATION` and guards the accepted S1.42AH baseline.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains runtime/evidence attribution only; it is not acceptance authority and does not mean a new runtime test is pending.

## R1 runtime decision

The R1 guard contract fails on any DIAG1 invalidation/rollback or required target-install failure. That historical run contains both `[DIAG1_INVALID]` and `[DIAG1_INSTALL_ROLLED_BACK]`, therefore R1 remains explicitly failed and must not be rerun unchanged even though the failure cause has now been repaired in source.

The operator-observed non-ShyGuy enemies are consistent with the confirmed rollback rather than a bypass through an armed isolation layer.

The operator also observed that a Shy Guy triggered inside did not follow outside. That behavior is separately explained by inherited Scopophobia configuration `Can Exit Facility = false`, which is present in accepted S1.42AH and R1. Inside-to-outside pursuit is not the same contract as the current BCMER interior-only spawn correction and remains a separate scope unless explicitly selected.

## Canonical Gale workflow

Whenever a later runtime candidate is actually armed, import/replace it only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. There is no active runtime candidate now, so this routing rule does not authorize a gameplay run by itself.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. Neither failed diagnostic can replace it.

## Exact next project action

First verify this canonical Current/Lifecycle transition on the final `main` Exact-HEAD `Knowledge Architecture` gate. Only after that gate is green, determine repository-native whether a successor diagnostic build is required and permissible and, if so, its exact successor identity and controller transition. Do not build a successor or request gameplay before that determination. The full-normal S1.42AI gate remains deferred, not waived.
