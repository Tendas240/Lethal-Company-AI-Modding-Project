# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-05

This file intentionally no longer duplicates the full project history or technical baseline. Durable facts belong in the registered `Knowledge/` topics and build/runtime evidence.

## Current gameplay gate

- **Accepted baseline:** S1.42AC — BCMER EventType Equal Distribution.
- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Fresh acceptance runtime: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the accepted full-normal-stack gameplay/rollback baseline.

## Active runtime candidate

**S1.42AE — Functional Microwave Provider Contract Correction — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`
- SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`
- Candidate: `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`
- Provider analysis: `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`
- Import-recovery analysis: `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`
- Plan: `BuildSpecs/S1.42AE_PLAN.md`
- Build workflow run: `33968217356`
- Build commit: `85e6caade0edd94ac5d7f409b9dd734fc8613f3f`
- DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`

The user-authorized target remains Functional Microwaves **half as often** (`SpawnScale = 0.5`). S1.42AE corrects rejected S1.42AD's provider contract: it validates exact 18 Moon/tag and 18 Interior/tag curves, logs both keysets, and scales only the 18 Moon/tag curves. Interior curves are validation-only.

S1.42AD remains rejected history and is not a build/gameplay base.

## Import/materialization blocker

Three S1.42AE game launches have failed before the candidate runtime gate. All are **invalid import/materialization evidence, not S1.42AE runtime rejections**.

The second and third game launches failed with `AutoHookGenPatcher` / `FixPluginTypesSerialization` unable to consume:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

S1.42AE's Microwave provider-contract code was not reached.

The third attempt additionally proved that v2.3's apparent successful materialization result was a **false positive**. The inherited `Get-ZipEntryText` emitted a non-terminating Windows PowerShell 5.1 `New-Object` overload error for its five-argument `StreamReader`; dependency derivation then received empty `ExpectedExportText`, emitted another non-terminating error, and the importer continued with no effective critical dependency list.

A fresh SHA-verified S1.42AC control import physically produced both nested SoundAPI DLLs. S1.42AC then passed the BepInEx preloader and reached the main menu normally. This isolates the current blocker to the Gale import/materialization proof path rather than S1.42AE's Functional Microwave code.

Current analysis authority:

`Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`

## Current Gale recovery

The canonical launcher is now:

`RuntimeTools/ReplaceActiveGaleProfileV24.ps1`

revision:

`2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`

v2.4 preserves the validated v2.2 Gale UI/import behavior and recursive package-root checks, but additionally:

- replaces the failing export-text reader with a direct four-argument `System.IO.StreamReader` constructor;
- terminates on export-reader construction/read failure;
- terminates on empty/whitespace export text before dependency derivation;
- rejects null/empty `ExpectedExportText`;
- fails closed on SoundAPI package-name parse drift;
- requires an LC binding to derive exactly two critical contracts;
- requires exactly one non-empty base SoundAPI DLL and exactly one non-empty LC-binding DLL recursively inside their respective Gale package roots;
- fails closed on missing roots, zero matches, empty files, duplicate files, or unexpected v2.2 helper drift.

Permanent regression guard:

`RepositoryTools/gale_import_helper_validator.py`

No valid complete S1.42AE runtime log has been ingested yet. The candidate remains active; no successor is armed.

## Continuation authority

`Current/124_HANDOVER_S1.42AE_V23_SEGMENT3_NEXT.md` is preserved as the handover checkpoint that led into the now-completed v2.3 user-facing attempt. Its v2.3 continuation instruction is superseded for live work by:

`Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`

and the current lifecycle/state authorities.

## Exact next action

**The same S1.42AE artifact must be re-imported with v2.4 after the repair is merged and CI is green. Do not build a successor.**

1. Run the canonical `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` repository launcher.
2. Require successful non-empty `export.r2x` text decoding.
3. Require the helper to derive/list exactly two SoundAPI critical materialization contracts.
4. Require exactly one non-empty base SoundAPI DLL and one non-empty LC-binding DLL inside their respective package roots.
5. Do not start the game unless all of those checks pass.
6. Start normally and reach main menu/lobby.
7. Play one normal run far enough for normal moon/interior generation and ordinary gameplay.
8. Upload the complete fresh `LogOutput.log` with the exact S1.42AE uploader in the candidate record.
9. Evaluate the log before any successor work.

Required S1.42AE evidence:

- `S1.42AE CodeRebirth Microwave Spawn Tuning 1.0.0` loads;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, and Dusk `0.9.25` validation succeeds;
- armed marker appears for the Moon-registry-freeze lifecycle;
- provider marker reports `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`;
- both exact Moon and Interior keyset markers appear;
- final marker reports all 18 Moon/tag curves scaled by `0.5` and 18 Interior curves validation-only/not mutated;
- no S1.42AE refusal/error marker;
- normal startup/round generation/gameplay remains healthy;
- no new fatal/project-critical regression.

A single normal run is sufficient for this technical gate. Do not require a statistically meaningful observed Microwave count from that run; deterministic provider mutation is the primary half-frequency evidence.

Current controllers:

- `BuildSpecs/current.json` is disabled.
- controller id: `IDLE_AFTER_S1.42AE_BUILD_AWAITING_RUNTIME_VALIDATION`.
- guarded base: S1.42AE candidate profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AE`.

The response that releases this runtime test must include both the repository-driven Gale v2.4 replacement/import one-liner and the exact S1.42AE self-contained PowerShell one-line runtime-log uploader.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Independent deferred items include:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence.

## Topic routes

- Current lifecycle / next test: `Knowledge/CURRENT_LIFECYCLE.md`
- Roadmap/deferred scopes: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- CodeRebirth: `Knowledge/CODEREBIRTH.md`
- Microwave / Immortal Snail: `Knowledge/ITEM_TUNING.md`
- BCMER: `Knowledge/BCMER.md`
- Interiors / LLL / CullFactory: `Knowledge/INTERIORS_AND_LLL.md`
- Enemy-spawn baseline: `Knowledge/ENEMY_SPAWN_BASELINE.md`
- Pikmin/enemy compatibility: `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`
- Black Mesa/Pikmin routing: `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`
- Known monitor-only errors: `Knowledge/MONITOR_ONLY_ERRORS.md`
- Build/runtime/GitHub pipeline: `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`
- Gale import: `Knowledge/GALE_PROFILE_WORKFLOW.md`
- Build history: `Current/BUILD_LINEAGE.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Permanent guardrail

Do not reopen rejected builds or rewrite historical outcomes because older snapshots say `current`. Current authority is determined by `Current/CURRENT_STATE.json`, `Current/DOCUMENT_AUTHORITY.md`, the Knowledge Map, and the latest build-specific acceptance/rejection evidence.
