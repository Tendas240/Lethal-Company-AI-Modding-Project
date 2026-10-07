README HANDOVER — S1.42M

Kanonischer aktueller Testkandidat:
Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z

SHA-256:
9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7

Status:
gebaut und statisch verifiziert; noch nicht runtime-validiert.

Letzte valide Runtime-Evidenz:
RuntimeEvidence/S1.42L/20260903T155132Z/

Log SHA-256:
812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10

S1.42L Runtime-Ergebnis:
Pikmin -> lebender Baboon Hawk Attack/Latch/Kill PASS.
Neuer Fehler: Death-Cleanup/Corpse-Ownership.

Compatibility Plugin:
v1.3.8

DLL SHA-256:
47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf

Import:
Gale -> Advanced options -> Import all files

Manifest:
188 gesamt / 182 enabled / 6 disabled.

BCMER:
SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0 ist in S1.42M deaktiviert.

EnemyIsolation:
aktiv.

Kanonische Übergabe:
Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md

Detaillierte S1.42L-Analyse:
Current/47_S1.42L_BABOON_ATTACK_PASS_DEATH_REGRESSION_ANALYSIS.md

Nächster Schritt:
S1.42M unverändert runtime-testen. Pikmin müssen beim Hawk-Tod erhalten/detacht bleiben; der Dead Baboon Hawk Körper muss Pikmin-tragbar zur Onion bleiben; lebende Hawks dürfen ihn nicht aufnehmen; Hawk -> Pikmin Ignore muss intakt bleiben.

Runtime-Upload:
RuntimeInbox/Current/

Routing:
RuntimeInbox/ACTIVE_BUILD.txt = S1.42M

Build-Controller:
BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME

Nach PASS:
EnemyIsolation entfernen, normalen Enemy-Stand exakt aus Current/ENEMY_SPAWN_BASELINE_S1.42C.json wiederherstellen, BCMER 1.71.0 reaktivieren und den normalen Zustand runtime-testen.

Bekannte nicht-funktionale Dokumentations-/Kommentar-Drift bleibt bis nach dem offenen Runtime-Gate vertagt.
