# Lethal Company AI Modding Project

Current canonical project state: **S1.39**

Current gameplay/test candidate:

`Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z`

Latest runtime-tested reference: **S1.38** - `Profiles/LC V1 S1.38 1440p Old Bird Resonance.r2z`.

S1.39 is build/diff/archive verified but **not yet runtime-tested**. S1.38 was run in game and is the newest runtime evidence source, but the run exposed issues that S1.39 is designed to correct.

## Critical S1.39 import requirement

S1.39 contains a project-local cumulative compatibility DLL.

When importing the `.r2z` in Gale, enable:

**Advanced options -> Import all files**

Expected BepInEx marker:

- `S1.39 Compatibility Fixes loaded.`

If that marker is absent, import this local mod separately:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

Do not evaluate S1.39's map-object filtering or Pikmin kill protection unless the local plugin load is confirmed.

## ChatGPT - read first

A new ChatGPT conversation should use the machine-readable repository content in this order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.39.md`
8. `Current/03_PROJECT_CHRONOLOGY.md`
9. `Current/Projektstatus_S1.39.json`
10. `Current/Aktive_Modliste_S1.39.txt`
11. `Current/S1.39_BUILD_VERIFICATION.txt`
12. `Current/VERIFIKATION_S1.39.txt`
13. `Current/DATEIINVENTAR_S1.39.txt`
14. `Current/SHA256SUMS_S1.39.txt`

Then inspect `Profiles/`, `Patches/`, `Logs/`, `References/`, and `Current/HumanReadable/` according to the task.

## Current key decisions

- **Malfunctions stays disabled** until the user explicitly requests reactivation.
- **ProjectSCP-SCP999 stays disabled.** Earlier runtime logs proved its startup NRE.
- AJB-Keep_hangar_ship_door_closed stays disabled while the local door failsafe is used.
- **BCMER stays disabled for S1.39.** It is intentionally parked, not permanently banned. Its reactivation should be isolated in a later build after S1.39 is accepted.
- Observer and Don't Touch Me stay disabled.
- Leaf Boy remains in the LethalMin Attack Blacklist.
- Mirage `neverDeleteRecordings=true` is desired. The user had to set it manually in the Main Menu/LethalConfig after profile import; the latest S1.38 log then confirmed the value was actually `true`. Do not assume the profile import applies this per-player game-root setting.
- Unknown enemy PowerLevels must never be guessed.
- CodeRebirthLib must not be reintroduced.

## What S1.39 changes

- Biodiversity Ogopogo disabled.
- Biodiversity Vermin companion mechanic disabled.
- Natural CodeRebirth Flash Turret spawning suppressed.
- Natural CodeRebirth currency map-object spawning suppressed; the earlier natural scrap currency filter remains.
- Direct CodeRebirth utility-kill protection for Pikmin/Puffmin added, closing the observed Autonomous Crane kill gap.
- GeneralImprovements health recharge station is explicitly verified enabled in the profile; full-heal behavior still needs runtime acceptance.
- S1.38 2560x1440 FixCameraResolution and Old-Bird-only Lethal Resonance configuration are carried forward unchanged.

## Runtime distinction

**Runtime-tested:** S1.38.

Confirmed in the S1.38 phase: FixCameraResolution loaded and was visually accepted by the user at 2560x1440; the S1.37 compatibility plugin loaded; after the user manually set Mirage retention in the Main Menu/LethalConfig, the log showed `neverDeleteRecordings=true`. The same run still showed natural CodeRebirth coins and led to the observed crane/Pikmin and cleanup requests that S1.39 addresses. Earlier S1.36 runtime testing had already accepted the ship-door failsafe, complete `enemies` output, and Pikmin immunity to the CodeRebirth microwave interaction.

**Build-tested only:** S1.39.

S1.39 has passed compilation, profile CRC, member-delta, package-manifest and config assertions. Its gameplay acceptance tests remain open.

## Priority rule

The chronologically newest confirmed information overrides older assumptions. Runtime evidence overrides package-manifest assumptions when they disagree about what actually loaded.

`Archive/` is historical reference material and must not override a newer confirmed state unless current documentation explicitly points back to it.

Do not repeat solutions documented as failed or obsolete without new evidence.

## Handover master prompt

The durable repository workflow and takeover instructions are in `START_HERE_ChatGPT_Masterprompt.txt`.

The repository is the canonical handover source. A ZIP backup is optional, not required.
