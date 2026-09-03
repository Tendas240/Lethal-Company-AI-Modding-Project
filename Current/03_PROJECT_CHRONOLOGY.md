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

## Current binding sequence

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
