<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`, `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R1 — ShyGuy Isolation Diagnostic Owner Type Resolution Repair — RUNTIME DIAGNOSTIC FAILED / REPAIR ANALYSIS REQUIRED / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z`  
SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`  
Candidate: `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`  
Runtime failure: `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`

R1 successfully repaired the predecessor's owner type-resolution defect: runtime derived `LethalMin.Pikmin.PikminType` from the exact `WithdrawPikminFromOnion` metadata contract. The diagnostic then failed a later strict complex-owner prevalidation because `ElevatorMod.Patches.EndlessElevator` was absent at runtime. DIAG1 marked itself invalid and rolled back all Harmony hooks owned by its instance, so ShyGuy-only isolation was not active during gameplay.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R1**, failed diagnostic evidence.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R1_RUNTIME_FAILURE_AWAITING_REPAIR_ANALYSIS` and guards the accepted S1.42AH baseline.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains runtime/evidence attribution only; it is not acceptance authority and does not mean a new runtime test is pending.

## R1 runtime decision

The R1 guard contract fails on any DIAG1 invalidation/rollback or required target-install failure. This run contains both `[DIAG1_INVALID]` and `[DIAG1_INSTALL_ROLLED_BACK]`, therefore R1 is explicitly failed and must not be rerun unchanged.

The operator-observed non-ShyGuy enemies are consistent with the confirmed rollback rather than a bypass through an armed isolation layer.

The operator also observed that a Shy Guy triggered inside did not follow outside. That behavior is separately explained by inherited Scopophobia configuration `Can Exit Facility = false`, which is present in accepted S1.42AH and R1. Inside-to-outside pursuit is not the same contract as the current BCMER interior-only spawn correction and remains a separate scope unless explicitly selected.

## Canonical Gale workflow

Whenever a later runtime candidate is actually armed, import/replace it only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. There is no active runtime candidate now, so this routing rule does not authorize a gameplay run by itself.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. Neither failed diagnostic can replace it.

## Exact next project action

Perform focused repository-native analysis of why the R1 complex-owner installer required exact runtime type `ElevatorMod.Patches.EndlessElevator` although that type was absent in the actual runtime profile, and why the static/materialized gates did not reject that mismatch. Determine the exact installed ownership contract before changing source or static validation. Do not guess a replacement CLR name, do not rerun DIAG1/R1 unchanged, and do not run the deferred full-normal S1.42AI gate yet.
