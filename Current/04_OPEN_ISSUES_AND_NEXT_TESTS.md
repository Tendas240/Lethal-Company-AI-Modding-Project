# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-05

This file intentionally no longer duplicates the full project history or technical baseline. The pre-overhaul version is preserved in Git history and in the verified standalone pre-overhaul repository; durable facts were extracted into the `Knowledge/` topic layer and build/runtime evidence.

## Current gameplay gate

- **Accepted baseline:** S1.42AC — BCMER EventType Equal Distribution.
- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Fresh acceptance runtime: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC is now explicitly accepted under the corrected BCMER `1.71.0` static EventType model. `Current/106...` remains historical rejection evidence; `Current/109...` corrected the per-event-weight interpretation and `Current/118...` is the later acceptance decision.

## Exact next action

**No runtime test is outstanding. No successor is armed. No build is implicitly authorized.**

Wait for explicit selection of the next isolated gameplay/compatibility scope through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.

Current controllers:

- `BuildSpecs/current.json` is disabled and guarded by accepted S1.42AC.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`.

Whenever a future runtime test becomes outstanding, the same response that explains the test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific self-contained PowerShell one-line runtime-log uploader.

## Open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Current deferred items include:

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
