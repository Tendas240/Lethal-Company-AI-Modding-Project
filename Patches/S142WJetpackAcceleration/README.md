# S1.42W Jetpack Acceleration Patch

Purpose: replace only the proven ButteRyBalance-owned local-player base Jetpack acceleration value immediately before the original `JetpackItem.Update()` body consumes it.

## Frozen behavior

- target: exact declared parameterless `void JetpackItem.Update()`;
- Harmony Prefix;
- ordered after `butterystancakes.lethalcompany.butterybalance`;
- `Priority.Last`;
- local-player only;
- expected owner-written baseline: `10f`;
- S1.42W target: `16f`;
- every non-10 value is untouched.

## Fail-closed dependency contract

The patch refuses to arm unless:

- ButteRyBalance = `0.7.0`;
- JetpackFixes = `1.6.3`;
- More Ship Upgrades, when present, = `3.14.1`;
- ButteRyBalance owns a prefix on the exact target;
- JetpackFixes owns a transpiler on the exact target;
- More Ship Upgrades owns a transpiler there when loaded;
- post-patch verification sees this plugin's prefix.

No fallback method scan, original-method skip, broad base-class patch, RPC, network state, save state or extra IL transpiler is introduced.

## Preserved behavior

- ButteRyBalance `Control Scheme = V49`;
- ButteRyBalance `Warmup Period = false`;
- V49 inertia/directional handling;
- deceleration;
- JetpackFixes collision/death/control fixes;
- `MidAirExplosions = Off`;
- maximum-speed/power remains owned separately;
- battery and item price are untouched;
- More Ship Upgrades Jet Fuel remains a separate percentage acceleration layer;
- More Ship Upgrades Jetpack Thrusters remains the separate maximum-speed/power layer.

## Why S1.42W is a separate project

S1.42V runtime proved the `10 -> 12` patch loads, validates all expected owners and arms correctly. The user rejected only the tuning magnitude. Keeping S1.42V source unchanged preserves exact historical reproducibility while S1.42W raises only the target value to 16.

## Runtime gate

The next runtime log must contain:

- `Loading [S1.42W Jetpack Acceleration 1.0.0]`;
- successful validation of ButteRyBalance 0.7.0, JetpackFixes 1.6.3 and More Ship Upgrades 3.14.1;
- `S1.42W Jetpack acceleration patch armed`;
- no Harmony target/owner/order exception.

Gameplay validation must cover fast lift-off, repeated flights, release/deactivation, safe landing, hard collision/high-speed ground touch, V49 handling, and absence of random mid-air explosion/state accumulation.
