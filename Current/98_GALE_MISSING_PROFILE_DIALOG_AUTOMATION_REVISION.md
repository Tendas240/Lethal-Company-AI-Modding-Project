# Gale Missing-Profile Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** IMPLEMENTED / USER VALIDATION PENDING

## Triggering observation

During replacement of the local Gale profile for S1.42AB, the user observed a previously unhandled Gale startup gate:

1. the helper closes Gale;
2. the helper deletes the selected local profile directory after explicit `y` confirmation;
3. opening the verified `.r2z` starts Gale;
4. Gale detects that the deleted profile still exists in its internal profile database but its directory is missing;
5. Gale opens the non-dismissible `Missing Profiles` dialog and requires `Locate` or `Delete` plus `Submit`;
6. this dialog blocks the normal profile-import dialog.

The previous helper validation with disposable profile `testpowershell` did not expose this blocking behavior in the same way, so the permanent helper contract required revision.

## Upstream Gale evidence

Current Gale source confirms this is intentional behavior rather than a random modal:

- `src/lib/components/dialogs/MissingProfilesDialog.svelte` opens whenever `profiles.list` contains missing profiles and cannot be closed until actions are submitted;
- `src/lib/components/dialogs/MissingProfileItem.svelte` exposes exactly `Locate` and `Delete` actions;
- the delete action calls Gale's `forgetProfile(profile.id)` path;
- Gale core `ManagedGame::forget_profile()` removes the in-memory profile entry and calls `db.delete_profile(id)`;
- `Db::delete_profile()` performs `DELETE FROM profiles WHERE id = ?`;
- Gale's changelog explicitly documents the missing-profile dialog for profiles manually moved or deleted outside Gale.

Direct external editing of `data.sqlite3` was considered and rejected for the canonical helper because it would couple the project to Gale's private database schema unnecessarily.

## Implemented helper revision

Canonical implementation remains:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

The helper still preserves all previously validated safety properties:

- repository-driven exact `ACTIVE_BUILD` / `AUTO_BUILD_RESULT` match;
- download before destructive action;
- SHA-256 verification before deletion;
- numeric local-profile selection;
- explicit `y/n` confirmation;
- no fuzzy build/profile matching;
- no local repository clone requirement;
- `Advanced options -> Import all files` remains a manual user gate.

After the selected local profile directory is deleted and the verified `.r2z` opens Gale, the helper now performs a best-effort **targeted Windows UI Automation** pass for the known Gale `Missing Profiles` dialog.

Automation is allowed only when all fail-closed conditions hold:

1. Windows UI Automation assemblies load successfully;
2. a Gale window is detected;
3. the exact `Missing Profiles` accessibility element is visible;
4. the selected/deleted profile name is visible in the Gale accessibility tree;
5. exactly one visible `Select an action` controller exists, proving the simple one-missing-profile case;
6. exactly one visible `Delete` option is exposed after expanding that controller;
7. exactly one visible `Submit` control is exposed;
8. the `Missing Profiles` dialog disappears after submission.

If any condition is not met, the helper **does not click anything blindly**. It prints a warning, asks the user to resolve the selected profile manually with `Delete` -> `Submit`, waits for confirmation, and only then continues.

After successful automatic or manual resolution, the helper re-opens the same already downloaded and SHA-verified `.r2z`. Gale's `ImportProfileDialog` is a singleton component, so this is intended to re-trigger/refresh the import event after the blocking missing-profile gate is gone rather than create an independent second import workflow.

## Explicitly not automated

The helper does **not** automate:

- `Advanced options`;
- `Import all files`;
- the final Gale `Import` button;
- arbitrary missing profiles when more than one is present;
- direct SQLite/database mutation;
- screen-coordinate mouse clicks;
- blind `Tab`/`Enter`/arrow-key sequences.

The user still explicitly enables `Advanced options -> Import all files` and completes the actual profile import.

## Validation required

The next use of the canonical launcher should verify:

1. selected old profile is deleted only after explicit `y`;
2. Gale opens;
3. when exactly that one deleted profile is reported missing, the helper selects `Delete` and submits it automatically;
4. no unrelated profile is touched;
5. the missing-profile dialog closes;
6. the normal profile import dialog becomes available/reopens;
7. the user can manually enable `Advanced options -> Import all files` and import S1.42AB normally;
8. temporary `.r2z` cleanup still occurs only after the user confirms successful import.

Until this exact revised flow is user-confirmed, describe the new missing-profile automation as **implemented but validation pending**. The older y/n/download/hash/profile-selection safety flow remains historically validated.
