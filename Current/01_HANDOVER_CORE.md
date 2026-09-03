# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest runtime evidence:
**S1.42P — PARTIAL/FAIL, exact 20 -> 18 Pikmin recovery**

Current built candidate:
**S1.42Q — LethalMin Native Minimal Rollback**

Profile:
`Profiles/LC V1 S1.42Q LethalMin Native Minimal Rollback.r2z`

SHA-256:
`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Compatibility plugin:
**v1.3.12**

Read first:
- `Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`
- `Current/60_S1.42Q_MINIMAL_NATIVE_ROLLBACK_BUILD.md`
- `Current/Projektstatus_S1.42Q.json`
- `Current/VERIFIKATION_S1.42Q.txt`
- `Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

## Architectural rule

Keep normal LethalMin ownership:

- Pikmin -> Enemy = native LethalMin
- enemy death / task completion = native LethalMin
- Pikmin -> dead enemy body = native LethalMin
- Onion delivery = native LethalMin
- Enemy -> Pikmin = blocked by native config plus only proven minimal compatibility shims

S1.42Q removes all project-local Hawk-death task cleanup and reflection-heavy post-grab recovery.

## Build verification

GitHub Actions #52:
**SUCCESS**

Profile SHA-256:
`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Embedded DLL SHA-256:
`f6a4e7b060af6a779da1c92236b2ce63d1bd5d890a21c9492517e568a9aaac45`

Only profile delta:
- LethalMin config
- compatibility DLL
- export profile name

Only LethalMin config value changed:
`Thumper Bite Limit = 0 -> 3`

## Exact next action

Import with:
**Gale -> Advanced options -> Import all files**

Test:
1. Crawler/Thumper native Pikmin attack/latch/kill
2. full follower recovery
3. Baboon Hawk native Pikmin attack/latch/kill
4. full follower recovery
5. Puffer harmlessness
6. Enemy -> Pikmin grab/bite protection
7. Dead Baboon Hawk native carry to Onion
8. living Hawk corpse ignore
9. no no-task Work loop
10. no leader-null loop

Expected:
`[LethalMinNativeOwnership]`

Must not appear:
`[BaboonHawkDeathCleanup]`

Then commit complete fresh log to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation:
enabled.

BCMER 1.71.0:
disabled.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Q`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42Q_BUILD_AWAITING_RUNTIME`
