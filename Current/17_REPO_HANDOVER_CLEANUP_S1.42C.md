# 17 — Repository Handover Cleanup S1.42C

**Date:** 2026-09-03

This cleanup was performed as part of the S1.42C -> next-chat handover.

## KEEP

Retain without deletion because they contain current, runtime, build, or diagnostic value:

- `Profiles/LC V1 S1.41 BCMER Reactivation.r2z` — last fully accepted gameplay baseline.
- S1.42A/B/C profiles and `ProfileSources/` snapshots — required lineage and regression bases.
- `RuntimeEvidence/S1.42A/`, `RuntimeEvidence/S1.42B/`, `RuntimeEvidence/S1.42C/`.
- `Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md`.
- `Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md`.
- `Current/15_RUNTIME_EVIDENCE_S1.42C.md`.
- `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`.
- Build plans S1.42A/B/C and draft S1.42D.
- `Patches/S139CompatibilityFixes/`.
- historical runtime/diagnostic material with unique evidence.

## UPDATE

Updated during this handover:

- `README.md`
- `Current/00_CURRENT_STATE.md`
- `Current/01_HANDOVER_CORE.md`
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
- `Current/06_RECENT_WORK_S1.42A-S1.42C.md`
- `Current/16_HANDOVER_S1.42C_TO_NEXT.md`
- `Current/Projektstatus_S1.42C.json`
- `Current/Aktive_Modliste_S1.42C.txt`
- `Current/README_Handover_S1.42C.txt`
- `Current/DATEIINVENTAR_S1.42C.txt`
- `Current/VERIFIKATION_S1.42C.txt`
- `BuildSpecs/current.json`

### Manifest correction

The previously generated `Current/Aktive_Modliste_S1.42C.txt` had shifted package/version associations.

It was regenerated directly from:

`ProfileSources/S1.42C/export.r2x`

Verified canonical manifest:
- 188 Thunderstore entries
- 183 enabled
- 5 disabled

Correct disabled set:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

This was a documentation-generation error only; the S1.42C profile itself was not changed.

## ADD

Current handover additions:
- `Current/15_RUNTIME_EVIDENCE_S1.42C.md`
- `Current/16_HANDOVER_S1.42C_TO_NEXT.md`
- `Current/17_REPO_HANDOVER_CLEANUP_S1.42C.md`
- `Current/NEXT_CHAT_START_PROMPT_S1.42C.txt`
- `Current/README_Handover_S1.42C.txt`
- `Current/Projektstatus_S1.42C.json`
- `Current/Aktive_Modliste_S1.42C.txt`
- `Current/VERIFIKATION_S1.42C.txt`
- `Current/DATEIINVENTAR_S1.42C.txt`
- `Current/SHA256SUMS_S1.42C.txt`
- `BuildSpecs/S1.42D_PLAN.md`

## ARCHIVE

The superseded S1.41 handover-support metadata are moved out of `Current/` into:

`Archive/S1.41/HandoverCheckpoint/`

These are preserved for reconstruction, but are no longer valid current entrypoints.

## DELETE

No project information is permanently deleted.

Files removed from `Current/` in this cleanup are first copied verbatim into `Archive/S1.41/HandoverCheckpoint/`.

## Binding current entrypoints

Use:
- `README.md`
- `START_HERE_ChatGPT_Masterprompt.txt`
- `Current/00_CURRENT_STATE.md`
- `Current/01_HANDOVER_CORE.md`
- `Current/16_HANDOVER_S1.42C_TO_NEXT.md`
- `Current/NEXT_CHAT_START_PROMPT_S1.42C.txt`

Do not use an archived S1.41 next-chat prompt as an operational instruction.
