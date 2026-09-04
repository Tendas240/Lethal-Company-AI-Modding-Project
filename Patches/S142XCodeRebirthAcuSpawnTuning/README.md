# S1.42X CodeRebirth ACU Spawn Tuning

Project-local narrow runtime tuner for CodeRebirth's Air Control Unit (the in-game Aerial Defense System).

## Purpose

Reduce Air Control Unit occurrence by 50% while preserving CodeRebirth's relative Moon/tag distribution and without globally changing other outside hazards.

Exact DawnLib key:

`code_rebirth:air_control_unit`

Expected owner versions:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- DawnLib.Dusk `0.9.25`.

## Why a provider tuner is used

CodeRebirth defines the ACU as a Dusk outside map object. Its spawn counts are driven by `MapObjectSpawnMechanics` animation curves which DawnLib evaluates in its outside-map-object spawning path.

The project therefore does not patch `RoundManager.SpawnOutsideHazards`, does not modify every outside hazard and does not rewrite CodeRebirth's asset bundle. Instead it finds only the final DawnLib provider belonging to `code_rebirth:air_control_unit` and scales that provider's registered Moon/tag curves.

## Exact mutation

After DawnLib's Moon-registry freeze/rebuild:

1. require the MapObjects registry to be frozen;
2. resolve exactly `code_rebirth:air_control_unit`;
3. require an OutsideInfo provider table;
4. require exactly one `Dusk.MapObjectSpawnMechanics` provider;
5. require the exact frozen 18-key ACU curve set;
6. multiply every ACU keyframe value, incoming tangent and outgoing tangent by `0.5`;
7. leave keyframe time and weights unchanged;
8. modify no other map-object provider.

Scaling values and tangents together preserves each curve's shape at half amplitude.

## Expected curve-key contract

- `lethal_company:vanilla`
- `lethal_company:custom`
- `code_rebirth:oxyde`
- `code_rebirth:air_control_unit_none`
- `code_rebirth:air_control_unit_low`
- `code_rebirth:air_control_unit_medium`
- `code_rebirth:air_control_unit_high`
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

## Patch Safety Review

Exact owner:

- CodeRebirth/Dusk owns the ACU definition;
- DawnLib owns its final `DawnOutsideMapObjectInfo.SpawnWeights` provider table and outside-spawn evaluation.

Smallest safe surface:

- one exact map-object key;
- one exact `MapObjectSpawnMechanics` provider;
- no Harmony patch;
- no global RoundManager interception;
- no prefab lifecycle mutation;
- no NetworkObject/RPC/state/save mutation;
- no other hazard curve mutation.

Lifecycle/order:

CodeRebirth is a hard dependency, so its Dusk registration occurs before this plugin. DawnLib's `MapObjectSpawnMechanics` refreshes its Moon curves during `LethalContent.Moons.OnFreeze`; this plugin subscribes afterwards and scales only the final rebuilt ACU curves.

Forbidden broader alternatives:

- do not halve all outside hazard spawning;
- do not patch the complete `SpawnOutsideHazards` loop just for ACU rarity;
- do not edit or replace CodeRebirth's asset bundle;
- do not guess a fallback map-object key/provider.

## Runtime acceptance

The log must show:

- exact dependency versions validated;
- plugin armed before Moon freeze;
- final marker confirming all 18 ACU curves were scaled by `0.5`;
- no contract-refusal/error marker.

Occurrence in a small runtime sample is not statistical proof of an exact 50% spawn reduction. The deterministic provider mutation plus clean runtime behavior is the primary acceptance evidence.

## Rollback

Remove `BepInEx/plugins/S142XCodeRebirthAcuSpawnTuning/S142XCodeRebirthAcuSpawnTuning.dll`. CodeRebirth/DawnLib then use their native ACU curves unchanged.
