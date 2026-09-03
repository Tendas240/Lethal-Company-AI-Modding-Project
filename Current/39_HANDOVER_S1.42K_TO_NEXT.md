# 39 — Current Handover S1.42K

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical state

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42J**

Evidence:
`RuntimeEvidence/S1.42J/20260903T145657Z/`

Log SHA-256:
`a8ce035bf64fa5b704e18c588215f43cd1fd184eef4f467dfbafa6fcb1379963`

Current built candidate / active runtime gate:
**S1.42K — Thumper Pikmin Attack Restore**

Profile:
`Profiles/LC V1 S1.42K Thumper Pikmin Attack Restore.r2z`

SHA-256:
`bbdc949c9477e138cc3dde7c261f36f014cf482dd930c393ab035d80f8560aa2`

Build:
- GitHub Actions success;
- 331 archive members;
- 330 readable snapshot files;
- changed only LethalMin config + export.r2x;
- compatibility DLL unchanged.

## S1.42J accepted results

### Baboon Hawk <-> Pikmin
**PASS.**
Complete zero interaction in both directions.

### Puffer -> Pikmin
**PASS / reconfirmed.**
Smoke does not affect Pikmin.

### Jetpack
**PASS / accepted by user.**
140-second target marker present, normal behavior accepted, old Coroner Jetpack PlayerController-null flood absent.
Remove Jetpack from active work unless a future regression appears.

### Thumper/Crawler -> Pikmin
**PASS.**
19 `[ThumperPikminGuard]` blocks during deliberate direct contact.
Zero `Leader is null when following` errors.

## Revised binding Thumper rule

The old "Thumper/Crawler <-> Pikmin zero interaction in both directions" decision is superseded.

Current binding rule:
- **Thumper/Crawler -> Pikmin:** no functional grab/bite state effect; keep the existing GrabPikmin guard.
- **Pikmin -> Thumper/Crawler:** normal LethalMin attack/latch must work, including throwing Pikmin onto a Thumper.

S1.42J failed only the reverse direction because `Crawler` was on LethalMin's Pikmin Attack Blacklist.

S1.42K removes only `Crawler` from that blacklist.
`Baboon hawk` and `Leaf boy` remain blacklisted.

## Exact next action

Runtime-test S1.42K.

Import:
**Gale -> Advanced options -> Import all files**

Primary acceptance:
1. throw Pikmin onto a Thumper/Crawler;
2. Pikmin must latch/attack normally;
3. Thumper may visibly snap, but its GrabPikmin route must still be blocked;
4. `[ThumperPikminGuard]` should still appear;
5. no grabbed death timer, leader removal, or leader-null loop.

Upload complete fresh log to:
`RuntimeInbox/Current/`

Runtime router:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42K`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42K_BUILD_AWAITING_RUNTIME`

## After S1.42K passes

The isolated enemy interaction gate is complete.

Then:
- remove/disable temporary EnemyIsolation;
- restore normal enemy configuration from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0;
- preserve Baboon Hawk <-> Pikmin zero interaction;
- preserve Thumper/Crawler -> Pikmin immunity while allowing Pikmin -> Thumper/Crawler attack/latch;
- preserve Puffer -> Pikmin immunity.

Do not start the pending repository structural migration before S1.42K is evaluated and documented.

Migration plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Key analyses:
- `Current/37_S1.42J_RUNTIME_ANALYSIS_AND_S1.42K_PLAN.md`
- `Current/38_S1.42K_THUMPER_PIKMIN_ATTACK_RESTORE_BUILD.md`
- `Current/Projektstatus_S1.42K.json`
