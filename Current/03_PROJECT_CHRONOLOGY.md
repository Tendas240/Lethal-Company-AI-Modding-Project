# 03 — Project Chronology

This is a technical reconstruction of the confirmed project history. It is not claimed to be a verbatim transcript.

## S1.2 — Profilname/Path-Length-Stabilisierung

Ein zu langer Gale-Profilname führte zu Windows-/BepInEx-Pfadproblemen. Profilname verkürzt; Coroner/Logging stabilisiert.

**Result / significance:** Dauerregel: Profilnamen kurz halten.

## S1.3 — Frühe Gameplay-/Pikmin-/Enemy-Bereinigung

Wild-Pikmin-Falloff und unerwünschte Skalierung neutralisiert; Stamina angepasst; Football-Spawns über eigene Rarities auf 0; BCMER deaktiviert.

**Result / significance:** Mehrere Spawn-Systeme als konkurrierende Owner erkannt.

## S1.4–S1.5 — Audio-/Kompatibilitätsdiagnose

Mirage-/Voice-Mimicking untersucht. Geplanter 20-Sekunden-MirageClipLimiter konnte nicht gebaut werden.

**Result / significance:** MirageClipLimiter.dll existiert nicht.

## S1.6 — Pikmin- und Battery-Tuning

Indoor Pikmin 0.08→0.12; historische Battery-Anpassungen; BCMER weiter aus.

**Result / significance:** Battery-Lösung später ersetzt.

## S1.7 — Facility-/Performance-Phase

Stamina testweise 2×; Facility-Verteilung; FacilityMeltdown entfernt; Rolling Giant temporär wegen Spam-Verdacht deaktiviert.

**Result / significance:** Rolling Giant war nicht die eigentliche Spam-Ursache.

## S1.8 — Gnome-Ursache isoliert

Gnomes als V81 PlayerIsTargetable MissingMethod-Spamquelle entfernt. Rolling Giant zurück. Stamina ~1.5× finalisiert. MoreBattery eingeführt.

**Result / significance:** Gnomes nicht wieder hinzufügen.

## S1.9 — Pikmin/Peepers Cleanup

Indoor Pikmin 0.12→0.11; Peepers vollständig entfernt.

**Result / significance:** Peeper-Tool ist davon getrennt.

## S1.10 — Spawn-Autoritäten-Audit

Indoor Pikmin 0.10; weitere Bereinigung; LLL als nicht alleinige Source of Truth erkannt.

**Result / significance:** Grundsatz: möglichst ein positiver Spawn-Owner pro Enemy.

## S1.11 — Erster Single-Owner-Versuch über LLL

Mehrere Enemies sollten zentral über LLL kontrolliert werden.

**Result / significance:** Für Rolling Giant/Siren Head später als unzuverlässig verworfen.

## S1.12 — Vier-Enemy-Offense-Test

Nur Rolling Giant, Shy Guy, Locker innen und Siren Head draußen vorgesehen.

**Result / significance:** Observer leakte über zusätzliche Match-Regeln.

## S1.13 — Runtime-Identifier/EnemyScan

Locker/Observer hart deaktiviert; Runtime-Namen getestet; EnemyScan installiert.

**Result / significance:** Don't Touch Me leakte; Rolling Giant Runtime-Weight 0; LLL-Ownership verworfen.

## S1.14 — Native Spawn-Ownership

Rolling Giant20, Shy Guy7, SirenHead30 wieder native; konkurrierende LLL-Entries entfernt.

**Result / significance:** Praktisch bestätigt und weiterhin maßgeblich.

## S1.15 — Rolling Giant juijui-Verhalten

RandomlyMoveWhileLooking, MoveSpeed2, Acceleration1 etc.

**Result / significance:** Bewährte Bewegungskonfiguration.

## S1.16 — Random Enemy Sizes

RandomEnemiesSize 1.1.20 integriert.

**Result / significance:** Praktisch bestätigt.

## S1.17 — Mirage/ShipWindows/Company-Vorbereitung

FearOverhauled entfernt; AutoCompanyBuilding 1.2.1; ShipWindows 2.11.1; LethalModDataLib entfernt.

**Result / significance:** AutoCompany später verworfen.

## S1.18 — Company-Automation Test 1

AutoCompanyBuilding 1.2.1 beibehalten.

**Result / significance:** Auto-Routing nicht zuverlässig.

## S1.19 — RandomMoonFX-Alternative

AutoCompanyBuilding entfernt; RandomMoonFX getestet.

**Result / significance:** Ungeeignet; nicht wiederverwenden.

## S1.20 — AutoCompanyBuilding 1.1.3

Ältere Version getestet.

**Result / significance:** Routing teils möglich, Auto-Landung nicht; verworfen.

## S1.21 — Pikmin Water Avoidance

Water Avoidance aktiviert; Company noch offen.

**Result / significance:** Löste Wasserproblem nicht.

## S1.22 — CompanyBuildingEnhancements + Hold Scan

CompanyBuildingEnhancements 2.6.0 und LethalHUD Hold-to-Scan eingeführt.

**Result / significance:** In S1.23 bestätigt.

## S1.23 — Pikmin Water Resistance + Company bestätigt

Alle Pikmin-Typen wasserresistent; Water Avoidance false; Deadline0→Gordion→Auto-Landung bestätigt.

**Result / significance:** Stabile Lösung.

## S1.24 — Enemy Restore / breite Spawn-Basis

Breiter Enemy-Roster; Pikmin Speed1.3; Referenzverhältnisse etabliert.

**Result / significance:** Letzter extrem ausführlich dokumentierter Altstand.

## S1.25 — SCP-999 Isolation

SCP-999 Enemy deaktiviert.

**Result / significance:** Massive SCP999AI/SnowyLib NRE-Flut verschwand.

## S1.26 — Spawn Balance

Immortal Snail max2; Screenshot-Verhältnisse bindend; Giant Sapsucker globaler Daytime-Ansatz.

**Result / significance:** Regeln für spätere Builds.

## S1.27 — Equal Interior Rotation

Normale Interiors auf gleiche Baseline.

**Result / significance:** Vorbereitung 26er-Rotation.

## S1.28 — Black Mesa Equal Rotation

Black Mesa über eigene DawnLib/Mod-Config Weight100 eingebunden.

**Result / significance:** Runtime: 26 viable, alle Weight100.

## S1.29 — CodeRebirth Runtime Test

CodeRebirth1.6.9 + Abhängigkeiten integriert.

**Result / significance:** Normale Gameplay-Basis hinter S1.30.

## S1.29D — Enemy Power Audit

S1.29 + RedPillEnemySpawn Diagnosemod.

**Result / significance:** Plugin lud, vollständige Runtime-Power-Tabelle blieb aus.

## S1.30 — Power Caps / Mimicless / Pikmin Shield

Mimics+CoronerMimics entfernt; CR-Pikmin-Schalter false; höhere Indoor-Caps.

**Result / significance:** Flash Turret Schutz bestätigt; Indoor subjektiv etwas zu dicht.

## S1.31 — Indoor Power Trim -4

Alle steuerbaren Indoor-Caps um4 reduziert; keine Weight-/Interior-/Pikmin-Änderungen.

**Result / significance:** Aktueller Build.
