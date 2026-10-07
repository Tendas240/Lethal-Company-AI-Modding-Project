# Build Lineage

**Status:** CURRENT / CANONICAL HISTORICAL INDEX  
**Authority:** human build-history router; exact build evidence remains in candidate/acceptance/rejection/runtime records  
**Canonical-For:** `build_lineage`  
**Machine Mirror:** `Current/BUILD_LINEAGE.json`  
**Last-Validated:** 2026-09-24

## Current lineage head

- **Accepted gameplay baseline:** S1.42AK — LC Office Camera Enemy Balance — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact / active candidate:** S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix — **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**.
- **Accepted predecessor / rollback provenance:** S1.42AI — BCMER ShyGuy Interior-Only Event Correction.
- **Balanced parent:** S1.42AJ — LC Office V81 Integration — not accepted; exact parent of S1.42AK.
- **Completed LC Office diagnostic evidence:** S1.42AJ-DIAG1 / S1.42AJ-DIAG2 — diagnostic-only, not gameplay accepted.
- **Current action:** run the bounded BMDSFIX1 Black Mesa x DeepSewersFlow runtime gate plus one non-target generation, then ingest the exact runtime log. S1.42AK remains accepted until an explicit decision.

For live lifecycle state use `Knowledge/CURRENT_LIFECYCLE.md`. This file is the build-history router; use the linked build-specific evidence for exact forensic detail.

## Meaningful build history

| Build | Status | Principal purpose / result |
|---|---|---|
| S1.2 | historical foundation | First reproducible profile/loading forensics. |
| S1.3 | historical foundation | Lethal Company V81 transition and early interaction compatibility. |
| S1.32-C | historical accepted step | LiveEnemyInfo safe subset. |
| S1.32-D | historical accepted step | Rolling Giant + Scopophobia LLL registration. |
| S1.32-E | historical accepted step | Counterattack/Butlers/KidnapperFoxOutskirts/Puffer compatibility refinement. |
| S1.32-F | historical accepted step | Puffer trigger cleanup. |
| S1.32-G | rejected | Accidental KidnapperFoxOutskirts divergence; never replay. |
| S1.33–S1.36 | diagnostic series | PikminNotice/EnemyCeiling focused diagnostics. |
| S1.37–S1.38 | diagnostic series | Minimal validation/error-logging refinement. |
| S1.39 | runtime-pass step | CodeRebirth/DawnLib modern ownership architecture; CodeRebirthLib removed. |
| S1.39A | historical accepted step | CodeRebirth utility-kill protection for Pikmin/Puffmin. |
| S1.39B | historical accepted step | Kidnapper Fox outside-disabled intent. |
| S1.39C / C2 | accepted/validated steps | Siren Head rarity 30 and all-outside validation. |
| S1.40 | rejected | Sparse Currency/Flash-Turret suppression; owner configs regenerated defaults. |
| S1.40A | rejected | Local object filters were the wrong ownership layer. |
| S1.40B | historical accepted step | Native CodeRebirth/DawnLib Currency + Flash-Turret control. |
| S1.41 | historical full-stack pass | Exact BCMER 1.71.0 reactivation with project ownership/rain guards. |
| S1.42A | historical runtime-pass | Interior expansion and LLL restrictions. |
| S1.42B | rejected | Enemy-spawn balance experiment not retained. |
| S1.42C | canonical restore baseline | Normal enemy-spawn/config restore point + Pikmin enemy guard. |
| S1.42D | rejected | Unsafe inherited-Start Jetpack Harmony target. |
| S1.42E | build-aborted | Fail-closed local patch reference mismatch. |
| S1.42F–H | superseded diagnostics | Jetpack ownership/Lost-state/Puffer iterations. |
| S1.42I | historical accepted step | Thumper Bite Limit 3, Crawler attack allowed, Puffer protection. |
| S1.42J–L | rejected/superseded/runtime-pass chain | Baboon compatibility iterations leading toward lifecycle-safe design. |
| S1.42M–Q | diagnostic/rejected chain | Long-run networking, NetworkObjectReference and PikminNotice evidence. |
| S1.42R | **rejected / do not repeat** | Whole-component `BaboonBirdPikminEnemy` disable broke inherited death/unlatch lifecycle. |
| S1.42S | runtime-accepted focused | Prevention-before-mutation Baboon architecture; adapter stays enabled. |
| S1.42T | historical accepted | Full-normal enemy restoration to the S1.42C-derived normal baseline. |
| S1.42U | historical accepted | Pill balance + equal eight-way BCMER static EventType scale concept. |
| S1.42V | historical accepted | Intermediate Jetpack/Pikmin/Snail retune. |
| S1.42W | rejected | Naive CodeRebirth aerial-defense reduction. |
| S1.42X | diagnostic-only | Aerial-defense ownership/pipeline diagnostic. |
| S1.42Y | rejected | Post-load provider evaluation; useful root-cause evidence, not accepted behavior. |
| S1.42Z | accepted predecessor | Final accepted balance/Jetpack/Pikmin/Microwave/Snail + DawnLib ACU/G.R.E.G. scaling. |
| S1.42AA | rejected | Config-only interior equalization failed to equalize final effective LLL rarities. |
| S1.42AB | accepted predecessor to AC | Post-viability LLL normalization to Weight 100 while preserving membership/exclusions. |
| S1.42AC | accepted predecessor to AF | Equal BCMER static EventType probability. Historical per-event-equality rejection is retained, but `Current/109` corrected its interpretation and `Current/118` explicitly accepted the artifact. |
| S1.42AD | **REJECTED** | Functional Microwave half-frequency attempt. Runtime exposed 18 Interior/tag curves instead of the frozen zero-Interior assumption; fail-closed refusal prevented the `0.5` mutation from applying. |
| S1.42AE | **SUPERSEDED — PATH-LENGTH BLOCKED, NOT GAMEPLAY-REJECTED** | Corrected provider code was never reached; v2.4 plus direct filesystem checks proved the 40,960-byte LC SoundAPI binding existed while its full path measured 262 characters and BepInEx/Mono still failed before chainloader startup. |
| S1.42AF | **ACCEPTED PREDECESSOR** | Path-length-safe packaging successor built directly from S1.42AC. Runtime proved the nested LC SoundAPI binding at 226 characters, normal startup, and the exact 18 Moon / 18 Interior Functional Microwave contract with only the 18 Moon/tag curves scaled by `0.5`. |
| S1.42AG | **RUNTIME REJECTED / PARTIAL FIX** | `MouthDogPikminEnemy.DoCheckInterval()` prevention successfully removed the LethalMin bite/grab/death-timer mutation path and the 707-warning aftermath, but a Mouth Dog still targeted/attacked a scrap-carrying Purple Pikmin through an unresolved path; reverse-direction Pikmin -> Dog behavior was not positively proven. |
| S1.42AH | **ACCEPTED PREDECESSOR TO AI** | Dual exact MouthDog adapter + Vanilla Pikmin collision prevention; targeted runtime preserved player, reverse Pikmin lifecycle and final non-Pikmin EnemyAI neighbor behavior. |
| S1.42AI | **ACCEPTED PREDECESSOR** | Accepted BCMER ShyGuy interior-only event correction; rollback provenance predecessor to S1.42AK. |
| S1.42AI-DIAG1 | **RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED** | Temporary exact ShyGuy isolation diagnostic built from S1.42AI. Build/static/materialized delta passed, but runtime owner prevalidation could not resolve the hardcoded `LethalMin.PikminType`, DIAG1 marked itself invalid and rolled back all of its own Harmony hooks. |
| S1.42AI-DIAG1R1 | **RUNTIME DIAGNOSTIC FAILED / REPAIR ANALYSIS REQUIRED / NOT ACCEPTED** | R1 repaired the exact `WithdrawPikminFromOnion` metadata-derived owner type and proved that repair at runtime. A later strict complex-owner target then failed because `ElevatorMod.Patches.EndlessElevator` was absent; DIAG1 invalidated and rolled back all owned Harmony hooks. Failure authority: `Current/147...`. |
| S1.42AI-DIAG1R2 | **RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED** | R2 armed the owner/applicability repairs, then failed exact ShyGuy identity resolution because source required ordinal `Shy Guy` while runtime proved `Shy guy`; failure authority: `Current/149...`. |
| S1.42AI-DIAG1R3 | **RUNTIME DIAGNOSTIC PASS / NOT GAMEPLAY ACCEPTED** | Exact `Shy guy` identity/isolation passed; interior visibility was observed and exterior visibility was not exercised. Diagnostic evidence only; the independent full-normal S1.42AI gate later passed. |
| S1.42AJ | **NOT ACCEPTED BALANCED PARENT** | Compatibility-first LC Office V81 package integration from exact accepted S1.42AI; exact balanced parent of S1.42AK. |
| S1.42AK | **ACCEPTED FULL NORMAL STACK** | Accepted balanced LC Office camera/enemy integration; full-normal Offense gate passed with limited hostile-indoor coverage explicitly preserved. |
| S1.42AK-BMDSFIX1 | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** | Exact pair-scoped Black Mesa x DeepSewersFlow size clamp over accepted S1.42AK; exact reviewed/published bytes are active for runtime qualification only. |

Older details are preserved in `Current/03_PROJECT_CHRONOLOGY.md`, the `Current/06_RECENT_WORK_*.md` series, build-specific decision records, and `RuntimeEvidence/`.

## Exact current-line artifacts

### S1.42AJ — LC Office V81 static-validated successor

- Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`
- SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`
- Parent: S1.42AI
- Candidate: `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`
- Static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`
- Build workflow run: `35222275686`
- Build commit: `7fbaae92523637ae3fec6c1e242ec2538918e7b7`
- Runtime: armed / full-normal validation outstanding / no runtime evidence yet


### S1.42AK — LC Office Camera Enemy Balance

- Parent: exact S1.42AJ, never DIAG1/DIAG2.
- Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`
- SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`
- Plan: `BuildSpecs/S1.42AK_PLAN.md`
- Static evidence: `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`
- Successful build workflow run: `35366580975`
- Build commit: `395f8298230d343b523eeda3afbfc9253a281931`
- Candidate: `Current/157_S1.42AK_BUILD_CANDIDATE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`
- Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`
- Project status: `Current/Projektstatus_S1.42AK_ACCEPTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`
- Runtime log SHA-256: `cc0f0a7a6c6a76ad44266aded11ff9cb2aca21f2623f5fb895d371ad778526b9`
- Status: **accepted full-normal-stack gameplay baseline**.
- Coverage qualification: the first attempt ended before interior entry; the second selected Spooky Manor and provided roughly three minutes of played interior coverage with no hostile enemy sighting. This is not treated as proof of a spawn regression.
- Accepted delta: LC Office `Camera Frame Speed = 0`, Men-stalker disabled, Aloe `PowerLevel = 0`; RandomEnemiesSize byte-identical and LC Office scrap untuned.

### S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix

- Parent: exact accepted S1.42AK.
- Profile: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`
- SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`
- BMDSFIX1 DLL SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`
- Plan: `BuildSpecs/S1.42AK-BMDSFIX1_PLAN.md`
- Build result: `BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/BUILD_RESULT.json`
- Publication evidence: `BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`
- Activation: `Current/174_S1.42AK_BMDSFIX1_RUNTIME_ACTIVATION.md`
- Status: **active runtime candidate / not accepted**.
- Scope: only Black Mesa x `DeepSewersFlow`; no Greenhouse, universal availability, package or config change.

### S1.42C — enemy-spawn restore baseline

- Profile: `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`
- SHA-256: `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`
- Restore-state authority: `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

### S1.42S — focused Baboon lifecycle acceptance

- Profile: `Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z`
- SHA-256: `addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`
- Acceptance: `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
- Runtime: `RuntimeEvidence/S1.42S/20260903T205550Z/`

### S1.42Z — accepted predecessor

- Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`
- SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`
- Candidate: `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
- Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
- Runtime: `RuntimeEvidence/S1.42Z/20260904T135820Z/`
- Build workflow run: `33874737048`
- Automated build commit: `267543634bb884bb447bf4bec320103ba75c9ff8`

### S1.42AA — rejected interior config-only attempt

- Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`
- SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`
- Runtime: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

### S1.42AB — accepted predecessor to AC

- Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Candidate: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`
- Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
- Runtime: `RuntimeEvidence/S1.42AB/20260904T174010Z/`
- Build workflow run: `33892396551`
- Build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`

### S1.42AC — accepted predecessor

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Candidate: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Historical rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Corrected source analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`
- Corrected acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Original runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`
- Fresh raw-log SHA-256: `98170374c4ffb6f40322a8019ad7f7f807e900525717dfdf7e70698bd7f28fa8`
- Build workflow run: `33903271224`
- Build commit: `a30b327580e28f42e55281e91abe03d32ae41363`

### S1.42AD — rejected Functional Microwave candidate

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- Candidate: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`
- Rejection: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`
- Project status: `Current/Projektstatus_S1.42AD_REJECTED.json`
- Plan / Patch Safety Review: `BuildSpecs/S1.42AD_PLAN.md`
- Build workflow run: `33959742235`
- Build commit: `1463a6cde5e8cb7655dd233f83da5157c91b036e`
- DLL SHA-256: `45f22f9b27e3ab7c853fe742bb7c2ce9bc94abc5a0856bb278c747076a2f99c7`
- Runtime evidence: `RuntimeEvidence/S1.42AD/20260905T103333Z/`
- Raw log SHA-256: `30c69254c4a4fd6bea1ec83cda075c168742c9060b88b09c22025973b074b3e8`
- Result: dependency validation passed, but provider contract failed closed on 18 unexpected Interior/tag curves; no x0.5 application marker.

### S1.42AE — superseded Functional Microwave correction candidate

- Profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`
- SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`
- Candidate: `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`
- Analysis: `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`
- Project status: `Current/Projektstatus_S1.42AE_CANDIDATE.json`
- Plan: `BuildSpecs/S1.42AE_PLAN.md`
- Build workflow run: `33968217356`
- Build commit: `85e6caade0edd94ac5d7f409b9dd734fc8613f3f`
- DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`
- Parent: accepted S1.42AC, not rejected S1.42AD.
- Status: superseded for path-length-safe packaging; provider code never executed; not accepted and not classified as a Microwave gameplay/runtime rejection.
- Supersession: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`

### S1.42AF — accepted predecessor to S1.42AH

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- Gale profile name: `LC V1 S1.42AF Microwave Fix`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Candidate: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Supersession/promotion analysis: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`
- Project status: `Current/Projektstatus_S1.42AF_ACCEPTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`
- Plan: `BuildSpecs/S1.42AF_PLAN.md`
- Build workflow run: `33993880634`
- Build commit: `2cab9044579e74739669440699c763a32f0fe379`
- DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Parent: accepted S1.42AC, not S1.42AE.
- Runtime path gate: nested `me.loaforc.soundapi.lethalcompany.dll` existed with 40960 bytes at a 226-character full path; normal BepInEx/game startup succeeded.
- Functional Microwave gate: CodeRebirth `1.6.9`, DawnLib/Dusk `0.9.25`, `PrioritiseMoons=true`, 18 Moon/tag curves and 18 Interior/tag curves; 18 Moon/tag curves scaled by `0.5`, Interior curves validation-only and not mutated.
- Status: accepted predecessor / safe rollback point.
- Separate inherited Mouth Dog / Pikmin compatibility finding: `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`.

### S1.42AG — rejected Mouth Dog Pikmin one-way protection candidate

- Parent: accepted S1.42AF.
- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Project status: `Current/Projektstatus_S1.42AG_REJECTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`
- Plan: `BuildSpecs/S1.42AG_PLAN.md`
- Atomic build workflow run: `34004938402`
- Build commit: `bb23701839d4c94bcad053a282f905ca571fc524`
- Compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`
- Proven partial fix: `Priority.First` prevention on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` successfully blocked the LethalMin Pikmin bite/grab/death-timer mutation path and eliminated the associated `Work state with no task assigned!` burst.
- Rejection reason: a Mouth Dog still visibly targeted and attacked a scrap-carrying Purple Pikmin through an unresolved path outside that dispatcher; intended Pikmin -> Mouth Dog attack/latch preservation was not positively proven.
- Status: runtime rejected / partial fix / not a safe gameplay base.

### S1.42AH — accepted Mouth Dog Pikmin dual prevention predecessor

- Parent: accepted S1.42AF, never rejected S1.42AG.
- Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Partial decisions: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`
- Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
- Project status: `Current/Projektstatus_S1.42AH_ACCEPTED.json`
- Final decisive runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`
- Final raw-log SHA-256: `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`
- Plan: `BuildSpecs/S1.42AH_PLAN.md`
- Build workflow run: `34141360051`
- Build commit: `fdb6b94e34144f860f6ac6eb2fd5bdbdd7797ef5`
- Archive delta: `export.r2x` + compatibility DLL only; all other members byte-identical to S1.42AF.
- Final neighbor evidence: deliberate last-run MouthDog/non-Pikmin test included MouthDogs and a Redwood Titan followed by normal Redwood Titan death. Exact V81 source plus the S1.42AH type gate prove non-Pikmin `EnemyAI` pass-through through `MouthDogAI.OnCollideWithEnemy` -> `HitEnemy(2)`; the death line itself does not encode attacker identity.
- Status: **accepted predecessor / rollback provenance for S1.42AI**.

### S1.42AI — accepted BCMER ShyGuy interior-only baseline

- Parent: accepted S1.42AH.
- Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
- SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
- Candidate: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`
- Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`
- Project status: `Current/Projektstatus_S1.42AI_ACCEPTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`
- Runtime log SHA-256: `1765a2b65cfa31da049ba415938119f9eb3690d09618a2f85a32209bfad6d9b5`
- Build workflow run: `34496960816`
- Build commit: `2dea753ec48ea2a8f417491ae9a13cf7a6d7b8b9`
- Static evidence: `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`
- Full-normal result: exact BCMER `1.71.0` loaded; ShyGuy event executed; the intended interior route remained active; BCMER logged `Adding 0 ShyGuy into list.`; no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker occurred; no new project regression failure was attributable to the isolated config delta.
- Status: **accepted full normal stack / current safe gameplay base**.

## Feature/fix lookup

| Feature / decision | Established by |
|---|---|
| CodeRebirthLib removed; DawnLib ownership | S1.39 |
| CodeRebirth utility-kill Pikmin protection | S1.39A |
| Native Currency/Flash-Turret control | S1.40B |
| BCMER 1.71.0 full-stack activation/guards | S1.41 |
| Interior package expansion/restrictions | S1.42A |
| Normal enemy-spawn restore baseline | S1.42C |
| Thumper Bite Limit 3 / Crawler attack allowed / Puffer protection | S1.42I |
| Lifecycle-safe Baboon Hawk prevention-before-mutation architecture | S1.42S |
| Full-normal restoration after diagnostics | S1.42T |
| Equal BCMER static EventType scale concept | S1.42U, later re-applied and accepted in S1.42AC |
| Final accepted Jetpack 18 + Pikmin/Microwave/Snail values | S1.42Z |
| Transactional CodeRebirth ACU/G.R.E.G. 18-curve ×0.5 scaling | S1.42Z |
| Config-only interior equalization proven insufficient | S1.42AA rejection |
| Post-viability interior rarity normalization to 100 | S1.42AB |
| Exact BCMER per-event-weight semantic correction | `Current/109...` analysis |
| Equal BCMER static EventType probability accepted | S1.42AC / `Current/118...` |
| Functional Microwave half-frequency target accepted | S1.42AF / `Current/128...` |
| Functional Microwave 0-Interior provider assumption disproved | S1.42AD runtime rejection |
| Functional Microwave corrected 18 Moon / 18 Interior contract | S1.42AE source, runtime-proved and accepted in S1.42AF |
| Functional Microwave path-length-safe packaging | S1.42AF |
| Mouth Dog LethalMin bite/grab/death-timer path prevention partial fix | S1.42AG rejection evidence / `Current/134...` |
| Mouth Dog dual Pikmin prevention with native reverse and non-Pikmin neighbor behavior preserved | S1.42AH / `Current/142...` |
| ShyGuy isolation diagnostic owner-type resolution repair, runtime-proved but later complex-owner failure | S1.42AI-DIAG1R1 / `Current/147...` |
| ShyGuy exact-identity/isolation diagnostic completed; exterior visibility not exercised | S1.42AI-DIAG1R3 / `Current/151...` |
| BCMER ShyGuy interior-only event correction accepted | S1.42AI / `Current/152...` |

## Parentage rules that matter

- S1.42C is the restore baseline after S1.42B's diagnostic divergence.
- S1.42S is the accepted recovery architecture after the rejected broad Baboon approaches.
- S1.42AB was built **directly from accepted S1.42Z**, not from rejected S1.42AA.
- S1.42AC was built **directly from accepted S1.42AB**. Its original rejection remains historical evidence, `Current/109` corrected the per-event-weight interpretation, and `Current/118` is the explicit later acceptance decision.
- S1.42AD was built **directly from accepted S1.42AC** and is rejected. It must not be used as a successor build base.
- S1.42AE was built **directly from accepted S1.42AC**, not from rejected S1.42AD. Its provider code was never reached during the preloader failures; it is superseded for packaging/path-length reasons and is not a safe gameplay base.
- S1.42AF was built **directly from accepted S1.42AC**, not from S1.42AE. It reuses the S1.42AE functional source under a path-length-safe Gale profile identity and remains an accepted predecessor in the current line.
- S1.42AG was built **directly from accepted S1.42AF**. Its `DoCheckInterval()` guard is a proven partial fix, but the build is runtime-rejected because a remaining targeting/attack path still allowed a Mouth Dog to select/attack a scrap-carrying Purple Pikmin. Do not use S1.42AG as a gameplay base.
- S1.42AH was built **directly from accepted S1.42AF**, not from rejected S1.42AG. Targeted runtime coverage plus the final non-Pikmin neighbor pass are explicitly accepted in `Current/142...`; it is the accepted predecessor and rollback provenance baseline for S1.42AI.
- S1.42AI was built **directly from accepted S1.42AH**. `Current/152...` explicitly accepts the BCMER ShyGuy interior-only correction; it is the accepted predecessor/rollback provenance baseline for S1.42AK.
- S1.42AI-DIAG1 has an explicit failed diagnostic runtime decision in `Current/145...`; it must not be rerun unchanged or treated as an active runtime candidate.
- S1.42AI-DIAG1R1 was built **directly from S1.42AI**, not from the failed S1.42AI-DIAG1 profile bytes. `Current/147...` records its explicit runtime diagnostic failure after the owner type-resolution repair succeeded but `ElevatorMod.Patches.EndlessElevator` was absent. It is not an active runtime candidate or safe gameplay base; do not rerun it unchanged.
- S1.42AI-DIAG1R3 was built **directly from exact S1.42AI** and passed exact ShyGuy identity/isolation; it remains diagnostic evidence only and is not a gameplay base.

- S1.42AK was built **directly from exact S1.42AJ**, never from DIAG1/DIAG2. `Current/158...` explicitly accepts the full-normal S1.42AK gate; its lack of a hostile indoor sighting in roughly three minutes of Spooky Manor coverage is preserved as a coverage limitation, not a proven spawn regression.

When an exact artifact/hash/status is not indexed here or in `Current/BUILD_LINEAGE.json`, open the linked build-specific record rather than inferring it from build-name order.