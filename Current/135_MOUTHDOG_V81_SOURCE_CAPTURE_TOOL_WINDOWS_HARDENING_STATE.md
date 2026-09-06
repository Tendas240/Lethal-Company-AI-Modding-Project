# S1.42AG Follow-Up — MouthDog V81 Source Capture Tool Windows Hardening State

**Status:** HISTORICAL / RESOLVED CAPTURE-HARDENING STATE  
**Authority:** resolved implementation history for the Windows source-capture tool  
**Superseded by:** `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`  
**Tool:** `AnalysisTools/InspectMouthDogV81.ps1`  
**Last-Validated:** 2026-09-06

## Purpose

This record preserves the five real failures reproduced on the user's Windows machine while making it explicit that they are no longer the current execution state.

The capture that this file was waiting for has now completed successfully. Current provenance, native-path findings and the exact remaining pre-successor proof boundary are authoritative in `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`.

Do not interpret any old `AWAITING_RETRY` wording from historical revisions of this file as live state.

## Successful completion

The hardened tool was re-run successfully after the focused-window narrowing/merge fix.

Successful capture:

- evidence branch: `source-evidence/mouthdog-v81-20260906t121738z`;
- evidence commit: `a618b19bfc30234ca556c924d681d43b2c13d1d9`;
- capture base: `3049b0fa52af79db39efb075d94684d229eed3c6`;
- assembly SHA-256: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Steam buildid: `22825947`;
- authoritative evidence root: `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`.

The successful publication contains only `MANIFEST.json` and `MOUTHDOGAI_FOCUSED_DECOMPILE.txt`; it does not publish `Assembly-CSharp.dll` or a full game decompile.

## Three observed Windows bootstrap failures and repository fixes

### 1. Local NuGet sources disabled / absent

Observed error:

`No NuGet sources are defined or enabled`

Fix commit:

`85ab213ca52f50ff629110429ee26b547fff108f`

Resolution: use a temporary explicit `nuget.config` containing only `https://api.nuget.org/v3/index.json`, without modifying the user's global NuGet configuration.

### 2. `dotnet-install.ps1` output contaminated the helper return value

The temporary .NET installation and `ilspycmd` installation succeeded, but installer output leaked into `Ensure-DotNetAndIlSpy`'s return stream.

Fix commit:

`cbc66e95ff4311f41fb3943230cc1de801742880`

Resolution: isolate installer output, re-emit it only through `Write-Host`, and fail closed unless exactly one launcher path is returned.

### 3. Generated `ilspycmd.exe` shim could not resolve the temporary .NET runtime

Observed error:

`You must install or update .NET to run this application.`

Fix commit:

`6781b8c881759417fac9987629826fa5de1542cf`

Resolution: locate exactly one `ilspycmd.dll` and execute it through the exact selected/bootstrapped temporary `dotnet.exe`; do not depend on the generated EXE shim's global runtime resolution.

## Two observed focused-report post-processing failures and repository fixes

### 4. Legitimate blank source line rejected by `Find-MethodStart`

Observed error:

`Cannot bind argument to parameter 'Lines' because it is an empty string.`

Fix commit:

`0b3da73c5aad2efc26a0aba65863a552f2bc0af9`

Resolution: allow legitimate blank C# decompiler source lines through the exact helper parameter without widening decompile/publication scope.

### 5. Focused extraction exceeded the 500-line publication ceiling

Observed error:

`Focused extraction expanded to 657 source lines, above the 500-line safety ceiling. Refusing to publish an over-broad decompile.`

Fix commit:

`553577cc493f00d7908837f5b016f2bb30ed3fdd`

Resolution:

- remove the unnecessary unconditional 73-line minimum expansion;
- keep each method-grouped marker window from the nearest method declaration through 28 lines after the last relevant marker;
- merge overlapping/adjacent windows;
- apply the unchanged 500-line safety ceiling to unique selected source lines.

The 500-line publication safety limit was never raised or bypassed.

## What remains relevant from this history

The successful capture confirms that the following are solved unless a future tool revision newly reproduces them:

- Steam installation / `Assembly-CSharp.dll` auto-detection;
- assembly hashing;
- isolated NuGet source handling;
- temporary .NET bootstrap;
- isolated `ilspycmd` installation;
- execution of `ilspycmd.dll` through the exact temporary runtime;
- blank-line handling;
- focused-window deduplication under the 500-line safety ceiling.

Therefore do not ask the user to configure global NuGet, install .NET/ILSpy manually, pass `-AssemblyPath`, clone the repository, upload `Assembly-CSharp.dll`, or repeat the successful MouthDog source capture merely because those actions appeared in earlier troubleshooting history.

## Lifecycle boundary

S1.42AF remains the accepted full-normal-stack baseline. S1.42AG remains runtime-rejected as a partial fix. No active candidate exists, no runtime test is outstanding and no successor is armed.

The next action is no longer another source-capture retry. Follow `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md` for the current targeted source-evidence extension and patch-safety boundary.
