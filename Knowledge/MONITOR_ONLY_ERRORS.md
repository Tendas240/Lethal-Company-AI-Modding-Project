# Monitor-Only Warnings and Error Classes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current triage policy for known non-blocking runtime noise  
**Canonical-For:** `monitor_only_errors`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`  
**Related:** `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`  
**Last-Validated:** 2026-09-06

## Triage rule

Do not patch a recurring log signature merely because it is Error-severity. Reopen a monitor-only class only when there is stronger reproducibility, a user-facing symptom, a changed frequency/source correlated with a candidate delta, or direct evidence that it blocks required behavior.

## Current accepted-run monitor classes

The accepted S1.42AF run retained the loaforcsSoundAPI / HarmonyX `TypeLoadException` during `RoundManager.GenerateNewFloor` that was already present in accepted S1.42AC evidence. S1.42AF nevertheless passed normal preloader/chainloader/game startup, required generation and its isolated Microwave contract; the inherited signature therefore remains monitor-only for that accepted scope.

Earlier accepted S1.42Z and S1.42AB runs also contained non-fatal Error-severity noise while their project-local runtime gates passed. Known classes include:

- loaforcsSoundAPI / HarmonyX `TypeLoadException` during `RoundManager.GenerateNewFloor`;
- SoftMask / SoftMasking setup `NullReferenceException` warnings.

Neither the accepted project-local S1.42Z tuning plugin, S1.42AB interior-normalization plugin, nor the accepted S1.42AF Microwave plugin produced a project-local fatal/error marker that invalidated its gate.

## Other historical warnings that are not automatic blockers

Historical technical evidence also classifies the following as monitor-first unless user-facing behavior proves impact:

- SellMyScrap `ShipInventoryUpdated` warnings;
- InjectionLibrary Mirage/Opus native scan noise;
- CodeRebirth Weather Registry unavailable compatibility warning;
- NavMeshInCompany NodeHelper warnings when Company navigation itself is not observed broken;
- isolated content missing-script/setup warnings that do not block required gameplay.

## What is not monitor-only

Do not use this topic to dismiss project-critical regression markers. Examples that must remain explicit gates when relevant include:

- `Work state with no task assigned!` when correlated with a proven harmful interaction/lifecycle mutation;
- `Leader is null when following`;
- Compatibility Fixes Error markers;
- repeated `NetworkObjectReference can only be created from spawned NetworkObjects` when introduced by a candidate;
- repeated `PikminNoticeZone.OnTriggerStay` regression signatures;
- Fatal errors;
- startup termination, periodic freezes or deterministic gameplay breakage.

The S1.42AF run's Mouth Dog / Eyeless Dog -> Pikmin bite/grab sequence is specifically **not** absorbed into monitor-only noise: it is the separate baseline-resident compatibility finding in `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md` and `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`.

Known Black Mesa/interior/Pikmin route errors likewise have their own unresolved evidence topic rather than being globally declared harmless. See `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`.
