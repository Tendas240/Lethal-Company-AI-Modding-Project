# 45 — Final Handover S1.42L

**Date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

This file is the newest dedicated handover and supersedes older current-gate handovers as a takeover pointer. Older handovers remain historical evidence.

## 1. Canonical state at handover

### Last fully accepted gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:
runtime accepted gameplay baseline.

### Latest built and runtime-tested candidate

**S1.42L — Pikmin Counterattack Restore**

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Readable snapshot:
`ProfileSources/S1.42L/`

Build result:
`Current/AUTO_BUILD_RESULT.json`

Build verification:
- GitHub Actions success;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only:
  - `BepInEx/config/NoteBoxz.LethalMin.cfg`
  - `export.r2x`;
- no added archive members;
- compatibility DLL unchanged from S1.42J.

Compatibility plugin:
- version **1.3.7**
- DLL SHA-256:
  `7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

### Latest valid runtime evidence

Evidence:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log:
`RuntimeEvidence/S1.42L/20260903T151817Z/raw/LogOutput.log`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

Runtime verdict:
**PARTIAL PASS — only Pikmin -> Baboon Hawk explicit attack/latch validation remains.**

## 2. Confirmed closed topics

### Thumper / Crawler

**PASS / CLOSED.**

Permanent asymmetric rule:
- **Thumper/Crawler -> Pikmin:** no functional GrabPikmin / leader removal / grabbed death timer / broken-state effect.
- **Pikmin -> Thumper/Crawler:** normal LethalMin attack/latch behavior allowed.

S1.42L evidence:
- LethalMin registered Crawler as Pikmin enemy with 2 latch triggers;
- Pikmin runtime logs found Crawler targets;
- `[ThumperPikminGuard]` fired **36 times**;
- `Leader is null when following` count = **0**;
- user confirmed Pikmin can be thrown onto the Thumper and attack it normally;
- user confirmed Thumper snapping does not hold Pikmin and does not put them into a broken state.

Accepted cosmetic behavior:
the Thumper may still visibly snap/bite toward Pikmin.
This is harmless and should be ignored unless a future functional regression appears.
Do not spend additional patch complexity merely to suppress the animation.

### Puffer -> Pikmin

**PASS / CLOSED.**

Permanent rule:
Puffer attack/smoke does not affect Pikmin.

Retained:
- `Puffer Can Poison Pikmin = false`;
- local Puffer smoke guard removes LethalMin Pikmin effect/latch components from Puffer smoke only.

Validated in S1.42H and reconfirmed by user/runtime in later runs.

### Jetpack

**PASS / CLOSED.**

Accepted behavior:
- project-local loaded Jetpack Item target = approximately **140 seconds**;
- JetpackFixes `MidAirExplosions = Off`;
- no historical Coroner `PlayerController was null` flood.

Runtime marker:
`[Jetpack140] Jetpack battery duration changed 50 -> 140 seconds via loaded Item registry.`

User explicitly confirmed Jetpack behavior works and the task can be closed.

### Baboon Hawk -> Pikmin

**PASS / CLOSED.**

Permanent enemy-side rule:
Baboon Hawks must not target/chase/bite/grab/hold Pikmin.

Retained S1.42J architecture:
1. disable exact `LethalMin.BaboonBirdPikminEnemy` adapter one frame after exact `BaboonBirdAI.Start`;
2. block exact declared `BaboonBirdPikminEnemy.BitePikmin`;
3. retain common exact `PikminAI.GrabPikmin(Transform,float,int)` Baboon-Hawk failsafe.

S1.42L confirms:
- zero-interaction initialization succeeded;
- spawned Hawks repeatedly had the exact adapter disabled;
- `Leader is null when following` count = 0.

## 3. Only remaining active runtime gate

### Pikmin -> Baboon Hawk

Desired permanent rule:
**Pikmin must be able to be thrown onto Baboon Hawks and attack/latch them normally.**

S1.42L already prepares this:
- `Baboon hawk` is no longer in LethalMin's Pikmin Attack Blacklist;
- LethalMin registers:
  `Registered Baboon hawk As Pikmin Enemy, Added (1) latch triggers`.

But the latest S1.42L log contains no unambiguous direct Pikmin attack/latch marker for a Hawk, and the user has not explicitly confirmed this direction yet.

Therefore this direction is **PENDING** and must not be inferred PASS from registration alone.

### Exact next action

**Do not build another candidate. Keep using S1.42L.**

Import profile with:
**Gale -> Advanced options -> Import all files**

Deliberate focused test:
1. find/spawn a Baboon Hawk;
2. throw one or more Pikmin directly onto it;
3. confirm Pikmin latch/attack it normally;
4. confirm the Hawk itself still ignores Pikmin and does not target/chase/bite/grab/hold them;
5. confirm no `Leader is null when following` loop;
6. upload the complete fresh log to:
   `RuntimeInbox/Current/`.

Runtime router:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42L`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

## 4. S1.42L Attack Blacklist

Current:
`Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy`

This exactly matches the modern S1.40B/S1.41 baseline.

Recent project-added entries from the isolated enemy work:
- `Crawler` — added in S1.42C, now removed;
- `Baboon hawk` — added in S1.42J, now removed.

No recent project-added blacklist entry remains.

Historical caveat:
the old juijui profile had only `Docile Locust Bees,Manticoil`, but it belongs to a different historical LethalMin/mod environment and is not the modern restore baseline.

## 5. Temporary isolated enemy-test state

BCMER package:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Current S1.42L state:
**disabled**

EnemyIsolation:
**enabled**

Diagnostic spawn allowlist:
- indoor: Crawler/Thumper + Puffer;
- outdoor: Baboon Hawk;
- daytime: none;
- Pikmin-family entities preserved.

This state is temporary.

### After Pikmin -> Baboon Hawk passes

The isolated enemy interaction gate is complete.

Then:
1. disable/remove temporary EnemyIsolation;
2. restore normal enemy configuration from:
   `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve permanent accepted rules:
   - Baboon Hawk -> Pikmin blocked;
   - Pikmin -> Baboon Hawk attack/latch allowed;
   - Thumper/Crawler -> Pikmin broken grab state blocked;
   - Pikmin -> Thumper/Crawler attack/latch allowed;
   - Puffer -> Pikmin no effect.

Do not reconstruct normal enemy settings from memory. Use the restore baseline.

## 6. Restore baseline — do not remove

Canonical enemy restore point:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Readable snapshot:
`ProfileSources/S1.42C/`

The baseline is for normal enemy spawn/configuration ownership after removing the temporary isolation overlay. Later explicitly accepted permanent interaction changes from S1.42J-L must be preserved.

## 7. Superseded candidates / historical evidence

### S1.42I
Built successfully, **never runtime-tested**, superseded before test.

Profile:
`Profiles/LC V1 S1.42I Baboon Hawk Grab Guard.r2z`

SHA-256:
`c7224aea97c51fb051da059648868bbae0421b9c3f02d5cc2dd60922efc28a97`

Do not treat it as runtime evidence.

### S1.42K
Built successfully, **never runtime-tested**, superseded by the user's clarified requirement that Pikmin must also be able to attack Baboon Hawks.

Profile:
`Profiles/LC V1 S1.42K Thumper Pikmin Attack Restore.r2z`

SHA-256:
`bbdc949c9477e138cc3dde7c261f36f014cf482dd930c393ab035d80f8560aa2`

Do not treat it as runtime evidence.

## 8. Critical do-not-regress rules

- Do not reintroduce the S1.42D broad/inherited LethalMin reflection/Harmony scan; it caused a startup crash.
- Prefer exact declared types/methods and narrow runtime anchors.
- Do not create an Update-driven or continuous global EnemyAI scene scan for EnemyIsolation.
- Do not build a successor before current runtime evidence is evaluated unless S1.42L itself cannot start.
- Do not re-enable BCMER before the last isolated direction gate passes.
- Do not upgrade BCMER 1.71.0 to 2.0.0 without explicit user decision.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not restore/cite the intentionally deleted oversized evidence formerly at:
  `RuntimeEvidence/S1.42G/20260903T100914Z/`.
- Preserve clean S1.42G BCMER-off evidence:
  `RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`.
- Preserve S1.42H evidence:
  `RuntimeEvidence/S1.42H/20260903T125734Z/`.
- Preserve S1.42J and S1.42L evidence.
- Profiles containing the project-local DLL must be imported through Gale:
  **Advanced options -> Import all files**.
- S1.29D is diagnostic-only and must never become a gameplay base.
- Unknown Enemy PowerLevels must never be guessed.
- Prefer one positive spawn owner per enemy.
- `CodeRebirthLib` must not return.

## 9. Other accepted/persistent project rules

Retain unless explicitly changed:
- Malfunctions disabled;
- SCP999 disabled;
- Observer disabled;
- Don't Touch Me disabled;
- AJB Keep Hangar Ship Door Closed disabled while local failsafe exists;
- Ogopogo disabled;
- Vermin disabled;
- Leaf Boy remains on LethalMin Attack Blacklist;
- Autonomous Crane cannot kill Pikmin/Puffmin;
- recharge station full heal;
- Old Bird Resonance retained;
- Mirage recording retained;
- no natural CodeRebirth Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- LethalModDataLib 1.2.2 null-plugin guard retained and confirmed working.

BCMER 1.71.0 ownership guards to preserve after re-enable:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Disabled BCMER rain event routes:
- Raining;
- HeavyRain;
- AllWeather;
- Hurricane.

Natural vanilla Rainy remains allowed.

## 10. Lower-priority pending work after active gate

### BCMER
After re-enable, re-check the historical BCMER Door System ERROR / ship-door interaction.

### Functional Microwave
Volume accepted:
`Functional Microwave | Volume = 0.7`

Future requirement:
Microwaves should be somewhat rarer.
Exact rarity reduction is not selected.
Do not mix this balance change into the current isolated gate.

### Interiors
Binding long-term rule:
all registered interiors should have equal effective selection probability on every moon, including future additions, where technically safe/supported.

Target:
Weight 100 per interior/moon pairing.

Pending:
- normalize weights;
- CullFactory disable culling for exact IDs `junkrooms` and `shatteredrooms`;
- MelanieMausoleum fog reduction only in that interior;
- keep Shatteredrooms Experimentation/Embrion author block until technical safety is understood.

### Monitor-only
- Mineshaft elevator + many Pikmin floor-clipping/fall-death causality remains unproven.
- Outdoor Pikmin Sprout density is a subjective concern; do not rebalance without statistics.

## 11. Known noise — do not escalate without user-facing symptoms

- SoundAPI TypeLoadException during floor reporting;
- SoftMaskKiller-protected SoftMask NREs;
- duplicate NetworkPrefab GlobalObjectIdHash warnings;
- RuntimeNavMeshBuilder unreadable-mesh messages;
- BCMER ButlerSword missing-script warning;
- historical S1.42C scene-teardown `Collection was modified` exception;
- Pikmin/NavMesh agent warnings;
- Coroner Baboon-Hawk player-damage noise separate from the resolved Jetpack null flood.

## 12. Repository-first workflow

Canonical:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`
- `Patches/`

Do not ask the user for a local clone or local PowerShell build while the required base/build infrastructure exists in GitHub.

At this handover:
`RuntimeInbox/Current/` contains only `.gitkeep`; the latest S1.42L log has already been ingested.

## 13. Deferred repository optimization

Plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Status:
**DEFERRED_UNTIL_ACTIVE_GATE_COMPLETE**

Do not perform the structural migration while the last Pikmin -> Baboon Hawk runtime sub-gate is open.

After that gate is evaluated and the resulting normal-enemy/BCMER state is documented, re-check the then-current repository and, if no critical gameplay/build gate is half-finished, perform the migration as a separate maintenance phase.

No destructive Git history rewrite, filter-repo/BFG, Git LFS migration, or external-storage migration without explicit user approval.

## 14. Read order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/45_HANDOVER_S1.42L_TO_NEXT_FINAL.md`
3. `Current/Projektstatus_S1.42L.json`
4. `Current/43_S1.42L_RUNTIME_ANALYSIS_THUMPER_CLOSED.md`
5. `Current/41_S1.42L_PIKMIN_COUNTERATTACK_RESTORE_BUILD.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/VERIFIKATION_S1.42L.txt`
10. `Current/SHA256SUMS_S1.42L.txt`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
13. `Current/02_TECHNICAL_BASELINE.md`
14. `BuildSpecs/current.json`
15. `RuntimeInbox/ACTIVE_BUILD.txt`
16. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## 15. Immediate next step in one sentence

**Use S1.42L unchanged and explicitly validate only Pikmin -> Baboon Hawk attack/latch while confirming the Hawk-side ignore guard remains intact; do not build, restore BCMER/enemies, or start repository migration before that evidence is evaluated.**
