# S1.42V Jetpack Acceleration

Project-local, single-purpose candidate patch for the S1.42V balance stage.

## Frozen behavior

- exact target: `JetpackItem.Update()`;
- exact field: `JetpackItem.jetpackAcceleration`;
- proven S1.42U base value under ButteRyBalance v0.7.0, `Control Scheme = V49`, `Warmup Period = false`: `10f`;
- S1.42V target: `12f` (+20%);
- local player only, mirroring ButteRyBalance ownership;
- prefix ordered after Harmony owner `butterystancakes.lethalcompany.butterybalance`;
- replacement occurs only when the field is still approximately `10f`;
- any non-10 value is preserved.

## Explicit non-scope

This patch does not change:

- ButteRyBalance `Control Scheme = V49`;
- `jetpackForceChangeSpeed` / inertia handling;
- `jetpackDeaccelleration`;
- Jetpack maximum power or maximum-speed logic;
- Jetpack battery or price;
- JetpackFixes `MidAirExplosions` or its collision/death fixes;
- More Ship Upgrades `Jet Fuel` or `Jetpack Thrusters` configuration.

More Ship Upgrades 3.14.1 reads `jetpackAcceleration` inside the original `JetpackItem.Update()` and applies the purchased Jet Fuel percentage there. Therefore the purchase-gated upgrade remains a separate multiplicative layer on top of the new 12f base instead of being repurposed as the always-on buff.

## Fail-closed validation

Before applying its Harmony prefix, the plugin requires/validates:

- ButteRyBalance exactly `0.7.0`;
- JetpackFixes exactly `1.6.3`;
- More Ship Upgrades exactly `3.14.1` when present;
- an exact declared `void JetpackItem.Update()` target;
- the expected ButteRyBalance prefix owner on that target;
- the expected JetpackFixes transpiler owner on that target;
- the expected More Ship Upgrades transpiler owner when that plugin is loaded.

If any frozen assumption is false, the plugin logs an error and does not arm. There is deliberately no broad method scan, fallback target, IL rewrite, original-method skip, or ownership replacement.

## Patch Safety Review summary

The original `JetpackItem.Update()` owns many secondary responsibilities including movement, collision/death handling and state transitions. For that reason this project does not replace or skip the original method and does not add another transpiler. It only changes one already-owned input field immediately before the original body executes.

ButteRyBalance is the current writer of the base acceleration. Its v0.7.0 prefix writes 10f each local-player frame under the frozen V49/no-warmup configuration. The project prefix runs after that owner and changes only that exact value to 12f.

JetpackFixes patches the same original method but does not write `jetpackAcceleration`; its 50u/s+ collision/death safety semantics remain in place. The +20% acceleration can make high velocity arrive sooner, so runtime acceptance must explicitly cover takeoff, handling, deactivation, safe landing, hard collision, high-speed ground touch and repeated flights.

Network scope is unchanged: the mutation mirrors ButteRyBalance's local-player gate and introduces no RPC, NetworkVariable or host-authoritative state.

Rollback is removal of `BepInEx/plugins/S142VJetpackAcceleration/S142VJetpackAcceleration.dll` from the candidate profile. No existing mod DLL is modified.

## Runtime acceptance

The candidate remains unaccepted until a fresh complete runtime log and gameplay check verify at minimum:

1. startup/main menu succeeds and this plugin logs that it armed;
2. exact dependency versions/owners validate without Harmony exceptions;
3. base Jetpack acceleration is modestly higher while V49 handling remains intact;
4. no unintended maximum-speed change;
5. JetpackFixes collision/death behavior has no new regression or random mid-air explosion;
6. release/deactivation, safe landing, hard collision and repeated flights remain sane;
7. More Ship Upgrades Jet Fuel, if purchased/tested, remains a separate percentage layer;
8. no unrelated BCMER/enemy/Pikmin compatibility regression is introduced.

See `BuildSpecs/S1.42V_PLAN.md` and `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` for the full build/runtime gate.
