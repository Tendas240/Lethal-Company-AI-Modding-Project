# 05 — Failed, Obsolete, or Deliberately Parked Approaches

Do **not** reintroduce the following without new technical evidence or explicit user instruction.

| Component / approach | Status / reason |
|---|---|
| LethalCompanyVariables / EnemyRarityConfig | Historically removed; do not restore as the spawn solution. |
| LethalQuantities 1.2.9 as global enemy owner | Enemy-control sections examined were not the active source of truth. |
| AutoCompanyBuilding 1.2.1 | Loaded but did not route reliably under V81. |
| AutoCompanyBuilding 1.1.3 | Routing could work, automatic landing did not. |
| RandomMoonFX 1.4.4 for Company automation | Active state interfered with manual moon selection; disabled state lacked needed routing patch. |
| Old Hold_Scan_Button | Replaced by working LethalHUD Hold-to-Scan. |
| Peepers enemy/hazard mod | Removed. Do not confuse with the Peeper tool. |
| CodeRebirthLib | Deprecated/unwanted. Do not install. |
| ProjectSCP-SCP999 | Must remain disabled. Recent S1.31–S1.34 logs proved it was accidentally active and throws a startup NRE in SCP999.Plugin.Awake(). S1.36 fixes the manifest. |
| Gnomes | Caused V81 PlayerIsTargetable MissingMethod spam; removed. |
| FacilityMeltdown | Fully removed. |
| ASTeam Racist Hoarding Bugs sound replacer | Removed. |
| FearOverhauled | Removed. |
| LethalModDataLib | Removed after ShipWindows update; old NRE disappeared. |
| LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight | Do not reactivate on V81 due to AI/collision problems. |
| MirageClipLimiter.dll | Unrealized plan; DLL does not exist. |
| Forcing Rolling Giant / Shy Guy / Siren Head positive weights through LLL | Native ownership is the reliable architecture. |
| AJB-Keep_hangar_ship_door_closed as current door solution | Disabled in S1.33+. Its unconditional power refill can turn an external close into a permanent outside lockout. Replaced by the narrower local failsafe. |
| Treating the S1.34 door countdown as proof the S1.33 algorithm failed | Invalid conclusion. The custom DLL never loaded; S1.34 was vanilla door behavior after AJB was disabled. |
| EnemyScan 1.2.1 original scan-node-filtered output as a complete enemy census | Incomplete by design. Base mod remains active, but S1.35/S1.36 patches its list-building method. |
| S1.35 as canonical profile | Superseded during handover because it still had ProjectSCP-SCP999 enabled. S1.36 is S1.35 plus that correction. |

## Deliberately disabled / parked, not permanently obsolete

### Malfunctions

zealsprince-Malfunctions is disabled from S1.34 onward by explicit user decision.

**Do not re-enable it unless the user explicitly says to do so in the future.**

This is a persistent project policy, not a claim that every Malfunctions feature is broken.

### BCMER

SoftDiamond-BrutalCompanyMinusExtraReborn remains disabled in the current baseline. It is not permanently forbidden.

If the user later wants it back, re-audit the current version/config and integrate it from the correct gameplay base without letting it silently override established spawn power/chance ownership.

## General anti-regression rule

Before proposing an old mod or configuration as a fix, search this file, 06_RECENT_WORK_S1.32-S1.36.md and the chronology first.

A solution that was previously rejected must not be presented as new unless there is a concrete reason why the old failure mode no longer applies.
