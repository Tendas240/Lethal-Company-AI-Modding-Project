# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/00_CURRENT_STATE.md`
2. `Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`
3. `BuildSpecs/S1.42V_PLAN.md`
4. `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`
5. `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`
6. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
7. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
8. `Current/Projektstatus_S1.42U.json`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
12. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
13. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
14. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
15. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
16. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
17. `BuildSpecs/current.json`
18. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer S1.42V candidate documentation controls the active test state. S1.42U acceptance/handover/audit documents remain authoritative for the last fully accepted baseline.

## Last accepted baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime verdict:

**PASS — last fully accepted full-normal-stack baseline.**

Acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Compatibility/plugin invariants accepted in S1.42U remain the rollback contract for S1.42V.

## Newest built candidate

**S1.42V — Post-BCMER Balance Tuning**

Profile:

`Profiles/LC V1 S1.42V Post-BCMER Balance Tuning.r2z`

SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Status:

**BUILD PASS / RUNTIME VALIDATION REQUIRED / NOT ACCEPTED**

Candidate record:

`Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`

Automated build commit:

`1f5dd23eeb5b23d565af624fd97b78dcea58b784`

GitHub Actions run:

`33859188647` = **success**

Automated archive verification reported exactly three changed existing members and one added DLL, with no package-state changes.

## Exact S1.42V scope

### Immortal Snail

- `Rarity = 80 -> 40`;
- `Max Snails = 2` preserved.

### Functional Microwave

- `Functional Microwave | Volume = 0.7 -> 0.5`;
- spawn rarity is still deferred.

### Always-on base Jetpack acceleration

Project-local patch:

`Patches/S142VJetpackAcceleration/`

Injected DLL SHA-256:

`084fe47b5e47d3637fbb6d4fdd735429a37934993fc190fb4b6abbc51eada00c`

Frozen behavior:

- exact `JetpackItem.Update()` target;
- local-player prefix after ButteRyBalance;
- proven base `jetpackAcceleration = 10f -> 12f` (+20%);
- only an approximately-10f value is replaced;
- fail-closed version/owner validation;
- no fallback/IL rewrite/original-method skip.

Owner interactions:

- ButteRyBalance 0.7.0 remains the base acceleration/handling owner and `Control Scheme = V49` is preserved;
- `Warmup Period = false` preserved;
- JetpackFixes 1.6.3 still owns collision/death/control fixes and `MidAirExplosions = Off` remains unchanged;
- More Ship Upgrades 3.14.1 `Jet Fuel` remains purchase-gated at 20/20 and layers over the base value;
- `Jetpack Thrusters` maximum-speed layer remains separate and unchanged.

Full Patch Safety Review:

`BuildSpecs/S1.42V_PLAN.md`

and:

`Patches/S142VJetpackAcceleration/README.md`

## Permanent technical state to preserve

- BCMER exact 1.71.0 enabled;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14;
- compatibility DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer -> Pikmin protection;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- normal enemy population restored;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Never repeat the S1.42R approach of disabling the whole `BaboonBirdPikminEnemy` adapter to block one interaction.

## Exact next action

**Runtime-test S1.42V. Do not build a successor yet.**

Run:

`LC V1 S1.42V Post-BCMER Balance Tuning`

`RuntimeInbox/ACTIVE_BUILD.txt` now points to `S1.42V`.

Minimum gate:

1. startup/main menu succeeds;
2. `S1.42V Jetpack Acceleration v1.0.0` validates exact dependencies/owners and logs `armed`;
3. no Harmony target/transpiler/ordering exception;
4. BCMER 1.71.0 and Compatibility Fixes 1.3.14 load normally;
5. normal enemies still spawn;
6. Jetpack base acceleration is modestly higher;
7. V49 handling/inertia remains unchanged;
8. no unintended maximum-speed/power change;
9. takeoff, release/deactivation, safe landing, hard collision and high-speed ground touch remain sane;
10. repeat Jetpack flights show no state accumulation/random mid-air explosion;
11. Immortal Snail remains functional at `Rarity = 40`, `Max Snails = 2`;
12. Functional Microwave remains functional and is audibly lower at `Volume = 0.5`;
13. if practical, test purchased Jet Fuel once as a separate percentage layer;
14. Work/no-task = 0;
15. Leader-null = 0;
16. no new compatibility exception flood;
17. commit/ingest a fresh complete runtime log.

S1.42U remains canonical accepted until this gate passes.

## Planned stages after S1.42V

Do not mix these into the current runtime gate.

### Environment / Interior tuning

- equal probability for all installed interiors and same rule for newly added interiors;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

### BCMER EventType balancing

- fixed equal distribution: **8 x 12.5% EventTypes**.

### Final S1.42 full-stack acceptance

- longer normal full-stack run after independent tuning gates pass;
- varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth coverage;
- full log ingest and permanent invariant check;
- promote only if clean.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42V_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = built S1.42V candidate;
- base SHA-256 = `06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`;
- no successor delta armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42V`

## Monitor-only observations

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception; absent in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message; no user-facing regression established.
3. Known setup SoundAPI/HarmonyX and SoftMaskKiller-handled exception classes remain non-blocking unless behavior changes, they flood, or become user-facing.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior.

Do not mix cosmetic cleanup with risky gameplay/runtime changes.

## Patch policy

All project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review. S1.42V satisfies this requirement in `BuildSpecs/S1.42V_PLAN.md` and `Patches/S142VJetpackAcceleration/README.md`.

## Local work

No local repository clone or local build is required. GitHub-native build infrastructure produced and verified the S1.42V candidate.
