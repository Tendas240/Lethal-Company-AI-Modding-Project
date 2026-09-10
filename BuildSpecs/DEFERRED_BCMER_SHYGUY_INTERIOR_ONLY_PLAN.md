# Deferred BCMER ShyGuy Interior-Only Event Correction

**Status:** IMPLEMENTED AS S1.42AI / STATIC-VERIFIED / RUNTIME VALIDATION PENDING
**Scope owner:** BCMER event configuration only  
**Observed build:** `S1.42AH`  
**Runtime evidence:** `RuntimeEvidence/S1.42AH/20260908T202138Z/`  
**Raw-log SHA-256:** `f2a0316815d411c6e37bf91651bf2e4602b9b2a7697e9327a010b28be4af6883`  
**Current source snapshot:** `ProfileSources/S1.42AH/`  
**Last-Validated:** 2026-09-10

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

The S1.42AH MouthDog lifecycle gate is closed and S1.42AH remains the accepted gameplay baseline. This independent correction has been implemented as active runtime candidate S1.42AI without modifying S1.42AH bytes or readable snapshot.

S1.42AI profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
Static evidence: `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`
Candidate authority: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`

The pending decision is now runtime-only. Do not mix LC Office, CullFactory, fog, Black Mesa, LethalEscape or other deferred scopes into S1.42AI. A final acceptance/rejection must preserve S1.42AH as the rollback/provenance base until S1.42AI explicitly passes.

This preserves provenance while ensuring the defect is not lost.
## Validation contract for S1.42AI

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
