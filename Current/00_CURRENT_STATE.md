# 00 — Current State

**Updated:** 2026-09-04 — S1.42Z accepted; S1.42AA runtime FAIL; S1.42AB built and awaiting runtime validation  
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

S1.42Z remains the rollback baseline until S1.42AB passes fresh runtime validation.

## Rejected candidate — S1.42AA

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

S1.42AA changed `Inject Dynamic Matching Weights = true -> false`, but fresh Offense runtime evidence proved the effective pool remained unequal: examples included LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25`, and `20`-weight interiors.

Root cause: LethalLevelLoader's matching architecture keeps the highest matching rarity. Generic project matches such as `Vanilla:100,Custom:100` therefore cannot lower a stronger author/planet/mod match such as `300` to `100`.

Black Mesa did successfully generate during the AA run. The same log contains repeated LethalMin evidence of unreachable interior entrance nodes and `Unpathable` ToShip routing that plausibly corresponds to the user-observed Pikmin stuck while carrying scrap from a table. Treat this as a separate Black Mesa/map/NavMesh/LethalMin routing compatibility finding; it is not part of the interior-weight fix.

The AA log also contained `Work state with no task assigned!` twice in a separate Pikmin lifecycle sequence. Leader-null remained `0` and Fatal remained `0`. Do not conflate those two Work/no-task warnings with the table/NavMesh incident without stronger correlation.

## Active runtime candidate — S1.42AB

**S1.42AB — Post-Viability Interior Weight Normalization**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Status: **BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

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
- mod state/add/remove changes `0`;
- config changes `0`.

The generated AB snapshot explicitly retains:

`Inject Dynamic Matching Weights = true`

Therefore AA's failed `false` experiment is not inherited.

## S1.42AB architecture

Exact target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

S1.42AB applies a Harmony Postfix only. LethalLevelLoader runs its complete native viability/matching/exclusion logic first. The project-local Postfix then receives the already-returned viable list and normalizes only positive `rarity` values to exactly `100`.

Rules:

- not returned by LLL -> remains excluded/unavailable;
- returned with positive rarity -> becomes `100`;
- no flow is appended, removed, re-registered or deduplicated;
- no LLL matching/config lists are rewritten;
- no Enemy/Scrap/MapObject rarity system is touched.

This is also the permanent future-interior equal-weight architecture: a newly installed interior automatically receives effective rarity `100` whenever LLL considers it viable. Hard technical exclusions remain upstream-owned.

Shatteredrooms' Experimentation/Embrion restriction remains a compatibility guard until dedicated evidence proves it safe to remove.

## Runtime-log interpretation — important

LLL writes its built-in `Viable ExtendedDungeonFlows` report inside the original method before the S1.42AB Postfix returns. That line can therefore still show pre-normalization values such as `300`, `275`, `75`, etc.

The authoritative AB evidence is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry in that final pool must be `(100)`.

## Exact next action

**Import and runtime-test S1.42AB on Offense. Do not build a successor first.**

Canonical Gale replacement launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

Complete Gale's **Advanced options -> Import all files** step when prompted.

Then run one normal Offense round, enter the generated interior and play normally. One successful run is sufficient if the final-pool marker is present. Do not farm every interior manually.

After the run use the exact build-specific uploader in:

`Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`

Minimum gate:

1. S1.42AB plugin loads and validates exact LLL `1.7.12`;
2. exact target-contract validation and armed marker succeed;
3. dungeon generation succeeds;
4. final effective viable pool marker appears;
5. all positive final pool entries are `100`;
6. no excluded flow is inserted;
7. accepted S1.42Z enemies/Pikmin/BCMER/Jetpack/CodeRebirth behavior remains healthy;
8. Leader-null `0`;
9. Fatal `0`;
10. Work/no-task preferably `0`; if reproduced, investigate separately.

## Accepted S1.42Z tuning preserved

- Jetpack base acceleration `10 -> 18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- CodeRebirth ACU exact 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`;
- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- narrow Hawk -> Pikmin prevention with native inherited lifecycle preserved;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Never repeat the S1.42R whole-component disable approach.

## Deferred — not part of S1.42AB

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

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- guarded base SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

Known non-functional historical drift in `Current/02_TECHNICAL_BASELINE.md` and old comments in `Patches/S139CompatibilityFixes/Plugin.cs` remains lower-authority than this current state, actual code/config and fresh runtime evidence.
