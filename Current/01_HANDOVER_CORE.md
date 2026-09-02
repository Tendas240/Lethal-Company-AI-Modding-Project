# 01 — Handover Core

## Binding state

- Canonical candidate: **S1.40**
- Profile: `Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z`
- Latest runtime-tested reference: **S1.39**
- S1.40 status: archive/config verified, not runtime-accepted
- S1.39 status: runtime-tested; currency cleanup failed

## Critical lineage

S1.36 established the clean cumulative baseline and runtime-accepted ship-door failsafe, complete EnemyScan output and CodeRebirth microwave/Pikmin protection.

S1.37 added natural CodeRebirth currency scrap filtering.

S1.38 added 2560x1440 FixCameraResolution and Old-Bird-only Lethal Resonance configuration. Mirage retention was only confirmed after manual setting in Main Menu/LethalConfig.

S1.39 added broader currency/map-object filtering, Flash Turret defensive filtering, Ogopogo/Vermin disablement and a direct CodeRebirth utility-kill shield for Pikmin/Puffmin. The plugin loaded in the real test, but Coins and Wallets still spawned. Therefore the late map-object filtering approach is confirmed insufficient for DawnLib-native currency map objects.

S1.40 keeps the S1.39 DLL unchanged and moves the cleanup to the actual owner: CodeRebirth/DawnLib generated map-object configuration.

## S1.40 native CodeRebirth/DawnLib overrides

Profile member: `BepInEx/config/CodeRebirth.cfg`

```ini
[Merchant Options]

Coin | Inside Moon Spawn Weights =
Coin | Inside Interior Spawn Weights =
Crisp Dollar Bill | Inside Moon Spawn Weights =
Crisp Dollar Bill | Inside Interior Spawn Weights =
Wallet | Inside Moon Spawn Weights =
Wallet | Inside Interior Spawn Weights =

[FlashTurret Options]

Flash Turret | Is Inside Hazard = false
Flash Turret | Inside Moon Spawn Weights =
Flash Turret | Inside Interior Spawn Weights =
```

Intent: remove only natural inside generation. Do not intentionally remove CodeRebirth currency registration or merchant/denomination/vending/enemy-drop mechanics.

## Import rule

S1.40 still embeds `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`.

Gale import must use **Advanced options -> Import all files**.

Expected runtime marker: `S1.39 Compatibility Fixes loaded.`

## Persistent rules

- S1.29D is diagnostic only and never a gameplay base.
- Malfunctions stays disabled until explicitly re-enabled by the user.
- ProjectSCP-SCP999 stays disabled.
- BCMER stays disabled until after S1.40 acceptance, then only isolated re-audit.
- AJB ship-door mod stays disabled while the local failsafe exists.
- CodeRebirthLib is not to be installed.
- Preserve the 26-interior equal-Weight100 architecture unless new runtime evidence requires change.
- Unknown enemy PowerLevels must not be guessed.
- Do not re-run failed late-filter currency approaches without new evidence.

## Next acceptance gate

S1.40 is accepted only after a real run confirms natural Coin/Wallet/Bill absence and no natural Flash Turret. The full runtime log must be preserved.
