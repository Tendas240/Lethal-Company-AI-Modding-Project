# Gale Import Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** V2.1 FULL END-TO-END USER-VALIDATED / PROMOTED INTO CANONICAL HELPER

## Context

The project wanted to eliminate the remaining manual Gale import sequence:

`Advanced options -> Import all files -> Import`

The preceding helper revision had already made Gale's blocking `Missing Profiles -> Delete -> Submit` recovery flow automatic and user-validated.

## Upstream Gale evidence

Current Gale source confirms:

- `.r2z` file opens are handled by `deep_link::handle()` and `import_profile_file()`;
- the single-instance handler forwards additional file-open invocations into the already running Gale process;
- `import_profile_file()` asynchronously reads the archive and emits a buffered `import_profile` event;
- `ImportProfileDialog.svelte` receives that event and opens the full import dialog;
- `Advanced options` contains the real Bits UI `Import all files` checkbox;
- the final Import control is a real HTML button;
- with `ImportOptions.import_all = true`, Gale's `import_config()` includes all source files, including `export.r2x`, in the destination profile.

This gives the helper a durable post-import verification primitive: hash the `export.r2x` entry inside the already SHA-verified `.r2z`, then require the imported target profile's local `export.r2x` to have that exact hash.

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

Therefore the UIA targeting for `Advanced options -> Import all files -> Import` itself was proven to work.

### V1 sequencing defect

V1 reopened the same `.r2z` after resolving Missing Profiles. That produced a second `.r2z` file-open event through Gale's single-instance/deep-link path.

Observed result:

- the real S1.42AB import completed;
- Gale showed S1.42AB as the active profile;
- a second empty `Import profile` dialog remained visible with only `Enter import code...` and the generic Import button;
- PowerShell waited for a transient success-toast marker.

The empty dialog was therefore a helper sequencing defect, not an S1.42AB profile/import failure.

## V2 implementation

Helper marker:

`2026-09-04-import-uia-v2-single-open-evidence`

Blob:

`aa2b5ac7084fb08f75382405658b4ffa49452587`

Implementation/final syntax-fix commit:

`2c25fccabdf177a6cc114a3eaba752014cf5cb45`

V2 changed the architecture:

1. open the verified `.r2z` exactly once;
2. do not re-send the file after Missing Profiles closes;
3. wait for the full import dialog already produced by the original buffered file-open event;
4. preserve the validated semantic UIA import sequence;
5. remove dependence on Gale's transient success toast;
6. hash the `export.r2x` entry inside the SHA-verified `.r2z` before opening Gale;
7. after Import, wait for the exact target directory and require its local `export.r2x` SHA-256 to equal the archive-entry hash;
8. remove the temporary `.r2z` only after that evidence passes.

### V2 download failure

The first controlled V2 user test failed safely before any destructive local action because V2 appended a cache-busting query string to the binary Raw GitHub `.r2z` download, producing:

`Invoke-WebRequest : 404: Not Found`

followed by:

`Download fehlgeschlagen oder Datei ist leer`

At that point the old profile had not yet been selected or deleted.

## V2.1 download hotfix

Canonical helper:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Validated helper marker:

`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob:

`9458f427b538615249714e7f064f3107d6dcd36c`

Validated hotfix commit:

`f711f53f4971f97200ed3605479ef887a14b243d`

V2.1 changed only the failing download plumbing:

- mutable controller reads may retain cache-busting/no-cache behavior;
- the binary candidate `.r2z` download uses the proven plain Raw GitHub URL with no query string;
- exact profile SHA-256 verification remains mandatory before any destructive local action;
- all V2 single-open, UIA import and `export.r2x` post-import verification behavior is preserved.

## V2.1 controlled validation — FULL PASS

Starting condition:

- S1.42AA existed normally in Gale;
- S1.42AB was not locally imported;
- the commit-pinned V2.1 helper was executed;
- the user selected S1.42AA and confirmed replacement with `y`.

Observed PowerShell evidence:

- helper marker: `2026-09-04-import-uia-v2.1-download-hotfix`;
- active repository build: `S1.42AB`;
- candidate: `LC V1 S1.42AB Interior Weight Normalization.r2z`;
- expected profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- downloaded profile SHA-256 matched exactly;
- archive `export.r2x` evidence SHA-256 was computed as `331c01bfe5eda5d4ce9bc2a887fd322b302f32dccf9d95918d6c7d0c7fb6cf40`;
- S1.42AA was deleted only after explicit `y`;
- the verified candidate was opened exactly once;
- Gale's Missing Profiles dialog was automatically resolved with `Delete -> Submit`;
- PowerShell explicitly waited for the import dialog from the single original `.r2z` invocation;
- `Import all files` was activated automatically;
- Import was invoked automatically;
- no second empty import-code dialog appeared;
- PowerShell verified the exact target profile's local `export.r2x` against the expected archive-entry SHA-256;
- the temporary downloaded `.r2z` was removed automatically;
- PowerShell returned to the prompt with no manual Gale click or final Enter after profile selection / `y`.

Therefore V2.1 is **FULL END-TO-END USER-VALIDATED** and is promoted into the canonical helper workflow.

## Canonical automatic import contract

After explicit profile selection and `y`, the helper automatically:

1. deletes only the selected old profile;
2. opens the SHA-verified candidate exactly once;
3. resolves the simple one-profile Missing Profiles gate;
4. locates the full target-profile import dialog;
5. verifies the exact expected profile identity;
6. expands `Advanced options`;
7. requires exactly one visible import toggle;
8. sets `Import all files` to On and verifies it remains On;
9. requires exactly one dialog-local Import button;
10. invokes Import;
11. waits for the exact target profile's `export.r2x`;
12. requires exact SHA-256 equality with the candidate archive's `export.r2x` entry;
13. removes the temporary `.r2z` only after verification.

## Fail-closed rules

Automatic UI interaction is refused if any relevant target is ambiguous. The helper never uses:

- screen-coordinate mouse clicks;
- blind `Tab` / `Enter` / arrow-key sequences;
- fuzzy profile/build matching;
- direct Gale SQLite mutation.

Additional permanent guards:

- the exact new target profile must not already exist separately before replacement;
- candidate SHA-256 must pass before deletion is offered;
- the `.r2z` must be opened exactly once during the automated sequence;
- do not append cache-busting query strings to the binary `.r2z` Raw GitHub URL;
- post-import success is established by exact target-profile `export.r2x` hash equality, not a transient toast;
- changed future automation branches require fresh user validation before they may be described as proven.
