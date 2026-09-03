# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42M Baboon Hawk death cleanup

Detailed predecessor-runtime analysis:
`Current/47_S1.42L_BABOON_ATTACK_PASS_DEATH_REGRESSION_ANALYSIS.md`

Canonical detailed handover:
`Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md`

Profile:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Compatibility plugin:
v1.3.8  
DLL SHA-256:
`47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Latest valid runtime evidence:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

## What S1.42L closed

**Pikmin -> Baboon Hawk live attack/latch is PASS.**

The evaluated run proves:
- Pikmin latch onto the Hawk;
- Pikmin repeatedly damage it;
- Pikmin can kill it;
- Hawk-side ignore protection remains;
- `Leader is null when following` = 0.

Therefore do not reopen the live attack/latch direction unless a regression appears.

## New issue found at Hawk death

After the Hawk died:
- Pikmin stayed on the old `BaboonHawkEnemy(Clone)` attack/latch target;
- they continued hitting it after `Kill enemy called! destroy: False`;
- SellBodiesFixed spawned `BaboonHawkBody(Clone)` after its configured 4-second delay;
- SellBodiesFixed then moved the original dead enemy transform away;
- latched Pikmin visually disappeared with that stale target;
- living Baboon Hawks grabbed the new corpse item as ordinary scrap.

## Desired result

- Pikmin detach from the dying Hawk and remain usable.
- SellBodies Baboon Hawk corpse generation remains enabled.
- Dead Baboon Hawk body remains on the ground.
- Players can still carry it.
- Pikmin can be thrown onto it and carry it toward the Onion.
- Living Baboon Hawks do not pick it up.
- Hawk -> Pikmin ignore remains intact.
- No leader-null loop.

## Exact S1.42M test

Use:
**Gale -> Advanced options -> Import all files**

1. find/spawn a Baboon Hawk;
2. throw multiple Pikmin directly onto it;
3. let the Pikmin kill it;
4. immediately confirm the attacking Pikmin detach/remain visible and usable;
5. wait at least 5 seconds;
6. confirm the Dead Baboon Hawk body remains at/near the death location;
7. throw Pikmin onto the corpse;
8. confirm they can carry the corpse toward the Onion;
9. if another living Hawk is available, confirm it does not pick up the corpse;
10. confirm living Hawk -> Pikmin remains blocked;
11. confirm no `Leader is null when following`;
12. upload the complete fresh log to `RuntimeInbox/Current/`.

Do not build a successor first.

## Temporary isolated test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal spawning/BCMER until S1.42M is evaluated.

## Closed — do not retest unless regression appears

- Thumper/Crawler -> Pikmin protection: PASS
- Pikmin -> Thumper/Crawler attack/latch: PASS
- Puffer -> Pikmin: PASS
- Jetpack: PASS
- Baboon Hawk -> Pikmin: PASS
- Pikmin -> living Baboon Hawk attack/latch: PASS

## After S1.42M PASS

Then:
1. remove/disable temporary EnemyIsolation;
2. restore normal enemy spawning/config from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric interaction rules and S1.42M corpse behavior;
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

General cleanup remains deferred during the active runtime gate.

Known non-functional drift:
- `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`
