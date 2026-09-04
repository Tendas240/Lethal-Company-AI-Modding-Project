# 04 — Open Issues and Next Tests

## Closed gate — S1.42U BCMER 1.71.0 Reactivation

**PASS**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

S1.42U remains the last fully accepted full-normal-stack baseline.

Confirmed accepted state:

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

## Active gate — S1.42V Post-BCMER Balance Tuning

**BUILD PASS / RUNTIME VALIDATION OPEN**

Candidate:

`Profiles/LC V1 S1.42V Post-BCMER Balance Tuning.r2z`

SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Candidate record:

`Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`

Frozen plan / Patch Safety Review:

`BuildSpecs/S1.42V_PLAN.md`

Build commit:

`1f5dd23eeb5b23d565af624fd97b78dcea58b784`

GitHub Actions run:

`33859188647` = **success**

Automated build verification:

- only `export.r2x`, Immortal Snail config and CodeRebirth config changed among existing members;
- exactly one new DLL added: `S142VJetpackAcceleration.dll`;
- no mod-state/add/remove change;
- all text assertions passed.

## Exact S1.42V changes under test

### Immortal Snail

`BepInEx/config/dev.idjut.SnailFork.cfg`

- `Rarity = 40`;
- `Max Snails = 2` preserved.

The deterministic requirement is the config change. A single run cannot statistically prove exactly half the final absolute spawn probability because `Rarity` participates in a weighted pool.

### CodeRebirth Functional Microwave

`BepInEx/config/CodeRebirth.cfg`

- `Functional Microwave | Volume = 0.5`;
- `Functional Microwave | Allow Editing Config = true` preserved.

Microwave spawn rarity remains a separate later backlog item.

### Always-on base Jetpack acceleration

Project-local plugin:

`BepInEx/plugins/S142VJetpackAcceleration/S142VJetpackAcceleration.dll`

DLL SHA-256:

`084fe47b5e47d3637fbb6d4fdd735429a37934993fc190fb4b6abbc51eada00c`

Frozen behavior:

- exact concrete target `JetpackItem.Update()`;
- Harmony Prefix ordered after ButteRyBalance;
- local player only;
- proven ButteRyBalance base `jetpackAcceleration = 10f -> 12f` (+20%);
- replacement only when the field is still approximately 10f;
- no fallback target, method skip or IL rewrite;
- fail-closed version/patch-owner verification.

Preserved:

- ButteRyBalance 0.7.0;
- `Control Scheme = V49`;
- `Warmup Period = false`;
- V49 handling/inertia and deceleration;
- Jetpack maximum-speed/power layer;
- battery and price;
- JetpackFixes 1.6.3 and `MidAirExplosions = Off`;
- More Ship Upgrades 3.14.1 Jet Fuel 20/20 purchase-gated layer;
- More Ship Upgrades Jetpack Thrusters maximum-speed layer.

## Exact next test

**Run S1.42V. Do not build a successor before this runtime gate is evaluated.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42V`

Minimum acceptance checks:

1. startup/main menu succeeds;
2. `S1.42V Jetpack Acceleration v1.0.0` loads;
3. plugin logs exact dependency validation and `armed`;
4. no Harmony target/transpiler/ordering exception;
5. exact BCMER 1.71.0 remains active and finishes patching;
6. Compatibility Fixes 1.3.14 loads unchanged;
7. normal enemies remain available/spawn normally;
8. unupgraded Jetpack accelerates modestly faster;
9. V49 directional handling/inertia remains unchanged;
10. no unintended maximum-speed/power change;
11. takeoff is normal;
12. release/deactivation is normal;
13. safe landing is normal;
14. hard collision and high-speed ground-touch behavior show no new JetpackFixes regression;
15. several repeated flights show no state accumulation or random mid-air explosion;
16. Immortal Snail remains functional at `Rarity = 40`, `Max Snails = 2`;
17. Functional Microwave remains functional and is audibly lower at `Volume = 0.5`;
18. if practical, purchase/test Jet Fuel once and confirm it remains a separate percentage layer on top of the base acceleration;
19. Work/no-task = 0;
20. Leader-null = 0;
21. no new project compatibility error/exception flood;
22. fresh complete runtime log is committed and ingested.

A heavy Baboon-Hawk stress test is not required unless new evidence reopens that path.

## Verified restore invariants — do not reopen without new evidence

### Moon power counts / spawn pools

S1.42U `LethalLevelLoader.cfg` is byte-identical to the canonical S1.42C restore baseline, Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

The S1.42V automated build did not change this archive member, so the same accepted per-moon inside/daytime/nighttime maximum power counts and spawn lists remain byte-identical in the candidate.

### Spawn timing

SpawnCycleFixes remains on:

`Consistent Spawn Times = true`

The S1.42V build did not change that member.

## Planned stage after S1.42V passes — Environment / Interior tuning

**No build ID assigned yet. Do not fold this into the current S1.42V runtime gate.**

Pending scope:

- equal probability for all installed interiors;
- permanent project rule: newly added interiors should receive the same probability as all other interiors unless deliberately overridden;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

Expected tests:

- deterministic config/delta verification;
- verify all intended interiors share equalized weight;
- multiple landings/reroutes;
- targeted `junkrooms` / `shatteredrooms` CullFactory behavior check;
- visual Mausoleum fog check;
- Microwave functionality plus lower occurrence over repeated normal play.

## Planned following stage — BCMER EventType balancing

**No build ID assigned yet. Keep separate from the environment/interior stage unless an explicit later decision changes it.**

Pending scope:

- fixed equal distribution: **8 EventTypes x 12.5%**.

Expected tests:

- deterministic config verification that all eight EventTypes are equally weighted;
- exact BCMER 1.71.0 preserved;
- repeated event/runtime coverage;
- no catastrophic event/system regression;
- do not claim statistical proof from a small runtime sample when configured weights are the primary evidence.

## Final S1.42 acceptance stage

After S1.42V plus later tuning stages pass independently:

- use/build the complete target full-stack profile;
- run a longer normal gameplay session;
- exercise varied enemies, Pikmin lifecycle, BCMER events, multiple interiors, Jetpack and CodeRebirth systems;
- ingest the complete runtime log;
- verify permanent compatibility/lifecycle counters and absence of crash/freeze;
- only then promote the final tuned profile as final S1.42 accepted baseline.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42V_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = built S1.42V candidate;
- base SHA-256 = `06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42V`

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
- `Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`

## Separate maintenance backlog

Known non-functional drift remains:

- stale historical local `current` wording in subsections of `Current/02_TECHNICAL_BASELINE.md`;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` that do not perfectly describe accepted v1.3.14 behavior.

Do not mix this cosmetic/documentation cleanup with runtime patch work.
