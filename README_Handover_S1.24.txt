LETHAL COMPANY MODDING - HANDOVER S1.24
=======================================

Zweck
-----
Dieses Paket ist fuer die nahtlose Uebergabe des laufenden Lethal-Company-Modding-Projekts an einen neuen ChatGPT-Chat.

WICHTIGSTER UEBERGABEPUNKT
--------------------------
- Aktuellster Build: LC V1 S1.24 Enemy Restore.r2z
- S1.24 wurde erstellt, aber vor der Uebergabe noch NICHT praktisch getestet.
- Letzter praktisch getesteter Build: LC V1 S1.23 All Pikmin Water Resistant.r2z
- In S1.23 praktisch bestaetigt:
  * Hold-Scan mit gedruecktem Rechtsklick funktioniert.
  * Alle Pikmin sind Water-resistant; Avoidance ist aus; das beobachtete Festhaengen im Wasser trat danach nicht mehr auf.
  * Tag 0 routet automatisch nach Gordion UND landet automatisch.
- S1.24 hebt den Offense-Isolationstest auf, reaktiviert den breiteren Enemy-Roster und erhoeht Pikmin Speed von 1.2 auf 1.3.

OFFENE PUNKTE
-------------
- S1.24 praktisch testen (Offense-Enemy-Mix, Pikmin Speed 1.3, Regressionen).
- Letzten S1.23-Diagnoselog auf Toy-Gun-only-Scrap auf March untersuchen.
- Lange Zeit bis/waehrend "Entering the Atmosphere" auf March untersuchen.
- Frame-Drops mit Full-Logging analysieren; bisherige Kandidaten sind noch keine bestaetigten Ursachen.
- Onion-Duplikate weiter beobachten und bei Reproduzierbarkeit Ownership/Fusion/Save-Erkennung von LethalMin pruefen.

WICHTIGE KORREKTUREN
---------------------
- Hydrogere ist ein Enemy/Slime, kein Wasser.
- Peeper (kaufbares Tool) und Peepers (Hazard/Enemy-Mod) nicht verwechseln; Peepers bleibt entfernt.
- RandomMoonFX ist als Routing-Loesung gescheitert und entfernt.
- AutoCompanyBuilding 1.1.3 routete bei Tag 0, landete aber nicht automatisch; aktuell bestaetigt ist CompanyBuildingEnhancements 2.6.0.
- Rolling Giant, Shy Guy und Siren Head behalten ihre nativen positiven Spawn-Owner.
- Observer, Don't Touch Me und BCMER bleiben deaktiviert.
- LethalPlaytime-Enemys Boxy Boo/Huggy Wuggy/Miss Delight nicht einfach wieder aktivieren; unter V81 waren AI/Kollisionen kaputt.

DATEIEN
-------
Dokumentation/Handover-Prompt_Lethal-Company_bis_S1.24.docx
  Vollstaendiger Rekonstruktions-/Fortsetzungsprompt, aktualisiert auf den neuen Uebergabepunkt.

Dokumentation/Lethal-Company_Chatverlauf_Handover_bis_S1.24.pdf
  Bisherige 246-seitige Verlauf-PDF plus chronologisch angehaengte Fortsetzung bis S1.24. Neuester Abschnitt hat bei Widerspruechen Vorrang.

Profile/LC V1 S1.24 Enemy Restore.r2z
  Aktuelle Arbeitsgrundlage; noch ungetestet.

Profile/LC V1 S1.23 All Pikmin Water Resistant.r2z
  Letzter praktisch getesteter Vergleichsstand.

Diagnose/LogOutput_S1.23_LastTest.log
  Letzter vollstaendiger S1.23-Diagnoselog. Relevant fuer Toy-Gun-Scrap, Atmosphere-Ladezeit und Frame-Drops.

Referenz/Offense_Referenz_Spawn-Rates.png
  Benutzer-Screenshot der frueheren Offense-Rarity-Verhaeltnisse, der fuer S1.24 als Referenz verwendet wurde.

NAECHSTER SCHRITT FUER DEN NEUEN CHAT
-------------------------------------
1. Zuerst Prompt und aktualisierte Verlauf-PDF als Vorgeschichte behandeln.
2. S1.24 als aktuelle Build-Basis verwenden.
3. Den beigefuegten S1.23-Log gezielt auf Toy-Gun-only, Atmosphere-Ladezeiten und Frame-Drops untersuchen.
4. Nach dem naechsten S1.24-Praxistest nur auf Basis der neuen Beobachtungen weiterbauen.
5. Nicht auf aeltere Profilstaende zurueckspringen, ausser fuer einen ausdruecklichen Vergleich.

SHA-256
-------
382b54ce11bb1edec2eca2bb82df1d092dc3feea72a60f5611b43ae887c5b379  Diagnose/LogOutput_S1.23_LastTest.log
18457aaf25c3c998bb0ca25d0825287d96466cf8c59d91781b739891f3404b4a  Dokumentation/Handover-Prompt_Lethal-Company_bis_S1.24.docx
9e2e68d0e89e9370f0948f9d26de7936e54f32a0b94e4955ed8458ef5e7b1db3  Dokumentation/Lethal-Company_Chatverlauf_Handover_bis_S1.24.pdf
f0366f9f94a32b623651ad2c1468439ecd103b37dd20ff49c47b052ec0bc1351  Profile/LC V1 S1.23 All Pikmin Water Resistant.r2z
4a68a9be611b86ea4782417a0c6158152b496e88bf50a2b5610f4f7fc59f0df4  Profile/LC V1 S1.24 Enemy Restore.r2z
aa73006ac77bb983538c78ddc798d265f3a7b1a664d14cf76d10503dc760bf05  Referenz/Offense_Referenz_Spawn-Rates.png
