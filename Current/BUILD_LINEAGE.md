# Build Lineage

**Status:** CURRENT / CANONICAL HISTORICAL INDEX  
**Authority:** human build-history router; exact build evidence remains in candidate/acceptance/rejection/runtime records  
**Canonical-For:** `build_lineage`  
**Machine Mirror:** `Current/BUILD_LINEAGE.json`  
**Last-Validated:** 2026-09-09

## Current lineage head

- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** S1.42AH.
- **Active candidate:** none.
- **Runtime test outstanding:** no.
- **Next build:** none armed. The next selected preparation scope is the BCMER ShyGuy interior-only correction under `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.

S1.42AF remains the accepted predecessor/rollback point. S1.42AG remains runtime-rejected partial-fix evidence.

For volatile lifecycle state use `Knowledge/CURRENT_LIFECYCLE.md`. This file is the build-history router; use linked build-specific evidence for exact forensic detail.

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
| S1.42AB | accepted predecessor | Post-viability LLL normalization to Weight 100 while preserving membership/exclusions. |
| S1.42AC | accepted predecessor | Equal BCMER static EventType probability. Historical per-event-equality rejection is retained, but `Current/109` corrected its interpretation and `Current/118` explicitly accepted the artifact. |
| S1.42AD | **rejected** | Functional Microwave half-frequency attempt failed closed on the actual 18-Interior provider contract. |
| S1.42AE | **superseded — path-length blocked, not gameplay-rejected** | Correct provider code was never reached because the nested SoundAPI path measured 262 characters. |
| S1.42AF | **accepted predecessor to AH** | Path-length-safe Microwave packaging; normal startup and exact 18 Moon / 18 Interior Functional Microwave contract accepted. |
| S1.42AG | **runtime rejected / partial fix** | LethalMin MouthDog bite/grab path blocked, but another MouthDog -> Pikmin path remained. |
| S1.42AH | **accepted current baseline** | Dual exact MouthDog/Pikmin prevention with player, reverse-direction Pikmin lifecycle and non-Pikmin EnemyAI neighbor behavior preserved. |

Older chronology and exact historical artifacts remain in `Current/03_PROJECT_CHRONOLOGY.md`, `Current/06_RECENT_WORK_*.md`, build-specific decision records, `Current/BUILD_LINEAGE.json`, `ProfileSources/`, and `RuntimeEvidence/`.

## Current-line artifacts

### S1.42AF — accepted predecessor / rollback point

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Candidate: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Status: accepted predecessor; safe rollback/provenance point.

### S1.42AG — rejected partial MouthDog fix

- Parent: S1.42AF.
- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Runtime: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Status: runtime rejected / partial fix / not a safe gameplay base.

### S1.42AH — accepted MouthDog dual prevention baseline

- Parent: accepted S1.42AF, never rejected S1.42AG.
- Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Partial runtime: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`
- Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
- Project status: `Current/Projektstatus_S1.42AH_ACCEPTED.json`
- Final decisive runtime: `RuntimeEvidence/S1.42AH/20260909T162513Z/`
- Final raw-log SHA-256: `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`
- Build workflow run: `34141360051`
- Build commit: `fdb6b94e34144f860f6ac6eb2fd5bdbdd7797ef5`
- Archive delta from S1.42AF: `export.r2x` + cumulative compatibility DLL only.
- Status: **ACCEPTED FULL NORMAL STACK / current safe gameplay base**.

The final acceptance uses the user's deliberately exercised last-run MouthDog/non-Pikmin neighbor test. The log confirms MouthDogs and a Redwood Titan in that run and normal Redwood Titan death; exact V81 source plus the S1.42AH type gate establish that non-Pikmin `EnemyAI` passes through `MouthDogAI.OnCollideWithEnemy` to native `HitEnemy(2)`. The death line itself does not encode attacker identity, so the acceptance record preserves that evidentiary limit.

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
| Functional Microwave half-frequency/path-safe contract | S1.42AF / `Current/128...` |
| Mouth Dog LethalMin bite/grab/death-timer path partial prevention | S1.42AG rejection evidence / `Current/134...` |
| Mouth Dog dual Pikmin prevention with native neighbor/reverse lifecycle preserved | S1.42AH / `Current/142...` |

## Parentage rules that matter

- S1.42C is the restore baseline after S1.42B's diagnostic divergence.
- S1.42S is the accepted recovery architecture after rejected broad Baboon approaches.
- S1.42AB was built **directly from accepted S1.42Z**, not from rejected S1.42AA.
- S1.42AC was built **directly from accepted S1.42AB**. Its original rejection remains historical evidence, `Current/109` corrected the per-event-weight interpretation, and `Current/118` is the explicit later acceptance decision.
- S1.42AD was built **directly from accepted S1.42AC** and is rejected.
- S1.42AE was built **directly from accepted S1.42AC**, not rejected S1.42AD; it is superseded for packaging/path-length reasons.
- S1.42AF was built **directly from accepted S1.42AC**, not S1.42AE; it is now the accepted predecessor/rollback point.
- S1.42AG was built **directly from accepted S1.42AF** and remains rejected.
- S1.42AH was built **directly from accepted S1.42AF**, not rejected S1.42AG; after targeted runtime coverage and the final non-Pikmin neighbor pass it is explicitly accepted in `Current/142...` as the current full-normal-stack gameplay baseline.

When an exact artifact/hash/status is not indexed here or in `Current/BUILD_LINEAGE.json`, open the linked build-specific record rather than inferring it from build-name order.