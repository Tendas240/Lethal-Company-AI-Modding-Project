# 04 — Open Issues and Next Tests

## Closed accepted baseline — S1.42U

**PASS**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

S1.42U remains the last fully accepted full-normal-stack gameplay baseline.

## Closed tuning evaluation — S1.42X

S1.42X technical paths worked, but the candidate was rejected for Jetpack balance and incomplete aerial-defense scope.

Profile:

`Profiles/LC V1 S1.42X Jetpack Pikmin ACU Retune.r2z`

SHA-256:

`57d8f9251236cf40eacf4366a21646ae8c51500b9ed6fa79cbc9b56c8daa611d`

Runtime evidence:

`RuntimeEvidence/S1.42X/20260904T115324Z/`

Raw log SHA-256:

`6fe57bda1c2a2a9e2a910304890e47b3fffd606460225bfd142ffae9fd996a9d`

Technical result:

- Jetpack plugin loaded and armed `10 -> 32`;
- CodeRebirth ACU plugin loaded;
- CodeRebirth 1.6.9 / DawnLib 0.9.25 / DawnLib.Dusk 0.9.25 validated;
- exact `code_rebirth:air_control_unit` provider validated;
- all 18 ACU curves scaled ×0.5;
- normal enemies remained active;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- Compatibility Fixes project error = 0.

Gameplay result:

- `32f` Jetpack acceleration is far too strong;
- Pikmin CarryStrength `3` / Purple `30` is correct and accepted;
- the Air Control Unit-only scope was incomplete because G.R.E.G. / Advanced Airspace Control is a separate `code_rebirth:gunslinger_greg` map object.

Record:

`Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`

## Active gate — S1.42Y

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Candidate:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Candidate record:

`Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`

Plan / Patch Safety Review:

`BuildSpecs/S1.42Y_PLAN.md`

Actions build run:

`33871219861` = success

## Exact S1.42Y changes

### Jetpack

- project-local DLL SHA-256: `fab15a520c1ff0172d33bc88303426d214b12135b34803f6e98689c295409c7e`;
- base acceleration `10f -> 22f` after ButteRyBalance;
- V49 handling/deceleration untouched;
- JetpackFixes safety behavior untouched;
- exact dependency/Harmony-owner fail-closed validation retained.

More Ship Upgrades:

- Jet Fuel initial/incremental acceleration = `15 / 15`;
- Jetpack Thrusters initial/incremental max speed = `25 / 20`.

### Pikmin

Preserve the user-confirmed values:

- Indoor Pikmin Spawn Chance = `0.08`;
- Blue / Red / Yellow / White / Winged / Rock / Ice / Glow / Bulbmin CarryStrength = `3`;
- Purple Pikmin CarryStrength = `30`.

### CodeRebirth aerial defense

Project-local DLL SHA-256:

`e017ccb74d92df10442bb5f8651a776787954f4861309059ec6c497e000a3d45`

The Y patch transactionally validates both exact providers before changing either:

1. `code_rebirth:air_control_unit` — 18 exact moon/tag curves;
2. `code_rebirth:gunslinger_greg` — G.R.E.G. / Advanced Airspace Control — 18 exact moon/tag curves.

After both contracts validate, both complete curve sets are scaled ×`0.5`. No unrelated map-object provider is changed.

The ×0.5 value is an exact curve-amplitude/spawn-weight reduction. DawnLib's later evaluation/rounding means short observed spawn counts need not be exactly half.

### Other tuning

- Functional Microwave Volume = `0.15`;
- Microwave spawn rarity remains deferred;
- Immortal Snail `Rarity = 40`;
- Immortal Snail `Max Snails = 2`.

## Exact next test

**Run S1.42Y. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

Import/run:

`LC V1 S1.42Y Jetpack Aerial Defense Retune`

Use Gale:

`Advanced options -> Import all files`

because Y contains two project-local DLLs.

Minimum checks:

1. startup/main menu succeeds;
2. `Loading [S1.42Y Jetpack Acceleration 1.0.0]` appears;
3. Jetpack dependency/owner validation succeeds;
4. exact `10 -> 22` armed marker appears;
5. `Loading [S1.42Y CodeRebirth Aerial Defense Spawn Tuning 1.0.0]` appears;
6. CodeRebirth 1.6.9 / DawnLib 0.9.25 / DawnLib.Dusk 0.9.25 validate;
7. Air Control Unit provider validates with exactly 18 curves;
8. G.R.E.G. provider validates with exactly 18 curves;
9. final transactional marker confirms both complete curve sets scaled ×0.5;
10. no aerial-defense contract-refusal marker;
11. 22f Jetpack is materially calmer than X/32f while still meaningfully stronger than old 10/16 behavior;
12. V49 handling, release/deactivation, landing, hard contact and repeated flights remain sane;
13. CarryStrength remains correct at 3 / Purple 30;
14. both aerial-defense systems remain functional and subjectively less common;
15. Microwave `0.15` is evaluated only if one is encountered;
16. Snail remains functional at rarity 40 / max 2;
17. BCMER 1.71.0, normal enemies and Compatibility Fixes 1.3.14 remain healthy;
18. Work/no-task = 0;
19. Leader-null = 0;
20. Fatal = 0;
21. no new project compatibility error flood;
22. commit and ingest the complete fresh runtime log.

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

## Deferred after S1.42Y

Do not silently mix into the current gate:

- equal probability for all installed interiors and same rule for future interiors;
- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction;
- BCMER EventTypes fixed to 8 × 12.5%;
- final long full-stack acceptance;
- AdditionalNetworking disconnect patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Y_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42Y;
- base SHA-256 = `f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

No successor is armed.

## Separate maintenance backlog

Known non-functional drift remains in older technical-baseline wording and historical comments inside the S139 Compatibility Fixes source. Keep cosmetic cleanup separate from runtime/gameplay tuning.
