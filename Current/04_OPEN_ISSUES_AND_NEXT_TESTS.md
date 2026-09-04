# 04 — Open Issues and Next Tests

## Closed accepted baseline — S1.42U

**PASS**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

S1.42U remains the last fully accepted full-normal-stack gameplay baseline.

## Closed tuning evaluation — S1.42V

S1.42V Jetpack architecture was proven at runtime, but its balance values were rejected by user feedback.

Runtime evidence:

`RuntimeEvidence/S1.42V/20260904T095739Z/`

Raw log SHA-256:

`5e094086efef862abdbaf1bfdaab85fb8c8ed20d73d865c9f1bc902e08180dfd`

Technical result:

- S1.42V Jetpack plugin loaded;
- ButteRyBalance 0.7.0 / JetpackFixes 1.6.3 / More Ship Upgrades 3.14.1 validated;
- patch armed successfully;
- Compatibility Fixes 1.3.14 loaded;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- no Jetpack Harmony owner/target/order failure.

Balance result:

- `12f` lift-off still too weak;
- Microwave `0.5` still too loud.

Record:

`Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`

One AdditionalNetworking NetworkObjectReference Fatal occurred during local-disconnect teardown after BCMER `OnLocalDisconnect`; monitor only unless it becomes reproducible before disconnect or user-facing.

## Active gate — S1.42W

**BUILD PASS / RUNTIME VALIDATION OPEN**

Candidate:

`Profiles/LC V1 S1.42W Lift-Off Microwave Retune.r2z`

SHA-256:

`f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`

Candidate record:

`Current/83_S1.42W_BUILD_CANDIDATE_LIFT_MICROWAVE_LGU.md`

Plan / Patch Safety Review:

`BuildSpecs/S1.42W_PLAN.md`

Build commit:

`165d102364438cace2fd2184af3fd091855ff0d7`

Actions run:

`33861561173` = success

## Exact S1.42W changes

### Jetpack

- S1.42W project-local DLL SHA-256: `95b7e689f68246ebda2fa6a0cab9fbe2ead206a00d85e6cbf64653d1f69d1fa8`;
- base acceleration `10f -> 16f` after ButteRyBalance;
- V49 handling/deceleration untouched;
- JetpackFixes safety logic untouched;
- exact dependency/Harmony-owner fail-closed validation retained.

### LateGameUpgrades / More Ship Upgrades

Jet Fuel remains:

- `Initial Acceleration Increase = 20`;
- `Incremental Acceleration Increase = 20`.

This already scales automatically with base 16f, producing 19.2 / 22.4 / 25.6 / 28.8 at 20/40/60/80% effects.

Jetpack Thrusters:

- `Initial Maximum Speed Increase = 25`;
- `Incremental Maximum Speed Increase = 20`.

### Microwave

`Functional Microwave | Volume = 0.15`

Microwave spawn rarity remains deferred.

### Immortal Snail

- `Rarity = 40`;
- `Max Snails = 2`.

## Exact next test

**Run S1.42W. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

Import/run:

`LC V1 S1.42W Lift-Off Microwave Retune`

Use Gale `Advanced options -> Import all files` unless all custom files are otherwise guaranteed to import.

Minimum checks:

1. startup/main menu succeeds;
2. `Loading [S1.42W Jetpack Acceleration 1.0.0]` appears;
3. dependency/owner validation succeeds;
4. `S1.42W Jetpack acceleration patch armed` appears;
5. BCMER 1.71.0 and Compatibility Fixes 1.3.14 remain healthy;
6. normal enemies still spawn;
7. lift-off is clearly faster than S1.42V and subjectively acceptable;
8. V49 handling/inertia remains acceptable;
9. release/deactivation and safe landing remain sane;
10. hard collision and high-speed ground touch show no new JetpackFixes regression;
11. repeated flights show no random mid-air explosion/state accumulation;
12. Jet Fuel remains useful as purchase-gated acceleration progression;
13. Jetpack Thrusters remains useful without obvious instability;
14. Microwave remains functional and `0.15` is acceptably quiet;
15. Snail remains functional at rarity 40 / max 2;
16. Work/no-task = 0;
17. Leader-null = 0;
18. no new project compatibility error flood;
19. commit and ingest the complete fresh runtime log.

## Verified restore invariants — do not reopen without evidence

- S1.42C-derived `LethalLevelLoader.cfg` moon power/spawn baseline;
- `Consistent Spawn Times = true`;
- exact BCMER 1.71.0;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14;
- narrow Baboon Hawk -> Pikmin block with native lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- normal enemy population.

## Deferred after S1.42W

Do not silently mix into the current gate:

- equal probability for all installed interiors and same rule for future interiors;
- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction;
- BCMER EventTypes fixed to 8 x 12.5%;
- final long full-stack acceptance;
- AdditionalNetworking disconnect patch without reproducible/user-facing evidence.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42W_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42W;
- base SHA-256 = `f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

No successor is armed.

## Separate maintenance backlog

Known non-functional drift remains in older technical-baseline wording and historical comments inside the S139 Compatibility Fixes source. Keep cosmetic cleanup separate from runtime/gameplay tuning.
