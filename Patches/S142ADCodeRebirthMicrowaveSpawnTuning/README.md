# S1.42AD CodeRebirth Functional Microwave Spawn Tuning

Project-local narrow runtime tuner for CodeRebirth's Functional Microwave inside hazard.

## Purpose

Reduce Functional Microwave occurrence by 50% while preserving CodeRebirth's relative Moon/tag distribution and without changing other inside hazards.

Exact DawnLib key:

`code_rebirth:functional_microwave`

Expected owner versions:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- DawnLib.Dusk `0.9.25`.

## Exact mutation

After DawnLib's Moon-registry freeze/rebuild:

1. require the MapObjects registry to be frozen;
2. resolve exactly `code_rebirth:functional_microwave`;
3. require an InsideInfo provider table;
4. require exactly one `Dusk.MapObjectSpawnMechanics` provider;
5. require the frozen 19-key microwave curve set;
6. multiply every microwave keyframe value, incoming tangent and outgoing tangent by `0.5`;
7. leave keyframe time and weights unchanged;
8. modify no other map-object provider.

Scaling values and tangents together preserves each curve's shape at half amplitude.

## Expected curve-key contract

- `lethal_company:vanilla`
- `lethal_company:custom`
- `code_rebirth:oxyde`
- `code_rebirth:functional_microwave_none`
- `code_rebirth:functional_microwave_low`
- `code_rebirth:functional_microwave_medium`
- `code_rebirth:functional_microwave_high`
- `code_rebirth:functional_microwave_ultra_high`
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

Any version/key/provider/curve-set drift causes a fail-closed refusal instead of a guessed fallback.

## Runtime acceptance

The log must show:

- exact dependency versions validated;
- plugin armed before Moon freeze;
- final marker confirming all 19 microwave curves were scaled by `0.5`;
- no contract-refusal/error marker;
- normal round generation without a new fatal regression.

A short runtime sample cannot statistically prove an exact 50% occurrence reduction. The deterministic provider mutation plus clean runtime behavior is the primary acceptance evidence.

## Rollback

Remove `BepInEx/plugins/S142ADCodeRebirthMicrowaveSpawnTuning/S142ADCodeRebirthMicrowaveSpawnTuning.dll`. CodeRebirth/DawnLib then use their native Functional Microwave curves unchanged.
