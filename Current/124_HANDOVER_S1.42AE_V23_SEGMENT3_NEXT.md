# Handover Checkpoint — S1.42AE v2.3 Recovery / Technical Segment 3 Next

**Date:** 2026-09-05  
**Status:** CURRENT HANDOVER CHECKPOINT  
**Purpose:** durable continuation point for transfer to a fresh ChatGPT chat  
**Repository Source of Truth:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Governing execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`

## 1. Current state

- Accepted full-normal-stack baseline: **S1.42AC — BCMER EventType Equal Distribution**.
- Accepted S1.42AC profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`.
- Accepted S1.42AC SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`.
- Latest built artifact and active runtime candidate: **S1.42AE — Functional Microwave Provider Contract Correction**.
- S1.42AE profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`.
- S1.42AE SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`.
- S1.42AE injected DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`.
- S1.42AE status: **BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AE`.
- `BuildSpecs/current.json` is disabled with id `IDLE_AFTER_S1.42AE_BUILD_AWAITING_RUNTIME_VALIDATION`.
- No successor is armed. Do not build S1.42AF or any other successor before S1.42AE runtime evidence is evaluated.
- No valid fresh S1.42AE `LogOutput.log` has been ingested yet.

At the start of this handover request, verified `main` was:

`c2aa8b2dd5d91d74601c09172e43bd4da7216b3b`

The corresponding `Knowledge Architecture` push run was `33976199579` and completed successfully with all permanent validation steps green. The final handover segment must re-resolve the final merged `main` commit/run after this handover checkpoint itself is merged.

## 2. What has been completed

### S1.42AE build and provider correction

S1.42AE was built successfully from the accepted S1.42AC baseline. It corrects rejected S1.42AD's Functional Microwave provider assumption.

The corrected S1.42AE contract is:

- CodeRebirth `1.6.9`;
- DawnLib/Dusk `0.9.25`;
- exact `code_rebirth:functional_microwave` provider;
- `PrioritiseMoons = true`;
- exactly 18 Moon/tag curves;
- exactly 18 Interior/tag curves;
- validate/log both exact tables;
- scale only the 18 Moon/tag curves by `SpawnScale = 0.5`;
- Interior curves are validation-only and are not mutated;
- fail closed on provider-contract drift.

### Two invalid launch attempts were classified correctly

Two S1.42AE launches failed in the BepInEx preloader before S1.42AE's own provider-contract code could execute. Neither is an S1.42AE runtime rejection.

The second capture exposed Gale's actual nested package path:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

This established that the prior v2.2 materialization sentinel modeled the dependency path too flatly and did not fully close the transitive base-SoundAPI requirement.

### Gale import recovery v2.3 was implemented and merged

PR #13, `Harden Gale materialization proof to v2.3`, was validated and merged.

The canonical launcher is now:

`RuntimeTools/ReplaceActiveGaleProfileV23.ps1`

Revision:

`2026-09-05-import-uia-v2.3-recursive-package-materialization-proof`

It preserves the validated v2.2 Gale/UI-import workflow but requires, before reporting import success:

- exactly one non-empty `me.loaforc.soundapi.dll` recursively inside the Gale package root `BepInEx\plugins\loaforc-loaforcsSoundAPI\`;
- exactly one non-empty `me.loaforc.soundapi.lethalcompany.dll` recursively inside `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`;
- the base SoundAPI requirement whenever the LethalCompany binding is required, even if Gale export metadata does not separately list the base package;
- fail closed on missing package roots, zero matches, empty DLLs, duplicate matches, or unexpected drift in the underlying validated v2.2 importer source.

No gameplay/profile/build bytes were changed by this import-recovery work.

## 3. What remains outstanding

The repository-side v2.3 recovery implementation is complete. What remains is the user-facing runtime acceptance gate for the **same S1.42AE artifact**.

Do not create a new build first.

Required sequence:

1. re-import the same S1.42AE profile using the canonical v2.3 Gale launcher;
2. require a positive v2.3 import-verification result before starting Lethal Company;
3. start the game and reach main menu/lobby cleanly;
4. play one normal run far enough for ordinary moon/interior generation and normal gameplay;
5. upload the complete fresh S1.42AE `LogOutput.log` with the exact uploader from the candidate record;
6. evaluate the log for the deterministic S1.42AE provider markers and regressions;
7. explicitly accept or reject S1.42AE from valid runtime evidence;
8. only after that decision may successor work be considered.

## 4. Exact continuation segment from the youngest technical task

The youngest technical task was split into three segments after the second S1.42AE preloader failure:

- **Technical Segment 1/3:** diagnose why v2.2 failed — completed.
- **Technical Segment 2/3:** implement/merge v2.3 and record the second invalid attempt — completed.
- **Technical Segment 3/3:** post-merge verification and handoff to the user's renewed S1.42AE test — this is the continuation point.

The technical post-merge verification for commit `c2aa8b2dd5d91d74601c09172e43bd4da7216b3b` was subsequently confirmed during handover inspection: `Knowledge Architecture` push run `33976199579` was successful and no PR was open at that inspection point.

Because this handover itself will create a newer final `main` commit, the handover's final validation segment must verify the final merged `main` again. After that, the new chat should continue the youngest technical task at **Technical Segment 3/3's user-facing test-release step**. Do not repeat Technical Segment 2/3 and do not build a successor.

## 5. What exactly must still be done for S1.42AE

### Gale v2.3 re-import

Use the canonical repository-driven launcher:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV23.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Do not start the game unless the helper positively verifies the exact imported `export.r2x` plus both recursive SoundAPI package-root materialization contracts.

If the helper reports missing/empty/duplicate dependency materialization, preserve its console output and investigate that import failure. Such a failure is not automatically an S1.42AE gameplay/runtime rejection.

### Runtime test

After positive v2.3 verification:

- start Lethal Company with `LC V1 S1.42AE Functional Microwave Provider Contract Correction`;
- reach main menu/lobby;
- play one normal run far enough for ordinary moon/interior generation;
- ordinary gameplay must remain healthy.

Required deterministic log evidence includes:

- `S1.42AE CodeRebirth Microwave Spawn Tuning 1.0.0` loads;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validations succeed;
- armed marker for the Moon-registry-freeze lifecycle;
- provider marker `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`;
- both exact Moon and Interior keyset markers;
- final marker showing 18 Moon/tag curves scaled by `0.5` and 18 Interior curves validation-only/not mutated;
- no S1.42AE refusal/error marker;
- no new fatal/project-critical regression.

A single normal run is sufficient for this technical gate. Do not require a statistically meaningful observed Microwave count; deterministic provider mutation is the primary evidence for the half-frequency target.

### Exact runtime-log uploader

After the test, use the exact build-specific uploader:

```powershell
$src=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AE Functional Microwave Provider Contract Correction\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AE runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}
```

## Authorities for the new chat

Start with the repository bootstrap and route through the current authorities. For this exact continuation, the most relevant files are:

- `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`;
- `START_HERE_ChatGPT_Masterprompt.txt`;
- `Current/CURRENT_STATE.json`;
- `Knowledge/CURRENT_LIFECYCLE.md`;
- this checkpoint: `Current/124_HANDOVER_S1.42AE_V23_SEGMENT3_NEXT.md`;
- `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`;
- `Current/Projektstatus_S1.42AE_CANDIDATE.json`;
- `Knowledge/GALE_PROFILE_WORKFLOW.md`;
- `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`;
- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`.

Normal follow-up questions should be routed through `Current/PROJECT_KNOWLEDGE_MAP.md/.json` rather than triggering a full repository audit by default.
