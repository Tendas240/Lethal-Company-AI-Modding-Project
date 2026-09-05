# S1.42AE CodeRebirth Functional Microwave Spawn Tuning

> **STATUS: CORRECTED SUCCESSOR CONTRACT — READY FOR REPOSITORY-NATIVE BUILD.**

S1.42AE is the corrected successor to runtime-rejected S1.42AD. The gameplay target is unchanged: Functional Microwaves should be encountered approximately half as often by scaling the effective spawn-weight curve amplitude with `SpawnScale = 0.5f`.

## Frozen owner contract

- CodeRebirth `1.6.9`
- DawnLib `0.9.25`
- DawnLib.Dusk `0.9.25`
- exact key `code_rebirth:functional_microwave`
- exactly one `Dusk.MapObjectSpawnMechanics`
- `PrioritiseMoons == true`
- exactly 18 Moon/tag curves
- exactly 18 Interior/tag curves

The S1.42AD assumption `InteriorCurves=0` was rejected by runtime evidence. Follow-up source/provenance analysis identified the April 9 CodeRebirth asset revision `eb4d5148047c625076b4735784a7ca2477ef17b6`, which adds the exact 18 Interior entries later observed at runtime. A later CodeRebirth bundle rebuild means this state is relevant to shipped 1.6.9; the previous April-6-last-bundle assumption was wrong.

## Dusk 0.9.25 selection semantics

With `PrioritiseMoons=true`, Dusk evaluates the provider in this order:

1. exact Moon key;
2. exact Interior key as fallback;
3. matching Moon tags;
4. otherwise zero.

Moon and Interior curves are not combined. Interior tags are not an additional tag fallback in this mode.

Therefore S1.42AE validates both tables but mutates only `CurvesByMoonOrTagName`. Scaling all Moon/tag curves by 0.5 also scales any averaged Moon-tag fallback result by 0.5 while preserving relative distribution.

## Expected Moon/tag keys — 18

- `lethal_company:vanilla`
- `lethal_company:custom`
- `code_rebirth:oxyde`
- `code_rebirth:functional_microwave_none`
- `code_rebirth:functional_microwave_low`
- `code_rebirth:functional_microwave_medium`
- `code_rebirth:functional_microwave_high`
- `lethal_company:experimentation`
- `lethal_company:vow`
- `lethal_company:march`
- `lethal_company:assurance`
- `lethal_company:offense`
- `lethal_company:adamance`
- `lethal_company:embrion`
- `lethal_company:rend`
- `lethal_company:dine`
- `lethal_company:titan`
- `lethal_company:artifice`

## Expected Interior/tag table — 18 validation-only entries

- `lethal_company:vanilla`
- `lethal_company:custom`
- `lethal_company:experimentation`
- `lethal_company:vow`
- `lethal_company:march`
- `lethal_company:assurance`
- `lethal_company:offense`
- `lethal_company:adamance`
- `lethal_company:embrion`
- `lethal_company:rend`
- `lethal_company:dine`
- `lethal_company:titan`
- `lethal_company:artifice`
- `code_rebirth:functional_microwave_none`
- `code_rebirth:functional_microwave_low`
- `code_rebirth:functional_microwave_medium`
- `code_rebirth:functional_microwave_high`
- `code_rebirth:functional_microwave_ultra_high`

`code_rebirth:oxyde` is not in the Interior table. `code_rebirth:functional_microwave_ultra_high` is in the Interior table but not in the Moon table.

## Fail-closed mutation contract

The plugin validates exact dependency versions, frozen MapObjects registry, exact map-object key, exact one-provider structure, `PrioritiseMoons=true`, both exact 18-key sets, and non-null/non-empty curves in both tables. It logs both tables before mutation. Any drift causes an error and no mutation.

Only after every check passes does it scale Moon/tag keyframe values and tangents by `0.5`. It does not mutate Interior curves, keyframe times or weights, any other map object, configs, networking, saves, or Functional Microwave behavior.

## Runtime acceptance markers

Required:

- dependency versions validated;
- armed/freeze lifecycle marker;
- `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`;
- logged Moon and Interior keysets;
- final marker that 18 Moon/tag curves were scaled by `0.5` while 18 Interior curves were validation-only;
- no S1.42AE refusal/error marker;
- healthy startup, round generation and ordinary gameplay.

The deterministic mutation is the primary evidence for the 50% target; a short gameplay sample is not expected to statistically prove a 50% observed occurrence rate.

## Rollback

Removing `BepInEx/plugins/S142AECodeRebirthMicrowaveSpawnTuning/S142AECodeRebirthMicrowaveSpawnTuning.dll` restores native CodeRebirth/DawnLib behavior.
