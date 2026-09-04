# S1.42X Jetpack Acceleration

Project-local diagnostic tuning plugin for the S1.42X candidate.

## Purpose

S1.42W proved that the existing narrow Jetpack patch path loads and runs, but the `10 -> 16` base-acceleration target was not perceptibly different enough during straight-up lift-off.

S1.42X therefore performs an intentionally large diagnostic step:

`jetpackAcceleration 10f -> 32f`

This is not assumed to be the final balanced value. If straight-up lift-off still does not change clearly at 32f, the project must stop increasing this field and identify the actual vertical force/ramp owner instead.

## Exact interception

- target: declared parameterless `void JetpackItem.Update()`;
- Harmony Prefix;
- local player only;
- ordered after ButteRyBalance with `HarmonyAfter` and `Priority.Last`;
- replaces only an approximately-`10f` value written by the frozen ButteRyBalance V49/no-warmup path;
- all other values are left untouched.

## Fail-closed contract

Required/validated:

- ButteRyBalance `0.7.0`;
- JetpackFixes `1.6.3`;
- More Ship Upgrades `3.14.1` when present;
- expected ButteRyBalance Prefix owner on `JetpackItem.Update()`;
- expected JetpackFixes Transpiler owner;
- expected More Ship Upgrades Transpiler owner when loaded;
- exact target signature;
- post-patch verification that this plugin owns an installed Prefix.

Any contract drift prevents the plugin from arming.

## Patch Safety Review

Smallest safe surface:

- no original method skip;
- no replacement of the Jetpack lifecycle;
- no additional IL transpiler;
- no network/RPC/save-state mutation;
- no battery/price change;
- no maximum-power/speed mutation in the custom DLL;
- no change to ButteRyBalance V49 inertia/deceleration;
- no change to JetpackFixes collision/death logic.

Known adjacent risk:

32f reaches dangerous velocity much sooner. Runtime validation must therefore cover repeated takeoff, release/deactivation, ordinary landing, hard/high-speed ground contact, directional handling and any JetpackFixes explosion/death behavior.

Forbidden broader alternative:

Do not disable ButteRyBalance or JetpackFixes, skip `JetpackItem.Update()`, or replace the complete Jetpack force/control lifecycle just to increase lift-off.

## Runtime acceptance

The log must prove:

- this exact plugin loads;
- dependency/version/owner validation succeeds;
- it logs the `10 -> 32` armed marker;
- no Harmony target/ordering/transpiler exception appears.

Gameplay must establish whether straight-up lift-off is now clearly faster. If not, `jetpackAcceleration` is no longer the tuning path to pursue.

## Rollback

Remove `BepInEx/plugins/S142XJetpackAcceleration/S142XJetpackAcceleration.dll` and restore the previous candidate/config state. The accepted rollback baseline remains S1.42U.
