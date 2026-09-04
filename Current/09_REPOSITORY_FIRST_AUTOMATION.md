# 09 — Repository-First Automation Policy

This file is binding for future project work unless the user explicitly changes the policy.

## Goal

The GitHub repository is the durable source of truth and build workspace.

Do not require a local repository clone on the user's PC for ChatGPT handovers, profile generation, patch compilation, build verification, or project documentation.

Do not ask the user to run local PowerShell build scripts when the required base artifacts already exist in GitHub.

## Canonical online locations

- Final Gale profiles: `Profiles/*.r2z`
- Human-/machine-readable profile contents: `ProfileSources/<build_id>/`
- Build request: `BuildSpecs/current.json`
- Build engine: `BuildSystem/profile_builder.py`
- Build workflow: `.github/workflows/profile-build.yml`
- Latest automated build result: `Current/AUTO_BUILD_RESULT.json` and `Current/AUTO_BUILD_RESULT.md`
- Runtime upload inbox: `RuntimeInbox/Current/`
- Active runtime build: `RuntimeInbox/ACTIVE_BUILD.txt`
- Persisted runtime evidence: `RuntimeEvidence/<build>/<timestamp>/`
- Canonical local Gale replacement helper: `RuntimeTools/ReplaceActiveGaleProfile.ps1`
- Permanent Gale replacement workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

## Future profile builds

ChatGPT should:

1. verify the exact base profile and its SHA-256 in `Profiles/`;
2. edit `BuildSpecs/current.json` directly on GitHub;
3. let GitHub Actions build the new profile;
4. inspect the workflow result/logs;
5. verify `Current/AUTO_BUILD_RESULT.*` and `ProfileSources/<build_id>/`;
6. continue project work from the generated GitHub profile.

The user should not need to download a base profile, edit an archive, run PowerShell, maintain a local repo clone, or calculate hashes.

The builder supports:
- internal Gale profile-name changes;
- exact enable/disable changes for existing Thunderstore packages;
- adding/removing exact Thunderstore package versions in `export.r2x`;
- BepInEx INI/config edits;
- repository-hosted file injection;
- building repository-hosted local .NET patches and injecting their output;
- exact base-hash guarding;
- member-delta verification;
- readable config/export snapshots.

## Mandatory ready-to-test build ChatGPT UX

Whenever ChatGPT produces or designates a **new build/profile whose next project step is runtime testing by the user**, the same ChatGPT response that announces that the build is ready to test must contain **both** of the following copy/pasteable PowerShell commands:

1. the canonical Gale active-profile replacement launcher;
2. the exact build-specific runtime-log uploader described below.

The user must not need to ask for either command again.

The Gale replacement launcher is always:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

It is repository-state driven and therefore must not be rewritten with a hard-coded build name. Before presenting it for a new candidate, ensure `RuntimeInbox/ACTIVE_BUILD.txt` and `Current/AUTO_BUILD_RESULT.json` both identify that exact ready-to-test build.

The full binding workflow and safety contract are documented in:

`Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

The replacement launcher does **not** replace the runtime-log uploader. Both commands are mandatory in every new ready-to-test build response.

## Runtime evidence

Game runtime itself necessarily happens on the user's PC. That is the remaining unavoidable local step.

After a test, the generated evidence goes to `RuntimeInbox/Current/`. The ingestion workflow then persists and extracts it online so ChatGPT can read it from GitHub.

The user should not need to rename `.cfg` to `.txt` merely for ChatGPT compatibility.

### Mandatory self-contained PowerShell upload one-liner for every new runtime test build

Whenever ChatGPT produces or designates a **new build/profile that the user is supposed to test next**, the same response that tells the user to test that build must also include exactly one ready-to-run **PowerShell one-line command** which uploads that exact Gale profile's:

`BepInEx\LogOutput.log`

from the local Gale profile directory:

`C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\<EXACT PROFILE NAME>\BepInEx\LogOutput.log`

to the repository path:

`RuntimeInbox/Current/LogOutput.log`

in:

`Tendas240/Lethal-Company-AI-Modding-Project`

The command must:

- contain the **exact new profile name**, not a placeholder, when ChatGPT already knows the build name;
- use GitHub CLI / GitHub API directly so a local repository clone is not required;
- target branch `main`;
- create `RuntimeInbox/Current/LogOutput.log` when absent;
- replace it safely when it already exists by supplying the current GitHub blob SHA;
- use a build-specific commit message such as `Upload S1.42Y runtime log`;
- be presented as a single copy/pasteable PowerShell line;
- be included automatically without waiting for the user to ask again;
- **self-bootstrap GitHub CLI robustly**: first resolve `gh` from the current PATH and the common installation paths `C:\Program Files\GitHub CLI\gh.exe`, `%LOCALAPPDATA%\Programs\GitHub CLI\gh.exe`, and `C:\Program Files (x86)\GitHub CLI\gh.exe`; only if still unresolved, invoke `winget install --id GitHub.cli ...` and then resolve `gh` again;
- **never treat the `winget` exit code alone as proof that GitHub CLI installation failed**. `winget install` can return a non-zero exit when GitHub CLI is already installed and no applicable upgrade exists. After any `winget` call, determine success by resolving an actual `gh.exe`; fail only if `gh` still cannot be found;
- work without requiring a PowerShell restart after a fresh GitHub CLI installation by resolving the executable directly from known installation paths;
- **self-bootstrap authentication**: if `gh auth status` is not already valid for github.com, run `gh auth login --hostname github.com --git-protocol https --web` inside the same command and continue to the upload after authentication completes;
- verify that the exact local `LogOutput.log` exists before attempting the upload and stop with a clear error if it does not.

Do **not** give the user a separate installation command plus a separate upload command when one self-contained command can do both. The normal expected UX is one pasted command per test build. The browser-based GitHub authorization may still require the user's interactive approval the first time, but it is launched from the same PowerShell command and the command continues afterwards.

### GitHub CLI bootstrap regression fixed 2026-09-04

An earlier canonical one-liner aborted incorrectly when `winget` reported that GitHub CLI was already installed/no newer applicable package was available, because it treated any non-zero `winget` exit code as a hard installation failure. That logic is superseded and must not be copied into future candidate records. The executable-presence check below is authoritative.

Canonical self-contained normal-log one-line pattern:

```powershell
$src='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\<EXACT PROFILE NAME>\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload <BUILD_ID> runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}
```

Do not substitute local clone / `git add` / `git push` instructions unless the direct GitHub CLI path is actually unavailable.

For unusually large logs that cannot safely use the normal GitHub Contents API / main-branch path, follow `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md` instead and provide the corresponding **single self-contained** large-log PowerShell command. Do not silently try to commit a >100 MiB raw log to `main`.

## Gale active-profile replacement helper — canonical and binding

The repository-backed local Gale profile replacement helper is maintained at:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Canonical workflow contract:

`Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

Historical validation record:

`Current/92_GALE_ACTIVE_PROFILE_REPLACEMENT_HELPER_CANDIDATE.md`

The user successfully validated the final y/n version under Windows PowerShell 5.1 with a disposable local Gale profile on 2026-09-04. The helper:

- closes Gale;
- resolves the exact active build from `RuntimeInbox/ACTIVE_BUILD.txt`;
- requires that `Current/AUTO_BUILD_RESULT.json` belongs to the same build;
- obtains the exact output profile path and SHA-256 from the build result rather than fuzzy-searching `Profiles/`;
- downloads the new `.r2z` before any destructive local action;
- verifies its SHA-256 before deletion is offered;
- numerically lists local Gale profiles;
- asks `y/n` before deleting only the selected local profile;
- opens the verified `.r2z` in Gale;
- keeps `Advanced options -> Import all files` as an explicit manual user gate;
- removes the downloaded `.r2z` only after the user confirms the import completed.

If the user answers `n`, no local profile is deleted and the temporary download is cleaned up.

This helper is now the **binding default profile-replacement workflow** for future ready-to-test builds. Every such build response must include the launcher in the Mandatory ready-to-test build ChatGPT UX section above.

Do not duplicate older experimental helper variants. In particular, do not reintroduce case-sensitive `LOESCHEN`, fuzzy profile-name matching, Windows PowerShell 5.1 array assumptions, or a variable named `$matches` that collides with PowerShell's automatic `$Matches` variable.

## Binary accessibility rule

Binary `.r2z`, `.zip`, and `.dll` artifacts may not be directly UTF-8-readable through the GitHub connector. Therefore every generated profile must also have:
- a readable `ProfileSources/<build_id>/` snapshot for text/config inspection;
- a file index containing member hashes;
- a GitHub Actions artifact for binary retrieval when required.

Binary manipulation should happen inside GitHub Actions, where repository checkout provides byte-accurate access.

## One-time migration — complete

The local-only gap has been closed.

Exact accepted S1.40B and canonical S1.41 were uploaded to `Profiles/` and automatically verified/indexed by GitHub Actions.

Verified online profiles:
- `Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z` — SHA-256 `fd303f73f0f2223a6375fcf2b7ed209dae77e1934e3b4e8139932a89e7de7eb9`
- `Profiles/LC V1 S1.41 BCMER Reactivation.r2z` — SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Readable snapshots:
- `ProfileSources/S1.40B/`
- `ProfileSources/S1.41/`

Future profile generation must default to GitHub-only automation. A local build chain is no longer required.
