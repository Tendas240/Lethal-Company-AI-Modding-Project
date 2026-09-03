# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42N Baboon Hawk death target resolver

Latest runtime analysis:
`Current/50_S1.42M_DEATH_CLEANUP_PARTIAL_PASS_ANALYSIS.md`

Current build:
`Current/51_S1.42N_BABOON_HAWK_DEATH_TARGET_RESOLVER_BUILD.md`

Profile:
`Profiles/LC V1 S1.42N Baboon Hawk Death Target Resolver.r2z`

SHA-256:
`c87d48464a750f87274e2848c44e5e1e24d4f1da087f59a33e2889744ebc13e9`

Compatibility plugin:
**v1.3.9**

## Latest valid runtime evidence — S1.42M

Evidence:
`RuntimeEvidence/S1.42M/20260903T163446Z/`

Log SHA-256:
`0639d5cc04aa54f5d7943ef4689e0d705c818871b019287ca1a1cdc2aa2492fb`

### Confirmed PASS

- Pikmin -> living Baboon Hawk attack/latch/kill;
- Dead Baboon Hawk body appears;
- corpse can be carried by Pikmin to Onion;
- living Hawks ignore Dead Baboon Hawk corpse;
- Hawk -> Pikmin ignore remains accepted;
- `Leader is null when following` = 0.

### Remaining FAIL

Attacking Pikmin still disappear when the Hawk dies.

The S1.42M death hook executed, and `PikminAI.RemoveCurrentTask()` resolved, but the resolver logged:
`released 0/0 latched Pikmin`.

Therefore the failed assumption is specifically that latched/attacking Pikmin are `PikminAI` children under the dying Hawk transform.

## S1.42N change

S1.42N leaves all passing corpse behavior untouched.

At Hawk death it performs a one-shot candidate pass through:
`RoundManager.Instance.SpawnedEnemies`

Then:
- keep only objects assignable to `LethalMin.PikminAI`;
- select under-Hawk or <= 4.0 m from the dying Hawk;
- call exact resolved `PikminAI.RemoveCurrentTask()`;
- log each release and aggregate counts.

No continuous Update scan and no broad/inherited Harmony scan.

## Exact S1.42N test

Use:
**Gale -> Advanced options -> Import all files**

1. find/spawn a Baboon Hawk;
2. throw several Pikmin directly onto it;
3. confirm normal latch/attack;
4. let the Pikmin kill it;
5. immediately confirm the attackers detach/remain visible and usable;
6. check that the log reports one or more `[BaboonHawkDeathCleanup] Released ...` lines;
7. check that the aggregate release count is non-zero;
8. wait at least 5 seconds;
9. confirm the Dead Baboon Hawk body remains;
10. carry it to the Onion with Pikmin;
11. confirm a living Hawk does not pick it up;
12. confirm living Hawk -> Pikmin remains blocked;
13. confirm no `Leader is null when following`;
14. commit the complete fresh log to `RuntimeInbox/Current/`.

Do not build a successor first unless S1.42N cannot start.

## Temporary isolated test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal spawning/BCMER until S1.42N is evaluated.

## Closed — do not retest unless regression appears

- Thumper/Crawler -> Pikmin protection: PASS
- Pikmin -> Thumper/Crawler attack/latch: PASS
- Puffer -> Pikmin: PASS
- Jetpack: PASS
- Baboon Hawk -> Pikmin: PASS
- Pikmin -> living Baboon Hawk attack/latch/kill: PASS

## After S1.42N PASS

Then:
1. remove/disable temporary EnemyIsolation;
2. restore normal enemy spawning/config exactly from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric interaction rules and corpse behavior;
5. runtime-check the restored normal state;
6. specifically monitor historical BCMER Door System ERROR / ship-door behavior;
7. document the normal-enemy/BCMER result before repository migration.

## Pending lower-priority work after restore

- Functional Microwaves should become somewhat rarer; exact target not selected.
- all registered interiors should ultimately have equal effective selection probability where technically safe;
- CullFactory exact IDs `junkrooms` and `shatteredrooms`;
- MelanieMausoleum fog reduction;
- preserve Shatteredrooms Experimentation/Embrion safety block until understood;
- monitor Mineshaft elevator/Pikmin crowding;
- do not rebalance outdoor Pikmin Sprout density without statistics.

## Deferred repository maintenance

Known non-functional drift:
- `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42N`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42N_BUILD_AWAITING_RUNTIME`
