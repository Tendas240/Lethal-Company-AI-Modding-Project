# 00 — Current State

**Updated:** 2026-09-04 — after successful S1.42V candidate build  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Current canonical state

### Last fully accepted full-normal-stack baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Profile SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Final S1.42U handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

Verdict:

**PASS — exact BCMER 1.71.0 restored, normal enemy population retained, no critical compatibility/lifecycle regression, no gameplay-visible technical problem reported.**

S1.42U remains the accepted canonical baseline until S1.42V passes fresh runtime validation.

### Newest built candidate

**S1.42V — Post-BCMER Balance Tuning**

Profile:

`Profiles/LC V1 S1.42V Post-BCMER Balance Tuning.r2z`

Profile SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Status:

**BUILD PASS / CANDIDATE ONLY / RUNTIME VALIDATION REQUIRED**

Build candidate record:

`Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`

Frozen build plan and Patch Safety Review:

`BuildSpecs/S1.42V_PLAN.md`

Automated build result:

`Current/AUTO_BUILD_RESULT.json`

Automated build commit:

`1f5dd23eeb5b23d565af624fd97b78dcea58b784`

GitHub Actions run:

`33859188647` = **success**

S1.42V is not runtime accepted yet and must not replace S1.42U as the canonical accepted baseline until the runtime gate passes.

## Exact S1.42V delta

The automated builder verified that only these existing archive members changed:

1. `export.r2x` — profile name;
2. `BepInEx/config/dev.idjut.SnailFork.cfg`;
3. `BepInEx/config/CodeRebirth.cfg`.

Exactly one new archive member was added:

`BepInEx/plugins/S142VJetpackAcceleration/S142VJetpackAcceleration.dll`

No package add/remove/enable/disable change occurred and no other existing archive member changed.

### Immortal Snail

`BepInEx/config/dev.idjut.SnailFork.cfg`

- `Rarity = 40`;
- `Max Snails = 2` preserved.

### Functional Microwave

`BepInEx/config/CodeRebirth.cfg`

- `Functional Microwave | Volume = 0.5`;
- functionality/editing flag preserved.

Microwave spawn rarity is still deferred.

### Always-on base Jetpack acceleration

Project-local plugin:

`Patches/S142VJetpackAcceleration/`

Injected DLL SHA-256:

`084fe47b5e47d3637fbb6d4fdd735429a37934993fc190fb4b6abbc51eada00c`

Frozen behavior:

- exact target `JetpackItem.Update()`;
- local-player prefix ordered after ButteRyBalance;
- ButteRyBalance-owned base `jetpackAcceleration = 10f` becomes `12f` (+20%);
- only the proven approximately-10f baseline value is replaced;
- every non-10 value remains untouched;
- exact ButteRyBalance 0.7.0 and JetpackFixes 1.6.3 are required/validated;
- More Ship Upgrades 3.14.1 is validated when loaded;
- expected Harmony owners are verified before the project-local patch arms;
- no fallback target or broad transpiler is used.

Preserved exactly:

- ButteRyBalance `Control Scheme = V49`;
- ButteRyBalance `Warmup Period = false`;
- V49 `jetpackForceChangeSpeed`/inertia handling;
- deceleration;
- Jetpack maximum-speed/power layer;
- Jetpack battery and price;
- JetpackFixes `MidAirExplosions = Off` and collision/death logic;
- More Ship Upgrades `Jet Fuel` values (`20` initial / `20` incremental);
- More Ship Upgrades `Jetpack Thrusters` values.

The exact owner/code/lifecycle/safety analysis is canonical in:

- `BuildSpecs/S1.42V_PLAN.md`;
- `Patches/S142VJetpackAcceleration/README.md`;
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## S1.42U runtime facts that remain the accepted baseline evidence

Confirmed from the complete accepted S1.42U runtime log:

- `Loading [BrutalCompanyMinusExtraReborn 1.71.0]`;
- `BrutalCompanyMinusExtraReborn 1.71.0 is done patching.`;
- `Loading [S1.39 Compatibility Fixes 1.3.14]`;
- EnemyIsolation disabled;
- `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- Fatal = 0;
- historical disconnect NoticeZone / unspawned NetworkObjectReference marker = 0;
- no crash/freeze;
- known setup SoundAPI/SoftMask exception classes did not become a gameplay cascade;
- user reported no gameplay-visible technical problem.

Direct runtime power evidence:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1;
- Crawler = 3;
- Bunker Spider = 2.

Runtime evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

## Permanent compatibility state to preserve

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Preserve:

- exact BCMER 1.71.0 enabled unless a deliberate diagnostic gate says otherwise;
- EnemyIsolation off;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- Pikmin -> Baboon Hawk attacks;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- restored normal enemy population.

Never-repeat root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Never disable the complete `LethalMin.BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction.

## Moon power-count / spawn restore verification

S1.42U:

`ProfileSources/S1.42U/BepInEx/config/LethalLevelLoader.cfg`

is byte-identical to the canonical S1.42C restore file:

`ProfileSources/S1.42C/BepInEx/config/LethalLevelLoader.cfg`

Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

The S1.42V automated build changed no LethalLevelLoader member, so this accepted moon power/spawn baseline is preserved byte-identically in the candidate.

Do not wholesale regenerate or normalize this file.

## Enemy spawn timing

S1.42U SpawnCycleFixes remained byte-identical to S1.42C with:

`Consistent Spawn Times = true`

The S1.42V build did not change this member.

## Immediate next action — S1.42V runtime gate

Do **not** build a successor yet.

Run:

`LC V1 S1.42V Post-BCMER Balance Tuning`

Then commit a fresh complete runtime log under the normal RuntimeInbox flow. `RuntimeInbox/ACTIVE_BUILD.txt` now points to `S1.42V`.

At minimum verify:

1. startup/main menu succeeds;
2. `S1.42V Jetpack Acceleration v1.0.0` validates dependencies/owners and logs that it armed;
3. no Harmony patch/target/transpiler exception;
4. BCMER 1.71.0 and Compatibility Fixes 1.3.14 remain healthy;
5. normal enemies still spawn;
6. unupgraded Jetpack acceleration is modestly higher;
7. V49 handling/inertia remains unchanged;
8. no unintended maximum-speed/power change;
9. takeoff, release/deactivation, safe landing, hard collision and high-speed ground touch remain sane;
10. repeat several Jetpack flights to catch state accumulation/random mid-air explosion regressions;
11. Snail remains functional at `Rarity = 40`, `Max Snails = 2`;
12. Microwave remains functional and is audibly lower at `Volume = 0.5`;
13. if practical, test purchased Jet Fuel once to verify it remains a separate percentage layer;
14. Work/no-task = 0;
15. Leader-null = 0;
16. no new compatibility exception flood;
17. ingest the complete fresh log.

A heavy Baboon-Hawk stress retest is not required unless new evidence reopens that path.

## Planned stages after S1.42V passes

Later stage IDs are intentionally **not assigned yet**.

### Environment / Interior tuning

Pending:

- equal probability for all installed interiors; newly added interiors should follow the same equal-probability project rule;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

### BCMER EventType balancing

Pending:

- fixed equal distribution: **8 x 12.5% EventTypes**.

### Final S1.42 full-stack acceptance

After the tuning stages pass independently:

- longer normal gameplay run;
- varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth systems;
- complete log ingest and critical-marker comparison;
- promote the resulting profile as final S1.42 baseline only if clean.

Do not silently mix any of these later scopes into S1.42V runtime validation.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42V_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = built S1.42V candidate;
- base SHA-256 = `06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`;
- no successor delta armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42V`

## Monitor-only issues

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception. It did not recur in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message. No gameplay impact established.
3. Known setup loaforcsSoundAPI/HarmonyX and SoftMaskKiller-handled exception classes remain non-blocking unless they change behavior, flood or become user-facing.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains older comments that do not perfectly describe accepted v1.3.14 behavior.

Actual current code/config/runtime evidence and chronologically newer canonical documents are authoritative. Cleanup remains separate maintenance and must not be mixed into risky gameplay patches.
