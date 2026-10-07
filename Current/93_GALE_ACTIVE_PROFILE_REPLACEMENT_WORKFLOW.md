# Gale Active Profile Replacement Workflow — Permanent

**Date:** 2026-09-04  
**Status:** CANONICAL / BINDING CHAT UX / FULL END-TO-END USER-VALIDATED

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

## Fully validated normal UX

The complete replacement flow was successfully validated on the real project machine under Windows PowerShell 5.1 during the S1.42AA -> S1.42AB transition.

After the user runs the launcher, the normal interaction boundary is now only:

1. choose the old local Gale profile numerically;
2. confirm destructive replacement with `y`.

After that confirmation, the helper performs the remaining replacement automatically unless a fail-closed safety fallback is triggered.

Validated end-to-end behavior:

1. close Gale;
2. read `RuntimeInbox/ACTIVE_BUILD.txt`;
3. require exact equality with `Current/AUTO_BUILD_RESULT.json.build_id`;
4. resolve exact output `.r2z`, profile name and SHA-256;
5. download the candidate before any destructive local action;
6. verify the candidate SHA-256;
7. compute the expected SHA-256 of the archive's `export.r2x` entry;
8. list local Gale profiles numerically;
9. let the user choose the profile to replace;
10. require explicit `y/n` confirmation;
11. delete only the selected profile after `y`;
12. open the verified `.r2z` exactly once;
13. resolve Gale's `Missing Profiles` dialog automatically for the one-profile case using `Delete -> Submit`;
14. wait for the already-buffered target-profile import dialog from the original `.r2z` open event;
15. expand `Advanced options`;
16. enable and verify `Import all files`;
17. invoke `Import`;
18. wait for the exact target profile's local `export.r2x`;
19. require that local file's SHA-256 to equal the `export.r2x` SHA-256 computed from the verified build archive;
20. remove the temporary downloaded `.r2z` only after that post-import evidence passes.

No additional Gale click or PowerShell Enter is required after profile selection / `y` during the validated happy path.

If the user answers `n`, no local profile is deleted and the temporary archive is cleaned up.

## Missing-profile startup gate — USER-VALIDATED

Real S1.42AB replacement exposed Gale's intentional `Missing Profiles` dialog after an externally deleted profile directory remains in Gale's internal database.

The helper resolves the simple one-missing-profile case through targeted Windows UI Automation:

- exactly one actionable `Select an action` control with `ExpandCollapsePattern`;
- exactly one actionable `Delete` item with `SelectionItemPattern`;
- exactly one actionable `Submit` button with `InvokePattern`;
- dialog disappearance verified after submission.

This path was tested repeatedly with the real S1.42AA -> S1.42AB starting condition and completed automatically without manual dialog interaction.

Therefore the Missing Profiles automation is **user-validated**.

## Import-dialog automation — USER-VALIDATED

The semantic UIA sequence is:

1. detect the localized full target-profile import dialog;
2. require the exact expected target profile identity;
3. expand `Advanced options` / `Erweiterte Optionen`;
4. require exactly one visible toggle in the create-new import dialog;
5. set `Import all files` to On and verify On;
6. require exactly one dialog-local `Import` / `Importieren` button;
7. invoke Import.

V1 first proved on the user's actual Gale/WebView that this UIA targeting could activate `Import all files` and start the import, but V1 reopened the same `.r2z` after resolving Missing Profiles and therefore generated a second empty import-code dialog through Gale's single-instance/deep-link path.

V2 removed the duplicate `.r2z` event and replaced transient success-toast detection with post-import `export.r2x` evidence. Its first controlled test failed safely before deletion because a cache-busting query string on the binary Raw GitHub `.r2z` download returned HTTP 404.

V2.1 removed that unnecessary binary-download query string while preserving the single-open/import/hash-evidence architecture.

## V2.1 validation — FULL PASS

Validated helper marker:

`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob:

`9458f427b538615249714e7f064f3107d6dcd36c`

Validated implementation commit:

`f711f53f4971f97200ed3605479ef887a14b243d`

Controlled test starting condition:

- S1.42AA existed normally in Gale;
- S1.42AB was not locally imported;
- the commit-pinned V2.1 helper was executed;
- the user selected S1.42AA and confirmed replacement with `y`.

Observed PASS evidence from PowerShell:

- candidate profile SHA-256 matched the repository expectation;
- `export.r2x` evidence SHA-256 was computed before deletion;
- S1.42AA was deleted only after explicit `y`;
- Gale `Missing Profiles` was resolved automatically with `Delete -> Submit`;
- the helper waited for the import dialog from the single original `.r2z` invocation;
- `Import all files` was activated automatically;
- Import was triggered automatically;
- no second empty import-code dialog appeared;
- the resulting local profile was exactly `LC V1 S1.42AB Interior Weight Normalization`;
- the imported target profile's local `export.r2x` matched the expected archive-entry SHA-256;
- the downloaded `.r2z` was removed automatically;
- PowerShell returned to the prompt with no manual Gale click or final Enter after profile selection / `y`.

Therefore the complete replacement workflow is **FULL END-TO-END USER-VALIDATED**.

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
- every UI Automation branch must fail closed and retain a safe manual fallback;
- open the candidate `.r2z` exactly once during the automated replacement sequence;
- do not add cache-busting query strings to the binary `.r2z` Raw GitHub download; integrity is enforced by the exact SHA-256 check;
- keep post-import verification tied to the exact target profile and exact `export.r2x` archive-entry SHA-256;
- do not describe future changed automation branches as user-validated until the changed behavior is actually tested on the project machine.

## Canonical normal UX

1. run the canonical one-line launcher;
2. select the old profile numerically;
3. confirm with `y`;
4. the helper handles Gale startup recovery, `Import all files`, Import, exact `export.r2x` verification and temporary archive cleanup automatically;
5. no further Gale click or PowerShell Enter is required unless a fail-closed fallback is triggered.
