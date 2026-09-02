# 04 — Open Issues and Next Tests

## Priority 1 — S1.31 indoor density

S1.30 felt somewhat too dense indoors. S1.31 reduced all controllable indoor caps by 4.

Test on a normal moon through the late day/evening and use EnemyScan several times.

Goal: determine whether S1.31 is now comfortable or whether the problem is spawn timing/curves rather than caps.

## Priority 2 — CodeRebirth Microwave vs Pikmins

The existing LethalMin compatibility switch for Microwave knockback is false.

Still unproven:

- burn immunity,
- cook/status immunity,
- permanent-burning-state prevention.

Test Pikmins deliberately inside a Microwave effect.

Any persistent burn/cook state means configuration alone is insufficient and a targeted compatibility patch is needed.

## Priority 3 — Enemy targeting of Pikmins

Pikmins are immortal, but immortality does not prove that enemies stop selecting them as AI targets.

Watch for enemies that remain occupied with unkillable Pikmins.

If reproducible, prefer a small target-filter compatibility solution over disabling enemies.

## Priority 4 — Other CodeRebirth hazards

Flash Turret is confirmed safe.

Still test when encountered:

- ACU
- Crane
- Fan
- Laser Turret
- Tornado
- Compactor

## Priority 5 — Beehives

Do not test this on Offense.

Prefer Assurance or March.

If several runs on real vanilla Bee moons still produce suspiciously few/no Hives, investigate the effective daytime pool and compensate carefully without destroying established ratios.

## Priority 6 — Dungeon “theme song”

Main candidates:

1. Haunted Harpist / Phantom Piper — spatial enemy music.
2. PizzaTowerEscapeMusic — event/escape music, likely connected to Apparatus behavior.

When it happens, record:

- moon,
- interior,
- game time,
- whether Apparatus has been removed,
- whether the sound is directional/spatial,
- EnemyScan output.

## Priority 7 — Disabled vanilla Turret

One disabled Turret was observed.

Do not change Turret behavior yet.

Investigate only if it repeats while these are ruled out:

- terminal disable,
- Hacking Tool,
- player action,
- other legitimate disable mechanic.

## Priority 8 — Exact enemy PowerLevels

Still unresolved:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man

Do not guess. Use runtime or binary/asset analysis.

## After every meaningful test run

Preserve the full `LogOutput.log`.

Compare at least:

- exceptions/NREs,
- NavMesh warning volume,
- null EnemyType warnings,
- CodeRebirth errors,
- Pikmin hazard interactions,
- interior viability/weights,
- load/landing anomalies.
