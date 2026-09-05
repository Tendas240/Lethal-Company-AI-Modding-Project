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

## First S1.42AE launch attempt

The first user launch attempt is classified as **invalid import/materialization evidence, not a candidate rejection**.

BepInEx failed during preloader initialization before S1.42AE's own provider-contract validation could run. The observed chain was `FixPluginTypesSerialization` `System.TypeInitializationException` with an inner `System.IO.FileNotFoundException` for the expected local Gale dependency DLL:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

Consequences:

- S1.42AE remains the active runtime candidate;
- S1.42AC remains the accepted rollback baseline;
- the S1.42AE runtime gate remains open;
- no successor is armed;
- no complete fresh valid S1.42AE `LogOutput.log` has been ingested;
- a new profile build is not justified by this incident.

The canonical Gale replacement/import helper was hardened in commit `7b8a23e57ad0ac678314564da1f22638362b97f3` with revision `2026-09-05-import-uia-v2.2-materialization-proof`. Besides exact `export.r2x` identity, it now requires the project-critical SoundAPI dependency files referenced by the export to be physically present and non-empty before import success is declared. See `Knowledge/GALE_PROFILE_WORKFLOW.md`.

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

1. replace/import S1.42AE using the canonical repository Gale helper hardened by commit `7b8a23e57ad0ac678314564da1f22638362b97f3`;
2. require the helper to positively verify exact imported `export.r2x` identity plus both required SoundAPI DLLs as physically present and non-empty;
3. only after that proof, start the game and reach main menu/lobby;
4. play one normal run far enough for ordinary moon/interior generation;
5. upload the complete fresh `LogOutput.log` using the exact S1.42AE uploader in the candidate record;
6. verify dependency versions, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keyset logs, final 18-Moon-curves `x0.5` marker, no contract refusal, and no new fatal/project-critical regression;
7. accept or reject S1.42AE from that valid evidence.

Do not build a successor before this runtime evidence is evaluated.
