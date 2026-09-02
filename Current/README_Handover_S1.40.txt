LETHAL COMPANY - CURRENT HANDOVER S1.40
Stand: 2026-09-02

KANONISCHER BUILD-/TESTKANDIDAT
Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z
SHA-256: f117cd1c6e234ed280ce8a55ca696ce26d3e14c8b20357ee3714919c5ebbac78

LETZTER TATSAECHLICH RUNTIME-GETESTETER STAND
S1.39 - LC V1 S1.39 Cleanup Health Pikmin Shield
SHA-256: b510e519b4af8b683e9b9e9f4e18035f90910d2e8782f2b9e6ded5e4ecef95fe

S1.39 RUNTIME-ERGEBNIS
- S1.39 Compatibility Fixes lud korrekt.
- Coins und Wallets spawnten weiterhin natuerlich im Dungeon.
- Flash Turrets wurden vom Benutzer im Run nicht gesehen; noch kein deterministischer Beweis.
- Ursache: CodeRebirth 1.6.9 / DawnLib besitzt eigene native Inside-MapObject-Spawnkurven.

S1.40 AENDERUNG
- genau ein neues Profilmitglied: BepInEx/config/CodeRebirth.cfg
- Coin/Crisp Dollar Bill/Wallet Inside Moon + Interior Spawn Weights leer
- Flash Turret Is Inside Hazard=false
- Flash Turret Inside Moon + Interior Spawn Weights leer
- S139CompatibilityFixes unveraendert
- Modliste unveraendert: 179 / 173 aktiv / 6 deaktiviert

KRITISCHE GALE-IMPORTREGEL
Advanced options -> Import all files
Erwarteter Marker: S1.39 Compatibility Fixes loaded.

NAECHSTER TEST
Natuerliche Coins/Wallets/Bills und Flash Turrets muessen im Dungeon ausbleiben. Danach restliche S1.39-Punkte regressionsweise pruefen und LogOutput.log sichern.

PERSISTENTE ENTSCHEIDUNGEN
Malfunctions aus bis explizit reaktiviert; SCP999 aus; BCMER bis nach S1.40-Abnahme aus; AJB aus; CodeRebirthLib nicht installieren.
