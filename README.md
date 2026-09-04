# Lethal Company AI Modding Project

GitHub is the canonical source of truth and build/handover workspace for this project.

Game: **Lethal Company V81**

Do not require a local repository clone or local profile build while the required base artifacts and GitHub-native infrastructure are present.

## Current canonical state

### Accepted full-normal-stack baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Canonical runtime acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine-readable accepted state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

S1.42AB was built directly from accepted S1.42Z and passed fresh Offense gameplay runtime validation.

Runtime proof:

- `S1.42AB Interior Weight Normalization 1.0.0` loaded;
- exact `imabatby.lethallevelloader v1.7.12` validated;
- exact post-viability dungeon-selection contract validated and armed;
- LLL's pre-Postfix Offense pool contained 40 viable entries with weights from `20` through `300`;
- the authoritative final effective pool contained the same 40 entries, all at exactly `100`;
- `12 / 40` weights were normalized;
- no flow membership was added or removed;
- Black Mesa remained single-registered and final rarity `100`;
- normal dungeon generation succeeded and `Expanded facility` was selected;
- user entered the generated interior, played normally until death, and reported no problematic behavior;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error marker `0`;
- unspawned NetworkObjectReference marker `0`;
- PikminNoticeZone regression marker `0`;
- Fatal `0`.

LLL's earlier built-in `Viable ExtendedDungeonFlows` line is pre-Postfix evidence only and may still show unequal values. The authoritative accepted marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry there is normalized to `(100)`.

### Previous accepted baseline

**S1.42Z — Jetpack Pikmin Retune — previous accepted rollback/provenance baseline**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`  
Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Its accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning is inherited by S1.42AB and remains part of the accepted stack.

### Rejected candidate

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

The config-only change `Inject Dynamic Matching Weights = false` did not equalize effective LethalLevelLoader dungeon rarities because LLL retains the highest matching rarity. Do not revive this approach.

Separate AA findings remain monitor/deferred evidence: Black Mesa table/NavMesh/Pikmin ToShip routing and two Work/no-task warnings in a separate White-Pikmin lifecycle sequence. Neither justified broad patching, and Work/no-task did not reproduce in the accepted AB run.

## Accepted interior architecture

S1.42AB patches `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` with a Harmony Postfix.

LLL owns native matching, viability and exclusions first. The project-local Postfix then normalizes only positive rarity values in the already-returned viable list to `100`.

Accepted permanent rule:

- not returned by LLL -> remains unavailable;
- returned with positive rarity -> effective rarity becomes `100`;
- no flow is appended, removed, re-registered or deduplicated;
- no LLL matching/config list is rewritten;
- Enemy, Scrap and MapObject rarity systems are untouched;
- future installed interiors automatically inherit effective rarity `100` whenever LLL itself considers them viable.

Preserve the Shatteredrooms Experimentation/Embrion compatibility restriction until dedicated evidence proves removal safe.

## Local Gale state

S1.42AB is already imported and remains the current Gale profile.

The canonical replacement helper `RuntimeTools/ReplaceActiveGaleProfile.ps1` is **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Validated revision: `2026-09-04-import-uia-v2.1-download-hotfix`  
Validated helper blob SHA: `9458f427b538615249714e7f064f3107d6dcd36c`  
Validated implementation commit: `f711f53f4971f97200ed3605479ef887a14b243d`

Permanent workflow: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Import automation history: `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
3. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`
8. `Current/100_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AB_RUNTIME_NEXT.md`
9. `Current/101_REPOSITORY_HANDOVER_AUDIT_S1.42AB.md`
10. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
11. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
12. `BuildSpecs/S1.42AB_PLAN.md`
13. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
14. `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`
15. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
16. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
17. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
18. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
19. `BuildSpecs/current.json`
20. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older version-specific wording. `Current/102` and `Current/Projektstatus_S1.42AB_ACCEPTED.json` are authoritative for the latest acceptance; `Current/100` and `Current/101` remain historical handover/audit evidence from immediately before the AB runtime gate closed.

## Exact next state

**No successor is armed. Do not build a new profile until the next isolated scope is explicitly selected.**

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AB_ACCEPTANCE`, guarded by S1.42AB SHA-256 `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

The BCMER EventTypes equal-distribution scope (`8 × 12.5%`) is now eligible to be chosen next because the AB gate is closed, but it is not armed or implicitly authorized.

## Permanent anti-regression state

Preserve:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`;
- Jetpack base acceleration `18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`, Purple `30`;
- CodeRebirth ACU and G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max Snails `2`;
- accepted S1.42AB post-viability interior normalization architecture.

Never repeat the S1.42R whole-component disable approach.

Project-local patch policy: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Deferred / monitor-only

Keep separate unless the user explicitly selects or groups scope:

- BCMER EventTypes fixed `8 × 12.5%`;
- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup.

Known non-functional historical drift remains intentionally in older chronology wording under `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs`; newer canonical documents, actual code/config and runtime evidence override them.
