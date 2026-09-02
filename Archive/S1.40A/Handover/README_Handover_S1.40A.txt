LETHAL COMPANY — CURRENT HANDOVER S1.40A
Stand: 2026-09-02

KANONISCHER BUILD-/TESTKANDIDAT
Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z
SHA-256:
ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5

STATUS
S1.40A ist build-/archiv-/config-verifiziert, aber noch NICHT runtime-getestet.

LETZTER RUNTIME-GETESTETER STAND
S1.40 — LC V1 S1.40 Native Currency Flash Turret Cleanup
SHA-256:
f117cd1c6e234ed280ce8a55ca696ce26d3e14c8b20357ee3714919c5ebbac78
Ergebnis: Acceptance fehlgeschlagen.

S1.40 EVIDENZ
- früher Run: Wallet + Flash Turret beobachtet;
- Benutzer vermutete später, dass bei diesem Import "Advanced options -> Import all files" eventuell nicht gesetzt war;
- spätere Runs: keine Currency visuell gefunden, aber weiterhin Flash Turret;
- Runtime-Log enthielt Currency-Clone-Instanzen;
- post-run CodeRebirth.cfg:
  Clean Unusued Configs=true
  Flash Turret | Is Inside Hazard=true
  positive Currency-Inside-Moon-Curves wieder vorhanden.

S1.40A FIX
Nur BepInEx/config/CodeRebirth.cfg ersetzt.
Zusätzlich:
Clean Unusued Configs=false
Currency Inside Moon/Interior Weights leer.
Flash Turret Is Inside Hazard=false.
Flash Turret Inside Weights leer.
Money | Enemy Drop Rates unverändert.
S139CompatibilityFixes unverändert.

GALE
Advanced options -> Import all files
Marker:
S1.39 Compatibility Fixes loaded.

NÄCHSTER TEST
- keine natürlichen Coins;
- keine natürlichen Crisp Dollar Bills;
- keine natürlichen Wallets;
- keine Flash Turret;
- danach post-run CodeRebirth.cfg prüfen;
- vollständigen LogOutput.log sichern.

WENN S1.40A BESTEHT
S1.41: exaktes vorhandenes BCMER 1.71.0 reaktivieren.
BCMER 2.0.0 nicht im selben Schritt verwenden.
Raining / HeavyRain / AllWeather / Hurricane deaktivieren.
BCMER Spawn-Ownership außerhalb Events einschränken.
Dann S1.41 testen.

DANACH
S1.42A Interior Config Seed mit den acht verbindlich geplanten Interior-Paketen.
Spiel starten -> Main Menu -> Save hosten/laden -> normale Moon landen -> Dungeon generieren -> beenden.
Dann komplettes BepInEx/config/ + LogOutput.log aus genau diesem Seed liefern.
Erst danach S1.42 final tunen.

VOLLSTÄNDIGE ROADMAP
Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md

WICHTIGE PERSISTENTE REGELN
Malfunctions aus bis explizit angefordert.
SCP999 aus.
AJB aus solange lokaler Door-Failsafe aktiv.
CodeRebirthLib niemals zurück.
LethalModDataLib nicht pauschal verbieten; nur isoliert für DULL testen.
Unknown Enemy PowerLevels niemals raten.
S1.29D niemals als Gameplay-Basis.
