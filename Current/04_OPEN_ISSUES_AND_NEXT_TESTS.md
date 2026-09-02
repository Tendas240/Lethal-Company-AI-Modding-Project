# 04 - Open Issues and Next Tests

## Priority 0 - verify S1.39 local plugin import

Import S1.39 in Gale with **Advanced options -> Import all files**.

Required marker:

- `S1.39 Compatibility Fixes loaded.`

Also expect the cumulative EnemyScan marker.

If the S1.39 marker is absent, import `Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip` into the same profile and relaunch.

Do not judge S1.39 map-object filtering or Pikmin kill protection before this is confirmed.

## Priority 1 - natural CodeRebirth currency cleanup

S1.37 filtered normal scrap rolls but S1.38 still showed `NewCoinPrefab(Clone)` instances through the map-object/hazard path.

S1.39 additionally filters indoor map-object generation.

Test several moons/interiors and confirm:

- no naturally generated Coin;
- no naturally generated Crisp Dollar Bill;
- no naturally generated Wayfarer's Wallet;
- no normal natural Credit Pad variants if they use the covered generation paths;
- dedicated CodeRebirth merchant/vending/enemy-drop currency mechanics still work when encountered.

When filtering activates, preserve `[MapObjectFilter]` log lines.

## Priority 2 - Flash Turret suppression

Confirm CodeRebirth Flash Turret no longer appears as a normal natural indoor hazard.

This is spawn suppression, not merely Pikmin immunity.

## Priority 3 - Ogopogo / Vermin disabled

Verify Biodiversity does not spawn Ogopogo and does not activate the related Vermin mechanic.

Config assertions passed; gameplay acceptance is pending.

## Priority 4 - CodeRebirth Autonomous Crane vs Pikmin/Puffmin

S1.38 runtime showed the crane could kill Pikmin despite:

- `Crane Targets Pikmin=false`
- `Crane Squishes Pikmin=false`
- Pikmin invincibility

S1.39 adds a direct CodeRebirth utility-kill guard.

Expected:

- crane may not kill Pikmin/Puffmin;
- if CodeRebirth attempts the guarded kill path, `[PikminCraneShield]` should log a block;
- normal enemy kills outside that CodeRebirth utility context must not be globally disabled.

## Priority 5 - health recharge station

`AddHealthRechargeStation=true` is already present and was explicitly verified in the profile.

Test:

1. take known damage;
2. use the ship health recharge station;
3. confirm it restores health to the desired full value and does not produce errors.

## Priority 6 - 2560x1440 camera carry-forward

S1.38 loaded FixCameraResolutions successfully. Confirm S1.39 still renders sharply at the intended 2560x1440 internal target and has not regressed because of profile import behavior.

## Priority 7 - Old Bird Lethal Resonance encounter validation

Plugin/config build validation exists, but a clean Old Bird encounter is still needed.

When an Old Bird appears, verify replacement audio for:

- main/mechanical/weapon group;
- footsteps;
- loudspeaker/voice group.

Also verify non-Old-Bird Lethal Resonance groups stay disabled.

## Priority 8 - Mirage retention

The user had to set `neverDeleteRecordings=true` manually in the Main Menu/LethalConfig after profile import. The later S1.38 log confirmed that manual value at runtime.

After importing S1.39, check the setting again. If it reverted, set it manually; do not treat `.r2z` import as authoritative for this game-root per-player setting.

## Confirmed behavior - CodeRebirth microwave vs Pikmins

S1.36 runtime testing produced an explicit user confirmation that Pikmins were no longer affected by the CodeRebirth microwaves. Treat this as accepted and **do not spend another build on it unless a later run shows a regression**.

## Priority 9 - enemy target selection against immortal Pikmins

Immortal Pikmins can still waste enemy AI if enemies select them as targets. If reproducible, prefer a small target-filter compatibility patch rather than disabling enemies.

## Priority 10 - exact enemy PowerLevels

Still unresolved and must not be guessed:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man

Use runtime, binary or asset analysis.

## Later phase - BCMER reactivation

BCMER remains disabled in S1.39. Do not fold it into the S1.39 acceptance test.

After S1.39 is accepted, the logical next isolated build is a BCMER re-audit/reactivation against the accepted gameplay base, with special attention to spawn power/chance ownership.

## Known warnings to leave alone unless functionality breaks

- SellMyScrap / ShipInventoryUpdated warnings.
- InjectionLibrary skipping Mirage/Opus native DLLs as non-.NET.
- CodeRebirth Weather Registry unavailable warning.
- NavMeshInCompany NodeHelper warnings.

## After every meaningful run

Preserve the full `LogOutput.log` and compare:

- exceptions/NREs;
- plugin load list;
- S1.39 compatibility marker;
- DoorAudit / DoorFailsafe;
- EnemyScanFix;
- `[MapObjectFilter]` / `[PikminCraneShield]`;
- SCP999 absence;
- Ogopogo/Vermin absence;
- currency/Flash Turret natural-spawn evidence;
- Pikmin hazard interactions;
- FixCameraResolution load/status;
- Lethal Resonance/SoundAPI load status;
- Mirage loaded settings.
