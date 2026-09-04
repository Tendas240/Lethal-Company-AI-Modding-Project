# 04 — Open Issues and Next Tests

## Accepted rollback baseline — S1.42Z

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`

S1.42Z remains the accepted rollback baseline while S1.42AB is under runtime validation.

## Rejected gate — S1.42AA

**RUNTIME FAIL / NOT ACCEPTED**

Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

The S1.42AA config-only experiment `Inject Dynamic Matching Weights = false` failed to equalize effective LethalLevelLoader dungeon weights. On Offense, the viable list still contained values from `20` through `300`, including LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25` and DeepcoreMines `25`.

Root cause: LLL preserves the highest matching rarity, so generic `Vanilla:100,Custom:100` values cannot lower a stronger author/planet/mod match.

Black Mesa generated successfully in this run. A separate Pikmin-carrying incident produced repeated LethalMin `Unpathable` / unreachable entrance routing evidence and is tracked as a likely Black Mesa/NavMesh/entrance-routing compatibility issue. Do not mix a global Pikmin recovery patch into the interior-weight work.

## Active gate — S1.42AB Post-Viability Interior Weight Normalization

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Successful build run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`

Candidate record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AB_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AB_PLAN.md`

Injected DLL:

`BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll`

DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

Archive delta vs S1.42Z:

- changed existing: exactly `export.r2x`;
- added: exactly the S1.42AB DLL;
- removed: `0`;
- config changes: `0`;
- mod state/add/remove changes: `0`.

The generated snapshot retains `Inject Dynamic Matching Weights = true`; S1.42AA's failed config experiment is not inherited.

## S1.42AB runtime contract

LLL performs its normal viability and exclusion logic first. A Harmony Postfix on

`DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

then normalizes only positive rarities in the already-returned viable list to `100`.

The patch does **not** append, remove, re-register or deduplicate dungeon flows. Technical exclusions remain owned by LLL/upstream matching. Enemy, Scrap and MapObject rarities are untouched.

Permanent rule: every future interior automatically receives effective rarity `100` whenever LLL considers it viable. Do not remove hard compatibility exclusions merely to make a flow eligible everywhere.

## Important log interpretation

LLL's built-in `Viable ExtendedDungeonFlows` report is emitted before the Postfix returns and can still show the old pre-normalization values.

The authoritative S1.42AB evidence is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry in this line must be `(100)`.

## Exact next test

**Import S1.42AB, then do one normal Offense run. Do not build a successor first.**

Canonical Gale replacement launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

Complete **Advanced options -> Import all files** in Gale when prompted.

Minimum runtime gate:

1. startup/main menu/lobby succeeds;
2. S1.42AB plugin loads;
3. exact LLL `1.7.12` and target-contract validation succeeds;
4. armed marker appears without refusal;
5. route/land on Offense and enter the generated interior;
6. `[InteriorWeightNormalization] Final effective viable pool ...` appears;
7. every positive listed rarity is `100`;
8. no excluded flow is inserted;
9. Facility/Mineshaft/other expected vanilla interiors remain viable;
10. no dungeon-generation failure;
11. accepted S1.42Z enemy/Pikmin/BCMER/Jetpack/CodeRebirth behavior remains healthy;
12. Leader-null `0`;
13. Fatal `0`;
14. Work/no-task preferably `0`; if reproduced, correlate separately;
15. upload the complete fresh `LogOutput.log` with the exact S1.42AB uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`.

One successful Offense run is sufficient if it provides the marker and full log. Do not manually farm every interior.

## Verified invariants — preserve

- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- BaboonBirdPikminEnemy enabled;
- narrow Hawk -> Pikmin block with native inherited lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- Jetpack `18f`, Jet Fuel `18/18`, Thrusters `25/20`;
- Indoor Pikmin `0.09`, CarryStrength `3 / 30`;
- ACU + G.R.E.G. exact 18-curve providers ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `40 / 2`.

Never repeat the S1.42R whole-component disable approach.

## Deferred after S1.42AB

- Black Mesa table/NavMesh/Pikmin route recovery;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by the S1.42AB profile SHA-256. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`
