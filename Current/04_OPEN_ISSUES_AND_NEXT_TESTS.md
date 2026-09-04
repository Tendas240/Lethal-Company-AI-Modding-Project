# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-04

This file intentionally no longer duplicates the full project history or technical baseline. The pre-overhaul version is preserved in Git history and in the verified standalone pre-overhaul repository; durable facts were extracted into the `Knowledge/` topic layer and build/runtime evidence.

## Current gameplay gate

- **Accepted baseline:** S1.42AB — Interior Weight Normalization.
- Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
- Runtime: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Latest built artifact is S1.42AC. It remains **formally rejected/not promoted**. The original rejection interpretation was corrected by exact BCMER 1.71.0 source analysis in `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`: unequal `Set eventType weight ...` log values are expected inverse-count **per-event** weights, not unequal aggregate EventType probability.

## Exact next action

**No runtime test is outstanding. No successor is armed. No compensation build should be created.**

If the BCMER EventType scope is continued, apply the corrected acceptance model in `Current/109...` to the existing S1.42AC artifact/evidence. Do not require equality of the eight per-event log values.

Current controllers:

- `BuildSpecs/current.json` is disabled and guarded by accepted S1.42AB.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`.

Whenever a future runtime test becomes outstanding, the same response that explains the test must include the exact build-specific PowerShell one-line log uploader.

## Open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Current deferred items include:

- reconsider existing S1.42AC under the corrected BCMER static EventType acceptance model;
- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence.

The repository information-architecture overhaul is **closed** and has passed the stricter post-acceptance re-audit against the frozen original instructions. Its current summary is `Knowledge/REPOSITORY_OVERHAUL.md`; final evidence is `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md`, `Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md` and `Current/OVERHAUL_VALIDATION_RESULTS.json`.

## Topic routes

- Current lifecycle / next test: `Knowledge/CURRENT_LIFECYCLE.md`
- BCMER: `Knowledge/BCMER.md`
- Interiors / LLL / CullFactory: `Knowledge/INTERIORS_AND_LLL.md`
- Enemy-spawn baseline: `Knowledge/ENEMY_SPAWN_BASELINE.md`
- Pikmin/enemy compatibility: `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`
- Black Mesa/Pikmin routing: `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`
- Jetpack: `Knowledge/JETPACK.md`
- CodeRebirth: `Knowledge/CODEREBIRTH.md`
- Microwave / Immortal Snail: `Knowledge/ITEM_TUNING.md`
- Known monitor-only errors: `Knowledge/MONITOR_ONLY_ERRORS.md`
- Build/runtime/GitHub pipeline: `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`
- Gale import: `Knowledge/GALE_PROFILE_WORKFLOW.md`
- Build history: `Current/BUILD_LINEAGE.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
- Repository overhaul: `Knowledge/REPOSITORY_OVERHAUL.md`

## Permanent guardrail

Do not reopen old diagnostic branches or rewrite historical outcomes merely because old files contain stale `current` wording. Current authority is determined by `Current/DOCUMENT_AUTHORITY.md` and the semantic knowledge map.
