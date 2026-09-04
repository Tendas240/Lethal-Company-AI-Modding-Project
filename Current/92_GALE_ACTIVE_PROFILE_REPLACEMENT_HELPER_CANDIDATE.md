# Gale Active Profile Replacement Helper — Historical Candidate Record

**Date:** 2026-09-04  
**Status:** USER-VALIDATED / PROMOTED / SUPERSEDED BY PERMANENT WORKFLOW

Canonical successor:

`Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`

## Purpose

This file preserves the validation history for the repository-backed Gale profile replacement helper. The maintained implementation remains:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

The helper is driven by repository state rather than a hard-coded build name.

It reads:

- `RuntimeInbox/ACTIVE_BUILD.txt` for the exact active build ID;
- `Current/AUTO_BUILD_RESULT.json` for the exact `output_profile` path and expected SHA-256.

It refuses to continue if the two sources disagree.

## Validated behavior

The user tested the final y/n version on 2026-09-04 under Windows PowerShell 5.1 using a disposable temporary Gale profile named `testpowershell` while S1.42AA was the active repository candidate.

Observed successful flow:

1. Gale closed;
2. active build resolved as `S1.42AA`;
3. exact repository profile resolved as `LC V1 S1.42AA Interior Weight Equalization.r2z`;
4. expected SHA-256 resolved as `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`;
5. profile downloaded before any local destructive action;
6. downloaded SHA-256 matched the repository build result exactly;
7. local Gale profiles were listed numerically;
8. disposable profile `testpowershell` was selected;
9. `y` confirmation successfully deleted only the selected profile;
10. the downloaded `.r2z` opened Gale's import flow;
11. the user used `Advanced options -> Import all files` and completed the import;
12. after user confirmation in PowerShell, the downloaded `.r2z` was removed from Downloads.

This closed the earlier helper bugs involving case-sensitive `LOESCHEN`, Windows PowerShell 5.1 array handling, and the automatic `$Matches` variable collision.

## Safety properties validated by this candidate

The helper deliberately performs the non-destructive work first:

1. resolve active build;
2. require `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
3. resolve exact profile path;
4. download profile;
5. verify SHA-256;
6. only then offer local profile deletion.

Deletion requires an explicit `y` answer. `n` leaves the selected local profile untouched and removes the temporary downloaded `.r2z`.

The helper never searches by fuzzy build-name matching and therefore avoids ambiguous IDs such as `S1.42A` vs `S1.42AA`.

## Remaining manual Gale step

Gale does not currently have a project-proven command-line switch in this workflow that safely forces `Advanced options -> Import all files`.

Therefore the helper deliberately opens the `.r2z` and requires the user to:

1. enable `Advanced options -> Import all files`;
2. complete the Gale import;
3. return to PowerShell and press Enter only after the import succeeded.

Do not replace this manual gate with blind GUI automation unless separately validated.

## Validated invocation

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

## Promotion outcome

The user subsequently required this launcher to be included automatically whenever a newly built profile is ready for runtime testing. The candidate has therefore been promoted to the permanent binding workflow in `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md` and `Current/09_REPOSITORY_FIRST_AUTOMATION.md`.

This file is retained only as historical validation evidence.
