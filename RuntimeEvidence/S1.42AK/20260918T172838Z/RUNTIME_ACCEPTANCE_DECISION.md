# S1.42AK Runtime Acceptance Decision

**Date:** 2026-09-18  
**Decision:** PASS / ACCEPT  
**Build:** `S1.42AK`  
**Profile SHA-256:** `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Raw LogOutput.log SHA-256:** `cc0f0a7a6c6a76ad44266aded11ff9cb2aca21f2623f5fb895d371ad778526b9`

The ingested full-normal evidence satisfies the build-specific gate in `Current/157_S1.42AK_BUILD_CANDIDATE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md` with one explicit coverage qualification.

The uploaded session contains two Offense attempts. The first was aborted by the user shortly after landing and before interior entry. The second naturally selected `Spooky manor`; the player entered at about 17:25:00 and died/exited at about 17:27:59. The user saw no hostile indoor enemy during those roughly three minutes. That observation is retained as limited hostile-indoor coverage rather than interpreted as proof of a spawn regression.

The log proves normal startup/game flow, normal interior normalization/selection, exterior enemy activity, scrap generation/interactions, Men-stalker absence, and zero project-critical regression markers covered by the gate. LC Office was not naturally selected, which the candidate contract explicitly permits because S1.42AJ-DIAG2 already provides the targeted LC Office generation/elevator/camera A/B.

The recurring one-shot `LethalMin.Compats.PiggyMetalDetectorPatch` startup failure is real and is not classified away. It is byte/runtime-lineage-preexisting across the normal S1.42AJ run plus DIAG1 and DIAG2; DIAG2 then exercised LC Office for roughly twelve minutes. No current user-facing metal-detector/Pikmin failure is established. The first attempt also contains a concentrated generation-time RuntimeNavMeshBuilder read-access burst, but that interior was never entered and the burst did not persist into the played Spooky Manor run.

No project-critical regression attributable to the accepted LC Office camera/enemy balance contract is established. S1.42AK is therefore eligible for canonical promotion.

Canonical promotion record: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`.
