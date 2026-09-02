# 04 — Open Issues and Next Tests

## Priority 0 — Verify S1.36 import

S1.36 is structurally verified but not runtime-tested.

When importing in Gale, enable:

**Advanced options → Import all files**

Then check LogOutput.log for:

- S1.35 Compatibility Fixes loaded
- [EnemyScanFix] Patched EnemyScan to list every active EnemyAI ...

If missing, import:

Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

into the S1.36 profile.

Do not evaluate door/EnemyScan behavior until this load requirement is satisfied.

## Priority 1 — Ship-door behavior

### Test A — living player inside ship

As the only living player, stand clearly inside the landed ship and close the hangar door.

Expected:

- door closes;
- energy remains at 100%;
- door stays closed indefinitely until intentionally opened or another legitimate game transition occurs.

Log should show DoorAudit and livingInsideShip=1.

### Test B — all living players outside

With all living players outside, reproduce a closed hangar door.

Expected:

- local patch does not refill energy;
- vanilla hydraulic countdown runs;
- door opens at zero;
- permanent outside lockout cannot occur.

Log should show DoorFailsafe saying all living players are outside.

If the door closes unexpectedly again, preserve the new audit stack because it may identify the calling method/mod.

## Priority 2 — Complete enemies output

EnemyScan 1.2.1 originally excluded EnemyAI without ScanNodeProperties.

S1.36 patches only this listing behavior.

Test while several known enemies are active, ideally including a modded or scanless case.

Compare:

- visible enemies,
- runtime spawn/AI lines,
- enemies terminal output.

Goal: every active EnemyAI appears and counts update correctly.

## Priority 3 — Verify SCP999 is truly gone

Latest S1.31–S1.34 logs showed SCP999 2.4.0 loading and immediately throwing a startup NRE.

S1.36 disables ProjectSCP-SCP999.

Expected:

- no Loading [SCP999 ...];
- no SCP999.Plugin.Awake NRE;
- no later [SCP999] Max health ... debug lines.

If it still loads, investigate whether Gale ignored the disabled state or another copy exists outside the profile.

## Priority 4 — Leaf Boy blacklist verification

S1.32+ appends Leaf boy to the LethalMin Attack Blacklist.

Original issue: multi-minute Pikmin attack loop against LeafBoi(Clone).

Confirm:

- Pikmins do not start attacks on Leaf Boy;
- no repeated LethalMin hit loop occurs;
- Leaf Boy otherwise behaves normally.

Do not alter Leaf Boy spawn rate/health to solve targeting.

## Priority 5 — CodeRebirth Microwave vs Pikmins

Microwave Knockbacks Pikmin=false does not prove burn/cook immunity.

Still unproven:

- burn immunity;
- cook/status immunity;
- prevention of permanent burning while Pikmins are immortal.

If persistent burning occurs, config is insufficient and a targeted compatibility patch is required.

## Priority 6 — Enemy targeting of immortal Pikmins

Immortality does not prove enemies stop selecting Pikmins as targets.

Watch for enemies remaining occupied with unkillable Pikmins.

If reproducible, prefer a small target-filter compatibility patch over disabling enemies.

## Priority 7 — Other CodeRebirth hazards

Flash Turret is confirmed safe.

Still test when encountered:

- ACU
- Crane
- Fan
- Laser Turret
- Tornado
- Compactor

## Priority 8 — SellMyScrap warnings

Current logs contain warnings that some SellMyScrap methods cannot load ShipInventoryUpdated 2.0.0.

Do not change anything solely because of the warning. First determine whether user-facing SellMyScrap functionality is actually broken.

## Priority 9 — Beehives

Do not use Offense as the bee baseline.

Prefer Assurance or March.

Only compensate Bee chance if several runs on actual vanilla Bee moons show a reproducible problem.

## Priority 10 — Dungeon theme song

Main candidates:

1. Haunted Harpist / Phantom Piper — spatial enemy music.
2. PizzaTowerEscapeMusic — event/escape music, likely tied to Apparatus behavior.

Record moon, interior, time, Apparatus state, directionality and enemies output when it occurs.

## Priority 11 — Exact enemy PowerLevels

Still unresolved:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man

Do not guess. Use runtime or binary/asset analysis.

## Lower-priority observations

- One disabled vanilla Turret was observed historically. Investigate only if repeated with player/terminal/hacking actions ruled out.
- CodeRebirth logs Weather Registry not found; investigate only if missing weather content matters.
- NavMeshInCompany missing NodeHelper warnings are known; investigate if navigation is actually broken.

## After every meaningful run

Preserve the full LogOutput.log and compare at least:

- exceptions/NREs;
- plugin load list;
- DoorAudit / DoorFailsafe;
- EnemyScanFix;
- SCP999 absence;
- Pikmin hazard interactions;
- LethalMin work-state warning volume;
- interior viability/weights;
- load/landing anomalies.
