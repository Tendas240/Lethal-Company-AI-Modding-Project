# 36 — Handover S1.42J to Next Chat

**Date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository is the source of truth:** https://github.com/Tendas240/Lethal-Company-AI-Modding-Project

## 1. Canonical current state

### Last fully accepted gameplay baseline

Build:
**S1.41**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:
**accepted gameplay baseline**

### Most recent valid runtime evidence

Build:
**S1.42H**

Evidence:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

Log SHA-256:
`81ed064ce97d25f250d6fba1585055baef8ce801cd0f13626d074bf4fef71029`

S1.42H runtime conclusions:
- exact common `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` hook loaded exactly once and startup was safe;
- isolated enemy spawning worked with BCMER disabled;
- the in-game `Enemies` terminal command displayed enemies according to the user's direct gameplay observation;
- Puffer smoke -> Pikmin passed;
- Baboon Hawk + invincible Pikmin failed because the enemy-side hold/re-grab loop persisted;
- direct Thumper/Crawler <-> Pikmin contact was not validated in that run;
- Coroner's historical Jetpack `PlayerController was null` flood remained absent;
- the BCMER-related zero-power ship-door flood did not reproduce while BCMER was disabled.

Key Baboon Hawk counts from S1.42H:
- 64 BitePikmin calls;
- 64 pre-grab captures;
- 59 grabbed states;
- 59 grabbed death timers;
- 59 invincibility-blocked kill attempts;
- 56 state repairs;
- 193 `Leader is null when following` errors.

### Superseded intermediate candidate

Build:
**S1.42I**

Profile:
`Profiles/LC V1 S1.42I Baboon Hawk Grab Guard.r2z`

SHA-256:
`c7224aea97c51fb051da059648868bbae0421b9c3f02d5cc2dd60922efc28a97`

Status:
**built successfully but never runtime-tested**

Reason for supersession:
the user changed the desired behavior before testing S1.42I. Instead of only preventing the broken invincible-Pikmin grab state, Baboon Hawks and Pikmin must now completely ignore each other.

Do not treat S1.42I as runtime evidence.

### Current built candidate / active runtime gate

Build:
**S1.42J — Baboon Hawk Zero Interaction**

Profile:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Compatibility plugin:
**v1.3.7**

Compatibility DLL SHA-256:
`7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

LethalMin config SHA-256:
`f7b2698171d9d6a7b6c2e7b415ff2cb2c63459fb267ff0807ebe0f4bcf3e0bd3`

Export SHA-256:
`89e03afcf1bc9b3390969f83709ad04dca865743de6249af0dde642d0e3e6fe5`

Build verification:
- GitHub Actions: success;
- 0 warnings;
- 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only:
  - `BepInEx/config/NoteBoxz.LethalMin.cfg`
  - `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
  - `export.r2x`;
- no added members;
- 188 packages total;
- 182 enabled;
- 6 disabled;
- BCMER 1.71.0 disabled.

Readable snapshot:
`ProfileSources/S1.42J/`

## 2. Binding enemy interaction rules

These are project requirements, not temporary diagnostics.

### Thumper / Crawler <-> Pikmin

**Zero interaction in both directions.**

Required:
- Thumper/Crawler must not grab, bite, remove leader, or start a grabbed death timer on Pikmin;
- Pikmin must not attack/latch onto Crawler;
- `Crawler` remains in LethalMin's Pikmin `Attack Blacklist`.

Expected runtime marker:
`[ThumperPikminGuard] Blocked Crawler/Thumper -> Pikmin GrabPikmin before leader/grab/death-timer state mutation.`

Runtime status:
**fix built, deliberate S1.42J direct-contact validation still pending.**

### Baboon Hawk <-> Pikmin

**Zero interaction in both directions.**

Reason:
Pikmin are intended to be invincible. Allowing Baboon Hawks to target/chase Pikmin while the final grab is blocked wastes AI behavior and can create interaction loops.

S1.42J implementation:
- disable exact `LethalMin.BaboonBirdPikminEnemy` adapter one frame after exact declared `BaboonBirdAI.Start`;
- directly block exact declared `BaboonBirdPikminEnemy.BitePikmin`;
- common exact `PikminAI.GrabPikmin` patch blocks Baboon Hawk-owned grabs as a final failsafe for all Pikmin;
- exact runtime enemy name `Baboon hawk` added to LethalMin `Attack Blacklist`, preventing Pikmin -> Baboon Hawk attack/latch;
- no broad/inherited LethalMin Harmony scan.

Expected startup marker:
`[BaboonHawkPikminGuard] Zero-interaction initialized; bitePatched=True; baboonStartPatched=True; declaredPikminMethods=[...].`

Expected per-Hawk marker:
`[BaboonHawkPikminGuard] Disabled LethalMin.BaboonBirdPikminEnemy on BaboonHawkEnemy(Clone). Baboon Hawk -> Pikmin targeting/chase/bite adapter is inactive.`

Failsafe markers should ideally not be required during normal zero-interaction:
`[BaboonHawkPikminGuard] Blocked LethalMin BaboonBirdPikminEnemy.BitePikmin. Baboon Hawks must ignore Pikmin completely.`

`[BaboonHawkPikminGuard] Blocked Baboon Hawk -> Pikmin GrabPikmin failsafe before hold/leader/death-timer state mutation.`

Runtime status:
**S1.42J not tested yet.**

### Puffer -> Pikmin

**Puffer attack/smoke must not affect Pikmin.**

Retained:
- `Puffer Can Poison Pikmin = false`;
- project-local smoke guard removes LethalMin Pikmin effect/latch components from Puffer smoke.

S1.42H evidence:
- two Puffer spawns;
- first guard activation removed 3 relevant components;
- second removed 2;
- user observed the smoke cloud and no Pikmin effect.

Status:
**PASS. Do not force another Puffer test unless convenient.**

## 3. Temporary isolated enemy test state

S1.42J is still an isolated diagnostic candidate.

BCMER:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Current S1.42J state:
**disabled**

EnemyIsolation:
**enabled**

Diagnostic allowlist:
- indoor: Crawler/Thumper + Puffer;
- outdoor: Baboon Hawk;
- daytime: none;
- Pikmin-family entities remain allowed.

Important:
this is temporary test state, not the final normal enemy configuration.

After the isolated gate passes:
1. disable/remove temporary EnemyIsolation;
2. restore the normal enemy configuration using:
   `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
3. re-enable exact BCMER 1.71.0;
4. preserve later explicitly accepted permanent gameplay rules such as Thumper/Pikmin and Baboon-Hawk/Pikmin zero interaction.

Do not reconstruct normal enemy settings from memory. Use the restore baseline.

## 4. Exact next action

**Runtime-test S1.42J. Do not build S1.42K first.**

Import:
**Gale -> Advanced options -> Import all files**

Primary test:
1. reach Main Menu and host successfully;
2. route/land on a normal moon;
3. verify no periodic routed-moon freeze regression;
4. verify `Enemies` still displays diagnostic targets;
5. deliberately place Pikmin around one or more Baboon Hawks;
6. Baboon Hawks must ignore Pikmin: no target/chase/bite/grab/hold behavior;
7. Pikmin must not attack/latch Baboon Hawks;
8. verify the S1.42J Baboon adapter-disable marker;
9. deliberately let a Crawler/Thumper cross into a Pikmin group;
10. verify Thumper/Crawler and Pikmin ignore each other in both directions and the Thumper guard marker appears;
11. Puffer only needs a spot-check if conveniently encountered;
12. upload the complete fresh log to:
   `RuntimeInbox/Current/`

Runtime routing is already configured:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42J`

Build controller is already idle:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`

## 5. Important do-not-regress / do-not-repeat rules

- **Do not reintroduce the S1.42D broad reflection/Harmony scan.**
  S1.42D startup-crashed after scanning inherited/non-declared Pikmin methods.
- Patch exact declared methods/types only when possible.
- Do not create an Update-driven global EnemyAI scene scan for EnemyIsolation.
- Do not treat S1.42I as runtime-tested.
- Do not restore BCMER before the isolated S1.42J enemy gate passes.
- Do not migrate BCMER from exact 1.71.0 to 2.0.0 without an explicit project decision.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not restore or cite the intentionally deleted oversized evidence formerly under:
  `RuntimeEvidence/S1.42G/20260903T100914Z/`
- Keep the clean valid S1.42G BCMER-off retest:
  `RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`
- Keep the valid S1.42H runtime evidence:
  `RuntimeEvidence/S1.42H/20260903T125734Z/`
- Do not ask the user for a local clone or local PowerShell build while the required base and GitHub build infrastructure exist.

## 6. Other retained project requirements / open work

### Functional Microwave

Current:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

Future user requirement:
Functional Microwaves should be somewhat rarer.

Exact rarity reduction is not yet selected.
Do not change rarity during the S1.42J isolated enemy gate.

### Jetpack

Target derived from historical juijui config evidence:
**140 seconds**

Current retained configuration:
- ButteRyBalance `Reduce Battery = false`;
- project-local loaded Jetpack Item target = 140 seconds;
- JetpackFixes `MidAirExplosions = Off`.

Still requires representative runtime validation for:
- approximately 140-second duration;
- no self-explosion from sustained/high-speed normal boost.

Historical reference:
`Current/18_JUIJUI_LEGACY_REFERENCE.md`

### Interiors

Binding long-term rule:
all registered interiors should have equal effective selection probability on every moon where technically safe/supported.

Target:
weight 100 per interior/moon pairing.

Pending:
- CullFactory: disable culling for exact IDs `junkrooms` and `shatteredrooms`;
- MelanieMausoleum: reduce fog specifically in that interior, not globally;
- author hard exclusions remain compatibility questions until safety is understood.

### BCMER final state

Pinned:
**1.71.0**

Carry-forward ownership guards:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Disabled BCMER rain-event routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy remains allowed.

EventType distribution:
all 8 categories = 12.5%.

Keep:
`Use custom weights? = false`

Scale:
`12.5, 0, 12.5, 12.5`

### Other persistent guards

Keep:
- Malfunctions disabled;
- SCP999 disabled;
- Observer disabled;
- Don't Touch Me disabled;
- AJB Keep Hangar Ship Door Closed disabled while local failsafe exists;
- CodeRebirthLib must not return;
- LethalModDataLib remains required with project-local null-plugin guard;
- Ogopogo disabled;
- Vermin disabled;
- Leaf Boy remains LethalMin Attack Blacklist;
- Autonomous Crane cannot kill Pikmin/Puffmin;
- recharge station full heal;
- Old Bird Resonance retained;
- Mirage recording retained;
- no natural CodeRebirth Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret.

## 7. Known noise / monitor-only

Only escalate with user-visible symptoms:
- SoundAPI TypeLoadException during floor reporting;
- SoftMaskKiller-protected SoftMask NREs;
- duplicate NetworkPrefab GlobalObjectIdHash warnings;
- RuntimeNavMeshBuilder unreadable-mesh messages;
- BCMER ButlerSword missing-script warning;
- S1.42C scene-teardown `Collection was modified` exception;
- Pikmin/NavMesh agent warnings;
- Coroner Baboon-Hawk player-damage noise is separate from the resolved historical Jetpack `PlayerController was null` flood.

Monitor-only gameplay observations:
- Mineshaft elevator + many Pikmin floor-clipping/fall-death incident;
- subjective outdoor Pikmin Sprout density concern.

## 8. Repository-first workflow

Canonical build infrastructure:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Profiles containing the project-local DLL must be imported with:
**Gale -> Advanced options -> Import all files**

Runtime itself is the only unavoidable local step.

## 9. Pending repository optimization / migration

A repository-architecture optimization has been reviewed and is **recommended**, but it must **not** be executed before the active S1.42J runtime gate is evaluated.

Canonical migration plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Core target:
**small canonical Current context + targeted retrieval from complete historical/evidence sources.**

Important migration rules:
- first finish the current critical runtime/build gate and document the resulting canonical state;
- then perform the migration as a dedicated repository-maintenance phase, avoiding unrelated gameplay/balance work during the structural change;
- introduce stable canonical paths such as a machine-readable project state and read order;
- archive historical Current generations instead of deleting them;
- extend existing profile/runtime indexing rather than creating competing parallel index systems;
- preserve raw RuntimeEvidence and failed approaches;
- do not aggressively deduplicate ProfileSources merely because identical paths repeat: Git already deduplicates identical blobs internally;
- no destructive Git history rewrite, LFS migration, or external-storage migration without explicit user approval;
- implement a repository validator and bootstrap test as part of the later migration.

A future chat must re-check the then-current repository state before starting this migration. Do not assume S1.42J is still current merely because the migration plan was authored during the S1.42J gate.

## 10. Read order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/36_HANDOVER_S1.42J_TO_NEXT.md`
3. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
4. `Current/33_S1.42J_BABOON_HAWK_ZERO_INTERACTION_BUILD.md`
5. `Current/32_S1.42H_RUNTIME_ANALYSIS_AND_S1.42I_BUILD.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/Projektstatus_S1.42J.json`
10. `Current/VERIFIKATION_S1.42J.txt`
11. `Current/SHA256SUMS_S1.42J.txt`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

When newer valid runtime evidence appears, it supersedes this handover's pending-test statements.
