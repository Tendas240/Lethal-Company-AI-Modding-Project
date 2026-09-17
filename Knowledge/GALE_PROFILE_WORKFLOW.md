# Gale Profile Replacement and Import

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic router to the fully user-validated Gale workflow  
**Canonical-For:** `gale_import`  
**Evidence:** `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
**Implementation:** `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` (canonical launcher), `RuntimeTools/ReplaceActiveGaleProfile.ps1` (validated v2.2 importer base)  
**Related:** `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`, `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`, `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`, `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`  
**Last-Validated:** 2026-09-04  
**Last-Hardened:** 2026-09-17 (`2026-09-17-import-uia-v2.4.1-diagnostic-build-result-url-delimiting`; diagnostic target resolver statically/regression validated after the first real DIAG1 import exposed a pre-import PowerShell URL-interpolation defect; local UI import behavior remains inherited from the previously user-validated path)

## Canonical launcher

For the currently ready-to-test build, use the repository-driven v2.4 launcher rather than a build-name-specific script:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Before presenting it, `RuntimeInbox/ACTIVE_BUILD.txt` must resolve fail-closed through one of exactly two repository-authorized paths:

1. **normal built-artifact path:** `ACTIVE_BUILD == Current/AUTO_BUILD_RESULT.json.build_id`; or
2. **explicit diagnostic runtime-target path:** `Current/CURRENT_STATE.json.controllers.runtime_active_build == ACTIVE_BUILD`, `selected_scope.diagnostic_revision.build_id == ACTIVE_BUILD`, the diagnostic status is exactly `PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED`, its `base_build_id` / base profile / base SHA bind back to the current `AUTO_BUILD_RESULT`, and its referenced `build_result` independently agrees on build ID, output profile/SHA, base profile/SHA and exact profile name.

No other `ACTIVE_BUILD` / `AUTO_BUILD_RESULT` mismatch is permitted. The diagnostic exception changes only repository target resolution; it does not promote the diagnostic artifact, replace the balanced candidate or weaken download/import integrity checks.

The v2.4 launcher deliberately wraps the already user-validated v2.2 importer instead of duplicating its UI Automation implementation. It first requires the exact expected v2.2 source-revision signature, replaces only the export-text reader, critical-materialization functions and repository target-resolution block in memory, stamps the current v2.4.x revision, and then executes the resulting helper. If the underlying v2.2 source drifts, v2.4 refuses to run until that drift is reviewed.

## Validated import path

The underlying helper was fully user-validated during S1.42AA -> S1.42AB on Windows PowerShell 5.1. The current launcher preserves that behavior:

- closes Gale;
- resolves the exact repository target through the normal build path or the explicit fail-closed diagnostic path above;
- downloads and SHA-256-verifies the `.r2z` before deletion is offered;
- asks the user to select the old local profile numerically and confirm deletion with `y`;
- opens the verified candidate exactly once;
- resolves the simple one-profile Gale `Missing Profiles` gate via semantic UI Automation;
- expands `Advanced options`;
- enables and verifies `Import all files`;
- invokes Import;
- waits for the exact target profile's local `export.r2x`;
- requires that local `export.r2x` hash to match the archive-entry hash;
- additionally requires project-critical external Thunderstore dependency DLLs to be physically materialized according to the v2.4 package-root contract;
- removes the temporary `.r2z` only after both export identity and required materialization proof succeed.

After profile number + `y`, no additional Gale click or PowerShell Enter is required on the previously validated happy path. The diagnostic resolver is repository-side selection logic. The first real S1.42AJ-DIAG1 import attempt did not reach profile download/import because it exposed the v2.4 dynamic build-result URL defect documented below; the corrected v2.4.1 diagnostic resolver still requires user runtime validation and is not retroactively labeled proven.

## Why v2.2 was insufficient

S1.42AE exposed two consecutive preloader-only launch failures before its own candidate code could execute. The second console capture made the actual Gale package layout explicit. BepInEx/AutoHookGenPatcher attempted to read the binding DLL below:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

The v2.2 sentinel modeled the package as a flat path directly below `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`. That path model was incomplete: Gale keeps a namespace/package outer directory and the Thunderstore package preserves its own `BepInEx/plugins/...` subtree beneath it.

There was also a dependency-closure gap. `loaforc-loaforcsSoundAPI_LethalCompany` depends on the base `loaforc-loaforcsSoundAPI` package, but the Gale export can list only the requested top-level binding package. Therefore the base SoundAPI DLL must be treated as a mandatory transitive materialization requirement whenever the LethalCompany binding is present.

## Why v2.3 was insufficient

The third S1.42AE launch attempt demonstrated a separate proof bug in the v2.3 wrapper. On the user's Windows PowerShell 5.1 environment, the inherited `Get-ZipEntryText` implementation emitted a non-terminating `New-Object` overload error for the five-argument `System.IO.StreamReader` construction. `ExpectedExportText` consequently became empty; `Get-RequiredCriticalMaterializationPaths` then emitted a parameter-binding error, but the importer continued and later printed a false-positive successful materialization result with no effective critical dependency contracts.

The game then failed in the same BepInEx preloader path because `me.loaforc.soundapi.lethalcompany.dll` was still absent from the runtime-consumed package path. This remains **invalid import/materialization evidence, not an S1.42AE runtime rejection**.

A controlled fresh import of accepted S1.42AC proved the contrast: both SoundAPI DLLs physically materialized at the expected nested package paths, and S1.42AC then passed the BepInEx preloader and reached the main menu normally. This demonstrates that the current game/mod stack can start when Gale materializes the dependency correctly.

## v2.4 export-read, diagnostic target and critical materialization proof

v2.4 preserves the v2.3 package-root semantics, closes the false-positive path before dependency derivation and supports an explicitly bound diagnostic runtime target without weakening the normal build guard:

- `Get-ZipEntryText` is replaced in-memory and uses the direct four-argument `System.IO.StreamReader` constructor rather than the failing `New-Object ... -ArgumentList` path;
- constructor/read failures terminate through `throw`;
- empty or whitespace `export.r2x` text terminates before dependency-contract derivation;
- `ExpectedExportText` is `[ValidateNotNullOrEmpty()]`;
- a mentioned SoundAPI package that cannot be recognized as the canonical `- name:` export entry fails closed rather than being treated as absent;
- an LC binding must resolve to exactly two materialization contracts: base SoundAPI plus LC binding;
- package-root searches still require exactly one non-empty expected DLL; zero, empty, or duplicate matches fail closed;
- normal targets still require exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- a mismatch is accepted only through the exact `CURRENT_STATE.controllers.runtime_active_build` + `selected_scope.diagnostic_revision` binding and its referenced build-result crosschecks;
- the diagnostic base identity must match the current `AUTO_BUILD_RESULT`, preventing an unrelated or stale diagnostic from being imported;
- the wrapper refuses if the validated v2.2 helper source revision drifts or if the legacy defective StreamReader constructor or unconditional mismatch-abort path survives the in-memory patch.

## v2.4.1 diagnostic build-result URL repair

The first real S1.42AJ-DIAG1 launcher execution reached the explicit diagnostic resolver and then failed before any candidate profile was downloaded. Windows PowerShell 5.1 parsed the expandable-string fragment `$encodedBuildResultPath?cb=...` as a variable name containing `?`, which PowerShell permits in ordinary variable names. The intended repository path therefore disappeared from the Raw GitHub URL and the request returned HTTP 404. Because the request was not forced terminating, execution then continued far enough to emit the misleading secondary message that the diagnostic build result belonged to an empty build ID.

Revision `2026-09-17-import-uia-v2.4.1-diagnostic-build-result-url-delimiting` repairs that exact path without weakening the authority chain:

- repository-path segments are encoded individually with `[Uri]::EscapeDataString()` while `/` separators are preserved;
- the interpolated path is explicitly delimited as `${encodedBuildResultPath}` before the `?cb` query delimiter;
- the diagnostic build-result request uses `-ErrorAction Stop` and converts any HTTP/load failure into one explicit fail-closed error naming the referenced repository path;
- empty, `.` or `..` path segments are rejected before URL construction;
- all existing build ID, profile, SHA and base-artifact crosschecks remain unchanged.

The permanent repository regression gate now rejects the original `$encodedBuildResultPath?cb=` interpolation shape and requires the delimited `${encodedBuildResultPath}?cb=` form plus terminating fetch semantics.

The permanent repository regression gate is `RepositoryTools/gale_import_helper_validator.py`, run by `.github/workflows/knowledge-architecture.yml`.

## Critical package-root contract

When `loaforc-loaforcsSoundAPI_LethalCompany` is present in the expected export, both of these contracts are mandatory:

- below `BepInEx\plugins\loaforc-loaforcsSoundAPI\`, recursively find **exactly one** `me.loaforc.soundapi.dll` and require it to be non-empty;
- below `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`, recursively find **exactly one** `me.loaforc.soundapi.lethalcompany.dll` and require it to be non-empty.

If the base `loaforc-loaforcsSoundAPI` package is explicitly present without the binding, the base-DLL contract still applies.

The recursive search is deliberately constrained to each package's own Gale package root. It therefore tolerates the package's inner directory layout while remaining fail-closed against absence, empty files, or ambiguous duplicate DLLs.

## Fail-closed requirements

Keep the exact workflow safety constraints from `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md` for the fully validated normal path, plus the explicit diagnostic resolver contract above, including:

- exact build/profile matching only;
- normal build resolution remains exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id`;
- diagnostic mismatches require exact controller + diagnostic revision + diagnostic status + base-build + build-result agreement; no generic fallback exists;
- the dynamic diagnostic build-result path must be segment-escaped, explicitly delimited before `?cb`, and its HTTP fetch must terminate on failure;
- explicit confirmation before deleting a local profile;
- no direct editing of Gale `data.sqlite3`;
- no coordinate clicks or blind key navigation;
- never auto-resolve multiple missing profiles;
- no cache-busting query string on the binary `.r2z` Raw GitHub URL;
- exact post-import `export.r2x` evidence remains mandatory;
- export text must be non-empty and successfully decoded before dependency contracts are derived;
- required project-critical dependency package roots must each contain exactly one expected non-empty DLL;
- the LethalCompany binding implies the base SoundAPI dependency even if the base package is not separately listed in export metadata;
- on materialization timeout/failure, report the unresolved contract and preserve the downloaded `.r2z` for diagnosis;
- if the validated importer source revision changes unexpectedly, the v2.4 wrapper must refuse rather than patch unknown code.

## Runtime-test pairing

The Gale replacement command never substitutes for the runtime-log uploader. Whenever a build is ready to test, both one-line PowerShell commands must be supplied together. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.
