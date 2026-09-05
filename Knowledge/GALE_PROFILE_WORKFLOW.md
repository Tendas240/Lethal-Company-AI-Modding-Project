# Gale Profile Replacement and Import

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic router to the fully user-validated Gale workflow  
**Canonical-For:** `gale_import`  
**Evidence:** `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
**Implementation:** `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
**Related:** `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`, `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`, `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`  
**Last-Validated:** 2026-09-04  
**Last-Hardened:** 2026-09-05 (critical dependency materialization proof; pending next user re-import)

## Canonical launcher

For a future ready-to-test build, use the repository-driven launcher rather than a build-name-specific script:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Before presenting it, the repository must have `RuntimeInbox/ACTIVE_BUILD.txt` and `Current/AUTO_BUILD_RESULT.json.build_id` pointing to the exact same ready candidate.

## Validated happy path

The helper was fully user-validated during S1.42AA -> S1.42AB on Windows PowerShell 5.1. It:

- closes Gale;
- resolves the exact repository candidate;
- downloads and SHA-256-verifies the `.r2z` before deletion is offered;
- asks the user to select the old local profile numerically and confirm deletion with `y`;
- opens the verified candidate exactly once;
- resolves the simple one-profile Gale `Missing Profiles` gate via semantic UI Automation;
- expands `Advanced options`;
- enables and verifies `Import all files`;
- invokes Import;
- waits for the exact target profile's local `export.r2x`;
- requires that local `export.r2x` hash to match the archive-entry hash;
- additionally requires project-critical external Thunderstore dependency DLLs referenced by the expected export to be physically materialized and non-empty in the imported profile;
- removes the temporary `.r2z` only after both export identity and required materialization proof succeed.

After profile number + `y`, no additional Gale click or PowerShell Enter is required on the validated happy path.

## Critical materialization proof

An exact `export.r2x` proves the imported profile metadata, but it does **not** by itself prove that Gale finished materializing every external Thunderstore package file. This distinction became operationally important when S1.42AE had the correct export metadata while BepInEx could not open the expected `loaforc-loaforcsSoundAPI_LethalCompany` DLL from the local Gale profile.

The helper therefore carries a narrow project-critical materialization contract. When the corresponding package names are present in the expected export, the import is not accepted until these files exist as non-empty files:

- `BepInEx\plugins\loaforc-loaforcsSoundAPI\me.loaforc.soundapi.dll`
- `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

This is a fail-closed sentinel for the observed dependency-installation failure. It is not a claim that every third-party Thunderstore DLL is embedded in the `.r2z`, and it does not replace runtime validation.

## Fail-closed requirements

Keep the exact workflow safety constraints from `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`, including:

- exact build/profile matching only;
- explicit confirmation before deleting a local profile;
- no direct editing of Gale `data.sqlite3`;
- no coordinate clicks or blind key navigation;
- never auto-resolve multiple missing profiles;
- no cache-busting query string on the binary `.r2z` Raw GitHub URL;
- exact post-import `export.r2x` evidence remains mandatory;
- required project-critical dependency files must also exist and be non-empty before the helper declares success or removes the downloaded `.r2z`;
- on materialization timeout/failure, report the missing relative paths and preserve the downloaded `.r2z` for diagnosis.

## Runtime-test pairing

The Gale replacement command never substitutes for the runtime-log uploader. Whenever a build is ready to test, both one-line PowerShell commands must be supplied together. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.
