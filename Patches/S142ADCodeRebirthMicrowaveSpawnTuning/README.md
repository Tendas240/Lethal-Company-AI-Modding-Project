# S1.42AD CodeRebirth Functional Microwave Spawn Tuning

> **STATUS: FINAL PRE-BUILD CONTRACT — SCALE USER-AUTHORIZED / OWNER CONTRACT VERIFIED.**
> The user explicitly authorized the Functional Microwave to be encountered half as often. S1.42AD therefore uses proportional curve-amplitude scaling with `SpawnScale = 0.5f`. The implementation is fail-closed against the independently verified CodeRebirth 1.6.9 / DawnLib 0.9.25 / Dusk 0.9.25 runtime-provider contract.

Project-local narrow runtime tuner for CodeRebirth's Functional Microwave inside hazard.

## Purpose

Reduce Functional Microwave occurrence by scaling its currently effective spawn-weight curves to 50% amplitude while preserving CodeRebirth's relative Moon/tag distribution and without changing any other inside hazard.

Exact DawnLib key:

`code_rebirth:functional_microwave`

Frozen owner versions:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- DawnLib.Dusk `0.9.25`.

## Verified provenance / owner contract

The independent source review established:

- CodeRebirth registers the exact map-object key `code_rebirth:functional_microwave` through DawnLib/Dusk;
- `DawnMapObjectInfo.InsideInfo.SpawnWeights` is the narrow owner surface;
- Dusk represents the target provider as `MapObjectSpawnMechanics`;
- the shipped/bundle-time Functional Microwave contract predates later Unity-source edits that added unused Interior curves;
- the expected runtime contract for the shipped 1.6.9 bundle is Moon-priority enabled, exactly 18 Moon/tag curves, and zero Interior/tag curves;
- Dusk 0.9.25 exposes `PrioritiseMoons`, `CurvesByMoonOrTagName`, and `CurvesByInteriorOrTagName` directly on `MapObjectSpawnMechanics`.

The later source-only 19-key/Interior-curve state is not accepted as the shipped runtime contract because those changes occurred after the last relevant `coderebirthasset` rebuild.

## Mutation contract

After DawnLib's Moon-registry freeze/rebuild the plugin must:

1. validate exact CodeRebirth/DawnLib/Dusk versions;
2. require the MapObjects registry to be frozen;
3. resolve exactly `code_rebirth:functional_microwave` with InsideInfo;
4. require the expected DawnLib ProviderTable structure;
5. require exactly one `Dusk.MapObjectSpawnMechanics` provider for the target;
6. require `PrioritiseMoons == true`;
7. require exactly zero `CurvesByInteriorOrTagName` entries;
8. require exactly the frozen 18-key `CurvesByMoonOrTagName` set below;
9. require every expected curve to be non-null and non-empty;
10. only then multiply every Microwave Moon/tag keyframe value, incoming tangent and outgoing tangent by `0.5`;
11. leave keyframe time and weights unchanged;
12. modify no other map-object provider.

Scaling values and tangents together preserves each curve's shape at half amplitude.

## Expected 18-key Moon/tag contract

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

`code_rebirth:functional_microwave_ultra_high` is deliberately absent. It belongs to a later Unity-source state that was added after the relevant asset-bundle rebuild and is not part of the verified shipped Moon/tag contract.

Any version/key/provider/priority/Interior-curve/Moon-curve drift causes a fail-closed refusal instead of a guessed fallback.

## Patch Safety Review

### Exact owner / smallest mutation surface

The patch touches only the Functional Microwave's own DawnLib/Dusk inside-spawn `AnimationCurve` provider after the owner registry lifecycle has settled. It does not patch global DawnLib selection, CodeRebirth lifecycle methods, other hazards, networking, saves, or object functionality.

### Lifecycle / secondary responsibilities

The plugin subscribes once to `LethalContent.Moons.OnFreeze` unless the registry is already frozen, validates MapObjects freeze state, validates the exact provider contract, applies once, and otherwise leaves native CodeRebirth/DawnLib spawn evaluation intact.

### State ownership

DawnLib/Dusk remains the owner of spawn evaluation. S1.42AD only performs deterministic proportional amplitude scaling on the exact target provider curves.

### Fail-closed guarantees

Do not:

- globally disable Functional Microwave;
- scale all Inside Hazards;
- globally patch DawnLib map-object selection;
- fall back to similar keys/providers;
- mutate Interior curves when the verified contract expects none;
- reinstall historical `CodeRebirthLib`.

If any exact contract check fails, the plugin logs an error and performs no curve mutation.

### Adjacent behavior preserved

- Functional Microwave remains fully functional when spawned;
- accepted `Functional Microwave | Volume = 0.15` remains unchanged;
- all other CodeRebirth inside/outside hazards remain unchanged;
- accepted S1.42Z ACU/G.R.E.G. tuning remains unchanged;
- all accepted S1.42AC BCMER/interior/enemy/Pikmin/Jetpack behavior remains unchanged.

## Runtime acceptance

The log must show:

- exact dependency versions validated;
- plugin armed on the intended Moon-freeze lifecycle;
- provider marker `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=0`;
- final marker confirming all 18 Microwave Moon/tag curves were scaled by `0.5`;
- no S1.42AD contract-refusal/error marker;
- normal startup and ordinary round generation without a new fatal regression.

A short runtime sample cannot statistically prove an exact observed occurrence ratio. The deterministic provider mutation plus clean adjacent runtime behavior is the primary acceptance evidence.

## Rollback

Removing `BepInEx/plugins/S142ADCodeRebirthMicrowaveSpawnTuning/S142ADCodeRebirthMicrowaveSpawnTuning.dll` restores CodeRebirth/DawnLib native Functional Microwave curves.
