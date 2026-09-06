# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`, `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Runtime acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`.

Latest built artifact and active runtime candidate: **S1.42AG — Mouth Dog Pikmin One-Way Protection — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**. Profile SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`. Candidate authority: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG`; `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AG_BUILD_AWAITING_RUNTIME_VALIDATION`. No successor beyond S1.42AG is armed.

S1.42AD remains runtime-rejected historical provider-contract evidence. S1.42AE remains superseded for packaging after its physically present SoundAPI binding was blocked through a 262-character runtime path. S1.42AF reused the corrected source on a 226-character path and passed both normal startup and the exact 18 Moon / 18 Interior Functional Microwave runtime contract.

## Exact next scope

The selected work is now **S1.42AG full-normal runtime validation**, not further Mouth Dog source-contract analysis and not a new build.

The S1.42AF acceptance run proved that a Mouth Dog could bite/grab Pikmin and start their death timers. Invincibility prevented the final kill but did not prevent harmful state mutation; the two affected White Pikmin then produced 707 `Work state with no task assigned!` warnings. This is the baseline-resident compatibility finding in `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`.

The exact LethalMin 1.1.108 source contract was subsequently proved in `Current/130...`, the smallest prevention boundary was authorized in `Current/131...`, and the pre-build safety review passed in `Current/132...`. S1.42AG implements a `Priority.First` prevention patch on exact declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` while keeping the adapter enabled.

The next ChatGPT action is therefore to follow `Current/133...`: import S1.42AG with the canonical Gale v2.4 replacement helper, exercise repeated Mouth Dog lunges around Pikmin under the full normal stack, prove the Dog -> Pikmin bite/grab/death-timer path is absent, prove Pikmin -> Mouth Dog attack/latch/death cleanup and Mouth Dog -> player attacks remain functional, confirm normal startup/generation and inherited S1.42AF Microwave health, then upload the complete fresh S1.42AG `LogOutput.log` with the build-specific uploader. **Do not accept S1.42AG from build/startup success alone.**

## Remaining deferred independent gameplay/compatibility scopes

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- broader LethalMin teardown/despawn repair only with stronger evidence beyond the now-selected Mouth Dog interaction.

## BCMER scope boundary

S1.42AC remains the accepted historical BCMER 1.71.0 static EventType-probability implementation inherited by S1.42AF and S1.42AG. Exact long-run executed EventType frequency after runtime eligibility filters is a broader algorithm-design scope and is not armed.

## Interior scope boundary

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AG does not alter that path. Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
