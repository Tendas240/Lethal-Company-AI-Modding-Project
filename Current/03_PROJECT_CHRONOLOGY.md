# 03 — Project Chronology

This is a technical reconstruction of confirmed project history, not a verbatim transcript. Newer confirmed runtime evidence overrides older assumptions.

## S1.2 — profile/path-length stabilization
Long Gale names caused Windows/BepInEx path trouble. Permanent rule: keep profile names reasonably short.

## S1.3-S1.10 — early cleanup and ownership work
Wild Pikmin/falloff, stamina, batteries, facility distribution and obsolete/broken mods were cleaned up. Gnomes were removed after V81 `PlayerIsTargetable` MissingMethod spam. Peepers enemy/hazard was removed. LLL was proven not to be the only spawn authority.

## S1.11-S1.14 — spawn-owner isolation
A central LLL-only approach failed for some enemies. Rolling Giant, Shy Guy/Scopophobia and Siren Head returned to native spawn configuration. Persistent rule: prefer one positive spawn owner per enemy.

## S1.15-S1.23 — gameplay stabilization
Rolling Giant movement tuned, RandomEnemiesSize added, Company automation went through failed AutoCompanyBuilding/RandomMoonFX attempts, and CompanyBuildingEnhancements 2.6.0 became the accepted solution. LethalHUD Hold-to-Scan replaced old Hold_Scan_Button. Pikmin water resistance was confirmed.

## S1.24-S1.28 — roster, balance and interiors
Enemy roster restored, reference spawn screenshots became binding, Immortal Snail max set to 2, and 26 intended interiors established at equal Weight 100. Black Mesa integrated through its own DawnLib/config path.

## S1.29 / S1.29D — CodeRebirth and Power audit
CodeRebirth 1.6.9 integrated. S1.29D is diagnostic-only and must never become a gameplay base.

## S1.30 — power caps, Mimicless, Pikmin shield
Mimics/CoronerMimics removed; CodeRebirth/Pikmin compatibility toggles set false; indoor caps raised, then judged dense.

## S1.31 — indoor power trim
All controllable indoor caps reduced by 4. Runtime exposed the Leaf Boy/Pikmin endless attack loop and SCP999 startup NRE.

## S1.32 — Leaf Boy + Mirage + ship-door lockout
`Leaf boy` appended to LethalMin Attack Blacklist. Mirage retention requested. A closed ship-door lockout was observed; exact close actor remained unproven, but AJB's unconditional power refill caused permanent outside lockout.

## S1.33-S1.35 — local door/EnemyScan patch development
AJB disabled. First local DLL was not imported by normal Gale import, so early behavior was not a valid runtime test. Plugin was rebuilt for V81 with ship-door anti-lockout, DoorAudit and complete EnemyScan. Standalone fallback package created.

## S1.36 — clean baseline and accepted local-patch runtime
ProjectSCP-SCP999 disabled. User imported using Gale `Advanced options -> Import all files`. Runtime confirmed:
- local compatibility plugin loaded;
- ship-door behavior worked as intended;
- terminal `enemies` matched runtime enemy population;
- Pikmins were no longer affected by CodeRebirth microwaves.

These are accepted unless regression evidence appears.

## S1.37 — normal-scrap Currency filtering
Cumulative plugin temporarily removes Coin, Crisp Dollar Bill, Wayfarer's Wallet and Credit Pad 100/500/1000cc from `RoundManager.SpawnScrapInLevel`, then restores them so dedicated CodeRebirth systems remain registered.

Later runtime showed Currency could still appear through another path.

## S1.38 — 1440p + Old-Bird-only Resonance
Added FixCameraResolution 1.5.3, Lethal Resonance 4.7.8 and SoundAPI_LethalCompany 1.0.2. Fixed 2560x1440 accepted visually. Only Old Bird / footsteps / speaker groups enabled. Mirage `neverDeleteRecordings=true` required manual setting after import. Cabinet was identified from runtime as the four-legged Jester-like enemy.

Currency objects still appeared. User also requested natural Flash Turret removal, Ogopogo/Vermin removal and reported Autonomous Crane could still kill Pikmin.

## S1.39 — broader cleanup + direct Pikmin kill shield
Added:
- `OgopogoEnabled=false`
- `EnableVermin=false`
- defensive late Currency/Flash Turret map-object filtering
- S1.37 normal-scrap Currency filter retained
- direct CodeRebirth utility-kill Pikmin/Puffmin guard
- GeneralImprovements health recharge config carry-forward
- S1.38 camera/audio carry-forward

Runtime proved `S1.39 Compatibility Fixes loaded.`, but natural Coins/Wallets still spawned. Therefore late `RoundManager/SelectableLevel` map-object filtering was confirmed insufficient for DawnLib-native Currency.

## S1.40 — native CodeRebirth/DawnLib config attempt
Built from exact S1.39 archive and added `BepInEx/config/CodeRebirth.cfg` with:
- blank Coin/Bill/Wallet inside weights;
- Flash Turret `Is Inside Hazard=false`;
- blank Flash Turret inside weights.

An early run found Wallet + Flash Turret; the user later suspected `Import all files` may have been omitted on that import. Additional runs did not visually find Currency but still found a Flash Turret. Runtime logs contained Currency clone instances.

The decisive post-run config showed the sparse overrides did not survive startup:
- `Clean Unusued Configs=true`
- Flash Turret back to `Is Inside Hazard=true`
- positive Currency moon curves restored.

S1.40 is therefore a failed acceptance candidate.

## S1.40A — cleanup retention only; still failed

S1.40A added:

`Clean Unusued Configs=false`

while retaining blank Currency inside weights and Flash Turret suppression.

Corrected migrated profile:

`Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`

SHA-256:

`0245e0c5551d77cab7f90eacf7f1627b0a6df62553260533a4e903d2a6426f27`

Historical note: an earlier pre-correction S1.40A archive variant had a different hash and should not be treated as the canonical migrated binary.

Runtime showed:
- `Clean Unusued Configs=false` now survived;
- but Coin/Bill/Wallet/Flash Turret still had per-content `Allow Editing Config=false`;
- DawnLib therefore continued to enforce author defaults;
- Currency/Flash Turret still appeared.

S1.40A failed acceptance.

## S1.40B — DawnLib per-content editing gate fix

S1.40B opened the relevant editing gates while retaining the natural-spawn suppression:

- Coin `Allow Editing Config=true`
- Crisp Dollar Bill `Allow Editing Config=true`
- Wallet `Allow Editing Config=true`
- Flash Turret `Allow Editing Config=true`
- Currency inside moon/interior weights blank
- Flash Turret `Is Inside Hazard=false`
- Flash Turret inside moon/interior weights blank
- `Clean Unusued Configs=false`

Profile:

`Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z`

SHA-256:

`fd303f73f0f2223a6375fcf2b7ed209dae77e1934e3b4e8139932a89e7de7eb9`

Runtime:
- user did not encounter the unwanted natural Currency/Flash Turret;
- prior natural Currency clone signatures were absent in the evaluated log;
- intended post-run config values survived.

**S1.40B accepted.**

## Repository-first migration

During the S1.40B/S1.41 transition, the project moved from user-run local PowerShell profile builds to a GitHub-first build architecture.

Added:
- `BuildSpecs/`
- `BuildSystem/`
- `.github/workflows/profile-build.yml`
- `.github/workflows/profile-index.yml`
- `.github/workflows/runtime-ingest.yml`
- `ProfileSources/`
- `RuntimeInbox/`
- `RuntimeEvidence/`

Exact S1.40B and S1.41 binaries were uploaded once, hash-verified and indexed. Future profile builds should occur in GitHub Actions rather than through a local repository clone.

## S1.41 — BCMER 1.71.0 reactivation

Built from accepted S1.40B.

Exact:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

was enabled.

BCMER 2.0.0 was deliberately not adopted.

Ownership guard:

```ini
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false
Enable Randomizer? = false
```

Disabled BCMER rain-event routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Runtime on 2026-09-02:
- exact BCMER 1.71.0 loaded and finished patching;
- ordinary events ran;
- ownership guard survived post-run;
- all four BCMER rain routes stayed disabled;
- S1.40B CodeRebirth natural Currency/Flash-Turret suppression survived;
- no severe BCMER regression was observed.

Evidence:

`RuntimeEvidence/S1.41/20260902T215804Z/`

**S1.41 accepted.**

A separate non-blocking incident occurred in the Mineshaft elevator: the player clipped through the floor while descending with many Pikmin and died from fall damage. Nearby logs contained heavy NavMesh-agent creation failures. Causality remains unproven and BCMER is not implicated.

## Historical binding sequence at the S1.41 -> S1.42A transition

1. Freeze accepted S1.41 as the current gameplay baseline.
2. Fresh-audit the eight planned interior packages and dependencies.
3. Build S1.42A Interior Config Seed through GitHub Actions.
4. Import with Gale `Advanced options -> Import all files`.
5. Main Menu -> host/load -> land -> let a dungeon generate -> exit.
6. Upload full `BepInEx/config/` ZIP + `LogOutput.log` to `RuntimeInbox/Current/`.
7. Analyze actual generated IDs/config sections and CullFactory identifiers.
8. Build tuned S1.42.
9. Runtime-test S1.42.

See:
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
- `Current/12_HANDOVER_S1.41_TO_S1.42A.md`
- `BuildSpecs/S1.42A_PLAN.md`


## S1.42A — Interior Config Seed

Built repository-first from accepted S1.41.

Profile:
`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:
`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Added eight requested interior packages plus required LethalModDataLib 1.2.2.

Runtime evidence:
`RuntimeEvidence/S1.42A/20260902T224318Z/`

Result:
- 52 ExtendedDungeonFlows total vs 26 in S1.41;
- 26 new flows discovered;
- real config/weight/ID generation succeeded;
- exact CullFactory IDs `junkrooms`, `shatteredrooms`;
- Mausoleum generated on Offense and was reported far too foggy;
- LethalModDataLib initialization NRE discovered.

S1.42A was a successful seed, not a clean final gameplay baseline.

## S1.42B — LethalModDataLib NRE Guard

Profile:
`Profiles/LC V1 S1.42B LMDL NRE Guard.r2z`

SHA-256:
`8523754926e3f67c0ccef5aee976cbe72ab976f997876c59b51fedcfb293befe`

The cumulative compatibility plugin added a null-safe replacement for LethalModDataLib's bulk ModDataAttribute scan.

Runtime evidence:
`RuntimeEvidence/S1.42B/20260902T231959Z/`

Confirmed:
- `MW.MagicWesleyInteriors` was the Chainloader entry with `PluginInfo.Instance == null`;
- guard skipped exactly that null instance;
- LMDL completed initialization;
- save/load/delete hooks connected;
- moddata load/save succeeded.

**LethalModDataLib initialization NRE resolved.**

The same run revealed:
- a Thumper/Crawler-related Pikmin grabbed-state/leader-null issue;
- Puffer smoke still receiving a LethalMin effect trigger despite `Puffer Can Poison Pikmin = false`.

## S1.42C — Pikmin Enemy Guard

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Changes:
- `Thumper Bite Limit = 0`;
- `Crawler` added to Pikmin Attack Blacklist;
- compatibility plugin v1.2.0 adds targeted Puffer smoke effect-trigger removal;
- LMDL guard retained.

Runtime evidence:
`RuntimeEvidence/S1.42C/20260902T235238Z/`

Result:
- no new startup regression attributable to S1.42C;
- LMDL remained healthy;
- Puffer did not spawn -> Puffer guard remains unvalidated;
- Crawler spawned but interaction was not deliberately tested -> Thumper total noninteraction remains unconfirmed;
- a Baboon Hawk explicitly bit a Bulbmin and reproduced the same repeated `Leader is null when following` loop.

Important conclusion:
the broken follower state is a **generic LethalMin enemy grab/bite + Invincible Pikmin interaction**, not a Thumper-only problem.

## Current post-S1.42C decisions

Binding:
- all interiors equal effective probability on all moons, including future additions;
- Mausoleum-specific fog reduction;
- BCMER 1.71.0 with eight fixed 12.5% EventType categories;
- Functional Microwave target volume 0.7 with edit gate;
- Jetpack historical juijui value must not be guessed;
- next preferred engineering work is a generic grab/bite + invincible follower-state repair.

`BuildSpecs/S1.42D_PLAN.md` is draft-only.


## S1.42D — isolated enemy regression startup failure

S1.42D combined:
- generic LethalMin grab/bite + Invincible Pikmin recovery attempt;
- temporary runtime enemy isolation to Thumper/Crawler, Puffer and Baboon Hawk;
- Jetpack historical 140-second target;
- Jetpack high-speed/mid-air self-explosion disabled;
- Functional Microwave volume 0.7.

Static build passed.

Runtime on 2026-09-03 failed before a usable Main Menu.

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

The log reached LethalLevelLoader's Main Menu unlock point, then compatibility plugin v1.3.0 began a broad LethalMin reflection/Harmony scan. HarmonyX warned repeatedly about inherited/non-declared patch targets. The log terminated during the scan.

S1.42D is therefore a failed startup diagnostic and must not be retested.

## S1.42E — startup-safe LethalMin hotfix

Built from S1.42D with no package/version/enabled-state changes.

Profile:
`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

Compatibility plugin v1.3.1 narrows Harmony targets to declared local interaction methods on `*PikminEnemy` adapter types and removes the inherited GrabbableObject.Start Jetpack hook.

Build passed with 0 compiler warnings/errors.

S1.42E is awaiting runtime validation. First gate is Main Menu startup.


## S1.42E — startup pass, diagnostic isolation freeze

Runtime evidence:
`RuntimeEvidence/S1.42E/20260903T091053Z/`

S1.42E fixed the S1.42D startup crash:
- compatibility plugin v1.3.1 loaded;
- safe generic LethalMin state guard registered on four declared enemy-adapter methods;
- Main Menu and host lobby were reached;
- Jetpack Item asset was successfully changed from 50 to 140 seconds.

The user observed short freezes approximately once per second in the ship lobby.

The log showed the temporary EnemyIsolation layer running against `71 Gordion` and producing six `MissingMethodException` failures per second because `SpawnableEnemyWithRarity` was created through a nonexistent parameterless constructor.

S1.42E therefore passed the startup gate but was not used for interaction testing.

## S1.42F — Enemy Isolation Freeze Fix

Built repository-first from S1.42E.

Profile:
`Profiles/LC V1 S1.42F Enemy Isolation Freeze Fix.r2z`

SHA-256:
`f09404a8195b46261570331f736d921fb1cb25cd304e8952e5f6fcb404ed9e6b`

Compatibility plugin v1.3.2:
- skips diagnostic pool work on Gordion/Company while the host lobby is in orbit;
- uses the `EnemyType, int` constructor for diagnostic spawn entries;
- falls back to cloning an existing pool entry;
- retains the S1.42E startup-safe DeclaredOnly LethalMin state-guard architecture.

GitHub Actions passed with 0 compiler warnings/errors. S1.42F is awaiting runtime lobby-smoothness validation.


## S1.42F — Gordion fix passed, routed-moon stalls remained

Runtime evidence:
`RuntimeEvidence/S1.42F/20260903T092728Z/`

Confirmed:
- S1.42E Gordion constructor-loop fix worked;
- zero `MissingMethodException` from EnemyIsolation;
- ship lobby was smooth before routing;
- routed moon still showed periodic freezes.

The log exposed two causes:
1. EnemyIsolation still performed a once-per-second global `FindObjectsOfType<EnemyAI>()` scan on actual moons.
2. Coroner's `JetpackItem.Update` patch queried an unheld Jetpack every frame, producing 16,138 dying-player warnings in the short run.

## S1.42G — Routed Moon Performance Fix

Built from S1.42F.

Profile:
`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

Compatibility plugin v1.3.3:
- EnemyIsolation only applies on SelectableLevel changes;
- continuous global EnemyAI scene scanning removed;
- Coroner stays enabled;
- only Coroner's faulty JetpackItem.Update prefix/postfix are unpatched.

Build passed with 0 compiler warnings/errors. Awaiting routed-moon runtime validation.


## S1.42G — oversized evidence discarded / BCMER-off retest reset

A later S1.42G test upload was ingested as a ZIP and expanded to an approximately 40 MB combined log.

The evidence path:
`RuntimeEvidence/S1.42G/20260903T100914Z/`

was intentionally deleted because:
- repository analysis repeatedly stalled on the oversized combined log;
- the user explicitly marked the first three runs as non-representative;
- the final run was not fully/reliably analyzed before discard.

No conclusions from that deleted evidence are canonical.

User-reported observations retained only for reproduction:
- repeated HangarShipDoor/DoorAudit caller stacks involving BCMER;
- suspicion around BCMER `Door System: ERROR`;
- no enemies visible and empty `Enemies` terminal result;
- Functional Microwaves felt too common.

Next clean test:
`S1.42G_BCMER_OFF_RETEST`

The user will import canonical S1.42G and manually disable BCMER only. No new profile build is authorized before this retest is evaluated.


## S1.42G BCMER-off clean retest — performance pass, Thumper grab failure

Runtime variant:
`S1.42G_BCMER_OFF_RETEST`

Evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Log SHA-256:
`ac410c42e8174eb4f01aba1d3b7bf54100454e033ed87659a932f3b7f4a3c87e`

The user manually disabled only BCMER 1.71.0 on canonical S1.42G.

Confirmed:
- the routed-moon periodic freezes were gone;
- four Crawler/Thumper and two Puffer spawned;
- Puffer smoke guard activated;
- Coroner's prior per-frame Jetpack `PlayerController was null` flood was absent;
- the prior repeated zero-power DoorAudit/HangarShipDoor stack flood did not reproduce without BCMER.

Thumper interaction failed the intended zero-interaction requirement:
- Thumper contacted the Pikmin group;
- LethalMin removed a Yellow Pikmin leader;
- grabbed death timer started;
- invincibility prevented death;
- repeated `Leader is null when following` followed.

The `Kill enemy called! destroy: True` line was tied to the Pikmin death attempt, not proof that the Crawler itself was destroyed.

Root cause:
the v1.3.3 state guard covered four declared enemy-adapter methods but did not cover the common declared `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` path used by this interaction.

## S1.42H — Thumper Grab Guard

Built repository-first from S1.42G.

Profile:
`Profiles/LC V1 S1.42H Thumper Grab Guard.r2z`

SHA-256:
`5859e15ce71d8cd71d27e20205640af1f10ff91fe6d4b956d4a7064ac8400e58`

Compatibility plugin:
v1.3.5

DLL SHA-256:
`d67f8f4bc2012f5b74086eb268fcb191f6990c93041617e9ef35c635ea33f186`

GitHub Actions:
- build succeeded;
- 0 warnings;
- 0 errors;
- 331 archive members;
- only DLL + `export.r2x` changed;
- no added archive members.

S1.42H:
- patches exactly the declared `PikminAI.GrabPikmin(Transform,float,int)` method once;
- blocks Crawler/Thumper grabs before leader removal/death timer;
- retains Crawler in the Pikmin Attack Blacklist;
- keeps non-Thumper generic invincible-Pikmin recovery;
- carries forward late-lifecycle EnemyIsolation with no continuous global EnemyAI scan;
- disables BCMER 1.71.0 inside the diagnostic profile itself;
- deliberately leaves Functional Microwave rarity unchanged.

Historical build-time status:
**awaiting first runtime validation.**

That runtime validation later occurred and is documented below.


## S1.42H runtime — Puffer pass, Baboon Hawk hold/re-grab failure

Evidence:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

Log SHA-256:
`81ed064ce97d25f250d6fba1585055baef8ce801cd0f13626d074bf4fef71029`

Confirmed:
- exact common `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` hook loaded exactly once;
- startup/Main Menu remained safe;
- isolated Crawler/Puffer/Baboon-Hawk spawning worked with BCMER disabled;
- user confirmed the in-game `Enemies` terminal displayed enemies;
- Puffer smoke -> Pikmin guard passed;
- Coroner's historical Jetpack `PlayerController was null` flood remained absent;
- prior zero-power BCMER-related door flood did not reproduce with BCMER disabled.

Baboon Hawk remained broken for invincible Pikmin:
- 64 BitePikmin calls;
- 59 grabbed states;
- 59 grabbed death timers;
- 59 invincibility-blocked kills;
- 56 post-grab repairs;
- 193 `Leader is null when following` errors.

The user visibly observed Pikmin held immobilized in Baboon Hawk beaks.

A Crawler spawned, but direct Thumper/Crawler <-> Pikmin contact was not validated in this run.

## S1.42I — narrow Baboon Hawk invincible-Pikmin Grab Guard

Built from S1.42H.

Profile:
`Profiles/LC V1 S1.42I Baboon Hawk Grab Guard.r2z`

SHA-256:
`c7224aea97c51fb051da059648868bbae0421b9c3f02d5cc2dd60922efc28a97`

Compatibility plugin:
v1.3.6

DLL SHA-256:
`76544a536f5c626f0c81b50dc06a7bf1521c265cd23a7698917789e3846eecb2`

S1.42I blocked Baboon Hawk-owned common `GrabPikmin` only for invincible Pikmin.

Build:
- GitHub Actions success;
- 0 warnings;
- 0 errors.

**S1.42I was never runtime-tested.**

Before testing it, the user selected a stronger gameplay rule:
Baboon Hawks and Pikmin should completely ignore each other in both directions because chasing invincible Pikmin is pointless AI behavior.

S1.42I is therefore a superseded intermediate build, not runtime evidence.

## S1.42J — Baboon Hawk Zero Interaction

Built from S1.42I.

Profile:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Compatibility plugin:
v1.3.7

DLL SHA-256:
`7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

LethalMin config SHA-256:
`f7b2698171d9d6a7b6c2e7b415ff2cb2c63459fb267ff0807ebe0f4bcf3e0bd3`

Export SHA-256:
`89e03afcf1bc9b3390969f83709ad04dca865743de6249af0dde642d0e3e6fe5`

Binding rule:
**Baboon Hawk <-> Pikmin = zero interaction in both directions.**

Implementation:
- exact `LethalMin.BaboonBirdPikminEnemy` adapter disabled after exact `BaboonBirdAI.Start`;
- exact declared `BaboonBirdPikminEnemy.BitePikmin` blocked;
- common exact `PikminAI.GrabPikmin` retains Baboon Hawk failsafe for all Pikmin;
- exact runtime enemy name `Baboon hawk` added to LethalMin Pikmin Attack Blacklist;
- no broad inherited reflection/Harmony scan.

GitHub Actions:
- success;
- 0 warnings;
- 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only: LethalMin config, compatibility DLL, `export.r2x`;
- no added members;
- BCMER 1.71.0 remains disabled;
- EnemyIsolation remains enabled.

Current status:
**built successfully; awaiting runtime validation.**

Exact next action:
runtime-test S1.42J. Do not build S1.42K first.

Primary gate:
- Baboon Hawks and Pikmin ignore each other completely;
- direct Thumper/Crawler <-> Pikmin zero interaction is finally validated;
- Puffer -> Pikmin remains accepted from S1.42H.

After isolated acceptance:
- disable/remove EnemyIsolation;
- restore normal enemy configuration from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.


## 2026-09-03 — handover refresh + repository optimization plan recorded

No gameplay/build/runtime state changed.

The repository handover was refreshed while S1.42J remained the active untested runtime gate.

Recorded:
- new canonical handover: `Current/36_HANDOVER_S1.42J_TO_NEXT.md`;
- pending structural repository optimization plan: `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`;
- the migration is recommended but explicitly deferred until the active critical runtime/build gate has been evaluated and the resulting canonical state documented;
- START_HERE, README, Current state/handover/open-issues/status pointers were synchronized;
- `Current/01_HANDOVER_CORE.md` stale wording calling compatibility source version 1.3.5 current was corrected: current S1.42J source is v1.3.7, while v1.3.5 is historical S1.42H-stage context.

Control state remained:
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42J`;
- `BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`;
- no new runtime evidence was present in `RuntimeInbox/Current/`.

Immediate next action remained:
**runtime-test S1.42J; do not build S1.42K and do not begin the structural repository migration first.**

## S1.42J runtime — Baboon Hawk enemy-side protection passes

Evidence:
`RuntimeEvidence/S1.42J/20260903T145657Z/`

Log SHA-256:
`a8ce035bf64fa5b704e18c588215f43cd1fd184eef4f467dfbafa6fcb1379963`

Confirmed:
- startup and exact common GrabPikmin hook remained safe;
- Baboon Hawks repeatedly had exact `LethalMin.BaboonBirdPikminEnemy` disabled after spawn;
- user confirmed Baboon Hawks ignored Pikmin instead of chasing/biting/grabbing/holding them;
- Puffer smoke immunity was reconfirmed;
- Jetpack 140-second behavior was accepted by the user;
- Thumper/Crawler -> Pikmin guard worked, but the then-current `Crawler` Attack Blacklist entry prevented Pikmin -> Thumper/Crawler attacks.

Runtime counts:
- 19 `[ThumperPikminGuard]` blocks;
- 0 `Leader is null when following`.

The user clarified that Pikmin must still be able to attack Thumpers and Baboon Hawks.

## S1.42K — Thumper Pikmin Attack Restore

Built from S1.42J.

Profile:
`Profiles/LC V1 S1.42K Thumper Pikmin Attack Restore.r2z`

SHA-256:
`bbdc949c9477e138cc3dde7c261f36f014cf482dd930c393ab035d80f8560aa2`

Change:
- removed `Crawler` from LethalMin Pikmin Attack Blacklist;
- compatibility DLL unchanged.

S1.42K was built successfully but **never runtime-tested**.

Before testing it, the user clarified that Pikmin must also be able to attack/latch Baboon Hawks. S1.42K is therefore a superseded intermediate build and not runtime evidence.

## S1.42L — Pikmin Counterattack Restore

Built from S1.42K.

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Change:
- removed `Baboon hawk` from LethalMin Pikmin Attack Blacklist;
- compatibility DLL remained v1.3.7 and unchanged;
- resulting Attack Blacklist exactly matches modern S1.40B/S1.41 baseline.

Build verification:
- GitHub Actions success;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only: LethalMin config + `export.r2x`;
- no added members.

## S1.42L runtime — Thumper closed; one Baboon reverse-direction gate remains

Evidence:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

Confirmed:
- `[ThumperPikminGuard]` fired 36 times;
- `Leader is null when following` count remained 0;
- user confirmed Pikmin can be thrown onto Thumper/Crawler and attack/latch normally;
- user confirmed Thumper snapping does not hold Pikmin or create a broken state;
- visible Thumper snapping is accepted as harmless cosmetic/AI behavior and should not be patched further unless a functional regression appears;
- Puffer -> Pikmin remains PASS;
- Jetpack remains PASS/closed;
- Baboon Hawk -> Pikmin remains PASS/closed;
- Baboon Hawks continue to receive the exact adapter-disable guard;
- LethalMin registers Baboon hawk as Pikmin enemy with one latch trigger.

Current isolated runtime status:
**only Pikmin -> Baboon Hawk explicit attack/latch validation remains.**

Do not build a successor before this check.
Keep EnemyIsolation enabled and BCMER 1.71.0 disabled.

After PASS:
- remove/disable EnemyIsolation;
- restore normal enemy configuration from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0;
- preserve accepted asymmetric Pikmin interaction rules.

Repository structural migration remains deferred until the active gate and resulting normal-enemy/BCMER state are documented.

## S1.42L second runtime — Pikmin -> Baboon Hawk PASS, death-cleanup regression found

Evidence:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Raw log:
`RuntimeEvidence/S1.42L/20260903T155132Z/raw/LogOutput.log`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

User-confirmed:
- thrown Pikmin latch onto a living Baboon Hawk normally;
- Pikmin attack it normally;
- Pikmin can kill it.

Therefore:
**Pikmin -> living Baboon Hawk attack/latch is PASS/CLOSED.**

Hawk-side protection remained accepted and `Leader is null when following` remained 0.

New regression found at death:
- Pikmin latched to the Hawk remained associated with the dead original `BaboonHawkEnemy(Clone)` target after death;
- the log continued to show attack activity against that old target;
- SellBodies generated `BaboonHawkBody(Clone)`;
- living Baboon Hawks subsequently logged three grabs of that corpse item;
- the user observed the attacking Pikmin disappear and the corpse not remain where expected.

The user clarified the binding corpse requirement:
- SellBodies Baboon Hawk corpse generation must stay enabled;
- the Dead Baboon Hawk body must remain carryable by Pikmin/players;
- Pikmin must be able to carry it toward the Onion;
- living Baboon Hawks should not pick up the corpse.

Detailed analysis:
`Current/47_S1.42L_BABOON_ATTACK_PASS_DEATH_REGRESSION_ANALYSIS.md`

## S1.42M — Baboon Hawk Death Cleanup

Built from S1.42L.

Profile:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Compatibility plugin:
v1.3.8

DLL SHA-256:
`47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Purpose:
- release only Pikmin attached under the specific dying Baboon Hawk via exact death lifecycle + exact LethalMin `RemoveCurrentTask()` runtime resolution;
- prevent living Baboon Hawks from treating only the SellBodies Dead Baboon Hawk body as collectible scrap;
- preserve player/Pikmin corpse carrying.

Narrow implementation:
- exact declared `BaboonBirdAI.KillEnemy(bool)`;
- exact declared `BaboonBirdAI.CanGrabScrap(GrabbableObject)`;
- no scene-wide Pikmin scan;
- no Update-driven scan;
- no broad/inherited LethalMin Harmony scan.

Build attempt #41 failed only because the build specification used an overly strict Attack Blacklist regex assertion. No failed gameplay profile was committed.

The assertion was corrected to an equivalent containment check.

Final GitHub Actions build #42:
- success;
- 0 warnings;
- 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- only compatibility DLL + `export.r2x` changed;
- no added members.

S1.42M configs for LethalMin, SellBodies and the compatibility plugin remain byte-identical to S1.42L.

Current status:
**built; awaiting first runtime validation.**

Controllers:
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`;
- `BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`.

Temporary test state remains:
- EnemyIsolation enabled;
- exact BCMER 1.71.0 disabled.

Immediate next action:
runtime-test S1.42M unchanged. Confirm the attacking Pikmin survive/detach at Hawk death, the SellBodies corpse remains and can be carried by Pikmin toward the Onion, living Hawks do not pick it up, Hawk -> Pikmin ignore stays intact, and no leader-null loop appears. Then commit the complete fresh log to `RuntimeInbox/Current/`.

After S1.42M PASS:
restore normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`, re-enable exact BCMER 1.71.0, runtime-check the normal state, and only afterward perform deferred repository maintenance.

Final detailed handover:
`Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md`

