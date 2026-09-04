# Gale Active Profile Replacement Workflow — Permanent

**Date:** 2026-09-04  
**Status:** CANONICAL / BINDING CHAT UX / BASE FLOW USER-VALIDATED / MISSING-PROFILE UIA USER-VALIDATED / IMPORT UIA V2 USER-VALIDATION PENDING

## Purpose

This is the permanent repository-backed workflow for replacing the local Gale profile before testing a newly built runtime candidate.

Canonical implementation:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Historical candidate/validation record:

`Current/92_GALE_ACTIVE_PROFILE_REPLACEMENT_HELPER_CANDIDATE.md`

Missing-profile automation record:

`Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`

Import-dialog automation record:

`Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`

## Mandatory ChatGPT behavior

Whenever ChatGPT has created or designated a new build/profile and the next project step is runtime testing by the user, the same response must include both:

1. the canonical Gale active-profile replacement launcher;
2. the exact build-specific runtime-log uploader governed by `Current/09_REPOSITORY_FIRST_AUTOMATION.md`.

Canonical cache-busting launcher:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

During helper-development validation, prefer a commit-pinned Raw GitHub URL so the exact tested revision is deterministic.

## Validated base behavior

The base y/n implementation was successfully tested under Windows PowerShell 5.1 on 2026-09-04.

Validated properties:

1. close Gale;
2. read `RuntimeInbox/ACTIVE_BUILD.txt`;
3. require exact equality with `Current/AUTO_BUILD_RESULT.json.build_id`;
4. resolve exact output `.r2z`, profile name and SHA-256;
5. download before any destructive local action;
6. verify SHA-256;
7. list local Gale profiles numerically;
8. let the user choose the profile to replace;
9. require explicit `y/n` confirmation;
10. delete only the selected profile after `y`;
11. no fuzzy build/profile matching;
12. no local repository clone required.

If the user answers `n`, no local profile is deleted and the temporary archive is cleaned up.

## Missing-profile startup gate — USER-VALIDATED

Real S1.42AB replacement exposed Gale's intentional `Missing Profiles` dialog after an externally deleted profile directory remains in Gale's internal database.

The helper resolves the simple one-missing-profile case through targeted Windows UI Automation:

- exactly one actionable `Select an action` control with `ExpandCollapsePattern`;
- exactly one actionable `Delete` item with `SelectionItemPattern`;
- exactly one actionable `Submit` button with `InvokePattern`;
- dialog disappearance verified after submission.

This path was tested by the user with the real S1.42AA -> S1.42AB starting condition using the commit-pinned interaction-pattern revision. Result: `Missing Profiles -> Delete -> Submit` completed automatically and the normal import dialog became available with no manual dialog interaction.

Therefore the Missing Profiles automation is **user-validated**.

## Import-dialog automation

The intended semantic UIA sequence is:

1. detect the localized full target-profile import dialog;
2. require the exact expected target profile identity;
3. expand `Advanced options` / `Erweiterte Optionen`;
4. require exactly one visible toggle in the create-new import dialog;
5. set `Import all files` to On and verify On;
6. require exactly one dialog-local `Import` / `Importieren` button;
7. invoke Import.

V1 proved on the user's actual Gale/WebView that this UIA targeting can activate `Import all files` and start the import. S1.42AB was successfully created/activated.

However, V1 also reopened the same `.r2z` a second time after resolving Missing Profiles. Gale's single-instance/deep-link path therefore received two import events, which produced a second empty import-code dialog after the real import completed. This was a helper sequencing defect, not a build/import failure.

## Current V2 contract

Current helper marker:

`2026-09-04-import-uia-v2-single-open-evidence`

Current helper blob:

`aa2b5ac7084fb08f75382405658b4ffa49452587`

Current implementation commit:

`2c25fccabdf177a6cc114a3eaba752014cf5cb45`

V2 changes the sequencing and completion proof:

1. the SHA-verified `.r2z` is opened exactly once;
2. after Missing Profiles closes, the helper waits for the already-buffered full import dialog from that original file-open event;
3. the `.r2z` is not re-sent to Gale;
4. before opening Gale, the helper computes the SHA-256 of the archive's `export.r2x` entry;
5. after Import, it waits for the exact local target profile's `export.r2x` and requires the same SHA-256;
6. that filesystem/hash evidence replaces the fragile success-toast dependency;
7. matching `export.r2x` also proves that `Import all files` copied the expected full-profile evidence;
8. temporary `.r2z` cleanup happens only after this verification passes;
9. manual fallbacks no longer require an additional PowerShell Enter merely to acknowledge that the dialog/import completed; PowerShell polls for dialog closure or final profile evidence automatically.

V2 is implemented but requires one user validation before being described as fully user-validated.

## Safety requirements

Preserve these properties:

- exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- download and SHA-256 verification before deletion;
- destructive local-profile deletion only after explicit `y`;
- abort if the exact new target profile already exists separately;
- no fuzzy profile/build matching;
- Windows PowerShell 5.1 compatibility;
- do not use `$matches` as a normal variable;
- do not directly edit Gale's `data.sqlite3`;
- never automatically resolve multiple missing profiles;
- no screen-coordinate mouse clicks;
- no blind `Tab` / `Enter` / arrow-key automation;
- every UI Automation branch must fail closed and retain a manual fallback;
- do not describe a new automation branch as user-validated until the user confirms it on the project machine.

## Intended normal UX after V2 validation

1. run the canonical one-line launcher;
2. select the old profile numerically;
3. confirm with `y`;
4. helper handles Missing Profiles, `Import all files`, Import, exact `export.r2x` verification and archive cleanup automatically;
5. no further Gale click or PowerShell Enter should be required unless a fail-closed fallback is triggered.