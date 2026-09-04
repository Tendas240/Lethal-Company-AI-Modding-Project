# 107 — Final Handover: S1.42AB Accepted / S1.42AC Rejected / BCMER Weight-Path Analysis Next

**Date:** 2026-09-04  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the Source of Truth.**

## Read first in a fresh ChatGPT session

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`
4. `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
5. `Current/Projektstatus_S1.42AC_REJECTED.json`
6. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
7. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
8. `Current/00_CURRENT_STATE.md`
9. `Current/01_HANDOVER_CORE.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
14. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
15. `OVERHAUL_START_HERE_ChatGPT.txt` only if the user explicitly starts the planned repository overhaul.

Do not require a local repository clone or local profile build while repository-native artifacts and GitHub automation are available.

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile:

`Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`

SHA-256:

`3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance:

`Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

Machine state:

`Current/Projektstatus_S1.42AB_ACCEPTED.json`

Runtime evidence:

`RuntimeEvidence/S1.42AB/20260904T174010Z/`

Raw LogOutput.log SHA-256:

`42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Accepted AB facts:

- exact LethalLevelLoader `1.7.12` validated;
- project-local post-viability normalization armed;
- Offense viable membership remained 40 entries;
- 12/40 positive rarities changed from pre-range `20..300` to final `100`;
- all positive final effective rarities = `100`;
- Black Mesa single-registered at `100`;
- `Expanded facility` generated successfully;
- Work/no-task = `0`;
- Leader-null = `0`;
- Compatibility Fixes Error = `0`;
- unspawned NetworkObjectReference regression = `0`;
- PikminNoticeZone regression = `0`;
- Fatal = `0`.

Authoritative interior marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

LLL's own earlier `Viable ExtendedDungeonFlows` line is pre-Postfix and may still show unequal values.

## Latest build — S1.42AC

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME FAIL / REJECTED / NOT ACCEPTED**

Profile:

`Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`

SHA-256:

`0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build workflow run:

`33903271224`

Automated build commit:

`a30b327580e28f42e55281e91abe03d32ae41363`

Candidate/build record:

`Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`

Runtime rejection:

`Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`

Machine state:

`Current/Projektstatus_S1.42AC_REJECTED.json`

Runtime evidence:

`RuntimeEvidence/S1.42AC/20260904T181854Z/`

Raw LogOutput.log SHA-256:

`8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

Runtime coverage:

- `2,000,261` bytes;
- `20,460` lines;
- `19,547` parsed events;
- `77` Error-severity events;
- Fatal `0`.

## Why S1.42AC failed

AC changed only BCMER `Difficulty_Settings.cfg` plus the Gale profile-name metadata. All eight `[_EventType Weights]` scales were set to the same constant:

`12.5, 0.0, 12.5, 12.5`

The intended target was exactly `8 × 12.5%`.

Fresh runtime evidence contains five repeated roll contexts where the final effective BCMER EventType weights were consistently:

- Insane `6843`
- VeryBad `506`
- Bad `355`
- Neutral `1368`
- Good `1244`
- VeryGood `2737`
- Rare `27375`
- Remove `883`

The eight final values are not equal. Therefore AC fails the primary acceptance objective.

Comparison with S1.42AB shows that AC did change the final weights relative to AB, so the configured scales influence the calculation. However, equal configured scales do not imply equal final type weights. BCMER 1.71.0 applies additional type-dependent calculation/weighting.

**Do-not-repeat:** do not build another candidate that merely gives all eight EventType scale curves the same value and assumes equal probability.

## What still passed in AC

The rejected candidate nevertheless preserved useful baseline behavior:

- normal BCMER event execution remained active;
- exact BCMER `1.71.0` remains the required version;
- S1.42AB interior normalization remained healthy;
- Offense final pool: 40 viable entries, all positive effective rarities `100`;
- `Mausoleum` generated successfully;
- later `CompanyBuildingLevel` normalization also showed 40 entries all `100`;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference regression `0`;
- PikminNoticeZone regression `0`;
- Fatal `0`.

AC is still rejected because its own target objective failed.

## Secondary AC evidence

AC emitted substantial Pikmin/NavMesh routing noise:

- 43 dominant `NavMeshAgent:SetDestination`-class Error signatures;
- 26 LethalMin route-failure Error signatures;
- repeated `Spoon(Clone)` failures involving interior entrance / `ReachInteriorEntrance` / `ToShip` routing.

This is not automatically caused by the BCMER config-only delta. Keep it as separate interior/Pikmin routing evidence. Do not mix a broad recovery patch into the immediate BCMER equal-distribution investigation.

## Exact next step

**No runtime test is currently outstanding. No successor is armed.**

Before building anything else for BCMER EventType equality:

1. inspect the exact BCMER `1.71.0` code/calculation path producing `Set eventType weight for <type> to <value>`;
2. identify the owner of the final effective EventType weight pool and every additional type-dependent input;
3. decide whether safe deterministic inverse compensation in config is provable, or whether a narrow project-local final-weight normalization is safer;
4. if code patching is required, follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, fail closed on the exact BCMER version/target contract, and preserve event eligibility/rain guards;
5. only then plan and arm a successor.

Do not silently choose a successor build ID before this analysis is complete.

## Controllers after handover

Canonical desired/current controller state:

- `BuildSpecs/current.json` disabled;
- build ID `IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED`;
- guarded base = accepted S1.42AB profile + SHA;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor armed;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`.

`RuntimeInbox/Current/` should contain only its placeholder after successful ingest.

## Permanent anti-regression invariants

Preserve:

- exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`; never silently upgrade to 2.x;
- accepted BCMER rain-event disables;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- only narrow Hawk -> Pikmin prevention;
- native inherited PikminEnemy lifecycle;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- Jetpack base acceleration `18`;
- Jet Fuel `18/18`;
- Jetpack Thrusters `25/20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`, Purple `30`;
- CodeRebirth ACU + G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max Snails `2`;
- accepted S1.42AB post-viability interior normalization.

Never repeat S1.42R's whole-component disable approach.

## Deferred, separate scopes

Keep separate unless the user explicitly chooses/groups them:

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.

## Planned repository information-architecture overhaul

The overhaul is fully planned but **not executed**.

Dedicated future-chat entry:

`OVERHAUL_START_HERE_ChatGPT.txt`

Plan:

`Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`

Execution playbook:

`Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`

Machine requirements:

`Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

When explicitly started in a future chat, the overhaul must first create and verify a **separate standalone pre-overhaul backup repository** against the frozen pre-overhaul HEAD before the first structural migration change. A branch/tag in the same repository alone is not sufficient. The actual project state at that future time must be re-resolved; do not assume this handover's build IDs are still current.

## Historical evidence retention

Do not delete failed builds, rejected candidates, runtime evidence, diagnostic records, restore baselines or do-not-regress decisions merely because they are not current. In particular retain S1.42AC and its runtime evidence as proof that equal configured BCMER EventType scales are not sufficient for equal final EventType probability.
