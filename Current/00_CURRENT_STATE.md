# 00 — Current State

**Updated:** 2026-09-04 — S1.42AB accepted; S1.42AC built and runtime validation next  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Accepted interior architecture: LethalLevelLoader owns viability/exclusion membership first; S1.42AB normalizes every positive rarity in the returned viable list to exactly `100` without adding/removing/re-registering flows. The accepted Offense runtime preserved all 40 viable entries, normalized 12/40 from range `20..300`, kept Black Mesa single-registered, successfully generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0` and Fatal `0`.

## Active runtime candidate

**S1.42AC — BCMER EventType Equal Distribution**

Status: **BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
Gale profile name: `LC V1 S1.42AC BCMER EventType Equal Distribution`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Candidate record: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_CANDIDATE.json`  
Plan: `BuildSpecs/S1.42AC_PLAN.md`  
Snapshot: `ProfileSources/S1.42AC/`

## Exact S1.42AC delta

Only `BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg` changes, plus the mandatory Gale profile-name update in `export.r2x`.

`Use custom weights? = false` remains preserved.

All eight `[_EventType Weights]` keys are fixed to:

`12.5, 0.0, 12.5, 12.5`

Target: Insane, VeryBad, Bad, Neutral, Good, VeryGood, Rare and Remove each at exactly `12.5%`, independent of difficulty.

Archive verification vs S1.42AB:

- ZIP members `334`;
- changed existing exactly `Difficulty_Settings.cfg` and `export.r2x`;
- added `0`;
- removed `0`;
- mod state/add/remove delta `0`;
- no DLL/code patch.

Exact BCMER `1.71.0` and all accepted S1.42AB invariants remain preserved.

## Current Gale state / exact next action

Last confirmed installed Gale profile: accepted S1.42AB.

Import S1.42AC with the fully validated helper:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

After import, run one normal Offense gameplay round. The primary probability gate is **not** observing all eight event categories manually; it is the complete log showing all eight BCMER `Set eventType weight for ...` values equal in the same roll context.

Then upload the complete fresh log using the exact S1.42AC uploader in `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

## Runtime acceptance gate

Require:

- startup/main menu/lobby PASS;
- exact BCMER `1.71.0` loads normally;
- Offense routing/landing succeeds;
- all eight BCMER EventType runtime-weight lines are present;
- all eight resulting values are identical;
- normal BCMER event execution remains functional;
- accepted S1.42AB interior normalization remains healthy when emitted;
- accepted enemy/Pikmin/Jetpack/CodeRebirth behavior remains healthy;
- Work/no-task preferably `0`;
- Leader-null `0`;
- Fatal `0`;
- no new config-induced error flood.

S1.42AB remains accepted until this gate passes.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_BUILD_AWAITING_RUNTIME_VALIDATION`;
- guarded base = `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`;
- guarded SHA-256 = `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`

## Planned repository information-architecture overhaul

The previous vague `cosmetic documentation cleanup` item is now formalized as a binding repository information-architecture overhaul:

- canonical plan: `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`;
- machine-readable requirements: `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`.

The overhaul targets deterministic limited-context ChatGPT retrieval through a compact bootstrap, topic knowledge map, formal authority/supersession metadata, build lineage, provenance links, readable binary snapshots, broken-link/orphan validation and an answerability-routing regression suite. It must preserve historical evidence and must not disturb the active S1.42AC runtime gate.

## Permanent invariants

Preserve exact BCMER `1.71.0`, EnemyIsolation off, Compatibility Fixes `1.3.14`, BaboonBirdPikminEnemy enabled with only narrow Hawk -> Pikmin prevention, native inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack, Puffer protection, Thumper Bite Limit `3`, Crawler absent from Attack Blacklist, accepted S1.42C moon power/spawn baseline, `Consistent Spawn Times = true`, Jetpack `18`, Jet Fuel `18/18`, Thrusters `25/20`, Indoor Pikmin `0.09`, CarryStrength `3 / 30`, CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`, Functional Microwave volume `0.15`, Immortal Snail `40 / 2`, and S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach.

## Deferred after AC

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking/LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul per `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, including cosmetic drift cleanup as a subordinate task.
