LETHAL COMPANY - CURRENT HANDOVER S1.36
Stand: 2026-09-02

KANONISCHER UEBERGABE-/TESTSTAND
Profiles/LC V1 S1.36 Handover Clean Baseline.r2z

LETZTER TATSAECHLICH RUNTIME-GETESTETER STAND
S1.34 - LC V1 S1.34 Malfunctions Disabled

STATUS
S1.36 ist Build-/Archiv-/Diff-verifiziert, aber noch nicht runtime-getestet.

KRITISCHE GALE-IMPORTREGEL
Beim Import des S1.36-.r2z:
Advanced options -> Import all files

S1.36 benoetigt:
Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

Erwartete Runtime-Load-Marker:
- S1.35 Compatibility Fixes loaded
- [EnemyScanFix] Patched EnemyScan to list every active EnemyAI ...

Fehlen diese Marker, wurde die lokale DLL nicht geladen. Dann das lokale Mod-ZIP separat in das S1.36-Profil importieren.

CHATGPT PRIMAERQUELLEN
START_HERE_ChatGPT_Masterprompt.txt
Current/00_CURRENT_STATE.md
Current/01_HANDOVER_CORE.md
Current/02_TECHNICAL_BASELINE.md
Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md
Current/05_FAILED_AND_OBSOLETE_APPROACHES.md
Current/06_RECENT_WORK_S1.32-S1.36.md
Current/03_PROJECT_CHRONOLOGY.md
Current/Projektstatus_S1.36.json
Current/Aktive_Modliste_S1.36.txt
Current/S1.36_BUILD_VERIFICATION.txt
Current/VERIFIKATION_S1.36.txt

PERSISTENTE ENTSCHEIDUNGEN
- Malfunctions bleibt deaktiviert, bis der Benutzer explizit Reaktivierung verlangt.
- ProjectSCP-SCP999 bleibt deaktiviert.
- AJB-Keep_hangar_ship_door_closed bleibt deaktiviert, solange der lokale Door-Failsafe verwendet wird.
- BCMER, Observer und Don't Touch Me bleiben deaktiviert.
- Leaf boy bleibt in der LethalMin Attack Blacklist.
- Mirage neverDeleteRecordings=true bleibt aktiv.
- Unbekannte Enemy-PowerLevels niemals raten.

ARCHIV
Die vorherigen S1.31-Current-Metadaten und HumanReadable-Dokumente liegen unter Archive/S1.31/.

HUMAN-READABLE S1.36
Current/HumanReadable/ enthaelt aktuelle DOCX/PDF-Komfortfassungen:
- Handover-Prompt_Lethal-Company_bis_S1.36
- Handover-Prompt_S1.36_Aktueller-Kern
- Lethal-Company_Chatverlauf_Handover_bis_S1.36
- Lethal-Company_Projektchronik_Kompakt_bis_S1.36

Diese Dateien sind sekundaer. Primaer fuer ChatGPT bleiben die Markdown/TXT/JSON-Dateien unter Current/.
