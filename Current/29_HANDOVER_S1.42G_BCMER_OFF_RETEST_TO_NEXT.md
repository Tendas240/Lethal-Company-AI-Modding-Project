# 29 — Handover S1.42G BCMER-Off Retest to Next Chat

**Handover date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical project state

Last fully accepted gameplay baseline:

**S1.41**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest clean runtime-tested technical candidate before the current diagnostic chain:

**S1.42C**

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Latest built candidate:

**S1.42G**

`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

Compatibility plugin:
**v1.3.3**

Embedded DLL SHA-256:
`39690bf06dd6876e42badeb80f69bd8448fdbfeecd888fab0105951c38812436`

S1.42G is **built but not cleanly runtime-validated yet**.

## Discarded S1.42G log

A previously committed S1.42G ZIP expanded to roughly 40 MB and contained four runs.

The first three runs were explicitly non-representative:
1. player died;
2. player died;
3. player was locked out of the dungeon by a Teleporter Trap.

Analysis of the fourth run repeatedly stalled because of the oversized combined log.

The entire ingest formerly under:

`RuntimeEvidence/S1.42G/20260903T100914Z/`

has been intentionally removed from the current repository.

**Do not search for, cite, restore, or use that deleted evidence for project decisions.**

User observations from that attempt are retained only as hypotheses in:
`Current/28_S1.42G_DISCARDED_LOG_BCMER_OFF_RETEST.md`

## Immediate next test — no new build

Do **not** create S1.42H or another profile before this retest.

Use the canonical archive:

`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

Import requirement:
**Gale -> Advanced options -> Import all files**

Then manually disable exactly one mod:

**SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0**

Do not alter any other mod state or config.

This deliberate manual runtime variant is named:

**S1.42G_BCMER_OFF_RETEST**

Routing is already configured:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42G_BCMER_OFF_RETEST`

Build controller is already idle:

`BuildSpecs/current.json`
- `enabled = false`
- `build_id = IDLE_S1.42G_BCMER_OFF_RETEST`

## Keep the new log short

Use one clean launch/run only.

Recommended sequence:
1. launch S1.42G;
2. host;
3. verify lobby/orbit is smooth;
4. route to one normal test moon;
5. verify routed-moon performance;
6. land;
7. use the terminal `Enemies` command after landing and again later in the day;
8. observe whether Crawler/Thumper, Puffer and Baboon Hawk actually appear;
9. if no enemies appear by late afternoon (around the previously observed 4:24 PM window), stop the run rather than extending the log unnecessarily;
10. exit and commit the complete fresh `LogOutput.log` (ZIP only if GitHub size requires it) to `RuntimeInbox/Current/`.

Do not combine several failed/aborted launches into one evidence log if avoidable.

## Primary questions for the retest

### 1. Enemy isolation / spawning

The temporary isolation target remains:
- indoor: Crawler/Thumper + Puffer/Spore Lizard;
- outdoor: Baboon Hawk;
- Pikmin-family entities remain allowed.

The discarded attempt suggested:
- no enemies visible;
- `Enemies` terminal output empty;
- no enemies even around 4:24 PM.

Those observations are **not confirmed evidence**.

Interpretation after clean BCMER-off retest:
- if enemies spawn without BCMER -> investigate BCMER interaction with temporary EnemyIsolation/spawn ownership;
- if enemies still do not spawn -> EnemyIsolation implementation itself is primary suspect.

Full normal enemy restore source:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

After the isolated regression stage, restore the full normal enemy configuration exactly from that baseline.

### 2. Routed-moon performance

S1.42G changed EnemyIsolation to:
- one-shot spawn-pool rewrite per SelectableLevel change;
- no continuous global `FindObjectsOfType<EnemyAI>()` scan.

The clean run must confirm the previous periodic short freezes remain gone after routing.

### 3. Coroner Jetpack spam

S1.42G keeps Coroner enabled but removes only Coroner's:
`Coroner.Patch.JetpackItemUpdatePatch`

from:
`JetpackItem.Update`

Expected:
- no frame-rate `PlayerController was null` / `Index not assigned!` flood from an unheld Jetpack.

### 4. BCMER Door System: ERROR / Hangar door interaction

The discarded attempt showed a screenshot with repeated:
`[DoorAudit] HangarShipDoor.SetDoorOpen called; currentPower=0.000`

and caller stack through:
`BrutalCompanyMinus.Minus.Handlers.HangarShipDoorPatches.OverwriteDoorPower`

The user suspects BCMER event:
**Door System: ERROR**

This is not yet confirmed from valid evidence.

Next test keeps BCMER disabled specifically to determine whether the door spam disappears.

If later reproduced specifically with BCMER enabled:
- prefer a narrow BCMER-`Door System: ERROR` compatibility patch;
- do not weaken/remove the general project ship-door anti-lockout failsafe globally.

## Functional Microwave

Current S1.42G config:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

New user requirement:
**Functional Microwaves should be somewhat rarer in a future build.**

Do not change their rarity during the BCMER-off retest because that retest must change BCMER only.

Exact rarity reduction has not yet been selected. Inspect the generated CodeRebirth config and choose a moderate config-first reduction later.

## Jetpack current truth

S1.42G:
- ButteRyBalance `Reduce Battery = false`;
- local compatibility plugin targets the loaded Jetpack Item asset at **140 seconds**;
- JetpackFixes `MidAirExplosions = Off`;
- Coroner Jetpack per-frame death hook is suppressed by the project-local guard.

Still requires clean runtime validation:
- approximately 140 seconds usable duration;
- sustained/high-speed normal boost does not self-explode;
- collision behavior may remain separate.

Do not revert documentation to the obsolete 40-second / OnlyTooHigh intermediate state.

## Pikmin interaction tests after spawn path works

Only after enemies reliably spawn:

1. Baboon Hawk
   - reproduce bite/grab on invincible Pikmin/Bulbmin;
   - verify generic state repair prevents persistent leader-null follow state.

2. Thumper/Crawler
   - no interaction in either direction.

3. Puffer
   - smoke/attack does not affect Pikmin;
   - normal player/Puffer behavior remains intact.

Highest engineering bug remains:
**generic LethalMin enemy grab/bite + Invincible Pikmin -> broken leader/follow state**

## BCMER normal project policy

BCMER remains a required normal gameplay mod after this isolated diagnostic stage.

Exact pinned version:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not upgrade to 2.0.0.

The BCMER-off state is **temporary test isolation only**.

Carry forward the accepted S1.41 BCMER config/ownership guards when BCMER is re-enabled.

## Retest-specific machine-readable artifacts

Use these for the manual variant:
- `Current/Aktive_Modliste_S1.42G_BCMER_OFF_RETEST.txt`
- `Current/README_Handover_S1.42G_BCMER_OFF_RETEST.txt`
- `Current/VERIFIKATION_S1.42G_BCMER_OFF_RETEST.txt`
- `Current/SHA256SUMS_S1.42G_BCMER_OFF_RETEST.txt`
- `Current/DATEIINVENTAR_S1.42G_BCMER_OFF_RETEST.txt`

The canonical S1.42G `export.r2x` must remain unchanged with BCMER enabled; BCMER-off exists only as the explicit manual retest state.

## Repository-first rules

GitHub is canonical.

Do not ask the user for:
- local repository clone;
- local PowerShell profile build;
- rebuilding from local files,

while the required bases exist in GitHub.

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

## Read order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/29_HANDOVER_S1.42G_BCMER_OFF_RETEST_TO_NEXT.md`
3. `Current/28_S1.42G_DISCARDED_LOG_BCMER_OFF_RETEST.md`
4. `Current/27_S1.42G_BUILD_AND_TEST.md`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/Projektstatus_S1.42G.json`
9. `Current/02_TECHNICAL_BASELINE.md`
10. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`

Then inspect older evidence/history only as needed.

## First action in the next chat

Do not build anything.

Confirm:
- current archive is S1.42G;
- `BuildSpecs/current.json` is idle;
- `RuntimeInbox/ACTIVE_BUILD.txt` is `S1.42G_BCMER_OFF_RETEST`;
- discarded S1.42G evidence is absent.

Then instruct the user to create the single short BCMER-off retest log described above, unless that new log has already been committed.
