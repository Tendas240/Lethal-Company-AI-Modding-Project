# 09 — Repository-First Automation Policy

This file is binding for future project work unless the user explicitly changes the policy.

## Goal

The GitHub repository is the durable source of truth and build workspace.

Do not require a local repository clone on the user's PC for ChatGPT handovers, profile generation, patch compilation, build verification, or project documentation.

Do not ask the user to run local PowerShell build scripts when the required base artifacts already exist in GitHub.

Game runtime itself necessarily remains local; build/profile generation and durable evidence handling remain repository-first.

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
- Missing-profile automation record: `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`
- Import-dialog automation record: `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`

## Future profile builds

ChatGPT should:

1. verify the exact base profile and its SHA-256 in `Profiles/`;
2. edit `BuildSpecs/current.json` directly on GitHub;
3. let GitHub Actions build the new profile;
4. inspect the workflow result/logs;
5. verify `Current/AUTO_BUILD_RESULT.*` and `ProfileSources/<build_id>/`;
6. continue project work from the generated GitHub profile.

The user should not need to download a base profile, edit an archive, run PowerShell build scripts, maintain a local repo clone, or calculate profile hashes manually.

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

Whenever ChatGPT produces or designates a **new build/profile whose next project step is runtime testing by the user**, the same response that announces that the build is ready to test must contain **both** of the following copy/pasteable PowerShell commands:

1. the canonical Gale active-profile replacement launcher;
2. the exact build-specific runtime-log uploader described below.

The user must not need to ask for either command again.

The canonical Gale replacement launcher is:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

It is repository-state driven and must not be rewritten with a hard-coded build name. Before presenting it for a new candidate, ensure `RuntimeInbox/ACTIVE_BUILD.txt` and `Current/AUTO_BUILD_RESULT.json` both identify that exact ready-to-test build.

The full binding workflow and safety contract are documented in:

`Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

The replacement launcher does **not** replace the runtime-log uploader. Both commands are mandatory in every new ready-to-test build response.

## Gale active-profile replacement helper — canonical and fully user-validated

The repository-backed helper is maintained at:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

The complete end-to-end flow was user-validated under Windows PowerShell 5.1 during the real S1.42AA -> S1.42AB replacement.

Validated normal happy path:

1. helper closes Gale;
2. resolves the exact active build from `RuntimeInbox/ACTIVE_BUILD.txt`;
3. requires exact equality with `Current/AUTO_BUILD_RESULT.json.build_id`;
4. obtains exact output profile path, target profile name and expected SHA-256;
5. downloads the `.r2z` before any destructive local action;
6. verifies the exact candidate SHA-256;
7. computes the SHA-256 of the candidate archive's `export.r2x` entry;
8. numerically lists local Gale profiles;
9. user selects the old profile;
10. user explicitly confirms deletion with `y`;
11. helper deletes only that selected profile;
12. helper opens the verified candidate `.r2z` exactly once;
13. Gale's simple one-profile `Missing Profiles` gate is resolved automatically through targeted UI Automation using `Delete -> Submit`;
14. helper waits for the target-profile import dialog already buffered by that same `.r2z` open event;
15. `Advanced options` is expanded automatically;
16. `Import all files` is enabled and verified automatically;
17. `Import` is invoked automatically;
18. helper waits for the exact new target profile's local `export.r2x`;
19. local `export.r2x` SHA-256 must equal the candidate archive-entry SHA-256;
20. only after that exact evidence passes is the temporary downloaded `.r2z` removed.

Therefore, after **profile number + `y`**, no further Gale click or PowerShell Enter is required during the validated happy path.

If any UI Automation target is ambiguous, the helper fails closed and retains safe manual fallback behavior. It never uses screen-coordinate clicks or blind `Tab` / `Enter` / arrow-key sequences.

Permanent helper safety requirements:

- exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- no fuzzy build/profile matching;
- candidate download and SHA-256 verification before deletion is offered;
- destructive deletion only after explicit `y`;
- abort if the exact target profile already exists separately;
- Windows PowerShell 5.1 compatibility;
- do not use `$matches` as a normal variable because PowerShell's automatic `$Matches` variable is case-insensitive;
- do not directly modify Gale's `data.sqlite3`;
- never automatically resolve multiple missing profiles;
- no screen-coordinate mouse automation;
- no blind keyboard-navigation automation;
- open the candidate `.r2z` exactly once per automated replacement sequence;
- do not append cache-busting query strings to the binary Raw GitHub `.r2z` URL; integrity is enforced by exact SHA-256;
- completion proof is the exact target profile's `export.r2x` hash matching the archive entry, not a transient Gale toast;
- future changed automation branches must be revalidated before being described as proven.

Current validated helper revision details and historical failed attempts are documented in `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`.

## Runtime evidence

After a gameplay test, the generated evidence goes to `RuntimeInbox/Current/`. The ingestion workflow then persists and extracts it online so ChatGPT can read it from GitHub.

The user should not need to rename `.cfg` to `.txt` merely for ChatGPT compatibility.

### Mandatory self-contained PowerShell upload one-liner for every new runtime test build

Whenever ChatGPT produces or designates a **new build/profile that the user is supposed to test next**, the same response that tells the user to test that build must also include exactly one ready-to-run **PowerShell one-line command** which uploads that exact Gale profile's:

`BepInEx\LogOutput.log`

from the local Gale profile directory:

`C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\<EXACT PROFILE NAME>\BepInEx\LogOutput.log`

to:

`RuntimeInbox/Current/LogOutput.log`

in:

`Tendas240/Lethal-Company-AI-Modding-Project`

The command must:

- contain the exact new profile name when known;
- use GitHub CLI / GitHub API directly so a local repository clone is not required;
- target branch `main`;
- create `RuntimeInbox/Current/LogOutput.log` when absent;
- replace it safely when it already exists by supplying the current GitHub blob SHA;
- use a build-specific commit message such as `Upload S1.42AB runtime log`;
- be presented as one copy/pasteable PowerShell line;
- be included automatically without waiting for the user to ask;
- resolve `gh` from PATH and the common install locations before attempting installation;
- only if still unresolved, run `winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements` and then resolve `gh` again;
- never treat the `winget` exit code alone as proof of installation failure;
- work without requiring a PowerShell restart after fresh GitHub CLI installation;
- self-bootstrap GitHub authentication with `gh auth login --hostname github.com --git-protocol https --web` when needed;
- verify the exact local `LogOutput.log` exists before upload and fail clearly if absent.

Do **not** give the user a separate GitHub CLI installation command plus a separate upload command when one self-contained command can do both.

Canonical normal-log one-line pattern:

```powershell
$src='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\<EXACT PROFILE NAME>\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload <BUILD_ID> runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}
```

Do not substitute local clone / `git add` / `git push` instructions unless the direct GitHub CLI path is actually unavailable.

For unusually large logs that cannot safely use the normal GitHub Contents API / main-branch path, follow `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md` instead and provide the corresponding single self-contained large-log PowerShell command. Do not silently try to commit a >100 MiB raw log to `main`.

## Binary accessibility rule

Binary `.r2z`, `.zip`, and `.dll` artifacts may not be directly UTF-8-readable through the GitHub connector. Therefore every generated profile must also have:

- a readable `ProfileSources/<build_id>/` snapshot for text/config inspection;
- a file index containing member hashes;
- a GitHub Actions artifact for binary retrieval when required.

Binary manipulation should happen inside GitHub Actions, where repository checkout provides byte-accurate access.

## One-time migration — complete

The local-only gap has been closed. Canonical profiles and readable snapshots now live in GitHub, and future profile generation must default to GitHub-only automation. A local build chain is no longer required.
