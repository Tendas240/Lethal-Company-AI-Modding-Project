# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`, `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`, `Current/Projektstatus_S1.42AE_CANDIDATE.json`  
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
- Current import-recovery analysis: `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`
- Machine state: `Current/Projektstatus_S1.42AE_CANDIDATE.json`
- Snapshot: `ProfileSources/S1.42AE/`

Automated archive QC vs accepted S1.42AC found exactly one changed existing member (`export.r2x`) and exactly one added member (the S1.42AE DLL), with zero mod-state/addition/removal/config changes.

## Three invalid S1.42AE launch attempts

All three user launch attempts are classified as **invalid Gale/Thunderstore import-materialization evidence, not candidate runtime rejections**. In every case BepInEx failed in the preloader before S1.42AE's own provider-contract validation could execute.

The second console capture exposed the actual package path used by `AutoHookGenPatcher`:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

It then failed through `FixPluginTypesSerialization` with the same missing binding dependency and fatal preloader termination.

The third attempt used v2.3 and exposed a separate proof bug before game launch: inherited `Get-ZipEntryText` produced a non-terminating Windows PowerShell 5.1 `New-Object` overload error for the five-argument `System.IO.StreamReader` construction. The resulting empty export text caused `Get-RequiredCriticalMaterializationPaths` parameter binding to fail, but the importer continued with no effective critical dependency list and printed a false-positive import success. The subsequent game start then failed in the same missing SoundAPI binding preloader path.

Consequences remain:

- S1.42AE is still the active runtime candidate;
- S1.42AC is still the accepted rollback baseline;
- the S1.42AE runtime gate remains open;
- no successor is armed;
- no complete fresh valid S1.42AE `LogOutput.log` has been ingested;
- a new profile build is not justified by these import/preloader incidents.

## S1.42AC control confirmation

A fresh SHA-verified S1.42AC import was used as an A/B control because S1.42AC carries the same SoundAPI dependency family. Both expected nested SoundAPI DLLs were physically present and non-empty after that import. The user then started S1.42AC and reached the main menu normally.

The supplied control log showed `Preloader finished`, `Chainloader ready`, `Chainloader started`, `DawnLib 0.9.25`, `DawnLib.DuskMod 0.9.25`, `CodeRebirth 1.6.9`, and `loaforcsSoundAPI 2.0.12` loading, with no Fatal marker. It was intentionally not ingested through `RuntimeInbox/Current/` because `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AE` and doing so would misattribute the control evidence.

Authority for this diagnostic conclusion:

`Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`

## Current Gale recovery

The canonical launcher is now `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, revision:

`2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`

It preserves the validated v2.2 UI/import workflow and the recursive package-root semantics, while additionally replacing `Get-ZipEntryText` in-memory so the export text is obtained through a direct four-argument `System.IO.StreamReader` constructor. Read/constructor failure, empty export text, package-name parse drift, missing roots, zero matches, empty DLLs, duplicate matches, or unexpected underlying v2.2 helper drift all fail closed.

For an export containing `loaforc-loaforcsSoundAPI_LethalCompany`, v2.4 requires exactly two critical contracts before success:

- exactly one non-empty `me.loaforc.soundapi.dll` recursively below the `loaforc-loaforcsSoundAPI` Gale package root;
- exactly one non-empty `me.loaforc.soundapi.lethalcompany.dll` recursively below the `loaforc-loaforcsSoundAPI_LethalCompany` package root.

Permanent regression gate:

`RepositoryTools/gale_import_helper_validator.py`

See `Knowledge/GALE_PROFILE_WORKFLOW.md`.

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

Re-import and runtime-test the **same S1.42AE artifact** after the v2.4 repository/CI repair is merged:

1. run the canonical `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` launcher;
2. require revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`;
3. require successful non-empty `export.r2x` text decoding before dependency derivation;
4. require the two SoundAPI critical contracts to be derived and listed;
5. require exactly one non-empty base SoundAPI DLL and one non-empty LC-binding DLL inside their respective Gale package roots;
6. only after that proof, start the game and reach main menu/lobby;
7. play one normal run far enough for ordinary moon/interior generation;
8. upload the complete fresh `LogOutput.log` using the exact S1.42AE uploader in the candidate record;
9. verify dependency versions, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keyset logs, final 18-Moon-curves `x0.5` marker, no contract refusal, and no new fatal/project-critical regression;
10. accept or reject S1.42AE from that valid evidence.

Do not build a successor before this runtime evidence is evaluated.
