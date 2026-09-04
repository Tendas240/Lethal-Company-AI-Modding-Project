# Gale Import Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** IMPLEMENTED / USER VALIDATION PENDING

## Context

The preceding helper revision successfully automated Gale's blocking `Missing Profiles -> Delete -> Submit` recovery flow. The user confirmed that this part now works on the actual project Gale/WebView environment.

The remaining manual step was the normal profile-import dialog:

`Advanced options -> Import all files -> Import`

The user explicitly requested that this remaining import step also be automated where it can be done safely.

## Upstream Gale evidence

Current Gale source confirms that the relevant controls are semantic UI controls rather than canvas-only elements:

- `ImportProfileDialog.svelte` contains the `Advanced options` details section;
- inside it, `Import all files` is bound to Gale's `Checkbox` component;
- `Checkbox.svelte` uses a real Bits UI checkbox root, which exposes a toggle semantic;
- the final `Import` control uses Gale's normal `Button` component, which renders a real HTML button;
- `Dialog.svelte` uses Bits UI dialog semantics with a real dialog title;
- Gale emits the localized success toast after `api.profile.import.profile(...)` returns successfully.

Therefore Windows UI Automation can target interaction patterns rather than screen coordinates or blind keyboard sequences.

## Implemented helper revision

Canonical implementation remains:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Current helper revision marker:

`2026-09-04-import-uia-v1`

Helper blob after implementation:

`689c9dcd7cbc38fcf9735309336106322a6203d8`

Commit that installed the revision:

`cace6989f12ed9c47d72e806851d17cdd706948b`

## Automatic import contract

After the missing-profile gate is resolved and the SHA-verified `.r2z` is reopened, the helper attempts the following fail-closed sequence:

1. detect the Gale import dialog by localized title (`Import profile` / `Profil importieren`);
2. resolve a dialog-local scope rather than scanning the entire Gale window for import controls;
3. require evidence that the dialog contains the exact expected target profile name, either as an accessible name or input `ValuePattern`;
4. if the advanced section is still collapsed, expand `Advanced options` / `Erweiterte Optionen` using `ExpandCollapsePattern` when available, otherwise a unique `InvokePattern` control;
5. require exactly one visible `TogglePattern` control inside the new-profile import dialog;
6. set that toggle to `On` if needed and verify it remains `On` before proceeding;
7. require exactly one dialog-local `Import` / `Importieren` button with `InvokePattern`;
8. invoke that button;
9. wait for Gale's localized import-success message for the exact expected profile name;
10. only after confirmed success remove the temporary `.r2z` automatically.

If the final Gale success toast is not exposed through UI Automation within the timeout, the helper does not assume success. It asks the user for the final confirmation before cleaning up the downloaded archive.

## Fail-closed rules

Automatic import is refused and the helper falls back to the established manual import instructions if any of these conditions occur:

- no Gale import dialog is detected;
- the expected profile identity cannot be verified;
- the advanced-options control is not uniquely actionable;
- the number of visible import-dialog toggle controls is not exactly one;
- the checkbox cannot be verified in `On` state;
- the final Import button is not uniquely actionable;
- Windows UI Automation is unavailable;
- any unexpected WebView accessibility shape makes the target ambiguous.

The helper never uses:

- mouse coordinates;
- blind `Tab` / `Enter` / arrow-key sequences;
- direct mutation of Gale's SQLite database;
- fuzzy profile-name matching.

## Additional safety guard

Before deleting the selected old profile, the helper now checks whether the exact new target profile name already exists as a separate local Gale profile. If it does, the helper aborts rather than risk an unintended overwrite.

## Validation target

For the next controlled validation, restore the known starting state:

- S1.42AA exists in Gale;
- S1.42AB is not locally imported;
- execute the exact commit-pinned helper revision for commit `cace6989f12ed9c47d72e806851d17cdd706948b`;
- select S1.42AA and confirm deletion with `y`.

Acceptance requires:

1. Missing Profiles is resolved automatically;
2. the S1.42AB import dialog appears;
3. `Advanced options` opens automatically;
4. `Import all files` becomes enabled automatically;
5. Import starts automatically;
6. no manual Gale click is required after the initial profile selection / `y` confirmation;
7. the resulting local profile is exactly `LC V1 S1.42AB Interior Weight Normalization`;
8. no unrelated Gale profile is touched;
9. temporary archive cleanup happens only after confirmed import success or explicit user confirmation fallback.

Until the user confirms that full sequence, describe the import-dialog UI Automation as **implemented but user-validation pending**.
