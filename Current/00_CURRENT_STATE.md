# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical acceptance state

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:
runtime accepted gameplay baseline.

### Current candidate

**S1.42M - Baboon Hawk Death Cleanup**

Profile:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Base:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

Compatibility plugin:
- version 1.3.8
- DLL SHA-256 `47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Build:
- GitHub Actions success;
- 0 warnings / 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only:
  - compatibility DLL;
  - `export.r2x`;
- no added members.

## Latest valid runtime evidence

Latest tested build remains **S1.42L**:

`RuntimeEvidence/S1.42L/20260903T155132Z/`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

Confirmed:
- Pikmin -> Baboon Hawk latch/attack **PASS**;
- Pikmin can kill Baboon Hawk;
- Baboon Hawk -> Pikmin protection remains **PASS**;
- `Leader is null when following` count = 0.

New reproduced issue:
latched Pikmin remained attached to the dead original Hawk target after death. SellBodiesFixed later created the carryable `BaboonHawkBody(Clone)` and moved the original enemy transform away, causing the attacking Pikmin to disappear with the stale target. Living Baboon Hawks also picked up the new corpse item as scrap.

## Closed topics

- Thumper/Crawler -> Pikmin protection: **PASS / CLOSED**
- Pikmin -> Thumper/Crawler attack/latch: **PASS / CLOSED**
- Puffer -> Pikmin: **PASS / CLOSED**
- Jetpack: **PASS / CLOSED**
- Baboon Hawk -> Pikmin: **PASS / CLOSED**
- Pikmin -> Baboon Hawk live attack/latch: **PASS / CLOSED**

Visible Thumper snapping remains accepted harmless cosmetic behavior.

## Active runtime gate - S1.42M

Desired permanent behavior:
- attacking/latching living Baboon Hawks remains allowed;
- Hawk -> Pikmin ignore remains active;
- Pikmin latched to a dying Hawk detach/remain visible and usable;
- SellBodiesFixed continues creating the Dead Baboon Hawk body;
- corpse remains on the ground and carryable by Pikmin/players;
- Pikmin can carry the corpse toward the Onion;
- living Baboon Hawks do not pick up the corpse;
- no leader-null loop.

S1.42M implementation is deliberately narrow:
- exact declared `BaboonBirdAI.KillEnemy(bool)`;
- exact declared `LethalMin.PikminAI.RemoveCurrentTask()` runtime resolution;
- only Pikmin under the specific dying Hawk hierarchy;
- exact declared `BaboonBirdAI.CanGrabScrap(GrabbableObject)`;
- only `BaboonHawkBody` / `Dead Baboon Hawk` is rejected for living Hawk scrap pickup.

No scene-wide scan and no broad LethalMin patching.

## Temporary isolated test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal spawning/BCMER until S1.42M is evaluated.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42M using:
**Gale -> Advanced options -> Import all files**

Then:
1. throw Pikmin onto a Baboon Hawk;
2. let them kill it;
3. verify Pikmin detach/remain usable;
4. wait beyond SellBodies' 4-second body delay;
5. verify Dead Baboon Hawk remains;
6. throw Pikmin onto corpse and verify carry toward Onion;
7. verify living Hawks do not pick up corpse;
8. verify Hawk -> Pikmin ignore;
9. verify no leader-null loop;
10. upload complete log to `RuntimeInbox/Current/`.

## Deferred maintenance

General repository/documentation cleanup remains deferred until the active runtime gate closes.

Known non-functional drift to clean later:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in `Patches/S139CompatibilityFixes/Plugin.cs`.

Do not mix that maintenance into the S1.42M runtime gate.

Repository optimization plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
