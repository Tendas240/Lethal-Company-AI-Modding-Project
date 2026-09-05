# S1.42AD CodeRebirth Functional Microwave Spawn Tuning

> **STATUS: UNBUILT IMPLEMENTATION DRAFT — NOT AN ACCEPTED BUILD CONTRACT.**
> The current source draft uses `SpawnScale = 0.5f` as a proposed value. Current canonical project authorities require the Functional Microwave to become rarer but do not yet authorize an exact reduction percentage. Resolve the target magnitude and complete the mandatory Patch Safety Review before arming/building S1.42AD. Recovery authority: `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`.

Project-local narrow runtime tuner draft for CodeRebirth's Functional Microwave inside hazard.

## Intended purpose

Reduce Functional Microwave occurrence while preserving CodeRebirth's relative Moon/tag distribution and without changing other inside hazards.

The **current draft proposal** is a 50% amplitude reduction. That value is not yet an accepted user target.

Exact DawnLib key:

`code_rebirth:functional_microwave`

Expected owner versions:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- DawnLib.Dusk `0.9.25`.

## Draft mutation

If the final approved target remains `0.5`, the draft intends to run after DawnLib's Moon-registry freeze/rebuild and:

1. require the MapObjects registry to be frozen;
2. resolve exactly `code_rebirth:functional_microwave`;
3. require an InsideInfo provider table;
4. require exactly one `Dusk.MapObjectSpawnMechanics` provider;
5. require the frozen 19-key microwave curve set;
6. multiply every microwave keyframe value, incoming tangent and outgoing tangent by `0.5`;
7. leave keyframe time and weights unchanged;
8. modify no other map-object provider.

Scaling values and tangents together preserves each curve's shape at half amplitude.

Do not treat the value `0.5` as final until the exact target magnitude is confirmed and recorded in the S1.42AD build plan.

## Expected curve-key draft contract

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

Any version/key/provider/curve-set drift should cause a fail-closed refusal instead of a guessed fallback.

This 19-key list still requires an explicit independent ownership/provenance review before the build is armed.

## Required pre-build gate

Before this draft may become a candidate:

- resolve the exact requested spawn reduction magnitude;
- independently confirm the exact CodeRebirth/DawnLib ownership and provider/key contract;
- complete the Patch Safety Review required by `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
- compile cleanly in the repository build environment;
- record the resulting DLL SHA-256;
- prove the candidate profile diff is limited to the intended DLL/build metadata;
- keep S1.42AC as the guarded base until a later explicit promotion.

## Runtime acceptance after a candidate exists

The log must show:

- exact dependency versions validated;
- plugin armed before Moon freeze;
- final marker confirming the approved Microwave curve scale was applied to all expected curves;
- no contract-refusal/error marker;
- normal round generation without a new fatal regression.

A short runtime sample cannot statistically prove an exact occurrence reduction. The deterministic provider mutation plus clean runtime behavior is the primary acceptance evidence.

## Rollback

If this plugin is eventually built into a candidate, removing `BepInEx/plugins/S142ADCodeRebirthMicrowaveSpawnTuning/S142ADCodeRebirthMicrowaveSpawnTuning.dll` restores CodeRebirth/DawnLib native Functional Microwave curves.

At the current repository state no S1.42AD profile contains this DLL yet, so no runtime rollback is presently required.
