# Gale Profile Replacement and Import

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic router to the fully user-validated Gale workflow  
**Canonical-For:** `gale_import`  
**Evidence:** `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
**Implementation:** `RuntimeTools/ReplaceActiveGaleProfileV23.ps1` (canonical launcher), `RuntimeTools/ReplaceActiveGaleProfile.ps1` (validated v2.2 importer base)  
**Related:** `Current/98_GALE_MISSING_PROFILE_DIALOG_AUTOMATION_REVISION.md`, `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`, `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`  
**Last-Validated:** 2026-09-04  
**Last-Hardened:** 2026-09-05 (`2026-09-05-import-uia-v2.3-recursive-package-materialization-proof`; pending next user re-import)

## Canonical launcher

For the currently ready-to-test build, use the repository-driven v2.3 launcher rather than a build-name-specific script:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV23.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Before presenting it, the repository must have `RuntimeInbox/ACTIVE_BUILD.txt` and `Current/AUTO_BUILD_RESULT.json.build_id` pointing to the exact same ready candidate.

The v2.3 launcher deliberately wraps the already user-validated v2.2 importer instead of duplicating its UI Automation implementation. It first requires the exact expected v2.2 source-revision signature, replaces only the narrow critical-materialization functions in memory, stamps the v2.3 revision, and then executes the resulting helper. If the underlying v2.2 source drifts, v2.3 refuses to run until that drift is reviewed.

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
- additionally requires project-critical external Thunderstore dependency DLLs to be physically materialized according to the v2.3 package-root contract;
- removes the temporary `.r2z` only after both export identity and required materialization proof succeed.

After profile number + `y`, no additional Gale click or PowerShell Enter is required on the validated happy path.

## Why v2.2 was insufficient

S1.42AE exposed two consecutive preloader-only launch failures before its own candidate code could execute. The second console capture made the actual Gale package layout explicit. BepInEx/AutoHookGenPatcher attempted to read the binding DLL below:

`BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll`

The v2.2 sentinel modeled the package as a flat path directly below `BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\`. That path model was incomplete: Gale keeps a namespace/package outer directory and the Thunderstore package preserves its own `BepInEx/plugins/...` subtree beneath it.

There was also a dependency-closure gap. `loaforc-loaforcsSoundAPI_LethalCompany` depends on the base `loaforc-loaforcsSoundAPI` package, but the Gale export can list only the requested top-level binding package. Therefore the base SoundAPI DLL must be treated as a mandatory transitive materialization requirement whenever the LethalCompany binding is present.

## v2.3 critical materialization proof

An exact `export.r2x` proves imported profile metadata, but it does **not** prove that Gale finished materializing every external Thunderstore package file. v2.3 therefore checks package roots rather than a guessed flat DLL path.

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
- required project-critical dependency package roots must each contain exactly one expected non-empty DLL;
- the LethalCompany binding implies the base SoundAPI dependency even if the base package is not separately listed in export metadata;
- on materialization timeout/failure, report the unresolved contract and preserve the downloaded `.r2z` for diagnosis;
- if the validated importer source revision changes unexpectedly, the v2.3 wrapper must refuse rather than patch unknown code.

## Runtime-test pairing

The Gale replacement command never substitutes for the runtime-log uploader. Whenever a build is ready to test, both one-line PowerShell commands must be supplied together. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.
