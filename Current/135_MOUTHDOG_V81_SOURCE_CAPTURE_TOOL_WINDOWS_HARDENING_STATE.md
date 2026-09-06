# S1.42AG Follow-Up — MouthDog V81 Source Capture Tool Windows Hardening State

**Status:** CURRENT / HANDOVER-CRITICAL WORK STATE  
**Authority:** current source-capture-tool execution state before authoritative Vanilla V81 MouthDogAI evidence exists  
**Related lifecycle:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`  
**Tool:** `AnalysisTools/InspectMouthDogV81.ps1`  
**Patch safety:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-06

## Purpose

This record prevents a successor ChatGPT chat from re-investigating source-capture bootstrap failures that were already reproduced on the user's actual Windows machine and fixed repository-native.

It does **not** claim that Vanilla V81 MouthDogAI source evidence has already been captured. No authoritative `SourceEvidence/VanillaV81/MouthDogAI/` report or manifest exists yet.

## What is already proven working

Across the user's real Windows runs, the tool has already proved that:

- Steam/Lethal Company auto-detection locates the installed `Lethal Company_Data/Managed/Assembly-CSharp.dll` without `-AssemblyPath`;
- the local assembly can be SHA-256 hashed successfully;
- the temporary .NET 10 bootstrap can complete;
- `ilspycmd 11.0.0.9375` can be installed into the temporary tool directory.

Therefore the next chat must not treat Steam discovery, the assembly path, NuGet availability, .NET installation, or ILSpy package installation as unresolved design questions unless the latest hardened tool actually reproduces one of those failures again.

## Three observed Windows bootstrap failures and their repository fixes

### 1. Local NuGet sources disabled / absent

Observed failure:

`No NuGet sources are defined or enabled`

The assembly had already been found and hashed. The failure occurred only when the tool attempted the isolated `ilspycmd` installation.

Repository fix merged on commit:

`85ab213ca52f50ff629110429ee26b547fff108f`

The tool now writes a temporary `nuget.config` containing only explicit `https://api.nuget.org/v3/index.json` and passes it through `dotnet tool install --configfile`. The user's global NuGet configuration is not modified.

### 2. `dotnet-install.ps1` output contaminated the helper return value

After the NuGet-source fix, the user's next run successfully bootstrapped .NET 10 and installed `ilspycmd`, but PowerShell output emitted by `dotnet-install.ps1` leaked into `Ensure-DotNetAndIlSpy`'s output stream. The caller therefore received install-log text plus the intended path instead of exactly one tool path.

Repository fix merged on commit:

`cbc66e95ff4311f41fb3943230cc1de801742880`

The bootstrap output is now captured, printed with `Write-Host`, and kept out of the function return stream. The caller also fails closed unless the helper returns exactly one launcher path.

### 3. Generated `ilspycmd.exe` shim could not resolve the temporary .NET runtime

After the output-isolation fix, the user's next run again bootstrapped .NET 10 and installed `ilspycmd 11.0.0.9375`, but direct execution of the generated shim failed with:

`You must install or update .NET to run this application.`

This was not a missing-package failure. The generated shim could not discover the SDK/runtime that existed only in the tool's temporary directory.

Repository fix merged on commit:

`6781b8c881759417fac9987629826fa5de1542cf`

The current tool now finds exactly one installed `ilspycmd.dll`, fails closed if that contract is not exact, and generates a temporary launcher that executes that DLL through the exact `dotnet.exe` selected or bootstrapped by the helper. It no longer depends on global .NET runtime resolution.

## Current execution status

**Current hardened tool revision:** repository `main` at or after `6781b8c881759417fac9987629826fa5de1542cf`.

**Evidence capture status:** `CAPTURE_TOOL_HARDENED_AFTER_THREE_WINDOWS_BOOTSTRAP_FAILURES_AWAITING_RETRY`.

**Authoritative source evidence status:** `NOT YET CAPTURED`.

The current hardened revision has **not yet been re-run by the user after the third fix**. Therefore there is still no successful `source-evidence/mouthdog-v81-*` branch and no authoritative:

- `MOUTHDOGAI_FOCUSED_DECOMPILE.txt`;
- `MANIFEST.json`.

## Exact next user action

Run the current tool from repository `main` with auto-detection:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/AnalysisTools/InspectMouthDogV81.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Do **not** add `-AssemblyPath` unless auto-detection actually fails in the new run.

If the run succeeds, capture the printed:

- `Evidence branch`;
- `Evidence commit`;
- `Assembly SHA-256`;
- `Steam buildid`.

Then inspect that exact temporary branch and verify:

- `SourceEvidence/VanillaV81/MouthDogAI/<timestamp>/MANIFEST.json`;
- `SourceEvidence/VanillaV81/MouthDogAI/<timestamp>/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`.

Only after provenance verification may the native `MouthDogAI` perception/noise/target/lunge/collision path be analyzed to prove or reject the carried-scrap/noise hypothesis and identify the exact remaining Mouth Dog -> Pikmin owner/method boundary.

## What is currently irrelevant / must not be repeated pre-emptively

Unless the hardened tool produces a new concrete failure, do not ask the user to:

- configure or enable global NuGet sources;
- install .NET manually;
- install ILSpy manually;
- supply `-AssemblyPath` manually;
- clone the repository locally;
- manually decompile or upload `Assembly-CSharp.dll`;
- re-run S1.42AG gameplay;
- upload another S1.42AG runtime log;
- build or arm a successor.

The prior three Windows bootstrap errors are **resolved implementation history**, not current blockers.

## Gameplay/lifecycle boundary remains unchanged

S1.42AF remains the accepted full-normal-stack baseline. S1.42AG remains runtime-rejected as a partial fix. No active candidate exists, no runtime test is outstanding, and no successor is armed.

The S1.42AG `Priority.First` guard on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` remains a proven useful prevention-before-mutation result, but it does not prove the remaining native target/attack owner.

Pikmin -> Mouth Dog combat is not a current failure signal: that direction was not deliberately exercised in S1.42AG. Passive follower Pikmin remaining non-aggressive is expected behavior.

Do not build a successor until the successful Vanilla V81 focused evidence capture proves the remaining Mouth Dog -> Pikmin boundary under the patch-safety policy.
