# 04 - Open Issues and Next Tests

## Immediate active gate - only remaining isolated enemy direction

**Build:** S1.42L - Pikmin Counterattack Restore

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Latest runtime:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

### Pending: Pikmin -> Baboon Hawk

Requirement:
Pikmin must be throwable onto a Baboon Hawk and must attack/latch it normally.

Existing S1.42L evidence:
- `Baboon hawk` is not on the Pikmin Attack Blacklist;
- LethalMin registers Baboon hawk as Pikmin enemy;
- one latch trigger is registered;
- Hawk-side adapter disable remains active;
- no leader-null loop occurred.

Missing:
explicit user/runtime confirmation that thrown Pikmin actually latch/attack the Hawk.

### Exact test

Do not build another candidate.

Use S1.42L unchanged:
1. throw Pikmin onto a Baboon Hawk;
2. confirm latch/attack;
3. confirm Hawk still ignores Pikmin from its own side;
4. confirm no bite/grab/hold loop;
5. confirm no `Leader is null when following`;
6. upload complete log to `RuntimeInbox/Current/`.

## Closed - do not retest unless regression appears

### Thumper / Crawler

**PASS / CLOSED**

- Pikmin -> Thumper attack/latch confirmed.
- Thumper -> Pikmin functional broken grab state blocked.
- 36 `[ThumperPikminGuard]` blocks.
- 0 leader-null errors.
- visible snapping is accepted as harmless cosmetic behavior.

### Puffer -> Pikmin

**PASS / CLOSED**

### Jetpack

**PASS / CLOSED**

- approximately 140-second target accepted;
- `MidAirExplosions = Off`;
- historical Coroner null flood absent.

### Baboon Hawk -> Pikmin

**PASS / CLOSED**

Exact adapter-disable/BitePikmin/GrabPikmin protection remains binding.

## After the remaining gate passes

1. remove/disable temporary EnemyIsolation;
2. restore normal enemy spawning/configuration from:
   `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve the accepted permanent asymmetric interaction rules;
5. runtime-check the restored normal state;
6. specifically monitor BCMER Door System ERROR / ship-door behavior;
7. document the resulting state before any repository migration.

## Pending gameplay/balance work after normal enemy/BCMER restore

### Functional Microwave

Current accepted:
`Functional Microwave | Volume = 0.7`

Future requirement:
Microwaves should be somewhat rarer.

Exact target rarity is not selected.
Do not change during the current isolated gate.

### Interiors

Binding:
all registered interiors should have equal effective probability on all moons where technically safe.

Target:
Weight 100 per interior/moon pairing.

Pending:
- normalize all current interiors;
- maintain equal-weight rule for future additions;
- CullFactory disable culling for exact IDs `junkrooms` and `shatteredrooms`;
- reduce fog only in MelanieMausoleum;
- keep Shatteredrooms Experimentation/Embrion block until safety is understood.

### BCMER final normal state

Pinned exact version:
1.71.0

Preserve ownership guards:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Keep BCMER rain event routes disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Vanilla Rainy remains allowed.

### Monitor only

- Mineshaft elevator + many Pikmin floor clipping/fall death: causality unproven.
- Outdoor Pikmin Sprout density: subjective concern only; no rebalance without statistics.

## Known noise - only escalate with user-facing symptoms

- SoundAPI TypeLoadException during floor reporting;
- SoftMaskKiller-protected SoftMask NREs;
- duplicate NetworkPrefab GlobalObjectIdHash warnings;
- RuntimeNavMeshBuilder unreadable-mesh messages;
- BCMER ButlerSword missing-script warning;
- historical S1.42C scene-teardown `Collection was modified`;
- Pikmin/NavMesh agent warnings;
- Coroner Baboon-Hawk player-damage noise separate from resolved Jetpack null flood.

## Do-not-regress

- no S1.42D broad/inherited LethalMin reflection/Harmony scan;
- no Update-driven continuous global EnemyAI scan for EnemyIsolation;
- no BCMER 2.0.0 migration without explicit decision;
- no removal of `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- no CodeRebirthLib return;
- no guessing unknown Enemy PowerLevels;
- no local clone/build request while GitHub infrastructure is sufficient.

## Build/runtime controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42L`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

## Deferred repository maintenance

`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Status:
**DEFERRED_UNTIL_ACTIVE_GATE_COMPLETE**

Do not begin structural migration until the last S1.42L gate and post-gate normal enemy/BCMER state have been documented.
