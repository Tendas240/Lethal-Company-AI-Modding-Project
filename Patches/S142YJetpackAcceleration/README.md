# S1.42Y Jetpack Acceleration

Project-local tuning layer for the S1.42Y runtime candidate.

## Exact behavior

- target: declared parameterless `JetpackItem.Update()`;
- Harmony Prefix ordered after ButteRyBalance and at `Priority.Last`;
- local player only;
- replaces only the proven ButteRyBalance-owned approximately-`10f` `jetpackAcceleration` baseline;
- target value: `22f`;
- no original-method skip;
- no additional transpiler;
- no max-power/speed, battery, price, inertia, deceleration, RPC, save-state or network ownership mutation.

## Frozen compatibility contract

The plugin refuses to arm unless these exact runtime owners match:

- ButteRyBalance `0.7.0` with its `JetpackItem.Update()` prefix;
- JetpackFixes `1.6.3` with its `JetpackItem.Update()` transpiler;
- More Ship Upgrades `3.14.1` and its `JetpackItem.Update()` transpiler when that mod is loaded.

S1.42X proved the same architecture at `32f`, but the user judged that acceleration far too strong. S1.42Y changes only the project-local target magnitude to `22f`.

## Runtime gate

Confirm:

- plugin loads and logs the `10 -> 22` armed marker;
- straight-up lift-off is clearly stronger than the old 10/16 values but materially calmer than S1.42X 32f;
- V49 directional handling and release behavior remain sane;
- ordinary landing, hard collision and high-speed ground contact remain sane;
- repeated flights do not accumulate state or reintroduce random mid-air explosions;
- More Ship Upgrades Jet Fuel / Thrusters remain separate purchase-gated layers.

Rollback: remove this DLL and revert its candidate config changes.
