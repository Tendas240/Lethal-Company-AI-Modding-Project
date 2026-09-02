# 01 — Handover Core

## Binding state

- Canonical candidate: **S1.40A**
- Profile: `Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`
- Latest runtime-tested reference: **S1.40**
- S1.40 status: runtime-tested, **failed acceptance**
- S1.40A status: archive/config verified, runtime pending

## Critical lineage

S1.39 proved late RoundManager/SelectableLevel filtering insufficient for DawnLib-native Currency.

S1.40 moved Currency and Flash Turret suppression to `CodeRebirth.cfg`, but runtime testing showed those values were not retained. The post-run config had `Clean Unusued Configs = true`, Flash Turret was again an inside hazard, and positive Currency moon curves had returned.

S1.40A keeps the S1.40 suppression values and disables CodeRebirth's unused-config cleanup so the preseeded DawnLib entries can survive startup.

## S1.40A config

```ini
[General]

Clean Unusued Configs = false

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

Do not intentionally remove Currency registration or `Money | Enemy Drop Rates`.

## Import rule

Gale: **Advanced options -> Import all files**.  
Expected marker: `S1.39 Compatibility Fixes loaded.`

## Persistent rules

- S1.29D is diagnostic only.
- Malfunctions disabled until user request.
- SCP999 disabled.
- BCMER exact existing 1.71.0 remains disabled until S1.40A passes.
- CodeRebirthLib must not return.
- Unknown PowerLevels are never guessed.
- S1.39 late Currency/map-object filter is only defensive fallback.

## Next gate

S1.40A passes only after runtime confirms natural Currency absence, Flash Turret absence, and post-run config retention.
