# Gale Import Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** V1 PARTIAL PASS / DUPLICATE EVENT ROOT CAUSE CONFIRMED / V2 IMPLEMENTED / USER VALIDATION PENDING

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

Therefore the UIA targeting for `Advanced options -> Import all files -> Import` itself is strongly evidenced as working.

## V1 runtime defect discovered

The same run exposed a sequencing bug in the helper.

After the original `.r2z` invocation started Gale, the helper resolved the blocking Missing Profiles dialog and then unconditionally called `Start-Process $dst` a **second time**. That produced a second `.r2z` file-open event through Gale's single-instance/deep-link path.

Observed result:

- PowerShell reported that `Import all files` was activated and Import was invoked;
- Gale already showed `LC V1 S1.42AB Interior Weight Normalization` as the active profile, proving the first import completed;
- a second empty `Import profile` dialog remained visible with only `Enter import code...` and the generic Import button;
- PowerShell waited for the success-toast UIA marker instead of recognizing the already imported profile.

The empty dialog is explained by the race between the two import events: while the first `importData()` awaited the actual import, the second event could set dialog state/open again; after the first await completed, its cleanup set `data = null` without necessarily undoing the second event's `open = true`, leaving the code-entry form visible.

This is a helper sequencing defect, not an S1.42AB profile/import failure.

## V2 implementation

Canonical helper remains:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Current helper marker:

`2026-09-04-import-uia-v2-single-open-evidence`

Current helper blob:

`aa2b5ac7084fb08f75382405658b4ffa49452587`

Implementation/final syntax-fix commit:

`2c25fccabdf177a6cc114a3eaba752014cf5cb45`

### V2 changes

1. The verified `.r2z` is opened **exactly once**.
2. After Missing Profiles is resolved, the helper does **not** re-send the file to Gale.
3. It waits up to 60 seconds for the full import dialog already produced by the original buffered file-open event.
4. The validated semantic UIA import sequence remains fail-closed.
5. The helper no longer depends on Gale's transient success toast.
6. Before opening Gale, it hashes the `export.r2x` entry inside the SHA-verified `.r2z`.
7. After Import is invoked, it waits for the exact target directory and requires its local `export.r2x` SHA-256 to equal the archive entry hash.
8. Only after that evidence passes is the temporary downloaded `.r2z` removed.
9. If import UIA falls back to manual interaction, PowerShell waits automatically for the same filesystem/hash evidence; no extra Enter is required after the manual import.
10. If Missing Profiles UIA falls back, PowerShell automatically waits for that dialog to close instead of requiring a separate Enter confirmation.
11. Raw GitHub build-state/profile downloads use cache-busting query values plus `Cache-Control: no-cache`.

## Fail-closed rules

Automatic UI interaction is refused if any relevant target is ambiguous. The helper never uses:

- screen-coordinate mouse clicks;
- blind `Tab` / `Enter` / arrow-key sequences;
- fuzzy profile/build matching;
- direct Gale SQLite mutation.

The exact new target profile must not already exist separately before replacement.

## Current validation target

V2 still requires one controlled user validation from the normal starting state.

Acceptance requires:

1. one old profile is selected and deletion confirmed with `y`;
2. Missing Profiles resolves automatically;
3. exactly one full target-profile import dialog is consumed;
4. `Import all files` is enabled automatically;
5. Import is invoked automatically;
6. no second empty import-code dialog appears;
7. the exact target profile becomes available in Gale;
8. PowerShell confirms the imported `export.r2x` hash automatically;
9. the temporary `.r2z` is removed automatically;
10. no manual Gale click or final Enter is required after profile selection / `y`.

Until this exact V2 flow is user-confirmed, describe V2 as implemented and validation pending. The Missing Profiles automation remains user-validated, and V1 already demonstrated that the actual Import-all-files/UIA controls can be operated successfully.