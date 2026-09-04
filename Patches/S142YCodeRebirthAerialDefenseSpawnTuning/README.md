# S1.42Y CodeRebirth Aerial Defense Spawn Tuning

Project-local spawn-weight tuning for the two CodeRebirth aerial-defense systems in S1.42Y.

## Exact targets

1. `code_rebirth:air_control_unit` — Air Control Unit / Aerial Defense System;
2. `code_rebirth:gunslinger_greg` — G.R.E.G. / Advanced Airspace Control.

Both are separate DawnLib outside map objects. S1.42X tuned only the Air Control Unit, so G.R.E.G. remained at native spawn weights. S1.42Y closes that scope gap.

## Behavior

- validates CodeRebirth `1.6.9`;
- validates DawnLib and DawnLib.Dusk `0.9.25`;
- waits for DawnLib's Moon-registry freeze/rebuild;
- requires a frozen MapObjects registry;
- resolves each exact CodeRebirth map-object key;
- requires exactly one `Dusk.MapObjectSpawnMechanics` provider per target;
- requires the exact frozen 18-key curve contract for each target;
- validates both targets completely before changing either one;
- scales every keyframe value, in-tangent and out-tangent by `0.5` for both targets;
- modifies no other map-object provider.

## Exact tag contracts

Air Control Unit target-specific tags:

- `code_rebirth:air_control_unit_none`
- `code_rebirth:air_control_unit_low`
- `code_rebirth:air_control_unit_medium`
- `code_rebirth:air_control_unit_high`

G.R.E.G. target-specific tags:

- `code_rebirth:gunslinger_greg_none`
- `code_rebirth:gunslinger_greg_low`
- `code_rebirth:gunslinger_greg_medium`
- `code_rebirth:gunslinger_greg_high`

Both also retain their native moon/common-tag entries such as Vanilla, Custom, Oxyde and the frozen vanilla moon set.

## Safety rationale

This is deliberately narrower than patching `RoundManager.SpawnOutsideHazards` or globally scaling all outside hazards. It does not touch prefab behavior, targeting, damage, RPCs, networking, save state, placement rules or any non-aerial CodeRebirth hazard.

The two-target validation is transactional: any missing provider, dependency mismatch or curve-key drift causes the plugin to apply no spawn scaling at all.

## Important probability note

The patch halves the native DawnLib animation-curve amplitudes. DawnLib later evaluates those curves and rounds the resulting quantity, so this is an exact 50% curve-weight reduction, not a mathematical guarantee that every observed short-run spawn count will be exactly half.

## Runtime gate

The log must show:

- plugin load;
- exact CodeRebirth/Dawn/Dusk version validation;
- both exact provider contracts validated with 18 curves each;
- one final transactional applied marker stating that both ACU and G.R.E.G. were scaled by 0.5;
- no contract-refusal marker.

Runtime should also confirm both systems remain functional and no unrelated outside-hazard behavior regresses.

Rollback: remove this DLL.
