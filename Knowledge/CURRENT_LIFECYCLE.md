# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`, `Current/Projektstatus_S1.42AE_CANDIDATE.json`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AE_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/CODEREBIRTH.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
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

Runtime-test S1.42AE before any successor work:

1. replace/import the active Gale profile using the canonical repository helper;
2. play one normal run far enough for ordinary moon/interior generation;
3. upload the complete fresh `LogOutput.log` using the exact S1.42AE uploader in the candidate record;
4. verify dependency versions, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keyset logs, final 18-Moon-curves `x0.5` marker, no contract refusal, and no new fatal/project-critical regression;
5. accept or reject S1.42AE from that evidence.

Do not build a successor before this runtime evidence is evaluated.
