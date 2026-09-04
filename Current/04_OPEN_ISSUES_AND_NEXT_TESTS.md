# 04 — Open Issues and Next Tests

## Accepted baseline — S1.42AB

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

S1.42AB remains the canonical accepted gameplay baseline.

## Latest build — S1.42AC rejected

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME FAIL / REJECTED / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_REJECTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`  
Raw log SHA-256: `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

### Primary failure

All eight configured EventType scales were set to `12.5, 0.0, 12.5, 12.5`, but five runtime roll contexts consistently produced final BCMER weights:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

The final weights are not equal, so the intended `8 × 12.5%` distribution was not achieved.

Comparison with S1.42AB shows that AC did influence the final weights, but equal configured scales do not equalize the final effective BCMER EventType pool. The exact additional BCMER `1.71.0` weighting path must be inspected before another implementation is attempted.

**Do not repeat:** no successor may simply set all eight scale curves to the same value and assume equal final probability.

### AC preserved regression checks

- normal BCMER event execution remained active;
- S1.42AB interior normalization remained healthy;
- Offense final viable pool: 40 entries, all positive effective rarities `100`;
- `Mausoleum` generated successfully;
- later `CompanyBuildingLevel` normalization: 40 entries all positive `100`;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference regression `0`;
- PikminNoticeZone regression `0`;
- Fatal `0`.

Runtime coverage: `2,000,261` bytes, `20,460` lines, `19,547` parsed events, `77` Error-severity events, Fatal `0`.

### Secondary AC observation

The log contains 43 dominant `NavMeshAgent:SetDestination` error signatures and 26 LethalMin route-failure signatures, including repeated Pikmin/interior entrance/ToShip failures. Treat as separate map/NavMesh/Pikmin routing evidence. Do not attribute causally to the BCMER config-only change without reproducibility and do not mix a broad routing patch into the immediate BCMER probability investigation.

## Exact next work — analysis, not gameplay test

**No runtime test is currently outstanding. No successor is armed.**

Next step:

1. inspect the exact BCMER `1.71.0` code/calculation path that produces `Set eventType weight for <type> to <value>`;
2. identify the owner of the final effective EventType weight pool and all additional type-dependent inputs;
3. determine whether safe deterministic inverse config compensation is provable or whether a narrow project-local final-weight normalization is safer;
4. if a code patch is needed, follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and fail closed on exact BCMER version/target contract;
5. preserve exact BCMER `1.71.0`, disabled rain routes, eligibility rules and all accepted S1.42AB behavior;
6. only after the calculation path is understood plan/arm a successor.

Do not assign a successor build ID before this analysis is complete.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED` and guarded by accepted S1.42AB profile SHA `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

No successor is armed. There is no log uploader to run now because there is no pending runtime test.

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

Planned/binding but **not executed**. It supersedes the old vague `cosmetic documentation cleanup` scope.

Entry: `OVERHAUL_START_HERE_ChatGPT.txt`  
Plan: `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`  
Execution playbook: `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`  
Machine requirements: `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

When explicitly started later, the future chat must re-resolve the then-current project state, freeze the exact pre-overhaul HEAD, create and verify a **separate standalone backup repository**, record `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`, and only then begin structural migration. A branch/tag in this repository alone is insufficient.

## Permanent invariants

Preserve exact BCMER `1.71.0`, accepted rain disables, EnemyIsolation off, Compatibility Fixes `1.3.14`, BaboonBirdPikminEnemy enabled, narrow Hawk -> Pikmin prevention only, inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack, Puffer protection, Thumper Bite Limit `3`, Crawler absent from Attack Blacklist, accepted S1.42C moon power/spawn baseline, `Consistent Spawn Times = true`, accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning, and accepted S1.42AB post-viability interior normalization.

Never repeat S1.42R's whole-component disable approach.
