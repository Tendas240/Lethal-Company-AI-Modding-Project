# 94 — Final Handover — S1.42Z Accepted / S1.42AA Runtime Next

**Date:** 2026-09-04  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Canonical state

### Accepted rollback baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
Gale profile name: `LC V1 S1.42Z Jetpack Pikmin Retune`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine status: `Current/Projektstatus_S1.42Z_ACCEPTED.json`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z runtime coverage: 1,586,159 bytes, 16,094 lines, 15,325 parsed events, 32 Error-severity events, Fatal `0`.

Confirmed acceptance facts include:

- S1.42Z Jetpack Acceleration plugin loaded;
- ButteRyBalance 0.7.0, JetpackFixes 1.6.3 and More Ship Upgrades 3.14.1 validated;
- exact Jetpack path armed `10 -> 18`;
- S1.42Z CodeRebirth aerial-defense tuning plugin loaded;
- CodeRebirth 1.6.9, DawnLib 0.9.25 and Dusk 0.9.25 validated;
- Air Control Unit provider: exactly 18 curves validated;
- G.R.E.G. / Advanced Airspace Control provider: exactly 18 curves validated;
- both complete provider sets transactionally scaled ×`0.5`;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference marker `0`;
- PikminNoticeZone regression marker `0`;
- project-local Error-severity output `0`;
- Fatal `0`;
- user reported the behavior as fully satisfactory.

### Active runtime candidate

**S1.42AA — Interior Weight Equalization — BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Build workflow run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

Candidate record: `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AA_CANDIDATE.json`  
Plan: `BuildSpecs/S1.42AA_PLAN.md`  
Readable snapshot: `ProfileSources/S1.42AA/`

## Why S1.42AA exists

S1.42Z already had the project-normalized LethalLevelLoader dungeon tag weights:

`Vanilla:100,Custom:100`

But LethalLevelLoader also had:

`Inject Dynamic Matching Weights = true`

That option re-injected mod-author Level/Dungeon MatchingProperties on each landing. S1.42Z Offense runtime evidence therefore still showed unequal effective viable-dungeon weights, including LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25`, and multiple `20` values.

S1.42AA makes the narrow owner-level change:

`Inject Dynamic Matching Weights = false`

Automated archive delta vs S1.42Z:

- ZIP members: `333`;
- changed existing members: exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- added members: `0`;
- removed members: `0`;
- mod state/add/remove changes: `0`;
- no project-local DLL changed.

Black Mesa remains on its dedicated native-owner path with `lethal_company:vanilla=+100,lethal_company:custom=+100`. Do not create a duplicate LLL owner path.

Shatteredrooms' Experimentation/Embrion restriction remains a compatibility guard until dedicated evidence proves removal safe.

Permanent rule: every eligible installed interior should have the same effective selection weight on vanilla and custom moons. Future interiors must be normalized into the same architecture before acceptance unless a documented technical incompatibility requires an exception.

## Accepted S1.42Z tuning that S1.42AA must preserve

- Jetpack base acceleration `18f` (`10 -> 18`);
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- ACU exact 18 curves ×`0.5`;
- G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`;
- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Project-local DLL SHA-256 values:

- Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`;
- Compatibility Fixes: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`.

Never repeat the S1.42R whole-component disable approach for BaboonBirdPikminEnemy.

## Gale profile-replacement workflow

The previously experimental profile replacement helper is now **user-validated, canonical and binding**.

Implementation: `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
Workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Historical validation record: `Current/92_GALE_ACTIVE_PROFILE_REPLACEMENT_HELPER_CANDIDATE.md`

Canonical launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The helper closes Gale, requires `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`, resolves the exact `output_profile`, downloads before deletion, verifies SHA-256, lists local profiles numerically, asks `y/n`, deletes only the selected profile after `y`, opens the verified `.r2z`, leaves `Advanced options -> Import all files` manual, and removes the temporary download only after successful import confirmation.

The final version was validated under Windows PowerShell 5.1 with a disposable `testpowershell` profile. Earlier variants failed due to case-sensitive `LOESCHEN`, PowerShell 5.1 array handling, and a `$matches` / automatic `$Matches` collision; do not reintroduce those patterns.

For every future ready-to-test build, ChatGPT must provide both the replacement launcher above and the exact build-specific runtime-log uploader in the same response.

## Local state confirmed by user before handover

The user successfully imported **S1.42AA** with Gale using **Advanced options -> Import all files**. The profile-replacement helper was also validated successfully with the disposable profile.

Therefore the immediate next action is not another build and does not require another profile replacement unless the user intentionally wants to reinstall it.

## Exact next action

**Runtime-test S1.42AA on Offense. Do not build a successor first.**

One normal Offense gameplay run is the intended minimum if generation succeeds:

1. start/main menu/lobby succeeds;
2. route to Offense and land;
3. enter the generated interior and play normally;
4. after the run, upload the complete fresh `LogOutput.log` using the exact S1.42AA one-line uploader in `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`;
5. analyze the full log before deciding any successor.

Primary acceptance proof from the log:

- eligible `Viable ExtendedDungeonFlows` use common effective weight `100` rather than S1.42Z's unequal author values;
- formerly unequal examples should be compared when present;
- vanilla Facility/Mineshaft remain viable where appropriate;
- no duplicate Black Mesa/native-owner registration;
- no dungeon-generation/seed failure;
- normal enemies, Pikmin and BCMER remain healthy;
- Work/no-task `0`;
- Leader-null `0`;
- Fatal `0`;
- no new project-local exception class.

Current controllers:

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`;
- `BuildSpecs/current.json.enabled = false`;
- `BuildSpecs/current.json.build_id = IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = S1.42AA;
- no successor armed;
- `RuntimeInbox/Current/` currently contains only `.gitkeep`, so no S1.42AA runtime log has been submitted yet.

## Deferred after the S1.42AA gate

Do not mix into the current runtime gate unless the user explicitly changes scope:

- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Monitor-only observations

Do not patch without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

## Known non-functional documentation drift

`Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local-current wording, and `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior.

These are documentation/comment drift only. Chronologically newer canonical documents, actual code/config and runtime evidence are authoritative. Keep cosmetic cleanup separate from the open S1.42AA runtime gate.
