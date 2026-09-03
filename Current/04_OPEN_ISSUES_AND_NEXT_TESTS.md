# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42Q minimal LethalMin-native rollback

Design:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`

Build:
`Current/60_S1.42Q_MINIMAL_NATIVE_ROLLBACK_BUILD.md`

Profile:
`Profiles/LC V1 S1.42Q LethalMin Native Minimal Rollback.r2z`

SHA-256:
`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Compatibility plugin:
**v1.3.12**

## What changed

Normal LethalMin combat/death/carry ownership is restored.

Removed:
- BaboonHawkDeathCleanup
- project-local FinishTask death handling
- 4.0m death scan
- delayed post-grab recovery
- reflected leader/follow/grab restoration

Kept:
- minimal pre-mutation Enemy -> Pikmin GrabPikmin prevention for proven Crawler/Thumper and Hawk gaps
- one-way Hawk -> Pikmin adapter/bite protection
- Puffer effect guard
- CodeRebirth utility-kill guard
- Dead Hawk corpse guard

Config:
`Thumper Bite Limit = 3`

## Exact runtime test

Use:
**Gale -> Advanced options -> Import all files**

1. record following count
2. attack/kill Crawler/Thumper with Pikmin
3. verify natural release/recovery
4. attack/kill Baboon Hawk with Pikmin
5. verify natural release/recovery
6. verify exact following-count recovery
7. verify Crawler/Thumper cannot grab Pikmin
8. verify Hawk cannot target/chase/bite/grab Pikmin
9. verify Puffer does not affect Pikmin
10. verify Dead Hawk body is carried to Onion
11. verify living Hawks ignore corpse
12. verify no `Work state with no task assigned!`
13. verify no `Leader is null when following`
14. verify `[LethalMinNativeOwnership]`
15. verify no `[BaboonHawkDeathCleanup]`
16. commit full log to `RuntimeInbox/Current/`

## Temporary state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Q`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42Q_BUILD_AWAITING_RUNTIME`

Do not restore normal enemies or BCMER until S1.42Q passes.
