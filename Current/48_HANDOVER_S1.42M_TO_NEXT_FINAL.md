# 48 — FINAL HANDOVER — S1.42M to next ChatGPT

**Date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

This file is the canonical detailed handover for the current open runtime gate.

---

## 1. State separation — do not conflate these

### Last fully accepted gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

This is still the last fully accepted normal-gameplay baseline.

### Latest valid runtime evidence

**S1.42L**

Evidence:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Raw log:
`RuntimeEvidence/S1.42L/20260903T155132Z/raw/LogOutput.log`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

This run closed the live Pikmin -> Baboon Hawk attack/latch gate, but exposed a new death-cleanup/corpse regression.

### Current built candidate awaiting runtime

**S1.42M — Baboon Hawk Death Cleanup**

Profile:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Base:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

Base SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Status:
**BUILT / NOT YET RUNTIME-TESTED**

---

## 2. S1.42L runtime result that opened S1.42M

Detailed analysis:
`Current/47_S1.42L_BABOON_ATTACK_PASS_DEATH_REGRESSION_ANALYSIS.md`

The user explicitly confirmed:
- Pikmin can again be thrown onto a living Baboon Hawk;
- Pikmin latch normally;
- Pikmin attack normally;
- Pikmin can kill the Hawk.

Therefore:
**Pikmin -> living Baboon Hawk attack/latch is PASS/CLOSED.**

The Hawk-side protection also remains accepted:
**Baboon Hawk -> Pikmin is PASS/CLOSED.**

Latest log:
- `Leader is null when following` = 0;
- after Hawk death, Pikmin continued acting against the old dead `BaboonHawkEnemy(Clone)`;
- SellBodies generated `BaboonHawkBody(Clone)`;
- living Hawks logged three grabs of that corpse item;
- `ShipOnion: saved 35 pikmin to disk on despawn` later appeared.

User-visible regression:
- Pikmin latched to the Hawk disappeared when it died;
- the dead Hawk body did not stay where expected.

The important clarification is that the SellBodies corpse **must not be disabled**. The corpse is supposed to remain a carryable item that Pikmin can transport to the Onion.

---

## 3. Binding Baboon Hawk / Pikmin rules

These are the desired permanent rules unless the user explicitly changes them later.

### Living Hawk -> Pikmin

**Blocked.**

The Hawk must not:
- target;
- chase;
- bite;
- grab;
- hold Pikmin.

### Pikmin -> living Hawk

**Allowed.**

Pikmin must be able to:
- be thrown onto the Hawk;
- latch;
- attack;
- kill it normally.

### Hawk death / corpse

When a Hawk dies:
- Pikmin latched to it must cleanly leave the stale attack/latch task;
- those Pikmin must remain visible and usable;
- SellBodies must still create/retain the Dead Baboon Hawk body;
- players may carry the corpse;
- Pikmin may carry the corpse;
- Pikmin must be able to carry it toward the Onion;
- living Baboon Hawks must not pick up or relocate the corpse.

Do not restore the historical S1.42J two-way zero-interaction rule.

---

## 4. S1.42M implementation

Compatibility plugin:
**S1.39 Compatibility Fixes v1.3.8**

Source:
`Patches/S139CompatibilityFixes/Plugin.cs`

Embedded DLL SHA-256:
`47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Build document:
`Current/46_S1.42M_BABOON_HAWK_DEATH_CLEANUP_BUILD.md`

Implementation is deliberately narrow:

1. exact declared `BaboonBirdAI.KillEnemy(bool)` postfix;
2. runtime resolution of exact declared `LethalMin.PikminAI.RemoveCurrentTask()`;
3. only Pikmin under the specific dying Hawk hierarchy are released;
4. exact declared `BaboonBirdAI.CanGrabScrap(GrabbableObject)` postfix;
5. only `BaboonHawkBody` / `Dead Baboon Hawk` is rejected for living-Hawk scrap pickup.

The corpse remains otherwise usable by players/Pikmin.

### Anti-regression architecture

Do **not** replace this with:
- broad/inherited LethalMin reflection/Harmony scanning;
- a scene-wide Pikmin scan;
- a continuous Update-driven EnemyAI/Pikmin scan.

S1.42D proved broad inherited LethalMin scanning can crash at startup.

---

## 5. S1.42M build verification

Final successful GitHub Actions run:
**Build canonical profile #42**

Final build:
- success;
- 0 compiler warnings;
- 0 compiler errors;
- 331 archive members;
- 330 readable snapshot files;
- changed existing archive members only:
  - `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
  - `export.r2x`;
- no added archive members.

Readable snapshot:
`ProfileSources/S1.42M/`

Build result:
`Current/AUTO_BUILD_RESULT.json`
`Current/AUTO_BUILD_RESULT.md`

Verification:
`Current/VERIFIKATION_S1.42M.txt`

Hashes:
`Current/SHA256SUMS_S1.42M.txt`

### Non-gameplay build-attempt note

The first S1.42M Actions attempt (#41) failed only because a build-spec text assertion used an overly strict regex for the LethalMin Attack Blacklist. No failed gameplay profile was committed from that run.

The assertion was changed to the equivalent exact containment check. Run #42 then succeeded.

Do not treat run #41 as a gameplay/runtime failure.

---

## 6. Config delta / temporary state

The following S1.42M configs are byte-identical to S1.42L:
- `BepInEx/config/NoteBoxz.LethalMin.cfg`
- `BepInEx/config/Entity378.sellbodies.cfg`
- `BepInEx/config/tendas.s139.compatibilityfixes.cfg`

Therefore:

### EnemyIsolation
**enabled**

### BCMER
Exact package:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Current state:
**disabled**

Do not silently upgrade BCMER to 2.0.0.

### SellBodies
Baboon Hawk corpse generation:
**enabled**

### LethalMin Attack Blacklist

Current:
`Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy`

Neither Crawler nor Baboon hawk is blacklisted.

---

## 7. Controllers — current exact state

Runtime router:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`

Build controller:
`BuildSpecs/current.json`

Current build-controller state:
- `enabled = false`
- `build_id = IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`
- base profile = S1.42M
- base SHA-256 = `9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Do **not** build S1.42N before S1.42M runtime evidence is evaluated unless S1.42M cannot start.

`RuntimeInbox/Current/` is currently expected to contain only `.gitkeep` until the user uploads the next log.

---

## 8. Exact next test

Import S1.42M using:

**Gale -> Advanced options -> Import all files**

Then:

1. find/spawn a Baboon Hawk;
2. throw multiple Pikmin directly onto the living Hawk;
3. verify normal latch/attack still works;
4. let the Pikmin kill it;
5. immediately verify those Pikmin detach/remain visible and usable;
6. wait at least 5 seconds so the SellBodies corpse replacement has definitely occurred;
7. verify the Dead Baboon Hawk body remains at/near the death location;
8. throw Pikmin onto the dead body;
9. verify the Pikmin can carry the corpse toward the Onion;
10. if another living Hawk is present, verify it does **not** pick up the corpse;
11. verify living Hawk -> Pikmin ignore remains intact;
12. verify there is no `Leader is null when following` loop;
13. upload the complete fresh `LogOutput.log` to:
    `RuntimeInbox/Current/`.

No build change is required before this test.

---

## 9. What happens after S1.42M PASS

Only after the S1.42M gate passes:

1. disable/remove temporary EnemyIsolation;
2. restore normal enemy spawning/config exactly from:
   `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric interaction rules plus the S1.42M corpse rule;
5. runtime-check the restored normal state;
6. specifically monitor the historical BCMER Door System ERROR / ship-door interaction;
7. document the restored normal-enemy/BCMER state;
8. only then reconsider repository optimization/migration.

Do not reconstruct normal enemy settings from memory.

---

## 10. Required restore baseline

Canonical enemy restore point:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Readable snapshot:
`ProfileSources/S1.42C/`

This file must not be removed.

---

## 11. Closed/PASS topics

Do not reopen these unless a regression appears:

- Thumper/Crawler -> Pikmin broken grab-state protection;
- Pikmin -> Thumper/Crawler normal attack/latch;
- Puffer -> Pikmin immunity;
- Jetpack ~140-second target / MidAirExplosions Off;
- Baboon Hawk -> Pikmin ignore protection;
- Pikmin -> living Baboon Hawk attack/latch.

Accepted Thumper caveat:
the Thumper may visibly snap/bite toward Pikmin, but if no Pikmin is held or broken this is accepted harmless cosmetic/AI behavior.

---

## 12. Important historical failures / do not regress

- **S1.42D:** broad/inherited LethalMin reflection/Harmony scan caused startup crash.
- **S1.42E:** EnemyIsolation parameterless `SpawnableEnemyWithRarity` construction caused periodic Gordion freezes.
- **S1.42F:** continuous global `FindObjectsOfType<EnemyAI>()` still caused routed-moon freezes; Coroner Jetpack null spam was also identified.
- Coroner faulty Jetpack detector must remain selectively guarded, not Coroner removed wholesale.
- Adapter-only LethalMin grabbed-state repair was insufficient; common exact `PikminAI.GrabPikmin(Transform,float,int)` was required.
- `CodeRebirthLib` is a permanent no-return rule.
- S1.29D is diagnostic-only and must never become gameplay base.
- Unknown Enemy PowerLevels must never be guessed.
- Prefer one positive spawn owner per enemy.
- Do not restore/cite deleted oversized evidence:
  `RuntimeEvidence/S1.42G/20260903T100914Z/`.

Preserve:
- `RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`
- `RuntimeEvidence/S1.42H/20260903T125734Z/`
- S1.42J evidence
- both S1.42L evidence sets.

Superseded/unvalidated builds remain historical only:
- S1.42I — built, never runtime-tested;
- S1.42K — built, never runtime-tested.

---

## 13. Persistent project rules

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
- recharge station full heal intended/retained;
- Old Bird Resonance retained;
- Mirage recording retention retained;
- no natural CodeRebirth Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- LethalModDataLib 1.2.2 null-plugin guard retained.

BCMER 1.71.0 ownership guards to preserve after re-enable:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Disabled BCMER rain event routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy remains allowed.

---

## 14. Deferred lower-priority work

Do not mix these into the open S1.42M gate.

### Functional Microwave
Accepted volume:
`Functional Microwave | Volume = 0.7`

Future request:
microwaves should become somewhat rarer.
Exact target not chosen.

### Interiors
Binding long-term invariant:
all registered interiors should have equal effective selection probability on every moon where technically safe/supported, including future interiors.

Common target:
Weight 100.

Pending:
- normalize interior weights;
- CullFactory exact IDs `junkrooms`, `shatteredrooms`;
- MelanieMausoleum fog reduction only in that interior;
- retain Shatteredrooms Experimentation/Embrion safety block until understood.

### Monitor-only
- Mineshaft elevator + many Pikmin floor-clipping/fall-death causality unproven;
- outdoor Pikmin Sprout density subjective; do not rebalance without statistics.

---

## 15. Deferred repository maintenance / known non-functional drift

Plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Status:
**DEFERRED_UNTIL_ACTIVE_GATE_COMPLETE**

Known non-functional drift:
- `Current/02_TECHNICAL_BASELINE.md` contains older "current" wording in historical subsections;
- `Patches/S139CompatibilityFixes/Plugin.cs` still contains some stale S1.42J-era comments in untouched historical sections describing two-way zero interaction / old blacklist assumptions.

Important:
- actual S1.42M code path/config is the authoritative functional state;
- do not perform broad cleanup while S1.42M runtime validation is open;
- clean these comments/docs later during repository maintenance.

Prefer ARCHIVE over DELETE.
No destructive history rewrite, filter-repo/BFG, Git LFS migration, or external-storage migration without explicit approval.

---

## 16. Repository-first operating model

Use GitHub as the canonical build/workspace.

Relevant infrastructure:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `.github/workflows/profile-index.yml`
- `.github/workflows/runtime-ingest.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`
- `Patches/`

Do not ask the user for a local clone or local build while the required base and build infrastructure exist in the repository.

---

## 17. Read order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md`
3. `Current/Projektstatus_S1.42M.json`
4. `Current/47_S1.42L_BABOON_ATTACK_PASS_DEATH_REGRESSION_ANALYSIS.md`
5. `Current/46_S1.42M_BABOON_HAWK_DEATH_CLEANUP_BUILD.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/VERIFIKATION_S1.42M.txt`
10. `Current/SHA256SUMS_S1.42M.txt`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
13. `Current/02_TECHNICAL_BASELINE.md`
14. `BuildSpecs/current.json`
15. `RuntimeInbox/ACTIVE_BUILD.txt`
16. `Current/49_REPOSITORY_HANDOVER_AUDIT_S1.42M.md`
17. `Current/Aktive_Modliste_S1.42M.txt`
18. `Current/DATEIINVENTAR_S1.42M.txt`
19. `Current/README_Handover_S1.42M.txt`
20. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

---

## 18. Immediate next step in one sentence

**Runtime-test S1.42M unchanged: confirm Pikmin survive/detach when they kill a Baboon Hawk, the SellBodies corpse remains Pikmin-carryable to the Onion, living Hawks do not carry that corpse, and Hawk -> Pikmin ignore still works; then commit the full fresh log to `RuntimeInbox/Current/`.**
