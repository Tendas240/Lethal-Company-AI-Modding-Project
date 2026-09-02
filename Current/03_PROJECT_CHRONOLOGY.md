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

## S1.40A — CodeRebirth config cleanup retention fix
Built from exact S1.40. Exactly one existing ZIP member replaced:

`BepInEx/config/CodeRebirth.cfg`

Adds:

`Clean Unusued Configs=false`

while retaining blank Currency inside weights and Flash Turret suppression.

No manifest/package/local-DLL changes.

Profile:
`Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`

SHA-256:
`ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5`

**Current status:** S1.40A is canonical and untested. S1.40 is latest runtime-tested and failed acceptance.

## Binding future sequence
1. Test S1.40A.
2. Only if Currency + Flash Turret pass, build S1.41 with exact BCMER 1.71.0.
3. Test S1.41.
4. Build S1.42A Interior Config Seed with all eight binding interior packages.
5. Run/host/land/generate, then collect full config directory + log.
6. Analyze real generated IDs/config sections.
7. Build tuned S1.42.

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
