# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Machine-readable current status:
`Current/Projektstatus_S1.42N.json`

Latest runtime analysis:
`Current/50_S1.42M_DEATH_CLEANUP_PARTIAL_PASS_ANALYSIS.md`

Current candidate build document:
`Current/51_S1.42N_BABOON_HAWK_DEATH_TARGET_RESOLVER_BUILD.md`

Historical detailed handover that preceded this result:
`Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md`

## State separation

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:
runtime accepted normal-gameplay baseline.

### Latest valid runtime evidence

**S1.42M - PARTIAL PASS**

Evidence:
`RuntimeEvidence/S1.42M/20260903T163446Z/`

Raw log:
`RuntimeEvidence/S1.42M/20260903T163446Z/raw/LogOutput.log`

Log SHA-256:
`0639d5cc04aa54f5d7943ef4689e0d705c818871b019287ca1a1cdc2aa2492fb`

Confirmed:
- Pikmin -> living Baboon Hawk attack/latch/kill remains functional;
- Dead Baboon Hawk body appears;
- Pikmin can carry the corpse to the Onion;
- living Baboon Hawks ignore the corpse item;
- `Leader is null when following` count = 0.

Failed:
- attacking Pikmin still disappear when the Hawk dies.

Critical diagnostic marker:
`[BaboonHawkDeathCleanup] Dying BaboonHawkEnemy(Clone): released 0/0 latched Pikmin ...`

Interpretation:
the exact `PikminAI.RemoveCurrentTask()` method resolved correctly, but S1.42M searched the wrong object relationship. Attacking/latching Pikmin are not discoverable as `PikminAI` children under the dying Hawk transform.

### Current built candidate awaiting runtime

**S1.42N - Baboon Hawk Death Target Resolver**

Profile:
`Profiles/LC V1 S1.42N Baboon Hawk Death Target Resolver.r2z`

SHA-256:
`c87d48464a750f87274e2848c44e5e1e24d4f1da087f59a33e2889744ebc13e9`

Base:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

Compatibility plugin:
**v1.3.9**

Build verification:
- GitHub Actions build #44: PASS;
- idle guard #45: PASS;
- 331 archive members;
- 330 readable snapshot files;
- changed existing archive members only:
  - compatibility DLL;
  - `export.r2x`;
- no added archive members.

No separate v1.3.9 DLL SHA-256 is currently recorded; do not invent one.

## S1.42N implementation

Only the failed S1.42M death target resolver changed.

At Hawk death, S1.42N:
- uses a one-shot read of `RoundManager.Instance.SpawnedEnemies`;
- filters to runtime objects assignable to `LethalMin.PikminAI`;
- considers Pikmin under the dying Hawk or within a 4.0 m death-release zone;
- invokes the exact resolved `PikminAI.RemoveCurrentTask()`;
- emits per-Pikmin release diagnostics and aggregate candidate/release counts.

This runs only on the Hawk death event.

Explicitly not used:
- continuous Update-driven global EnemyAI/Pikmin scans;
- broad/inherited LethalMin Harmony scanning.

The S1.42M corpse guard is retained unchanged because it passed runtime.

## Closed / retained behavior

- Thumper/Crawler -> Pikmin protection: PASS / CLOSED
- Pikmin -> Thumper/Crawler attack/latch: PASS / CLOSED
- Puffer -> Pikmin: PASS / CLOSED
- Jetpack: PASS / CLOSED
- Baboon Hawk -> Pikmin ignore: PASS / CLOSED
- Pikmin -> living Baboon Hawk attack/latch/kill: PASS / CLOSED
- Dead Baboon Hawk corpse exists and is Pikmin-carryable to Onion: PASS
- living Baboon Hawks ignore Dead Baboon Hawk corpse: PASS

Visible Thumper snapping remains accepted harmless cosmetic behavior.

## Active runtime gate - S1.42N

Required result:
- attacking/latching Pikmin are actually found by the death resolver;
- those Pikmin detach/remain visible and usable after Hawk death;
- corpse behavior remains intact;
- living Hawk corpse ignore remains intact;
- Hawk -> Pikmin ignore remains intact;
- no leader-null loop.

## Temporary isolated test state

EnemyIsolation:
**enabled**

BCMER exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42N is evaluated.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42N`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42N_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42N using:
**Gale -> Advanced options -> Import all files**

Then:
1. throw several Pikmin onto a living Baboon Hawk;
2. confirm normal attack/latch;
3. let them kill it;
4. verify the attacking Pikmin remain visible and usable;
5. verify the log contains one or more `[BaboonHawkDeathCleanup] Released ...` lines and a non-zero release count;
6. wait for the SellBodies corpse;
7. verify the Dead Baboon Hawk body remains;
8. verify Pikmin can still carry it to the Onion;
9. verify living Hawks do not pick it up;
10. verify Hawk -> Pikmin ignore;
11. verify no `Leader is null when following`;
12. commit the complete fresh `LogOutput.log` to `RuntimeInbox/Current/`.

Do not build a successor first unless S1.42N cannot start.

## Deferred maintenance

General repository/documentation cleanup remains deferred until the active runtime gate closes.

Known non-functional drift:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical sections of `Patches/S139CompatibilityFixes/Plugin.cs`.

Repository optimization plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
