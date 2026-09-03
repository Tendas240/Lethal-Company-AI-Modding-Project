# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Machine-readable status:
`Current/Projektstatus_S1.42Q.json`

Current design:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`

Current built candidate:
`Current/60_S1.42Q_MINIMAL_NATIVE_ROLLBACK_BUILD.md`

Verification:
`Current/VERIFIKATION_S1.42Q.txt`

Hashes:
`Current/SHA256SUMS_S1.42Q.txt`

Current mod list:
`Current/Aktive_Modliste_S1.42Q.txt`

Latest runtime analysis:
`Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

## Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

## Latest valid runtime evidence

**S1.42P - PARTIAL / FAIL**

Evidence:
`RuntimeEvidence/S1.42P/20260903T181706Z/`

Log SHA-256:
`d656095fb874a415a1bd2377c0411339d3d6eb002dce4ec3f6216e879294127f`

The user's 20 -> 18 Pikmin recovery failure was confirmed exactly.

## Current built candidate awaiting runtime

**S1.42Q - LethalMin Native Minimal Rollback**

Profile:
`Profiles/LC V1 S1.42Q LethalMin Native Minimal Rollback.r2z`

SHA-256:
`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Git blob SHA:
`9e1beec739c193c95e936a56fefb060a84577559`

Compatibility plugin:
**v1.3.12**

Embedded DLL SHA-256:
`f6a4e7b060af6a779da1c92236b2ce63d1bd5d890a21c9492517e568a9aaac45`

Build:
- GitHub Actions #52: SUCCESS
- generated commit `bd6e1ca023921e5fecb14e301e9c24cf73cb4aea`
- 331 ZIP members
- 330 readable snapshot files
- no added members

Changed profile members only:
1. `BepInEx/config/NoteBoxz.LethalMin.cfg`
2. `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
3. `export.r2x`

## S1.42Q architecture

Native LethalMin owns:
- Pikmin -> enemy attack/latch
- enemy-death task completion
- Pikmin -> dead enemy body carry
- Onion delivery

Project-local code only keeps proven minimal Enemy -> Pikmin protection and unrelated compatibility shims.

Removed:
- BaboonHawkDeathCleanup
- project-local FinishTask death finalization
- 4.0 m Hawk-death scan
- delayed/reflection-heavy post-grab state repair

Kept:
- prevention-only GrabPikmin prefix for Crawler/Thumper and Baboon Hawk Enemy -> Pikmin gaps
- one-way Baboon Hawk -> Pikmin adapter/bite protection
- Puffer effect guard
- CodeRebirth utility-kill shield
- Dead Baboon Hawk corpse CanGrabScrap guard

LethalMin config delta from S1.42P:
**exactly one value**
- `Thumper Bite Limit = 0` -> `3`

## Temporary test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Q`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42Q_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42Q through:

**Gale -> Advanced options -> Import all files**

Then perform the focused Crawler/Thumper + Baboon Hawk + Puffer runtime test.

Required startup marker:
`[LethalMinNativeOwnership]`

Forbidden old marker:
`[BaboonHawkDeathCleanup]`

Record following count before/after each enemy fight. Verify native attack/death/carry, Enemy -> Pikmin protection, corpse-to-Onion behavior, and no leader/no-task loops.

Commit the complete fresh `LogOutput.log` to:
`RuntimeInbox/Current/`

Do not restore normal enemies or BCMER before S1.42Q passes.
