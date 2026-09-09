<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AH candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `RuntimeEvidence/S1.42AH/20260909T162513Z/`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`  
**Last-Validated:** 2026-09-09

## Accepted baseline / latest built artifact

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Final decisive runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`  
Final raw-log SHA-256: `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`

S1.42AH supersedes S1.42AF as the accepted gameplay baseline. S1.42AF remains the accepted predecessor/rollback point. S1.42AG remains runtime-rejected partial-fix evidence.

## Why the final S1.42AH gate passed

The two earlier targeted S1.42AH runs already proved the intended dual patch installation, repeated MouthDog -> Pikmin prevention, MouthDog -> player preservation, native Pikmin -> MouthDog latch/attack/damage, MouthDog death, unlatch/task cleanup, corpse carrying, live adapter prevention, ordinary noise response and clean known project-regression markers.

The only remaining neighbor requirement was non-Pikmin `EnemyAI` pass-through through the patched Vanilla collision surface.

For the final decision the user explicitly directed analysis to the **last gameplay run only** in `RuntimeEvidence/S1.42AH/20260909T162513Z/`. That run records two Mouth Dogs and a Redwood Titan spawning, followed by a normal Redwood Titan enemy-death sequence. The user deliberately performed the neighbor test and reported observing what appeared to be a Mouth Dog killing the Redwood Titan. The log does not encode attacker identity on the Titan death line, so the acceptance does not claim a nonexistent attacker field; the positive manual interaction is combined with the independently logged target death and exact source/patch behavior.

The exact S1.42AH collision prefix returns `true` for null and every non-`LethalMin.PikminAI` `EnemyAI`. Exact Vanilla V81 source proves `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` then performs its normal non-same-type collision path and calls `collidedEnemy.HitEnemy(2, null, playHitSFX: true)`. The prior `BiteKillEnemyAI` wording was shorthand; the exact current V81 contract is `OnCollideWithEnemy` -> `HitEnemy(2)`.

This closes the final neighboring-path requirement under the permanent patch-safety policy.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AH**.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled: `IDLE_AFTER_S1.42AH_ACCEPTANCE_PREP_SHYGUY_CONFIG_SUCCESSOR`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH` remains the runtime/evidence-attribution pointer.
- No successor has yet been built or armed.

## Canonical Gale workflow

The current Gale active-profile replacement/import workflow remains the repository-driven **v2.4** path in `Knowledge/GALE_PROFILE_WORKFLOW.md`, implemented by `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. Do not regress current lifecycle guidance to the older v2.2/v2.3 paths. When a future successor becomes ready for runtime testing, pair that canonical v2.4 launcher with the exact build-specific runtime-log uploader required by `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.

## Exact next project action

Prepare and arm a **single-variable BCMER/config successor from accepted S1.42AH** implementing only `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`:

- keep BCMER `[ShyGuy] Event Enabled? = true`;
- keep its EventType and all three interior values unchanged;
- set only `ShyGuyDef OutsideEnemyRarity`, `ShyGuyDef MinOutsideEnemy`, and `ShyGuyDef MaxOutsideEnemy` to `0, 0, 0, 0`;
- keep ordinary Scopophobia `SpawnOutside = false`;
- do not mix LC Office, CullFactory, fog, Black Mesa or LethalEscape changes into the same build;
- statically validate the exact archive delta before any new runtime test.

There is currently no runtime test for the user to perform until that successor is built and designated ready.