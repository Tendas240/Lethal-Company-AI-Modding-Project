README HANDOVER — S1.42C CHECKPOINT

Accepted gameplay baseline:
S1.41
Profiles/LC V1 S1.41 BCMER Reactivation.r2z
SHA-256 d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b

Latest runtime-tested technical candidate:
S1.42C
Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z
SHA-256 22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3

Read first:
1. README.md
2. START_HERE_ChatGPT_Masterprompt.txt
3. Current/00_CURRENT_STATE.md
4. Current/01_HANDOVER_CORE.md
5. Current/16_HANDOVER_S1.42C_TO_NEXT.md
6. Current/17_REPO_HANDOVER_CLEANUP_S1.42C.md
7. Current/06_RECENT_WORK_S1.42A-S1.42C.md
7. Current/15_RUNTIME_EVIDENCE_S1.42C.md
8. Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md
9. Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md
10. Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md
11. Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md
12. BuildSpecs/S1.42D_PLAN.md
13. BuildSpecs/current.json
14. Current/Projektstatus_S1.42C.json
15. Current/Aktive_Modliste_S1.42C.txt
16. ProfileSources/S1.42C/

Key result:
LethalModDataLib NRE is fixed and runtime-confirmed. Null plugin entry was MW.MagicWesleyInteriors.

Highest engineering priority:
generic repair for LethalMin enemy-grab/bite + Invincible-Pikmin leader/follow state. Confirmed with Baboon Hawk in S1.42C.

Specific retained user requirements:
- Thumper and Pikmin must ignore each other completely.
- Puffer smoke/attack must not affect Pikmin.
- all interiors equal effective probability on all moons, including future interiors.
- reduce Mausoleum fog only.
- BCMER EventTypes = 12.5% each globally.
- Functional Microwave volume target 0.7 with edit gate.
- Jetpack old juijui duration: unresolved historical reference, do not guess.

BuildSpecs/S1.42D_PLAN.md is draft only.
BuildSpecs/current.json is disabled/idle.

Repository-first only.
Gale imports with local DLL:
Advanced options -> Import all files


Manifest note:
Current/Aktive_Modliste_S1.42C.txt was regenerated directly from ProfileSources/S1.42C/export.r2x during final handover verification after a shifted-version documentation error was discovered. Canonical counts remain 188 total / 183 enabled / 5 disabled.

Superseded S1.41 handover metadata are archived under:
Archive/S1.41/HandoverCheckpoint/
