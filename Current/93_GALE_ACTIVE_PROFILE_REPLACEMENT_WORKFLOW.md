# Gale Active Profile Replacement Workflow — Permanent

**Date:** 2026-09-04  
**Status:** CANONICAL / BINDING CHAT UX / BASE FLOW USER-VALIDATED / MISSING-PROFILE UIA USER-VALIDATED / IMPORT UIA USER-VALIDATION PENDING

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

Whenever ChatGPT has created or designated a new build/profile and the next project step is for the user to runtime-test that build, the same response that announces the ready-to-test build must include this launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The same response must also include the exact build-specific runtime-log uploader governed by `Current/09_REPOSITORY_FIRST_AUTOMATION.md`.

During helper-development validation, prefer a commit-pinned Raw GitHub URL so the exact tested script revision is deterministic and not affected by mutable-`main` cache ambiguity.

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
12. no local repository clone required;
13. temporary `.r2z` cleanup occurs only after the import is confirmed successful or the explicit fallback confirmation is given.

If the user answers `n`, no local profile is deleted and the temporary archive is cleaned up.

## Missing-profile startup gate

Real S1.42AB replacement exposed Gale's intentional `Missing Profiles` dialog after an externally deleted profile directory remains in Gale's internal database.

The helper now resolves the simple one-missing-profile case through targeted Windows UI Automation. It filters the WebView accessibility tree by actual supported interaction patterns rather than raw text-node uniqueness:

- exactly one actionable `Select an action` control with `ExpandCollapsePattern`;
- exactly one actionable `Delete` item with `SelectionItemPattern`;
- exactly one actionable `Submit` button with `InvokePattern`;
- dialog disappearance verified after submission.

This path was tested by the user with the real S1.42AA -> S1.42AB starting condition using the commit-pinned revision from commit:

`2e3aaf5e9dc8381b979ce85b03e38970cf55fbf4`

Result: `Missing Profiles -> Delete -> Submit` completed automatically and the normal S1.42AB import dialog became available without manual interaction.

Therefore the missing-profile automation is **user-validated**.

## Import-dialog automation — current test revision

The user then requested automation of the remaining manual step:

`Advanced options -> Import all files -> Import`

The current helper revision implements a fail-closed targeted UIA flow:

1. detect the localized Gale import dialog (`Import profile` / `Profil importieren`);
2. resolve a dialog-local scope;
3. require the exact expected target profile name to be exposed as an accessible name or input value;
4. expand `Advanced options` / `Erweiterte Optionen` through `ExpandCollapsePattern`, or a unique `InvokePattern` fallback;
5. require exactly one visible `TogglePattern` control in the new-profile import dialog;
6. set that toggle to `On` and verify it is `On`;
7. require exactly one dialog-local `Import` / `Importieren` button with `InvokePattern`;
8. invoke Import;
9. wait for Gale's localized success message for the exact profile name;
10. remove the temporary `.r2z` only after confirmed success.

If the final success toast is not exposed by UI Automation, the helper asks only for the final success confirmation before cleanup.

If any import-dialog target is ambiguous, the helper clicks nothing blindly and falls back to the manual import instructions.

Current import-automation test revision:

- helper marker: `2026-09-04-import-uia-v1`;
- helper blob: `689c9dcd7cbc38fcf9735309336106322a6203d8`;
- implementation commit: `cace6989f12ed9c47d72e806851d17cdd706948b`.

This import automation remains **user-validation pending** until the user confirms that the whole post-`y` flow requires no manual Gale click.

## Safety requirements

Preserve these properties in future revisions:

- exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- download and SHA-256 verification before deletion;
- destructive local-profile deletion only after explicit `y`;
- abort if the exact new target profile already exists separately, rather than risk unintended overwrite;
- no fuzzy profile/build matching;
- remain compatible with Windows PowerShell 5.1;
- do not use `$matches` as a normal variable because PowerShell's automatic `$Matches` variable is case-insensitive;
- do not directly edit Gale's `data.sqlite3`;
- never automatically resolve multiple missing profiles;
- no screen-coordinate mouse clicks;
- no blind `Tab` / `Enter` / arrow-key automation;
- every UI Automation branch must fail closed and retain a manual fallback;
- do not describe a new automation branch as user-validated until the user has actually confirmed it on the project machine.

## Current intended UX

Once the import-dialog revision is validated, the intended normal profile replacement UX is:

1. run the canonical one-line launcher;
2. select the old profile numerically;
3. confirm with `y`;
4. the helper handles Gale startup recovery, `Import all files`, Import, and temporary archive cleanup automatically;
5. no further Gale click should be required unless a fail-closed fallback is triggered.
