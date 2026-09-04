# 00 — Current State

**Updated:** 2026-09-04 — S1.42AB accepted; S1.42AC runtime rejected; BCMER final-weight-path analysis next  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the Source of Truth.**

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Accepted interior architecture: LethalLevelLoader `1.7.12` owns viable/excluded flow membership first; S1.42AB then normalizes every positive rarity in the returned viable list to exactly `100` without adding/removing/re-registering flows. Accepted Offense runtime preserved all 40 viable entries, normalized 12/40 from `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

Authoritative marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

LLL's earlier `Viable ExtendedDungeonFlows` line is pre-Postfix and may remain unequal.

## Latest build / rejected candidate

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME FAIL / REJECTED / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Candidate record: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Rejection record: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_REJECTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`  
Raw log SHA-256: `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

S1.42AC changed only BCMER `Difficulty_Settings.cfg` plus the normal Gale profile-name metadata. All eight `[_EventType Weights]` scales were set to `12.5, 0.0, 12.5, 12.5`, with `Use custom weights? = false` preserved.

### Runtime rejection reason

The primary gate required all eight final BCMER runtime values from:

`Set eventType weight for <type> to <value>`

to be identical in the same roll context.

Five observed roll contexts consistently produced:

- Insane `6843`
- VeryBad `506`
- Bad `355`
- Neutral `1368`
- Good `1244`
- VeryGood `2737`
- Rare `27375`
- Remove `883`

Therefore the target `8 × 12.5%` equal final distribution was not achieved.

Comparison with S1.42AB proves the AC scale changes influenced the final BCMER weights, but equal configured scales do **not** imply equal final effective EventType weights. The exact additional BCMER `1.71.0` calculation is not yet proven and must be inspected before a successor is designed.

**Do not repeat:** do not build another candidate that merely gives all eight EventType scale curves the same value and assumes equal probability.

## AC regression evidence

AC otherwise preserved important baseline behavior:

- normal BCMER event execution remained active;
- S1.42AB interior normalization remained healthy;
- Offense final pool had 40 entries, all positive effective rarities `100`;
- `Mausoleum` generated successfully;
- later `CompanyBuildingLevel` normalization also had 40 entries all `100`;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference regression `0`;
- PikminNoticeZone regression `0`;
- Fatal `0`.

AC runtime coverage: `2,000,261` bytes, `20,460` lines, `19,547` parsed events, `77` Error-severity events, Fatal `0`.

Secondary AC evidence includes 43 dominant `NavMeshAgent:SetDestination` error signatures and 26 LethalMin route-failure signatures involving Pikmin/interior routing. Treat this as separate map/NavMesh/Pikmin evidence, not as proven causality from the BCMER config-only delta.

## Exact next action

**No runtime test is currently outstanding. No successor is armed.**

Next technical step:

1. inspect the exact BCMER `1.71.0` calculation that produces final `Set eventType weight for <type> to <value>` values;
2. identify the final effective EventType-weight owner and all additional type-dependent inputs;
3. decide whether deterministic inverse compensation in config is safely provable or whether a narrow fail-closed project-local final-weight normalization is safer;
4. preserve exact BCMER `1.71.0`, rain-event disables, event eligibility and all S1.42AB invariants;
5. only after this analysis plan/arm a successor.

Do not assign a successor build ID merely for convenience before the implementation path is verified.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED`;
- guarded base = `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`;
- guarded SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

`RuntimeInbox/Current/` is clean after AC ingest.

## Permanent anti-regression state

Preserve exact BCMER `1.71.0`; accepted BCMER rain disables; EnemyIsolation disabled; Compatibility Fixes `1.3.14`; BaboonBirdPikminEnemy enabled; narrow Hawk -> Pikmin prevention only; native inherited PikminEnemy lifecycle; Pikmin -> Baboon Hawk attack allowed; Puffer protection; Thumper Bite Limit `3`; Crawler absent from LethalMin Attack Blacklist; accepted S1.42C moon power/spawn baseline; `Consistent Spawn Times = true`; Jetpack `18`; Jet Fuel `18/18`; Thrusters `25/20`; Indoor Pikmin `0.09`; CarryStrength `3 / 30`; CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`; Functional Microwave volume `0.15`; Immortal Snail `40 / 2`; accepted S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach. Project-local patches must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## Deferred separate scopes

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

Planned, binding, **not executed**. It remains separate from gameplay/config/code changes.

Future-chat entry: `OVERHAUL_START_HERE_ChatGPT.txt`  
Plan: `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`  
Execution playbook: `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`  
Machine requirements: `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

When explicitly started later, first re-resolve the then-current project state and create/verify a separate standalone pre-overhaul backup repository before the first structural migration change.
