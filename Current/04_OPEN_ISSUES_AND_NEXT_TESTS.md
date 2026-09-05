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
- Analysis: `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`
- Plan: `BuildSpecs/S1.42AE_PLAN.md`
- Build workflow run: `33968217356`
- Build commit: `85e6caade0edd94ac5d7f409b9dd734fc8613f3f`
- DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`

The user-authorized target remains Functional Microwaves **half as often** (`SpawnScale = 0.5`). S1.42AE corrects rejected S1.42AD's provider contract: it validates exact 18 Moon/tag and 18 Interior/tag curves, logs both keysets, and scales only the 18 Moon/tag curves. Interior curves are validation-only.

S1.42AD remains rejected history and is not a build/gameplay base.

## Import/materialization blocker

Two S1.42AE game launches have failed before the candidate runtime gate. Both are **invalid import/materialization evidence, not S1.42AE runtime rejections**.

The second console capture explicitly showed `AutoHookGenPatcher` trying to read:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

The local path did not exist, followed by `FixPluginTypesSerialization` `System.TypeInitializationException` / inner `System.IO.FileNotFoundException` and fatal BepInEx preloader termination. S1.42AE's Microwave provider-contract code was not reached.

The previous v2.2 Gale materialization sentinel used a flat path model and did not close the transitive dependency requirement. The current canonical launcher is now:

`RuntimeTools/ReplaceActiveGaleProfileV23.ps1`

revision:

`2026-09-05-import-uia-v2.3-recursive-package-materialization-proof`

For a binding-enabled export it requires, before import success:

- exactly one non-empty `me.loaforc.soundapi.dll` recursively inside the `loaforc-loaforcsSoundAPI` Gale package root;
- exactly one non-empty `me.loaforc.soundapi.lethalcompany.dll` recursively inside the `loaforc-loaforcsSoundAPI_LethalCompany` Gale package root.

Missing roots, zero matches, empty files, or duplicate matches fail closed. The base SoundAPI requirement is implied by the binding package even when Gale export metadata does not separately list the base package.

No valid complete S1.42AE runtime log has been ingested yet. The candidate remains active; no successor is armed.

## Exact next action

**The same S1.42AE artifact must be re-imported with v2.3 and tested. Do not build a successor.**

1. Run the canonical `RuntimeTools/ReplaceActiveGaleProfileV23.ps1` repository launcher.
2. Do not start the game unless it positively verifies exact `export.r2x` identity and both recursive SoundAPI package-root contracts.
3. Start normally and reach main menu/lobby.
4. Play one normal run far enough for normal moon/interior generation and ordinary gameplay.
5. Upload the complete fresh `LogOutput.log` with the exact S1.42AE uploader in the candidate record.
6. Evaluate the log before any successor work.

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

The response that explains this runtime test must include both the repository-driven Gale v2.3 replacement/import one-liner and the exact S1.42AE self-contained PowerShell one-line runtime-log uploader.

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
