# Gale Missing-Profile Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** USER-VALIDATED / PROMOTED INTO CANONICAL HELPER

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

The helper preserves all previously validated safety properties:

- repository-driven exact `ACTIVE_BUILD` / `AUTO_BUILD_RESULT` match;
- download before destructive action;
- SHA-256 verification before deletion;
- numeric local-profile selection;
- explicit `y/n` confirmation;
- no fuzzy build/profile matching;
- no local repository clone requirement.

After the selected local profile directory is deleted and the verified `.r2z` opens Gale, the helper performs targeted Windows UI Automation for the known Gale `Missing Profiles` dialog.

The working implementation filters the Gale/WebView accessibility tree by actual interaction patterns rather than trusting duplicate visible text nodes:

1. exactly one actionable `Select an action` element with `ExpandCollapsePattern` must be present;
2. that selector is expanded;
3. exactly one actionable `Delete` item with `SelectionItemPattern` must be present;
4. `Delete` is selected;
5. exactly one actionable `Submit` control with `InvokePattern` must be present;
6. `Submit` is invoked;
7. the helper verifies that `Missing Profiles` disappears.

If any condition fails or more than one unresolved row is exposed, the helper does not click blindly and falls back to manual resolution.

## Validation history

Two early tests of mutable `main/.../ReplaceActiveGaleProfile.ps1` URLs fell back with `ambiguous`. One of those screenshots lacked diagnostics that were mandatory in the newest revision, so stale Raw-GitHub/CDN content was suspected.

The user then restored the real pre-S1.42AB replacement state with S1.42AA present locally and S1.42AB not yet imported and tested the exact commit-pinned helper revision from:

`2e3aaf5e9dc8381b979ce85b03e38970cf55fbf4`

Result:

- profile download and SHA-256 verification succeeded;
- S1.42AA selection/deletion flow succeeded;
- Gale opened;
- `Missing Profiles` was resolved automatically;
- the normal S1.42AB import dialog became available without manual `Delete -> Submit` interaction.

Therefore the missing-profile UI Automation path is now **user-validated** for the actual Gale/WebView environment used by this project.

## Cache lesson

During helper-development validation, use a commit-pinned Raw GitHub URL so the exact script revision is deterministic. Mutable `main` is appropriate again only after a helper revision has been validated and stabilized.

## Successor work

The remaining manual boundary after this validation was:

`Advanced options -> Import all files -> Import`

That successor automation is tracked in:

`Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`
