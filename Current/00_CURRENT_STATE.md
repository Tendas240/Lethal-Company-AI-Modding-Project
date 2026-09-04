# 00 — Current State

**Updated:** 2026-09-04 — S1.42Z accepted; S1.42AA imported and awaiting runtime validation  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

Latest handover records:

- `Current/94_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AA_RUNTIME_NEXT.md`
- `Current/95_REPOSITORY_HANDOVER_AUDIT_S1.42AA.md`
- `Current/06_RECENT_WORK_S1.42AA.md`

## Canonical accepted baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine status: `Current/Projektstatus_S1.42Z_ACCEPTED.json`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains the rollback baseline until S1.42AA passes fresh runtime validation.

Accepted runtime facts include Jetpack `10 -> 18`, ACU + G.R.E.G. exact 18-curve provider contracts ×`0.5`, Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0`, relevant NetworkObjectReference/PikminNoticeZone regression markers `0`, project-local Error-severity `0`, Fatal `0`, and user acceptance of the resulting behavior.

## Active runtime candidate

**S1.42AA — Interior Weight Equalization**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Status: **BUILD PASS / PROFILE IMPORT CONFIRMED / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build workflow run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

Candidate record: `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AA_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AA_PLAN.md`  
Readable snapshot: `ProfileSources/S1.42AA/`

The user successfully imported S1.42AA through Gale with **Advanced options -> Import all files** before this handover. No S1.42AA gameplay runtime test has been completed yet.

## S1.42AA root cause and exact change

S1.42Z already contained normalized project dungeon tag weights `Vanilla:100,Custom:100`, but LethalLevelLoader still had:

`Inject Dynamic Matching Weights = true`

That option re-injected mod-author Level/Dungeon MatchingProperties on every landing. S1.42Z Offense runtime evidence therefore still produced unequal effective values such as LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25`, and several `20` values.

S1.42AA changes only:

`Inject Dynamic Matching Weights = false`

Generated archive delta vs S1.42Z:

- ZIP members `333`;
- changed existing members exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- added `0`;
- removed `0`;
- mod state/add/remove changes `0`;
- no project-local DLL changed.

Black Mesa remains on its dedicated native-owner config path with `lethal_company:vanilla=+100,lethal_company:custom=+100`. Do not enable a duplicate LLL owner path.

Permanent interior rule: every eligible installed interior should have the same effective selection weight on vanilla and custom moons. Future added interiors must be normalized into the same architecture before acceptance unless an explicitly documented technical incompatibility requires an exception.

Shatteredrooms' Experimentation/Embrion restriction remains a compatibility guard pending dedicated proof that removing it is safe.

## Accepted S1.42Z tuning preserved by S1.42AA

- Jetpack base acceleration `10 -> 18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- CodeRebirth ACU exact 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`.

Project-local DLL SHA-256 values:

- Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`;
- Compatibility Fixes: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`.

## Exact next action

**Runtime-test S1.42AA on Offense. Do not build a successor first.**

The profile is already imported. A replacement/re-import is not required unless the user intentionally wants to reinstall it.

Do one normal Offense gameplay run, enter the generated interior and play normally. Then upload the complete fresh `LogOutput.log` using the exact S1.42AA one-line uploader in:

`Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`

The log must prove that eligible `Viable ExtendedDungeonFlows` use common effective weight `100` rather than the prior unequal author values. Also verify no dungeon-generation failure, no duplicate Black Mesa/native-owner regression, Work/no-task `0`, Leader-null `0`, Fatal `0`, and no new project-local exception class.

## Permanent compatibility state to preserve

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection preserved;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Never repeat the S1.42R whole-component disable approach.

Patch policy: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Gale profile replacement workflow — canonical and binding

Implementation: `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
Workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Binding automation/chat policy: `Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Canonical launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The validated flow matches `ACTIVE_BUILD` to `AUTO_BUILD_RESULT`, downloads before deletion, verifies SHA-256, lists profiles numerically, requires `y/n`, opens Gale, keeps **Advanced options -> Import all files** manual, and cleans the downloaded `.r2z` after confirmed import.

Every future ready-to-test build response must include both this launcher and the exact build-specific runtime-log uploader without the user having to ask again.

## Monitor-only observations

Do not patch without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

Known non-functional drift remains in older chronology/current wording under `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs`. Chronologically newer canonical docs, actual code/config and runtime evidence override that drift.

## Deferred — not mixed into S1.42AA

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`;
- base SHA-256 = `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`;
- no successor work armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

`RuntimeInbox/Current/` contains only `.gitkeep`; there is no S1.42AA runtime log yet.
