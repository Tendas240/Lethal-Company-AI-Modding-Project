# S1.42AI-DIAG1R1 Minimal Guard Contract

**Status:** CURRENT RUNTIME CONTRACT FOR REPAIRED DIAGNOSTIC SUCCESSOR  
**Parent contract:** `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`  
**Owner-resolution repair authority:** `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` plus the repaired `Patches/S142AIDiag1Isolation/PackageOwnerGuards.cs` and strengthened `AnalysisTools/validate_s142ai_diag1_static.py`.

S1.42AI-DIAG1R1 preserves the exact DIAG1 isolation/gameplay contract. The only intended diagnostic revision is the fail-closed owner-type-resolution repair: `LethalMin.Onion.WithdrawPikminFromOnion` is resolved declared-only, the real `List<T>` argument is derived from CLR method metadata, `T` must identify `PikminType` in the same LethalMin assembly as exact `LethalMin.Onion` / `LethalMin.Leader`, and that exact `Type` object is used for the owner lookup.

The materialized static gate proves the actual generic argument is `LethalMin.Pikmin.PikminType`; this string is evidence, not a new runtime hardcoding.

## Runtime success boundary

A successful R1 diagnostic run must show the repaired owner contract arms rather than rolls back, all approved DIAG1 isolation layers install, no isolation-bypass marker identifies a live non-ShyGuy `EnemyAI`, no unexpected non-ShyGuy enemy is observed, and the exact Shy Guy identity remains observable. Any owner-target invalidation, DIAG1 invalidation/rollback, target-install failure, non-ShyGuy bypass, or broad shared-spawn/network regression fails the diagnostic.

This diagnostic cannot accept the deferred full-normal S1.42AI gate. S1.42AH remains the sole accepted gameplay baseline until an explicit later runtime decision changes that state.
