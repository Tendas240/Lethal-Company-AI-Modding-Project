# Gale Active Profile Replacement Workflow — Permanent

**Date:** 2026-09-04  
**Status:** USER-VALIDATED / CANONICAL / BINDING CHAT UX

## Purpose

This is the permanent repository-backed workflow for replacing the local Gale profile before testing a newly built runtime candidate.

Canonical implementation:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Historical candidate/validation record:

`Current/92_GALE_ACTIVE_PROFILE_REPLACEMENT_HELPER_CANDIDATE.md`

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

## Validated behavior

The final y/n implementation was successfully tested under Windows PowerShell 5.1 on 2026-09-04 using a disposable local Gale profile named `testpowershell` while S1.42AA was active.

Validated flow:

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

## Safety requirements

Preserve these properties in future revisions:

- do not fuzzy-match build IDs or profile names;
- require `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- download and verify SHA-256 before offering deletion;
- keep destructive deletion behind explicit user confirmation;
- do not reintroduce the case-sensitive `LOESCHEN` flow;
- remain compatible with Windows PowerShell 5.1;
- do not use `$matches` as a normal variable because PowerShell's automatic `$Matches` variable is case-insensitive;
- do not automate `Advanced options -> Import all files` through blind GUI keystrokes unless separately proven safe.

## Current manual boundary

The helper opens the `.r2z`, but the user still explicitly enables `Advanced options -> Import all files` and completes the Gale import. This is intentional and remains the safe project contract.

Any future change to this workflow must be documented and revalidated before replacing `RuntimeTools/ReplaceActiveGaleProfile.ps1` as the canonical implementation.
