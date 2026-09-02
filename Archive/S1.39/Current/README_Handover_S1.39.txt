LETHAL COMPANY - CURRENT HANDOVER S1.39
Stand: 2026-09-02

KANONISCHER BUILD-/TESTKANDIDAT
Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z
SHA-256: b510e519b4af8b683e9b9e9f4e18035f90910d2e8782f2b9e6ded5e4ecef95fe

LETZTER TATSAECHLICH RUNTIME-GETESTETER STAND
S1.38 - LC V1 S1.38 1440p Old Bird Resonance
SHA-256: a6ec9e716759708bfb375e69cd4405795892957540ec954406584df79c6ce5f0

STATUS
S1.39 ist Build-/Archiv-/Diff-/Config-verifiziert, aber noch nicht runtime-akzeptiert.
S1.38 ist der neueste Runtime-Referenzstand. FixCameraResolution wurde vom Benutzer als korrekt bestaetigt und S1.37 Compatibility Fixes lud. Mirage neverDeleteRecordings=true wurde erst nach manueller Einstellung im Main Menu/LethalConfig im Log bestaetigt; der Profilimport allein ist dafuer nicht verlaesslich.

KRITISCHE GALE-IMPORTREGEL
Advanced options -> Import all files

S1.39 fallback local mod:
Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip

Erwarteter Runtime-Marker:
- S1.39 Compatibility Fixes loaded.

S1.39 AENDERUNGEN
- Ogopogo aus
- Vermin aus
- natuerliche Flash-Turret-Spawns blockiert
- natuerliche CodeRebirth-Waehrungs-MapObjects blockiert
- S1.37 Scrap-Waehrungsfilter beibehalten
- direkter CodeRebirth-Kill-RPC-Schutz fuer Pikmin/Puffmin
- Health Recharge Station in GeneralImprovements verifiziert aktiv
- 2560x1440 FixCameraResolution aus S1.38 beibehalten
- Lethal Resonance weiterhin nur Old Bird / Footsteps / Speaker
- BCMER weiterhin aus

NAECHSTE TESTS
1. S1.39 Plugin-Load bestaetigen.
2. Coins/Wallet/Bills/CreditPads und Flash Turret auf natuerliche Spawns pruefen.
3. Ogopogo/Vermin-Abwesenheit pruefen.
4. Crane vs Pikmin/Puffmin pruefen.
5. Health Recharge Station auf Full-Heal pruefen.
6. 2560x1440 pruefen.
7. Bei Old-Bird-Begegnung Lethal Resonance validieren.
8. Mirage neverDeleteRecordings nach Import pruefen; falls zurueckgesetzt, manuell im Main Menu/LethalConfig auf true stellen.
9. Vollstaendigen LogOutput.log sichern.

PERSISTENTE ENTSCHEIDUNGEN
- Malfunctions bleibt aus bis explizite Reaktivierung verlangt wird.
- SCP999 bleibt aus.
- AJB bleibt aus solange der lokale Door-Failsafe aktiv ist.
- BCMER bleibt fuer S1.39 aus; spaeter isoliert neu auditieren.
- Observer und Don't Touch Me bleiben aus.
- Leaf boy bleibt in der LethalMin Attack Blacklist.
- CodeRebirthLib nicht installieren.
- Unbekannte PowerLevels niemals raten.

REPOSITORY-QA
- Current/REPO_CLEANUP_PLAN_S1.39.txt
- Current/DATEIINVENTAR_S1.39.txt
- Current/SHA256SUMS_S1.39.txt
- HumanReadable DOCX/PDF wurden final gerendert und visuell geprueft.
