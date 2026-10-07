# S1.42Z Jetpack Acceleration

Project-local Jetpack tuning layer for S1.42Z.

## Exact behavior

- exact declared parameterless `JetpackItem.Update()` target;
- Harmony Prefix ordered after ButteRyBalance at `Priority.Last`;
- local player only;
- replaces only the validated ButteRyBalance-owned approximately-`10f` `jetpackAcceleration` baseline;
- target value: `18f`;
- no original skip;
- no additional transpiler;
- no max-power/speed, battery, price, inertia, deceleration, RPC, save-state or network mutation.

## Frozen compatibility contract

The patch refuses to arm unless these exact runtime owners match:

- ButteRyBalance `0.7.0` and its `JetpackItem.Update()` Prefix;
- JetpackFixes `1.6.3` and its `JetpackItem.Update()` transpiler;
- More Ship Upgrades `3.14.1` and its `JetpackItem.Update()` transpiler when loaded.

S1.42Y runtime proved the same architecture at `22f` with no project-local runtime failure. S1.42Z changes only the project-local acceleration magnitude to the user-requested `18f`.

## Patch Safety Review

- exact owner/call site remains `JetpackItem.Update()`;
- no lifecycle method is skipped or replaced wholesale;
- V49 handling/deceleration ownership remains with ButteRyBalance;
- collision/death/control safety remains with JetpackFixes;
- purchase-gated acceleration remains with More Ship Upgrades;
- no state is persisted or network-synchronized by this patch;
- fail closed on target/version/Harmony-owner drift.

Forbidden broader alternative: disable or replace ButteRyBalance, JetpackFixes, More Ship Upgrades, or the full Jetpack lifecycle merely to change base acceleration.

## Runtime gate

Confirm:

- plugin loads and logs exact `10 -> 18` armed marker;
- straight-up lift-off feels acceptable between prior 16f and rejected 22f/32f targets;
- V49 directional handling, release/deactivation, ordinary landing and repeated flights remain sane;
- hard/high-speed ground contact shows no new JetpackFixes regression;
- Jet Fuel / Thrusters remain separate purchase-gated layers.

Rollback: remove this DLL and revert the candidate config changes.
