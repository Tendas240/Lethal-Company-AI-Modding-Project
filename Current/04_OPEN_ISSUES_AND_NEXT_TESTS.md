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

## Latest built artifact

**S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- Candidate: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`
- Rejection: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`
- Runtime evidence: `RuntimeEvidence/S1.42AD/20260905T103333Z/`
- Raw log SHA-256: `30c69254c4a4fd6bea1ec83cda075c168742c9060b88b09c22025973b074b3e8`

The user-authorized target remains Functional Microwaves **half as often** (`SpawnScale = 0.5`). S1.42AD did not apply that change: its fail-closed patch expected zero Interior/tag curves but runtime exposed 18, including `code_rebirth:functional_microwave_ultra_high`, so mutation was correctly refused.

## Exact next action

**No runtime test is outstanding. No successor is armed. Do not build from S1.42AD.**

Before a corrected Microwave successor is armed, independently establish:

1. the actual runtime Moon-curve count and exact key set;
2. the actual runtime Interior-curve count and exact key set;
3. DawnLib/Dusk `MapObjectSpawnMechanics` selection/evaluation semantics for `PrioritiseMoons = true`;
4. which effective curve table or tables must be proportionally scaled for the half-frequency target;
5. a revised fail-closed contract that logs/verifies both tables before mutation.

Do not merely remove the Interior check and do not blindly scale both dictionaries.

Current controllers:

- `BuildSpecs/current.json` is disabled.
- controller id: `IDLE_AFTER_S1.42AD_REJECTION_MICROWAVE_PROVIDER_ANALYSIS_PENDING`.
- guarded base: accepted S1.42AC profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`.

Whenever a future runtime test becomes outstanding, the same response that explains the test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific self-contained PowerShell one-line runtime-log uploader.

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