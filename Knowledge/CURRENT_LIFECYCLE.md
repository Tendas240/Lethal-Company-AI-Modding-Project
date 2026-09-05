# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/Projektstatus_S1.42AC_ACCEPTED.json`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/Projektstatus_S1.42AD_REJECTED.json`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AD_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/BCMER.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/ITEM_TUNING.md`  
**Last-Validated:** 2026-09-05

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Machine state: `Current/Projektstatus_S1.42AC_ACCEPTED.json`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the accepted full-normal-stack gameplay/rollback baseline.

## Latest built artifact — rejected

**S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- Profile SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- Candidate record: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`
- Rejection: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`
- Machine rejection state: `Current/Projektstatus_S1.42AD_REJECTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AD/20260905T103333Z/`
- Raw log SHA-256: `30c69254c4a4fd6bea1ec83cda075c168742c9060b88b09c22025973b074b3e8`

S1.42AD loaded successfully and validated CodeRebirth `1.6.9`, DawnLib `0.9.25` and Dusk `0.9.25`. Its fail-closed patch then refused mutation because the runtime Functional Microwave provider exposed **18 Interior/tag curves**, while the frozen candidate contract required `0`.

The refusal included `code_rebirth:functional_microwave_ultra_high` in the actual Interior-curve set. No later S1.42AD application marker exists, so the user-authorized `SpawnScale = 0.5` was not applied.

The candidate is rejected because the target tuning did not execute. The fail-closed behavior itself worked correctly.

## Active candidate

**NONE.**

No runtime test is outstanding. Do not use S1.42AD as a gameplay/build base.

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt` contains:

`S1.42AC`

`BuildSpecs/current.json` is disabled:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AD_REJECTION_MICROWAVE_PROVIDER_ANALYSIS_PENDING`;
- guarded base = accepted S1.42AC profile/SHA;
- no successor is armed.

## Regression triage from S1.42AD

Fresh S1.42AD evidence kept project-critical regression markers clean:

- Work/no-task = `0`;
- Leader-null = `0`;
- Compatibility Fixes Error = `0`;
- Fatal = `0`;
- NetworkObjectReference-unspawned regression = `0`;
- PikminNoticeZone regression = `0`.

The known loaforcsSoundAPI/HarmonyX TypeLoadException and SoftMask NullReference warnings remain monitor-only under `Knowledge/MONITOR_ONLY_ERRORS.md`.

## Exact next project action

The user's desired Functional Microwave target remains **half as often** (`SpawnScale = 0.5`). Before any corrected successor is armed, independently resolve:

1. the actual runtime Moon-curve count and exact keys;
2. the actual runtime Interior-curve count and exact keys;
3. DawnLib `MapObjectSpawnMechanics` selection/evaluation semantics when `PrioritiseMoons = true`;
4. which effective table or tables must be scaled to produce true half-frequency behavior;
5. a revised fail-closed contract that logs and verifies both tables before mutation.

Do not simply remove the Interior check or blindly scale both dictionaries. No successor build or runtime test is currently pending.
