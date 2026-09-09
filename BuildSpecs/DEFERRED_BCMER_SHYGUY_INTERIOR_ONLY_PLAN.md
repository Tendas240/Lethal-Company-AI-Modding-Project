# Deferred BCMER ShyGuy Interior-Only Event Correction

**Status:** DEFERRED / CONFIRMED RUNTIME DEFECT / NOT ARMED  
**Scope owner:** BCMER event configuration only  
**Observed build:** `S1.42AH`  
**Runtime evidence:** `RuntimeEvidence/S1.42AH/20260908T202138Z/`  
**Raw-log SHA-256:** `f2a0316815d411c6e37bf91651bf2e4602b9b2a7697e9327a010b28be4af6883`  
**Current source snapshot:** `ProfileSources/S1.42AH/`  
**Last-Validated:** 2026-09-09

## Runtime finding

The first gameplay run in the cited S1.42AH evidence selected the BCMER `ShyGuy` event. The same run then logged `ShyGuy(Clone) spawned outside; Switching to exterior AI`, proving that BCMER created a ShyGuy on the exterior path.

The user also observed that this exterior ShyGuy was visually invisible while remaining functionally present; the log later proves a working ShyGuy enemy entity/attack path. The exact renderer/material cause of the invisibility is **not proven** and must not be promoted to a stronger causal claim.

## Configuration conflict

Normal ShyGuy spawn ownership belongs to Scopophobia. In the current Scopophobia v1.3.4 configuration, ordinary moon sections declare:

```text
# Default value: true
SpawnInside = true

# Default value: false
SpawnOutside = false
```

The current profile retains that `SpawnOutside = false` contract.

BCMER 1.71.0 independently overrides the location contract when its `[ShyGuy]` event executes. In:

`ProfileSources/S1.42AH/BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`

its current event values are:

```text
ShyGuyDef InsideEnemyRarity = 20, 0.8, 20, 100
ShyGuyDef MinInsideEnemy = 2, 0.04, 2, 6
ShyGuyDef MaxInsideEnemy = 2, 0.04, 2, 6

ShyGuyDef OutsideEnemyRarity = 10, 0.4, 10, 50
ShyGuyDef MinOutsideEnemy = 1, 0.02, 1, 3
ShyGuyDef MaxOutsideEnemy = 2, 0.04, 2, 6
```

The positive exterior triplet is sufficient to explain why the BCMER event can create an exterior ShyGuy even though Scopophobia itself has exterior spawning disabled.

## Required correction

For the first eligible independent BCMER/config successor after the S1.42AH lifecycle gate closes, preserve the event and all interior values, but set only the ShyGuy exterior triplet to zero:

```text
ShyGuyDef OutsideEnemyRarity = 0, 0, 0, 0
ShyGuyDef MinOutsideEnemy = 0, 0, 0, 0
ShyGuyDef MaxOutsideEnemy = 0, 0, 0, 0
```

Preserve unchanged:

- `[ShyGuy] Event Enabled? = true`;
- `[ShyGuy] Event Type = VeryBad`;
- `ShyGuyDef InsideEnemyRarity = 20, 0.8, 20, 100`;
- `ShyGuyDef MinInsideEnemy = 2, 0.04, 2, 6`;
- `ShyGuyDef MaxInsideEnemy = 2, 0.04, 2, 6`;
- Scopophobia `SpawnInside` / `SpawnOutside` settings;
- BCMER 1.71.0 and the accepted EventType-weight architecture;
- all unrelated BCMER events and normal enemy-spawn ownership.

Do not solve this by setting Scopophobia `SpawnOutside = true`. The target is specifically **BCMER ShyGuy event = interior-only**, consistent with the normal Scopophobia spawn contract.

## Lifecycle / provenance boundary

S1.42AH is already a built, checksum-fixed active runtime candidate. Do **not** edit its `.r2z`, `ProfileSources/S1.42AH/`, build metadata, or controller state to retroactively apply this correction.

The current S1.42AH MouthDog final non-Pikmin-neighbor runtime gate remains authoritative and must close first.

- If S1.42AH is accepted, this correction is eligible as the next independent BCMER/config successor scope.
- If S1.42AH is rejected, first follow the canonical S1.42AF-derived MouthDog recovery path. Do not silently mix this unrelated BCMER correction into a rejection-recovery build unless the lifecycle explicitly arms a combined scope. Keep this correction pending and mandatory for the first eligible independent successor afterward.

This preserves provenance while ensuring the defect is not lost.

## Validation contract for the future corrected build

Static validation must prove:

1. the three ShyGuy exterior values are exactly `0, 0, 0, 0`;
2. the three ShyGuy interior values remain unchanged;
3. the ShyGuy event remains enabled and retains its EventType;
4. Scopophobia still retains its ordinary `SpawnOutside = false` contract;
5. no unrelated BCMER event/spawn-owner setting changed.

Runtime validation should deliberately force or otherwise positively observe the BCMER `ShyGuy` event and prove:

1. the event is selected/executed;
2. ShyGuy remains available through the intended interior event path;
3. no ShyGuy is added/spawned through the BCMER exterior list;
4. no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker occurs as a result of this event;
5. known project regression markers remain clean.

Absence of the prior exterior visual symptom is useful corroboration, but do not claim the exact invisibility mechanism was repaired unless separate evidence establishes that mechanism.

## LethalEscape boundary

The deferred `woah25-LethalEscapeUpdated 2.5.0` evaluation is a separate compatibility scope. An enemy that **spawns inside and later transitions outside** is not equivalent to enabling ordinary exterior spawning.

Do not set Scopophobia `SpawnOutside = true` merely to emulate LethalEscape. If ShyGuy is evaluated with LethalEscape later, explicitly validate the interior-to-exterior transition, visibility/material state, navigation, targeting, networking and return/cleanup behavior as its own compatibility contract.
