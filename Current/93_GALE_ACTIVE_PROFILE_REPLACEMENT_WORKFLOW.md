# Gale Active Profile Replacement Workflow — Permanent

**Date:** 2026-09-04  
**Status:** CANONICAL / BINDING CHAT UX / BASE FLOW USER-VALIDATED / MISSING-PROFILE UIA REVISION USER-VALIDATION PENDING

## Purpose

This is the permanent repository-backed workflow for replacing the local Gale profile before testing a newly built runtime candidate.

Canonical implementation:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Historical candidate/validation record:

`Current/92_GALE_ACTIVE_PROFILE_REPLACEMENT_HELPER_CANDIDATE.md`

Current missing-profile revision record:

`Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`

## Mandatory ChatGPT behavior

Whenever ChatGPT has created or designated a new build/profile and the next project step is for the user to runtime-test that build, the same ChatGPT response that announces the ready-to-test build must include this copy/pasteable PowerShell one-line launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The user must not need to ask for this command again.

This profile-replacement command is required **in addition to** the separate mandatory build-specific runtime-log upload one-liner governed by `Current/09_REPOSITORY_FIRST_AUTOMATION.md`.

Therefore every new ready-to-test build response must provide both:

1. the canonical Gale active-profile replacement launcher above;
2. the exact build-specific `LogOutput.log` uploader for that candidate.

## Historically validated base behavior

The y/n implementation was successfully tested under Windows PowerShell 5.1 on 2026-09-04 using a disposable local Gale profile named `testpowershell` while S1.42AA was active.

The historically validated portion is:

1. close Gale;
2. read the active build from `RuntimeInbox/ACTIVE_BUILD.txt`;
3. require the same build ID in `Current/AUTO_BUILD_RESULT.json`;
4. resolve the exact repository `.r2z` and expected SHA-256 from the build result;
5. download the new profile before any destructive local action;
6. verify the downloaded SHA-256;
7. list local Gale profiles numerically;
8. let the user choose the local profile to remove;
9. require explicit `y/n` confirmation;
10. delete only the selected profile after `y`;
11. open the verified `.r2z` in Gale;
12. require the manual Gale gate `Advanced options -> Import all files`;
13. after the user confirms successful import in PowerShell, remove the temporary `.r2z` from Downloads.

If the user answers `n`, the selected local profile is not deleted and the temporary downloaded `.r2z` is cleaned up.

## Missing-profile startup gate discovered during S1.42AB

A later real replacement attempt exposed an additional Gale behavior that the disposable test did not fully exercise:

- deleting a profile directory outside Gale leaves Gale's internal profile record behind;
- on the next Gale startup, Gale intentionally opens a non-dismissible `Missing Profiles` dialog;
- each missing profile must be resolved with `Locate` or `Delete`, then `Submit`;
- while that dialog is open, the normal `.r2z` profile-import dialog can be blocked.

Current Gale source confirms this is an intentional recovery flow. The delete choice uses Gale's `forgetProfile` path; direct external SQLite editing is therefore not part of the project workflow.

## Current canonical missing-profile handling

After deleting the explicitly selected local profile and opening the already SHA-verified `.r2z`, the helper now performs a best-effort targeted Windows UI Automation pass.

Automatic `Delete -> Submit` is permitted only when all of the following hold:

1. Windows UI Automation is available;
2. a Gale window is detected;
3. `Missing Profiles` is visible;
4. the exact selected/deleted profile name is visible;
5. exactly one visible `Select an action` controller exists;
6. exactly one visible `Delete` option is exposed;
7. exactly one visible `Submit` control is exposed;
8. the dialog disappears after submission.

This is intentionally **not** screen-coordinate automation and **not** blind keyboard navigation.

If any check fails or more than one missing profile is present, the helper does not automatically delete anything. It falls back to a manual instruction for the user to resolve the intended profile using `Delete -> Submit`, waits for confirmation, and then continues.

After the blocking missing-profile dialog is resolved, the helper re-opens the same downloaded and SHA-verified `.r2z` to ensure the import event is delivered after the modal gate is gone.

The new UI-Automation branch is implemented but remains **user-validation pending** until the user confirms the revised flow in Gale. The older download/hash/selection/y-n safety flow remains validated.

## Safety requirements

Preserve these properties in future revisions:

- do not fuzzy-match build IDs or profile names;
- require `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- download and verify SHA-256 before offering deletion;
- keep destructive local-profile deletion behind explicit user confirmation;
- do not reintroduce the case-sensitive `LOESCHEN` flow;
- remain compatible with Windows PowerShell 5.1;
- do not use `$matches` as a normal variable because PowerShell's automatic `$Matches` variable is case-insensitive;
- do not directly edit Gale's `data.sqlite3` as part of the canonical helper;
- never automatically resolve multiple missing profiles;
- never use screen-coordinate clicks or blind `Tab`/`Enter` sequences for the missing-profile flow;
- do not automate `Advanced options -> Import all files` through GUI automation unless separately proven safe and explicitly approved.

## Current manual boundary

The helper may resolve the single known missing-profile startup gate, but the user still explicitly enables `Advanced options -> Import all files` and completes the actual Gale profile import. This is intentional and remains the safe project contract.

Any future change to this workflow must be documented and revalidated before its new behavior is described as user-validated.
