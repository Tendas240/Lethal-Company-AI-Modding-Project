# 05 - Failed, Obsolete, or Deliberately Parked Approaches

Do **not** reintroduce these without new technical evidence or explicit user instruction.

| Component / approach | Status / reason |
|---|---|
| LethalCompanyVariables / EnemyRarityConfig | Historically removed; do not restore as the spawn solution. |
| LethalQuantities 1.2.9 as global enemy owner | Examined enemy-control sections were not the active source of truth. |
| AutoCompanyBuilding 1.2.1 | Loaded but routing was unreliable on V81. |
| AutoCompanyBuilding 1.1.3 | Routing could work, automatic landing did not. |
| RandomMoonFX 1.4.4 for Company automation | Active state interfered with manual moon selection; disabled state lacked the needed behavior. |
| Old Hold_Scan_Button | Replaced by working LethalHUD Hold-to-Scan. |
| Peepers enemy/hazard mod | Removed; do not confuse with Peeper tool. |
| CodeRebirthLib | Deprecated/unwanted; do not install. |
| ProjectSCP-SCP999 | Keep disabled; S1.31-S1.34 logs proved startup NRE in `SCP999.Plugin.Awake()`. |
| Gnomes | Caused V81 PlayerIsTargetable MissingMethod spam; removed. |
| FacilityMeltdown | Fully removed. |
| ASTeam Racist Hoarding Bugs sound replacer | Removed. |
| FearOverhauled | Removed. |
| LethalModDataLib | Removed after ShipWindows update; old NRE disappeared. |
| LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight | Do not reactivate on V81 due to AI/collision problems. |
| MirageClipLimiter.dll | Unrealized plan; DLL does not exist. |
| Forcing Rolling Giant / Shy Guy / Siren Head positive weights through LLL | Native ownership is the reliable architecture. |
| AJB-Keep_hangar_ship_door_closed | Its unconditional refill can turn an ordinary close into permanent outside lockout. Replaced by narrower local failsafe. |
| Treating S1.34 door countdown as a failed custom algorithm | Invalid: the custom DLL never loaded; observed behavior was vanilla. |
| EnemyScan 1.2.1 original scan-node-filtered list as complete census | Incomplete by design; local patch replaces only list-building output. |
| S1.35 or S1.36 as current canonical candidate | Superseded by later builds. S1.36 remains the deterministic baseline/source profile, not the current test candidate. |
| S1.37 scrap-only currency filter as complete natural-currency solution | Insufficient alone: S1.38 still produced Coin through the map-object/hazard path. S1.39 adds SpawnMapObjects filtering. |
| Assuming LethalMin `Crane Targets/Squishes Pikmin=false` alone prevents all crane kills | Runtime disproved this. S1.39 adds direct CodeRebirth utility-kill protection. |
| Enabling all of Lethal Resonance | Not desired. Current design is Old-Bird-only. |

## Deliberately disabled / parked, not permanently obsolete

### Malfunctions

Disabled from S1.34 onward by explicit user decision. **Do not re-enable unless the user explicitly asks.**

### BCMER

SoftDiamond-BrutalCompanyMinusExtraReborn remains disabled in S1.39. It is not permanently forbidden.

If the user wants it back, do a new isolated compatibility/config audit after S1.39 acceptance. Do not let BCMER silently override established spawn power/chance ownership.

## General anti-regression rule

Before proposing an old mod or configuration as a fix, search this file, `06_RECENT_WORK_S1.32-S1.39.md`, and the chronology first.
