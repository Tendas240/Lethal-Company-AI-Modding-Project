# Pre-Overhaul Backup and Recovery

**Status:** CURRENT / VERIFIED RECOVERY TOPIC  
**Authority:** semantic recovery router; machine proof is `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`  
**Canonical-For:** `pre_overhaul_backup_and_recovery`  
**Evidence:** `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`, reciprocal backup `PRE_OVERHAUL_BACKUP_MANIFEST.json`  
**Related:** `Knowledge/REPOSITORY_OVERHAUL.md`, `Current/OVERHAUL_EXECUTION_STATE.json`  
**Last-Validated:** 2026-09-04

## Frozen recovery point

Primary repository pre-overhaul checkpoint:

- repository: `Tendas240/Lethal-Company-AI-Modding-Project`
- frozen commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`
- frozen tree: `0e17aac410cf600a164396b5586b5b50f084df22`

Supplemental same-repository branch:

`pre-overhaul-freeze-20260904-5dbd0e6`

The branch is extra protection only; it did **not** satisfy the standalone-backup gate by itself.

## Standalone backup repository

`Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`

The exact frozen commit and exact frozen tree are present in that independent repository. Normal project branches were preserved, including `runtime-large`; the source had no tags at verification time.

The backup repository has one archival provenance-manifest commit on top of the exact frozen source commit so it can identify its recovery purpose and primary repository.

## Mirror limitation

During the user-run `git push --mirror`, GitHub rejected hidden `refs/pull/*` refs because GitHub manages those refs internally and denies updates to them. Normal branches were preserved, no tags were missing, and the exact frozen source commit/tree identity was independently verified.

This limitation is recorded in the machine manifest and does not invalidate project recovery.

## Authority rule

The backup is:

- historical/read-only;
- a recovery/comparison source;
- **not** the current Source of Truth;
- not to be reused for continued development.

The primary repository remains the current Source of Truth.

## Rollback use

If the information-architecture migration loses information, produces ambiguous authority, breaks navigation or fails validation:

1. stop further destructive migration;
2. compare against the standalone backup/frozen checkpoint;
3. restore missing knowledge/references;
4. revert/replan if necessary rather than continuing cleanup for appearance.

Machine provenance and exact verification details: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.
