# 01 - Handover Core

This is the compact current-state handover. For the complete latest handover, read:
`Current/45_HANDOVER_S1.42L_TO_NEXT_FINAL.md`

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Current built/runtime-tested candidate:
**S1.42L - Pikmin Counterattack Restore**

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Latest runtime:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

## Current verdict

Closed/PASS:
- Thumper/Crawler -> Pikmin protection;
- Pikmin -> Thumper/Crawler attack/latch;
- Puffer -> Pikmin immunity;
- Jetpack;
- Baboon Hawk -> Pikmin protection.

Only open isolated direction:
**Pikmin -> Baboon Hawk attack/latch.**

Do not build another profile before testing that direction on S1.42L.

## Binding asymmetric enemy/Pikmin rules

### Thumper / Crawler

Enemy -> Pikmin:
blocked functional GrabPikmin / leader-removal / grabbed-death-state effect.

Pikmin -> enemy:
normal attack/latch allowed.

Visible snapping by the Thumper is accepted as harmless and should be ignored.

### Baboon Hawk

Enemy -> Pikmin:
blocked target/chase/bite/grab/hold through exact adapter disable + BitePikmin block + common GrabPikmin failsafe.

Pikmin -> enemy:
normal attack/latch must be allowed.

### Puffer

Puffer -> Pikmin:
no effect.

## Exact next action

Keep S1.42L.

Import with:
**Gale -> Advanced options -> Import all files**

Test only:
1. throw Pikmin onto a Baboon Hawk;
2. verify normal Pikmin latch/attack;
3. verify the Hawk itself continues to ignore Pikmin;
4. verify no leader-null loop;
5. upload complete log to `RuntimeInbox/Current/`.

## Temporary test state

EnemyIsolation:
enabled.

BCMER:
exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` disabled.

Do not restore normal spawning or BCMER before the remaining direction is accepted.

After PASS:
- remove EnemyIsolation;
- restore normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0;
- preserve accepted permanent interaction rules.

## Critical technical lineage

S1.42D broad/inherited LethalMin reflection/Harmony scanning caused startup crash.
Never reintroduce it.

Use exact declared types/methods and narrow lifecycle anchors.

EnemyIsolation must not use an Update-driven continuous global EnemyAI scene scan.

S1.42I and S1.42K were built but never runtime-tested and must not be treated as runtime evidence.

## Important persistent accepted fixes

- CodeRebirth natural Coin / Crisp Dollar Bill / Wallet suppression retained.
- Natural Flash Turret suppression retained.
- LethalModDataLib 1.2.2 null-plugin guard confirmed.
- Recharge station full heal retained.
- Autonomous Crane cannot kill Pikmin/Puffmin.
- Leaf Boy remains on LethalMin Attack Blacklist.
- Ogopogo and Vermin disabled.
- SCP999 disabled.
- AJB Keep Hangar Ship Door Closed disabled while project-local failsafe exists.
- Old Bird Resonance retained.
- Mirage recording retention retained.
- CodeRebirthLib must not return.

## BCMER persistent rules

Pinned:
**1.71.0**

Do not silently migrate to 2.0.0.

Preserve after re-enable:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Disabled BCMER rain routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Vanilla natural Rainy remains allowed.

## Lower-priority work after active gate

- re-check BCMER Door System ERROR / ship-door behavior after BCMER is re-enabled;
- make Functional Microwaves somewhat rarer once an exact target is selected;
- interior equal-probability normalization;
- CullFactory exact IDs `junkrooms`, `shatteredrooms`;
- MelanieMausoleum fog reduction;
- preserve Shatteredrooms Experimentation/Embrion safety block until understood;
- monitor Mineshaft elevator/Pikmin crowding;
- do not rebalance outdoor Pikmin Sprout density without statistics.

## Repository-first

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`
- `Patches/`

No local clone/build is needed while repository infrastructure contains the required bases.

## Deferred maintenance

Repository optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Do not start it until the active S1.42L direction gate and post-gate normal-enemy/BCMER state are documented.

Historical detail remains available in:
- `Current/03_PROJECT_CHRONOLOGY.md`
- `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
- older handovers/analysis files;
- `RuntimeEvidence/`.
