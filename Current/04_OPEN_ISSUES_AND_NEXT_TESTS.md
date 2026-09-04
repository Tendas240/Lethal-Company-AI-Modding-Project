# 04 — Open Issues and Next Tests

## Closed accepted gate — S1.42Z

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains the accepted rollback baseline while S1.42AA is under runtime validation.

## Active gate — S1.42AA Interior Weight Equalization

**BUILD PASS / PROFILE IMPORT CONFIRMED / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Build run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

Candidate record: `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AA_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AA_PLAN.md`

The user has already imported S1.42AA through Gale using **Advanced options -> Import all files**. The gameplay/runtime gate is still open and no S1.42AA log has been submitted yet.

## Root cause proven before build

S1.42Z already had `Vanilla:100,Custom:100` configured for the project-normalized LethalLevelLoader dungeon tag weights. The remaining runtime inequality came from:

`Inject Dynamic Matching Weights = true`

which tells LethalLevelLoader to inject mod-author Level/Dungeon MatchingProperties on each landing.

On accepted S1.42Z Offense runtime evidence, the effective viable pool therefore still included unequal weights such as LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25`, and `20`-weight interiors.

## Exact S1.42AA change

Only one functional value changed:

`Inject Dynamic Matching Weights = true -> false`

The only other changed archive member is `export.r2x` for the Gale profile name.

Automated archive verification:

- ZIP members `333`;
- changed existing members exactly `2`;
- added `0`;
- removed `0`;
- mod state changes `0`;
- mod additions `0`;
- mod removals `0`;
- no project-local DLL changed.

Generated snapshot confirms `Inject Dynamic Matching Weights = false`. Build assertions preserve `Vanilla:100,Custom:100`, Black Mesa's dedicated native-owner `lethal_company:vanilla=+100,lethal_company:custom=+100`, and Indoor Pikmin Spawn Chance `0.09`.

## Exact next test

**Run S1.42AA on Offense. Do not build a successor first.**

Because S1.42AA is already imported, do not require a new replacement/import before this test unless the user explicitly wants to reinstall it.

Minimum gate:

1. startup/main menu/lobby succeeds;
2. route and land on Offense;
3. enter the generated interior and play a normal run;
4. fresh log contains `Viable ExtendedDungeonFlows` and eligible interiors use the common effective weight `100` rather than S1.42Z's unequal author values;
5. compare formerly unequal examples when present: LiminalHouse, Sub Systems, Abandoned Foundry, Shatteredrooms, Lead Factory, Spelunkers Caverns (Random), Crimson Keep, Gray Apartments, DeepcoreMines;
6. vanilla interiors such as Facility/Mineshaft remain viable where appropriate;
7. no duplicate Black Mesa/native-owner registration is introduced;
8. no dungeon-generation or seed failure;
9. normal enemies, Pikmin, BCMER and accepted S1.42Z Compatibility behavior remain healthy;
10. Work/no-task = `0`;
11. Leader-null = `0`;
12. Fatal = `0`;
13. no new project-local exception class;
14. preserve Shatteredrooms' Experimentation/Embrion technical restriction unless dedicated evidence proves removal safe;
15. upload the complete fresh `LogOutput.log` using the exact one-line uploader in `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`.

One successful normal Offense run is the intended minimum. Do not manually farm all interiors just to measure their weights; the complete log is the primary pool evidence.

## Permanent interior rule

Every eligible installed interior should have equal effective selection weight on vanilla and custom moons. Whenever new interiors are added later, their generated registration/config must be inspected and normalized into the same architecture before acceptance unless an explicit technical incompatibility requires a documented exception.

Do not blindly remove hard compatibility restrictions merely to make an interior eligible everywhere.

## Verified restore invariants — do not reopen without evidence

- accepted S1.42Z full-normal-stack state;
- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin block with native inherited lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- Jetpack `18f`, Jet Fuel `18/18`, Thrusters `25/20`;
- Indoor Pikmin `0.09`, CarryStrength `3 / 30`;
- ACU + G.R.E.G. exact 18-curve providers ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `40 / 2`.

Never repeat the S1.42R whole-component disable approach.

## Gale profile replacement workflow — canonical

Implementation: `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
Workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Binding automation/chat policy: `Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Canonical one-line launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The final y/n version was user-validated under Windows PowerShell 5.1 with a disposable `testpowershell` profile. It is now the permanent profile-replacement workflow. Every future ready-to-test build response must include this launcher and the exact build-specific runtime-log uploader together.

Do not reuse failed experimental helper patterns: case-sensitive `LOESCHEN`, fuzzy profile matching, Windows PowerShell 5.1 array assumptions, or a normal `$matches` variable that collides with automatic `$Matches`.

## Monitor-only issues

Do not patch without stronger reproducibility or user-facing impact:

- S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- S1.42T one-off AloeChase FSB load-state message;
- S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

## Deferred after S1.42AA

Keep separate unless explicitly grouped by the user:

- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42AA candidate;
- base SHA-256 = `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`;
- no successor build work armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

`RuntimeInbox/Current/` contains only `.gitkeep`.

## Handover references

Latest handover: `Current/94_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AA_RUNTIME_NEXT.md`  
Latest audit: `Current/95_REPOSITORY_HANDOVER_AUDIT_S1.42AA.md`  
Recent work: `Current/06_RECENT_WORK_S1.42AA.md`
