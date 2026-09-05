# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/Projektstatus_S1.42AC_ACCEPTED.json`, `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`, `Current/Projektstatus_S1.42AD_CANDIDATE.json`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AD_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/BCMER.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Knowledge/ITEM_TUNING.md`  
**Last-Validated:** 2026-09-05

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Machine state: `Current/Projektstatus_S1.42AC_ACCEPTED.json`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the rollback/full-normal-stack baseline until S1.42AD completes a fresh runtime gate. Its corrected BCMER 1.71.0 interpretation remains unchanged: equal EventType scales of 12.5 implement equal static type probability while logged per-event weights may differ because they are inverse-population normalization values.

## Active candidate

**S1.42AD — Functional Microwave Spawn Rarity Reduction — BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- Profile SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- Candidate record: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`
- Machine candidate state: `Current/Projektstatus_S1.42AD_CANDIDATE.json`
- Build workflow run: `33959742235` — SUCCESS
- Automated build commit: `1463a6cde5e8cb7655dd233f83da5157c91b036e`
- DLL SHA-256: `45f22f9b27e3ab7c853fe742bb7c2ce9bc94abc5a0856bb278c747076a2f99c7`

The user explicitly authorized the Functional Microwave target as **half as often**, implemented as proportional `SpawnScale = 0.5f` on the validated effective Moon/tag curves.

The finalized fail-closed runtime contract is:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- Dusk `0.9.25`;
- exact key `code_rebirth:functional_microwave`;
- exactly one `MapObjectSpawnMechanics` provider;
- `PrioritiseMoons = true`;
- exactly 18 Moon/tag curves;
- exactly 0 Interior/tag curves;
- no mutation on any contract drift.

The 18/0 expectation is based on the relevant shipped asset-bundle provenance, not the later Unity-source-only 19/Interior state.

## Build result / archive delta

Automated profile verification passed:

- ZIP members: `335`;
- changed existing members: only `export.r2x`;
- added members: only `BepInEx/plugins/S142ADCodeRebirthMicrowaveSpawnTuning/S142ADCodeRebirthMicrowaveSpawnTuning.dll`;
- package state/additions/removals: none;
- config patches: none;
- accepted Functional Microwave Volume `0.15` preserved.

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt` contains:

`S1.42AD`

`BuildSpecs/current.json` is disabled after the successful candidate build:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AD_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = generated S1.42AD profile / SHA `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`;
- no successor is armed.

## Pending runtime test

**YES — S1.42AD.**

The next evidence must confirm:

1. normal startup/main menu/lobby;
2. S1.42AD plugin load;
3. exact CodeRebirth/Dawn/Dusk version validation;
4. provider marker `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=0`;
5. final marker showing all 18 Functional Microwave Moon/tag curves scaled by `0.5`;
6. no S1.42AD contract-refusal/error;
7. normal moon/interior generation and ordinary gameplay;
8. no new fatal/project-critical regression.

A short gameplay sample is not expected to statistically prove an exact observed 50% occurrence ratio; the deterministic provider mutation is the primary technical evidence.

## Exact next gameplay action

Replace/import the generated S1.42AD Gale profile using the canonical repository helper, play one normal round far enough for normal moon/interior generation, and upload the complete fresh `LogOutput.log` using the exact S1.42AD uploader recorded in `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`.

Do not arm or build a successor before this runtime evidence is analyzed.
