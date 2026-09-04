# 00 — Current State

**Updated:** 2026-09-04 — S1.42AB accepted after fresh Offense runtime validation  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Build run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`  
Injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

## Runtime acceptance summary

Fresh Offense runtime proved:

- S1.42AB plugin loaded;
- exact LethalLevelLoader `1.7.12` validated;
- exact post-viability target contract validated;
- patch armed without refusal;
- LLL pre-Postfix viable pool = 40 entries with rarity range `20..300`;
- authoritative final effective viable pool = the same 40 entries, all at exactly `100`;
- `12 / 40` entries were normalized;
- no flow membership was added or removed;
- Black Mesa remained single-registered at final rarity `100`;
- normal dungeon generation succeeded and `Expanded facility` was selected;
- user entered the generated interior, played normally until death and reported no problematic behavior;
- Work/no-task = `0`;
- Leader-null = `0`;
- Compatibility Fixes Error marker = `0`;
- unspawned NetworkObjectReference marker = `0`;
- PikminNoticeZone regression marker = `0`;
- Fatal = `0`.

The complete AB log contains 32 Error-severity events, matching accepted S1.42Z. Known loaforcsSoundAPI/HarmonyX and SoftMask/SoftMasking exception classes remain monitor-only and are not AB project-local regressions.

## Accepted interior architecture

Exact target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

LLL performs native matching, viability and exclusions first. The project-local Harmony Postfix only normalizes positive rarity values in the already-returned viable list to exactly `100`.

Permanent accepted rule:

- not returned by LLL -> remains unavailable;
- returned with positive rarity -> effective rarity becomes `100`;
- no flow is appended, removed, re-registered or deduplicated;
- no matching/config list is rewritten;
- Enemy, Scrap and MapObject rarity systems are untouched;
- future interiors inherit effective rarity `100` whenever LLL considers them viable.

Preserve the Shatteredrooms Experimentation/Embrion restriction until dedicated evidence proves removal safe.

LLL's built-in `Viable ExtendedDungeonFlows` line is logged before the Postfix and can still show unequal values. The authoritative accepted marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## Previous / rejected states

### Previous accepted baseline

**S1.42Z — Jetpack Pikmin Retune** remains the previous accepted rollback/provenance artifact.

SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`  
Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Its accepted tuning is inherited by S1.42AB.

### Rejected candidate

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

The config-only `Inject Dynamic Matching Weights = false` approach failed because LLL retains the highest matching rarity. Do not revive it.

Separate AA findings remain deferred/monitor-only: Black Mesa table/NavMesh/Pikmin ToShip routing and the two-warning White-Pikmin Work/no-task lifecycle case. Work/no-task did not reproduce in AB.

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
- narrow Hawk -> Pikmin prevention only with inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- accepted S1.42AB interior normalization architecture.

Never repeat S1.42R's whole-component disable approach.

## Current Gale / tooling state

S1.42AB remains installed and current in Gale.

`RuntimeTools/ReplaceActiveGaleProfile.ps1` is fully end-to-end user-validated under Windows PowerShell 5.1. See `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md` and `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`.

Validated revision: `2026-09-04-import-uia-v2.1-download-hotfix`  
Helper blob SHA: `9458f427b538615249714e7f064f3107d6dcd36c`  
Validated commit: `f711f53f4971f97200ed3605479ef887a14b243d`

## Exact next state

**No successor is armed.**

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AB_ACCEPTANCE`;
- guarded base = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- guarded SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

The next isolated scope requires explicit selection. BCMER EventTypes equal distribution (`8 × 12.5%`) is now eligible to be selected next because AB is accepted, but it is not implicitly authorized or armed.

## Deferred / monitor-only

- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup;
- historical monitor-only exception classes already documented elsewhere.

Known non-functional historical drift in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` remains lower-authority than this file, actual code/config and fresh runtime evidence.
