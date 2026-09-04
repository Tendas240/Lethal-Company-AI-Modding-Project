# 04 — Open Issues and Next Tests

## Closed gate — S1.42U BCMER 1.71.0 Reactivation

**PASS**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Final handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Confirmed:

- exact BCMER 1.71.0 loads and finishes patching;
- Compatibility Fixes 1.3.14 loads;
- EnemyIsolation off;
- normal enemy population active (`ADDING ENEMY` = 13);
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- Fatal = 0;
- old NoticeZone/unspawned NetworkObjectReference regression absent;
- no crash/freeze;
- no gameplay-visible technical problem reported.

S1.42U is the newest accepted full-normal-stack gameplay baseline and newest runtime-accepted technical descendant. There is no newer built candidate.

## Verified restore invariants — already correct

### Moon power counts / spawn pools

S1.42U `LethalLevelLoader.cfg` is byte-identical to the canonical S1.42C restore baseline, Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

All stored per-moon inside/daytime/nighttime maximum power counts and enemy spawning lists are therefore preserved exactly.

Do not reopen this as a repair task unless a later build actually changes the file or new runtime evidence contradicts the baseline.

### Spawn timing

S1.42U SpawnCycleFixes remains byte-identical to S1.42C with:

`Consistent Spawn Times = true`

Preserve this. It standardizes the first spawn wave around 07:39 and prevents the vanilla vent-empty dependency from delaying the first outside/daytime wave.

## Active next planning task — S1.42V Post-BCMER Balance Tuning

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed / no S1.42V profile exists.**

Base:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Base SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

### Confirmed requested config changes

#### Immortal Snail

`BepInEx/config/dev.idjut.SnailFork.cfg`

`Rarity = 80 -> 40`

Keep:

`Max Snails = 2`

The deterministic requirement is the config change. A single runtime run cannot statistically prove exactly half the final absolute spawn probability because this is a weighted pool value.

#### CodeRebirth Functional Microwave volume

`BepInEx/config/CodeRebirth.cfg`

Current:

`Functional Microwave | Volume = 0.7`

The prior reduction survived into S1.42U, but the user still perceived it as too loud.

Proposed next target:

`Functional Microwave | Volume = 0.5`

Microwave spawn rarity is a separate later backlog item; do not confuse frequency with volume.

### Jetpack acceleration — blocking implementation question

User requirement:

**modest always-on base Jetpack acceleration increase.**

Current ButteRyBalance:

`Control Scheme = V49`

This is a broad inertia/handling mode, not a numeric base-acceleration knob. Do not switch V49 -> Vanilla/Dynamic merely to approximate the requested change.

More Ship Upgrades `Jet Fuel` currently has:

- `Initial Acceleration Increase = 20`;
- `Incremental Acceleration Increase = 20`.

That only affects purchased Jet Fuel tiers. It is not the requested unconditional base behavior unless the user explicitly changes scope.

### Exact next technical action

Before S1.42V may be armed:

1. identify the exact runtime owner/method/field controlling base Jetpack acceleration;
2. inspect interaction with ButteRyBalance V49 and JetpackFixes;
3. prefer a narrow existing config/owner if one truly exists;
4. do not invent a config key;
5. do not silently substitute a purchase-gated Jet Fuel change;
6. if project-local code is necessary, perform a Patch Safety Review and isolate that code change from unrelated balance changes if practical;
7. freeze the exact file/value/code delta;
8. then arm `BuildSpecs/current.json` and build repository-first through GitHub Actions.

## S1.42V test gate

At minimum after the build:

1. startup/main menu succeeds;
2. exact BCMER 1.71.0 remains active and finishes patching;
3. Compatibility Fixes 1.3.14 loads;
4. normal enemies remain available/spawn normally;
5. deterministic Snail config is `Rarity = 40`, `Max Snails = 2` and Snail still functions;
6. Functional Microwave is audibly lower without functional regression;
7. Jetpack acceleration is modestly higher as intended;
8. no unintended max-speed, V49 inertia/handling, explosion/death or JetpackFixes regression;
9. Work/no-task = 0;
10. Leader-null = 0;
11. no new project compatibility error/exception flood;
12. fresh complete runtime log is ingested.

A heavy Baboon-Hawk stress test is not required unless the Jetpack implementation unexpectedly touches compatibility code or new evidence reopens that path.

## Planned stage after S1.42V — Environment / Interior tuning

**No build ID assigned yet. Do not silently fold this into S1.42V.**

Pending scope:

- equal probability for all installed interiors;
- permanent project rule: newly added interiors should receive the same probability as all other interiors unless deliberately overridden;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

Expected tests:

- deterministic config/delta verification;
- verify all intended interiors share the equalized weight;
- multiple landings/reroutes to exercise different interiors;
- targeted `junkrooms` / `shatteredrooms` CullFactory behavior check;
- visual Mausoleum fog check;
- Microwave remains functional and is less common over repeated normal play.

Do not claim a precise empirical rarity percentage from only a handful of runs when the config can be verified deterministically.

## Planned following stage — BCMER EventType balancing

**No build ID assigned yet. Keep separate from the environment/interior stage unless a later explicit decision changes that.**

Pending scope:

- fixed equal distribution: **8 EventTypes x 12.5%**.

Expected tests:

- exact deterministic config verification that all eight EventTypes are equally weighted;
- exact BCMER 1.71.0 preserved;
- multiple BCMER event/runtime runs for functional coverage;
- no catastrophic event/system regression;
- do not pretend a small runtime sample statistically proves 12.5% when the configured weights are the primary evidence.

## Final S1.42 acceptance stage

After S1.42V plus later tuning stages pass individually:

- build/use the complete target full-stack profile;
- run a longer normal gameplay session;
- exercise varied enemies, Pikmin lifecycle, BCMER events, multiple interiors, Jetpack and CodeRebirth systems;
- ingest the complete runtime log;
- verify critical compatibility/lifecycle counters and absence of crash/freeze;
- only then promote the final tuned profile as the final S1.42 accepted baseline.

## Enemy information verified from current stack/runtime

### Janitor / Scrap-E

Owner: CodeRebirth.  
Runtime power count: **1**.  
Role: cleanup/hoarding-style robot that collects loose scrap/debris and keeps it; strong claws make it an active threat around litter/scrap.

### Aloe

Owner: Biodiversity.  
Runtime/config power count: **1**.  
Role: neutral Bracken-like stalker that preferentially targets wounded players, drags them to a chosen location and heals them; current config keeps healing mode rather than damage mode.

### Immortal Snail

Runtime power count: **1**.  
Current configured spawn rarity/weight: **80**.  
Requested next value: **40**.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U;
- no successor change armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

## Monitor-only issues

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception; absent in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message; no user-facing regression established.
3. Known setup loaforcsSoundAPI/HarmonyX TypeLoadException and SoftMaskKiller-handled SoftMask NullReferenceException classes are non-blocking unless they change, flood or become user-facing.

## Permanent do-not-regress references

- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
- `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
- `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
- `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
- `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
- `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

## Separate maintenance backlog

Known non-functional drift remains:

- older stale local `current` wording in subsections of `Current/02_TECHNICAL_BASELINE.md`;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` that do not perfectly describe accepted v1.3.14 behavior.

Do not mix this cosmetic/documentation cleanup with risky runtime patch work.
