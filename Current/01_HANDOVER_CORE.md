# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/00_CURRENT_STATE.md`
2. `Current/83_S1.42W_BUILD_CANDIDATE_LIFT_MICROWAVE_LGU.md`
3. `Current/Projektstatus_S1.42W_CANDIDATE.json`
4. `BuildSpecs/S1.42W_PLAN.md`
5. `Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`
6. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
7. `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`
8. `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer S1.42W documents define the active test candidate. S1.42U remains the last fully accepted gameplay baseline.

## Accepted rollback baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

## S1.42V outcome

S1.42V proved the narrow Jetpack patch architecture in runtime but was not promoted because the user rejected the tuning magnitude.

Evidence:

`RuntimeEvidence/S1.42V/20260904T095739Z/`

Raw log SHA-256:

`5e094086efef862abdbaf1bfdaab85fb8c8ed20d73d865c9f1bc902e08180dfd`

Technical facts:

- Jetpack plugin loaded and armed;
- ButteRyBalance 0.7.0, JetpackFixes 1.6.3, More Ship Upgrades 3.14.1 validated;
- Compatibility Fixes 1.3.14 healthy;
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- user reported `12f` lift still too weak and Microwave `0.5` still too loud.

One AdditionalNetworking NetworkObjectReference Fatal occurred during local-disconnect teardown after BCMER `OnLocalDisconnect`; monitor only unless reproducible/user-facing.

Canonical S1.42V runtime record:

`Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`

## Active candidate

**S1.42W — Lift-Off Microwave Retune**

`Profiles/LC V1 S1.42W Lift-Off Microwave Retune.r2z`

SHA-256:

`f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`

Status:

**BUILD PASS / RUNTIME VALIDATION REQUIRED / NOT ACCEPTED**

Build commit:

`165d102364438cace2fd2184af3fd091855ff0d7`

Actions run:

`33861561173` = **success**

S1.42W was built directly from S1.42U to avoid stacking the superseded S1.42V Jetpack DLL.

## Exact S1.42W scope

### Jetpack base

- project plugin: `Patches/S142WJetpackAcceleration/`;
- DLL SHA-256: `95b7e689f68246ebda2fa6a0cab9fbe2ead206a00d85e6cbf64653d1f69d1fa8`;
- exact `JetpackItem.Update()` local-player Prefix after ButteRyBalance;
- base `10f -> 16f`;
- V49 handling/deceleration untouched;
- JetpackFixes safety logic untouched;
- fail-closed owner/version checks.

### LateGameUpgrades / More Ship Upgrades

Jet Fuel stays:

- initial acceleration `20%`;
- incremental acceleration `20%`.

It already scales automatically with the 16f base, giving 19.2 / 22.4 / 25.6 / 28.8 across 20/40/60/80% effects.

Jetpack Thrusters:

- initial max-speed increase `25%`;
- incremental max-speed increase `20%`.

### Other tuning

- Functional Microwave volume = `0.15`;
- Immortal Snail `Rarity = 40`;
- Immortal Snail `Max Snails = 2`.

## Permanent anti-regression state

Preserve:

- exact BCMER 1.71.0;
- EnemyIsolation off;
- Compatibility Fixes 1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin block only;
- native inherited PikminEnemy lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Never disable the entire `BaboonBirdPikminEnemy` just to block one interaction.

## Exact next action

**Runtime-test S1.42W. Do not build another successor yet.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

Run:

`LC V1 S1.42W Lift-Off Microwave Retune`

Use Gale `Advanced options -> Import all files` unless custom files are otherwise guaranteed to import.

Minimum gate:

1. S1.42W Jetpack plugin loads, validates dependencies/owners and logs `armed`;
2. lift-off is clearly faster and acceptable;
3. V49 handling remains acceptable;
4. release, landing, hard collision and high-speed ground touch remain sane;
5. repeated flights show no state accumulation/random mid-air explosion;
6. Jet Fuel and Thrusters remain useful;
7. Microwave `0.15` is acceptable and still functional;
8. Snail remains functional at 40 / max 2;
9. BCMER, normal enemies and Compatibility Fixes remain healthy;
10. Work/no-task = 0;
11. Leader-null = 0;
12. no new compatibility error flood;
13. ingest the complete fresh log.

## Deferred after W

Do not mix into the W gate:

- equal interior probability / future-interior rule;
- CullFactory exceptions;
- Mausoleum fog;
- Microwave rarity;
- BCMER 8 x 12.5% EventTypes;
- final long full-stack acceptance;
- AdditionalNetworking disconnect patch without new evidence.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42W_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42W candidate;
- base SHA-256 = `f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

No successor is armed.
