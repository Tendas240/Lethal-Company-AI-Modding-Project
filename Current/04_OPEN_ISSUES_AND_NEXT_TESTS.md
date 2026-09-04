# 04 — Open Issues and Next Tests

## Closed accepted gate — S1.42Z

**PASS / ACCEPTED**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

Raw log SHA-256:

`ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

Coverage:

- 1,586,159 bytes;
- 16,094 lines;
- 15,325 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

Confirmed technical gate:

- S1.42Z Jetpack plugin loaded and exact `10 -> 18` path armed;
- ButteRyBalance `0.7.0`, JetpackFixes `1.6.3`, More Ship Upgrades `3.14.1` validated;
- S1.42Z CodeRebirth aerial-defense plugin loaded;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validated;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. provider validated with exactly 18 curves;
- transactional ×0.5 scaling applied to both complete sets;
- no aerial-defense contract refusal;
- EnemyIsolation diagnostic isolation disabled;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0;
- no Error-severity output from either S1.42Z project-local plugin.

User runtime verdict:

**Everything is in order.**

The subjective balance gate is closed. S1.42Z is now the canonical accepted full-normal-stack baseline.

## Accepted S1.42Z tuning

### Jetpack

- base acceleration `10f -> 18f`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- V49 handling/deceleration preserved;
- JetpackFixes safety behavior preserved.

Jetpack DLL SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth aerial defense

- Air Control Unit exact 18-curve provider ×0.5;
- G.R.E.G. exact 18-curve provider ×0.5;
- transactional all-or-nothing validation retained;
- no other map-object provider modified.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

### Accepted carried tuning

- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`.

## Error-severity classification

The 32 Error-severity events do not represent a new S1.42Z project-local regression. Observed exception classes remain within already monitored non-project-local/setup classes, including the known loaforcsSoundAPI/HarmonyX `TypeLoadException` and SoftMask/SoftMasking setup `NullReferenceException` class.

Do not patch these classes without stronger reproducibility or user-facing impact.

## No active runtime gate

There is currently **no successor candidate to test**.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

This identifies the latest accepted runtime build until another candidate is explicitly designated.

## Next planned stage

When the user requests the next gameplay/config build, start with the deferred interior-probability scope:

1. determine the complete currently installed interior set from the accepted S1.42Z profile;
2. make every installed interior have equal effective selection probability;
3. implement/document the permanent rule that future added interiors receive the same effective probability unless explicitly overridden;
4. preserve all accepted S1.42Z gameplay/config/runtime invariants;
5. keep unrelated deferred changes out of the same build unless the user explicitly asks to combine them;
6. perform archive-delta and Patch Safety Review requirements before build promotion;
7. runtime-test the resulting candidate before acceptance.

No successor is armed yet.

## Verified restore invariants — do not reopen without evidence

- S1.42C-derived `LethalLevelLoader.cfg` moon power/spawn baseline;
- `Consistent Spawn Times = true`;
- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Baboon Hawk -> Pikmin block with native inherited lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- normal enemy population.

Never repeat the S1.42R whole-component disable approach.

## Monitor-only issues

Do not patch without stronger reproducibility or user-facing impact:

- S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- S1.42T one-off AloeChase FSB load-state message;
- S1.42W `InvalidOperationException: Collection was modified` in `PikminManager.DespawnLumiknulls()` during teardown/despawn;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

## Later deferred scopes

Keep separate unless explicitly grouped by the user:

- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Functional Microwave spawn rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Known non-functional drift

Older chronology wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` are not authoritative for current behavior. Actual code/config/runtime evidence and chronologically newer canonical documents override them. Keep cosmetic cleanup separate from gameplay/runtime work.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_ACCEPTANCE`;
- base = accepted S1.42Z;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- no build work armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

`RuntimeInbox/Current/` contains only `.gitkeep` after the successful runtime ingestion.

## Mandatory one-line runtime upload

Whenever a future new runtime profile is designated, ChatGPT must supply one self-contained PowerShell command with that exact profile name that uploads its `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
