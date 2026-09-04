# Final Handover — S1.42Z Accepted / S1.42AB Runtime Next

**Date:** 2026-09-04  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Game:** Lethal Company V81  
**Repository is the source of truth and canonical build/handover workspace.**

Do not require a local repository clone or local profile build while the repository contains the needed base artifacts and GitHub-native build infrastructure.

## Canonical state at handover

### Accepted rollback baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
Gale profile name: `LC V1 S1.42Z Jetpack Pikmin Retune`  
Profile SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine status: `Current/Projektstatus_S1.42Z_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

Confirmed accepted S1.42Z runtime facts:

- Jetpack project-local patch loaded and exact local-player base acceleration changed `10 -> 18`;
- CodeRebirth ACU provider exactly 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. provider exactly 18 curves ×`0.5`;
- Work/no-task `0`;
- Leader-null `0`;
- unspawned NetworkObjectReference marker `0`;
- PikminNoticeZone regression marker `0`;
- Compatibility Fixes Error marker `0`;
- project-local Error severity `0`;
- Fatal `0`;
- user accepted the resulting gameplay behavior as satisfactory.

S1.42Z remains the accepted rollback baseline until S1.42AB passes its own fresh gameplay runtime gate.

## Rejected candidate — S1.42AA

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Build run: `33884101262`  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

S1.42AA changed only:

`Inject Dynamic Matching Weights = true -> false`

Fresh Offense runtime evidence proved this did **not** equalize the actual LethalLevelLoader effective dungeon pool. Examples remained:

- LiminalHouse `300`;
- Sub Systems `275`;
- Abandoned Foundry `250`;
- Shatteredrooms `75`;
- Lead Factory `70`;
- Spelunkers Caverns (Random) `50`;
- Crimson Keep `35`;
- Gray Apartments `25`;
- DeepcoreMines `25`;
- several `20`-weight interiors.

Root cause established from LethalLevelLoader behavior: matching sources are combined by retaining the highest matching rarity, so a generic `Vanilla:100,Custom:100` match cannot lower a stronger author/planet/mod match such as `300` to `100`.

Black Mesa generated successfully during the AA run. A separate user-visible Pikmin incident occurred when scrap sat on a Black Mesa table: the thrown Pikmin became stuck running in place while trying to carry the scrap. The log showed repeated unreachable entrance-node checks, `Unpathable` ToShip routing and failed route creation. Treat this as a separate Black Mesa/map/NavMesh/LethalMin compatibility finding, not as the interior-weight failure. Do not introduce a broad global Pikmin recovery patch without stronger reproducibility and a narrow safe design.

The same AA log contained `Work state with no task assigned!` twice in a separate White-Pikmin lifecycle sequence after leader/task state changed. Leader-null remained `0` and Fatal remained `0`. Monitor this separately if it reproduces.

## Active runtime candidate — S1.42AB

**S1.42AB — Interior Weight Normalization**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
Profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Status: **BUILD PASS / LOCAL IMPORT PASS / GAMEPLAY RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Successful build workflow run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`

Candidate record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AB_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AB_PLAN.md`  
Patch source: `Patches/S142ABInteriorWeightNormalization/`  
Readable snapshot: `ProfileSources/S1.42AB/`

Injected DLL:

`BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll`

DLL SHA-256:

`901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

Automated archive delta vs accepted S1.42Z:

- ZIP members `334`;
- changed existing member exactly `export.r2x`;
- added member exactly the S1.42AB DLL;
- removed members `0`;
- config changes `0`;
- mod state changes/additions/removals `0`.

The generated AB snapshot explicitly retains:

`Inject Dynamic Matching Weights = true`

Therefore S1.42AA's failed `false` experiment is not inherited.

## S1.42AB architecture / safety contract

Exact target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

S1.42AB installs a Harmony Postfix only. LethalLevelLoader first performs its complete normal matching, viability and exclusion logic. The project-local Postfix then receives the already-returned viable list and normalizes only positive `rarity` values to exactly `100`.

Contract:

- flow not returned by LLL -> remains excluded/unavailable;
- flow returned with positive rarity -> becomes `100`;
- no flow is appended;
- no flow is removed;
- no flow is re-registered or deduplicated;
- no LLL matching/config list is rewritten;
- Enemy, Scrap and MapObject rarity systems are untouched.

The plugin fails closed unless exact LethalLevelLoader `1.7.12` and the expected target/return/field contract are present. Preserve the Shatteredrooms Experimentation/Embrion restriction until dedicated evidence proves it safe to remove.

Permanent interior rule implemented by this architecture: every newly installed interior should receive effective rarity `100` automatically whenever LLL itself considers that interior viable. Equal probability does not mean overriding hard technical exclusions.

## Important S1.42AB log interpretation

LethalLevelLoader writes its built-in `Viable ExtendedDungeonFlows` line inside the original method before the Postfix returns. That line can still show the old pre-normalization values such as `300`, `275`, `75`, etc. Do **not** reject AB merely because this earlier line remains unequal.

The authoritative project-local evidence is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry in that final effective pool must be `(100)`.

## Local Gale import state — already complete

S1.42AB is **already imported locally in Gale and is the current profile**. The next chat must not ask the user to reinstall/re-import AB before the immediate gameplay test.

The repository-backed replacement helper is now **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Implementation: `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
Contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Import automation history: `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`

Validated revision marker:

`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob SHA:

`9458f427b538615249714e7f064f3107d6dcd36c`

Validated implementation commit:

`f711f53f4971f97200ed3605479ef887a14b243d`

AB archive `export.r2x` evidence SHA-256:

`331c01bfe5eda5d4ce9bc2a887fd322b302f32dccf9d95918d6c7d0c7fb6cf40`

Validated happy path after old-profile number + explicit `y`:

1. candidate is downloaded before deletion;
2. candidate profile SHA-256 is verified;
3. archive `export.r2x` evidence SHA is computed;
4. only the selected old profile is deleted;
5. the verified candidate `.r2z` is opened exactly once;
6. Gale Missing Profiles is automatically resolved with `Delete -> Submit`;
7. the already-buffered target import dialog is used;
8. `Advanced options` is expanded automatically;
9. `Import all files` is enabled and verified automatically;
10. Import is invoked automatically;
11. exact local target-profile `export.r2x` is hash-verified against the archive entry;
12. temporary `.r2z` is removed only after evidence passes;
13. no additional Gale click or PowerShell Enter is required in the validated happy path.

Historical failed helper attempts are intentionally preserved. Do not reintroduce:

- direct edits to Gale `data.sqlite3`;
- screen-coordinate clicks;
- blind `Tab`/`Enter`/arrow navigation;
- duplicate `.r2z` open events;
- cache-busting query strings on the binary Raw-GitHub `.r2z` URL;
- fuzzy build/profile matching;
- a normal variable named `$matches` that collides case-insensitively with PowerShell's automatic `$Matches`;
- claims that changed automation is validated before it is actually tested on the project machine.

## Exact next action

**Gameplay-runtime-test the already-imported S1.42AB on Offense. Do not build S1.42AC or any successor first.**

Minimum intended test:

1. start the current S1.42AB profile normally and reach main menu/lobby;
2. route to Offense and land;
3. enter the generated interior;
4. play one normal round;
5. upload the complete fresh `LogOutput.log` with the exact S1.42AB uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`;
6. analyze the complete log before accepting AB or designing any successor.

One successful Offense run is sufficient if the final-pool marker is present. Do not manually farm every interior.

Minimum runtime gate:

- `S1.42AB Interior Weight Normalization 1.0.0` loads;
- exact LLL `1.7.12` validation succeeds;
- exact target-contract validation succeeds;
- armed marker appears without refusal;
- normal dungeon generation succeeds;
- final effective viable-pool marker appears;
- every positive final-pool entry is `100`;
- no excluded flow is inserted;
- expected vanilla/custom viable flows remain available;
- no duplicate Black Mesa registration;
- accepted S1.42Z enemies/Pikmin/BCMER/Jetpack/CodeRebirth behavior remains healthy;
- Leader-null `0`;
- Fatal `0`;
- Work/no-task preferably `0`; if reproduced, correlate separately;
- no new project-local exception/error flood.

`RuntimeInbox/Current/` currently contains only `.gitkeep`, so no S1.42AB gameplay log has been submitted yet.

## Controllers — verified at handover

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- guarded base SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor is armed.

`Current/AUTO_BUILD_RESULT.json` identifies S1.42AB with the same output SHA-256.

## Accepted tuning / compatibility invariants — preserve

- Jetpack base acceleration `18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- CodeRebirth ACU exactly 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. exactly 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max Snails `2`;
- exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`; never silently upgrade to 2.x;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- inherited PikminEnemy death/unlatch/task lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Never repeat the S1.42R strategy of disabling the complete `LethalMin.BaboonBirdPikminEnemy` component merely to block one interaction.

Every future project-local patch must comply with `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## Deferred / monitor-only — do not mix into S1.42AB

Deferred until the AB gate closes unless the user explicitly changes scope:

- Black Mesa table/NavMesh/Pikmin route recovery;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

Monitor-only without stronger evidence:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- loaforcsSoundAPI/HarmonyX `TypeLoadException`;
- SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

Potential later roadmap item after AB closes: isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0` for V81. Do not add it to AB. Inspect the actual 2.5.0 package/config first; initially avoid arbitrary direct-outside spawning and be especially conservative around Baboon Hawk/LethalMin/Pikmin lifecycle plus SmartEnemyPathfinding/FairAI/NavMesh behavior.

## Known intentional non-functional drift

Older chronology subsections in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` contain stale wording. This is non-functional documentation/comment drift only. Chronologically newer Current documents, actual code/config and fresh runtime evidence are authoritative. Cosmetic cleanup remains deferred.

## Mandatory future ready-to-test UX

For every future newly built runtime candidate, the response announcing it as ready to test must provide **both**:

1. the canonical Gale replacement launcher from `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`;
2. the exact build-specific self-contained runtime-log uploader.

The user must not need to ask again for either command.
