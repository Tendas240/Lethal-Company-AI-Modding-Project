# 00 — Current State

**Updated:** 2026-09-04 — S1.42Z accepted; S1.42AA runtime FAIL; S1.42AB imported and gameplay runtime next  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Canonical accepted baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine status: `Current/Projektstatus_S1.42Z_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains the rollback baseline until S1.42AB passes fresh gameplay runtime validation.

Accepted S1.42Z runtime facts include Jetpack `10 -> 18`, both CodeRebirth aerial-defense providers at exactly 18 curves ×`0.5`, Work/no-task `0`, Leader-null `0`, relevant NetworkObjectReference/PikminNoticeZone regression markers `0`, Compatibility Fixes Error `0`, project-local Error severity `0`, Fatal `0`, and user acceptance of the resulting behavior.

## Rejected candidate — S1.42AA

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Build run: `33884101262`  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

AA changed `Inject Dynamic Matching Weights = true -> false`, but the fresh Offense log proved that effective dungeon weights remained unequal. Examples included LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25` and several `20`-weight interiors.

Root cause: LethalLevelLoader keeps the highest matching rarity across its matching sources, so generic `Vanilla:100,Custom:100` values cannot lower a stronger author/planet/mod match such as `300` to `100`.

Black Mesa generated successfully in the AA run. A separate user-observed Pikmin carrying scrap from a Black Mesa table became stuck; the log repeatedly showed unreachable entrance nodes, `Unpathable` routing and failed ToShip routing. Treat this as a Black Mesa/map/NavMesh/LethalMin compatibility finding, not as the interior-weight defect. The same AA log also contained `Work state with no task assigned!` twice in a separate White-Pikmin lifecycle sequence; Leader-null remained `0` and Fatal remained `0`. Monitor both findings separately unless they reproduce more strongly.

## Active runtime candidate — S1.42AB

**S1.42AB — Interior Weight Normalization**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
Profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Status: **BUILD PASS / LOCAL IMPORT PASS / GAMEPLAY RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Successful workflow run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`

Candidate record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AB_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AB_PLAN.md`  
Patch source: `Patches/S142ABInteriorWeightNormalization/`  
Readable snapshot: `ProfileSources/S1.42AB/`

Injected DLL:
`BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll`

DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

Automated archive delta vs accepted S1.42Z:

- ZIP members `334`;
- changed existing member exactly `export.r2x`;
- added member exactly the S1.42AB DLL;
- removed `0`;
- config changes `0`;
- mod state/add/remove changes `0`.

The AB snapshot retains `Inject Dynamic Matching Weights = true`, so AA's failed `false` experiment is not inherited.

## S1.42AB architecture

Exact target:
`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

S1.42AB applies a Harmony Postfix only. LethalLevelLoader runs its complete native viability/matching/exclusion logic first. The project-local Postfix then receives the already-returned viable list and normalizes only positive `rarity` values to exactly `100`.

Contract:

- not returned by LLL -> remains excluded/unavailable;
- returned with positive rarity -> becomes `100`;
- no flow is appended, removed, re-registered or deduplicated;
- no LLL matching/config list is rewritten;
- Enemy, Scrap and MapObject rarity systems are untouched.

This is the intended permanent future-interior equal-weight architecture: newly installed interiors inherit effective rarity `100` whenever LLL itself considers them viable. Hard technical exclusions remain upstream-owned. Preserve the Shatteredrooms Experimentation/Embrion restriction until dedicated evidence proves removal safe.

## Local import state — PASS

S1.42AB is **already imported locally in Gale and is the current profile**. Do not ask the user to import it again before the immediate gameplay test.

The canonical replacement helper `RuntimeTools/ReplaceActiveGaleProfile.ps1` is now **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Validated helper revision:
`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob SHA:
`9458f427b538615249714e7f064f3107d6dcd36c`

Validated helper commit:
`f711f53f4971f97200ed3605479ef887a14b243d`

Validated AB import evidence:

- profile download SHA matched `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- archive `export.r2x` evidence SHA-256 = `331c01bfe5eda5d4ce9bc2a887fd322b302f32dccf9d95918d6c7d0c7fb6cf40`;
- old AA profile deleted only after explicit numeric selection + `y`;
- Gale Missing Profiles `Delete -> Submit` automatic;
- candidate `.r2z` opened exactly once;
- `Advanced options -> Import all files -> Import` automatic;
- exact target profile's local `export.r2x` matched the archive-entry SHA;
- temporary `.r2z` removed automatically;
- no manual Gale click or final PowerShell Enter after selection + `y`.

Historical helper failures are preserved in `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md` and `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`; do not reintroduce duplicate `.r2z` opens, binary Raw-GitHub cache-busting query strings, direct SQLite edits, screen-coordinate clicks, blind keyboard navigation, fuzzy matching or `$matches` variable collisions.

## Runtime-log interpretation — important

LLL writes its built-in `Viable ExtendedDungeonFlows` report inside the original method before the AB Postfix returns. That line can therefore still show pre-normalization values such as `300`, `275`, `75`, etc. This is not by itself an AB failure.

The authoritative AB evidence is:
`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry in that final pool must be `(100)`.

## Exact next action

**Gameplay-runtime-test the already-imported S1.42AB on Offense. Do not build S1.42AC or another successor first.**

Minimum intended test:

1. start S1.42AB normally and reach main menu/lobby;
2. route to Offense and land;
3. enter the generated interior;
4. play one normal run;
5. upload the complete fresh `LogOutput.log` using the exact S1.42AB uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`;
6. analyze the full log before deciding any successor.

One successful Offense run is sufficient if the final-pool marker is present; do not manually farm every interior.

Minimum acceptance gate:

- S1.42AB plugin loads and validates exact LLL `1.7.12`;
- exact target contract validates and armed marker appears;
- dungeon generation succeeds;
- final effective viable pool marker appears;
- every positive final-pool entry is `100`;
- no excluded flow is inserted;
- normal S1.42Z enemies/Pikmin/BCMER/Jetpack/CodeRebirth behavior remains healthy;
- Black Mesa remains single-registered when present;
- Leader-null `0`;
- Fatal `0`;
- Work/no-task preferably `0`; if reproduced, correlate separately;
- no new project-local exception/error flood.

## Accepted tuning / compatibility invariants — preserve

- Jetpack base acceleration `18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- CodeRebirth ACU exact 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`;
- exact BCMER `1.71.0`; never silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only with native inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Never repeat S1.42R's whole-component disable approach.

## Deferred / monitor-only — not part of S1.42AB

- Black Mesa table/NavMesh/Pikmin route recovery;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup;
- historical S1.42S disconnect PikminNoticeZone/unspawned NetworkObjectReference exception;
- historical S1.42T AloeChase FSB message;
- historical S1.42W `DespawnLumiknulls()` collection-modified teardown exception;
- loaforcsSoundAPI/HarmonyX `TypeLoadException`;
- SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

Potential later roadmap item after AB closes: isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0` for V81. Do not add it to AB. Inspect the actual 2.5.0 package/config first; keep direct outside-spawn behavior disabled initially and be especially conservative around Baboon Hawk/LethalMin/Pikmin interactions and SmartEnemyPathfinding/FairAI/NavMesh behavior.

## Controllers

`BuildSpecs/current.json` is correctly disarmed:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- guarded base SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

Known non-functional historical drift in `Current/02_TECHNICAL_BASELINE.md` and old comments in `Patches/S139CompatibilityFixes/Plugin.cs` remains lower-authority than this current state, actual code/config and fresh runtime evidence.
