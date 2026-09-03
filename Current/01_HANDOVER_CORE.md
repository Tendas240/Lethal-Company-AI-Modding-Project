# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42M — partial pass**

Current built candidate:
**S1.42N - Baboon Hawk Death Target Resolver**

Profile:
`Profiles/LC V1 S1.42N Baboon Hawk Death Target Resolver.r2z`

SHA-256:
`c87d48464a750f87274e2848c44e5e1e24d4f1da087f59a33e2889744ebc13e9`

Compatibility plugin:
**v1.3.9**

Current build document:
`Current/51_S1.42N_BABOON_HAWK_DEATH_TARGET_RESOLVER_BUILD.md`

Latest runtime analysis:
`Current/50_S1.42M_DEATH_CLEANUP_PARTIAL_PASS_ANALYSIS.md`

Machine-readable status:
`Current/Projektstatus_S1.42N.json`

## Latest runtime result — S1.42M

Evidence:
`RuntimeEvidence/S1.42M/20260903T163446Z/`

Log SHA-256:
`0639d5cc04aa54f5d7943ef4689e0d705c818871b019287ca1a1cdc2aa2492fb`

PASS:
- Dead Baboon Hawk body appears;
- Pikmin can carry the body to the Onion;
- living Baboon Hawks ignore the body;
- no `Leader is null when following`;
- live Pikmin -> Hawk attack/latch/kill remains functional.

FAIL:
- Pikmin attacking the Hawk still disappear when the Hawk dies.

Decisive marker:
`released 0/0 latched Pikmin`

The exact `PikminAI.RemoveCurrentTask()` method resolved successfully. The failure was S1.42M target discovery: attacking Pikmin are not children of the Hawk transform.

## Binding desired Baboon Hawk behavior

Living Hawk -> Pikmin:
blocked target/chase/bite/grab/hold.

Pikmin -> living Hawk:
normal attack/latch/kill allowed.

On Hawk death:
- attacking Pikmin detach and remain usable;
- SellBodies corpse remains enabled;
- Dead Baboon Hawk body remains carryable by players/Pikmin;
- Pikmin can carry it to the Onion;
- living Hawks cannot pick it up.

Do not restore the historical S1.42J two-way zero-interaction behavior.

## S1.42N scope

Only the death target resolver changes:
- exact `BaboonBirdAI.KillEnemy(bool)` death hook retained;
- exact runtime `PikminAI.RemoveCurrentTask()` retained;
- one-shot `RoundManager.Instance.SpawnedEnemies` candidate registry;
- only runtime objects assignable to `LethalMin.PikminAI`;
- under-Hawk or <= 4.0 m from dying Hawk;
- per-candidate diagnostics;
- S1.42M Dead Baboon Hawk corpse guard retained unchanged.

No continuous global scan.
No broad/inherited LethalMin scan.

## Exact next action

Import:
**Gale -> Advanced options -> Import all files**

Test S1.42N only:
1. throw Pikmin onto living Hawk;
2. let them kill it;
3. confirm attackers remain visible/usable;
4. confirm log has non-zero death-release count;
5. confirm corpse still appears;
6. confirm Pikmin can still carry corpse to Onion;
7. confirm living Hawks still ignore corpse;
8. confirm Hawk -> Pikmin ignore;
9. confirm no leader-null loop;
10. upload complete fresh log to `RuntimeInbox/Current/`.

## Temporary test state

EnemyIsolation:
enabled.

BCMER exact 1.71.0:
disabled.

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal spawning/BCMER before S1.42N is evaluated.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42N`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42N_BUILD_AWAITING_RUNTIME`

## Critical anti-regression

- no S1.42D broad/inherited LethalMin Harmony scan;
- no continuous Update-driven global EnemyAI scan;
- no silent BCMER 2.0.0 upgrade;
- do not remove the S1.42C enemy restore baseline;
- CodeRebirthLib must not return;
- unknown Enemy PowerLevels must not be guessed.

## Deferred maintenance

Do not clean unrelated documentation/source drift during the active S1.42N gate.

Known later cleanup:
- `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in `Patches/S139CompatibilityFixes/Plugin.cs`;
- structural optimization per `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`.
