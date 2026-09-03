# 04 - Open Issues and Next Tests

## Active runtime gate — S1.42R

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Plugin:
**v1.3.13**

## Confirmed S1.42Q failure

S1.42Q proved that native LethalMin 1.1.108 has a specific `AttackEnemyTask` bug.

Three Pikmin attacked the first Hawk:
- ruCpzY
- PerDu
- hcRGph

hcRGph reached native `Task finished` and remained usable.

ruCpzY and PerDu never reached `Task finished`, kept hitting the dead first Hawk until teardown, and exactly match the two missing Pikmin reported by the user.

## Root cause

`AttackEnemyTask.IntervaledUpdate()` checks:

`CurrentIntention != Attack || IsPikminOnEnemy`

and returns before its later:

`enemy.enemyScript.isEnemyDead`

check.

Latched co-attackers therefore cannot reach native dead-target completion.

## S1.42R correction

Patch only the exact task method.

When its own target is dead while still latched, request the exact native:

`PikminAI.FinishTaskServerRpc()`

No external attacker selection exists anymore.

## Runtime test

1. Import via Gale "Advanced options -> Import all files".
2. Start with known follower count.
3. Put at least three Pikmin onto the same Baboon Hawk.
4. Kill Hawk.
5. Confirm all affected Pikmin stop attacking.
6. Confirm `[LethalMinLatchedDeathGuard]` for latched co-attackers.
7. Confirm native `Task finished` for each.
8. Whistle all and verify exact follower count.
9. Repeat on second Hawk.
10. Verify corpse remains Onion-carryable.
11. Verify living Hawk ignores corpse.
12. Verify Hawk -> Pikmin remains blocked.
13. Verify no Work/no-task loop.
14. Verify no Leader-null loop.
15. Commit complete fresh log to `RuntimeInbox/Current/`.

EnemyIsolation remains enabled.
BCMER 1.71.0 remains disabled.
