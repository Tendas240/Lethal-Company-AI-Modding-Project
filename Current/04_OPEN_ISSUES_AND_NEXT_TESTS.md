# 04 — Open Issues and Next Tests

## Closed gate — S1.42U BCMER 1.71.0 Reactivation

**PASS**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Confirmed:

- exact BCMER 1.71.0 loads and finishes patching;
- Compatibility Fixes 1.3.14 loads;
- EnemyIsolation off;
- normal enemy population remains active (`ADDING ENEMY` = 13);
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- Fatal = 0;
- no crash/freeze;
- no gameplay-visible technical problem reported.

S1.42U is now the newest accepted full-normal-stack gameplay baseline and newest runtime-accepted technical descendant.

## Verified restore invariants

### Moon power counts / spawn pools

S1.42U `LethalLevelLoader.cfg` is byte-identical to the canonical S1.42C restore baseline.

All stored per-moon inside/daytime/nighttime maximum power counts and enemy spawning lists are therefore preserved exactly.

### Spawn timing

S1.42U SpawnCycleFixes remains byte-identical to S1.42C with:

`Consistent Spawn Times = true`

Preserve this. It standardizes the first spawn wave around 7:39 AM and prevents the vanilla vent-empty dependency from delaying the first outside/daytime wave.

## Active next planning task — S1.42V Post-BCMER Balance Tuning

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed**

Base:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Base SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

### Confirmed requested config changes

#### Immortal Snail

`BepInEx/config/dev.idjut.SnailFork.cfg`

`Rarity = 80 -> 40`

Keep `Max Snails = 2`.

#### CodeRebirth Functional Microwave

`BepInEx/config/CodeRebirth.cfg`

Current volume is confirmed at `0.7`; the previous reduction therefore exists in S1.42U.

Proposed next target after user reported it still sounds too loud:

`Functional Microwave | Volume = 0.5`

### Jetpack acceleration

Requested: modest acceleration increase.

Current ButteRyBalance uses `Control Scheme = V49`. This is a broad inertia/handling mode and must not be switched merely to approximate a small acceleration buff.

More Ship Upgrades has a real `Jet Fuel` acceleration upgrade currently configured at:

- `Initial Acceleration Increase = 20`;
- `Incremental Acceleration Increase = 20`.

That only affects purchased Jet Fuel tiers. If the desired buff is always-on base Jetpack acceleration, an exact narrow implementation must be identified first. Do not guess a config key or introduce broad movement changes.

Do not arm S1.42V until the exact Jetpack implementation is frozen.

## Enemy information verified from current stack/runtime

### Janitor / Scrap-E

Owner: CodeRebirth.

Runtime power count:

**1**

Gameplay role: cleanup/hoarding-style robot that collects loose scrap/debris and keeps it; strong claws make it an active threat around litter/scrap.

### Aloe

Owner: Biodiversity.

Runtime/config power count:

**1**

Gameplay role: neutral Bracken-like stalker that preferentially targets wounded players, kidnaps/drags them to a chosen location and heals them; players can struggle free. Current config keeps healing mode rather than damage mode.

### Immortal Snail

Runtime power count:

**1**

Current configured spawn rarity/weight:

**80**

## Broader tuning backlog — not automatically part of S1.42V

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwave rarity reduction.

Each must be explicitly listed with its exact delta before being mixed into a build.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

No S1.42V profile exists yet.

## Monitor-only issues

1. Historical S1.42S disconnect-only LethalMin NoticeZone NetworkObjectReference exception; absent in S1.42U.
2. Historical S1.42T one-off AloeChase FSB load-state message; no user-facing regression established.

## Permanent do-not-regress references

- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
- `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
- `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
- `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
