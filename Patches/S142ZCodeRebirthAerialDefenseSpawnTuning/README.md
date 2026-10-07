# S1.42Z CodeRebirth Aerial Defense Spawn Tuning

Project-local spawn-weight tuning for both CodeRebirth aerial-defense systems in S1.42Z.

## Exact targets

1. `code_rebirth:air_control_unit` — Air Control Unit / Aerial Defense System;
2. `code_rebirth:gunslinger_greg` — G.R.E.G. / Advanced Airspace Control.

## Behavior

- validates CodeRebirth `1.6.9`;
- validates DawnLib and DawnLib.Dusk `0.9.25`;
- waits for DawnLib's Moon-registry freeze/rebuild;
- requires frozen MapObjects registry;
- resolves both exact CodeRebirth map-object keys;
- requires exactly one `Dusk.MapObjectSpawnMechanics` provider per target;
- requires the exact frozen 18-key curve contract for each target;
- validates both targets before changing either one;
- scales every keyframe value, in-tangent and out-tangent by `0.5` for both targets;
- modifies no other map-object provider.

S1.42Y runtime proved this exact two-target architecture and its transactional applied marker. S1.42Z preserves the same behavior under a candidate-specific plugin identity so no historical Y tuning DLL is stacked into the rebuilt profile.

## Patch Safety Review

- exact two map-object keys only;
- no Harmony patch;
- no global outside-hazard spawn-loop modification;
- no prefab, targeting, damage, RPC, networking, save-state or placement-rule mutation;
- both contracts must validate before either target is changed;
- fail closed on dependency/provider/key drift.

Forbidden broader alternative: globally reduce all outside hazards or patch the entire outside map-object spawn loop.

## Probability semantics

The patch halves the native DawnLib animation-curve amplitudes. DawnLib subsequently evaluates and rounds the resulting quantity, so this is an exact 50% curve-weight reduction, not a guarantee that a short observed run contains exactly half as many objects.

## Runtime gate

The log must show:

- plugin load;
- exact CodeRebirth / Dawn / Dusk version validation;
- Air Control Unit provider validated with 18 curves;
- G.R.E.G. provider validated with 18 curves;
- one final transactional marker stating both 18-curve sets were scaled by 0.5;
- no contract-refusal marker.

Rollback: remove this DLL.
