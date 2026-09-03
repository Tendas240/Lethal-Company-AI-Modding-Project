# 04 - Open Issues and Next Tests

## Immediate next stage — S1.42Q minimal LethalMin-native rollback

Canonical plan:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`

S1.42P runtime analysis remains:
`Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

## New architectural decision

The project must stop owning normal LethalMin Pikmin lifecycle behavior.

Native LethalMin should own:
- Pikmin -> enemy target/latch/attack;
- enemy-death task completion;
- Pikmin -> enemy-body carry;
- Onion delivery.

Project-local code should own only:
- proven Enemy -> Pikmin prevention gaps;
- unrelated compatibility fixes already independently justified.

This supersedes the previous idea of adding another custom dead-Hawk target filter/reacquisition layer.

## S1.42Q removals

Remove:
- `PatchBaboonHawkDeathCleanup()`;
- `BaboonHawkDeathCleanup`;
- Hawk-death `PikminAI.FinishTask()` reflection;
- 4.0 m SpawnedEnemies death selector;
- delayed post-grab snapshot/leader/follow reflection repair where prevention can replace it.

Do not add custom AttackEnemy or CarryItem logic.

## Config rollback

S1.41 vs S1.42P LethalMin config comparison shows only one difference:

`[Enemy Behavior] Thumper Bite Limit`
- S1.41: `3`
- S1.42P: `0`

Restore `3` in S1.42Q unless a new isolated test proves it must differ.

Keep the existing native LethalMin protection settings such as invincible Pikmin, Puffer poison off, Old Bird grabs off, CodeRebirth interaction toggles off, etc.

## Narrow shims that may remain

- CodeRebirth Crane kill shield: previously proven necessary despite native config;
- Dead Baboon Hawk `CanGrabScrap` guard: separate SellBodies compatibility shim; it does not implement Pikmin carrying and may remain unless a clean native test proves unnecessary;
- minimal exact Enemy -> Pikmin Bite/Grab blockers only where runtime evidence proves upstream/config still allows the interaction.

Prefer blocking before Pikmin state mutation. Avoid repairing state afterward.

## S1.42Q acceptance

1. Pikmin attack/latch/kill Thumper/Crawler natively.
2. Pikmin attack/latch/kill Baboon Hawk natively.
3. Enemy death releases attackers naturally with no project-local FinishTask marker.
4. All Pikmin remain responsive and whistle back.
5. Following count recovers exactly.
6. Dead Baboon Hawk is carried to Onion natively.
7. Enemies do not target/bite/grab/harm Pikmin.
8. Puffer remains harmless to Pikmin.
9. no `Work state with no task assigned!`.
10. no `Leader is null when following`.
11. no `BaboonHawkDeathCleanup` runtime markers.

## Temporary state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_MINIMAL_ROLLBACK_BUILD`

Do not restore normal enemies or BCMER until this minimal architecture passes.
