# 12 — Handover: S1.41 accepted -> S1.42A Interior Config Seed

> **Progress update 2026-09-03:** This handover has been consumed. S1.42A was built via GitHub Actions as `Profiles/LC V1 S1.42A Interior Config Seed.r2z` with SHA-256 `70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe` and passed automated member-delta QC. Do not rebuild it by default. Immediate next step: runtime config-generation seed run and upload to `RuntimeInbox/Current/`. S1.41 remains the runtime-accepted baseline.


**Handover date:** 2026-09-03  
**Canonical state:** S1.41 — runtime accepted  
**Game:** Lethal Company V81

## 1. Canonical profile

Installable profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

GitHub Actions hash-verified/indexed this exact binary.

Readable profile snapshot:

`ProfileSources/S1.41/`

Manifest:
- 179 Thunderstore entries
- 174 enabled
- 5 disabled
- plus project-local cumulative compatibility plugin

Exact package list:

`Current/Aktive_Modliste_S1.41.txt`

Disabled:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

## 2. S1.41 acceptance — BCMER

Exact BCMER:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

BCMER 2.0.0 was deliberately NOT adopted.

Runtime evidence is persisted at:

`RuntimeEvidence/S1.41/20260902T215804Z/`

Ingested evidence hashes:
- LogOutput.log: `f0184428806955d88935f437f4f106104c7b5d9a14f97dfa2763d5215f199a8d`
- CodeRebirth.cfg: `51e269a79824eb177b1726ee4442ce59f086f75103a2cdb4b6e7829bff08e084`
- BrutalCompanyMinusExtraReborn.zip: `f22e390ae17f2d117db5c69bcc16096bdc5432fb0cd3454e53da1d4d9bbf8fb5`

BCMER loaded and finished patching. The run selected:
- Arachnophobia
- ScarceOutsideScrap
- LeaflessTrees as additional event

Post-run BCMER ownership guard survived exactly:

```ini
[Events Features]
Disable all events? = false

[Mod Compatibility]
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false

[Randomizer]
Enable Randomizer? = false
```

The four BCMER rain-event routes stayed disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy weather is still allowed.

**S1.41 is accepted.**

## 3. S1.40B CodeRebirth fix remains accepted

S1.40B solved the DawnLib per-content edit gate.

Accepted profile:

`Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z`

SHA-256:

`fd303f73f0f2223a6375fcf2b7ed209dae77e1934e3b4e8139932a89e7de7eb9`

S1.41 post-run CodeRebirth config proves the fix survived BCMER reactivation:
- `Clean Unusued Configs = false`
- Coin `Allow Editing Config = true`
- Crisp Dollar Bill `Allow Editing Config = true`
- Wallet `Allow Editing Config = true`
- their inside moon/interior weights remain blank
- Flash Turret `Allow Editing Config = true`
- `Flash Turret | Is Inside Hazard = false`
- Flash Turret inside moon/interior weights remain blank
- `Money | Enemy Drop Rates` is not part of the natural-spawn suppression and must not be blanked as collateral damage

No natural Currency/Flash-Turret regression was identified in S1.41.

Important historical distinction:
- S1.40 failed because CodeRebirth regenerated defaults.
- S1.40A made `Clean Unusued Configs=false` survive but still failed because per-content `Allow Editing Config=false`.
- S1.40B opened exactly the needed gates and passed.

## 4. Project-local compatibility plugin

Source:

`Patches/S139CompatibilityFixes/`

Embedded DLL path inside profile:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected and S1.41-confirmed runtime marker:

`S1.39 Compatibility Fixes loaded.`

Functions currently retained:
1. ship-door anti-lockout / DoorAudit / DoorFailsafe;
2. complete EnemyScan terminal output;
3. S1.37 normal-scrap CodeRebirth Currency filter;
4. defensive late Currency/map-object filter;
5. defensive Flash Turret filter;
6. direct CodeRebirth utility-kill Pikmin/Puffmin protection.

The late map-object filter is defense-in-depth only. It was not sufficient as the primary DawnLib Currency control.

Gale import rule for profiles containing this local DLL:

**Advanced options -> Import all files**

## 5. Repository-first automation — binding

Do not ask the user to maintain a local repository clone or run PowerShell profile-build scripts when the required base is online.

Canonical automation:
- build request: `BuildSpecs/current.json`
- builder: `BuildSystem/profile_builder.py`
- build workflow: `.github/workflows/profile-build.yml`
- uploaded profile index workflow: `.github/workflows/profile-index.yml`
- readable generated profiles: `ProfileSources/<build_id>/`
- runtime upload inbox: `RuntimeInbox/Current/`
- active runtime build marker: `RuntimeInbox/ACTIVE_BUILD.txt`
- runtime ingest workflow: `.github/workflows/runtime-ingest.yml`
- persisted runtime evidence: `RuntimeEvidence/<build>/<timestamp>/`

Current `BuildSpecs/current.json` is intentionally disabled/idle and points at S1.41 as the next base.

Current `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.41` until the next candidate exists.

For S1.42A:
1. research/audit exact current package slugs, versions and dependencies;
2. edit `BuildSpecs/current.json` directly on GitHub;
3. trigger GitHub Actions;
4. inspect the workflow result and generated `Current/AUTO_BUILD_RESULT.*`;
5. verify the generated `ProfileSources/S1.42A/`;
6. then set `RuntimeInbox/ACTIVE_BUILD.txt` to `S1.42A` before asking for runtime evidence.

### Build-system readiness

S1.42A depends on automated `mod_additions`. During handover QC, the builder's Gale `export.r2x` list-indentation handling was corrected and a self-test was added. GitHub Actions successfully passed the self-test. Do not bypass it.

## 6. Immediate next build — S1.42A Interior Config Seed

Do NOT deep-tune interiors yet.

Purpose:
- add the binding interior content;
- allow real config sections/IDs to be generated by the runtime;
- discover actual CullFactory identifiers;
- observe real dependency/runtime behavior;
- only then tune S1.42.

Binding planned additions:

1. `Beaniebe-Liminal_House 1.1.6`
2. `MelanieMelicious-Melanie_Interiors`
   - previously researched target 1.2.1
   - fresh audit before build; adopt newer only deliberately
3. `Beaniebe-Deepcore_Mines 1.0.9`
4. `MrKixcat-Junkrooms 4.0.2`
5. `Beaniebe-Super_Market 1.0.3`
6. `MrKixcat-Shatteredrooms 2.1.6`
7. `Lead Interiors 0.0.7`
   - exact current Thunderstore slug/dependencies must be freshly confirmed
8. `Dungeons_Ultimately_Lacking_Liveliness 1.8.8`
   - exact current Thunderstore slug/dependencies must be freshly confirmed

Do not install `Beaniebe-Beanies_Interiors 1.0.6` if it duplicates the already-present standalone Storage Complex.

Already-present infrastructure includes:
- BepInExPack 5.4.2305
- LethalLevelLoader 1.7.12
- JLL 1.10.1
- DungeonGenerationPlus 1.5.0
- BeanieLib 1.0.9
- itolib 0.9.3
- WaterAssetRestorer 1.0.1
- LethalLib 1.2.0
- HookGen/AutoHookGen infrastructure
- CullFactory 2.0.7
- LethalSponge 1.4.3

Do not assume this eliminates every new package dependency; audit manifests fresh.

### Special dependency/risk rules

**DULL / LethalModDataLib**
- Prior research indicated DULL 1.8.8 may require `MaxWasUnavailable-LethalModDataLib 1.2.2`.
- LethalModDataLib is NOT a hard ban.
- It was removed historically after an old ShipWindows/save/mod-data NRE disappeared, but causality was never proven.
- If the selected DULL version requires it, reintroduce it only in isolated S1.42A and regression-test save/mod-data/netcode behavior.

**Lead Interiors / Boom_Scraps**
- Prior research indicated some functionality may depend on Boom_Scraps.
- Determine from the current package whether Boom_Scraps is a hard dependency, optional integration, or feature-specific dependency.
- Do not blindly add it without evidence.

**Junkrooms / Shatteredrooms / CullFactory**
- Known CullFactory compatibility concerns exist.
- Do not guess identifiers in S1.42A.
- Generate the interiors first, collect runtime/config IDs, then add exact disable-culling exceptions in tuned S1.42.

**Shatteredrooms**
- Preserve author moon restrictions, including prior research that it should not appear on Experimentation/Embrion.
- Weight-100 normalization must not override safety restrictions.

## 7. S1.42A runtime generation procedure

After the online build succeeds, user imports the generated profile with:

**Gale -> Advanced options -> Import all files**

Then:
1. reach Main Menu;
2. host/load a save;
3. land on at least one normal moon;
4. let a dungeon actually generate;
5. exit the game.

Then upload through GitHub:

`RuntimeInbox/Current/`

Required preferred evidence:
- complete `BepInEx/config/` directory as ZIP;
- full `LogOutput.log`.

The user should not rename CFG files to TXT.

## 8. S1.42 final tuning rules

Only after real generated configs/IDs exist:
- normalize ordinary new interior weights toward Weight 100 where technically supported;
- preserve author safety/moon restrictions;
- avoid duplicate registration;
- do not double-register Black Mesa or content with its own DawnLib/native path;
- add CullFactory exceptions using actual generated IDs;
- evaluate DULL/LethalModDataLib behavior;
- evaluate Lead Interiors/Boom_Scraps behavior.

The final interior count will be more than +8 because some packages contain multiple interiors.

## 9. Open/non-blocking runtime issue — Mineshaft elevator + large Pikmin group

During S1.41, the user stood in the Mineshaft elevator with many Pikmin while it descended.

Observed:
- player clipped through the floor;
- player died from fall/gravity damage;
- many `Failed to create agent because it is not close enough to the NavMesh` warnings occurred around the elevator period;
- LethalMin recognized/patched the Mineshaft elevator.

Do NOT claim causality that Pikmins physically pushed the player through the floor. It is plausible but not proven.

Do NOT attribute this to BCMER without evidence.

Track during future elevator/interior tests.

## 10. Pikmin outdoor Sprout observation

User felt that fewer Pikmin may have been appearing as outdoor Sprouts since CodeRebirth was introduced.

Current interpretation:
- no strong evidence of a CodeRebirth-caused reduction;
- recent Offense runs were broadly consistent with the configured ~0.45 spawn chance and produced counts in the expected rough range;
- more Pikmin types and spatial distribution can make the same total feel sparser.

Treat as monitor-only unless new logs show a real statistical change.

## 11. Other carry-forward checks

When naturally encountered:
- GeneralImprovements recharge station should fully heal;
- Old Bird Resonance replacement still needs a clean real encounter validation;
- Mirage `neverDeleteRecordings=true` can live outside profile import and may require per-player verification;
- Ogopogo stays disabled;
- Vermin stays disabled;
- Autonomous Crane direct CodeRebirth utility-kill protection for Pikmin/Puffmin must not regress;
- Leaf Boy remains in the LethalMin Attack Blacklist;
- unknown Enemy PowerLevels must never be guessed;
- S1.29D remains diagnostic-only;
- CodeRebirthLib must never be reinstalled.

## 12. Known warnings — do not overreact without user-facing failure

Examples already seen:
- InjectionLibrary native Mirage/Opus DLL scan warnings;
- SellMyScrap missing ShipInventoryUpdated integration warnings;
- CodeRebirth Weather Registry unavailable warning;
- NavMeshInCompany NodeHelper warning;
- BCMER ButlerSword missing-script warning in S1.41.

The ButlerSword warning did not prevent S1.41 acceptance; monitor if a Butler/ButlerSword event exposes actual breakage.

## 13. New-chat first action

Read:
1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/00_CURRENT_STATE.md`
4. `Current/01_HANDOVER_CORE.md`
5. `Current/02_TECHNICAL_BASELINE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
8. `Current/06_RECENT_WORK_S1.32-S1.41.md`
9. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
10. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
11. `Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md`
12. this file
13. `Current/Projektstatus_S1.41.json`
14. `Current/Aktive_Modliste_S1.41.txt`
15. `ProfileSources/S1.41/PROFILE_INDEX_RESULT.json`
16. `BuildSpecs/current.json`

Then take over from accepted S1.41 and prepare S1.42A through the repository-first workflow.
