> **S1.42S GATE CLOSED — PASS:** The Baboon-Hawk/Pikmin isolated regression is resolved. Runtime evidence: `RuntimeEvidence/S1.42S/20260903T205550Z/`. No focused attacker continued hitting after Hawk death; all three were recoverable; corpse carry to Onion passed; Work/no-task and Leader-null counts are zero. See `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`. **Next active task:** remove/disable EnemyIsolation and restore normal enemy-related configuration from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`, preserving later accepted fixes. BCMER must remain exact 1.71.0 whenever reintroduced.

> **S1.42S ACTIVE GATE:** Import `Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z` via Gale **Advanced options -> Import all files**. Latch at least 3 Pikmin onto one Baboon Hawk, kill it, verify all fall off/stop attacking and exact follower count recovers. Also verify Hawk -> Pikmin bite/grab remains blocked and Dead Baboon Hawk carry remains normal. S1.42R is failed and superseded. See Current/66 and Current/67.

# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42R

Final handover:
`Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`

Repository audit:
`Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Compatibility plugin:
**v1.3.13**

Root cause:
`Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

Exact upstream decompile:
`Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`

## S1.42Q confirmed failure

First Baboon Hawk had three attackers:
- `Yellow Pikmin_ruCpzY`
- `Yellow Pikmin_PerDu`
- `Yellow Pikmin_hcRGph`

Only `hcRGph` got native `Task finished`.

`ruCpzY` and `PerDu` stayed on the first dead Hawk with no task transition.

The second Hawk did not lose its correctly transitioned attacker.

## Exact upstream defect

LethalMin 1.1.108 `AttackEnemyTask.IntervaledUpdate()` checks:

`if (CurrentIntention != Attack || IsPikminOnEnemy) return;`

before it checks:

`enemy.enemyScript.isEnemyDead`

and calls:

`FinishTaskServerRpc()`.

So a still-latched co-attacker is structurally prevented from reaching the native dead-target completion code.

## S1.42R

One narrow prefix on the exact `AttackEnemyTask.IntervaledUpdate()`:

If this exact task is latched to its own dead target:
- request native `PikminAI.FinishTaskServerRpc()`;
- skip the broken upstream interval for that tick.

No:
- death hook
- scan
- radius
- name matching
- direct state mutation
- custom unlatch/carry

## Runtime test

1. Import with Gale **Advanced options -> Import all files**.
2. Record follower count.
3. Put at least 3 Pikmin onto the same Baboon Hawk.
4. Kill the Hawk.
5. Verify every attacker immediately stops.
6. Verify `[LethalMinLatchedDeathGuard] Requested native FinishTaskServerRpc` for co-attackers.
7. Verify native `Task finished` for those Pikmin.
8. Whistle all Pikmin back and verify exact count.
9. Repeat on a second Hawk.
10. Verify Dead Hawk body remains normally carryable to Onion.
11. Verify living Hawk still ignores corpse/Pikmin.
12. Verify no `Work state with no task assigned!`.
13. Verify no `Leader is null when following`.
14. Commit full fresh log to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`

Do not restore normal enemies or BCMER until R passes.

There is currently no S1.42R runtime evidence. The next action is the runtime test itself, not another build.
