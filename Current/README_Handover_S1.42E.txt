README HANDOVER — S1.42E CHECKPOINT

Accepted gameplay baseline:
S1.41
Profiles/LC V1 S1.41 BCMER Reactivation.r2z
SHA-256 d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b

Latest runtime-tested technical candidate reaching gameplay:
S1.42C
Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z
SHA-256 22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3

Failed diagnostic:
S1.42D
Startup crash during broad LethalMin reflection/Harmony patch scan.
DO NOT RETEST.
Evidence: RuntimeEvidence/S1.42D/20260903T084247Z/

Next built test candidate:
S1.42E
Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z
SHA-256 4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348
Status: built, NOT runtime tested yet.

First gate:
Reach Main Menu without crash.

If startup succeeds:
- safe LethalMin registration marker must complete;
- then test Baboon Hawk generic grabbed-state recovery;
- Thumper<->Pikmin zero interaction;
- Puffer smoke/attack no Pikmin effect;
- Jetpack ~140s and no sustained/high-speed mid-air self-explosion;
- Microwave volume 0.7.

Temporary enemy isolation in S1.42E:
Indoor: Crawler/Thumper + Puffer
Outdoor: Baboon Hawk
Daytime: none
Full normal enemy configuration restore source:
Current/ENEMY_SPAWN_BASELINE_S1.42C.json

Historical juijui:
References/LegacyProfiles/juijui/juijui.r2z
SHA-256 ddd10bcec3329c155b3a0a2d74460928b02df147356701fb6cf79ebb5a9f7e00
Recovered Jetpack evidence: JetpackBatteryUsage = 140.

Build control:
BuildSpecs/current.json disabled / IDLE_AFTER_S1.42E_BUILD_AWAITING_RUNTIME

Runtime routing:
RuntimeInbox/ACTIVE_BUILD.txt = S1.42E
Upload LogOutput.log to RuntimeInbox/Current/

Import:
Gale -> Advanced options -> Import all files

Read first:
1. README.md
2. START_HERE_ChatGPT_Masterprompt.txt
3. Current/00_CURRENT_STATE.md
4. Current/01_HANDOVER_CORE.md
5. Current/22_HANDOVER_S1.42E_TO_NEXT.md
6. Current/21_S1.42D_CRASH_S1.42E_HOTFIX.md
7. Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md
8. Current/05_FAILED_AND_OBSOLETE_APPROACHES.md
9. Current/06_RECENT_WORK_S1.42D-S1.42E.md
10. Current/18_JUIJUI_LEGACY_REFERENCE.md
11. Current/Projektstatus_S1.42E.json
12. Current/VERIFIKATION_S1.42E.txt
13. ProfileSources/S1.42E/
14. BuildSpecs/current.json

Repository-first only.
