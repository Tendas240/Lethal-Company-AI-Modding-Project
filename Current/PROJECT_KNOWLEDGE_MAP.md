<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER  
**Authority:** primary human topic router for repository knowledge  
**Canonical-For:** topic discovery from bootstrap  
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`  
**Current State:** `Current/00_CURRENT_STATE.md`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Last-Validated:** 2026-09-08

Before performing project work, every ChatGPT chat must read and follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. Use this map for semantic routing; current lifecycle facts come from `Current/CURRENT_STATE.json` plus the routed canonical topic, not from historical handovers.

## Immediate routing

| User question / topic | Topic ID | Canonical source |
|---|---|---|
| How must ChatGPT divide and execute project work? | `chatgpt_segmented_execution` | `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` |
| What is accepted/active and what happens next? | `accepted_baseline`, `active_candidate_and_next_test` | `Knowledge/CURRENT_LIFECYCLE.md` |
| How do I hand the project to a new ChatGPT chat? | `chat_handover` | `Current/HANDOVER_PREPARATION_PROMPT.md` |
| How are profiles built and runtime logs ingested? | `build_pipeline`, `runtime_upload_and_ingest` | `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` |
| How do I replace/import the active Gale profile? | `gale_import` | `Knowledge/GALE_PROFILE_WORKFLOW.md` |
| Which BCMER settings/weight rules are current? | `bcmer` | `Knowledge/BCMER.md` |
| How do interiors/LLL/CullFactory work? | `interiors_and_lll` | `Knowledge/INTERIORS_AND_LLL.md` |
| What is the normal enemy-spawn baseline? | `enemy_spawn_baseline` | `Knowledge/ENEMY_SPAWN_BASELINE.md` |
| How should Pikmin interact with enemies including Mouth Dog? | `pikmin_enemy_compatibility` | `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md` |
| What are the accepted Jetpack values? | `jetpack` | `Knowledge/JETPACK.md` |
| How is CodeRebirth/DawnLib configured? | `coderebirth` | `Knowledge/CODEREBIRTH.md` |
| What are Microwave/Snail values? | `functional_microwave`, `immortal_snail` | `Knowledge/ITEM_TUNING.md` |
| Which errors/warnings are monitor-only? | `monitor_only_errors` | `Knowledge/MONITOR_ONLY_ERRORS.md` |
| What is the Black Mesa/Pikmin routing problem? | `black_mesa_pikmin_routing` | `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md` |
| What remains on the live roadmap? | `roadmap_and_deferred_scopes` | `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md` |
| What rules govern project-local patches? | `patch_safety_policy` | `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` |
| What is the repository-overhaul/recovery state? | `repository_overhaul`, `pre_overhaul_backup_and_recovery` | `Knowledge/REPOSITORY_OVERHAUL.md`, `Knowledge/PRE_OVERHAUL_BACKUP_AND_RECOVERY.md` |
| Which build introduced/rejected/fixed something? | `build_lineage` | `Current/BUILD_LINEAGE.md` |

## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging**.

Latest built artifact and active runtime candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / PARTIAL RUNTIME PASS / TARGETED REMAINDER OUTSTANDING / NOT ACCEPTED**.

Runtime test outstanding: **yes**. S1.42AH is neither accepted nor rejected. No successor beyond S1.42AH is armed. `BuildSpecs/current.json` is disabled and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.

S1.42AH already implements the reviewed dual-prevention architecture from `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`. Its first ingested run, recorded in `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, positively proves patch installation, repeated live Vanilla MouthDog -> Pikmin collision blocking, and exercised MouthDog -> player maul/kill preservation. The exact next gameplay action is only the targeted reverse-direction/adapter/cleanup remainder documented in `Current/140`; do not rebuild the candidate, repeat the S1.42AG run, or repeat already-proven AH coverage first.

## Authority rule

1. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` controls execution cadence.
2. `Current/CURRENT_STATE.json` is the global machine lifecycle authority; `Current/00_CURRENT_STATE.md` is its concise generated human mirror.
3. This map chooses the semantic topic; it intentionally avoids duplicating volatile per-build evidence lists in its machine mirror.
4. The canonical topic states current rules and points to provenance.
5. Build-specific acceptance/rejection/candidate/partial-runtime records and RuntimeEvidence prove historical or pending decisions.
6. Historical files never override the current machine state or a later explicit decision.

When the user requests transfer to a new ChatGPT chat, route directly to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify the current repository state before producing the handover.

## Historical navigation

- Project chronology: `Current/03_PROJECT_CHRONOLOGY.md`
- Failed/obsolete approaches: `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
- Build lineage: `Current/BUILD_LINEAGE.md` / `.json`
- Build-specific records: numbered `Current/*S1.*` files
- Historical profile evidence: `ProfileSources/<build>/`
- Runtime evidence: `RuntimeEvidence/<build>/<timestamp>/`
- Deep archival fallback: `Archive/`, `Logs/`, `References/`

`Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` remain historical/durable evidence only and are not unqualified current-state authority.
