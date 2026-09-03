# 42 — Handover S1.42L to Next

**Date:** 2026-09-03
**Game:** Lethal Company V81

## Canonical current state

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42J**

Evidence:
`RuntimeEvidence/S1.42J/20260903T145657Z/`

Log SHA-256:
`a8ce035bf64fa5b704e18c588215f43cd1fd184eef4f467dfbafa6fcb1379963`

Current active runtime candidate:
**S1.42L — Pikmin Counterattack Restore**

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

S1.42K:
**built successfully but never runtime-tested; superseded.**

## Why S1.42L exists

S1.42J proved:
- Baboon Hawk -> Pikmin protection PASS;
- Thumper/Crawler -> Pikmin protection PASS;
- Puffer -> Pikmin PASS;
- Jetpack PASS.

But S1.42J intentionally blacklisted both Crawler and Baboon hawk from Pikmin attacks.

The user clarified that Pikmin must still be throwable onto and attack/latch:
- Thumper/Crawler;
- Baboon Hawks.

Therefore the permanent architecture is asymmetric.

## Binding enemy rules

### Baboon Hawk -> Pikmin
No target/chase/bite/grab/hold.
Keep the S1.42J adapter disable, BitePikmin block, and GrabPikmin failsafe.

### Pikmin -> Baboon Hawk
Normal LethalMin attack/latch allowed.

### Thumper/Crawler -> Pikmin
No functional GrabPikmin / leader removal / grabbed death timer.
Keep ThumperPikminGuard.

### Pikmin -> Thumper/Crawler
Normal LethalMin attack/latch allowed.

### Puffer -> Pikmin
No effect. PASS.

## Attack Blacklist

S1.42L:
`Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy`

This exactly matches the modern S1.40B/S1.41 baseline.

Recent project-added entries:
- Crawler — added in S1.42C, now removed;
- Baboon hawk — added in S1.42J, now removed.

No recent project-added enemy blacklist entries remain.

Historical caveat:
the old juijui profile had a much shorter blacklist, but it is not the modern canonical baseline and used a different historical mod environment.

## Exact next action

Runtime-test S1.42L.

Import:
**Gale -> Advanced options -> Import all files**

Focused checks:
1. throw Pikmin onto Thumper/Crawler -> Pikmin latch/attack;
2. let Thumper snap at Pikmin -> ThumperPikminGuard still blocks GrabPikmin;
3. throw Pikmin onto Baboon Hawk -> Pikmin latch/attack;
4. Baboon Hawk itself still ignores Pikmin from its AI side;
5. no bite/grab/hold loop;
6. no `Leader is null when following`.

Upload complete fresh log to:
`RuntimeInbox/Current/`

If PASS:
- isolated enemy interaction gate complete;
- remove/disable EnemyIsolation;
- restore normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0;
- preserve all asymmetric permanent interaction rules above.

Repository migration remains deferred until this gate is evaluated and documented.
