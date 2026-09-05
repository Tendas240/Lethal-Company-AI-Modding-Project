# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`, `Current/Projektstatus_S1.42AE_CANDIDATE.json`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AE_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/CODEREBIRTH.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Knowledge/GALE_PROFILE_WORKFLOW.md`  
**Last-Validated:** 2026-09-05

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Machine state: `Current/Projektstatus_S1.42AC_ACCEPTED.json`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the accepted full-normal-stack gameplay/rollback baseline.

## Rejected predecessor

**S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED.**

S1.42AD failed closed because it expected `InteriorCurves=0`, while runtime exposed 18 Interior/tag curves. No `0.5` mutation executed. Rejection authority:

`Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`

## Active candidate

**S1.42AE — Functional Microwave Provider Contract Correction — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`
- Profile SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`
- DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`
- Successful build run: `33968217356`
- Automated build commit: `85e6caade0edd94ac5d7f409b9dd734fc8613f3f`
- Candidate record: `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`
- Correction analysis: `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`
- Machine state: `Current/Projektstatus_S1.42AE_CANDIDATE.json`
- Snapshot: `ProfileSources/S1.42AE/`

Automated archive QC vs accepted S1.42AC found exactly one changed existing member (`export.r2x`) and exactly one added member (the S1.42AE DLL), with zero mod-state/addition/removal/config changes.

## Two invalid S1.42AE launch attempts

Both user launch attempts are classified as **invalid Gale/Thunderstore import-materialization evidence, not candidate runtime rejections**. In both cases BepInEx failed in the preloader before S1.42AE's own provider-contract validation could execute.

The second console capture exposed the actual package path used by `AutoHookGenPatcher`:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

It then failed through `FixPluginTypesSerialization` with the same missing binding dependency and fatal preloader termination.

Consequences remain:

- S1.42AE is still the active runtime candidate;
- S1.42AC is still the accepted rollback baseline;
- the S1.42AE runtime gate remains open;
- no successor is armed;
- no complete fresh valid S1.42AE `LogOutput.log` has been ingested;
- a new profile build is not justified by either incident.

The first hardening, helper v2.2 in commit `7b8a23e57ad0ac678314564da1f22638362b97f3`, used a flat dependency path model. The second failure established that this model did not match Gale's preserved inner Thunderstore plugin subtree. It also exposed that `loaforc-loaforcsSoundAPI_LethalCompany` must imply the base `loaforc-loaforcsSoundAPI` materialization requirement even when the base dependency is not separately listed in Gale export metadata.

The current canonical launcher is therefore `RuntimeTools/ReplaceActiveGaleProfileV23.ps1`, revision `2026-09-05-import-uia-v2.3-recursive-package-materialization-proof`. It keeps the validated v2.2 UI/import behavior but requires exactly one non-empty expected DLL recursively within each required Gale package root, and fails closed on missing roots, missing/empty DLLs, or duplicates. See `Knowledge/GALE_PROFILE_WORKFLOW.md`.

## Corrected Functional Microwave contract

The user-authorized target remains `SpawnScale = 0.5`.

S1.42AE requires:

- CodeRebirth `1.6.9`;
- DawnLib/Dusk `0.9.25`;
- exact `code_rebirth:functional_microwave` provider;
- `PrioritiseMoons=true`;
- exact 18-key Moon/tag table;
- exact 18-key Interior/tag table;
- all curves valid.

Dusk 0.9.25 selection semantics under Moon priority are exact Moon -> exact Interior fallback -> matching Moon tags. The two tables are not combined. S1.42AE therefore logs/validates both tables and scales only the 18 Moon/tag curves by `0.5`; the 18 Interior curves are validation-only.

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt`:

`S1.42AE`

`BuildSpecs/current.json` is disabled after successful generation:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AE_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = S1.42AE candidate profile/SHA;
- no successor is armed.

## Exact next project action

Re-import and runtime-test the **same S1.42AE artifact** before any successor work:

1. run the canonical `RuntimeTools/ReplaceActiveGaleProfileV23.ps1` launcher;
2. require revision `2026-09-05-import-uia-v2.3-recursive-package-materialization-proof` to positively verify exact imported `export.r2x` identity;
3. require exactly one non-empty `me.loaforc.soundapi.dll` recursively below the `loaforc-loaforcsSoundAPI` Gale package root and exactly one non-empty `me.loaforc.soundapi.lethalcompany.dll` recursively below the `loaforc-loaforcsSoundAPI_LethalCompany` package root;
4. only after that proof, start the game and reach main menu/lobby;
5. play one normal run far enough for ordinary moon/interior generation;
6. upload the complete fresh `LogOutput.log` using the exact S1.42AE uploader in the candidate record;
7. verify dependency versions, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keyset logs, final 18-Moon-curves `x0.5` marker, no contract refusal, and no new fatal/project-critical regression;
8. accept or reject S1.42AE from that valid evidence.

Do not build a successor before this runtime evidence is evaluated.
