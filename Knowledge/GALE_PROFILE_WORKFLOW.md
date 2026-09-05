# Gale Profile Replacement and Import

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic router to the fully user-validated Gale workflow  
**Canonical-For:** `gale_import`  
**Evidence:** `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
**Implementation:** `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` (canonical launcher), `RuntimeTools/ReplaceActiveGaleProfile.ps1` (validated v2.2 importer base)  
**Related:** `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`, `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`, `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`, `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`  
**Last-Validated:** 2026-09-04  
**Last-Hardened:** 2026-09-05 (`2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`; pending next user re-import)

## Canonical launcher

For the currently ready-to-test build, use the repository-driven v2.4 launcher rather than a build-name-specific script:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Before presenting it, the repository must have `RuntimeInbox/ACTIVE_BUILD.txt` and `Current/AUTO_BUILD_RESULT.json.build_id` pointing to the exact same ready candidate.

The v2.4 launcher deliberately wraps the already user-validated v2.2 importer instead of duplicating its UI Automation implementation. It first requires the exact expected v2.2 source-revision signature, replaces only the export-text reader and critical-materialization functions in memory, stamps the v2.4 revision, and then executes the resulting helper. If the underlying v2.2 source drifts, v2.4 refuses to run until that drift is reviewed.

## Validated import path

The underlying helper was fully user-validated during S1.42AA -> S1.42AB on Windows PowerShell 5.1. The current launcher preserves that behavior:

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
- additionally requires project-critical external Thunderstore dependency DLLs to be physically materialized according to the v2.4 package-root contract;
- removes the temporary `.r2z` only after both export identity and required materialization proof succeed.

After profile number + `y`, no additional Gale click or PowerShell Enter is required on the validated happy path.

## Why v2.2 was insufficient

S1.42AE exposed two consecutive preloader-only launch failures before its own candidate code could execute. The second console capture made the actual Gale package layout explicit. BepInEx/AutoHookGenPatcher attempted to read the binding DLL below:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

The v2.2 sentinel modeled the package as a flat path directly below `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`. That path model was incomplete: Gale keeps a namespace/package outer directory and the Thunderstore package preserves its own `BepInEx/plugins/...` subtree beneath it.

There was also a dependency-closure gap. `loaforc-loaforcsSoundAPI_LethalCompany` depends on the base `loaforc-loaforcsSoundAPI` package, but the Gale export can list only the requested top-level binding package. Therefore the base SoundAPI DLL must be treated as a mandatory transitive materialization requirement whenever the LethalCompany binding is present.

## Why v2.3 was insufficient

The third S1.42AE launch attempt demonstrated a separate proof bug in the v2.3 wrapper. On the user's Windows PowerShell 5.1 environment, the inherited `Get-ZipEntryText` implementation emitted a non-terminating `New-Object` overload error for the five-argument `System.IO.StreamReader` construction. `ExpectedExportText` consequently became empty; `Get-RequiredCriticalMaterializationPaths` then emitted a parameter-binding error, but the importer continued and later printed a false-positive successful materialization result with no effective critical dependency contracts.

The game then failed in the same BepInEx preloader path because `me.loaforc.soundapi.lethalcompany.dll` was still absent from the runtime-consumed package path. This remains **invalid import/materialization evidence, not an S1.42AE runtime rejection**.

A controlled fresh import of accepted S1.42AC proved the contrast: both SoundAPI DLLs physically materialized at the expected nested package paths, and S1.42AC then passed the BepInEx preloader and reached the main menu normally. This demonstrates that the current game/mod stack can start when Gale materializes the dependency correctly.

## v2.4 export-read and critical materialization proof

v2.4 preserves the v2.3 package-root semantics but closes the false-positive path before dependency derivation:

- `Get-ZipEntryText` is replaced in-memory and uses the direct four-argument `System.IO.StreamReader` constructor rather than the failing `New-Object ... -ArgumentList` path;
- constructor/read failures terminate through `throw`;
- empty or whitespace `export.r2x` text terminates before dependency-contract derivation;
- `ExpectedExportText` is `[ValidateNotNullOrEmpty()]`;
- a mentioned SoundAPI package that cannot be recognized as the canonical `- name:` export entry fails closed rather than being treated as absent;
- an LC binding must resolve to exactly two materialization contracts: base SoundAPI plus LC binding;
- package-root searches still require exactly one non-empty expected DLL; zero, empty, or duplicate matches fail closed;
- the wrapper refuses if the validated v2.2 helper source revision drifts or if the legacy defective StreamReader constructor survives the in-memory patch.

The permanent repository regression gate is `RepositoryTools/gale_import_helper_validator.py`, run by `.github/workflows/knowledge-architecture.yml`.

## Critical package-root contract

When `loaforc-loaforcsSoundAPI_LethalCompany` is present in the expected export, both of these contracts are mandatory:

- below `BepInEx\plugins\loaforc-loaforcsSoundAPI\`, recursively find **exactly one** `me.loaforc.soundapi.dll` and require it to be non-empty;
- below `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`, recursively find **exactly one** `me.loaforc.soundapi.lethalcompany.dll` and require it to be non-empty.

If the base `loaforc-loaforcsSoundAPI` package is explicitly present without the binding, the base-DLL contract still applies.

The recursive search is deliberately constrained to each package's own Gale package root. It therefore tolerates the package's inner directory layout while remaining fail-closed against absence, empty files, or ambiguous duplicate DLLs.

## Fail-closed requirements

Keep the exact workflow safety constraints from `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`, including:

- exact build/profile matching only;
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
