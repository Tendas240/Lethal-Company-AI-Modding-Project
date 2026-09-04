# 89 — Repository Handover Audit — S1.42Z

**Date:** 2026-09-04  
**Audit verdict:** PASS — repository is ready for a new ChatGPT handover  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Canonical state verified

Last fully accepted full-normal-stack baseline:

- build: **S1.42U**;
- profile: `Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`;
- SHA-256: `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`;
- acceptance: `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`.

Latest completed runtime evaluation:

- build: **S1.42Y**;
- profile SHA-256: `f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`;
- evidence: `RuntimeEvidence/S1.42Y/20260904T123817Z/`;
- raw log SHA-256: `dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`;
- verdict: technical paths PASS, Microwave/Carry tuning accepted, Jetpack/Indoor Pikmin retune requested, not promoted.

Active runtime candidate:

- build: **S1.42Z**;
- profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`;
- SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- status: BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED;
- GitHub Actions run: `33874737048` — success;
- automated build commit: `267543634bb884bb447bf4bec320103ba75c9ff8`.

## S1.42Z build integrity verified

`Current/AUTO_BUILD_RESULT.json` and `ProfileSources/S1.42Z/` establish:

- ZIP members = `333`;
- changed existing members vs S1.42U = `15`;
- added members = exactly two S1.42Z project-local DLLs;
- mod state changes = none;
- mod additions = none;
- mod removals = none;
- S1.42Z was built directly from S1.42U;
- historical V/W/X/Y tuning DLLs are absent from the Z snapshot.

Project-local DLL hashes:

- `BepInEx/plugins/S142ZJetpackAcceleration/S142ZJetpackAcceleration.dll` — SHA-256 `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- `BepInEx/plugins/S142ZCodeRebirthAerialDefenseSpawnTuning/S142ZCodeRebirthAerialDefenseSpawnTuning.dll` — SHA-256 `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

Verified current tuning:

- Jetpack base acceleration `18f`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- ACU exact 18 curves ×0.5;
- G.R.E.G. exact 18 curves ×0.5;
- Functional Microwave volume `0.15`, user accepted;
- Immortal Snail Rarity `40`, Max `2`.

## Runtime controller state verified

`RuntimeInbox/ACTIVE_BUILD.txt` contains exactly:

`S1.42Z`

`RuntimeInbox/Current/` contains only `.gitkeep`, so no un-ingested runtime log is waiting under the normal inbox path.

## Build controller state verified

`BuildSpecs/current.json` is safely disarmed:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base profile = `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`;
- guarded base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no config patches, local plugin builds or text assertions are armed.

No successor build is active.

## Canonical documentation updated

The following canonical entry points were synchronized to the S1.42Z handover state:

- `START_HERE_ChatGPT_Masterprompt.txt`;
- `README.md`;
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`;
- `Current/Projektstatus_S1.42Z_CANDIDATE.json`.

`BuildSpecs/S1.42Z_PLAN.md` is finalized as:

`FROZEN / BUILD PASS / RUNTIME VALIDATION OPEN`

and records the final profile hash, Actions run, automated build commit and DLL hashes.

New handover file:

`Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`

The `START_HERE_ChatGPT_Masterprompt.txt` bootstrap block now points to U accepted / Y technical PASS / Z built. Its durable generic `MASTER-PROMPT - Lethal Company Modding Project` section was preserved.

## Permanent invariants retained

The handover explicitly preserves:

- exact BCMER 1.71.0; no silent 2.x upgrade;
- EnemyIsolation disabled;
- Compatibility Fixes 1.3.14 / SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- S1.42C-derived moon power/spawn restore baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

The S1.42R whole-component disable approach remains explicitly prohibited.

Project-local patch policy remains binding:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Runtime/error history retained

No runtime evidence or unique diagnostic history was deleted.

Important retained evidence includes:

- S1.42U full-normal-stack acceptance;
- S1.42Y raw/processed runtime evidence and its complete 32-Error classification;
- S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference history;
- S1.42T AloeChase FSB one-off history;
- S1.42W `PikminManager.DespawnLumiknulls()` teardown collection-modified history;
- Baboon/Pikmin lifecycle root-cause and acceptance history;
- previous tuning candidates V/W/X/Y and their profile/snapshot evidence.

The known non-Y setup/mod Error classes remain monitor-only unless they become reproducible and user-facing.

## Known non-functional drift retained deliberately

Two known cleanup items remain intentionally unresolved because they are non-functional and should not be mixed into the active runtime gate:

- older chronology subsections in `Current/02_TECHNICAL_BASELINE.md` contain stale local `current` wording;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` do not perfectly describe accepted v1.3.14 behavior.

Chronologically newer current docs, actual code/config and runtime evidence are authoritative.

## Cleanup classification

### KEEP

- all accepted/runtime evidence under `RuntimeEvidence/` with continuing diagnostic value;
- historical V/W/X/Y tuning records and snapshots;
- S1.42U accepted rollback profile and acceptance documents;
- S1.42C restore baseline and enemy-spawn baseline;
- failed/obsolete approach history;
- project-local patch safety policy;
- large runtime log retention policy;
- historical handovers and root-cause files with unique evidence.

### UPDATE

- `START_HERE_ChatGPT_Masterprompt.txt`;
- `README.md`;
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`;
- `Current/Projektstatus_S1.42Z_CANDIDATE.json`.

### ADD

- `Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`;
- `Current/89_REPOSITORY_HANDOVER_AUDIT_S1.42Z.md`.

### ARCHIVE

No additional archive move was necessary. Existing historical files already retain their diagnostic context in place.

### DELETE

**None.** No file or evidence was sufficiently certain to be permanently valueless. No runtime evidence was deleted.

## Deferred work preserved

Do not mix into the active S1.42Z gate:

- equal effective probability for all installed interiors;
- permanent future-interior equal-probability rule;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Exact next step

**Runtime-test S1.42Z before building anything else.**

Import/run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Use Gale:

**Advanced options -> Import all files**

unless the concrete import flow independently guarantees retention of all custom files.

Then verify the Z plugin load/validation markers, Jetpack 18f behavior, Indoor Pikmin 0.09 density, accepted CarryStrength/Microwave state, normal enemy/BCMER/Compatibility health, and upload one complete fresh `LogOutput.log` with the exact self-contained PowerShell command in `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`.

## Manual local work required at handover

None now. No local repository clone, local build or manual repo maintenance is required.

The next unavoidable local action is only the actual S1.42Z gameplay test and subsequent runtime-log upload.