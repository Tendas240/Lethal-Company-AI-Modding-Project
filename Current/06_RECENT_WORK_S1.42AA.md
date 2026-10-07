# 06 — Recent Work — S1.42AA

**Date:** 2026-09-04  
**Scope:** S1.42AA Interior Weight Equalization + validated Gale active-profile replacement workflow

## Starting accepted state

The accepted full-normal-stack rollback baseline remains:

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z runtime acceptance confirmed Jetpack `10 -> 18`, CodeRebirth ACU + G.R.E.G. exact 18-curve provider contracts ×`0.5`, Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0`, relevant NetworkObjectReference/PikminNoticeZone regression markers `0`, project-local Error-severity `0`, and Fatal `0`. The user reported the resulting behavior as satisfactory.

## Interior equalization root cause

The project-normalized LethalLevelLoader configured dungeon tag weights were already `Vanilla:100,Custom:100` in S1.42Z.

However, LethalLevelLoader still had:

`Inject Dynamic Matching Weights = true`

That setting re-injected mod-author Level/Dungeon MatchingProperties on landing. S1.42Z Offense runtime evidence therefore still showed unequal effective viable-dungeon weights such as LiminalHouse `300`, Sub Systems `275`, Abandoned Foundry `250`, Shatteredrooms `75`, Lead Factory `70`, Spelunkers Caverns (Random) `50`, Crimson Keep `35`, Gray Apartments `25`, DeepcoreMines `25`, and multiple `20` values.

The narrow architecture chosen for the next build was therefore to disable the re-injection rather than rewriting dozens of already-normalized dungeon blocks.

## S1.42AA build

**S1.42AA — Interior Weight Equalization**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Build workflow run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

Candidate record: `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`  
Plan: `BuildSpecs/S1.42AA_PLAN.md`  
Readable snapshot: `ProfileSources/S1.42AA/`

Exact functional change:

`Inject Dynamic Matching Weights = true -> false`

Automated archive delta vs accepted S1.42Z:

- ZIP members: `333`;
- changed existing members: exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- added members: `0`;
- removed members: `0`;
- mod-state changes: `0`;
- mod additions/removals: `0`;
- no project-local DLL changed.

Black Mesa remains on its dedicated native-owner configuration path with `lethal_company:vanilla=+100,lethal_company:custom=+100`. Do not create a duplicate LLL owner path.

Shatteredrooms' Experimentation/Embrion restriction remains a technical compatibility guard pending dedicated evidence that removing it is safe.

## Permanent interior rule

Every eligible installed interior should have the same effective selection weight on vanilla and custom moons. Future interiors must be inspected and normalized into the same architecture before acceptance unless a documented technical incompatibility requires an exception.

Equal probability does not mean blindly removing hard compatibility restrictions.

## Gale profile-replacement helper development

A repository-backed helper was developed to replace repetitive manual profile-download/import preparation.

Early experimental variants failed for three distinct reasons and must not be reintroduced:

1. case-sensitive `LOESCHEN` confirmation (`-cne`) rejected lowercase user input;
2. Windows PowerShell 5.1 array behavior caused GitHub directory results to be treated as `System.Object[]` where a single path/string was expected;
3. a normal variable named `$matches` collided case-insensitively with PowerShell's automatic `$Matches` variable after `-match` evaluation.

The architecture was simplified to use repository controllers directly instead of fuzzy profile matching:

- `RuntimeInbox/ACTIVE_BUILD.txt` supplies the active build ID;
- `Current/AUTO_BUILD_RESULT.json` must contain the same build ID;
- `output_profile` supplies the exact `.r2z` path;
- `output_sha256` supplies the exact expected hash.

Final helper: `RuntimeTools/ReplaceActiveGaleProfile.ps1`

Validated behavior under Windows PowerShell 5.1:

- closes Gale;
- resolves exact active build and exact repository profile;
- downloads the new profile before any destructive local action;
- verifies SHA-256;
- lists local Gale profiles numerically;
- asks `y/n` before deleting only the selected profile;
- opens the verified `.r2z` in Gale;
- preserves the manual safe gate `Advanced options -> Import all files`;
- deletes the downloaded `.r2z` from Downloads only after the user confirms the import completed.

The user validated the final `y/n` version using a disposable profile named `testpowershell`. The user also successfully imported S1.42AA through the workflow. The helper is now canonical and binding for future ready-to-test builds.

Canonical workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

Permanent one-line launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

For every future ready-to-test build ChatGPT must provide both this replacement launcher and the build-specific runtime-log uploader in the same response.

## Current state at handover

S1.42AA is **BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**.

The user has already imported S1.42AA successfully with `Advanced options -> Import all files`. No S1.42AA gameplay runtime gate has been performed yet and `RuntimeInbox/Current/` contains only `.gitkeep`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION` with S1.42AA as guarded base. No successor is armed.

## Exact next step

Do **one normal Offense gameplay run** in S1.42AA, enter the generated interior, then upload the complete fresh `LogOutput.log` using the exact S1.42AA uploader in `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`.

The runtime log must prove that eligible `Viable ExtendedDungeonFlows` use the common effective weight `100` instead of the former unequal author weights, while normal generation/gameplay remains healthy. Required regressions: Work/no-task `0`, Leader-null `0`, Fatal `0`, no new project-local exception class, no duplicate Black Mesa/native-owner regression, and no unsafe dungeon generation.

Do not build a successor before analyzing this evidence.

## Deferred, intentionally not mixed into S1.42AA

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed equal distribution `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.
