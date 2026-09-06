# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER  
**Authority:** primary human topic router for repository knowledge  
**Canonical-For:** topic discovery from bootstrap  
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`  
**Current State:** `Current/00_CURRENT_STATE.md`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Last-Validated:** 2026-09-06

Before performing project work, every ChatGPT chat must read and follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. Use this map for the semantic content route inside each execution segment.

Use this map before repository search. Open only the topic that matches the user's question, then follow its evidence/config/code links as needed.

## Immediate routing

| User question / topic | Topic ID | Canonical source |
|---|---|---|
| How must ChatGPT divide and execute project work? When must it stop and wait for `weiter`? | `chatgpt_segmented_execution` | `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` |
| What is the accepted build? What is active? What must I test or analyze next? | `accepted_baseline`, `active_candidate_and_next_test` | `Knowledge/CURRENT_LIFECYCLE.md` |
| How do I hand the project over to a new ChatGPT chat? What should happen when the user signals a handover? | `chat_handover` | `Current/HANDOVER_PREPARATION_PROMPT.md` |
| How are profiles built in GitHub? Where is the runtime uploader/ingest? | `build_pipeline`, `runtime_upload_and_ingest` | `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` |
| How do I replace/import the active Gale profile? | `gale_import` | `Knowledge/GALE_PROFILE_WORKFLOW.md` |
| Which BCMER version/settings are allowed? Are EventTypes equally likely? | `bcmer` | `Knowledge/BCMER.md` |
| How do interior weights work? LLL? Shatteredrooms? CullFactory? Black Mesa registration? | `interiors_and_lll` | `Knowledge/INTERIORS_AND_LLL.md` |
| What is the normal enemy spawn baseline / ownership architecture? | `enemy_spawn_baseline` | `Knowledge/ENEMY_SPAWN_BASELINE.md` |
| How should Thumper/Puffer/Baboon Hawk/Mouth Dog/Eyeless Dog interact with Pikmin? | `pikmin_enemy_compatibility` | `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md` |
| What are the accepted Jetpack values and owner? | `jetpack` | `Knowledge/JETPACK.md` |
| How is CodeRebirth/DawnLib configured/tuned? | `coderebirth` | `Knowledge/CODEREBIRTH.md` |
| What are Microwave/Snail values? What is still deferred? | `functional_microwave`, `immortal_snail` | `Knowledge/ITEM_TUNING.md` |
| Which errors/warnings should only be monitored? | `monitor_only_errors` | `Knowledge/MONITOR_ONLY_ERRORS.md` |
| What is the Black Mesa/Pikmin routing problem? | `black_mesa_pikmin_routing` | `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md` |
| What remains on the live roadmap? | `roadmap_and_deferred_scopes` | `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md` |
| What rules govern project-local Harmony/runtime patches? | `patch_safety_policy` | `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` |
| What is happening with the repository overhaul? | `repository_overhaul` | `Knowledge/REPOSITORY_OVERHAUL.md` |
| Where is the untouched pre-overhaul recovery point? | `pre_overhaul_backup_and_recovery` | `Knowledge/PRE_OVERHAUL_BACKUP_AND_RECOVERY.md` |
| Which build introduced/rejected/fixed something? What came before build X? | `build_lineage` | `Current/BUILD_LINEAGE.md` |

The current accepted gameplay baseline is **S1.42AF — Path-Length-Safe Microwave Packaging**. The latest built artifact is **S1.42AG — Mouth Dog Pikmin One-Way Protection — runtime rejected / partial fix**. There is no active runtime candidate and no successor is armed.

The previously pending Vanilla V81 MouthDogAI capture has completed successfully. Current Mouth Dog analysis authority is `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, with provenance-safe source evidence under `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`. `Current/135_MOUTHDOG_V81_SOURCE_CAPTURE_TOOL_WINDOWS_HARDENING_STATE.md` is resolved capture-tool history.

The exact next action is the targeted source-evidence extension registered in `Knowledge/CURRENT_LIFECYCLE.md` and `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`: prove Vanilla V81 `EnemyAI.OnCollideWithEnemy()` base behavior and exact LethalMin 1.1.108 `PikminItem.CarryNumerator()` / carry-audio-noise callsites before any successor safety review or build.

## Authority rule

For current questions:

1. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` controls execution cadence for project work.
2. `Current/00_CURRENT_STATE.md` is the sole concise human current-state declaration.
3. This Knowledge Map chooses the semantic topic.
4. The topic canonical source states the current rule/value and points to provenance.
5. Build-specific acceptance/rejection/diagnostic records and RuntimeEvidence prove historical decisions.
6. Historical files may accurately describe what was current **at that time** but do not override current semantic topics.

Machine lifecycle authority is `Current/CURRENT_STATE.json`. `BuildSpecs/current.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are controller inputs whose lifecycle must remain consistent with that canonical machine state.

When the user requests transfer to a new ChatGPT chat, route directly to `Current/HANDOVER_PREPARATION_PROMPT.md`; that procedure resolves the then-current state and generates a fresh new-chat start prompt while remaining subject to the segmented-execution continuation gate.

## Historical navigation

- Project chronology: `Current/03_PROJECT_CHRONOLOGY.md`
- Failed/obsolete approaches: `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
- Build lineage: `Current/BUILD_LINEAGE.md` / `.json`
- Exact build records: numbered `Current/*S1.*` candidate/acceptance/rejection/runtime files
- Historical profile evidence: `ProfileSources/<build>/`
- Runtime evidence: `RuntimeEvidence/<build>/<timestamp>/`
- Deep archival fallback: `Archive/`, `Logs/`, `References/`

Repository/code search is appropriate for unknown symbols, exact error strings or deep historical reconstruction, but ordinary canonical questions should route through this map first.

## Current authority exclusions

The following retained files contain valuable historical/durable evidence but must not be treated as unqualified current-state authority after the overhaul:

- `Current/02_TECHNICAL_BASELINE.md` — mixes durable facts with obsolete S1.41/S1.42S/T current wording;
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` — mixes durable/binding interior research with obsolete S1.42U/S1.42V current checkpoint wording.

Their still-live facts have been extracted into semantic topics above; the original files remain provenance/history.
