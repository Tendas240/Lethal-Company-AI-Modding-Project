LETHAL COMPANY MODDING - HANDOVER-PAKET
Stand: 01.09.2026 | Übergabepunkt: S1.29D

ZWECK
Dieses Paket ist die kompakte, aktuelle Übergabe an einen neuen ChatGPT-Chat. Es ersetzt für die unmittelbare Fortsetzung die ältere S1.24-Übergabe. Chronologisch jüngere Testergebnisse, Korrekturen und Entscheidungen in der aktualisierten Verlauf-PDF haben Vorrang vor älteren Annahmen.

ZUERST LESEN
1. Handover-Prompt_Lethal-Company_bis_S1.29D.docx
2. Lethal-Company_Chatverlauf_Handover_bis_S1.29D.pdf
3. Danach die Profile und Moon-Referenzscreenshots prüfen.

AKTUELLER STAND
- Neuester Profilstand: "LC V1 S1.29D Enemy Power Audit.r2z".
- S1.29D ist ein temporärer Diagnosebuild auf Basis von S1.29 und ergänzt RedPillEnemySpawn 0.3.0 als PowerLevel-Dumper; dessen Rarity ist 0.
- Letzter normaler Gameplay-Build: "LC V1 S1.29 CodeRebirth Runtime Test.r2z".
- CodeRebirth 1.6.9 ist aktiv.
- S1.29D wurde bereits gestartet/getestet.
- Danach wurde "LogOutput(4).zip" hochgeladen, aber noch nicht ausgewertet. Die Auswertung dieses Logs ist der unmittelbare nächste Schritt.

WICHTIG: NICHT PHYSISCH IM PAKET
Der exakte Binäranhang "LogOutput(4).zip" war beim Erstellen dieses neuen ZIPs nicht mehr als kopierbare Datei im aktiven Dateisystem verfügbar. Wenn er im neuen Chat nicht automatisch vorhanden ist, muss genau "LogOutput(4).zip" erneut hochgeladen werden. Er gehört zum S1.29D Enemy Power Audit und soll insbesondere die tatsächlichen Runtime-EnemyType.PowerLevel-Werte liefern.

Auch die historische Originaldatei "juijui.r2z" ist nicht physisch im Paket enthalten. Die für den unmittelbar geplanten S1.30-Schritt relevanten daraus gelesenen Referenzwerte sind in der Verlauf-PDF und zusätzlich in "Referenz/juijui_Referenzwerte.txt" dokumentiert. Die Originaldatei nur erneut anfordern, wenn ein exakter weiterer Alt-Config-Vergleich notwendig wird.

MITGELIEFERTE PROFILE
- S1.28: letzte Basis vor CodeRebirth; Equal-Interior-Rotation inklusive Black Mesa.
- S1.29: aktueller normaler Gameplay-Build mit CodeRebirth.
- S1.29D: aktueller Diagnosebuild für Runtime-PowerLevel-Audit.

Ältere S1.25-S1.27-Profile wurden zur Speicher- und Kontextoptimierung nicht erneut beigelegt, weil ihre Änderungen vollständig in S1.28/S1.29 aufgegangen und in der Verlauf-PDF chronologisch dokumentiert sind.

UNMITTELBAR NACH LOGOUTPUT(4)-AUSWERTUNG
Geplanter S1.30-Bereich:
- Mimics 2.7.4 deaktivieren (Fake Fire Exits entfernen); CoronerMimics ebenfalls deaktivieren.
- Indoor Power Counts nach fester Regel Vanilla/default x2; Experimentation = 8. Custom Moons ebenfalls jeweiliger Default x2.
- Enemies auf allen Monden früher tatsächlich spawnfähig machen, ohne SpawnCycleFixes blind zu entfernen.
- Screenshot-Referenzverhältnisse der dort gelisteten Enemies weiterhin exakt relativ zueinander erhalten; neue CodeRebirth-/sonstige Enemies dürfen den Gesamtpool erweitern und die effektiven Einzelchancen verwässern.
- Pikmins gegen Enemies/Hazards immun halten und Enemy-Targeting auf Pikmins soweit möglich vollständig verhindern.
- Alle schädlichen CodeRebirth->Pikmin-Schalter in LethalMin auf false; besonders Microwave-Interaktion. Falls Pikmins trotzdem brennen, gezielten Compatibility-Patch gegen Microwave-Cook/Hit-Logik bauen.

NICHT WIEDER AUFWÄRMEN
- Peeper-Tool != Peepers-Enemy-Mod. Peeper bleibt, Peepers bleibt draußen.
- LethalCompanyVariables und EnemyRarityConfig bleiben entfernt.
- AutoCompanyBuilding und RandomMoonFX sind nicht die funktionierende Company-Endlösung.
- Hold Scan läuft über LethalHUD; alten Hold_Scan_Button-Mod nicht zurückbringen.
- Rolling Giant/Shy Guy/Siren Head über native Spawn-Configs steuern.
- SCP-999-Enemy bleibt deaktiviert.
- BCMER bleibt vorerst aus; später nur Event-System ohne permanente Power-/Spawnchance-Steuerung.
