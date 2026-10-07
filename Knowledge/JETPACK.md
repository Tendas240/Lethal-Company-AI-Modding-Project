# Jetpack Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted Jetpack tuning and provenance  
**Canonical-For:** `jetpack`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
**Related:** S1.42Z ProfileSources and project-local Jetpack source/build records  
**Last-Validated:** 2026-09-04

## Accepted values

Current accepted full-stack descendants preserve the S1.42Z Jetpack tuning:

- project-local base acceleration: `10f -> 18f`;
- Jet Fuel: `18 / 18`;
- Jetpack Thrusters: `25 / 20`;
- ButteRyBalance V49 handling/deceleration preserved;
- JetpackFixes collision/death/control safety preserved.

S1.42Z runtime explicitly validated the exact project-local acceleration path and accepted the user-facing behavior.

## Provenance

S1.42Z Jetpack DLL:

`BepInEx/plugins/S142ZJetpackAcceleration/S142ZJetpackAcceleration.dll`

SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

Accepted runtime record:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

## Historical safety lesson

Do not patch inherited `GrabbableObject.Start` through `JetpackItem.Start`. The S1.42D attempt resolved an inherited lifecycle target and produced HarmonyX warnings. The later implementation targets the loaded Jetpack Item asset / exact acceleration owner instead.

Any future Jetpack code change must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and must preserve the accepted ButteRyBalance/JetpackFixes ownership unless explicit evidence justifies a change.
