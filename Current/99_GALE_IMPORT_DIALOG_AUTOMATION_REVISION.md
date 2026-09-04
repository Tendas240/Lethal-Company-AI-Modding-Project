# Gale Import Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** V1 IMPORT UIA PASS / V1 DUPLICATE-EVENT DEFECT CONFIRMED / V2 DOWNLOAD 404 FAIL-CLOSED / V2.1 IMPLEMENTED / USER VALIDATION PENDING

## Context

The preceding helper revision successfully automated Gale's blocking `Missing Profiles -> Delete -> Submit` recovery flow. The user confirmed that this part works on the actual project Gale/WebView environment.

The remaining desired automation is:

`Advanced options -> Import all files -> Import`

## Upstream Gale evidence

Current Gale source confirms:

- `.r2z` file opens are handled by `deep_link::handle()` and `import_profile_file()`;
- the single-instance handler forwards a second file-open invocation into the already running Gale process;
- `import_profile_file()` asynchronously reads the archive and emits a buffered `import_profile` event;
- `ImportProfileDialog.svelte` receives that event and opens the full import dialog;
- `Advanced options` contains the real Bits UI `Import all files` checkbox;
- the final Import control is a real HTML button;
- `importData()` closes the dialog before awaiting the profile import, then clears its `data` after the await;
- with `ImportOptions.import_all = true`, Gale's `import_config()` includes all source files, including `export.r2x`, in the destination profile.

This last point gives the project a durable post-import verification primitive: hash the `export.r2x` entry inside the already SHA-verified `.r2z`, then require the imported target profile's local `export.r2x` to have that exact hash.

## V1 implementation

Helper marker:

`2026-09-04-import-uia-v1`

Blob:

`689c9dcd7cbc38fcf9735309336106322a6203d8`

Implementation commit:

`cace6989f12ed9c47d72e806851d17cdd706948b`

V1 correctly performed the semantic UI Automation sequence on the user's machine:

1. Missing Profiles was resolved automatically;
2. the full S1.42AB import dialog was found;
3. `Import all files` was toggled on;
4. Import was invoked automatically;
5. Gale created/activated `LC V1 S1.42AB Interior Weight Normalization`.

Therefore the UIA targeting for `Advanced options -> Import all files -> Import` itself is **user-evidenced as working**.

## V1 runtime defect discovered

After the original `.r2z` invocation started Gale, the helper resolved the blocking Missing Profiles dialog and then unconditionally called `Start-Process $dst` a **second time**. That produced a second `.r2z` file-open event through Gale's single-instance/deep-link path.

Observed result:

- PowerShell reported that `Import all files` was activated and Import was invoked;
- Gale already showed `LC V1 S1.42AB Interior Weight Normalization` as the active profile, proving the first import completed;
- a second empty `Import profile` dialog remained visible with only `Enter import code...` and the generic Import button;
- PowerShell waited for the success-toast UIA marker instead of recognizing the already imported profile.

The empty dialog is explained by the race between the two import events. This is a helper sequencing defect, not an S1.42AB profile/import failure.

## V2 implementation

Helper marker:

`2026-09-04-import-uia-v2-single-open-evidence`

Blob:

`aa2b5ac7084fb08f75382405658b4ffa49452587`

Implementation/final syntax-fix commit:

`2c25fccabdf177a6cc114a3eaba752014cf5cb45`

V2 changes:

1. The verified `.r2z` is opened exactly once.
2. After Missing Profiles is resolved, the helper does not re-send the file to Gale.
3. It waits for the full import dialog already produced by the original buffered file-open event.
4. The validated semantic UIA import sequence remains fail-closed.
5. The helper no longer depends on Gale's transient success toast.
6. Before opening Gale, it hashes the `export.r2x` entry inside the SHA-verified `.r2z`.
7. After Import is invoked, it waits for the exact target directory and requires its local `export.r2x` SHA-256 to equal the archive entry hash.
8. Only after that evidence passes is the temporary downloaded `.r2z` removed.
9. If import UIA falls back to manual interaction, PowerShell waits automatically for the same filesystem/hash evidence; no extra Enter is required after the manual import.
10. If Missing Profiles UIA falls back, PowerShell automatically waits for that dialog to close instead of requiring a separate Enter confirmation.

## V2 validation attempt — download 404

The first controlled V2 user test failed **before any destructive local action**.

Observed PowerShell failure:

`Invoke-WebRequest : 404: Not Found`

followed by the guard:

`Download fehlgeschlagen oder Datei ist leer`

At this point the helper had only resolved the active build/controller metadata and attempted to download the S1.42AB `.r2z`; it had not yet listed/selected/deleted the old profile. Therefore the reproduced S1.42AA starting state remained intact.

Root cause: V2 added a cache-busting query string to the binary Raw GitHub profile download:

`.../<profile>.r2z?cb=<ticks>`

That cache-buster was unnecessary because candidate profile filenames are build-specific and the downloaded binary is immediately SHA-256 verified. The previously validated helper versions used the plain Raw URL successfully.

## V2.1 download hotfix

Canonical helper remains:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Current helper marker:

`2026-09-04-import-uia-v2.1-download-hotfix`

Current helper blob:

`9458f427b538615249714e7f064f3107d6dcd36c`

Hotfix commit:

`f711f53f4971f97200ed3605479ef887a14b243d`

V2.1 changes only the download plumbing relevant to the observed failure:

- mutable controller reads (`RuntimeInbox/ACTIVE_BUILD.txt`, `Current/AUTO_BUILD_RESULT.json`) may retain cache-busting/no-cache behavior;
- the binary candidate `.r2z` download again uses the proven plain Raw GitHub URL with no query string;
- the profile remains protected by the exact expected SHA-256 before any destructive local action;
- all V2 single-open, UIA import and `export.r2x` post-import verification behavior is preserved.

## Fail-closed rules

Automatic UI interaction is refused if any relevant target is ambiguous. The helper never uses:

- screen-coordinate mouse clicks;
- blind `Tab` / `Enter` / arrow-key sequences;
- fuzzy profile/build matching;
- direct Gale SQLite mutation.

The exact new target profile must not already exist separately before replacement.

## Current validation target

V2.1 requires one controlled user validation from the normal starting state.

Acceptance requires:

1. candidate `.r2z` downloads and exact SHA-256 verification passes;
2. one old profile is selected and deletion confirmed with `y`;
3. Missing Profiles resolves automatically;
4. exactly one full target-profile import dialog is consumed;
5. `Import all files` is enabled automatically;
6. Import is invoked automatically;
7. no second empty import-code dialog appears;
8. the exact target profile becomes available in Gale;
9. PowerShell confirms the imported `export.r2x` hash automatically;
10. the temporary `.r2z` is removed automatically;
11. no manual Gale click or final Enter is required after profile selection / `y`.

Until this exact V2.1 flow is user-confirmed, describe it as implemented and validation pending. The Missing Profiles automation remains user-validated, and V1 already demonstrated that the actual Import-all-files/UIA controls can be operated successfully.