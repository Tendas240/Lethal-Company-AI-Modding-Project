# 04 — Open Issues and Next Tests

## Accepted baseline — S1.42AB

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

S1.42AB remains accepted while S1.42AC is under runtime validation.

## Active gate — S1.42AC BCMER EventType Equal Distribution

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
Gale profile name: `LC V1 S1.42AC BCMER EventType Equal Distribution`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`

Candidate: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_CANDIDATE.json`  
Plan: `BuildSpecs/S1.42AC_PLAN.md`

### Frozen delta

Only `BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg` is intentionally modified, plus `export.r2x` for the Gale profile name.

`Use custom weights? = false` remains unchanged.

All eight EventType scales are:

`12.5, 0.0, 12.5, 12.5`

for Insane, VeryBad, Bad, Neutral, Good, VeryGood, Rare and Remove.

This removes difficulty-based skew from EventType selection and targets a fixed equal normalized distribution of `8 × 12.5%`.

Automated build QC:

- ZIP members `334`;
- changed existing exactly `Difficulty_Settings.cfg` and `export.r2x`;
- no added/removed members;
- no mod state/add/remove changes;
- no DLL/code patch.

## Exact next test

First import AC with the canonical validated helper:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Then do one normal **Offense** gameplay run.

Primary gate:

1. startup/main menu/lobby succeeds;
2. exact BCMER `1.71.0` loads normally;
3. Offense route/landing succeeds;
4. complete log contains all eight `Set eventType weight for <type> to <value>` lines for the same roll context;
5. all eight values are identical;
6. normal BCMER events still run;
7. disabled BCMER rain-event configuration remains preserved;
8. accepted S1.42AB interior normalization remains healthy when emitted;
9. accepted enemy/Pikmin/Jetpack/CodeRebirth behavior remains healthy;
10. Work/no-task preferably `0`;
11. Leader-null `0`;
12. Fatal `0`;
13. no new config-induced error flood.

Do **not** manually farm eight EventTypes. Equal runtime weights are the probability proof.

After the run, use the exact S1.42AC uploader in `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by AC SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`

No successor is armed.

## Deferred after AC

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- **repository information-architecture overhaul** per `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, with machine requirements in `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`. This supersedes the old vague `cosmetic documentation cleanup` scope and includes cosmetic drift cleanup as only one subordinate task.

The repository overhaul is specifically intended to make limited-context ChatGPT retrieval deterministic: compact bootstrap, topic knowledge map, explicit current-vs-history authority, build lineage, provenance links, readable binary snapshots, broken-reference/orphan CI checks and answerability-routing regression cases. Do not execute it in a way that muddies attribution during the open S1.42AC runtime gate.

## Permanent invariants

Preserve exact BCMER `1.71.0`, EnemyIsolation off, Compatibility Fixes `1.3.14`, BaboonBirdPikminEnemy enabled, narrow Hawk -> Pikmin prevention only, inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack, Puffer protection, Thumper Bite Limit `3`, Crawler absent from Attack Blacklist, accepted S1.42C moon power/spawn baseline, `Consistent Spawn Times = true`, accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning, and accepted S1.42AB post-viability interior normalization.
