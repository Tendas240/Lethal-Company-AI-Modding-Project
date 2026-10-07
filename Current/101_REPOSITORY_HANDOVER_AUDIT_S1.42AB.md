# Repository Handover Audit — S1.42AB

**Date:** 2026-09-04  
**Verdict:** **PASS WITH INTENTIONAL HISTORICAL DRIFT PRESERVED**

This audit verifies the repository handover state after S1.42AA runtime rejection, S1.42AB build creation, and successful end-to-end validation of the automated Gale replacement workflow.

## Canonical project state

- Accepted rollback baseline: **S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**.
- Rejected candidate: **S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**.
- Active runtime candidate: **S1.42AB — Interior Weight Normalization — BUILD PASS / LOCAL IMPORT PASS / GAMEPLAY RUNTIME OPEN / NOT ACCEPTED**.
- Exact next step: one normal Offense gameplay run with the already-imported S1.42AB, then upload the complete fresh `LogOutput.log` and analyze it before any successor is built.

## Identity / hashes — consistent

### S1.42Z accepted

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`  
Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

### S1.42AA rejected

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

Runtime proved the config-only attempt did not equalize effective LethalLevelLoader weights.

### S1.42AB active

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Successful build run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`  
Injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

`Current/AUTO_BUILD_RESULT.json` identifies S1.42AB and the same output SHA-256.

## S1.42AB archive-delta audit

Compared with accepted S1.42Z:

- total ZIP members: `334`;
- changed existing member: exactly `export.r2x`;
- added member: exactly `BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll`;
- removed members: `0`;
- config changes: `0`;
- mod state changes: `0`;
- mod additions/removals: `0`.

The S1.42AB snapshot retains `Inject Dynamic Matching Weights = true`, so the failed S1.42AA config change is not inherited.

## Controller audit — PASS

`RuntimeInbox/ACTIVE_BUILD.txt`:

`S1.42AB`

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base profile = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- base SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor is armed.

`RuntimeInbox/Current/` contains only `.gitkeep`. Therefore no S1.42AB gameplay runtime log has yet been submitted or misattributed.

## S1.42AB architecture audit — PASS

Patch target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

Architecture:

1. LethalLevelLoader performs native matching, viability and exclusion first.
2. Project-local Harmony Postfix receives only the already-returned viable list.
3. Only positive rarity values are normalized to `100`.
4. No flow membership is added, removed, re-registered or deduplicated.
5. Enemy, Scrap and MapObject rarity systems are untouched.
6. Exact LLL version/target contract is checked fail-closed.

This is materially narrower than modifying every matching property and preserves upstream technical exclusions.

## Runtime-evidence interpretation audit — PASS

Do not treat the built-in LLL `Viable ExtendedDungeonFlows` line as final AB output because it is logged before the Postfix returns.

Authoritative marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Acceptance requires every positive entry in the final effective pool to be `(100)`.

## Local Gale state / automation audit — PASS

S1.42AB is already imported and current in Gale. The next chat must not request a redundant reinstall before the immediate gameplay run.

Canonical helper:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Status:

**FULL END-TO-END USER-VALIDATED under Windows PowerShell 5.1**

Validated revision marker:

`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob SHA:

`9458f427b538615249714e7f064f3107d6dcd36c`

Validated implementation commit:

`f711f53f4971f97200ed3605479ef887a14b243d`

AB archive `export.r2x` evidence SHA:

`331c01bfe5eda5d4ce9bc2a887fd322b302f32dccf9d95918d6c7d0c7fb6cf40`

The final user test proved the automated path after numeric old-profile selection + `y`:

- candidate download and SHA validation;
- selective old-profile deletion;
- automatic Gale Missing Profiles `Delete -> Submit`;
- single `.r2z` open event;
- automatic `Advanced options` expansion;
- automatic `Import all files` activation;
- automatic Import;
- exact local target `export.r2x` SHA verification;
- temporary archive cleanup;
- no second empty import dialog;
- no further Gale click or PowerShell Enter required.

Failed helper iterations remain intentionally documented in `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md` and `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md` because they contain do-not-regress evidence.

## Runtime-log uploader bootstrap audit

The project runtime uploader contract remains self-contained:

- verifies the exact local `LogOutput.log` path;
- resolves `gh.exe` from PATH and common install locations;
- if absent, installs GitHub CLI through `winget` and resolves it again without requiring a PowerShell restart;
- checks `gh auth status`;
- if not authenticated, launches `gh auth login --hostname github.com --git-protocol https --web`;
- uses the GitHub API directly and requires no local repository clone;
- safely creates/replaces `RuntimeInbox/Current/LogOutput.log`.

The profile-replacement launcher itself does not require GitHub CLI authentication because it reads the public repository through HTTP and uses local Windows/.NET facilities.

## Permanent compatibility / do-not-regress audit — preserved

Preserve:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- accepted S1.42Z Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning.

Never repeat S1.42R's whole-component disable strategy.

Every future project-local patch must comply with `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## Open findings preserved

### Black Mesa / Pikmin pathfinding

S1.42AA Black Mesa runtime showed repeated unreachable entrance-node / `Unpathable` ToShip routing correlated with a user-observed Pikmin stuck on a table while carrying scrap. This is diagnostic evidence worth retaining, but no broad fix is justified yet.

### Work/no-task

Two `Work state with no task assigned!` warnings occurred during a separate White-Pikmin lifecycle sequence in S1.42AA. Do not automatically attribute them to the Black Mesa table incident. Re-evaluate only if reproduced.

### Deferred scopes

Keep separate from AB until its gate closes unless the user explicitly changes scope:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup;
- Black Mesa table/NavMesh/Pikmin recovery.

Potential later isolated investigation: `woah25-LethalEscapeUpdated 2.5.0` for V81. It must not be mixed into AB and requires inspection of the actual 2.5.0 package/config plus isolated runtime validation against the AI/pathfinding-heavy stack.

## Intentional historical drift — preserved

The audit intentionally does **not** modify:

- stale chronology/current wording in older subsections of `Current/02_TECHNICAL_BASELINE.md`;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` that no longer perfectly describe accepted Compatibility Fixes `1.3.14` behavior.

These are non-functional and lower-authority than chronologically newer Current documents, actual code/config and fresh runtime evidence. Cosmetic cleanup remains deferred.

## Deletion audit

No runtime evidence or diagnostically useful historical material was deleted.

No file was identified with sufficient certainty as both obsolete and valueless to justify deletion during this handover.

## Final audit verdict

**PASS WITH INTENTIONAL HISTORICAL DRIFT PRESERVED.**

Canonical next action remains:

**Run one normal Offense gameplay round with the already-imported S1.42AB, enter the generated interior, upload the full fresh S1.42AB `LogOutput.log`, and analyze the authoritative final effective viable-pool marker before any successor is built.**
