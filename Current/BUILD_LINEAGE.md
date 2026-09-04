# Build Lineage

**Status:** CURRENT / CANONICAL HISTORICAL INDEX  
**Authority:** human build-history router; exact build evidence remains in candidate/acceptance/rejection/runtime records  
**Canonical-For:** `build_lineage`  
**Machine Mirror:** `Current/BUILD_LINEAGE.json`  
**Sources:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/06_RECENT_WORK_S1.42N-S1.42Z.md`, `Current/06_RECENT_WORK_S1.42AA-S1.42AB.md`, build-specific Current records, BuildSpecs and RuntimeEvidence  
**Last-Validated:** 2026-09-04

## Current lineage head

- **Accepted gameplay baseline:** S1.42AB — Interior Weight Normalization.
- **Latest built artifact:** S1.42AC — BCMER EventType Equal Distribution — formally rejected/not promoted.
- **Active candidate:** none.
- **Next build:** none armed.

For current lifecycle state, use `Knowledge/CURRENT_LIFECYCLE.md`; this file answers historical lineage questions.

## Meaningful build history

| Build | Status / base safety | Principal purpose or result | Primary evidence |
|---|---|---|---|
| S1.2 | historical foundation | First profile/loading forensics and reproducible mod-stack investigation. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.3 | historical foundation | Lethal Company V81 transition and first interaction compatibility fixes. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.32-C | historical accepted step | LiveEnemyInfo safe-subset integration. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.32-D | historical accepted step | Rolling Giant + Scopophobia LLL registration. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.32-E | historical accepted step | CounterAttack/Butlers/KidnapperFoxOutskirts/Puffer compatibility changes. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.32-F | historical accepted step | Puffer trigger cleanup. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.32-G | obsolete / never replay | Accidental KidnapperFoxOutskirts divergence; preserved as a warning, not a restore point. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.33–S1.36 | diagnostic series | PikminNotice/EnemyCeiling and related targeted diagnostics. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.37–S1.38 | diagnostic/validation series | Minimal validation and error-logging refinement. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.39 | historical runtime-pass step | CodeRebirth/DawnLib upgrade architecture; CodeRebirthLib removed. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.39A | historical accepted step | Direct CodeRebirth utility-kill protection for Pikmin/Puffmin. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.39B | historical accepted step | Kidnapper Fox outside-disabled intent. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.39C | historical accepted step | Siren Head wrong-rarity correction to 30. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.39C2 | historical validated step | All-outside Siren Head behavior validated through Gale. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.40 | rejected approach | First CodeRebirth Currency/Flash-Turret natural-spawn suppression attempt; DawnLib regenerated author defaults. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.40A | rejected / no-go | Project-local filters partially worked but were not an acceptable ownership solution. | `Current/03_PROJECT_CHRONOLOGY.md`, `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md` |
| S1.40B | historical accepted step | Native-owner CodeRebirth/DawnLib config solution for Currency + Flash Turret. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.41 | historical full-stack runtime-pass baseline | BCMER 1.71.0 reactivation with normal project ownership guards; later superseded by S1.42 family. | `Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md` |
| S1.42A | historical runtime-validated step | Interior Expansion + LLL exclusions/restrictions. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42B | rejected / diagnostic | Enemy Spawn Balance + Texture Cleanup; failed intended power-over-time correction and was not retained. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42C | canonical restore baseline for enemy spawn/config | Reverted B's unwanted spawn-balance divergence, added Pikmin enemy guard, and became the permanent normal enemy-spawn restore point. | `Current/ENEMY_SPAWN_BASELINE_S1.42C.json` |
| S1.42D | rejected | Jetpack acceleration patch targeted inherited `Start` incorrectly; HarmonyX warning proved unsafe ownership. | `Current/03_PROJECT_CHRONOLOGY.md`, `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md` |
| S1.42E | build-aborted / invalid | Fail-closed local patch build-reference mismatch; no valid gameplay profile. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42F | mixed / superseded | Typed inherited-Start Jetpack attempt loaded acceleration 50 but exposed Lost->Company `GrabbableObject.Update` failure. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42G | build-pass candidate / superseded | Narrow follow-up for Lost-state crash; evidence retained but later Jetpack line superseded it. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42H | superseded | Jetpack balance + Puffer guard, acceleration 40. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42I | historical accepted step | Jetpack/Puffer/enemy cleanup; Bite Limit 3, Crawler removed from attack blacklist, Puffer protection. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42J | rejected/fallback | Baboon Hawk complete-isolation approach; later lifecycle evidence proved this architecture too broad. | `Current/03_PROJECT_CHRONOLOGY.md`, `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md` |
| S1.42K | superseded | Removed one Baboon issue but inherited adapter lifecycle crash remained. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42L | runtime-pass / superseded | Target regression-clean runtime step before long-run teardown investigation. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42M | not accepted | Long playtest ended with AdditionalNetworking + NetworkBehaviourReplication errors and severe freeze. | `Current/03_PROJECT_CHRONOLOGY.md` |
| S1.42N | diagnostic / inconclusive | AdditionalNetworking targeted repair; primary run invalid because target mod was not loaded. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42O | focused runtime-pass evidence / not full-stack baseline | One-ship focused enhancement; target fix loaded/executed and avoided target endgame freeze, but this was not a normal full-stack acceptance. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42P | rejected | Full-normal restoration caused `NetworkObjectReference` flood and sub-1fps freeze. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42Q | rejected | Narrow NetworkObjectReference prevention removed that signature but exposed repeated `PikminNoticeZone.OnTriggerStay` NRE/freeze. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42R | rejected / do not repeat | Whole-component `BaboonBirdPikminEnemy` disable removed target entry-point errors but broke inherited PikminEnemy death/unlatch lifecycle. | `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md` |
| S1.42S | runtime-accepted | Prevention-before-mutation Baboon architecture: adapter stays enabled; narrow Hawk/Grab guards; target lifecycle regressions zero. | `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md` |
| S1.42T | historical full-normal accepted step | Restored normal stack from S while reverting temporary diagnostic reductions to S1.42C baseline. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42U | historical accepted balance step | Pill balance + equal eight-way BCMER static EventType scales; later builds carry the concept forward. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42V | historical accepted balance step | Jetpack/Pikmin/Snail retune stage. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42W | rejected/not accepted | Naive static CodeRebirth aerial-defense reduction approach. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42X | diagnostic-only | Pipeline/refactor diagnostic; not a gameplay acceptance baseline. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42Y | rejected/not accepted | Post-load aerial-provider evaluation found 0 providers; useful root-cause evidence, not accepted behavior. | `Current/06_RECENT_WORK_S1.42N-S1.42Z.md` |
| S1.42Z | **accepted full-stack predecessor to AB** | Transactional DawnLib ACU/G.R.E.G. scaling + final Jetpack/Pikmin/Microwave/Snail retune. | `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md` |
| S1.42AA | rejected | Config-only interior equalization (`Inject Dynamic Matching Weights=false`) failed because LLL retained stronger matching rarities. | `Current/06_RECENT_WORK_S1.42AA-S1.42AB.md` |
| S1.42AB | **ACCEPTED CURRENT BASELINE** | Post-viability LLL normalization to Weight 100; preserves membership/exclusions and fixes AA's architectural limitation. | `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md` |
| S1.42AC | formally rejected/not promoted; interpretation corrected | Eight BCMER scales at 12.5. Old rejection required equal per-event log weights; source analysis proved those values are intentionally inverse-count-normalized. No successor compensation build is justified. | `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md` |

## Key exact artifacts

### S1.41

- Profile SHA-256: `21161fcfa9cf5aac23ecffd9da4720308988868cf764bad108519077fea86932`
- Exact BCMER: `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

### S1.42A

- Profile SHA-256: `476e9c1a464cc6788e56e97394eceb79fa26f2d11a3761005cce022ce07dbd1c`

### S1.42C

- Profile: `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`
- SHA-256: `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

### S1.42G

- Profile SHA-256: `2bd2778547d552e7bd60e9170360c06c17d163f0b759731c50632ce5526c86af`

### S1.42Z

- Profile: `Profiles/LC V1 S1.42Z Final Balance Acceptance.r2z`
- SHA-256: `841f3b8fb9eee7f0f374b36975b03e9b4f96413f2b3344287b3cceb9f3855263`
- Runtime: `RuntimeEvidence/S1.42Z/20260904T135820Z/`
- Aerial-defense DLL SHA-256: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`
- Jetpack DLL SHA-256: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### S1.42AA

- Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`
- SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`
- Runtime: `RuntimeEvidence/S1.42AA/20260904T153744Z/`
- Result: rejected; final effective LLL rarities remained unequal.

### S1.42AB

- Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Runtime: `RuntimeEvidence/S1.42AB/20260904T174010Z/`
- Workflow run: `33892396551`
- Build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`
- Interior-normalization DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

### S1.42AC

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Runtime: `RuntimeEvidence/S1.42AC/20260904T181854Z/`
- Build workflow run: `33903271224`
- Build commit: `a30b327580e28f42e55281e91abe03d32ae41363`

## Feature/fix lookup

| Feature / decision | Introduced / established by |
|---|---|
| CodeRebirthLib removed; DawnLib ownership | S1.39 |
| CodeRebirth utility-kill Pikmin protection | S1.39A |
| Native Currency/Flash-Turret natural-spawn control | S1.40B |
| BCMER 1.71.0 full-stack activation/guards | S1.41 |
| Interior package expansion/restrictions | S1.42A |
| Normal enemy-spawn restore baseline | S1.42C |
| Thumper Bite Limit 3 / Crawler attack allowed / Puffer protection | S1.42I and later accepted descendants |
| Correct Baboon Hawk prevention-before-mutation lifecycle | S1.42S |
| Full-normal restoration after diagnostic chain | S1.42T |
| Equal BCMER static EventType scale concept | S1.42U, later re-applied in S1.42AC |
| Final accepted Jetpack acceleration 18 + Pikmin/Microwave/Snail values | S1.42Z |
| Transactional CodeRebirth ACU/G.R.E.G. 18-curve ×0.5 scaling | S1.42Z |
| Config-only interior equalization proven insufficient | S1.42AA rejection |
| Post-viability interior rarity normalization to 100 | S1.42AB |
| Exact BCMER per-event-weight semantic correction | post-S1.42AC analysis in `Current/109...` |

## Parentage rules that matter

- S1.42C is the restore baseline for normal enemy-spawn/config state after S1.42B diagnostic divergence.
- S1.42S is the accepted recovery from the rejected S1.42R whole-component disable architecture.
- S1.42AB was built **directly from accepted S1.42Z**, not from rejected S1.42AA. AA is diagnostic evidence proving the config-only approach failed.
- S1.42AC was built from S1.42AB but was never promoted, so the current accepted gameplay baseline remains S1.42AB.

When an exact profile/hash/status is not listed here or in the machine mirror, open the referenced build-specific record rather than inferring it from build-name order.
