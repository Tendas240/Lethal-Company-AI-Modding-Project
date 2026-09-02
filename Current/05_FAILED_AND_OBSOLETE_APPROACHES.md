# 05 — Failed and Obsolete Approaches

Do **not** reintroduce the following without new technical evidence.

| Component / approach | Status / reason |
|---|---|
| LethalCompanyVariables / EnemyRarityConfig | Historically removed; do not restore as the spawn solution. |
| LethalQuantities 1.2.9 | Present historically, but enemy-control sections examined were not active. |
| AutoCompanyBuilding 1.2.1 | Loaded but did not route reliably under V81. |
| AutoCompanyBuilding 1.1.3 | Routing could work, automatic landing did not. |
| RandomMoonFX 1.4.4 for Company automation | Active state interfered with manual moon selection; disabled state lacked the needed routing patch. |
| Old Hold_Scan_Button | Replaced by working LethalHUD Hold-to-Scan. |
| Peepers enemy/hazard mod | Removed. Do not confuse with the Peeper tool. |
| CodeRebirthLib | Deprecated/unwanted. Do not install. |
| SCP-999 enemy | Do not re-enable; caused massive repeated runtime NREs. |
| Gnomes | Caused V81 PlayerIsTargetable MissingMethod spam; removed. |
| FacilityMeltdown | Fully removed. |
| ASTeam Racist Hoarding Bugs sound replacer | Removed. |
| FearOverhauled | Removed. |
| LethalModDataLib | Removed after ShipWindows update; old NRE disappeared. |
| LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight | Do not reactivate on V81 due to AI/collision problems. |
| MirageClipLimiter.dll | Was only an unrealized plan; do not assume the DLL exists. |
| Forcing Rolling Giant / Shy Guy / Siren Head positive weights through LLL | Earlier diagnostics showed native ownership is the reliable architecture. |

## General anti-regression rule

Before proposing an “old” mod or configuration as a fix, search this file and the chronology first. A solution that was previously rejected must not be presented as new unless there is a concrete reason why the old failure mode no longer applies.
