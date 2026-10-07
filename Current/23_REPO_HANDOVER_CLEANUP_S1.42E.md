# 23 — Repository Handover Cleanup S1.42E

## KEEP

Keep as primary/diagnostic evidence:
- S1.41 accepted gameplay profile and runtime evidence;
- S1.42A/B/C profiles, snapshots and runtime evidence;
- S1.42D failed profile and its startup-crash evidence;
- S1.42E profile and snapshot;
- all project-local compatibility source/history;
- juijui original binary and extracted snapshot;
- S1.42C enemy restore baseline;
- CodeRebirth/BCMER/interior historical diagnostics;
- failed/obsolete approach history.

## UPDATE

Updated/currentized:
- README.md;
- Current/00_CURRENT_STATE.md;
- Current/01_HANDOVER_CORE.md;
- Current/02_TECHNICAL_BASELINE.md;
- Current/03_PROJECT_CHRONOLOGY.md;
- Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md;
- Current/05_FAILED_AND_OBSOLETE_APPROACHES.md;
- BuildSpecs/S1.42D_PLAN.md;
- Current/20_S1.42D_BUILD_AND_TEST.md;
- References/juijui_Referenzwerte.txt.

## ADD

New S1.42E handover/current files:
- Current/22_HANDOVER_S1.42E_TO_NEXT.md
- Current/23_REPO_HANDOVER_CLEANUP_S1.42E.md
- Current/06_RECENT_WORK_S1.42D-S1.42E.md
- Current/NEXT_CHAT_START_PROMPT_S1.42E.txt
- Current/README_Handover_S1.42E.txt
- Current/Projektstatus_S1.42E.json
- Current/Aktive_Modliste_S1.42E.txt
- Current/VERIFIKATION_S1.42E.txt
- Current/DATEIINVENTAR_S1.42E.txt
- Current/SHA256SUMS_S1.42E.txt

## ARCHIVE

The purely superseded S1.42C entrypoint files were moved out of Current:
- `Current/NEXT_CHAT_START_PROMPT_S1.42C.txt`
- `Current/README_Handover_S1.42C.txt`

They are now preserved under:
`Archive/S1.42C/HandoverCheckpoint/`

No information was lost; the archive prevents them from being mistaken for the current entrypoint.

Detailed S1.42C technical/runtime handovers remain available because they contain unique diagnostic history.

## DELETE

No unique project evidence should be permanently deleted.

The only incorrect evidence placement created during the S1.42D crash ingest was already corrected:
- the crash log/index were copied to `RuntimeEvidence/S1.42D/20260903T084247Z/`;
- the misclassified duplicates under S1.42C were removed.

That deletion removed only the incorrect duplicate location, not the evidence.

## Canonical control state

`BuildSpecs/current.json`:
disabled / `IDLE_AFTER_S1.42E_BUILD_AWAITING_RUNTIME`

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42E`
