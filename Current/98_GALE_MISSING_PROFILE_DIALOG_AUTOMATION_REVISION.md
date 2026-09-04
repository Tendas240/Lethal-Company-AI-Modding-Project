# Gale Missing-Profile Dialog Automation Revision

**Date:** 2026-09-04  
**Status:** IMPLEMENTED / USER VALIDATION STILL OPEN / TWO OBSERVED FALLBACK RUNS

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

After the selected local profile directory is deleted and the verified `.r2z` opens Gale, the helper performs a best-effort targeted Windows UI Automation pass for the known Gale `Missing Profiles` dialog.

The current helper revision filters candidate controls by their actual supported UIA interaction patterns rather than trusting duplicate visible text nodes from the Gale/Chromium accessibility tree. It also emits diagnostic counts when the actionable selector cannot be resolved uniquely.

The single-missing-profile automation remains fail-closed. If the expected actionable controls are not uniquely resolved, the helper does not click anything; it asks the user to resolve `Delete -> Submit` manually and waits for confirmation.

## Validation attempts on S1.42AB

### Attempt 1

The first UIA implementation fell back with:

`ambiguous`

The `Missing Profiles` dialog remained open, the user had to select `Delete`, press `Submit`, then return to PowerShell and press Enter. The final `Advanced options -> Import all files -> Import` step also remained manual.

This first revision used raw accessible-name uniqueness and was superseded.

### Attempt 2 / cache ambiguity

A second user reproduction again showed the same `ambiguous` fallback and manual interaction requirement.

However, the screenshot from that run does **not** contain the mandatory diagnostic line added by the newer interaction-pattern revision, such as:

`UIA diagnostic: actionable missing-profile selectors = <count>`

The invoked command used the same mutable Raw GitHub `main/.../ReplaceActiveGaleProfile.ps1` URL repeatedly shortly after repository updates. Therefore this run cannot prove that the latest helper blob executed; a stale Raw-GitHub/CDN response is a plausible explanation.

The next validation must therefore use a commit-pinned Raw URL (or an explicit cache-busting launcher) so the executed script revision is unambiguous.

Current interaction-pattern helper blob:

`54fddc6731ef97377730d3eb741826cfd738aa08`

Commit that installed that revision:

`2e3aaf5e9dc8381b979ce85b03e38970cf55fbf4`

## Exact next helper validation

Reproduce the known starting condition only if the user wants to continue helper validation:

- S1.42AA exists normally in Gale;
- S1.42AB is not yet locally imported/downloaded for that reproduction;
- invoke the helper by the exact commit-pinned URL for commit `2e3aaf5e9dc8381b979ce85b03e38970cf55fbf4`;
- select S1.42AA and confirm deletion with `y`;
- observe the PowerShell output when `Missing Profiles` appears.

Acceptance for the UIA branch requires automatic `Delete -> Submit` with no manual dialog interaction. If it still falls back, the diagnostic selector count must be captured before changing the implementation again.

## Separate architecture finding: Gale native overwrite

Current Gale import source was also inspected after the failed UIA attempts. Gale supports overwriting an existing profile natively. With `merge = false`, Gale's `incremental_update` removes Thunderstore mods that are not in the imported profile, reconciles enabled states, and installs missing/new versions. Its `import_config` path removes extra destination config files when not merging and, with `import_all = true`, copies all profile files rather than only normally allowed config formats.

This is a promising future redesign because it can avoid externally deleting a profile before Gale starts and therefore avoid creating the `Missing Profiles` state at all. It is not yet the canonical workflow because Gale's overwrite path uses the selected existing profile name; the project still needs a clean strategy for ending with the new canonical build/profile name rather than retaining the old name.

## Explicitly not automated yet

The helper does not yet automate:

- `Advanced options`;
- `Import all files`;
- the final Gale `Import` button;
- arbitrary missing profiles when more than one is present;
- direct SQLite/database mutation;
- screen-coordinate mouse clicks;
- blind `Tab`/`Enter`/arrow-key sequences.

Until a specific UIA path is proven on the user's actual Gale/WebView environment, these remain manual.
