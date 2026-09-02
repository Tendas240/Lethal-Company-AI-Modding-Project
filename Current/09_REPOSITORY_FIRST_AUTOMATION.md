# 09 — Repository-First Automation Policy

This file is binding for future project work unless the user explicitly changes the policy.

## Goal

The GitHub repository is the durable source of truth and build workspace.

Do not require a local repository clone on the user's PC for ChatGPT handovers, profile generation, patch compilation, build verification, or project documentation.

Do not ask the user to run local PowerShell build scripts when the required base artifacts already exist in GitHub.

## Canonical online locations

- Final Gale profiles: `Profiles/*.r2z`
- Human-/machine-readable profile contents: `ProfileSources/<build_id>/`
- Build request: `BuildSpecs/current.json`
- Build engine: `BuildSystem/profile_builder.py`
- Build workflow: `.github/workflows/profile-build.yml`
- Latest automated build result: `Current/AUTO_BUILD_RESULT.json` and `Current/AUTO_BUILD_RESULT.md`
- Runtime upload inbox: `RuntimeInbox/Current/`
- Active runtime build: `RuntimeInbox/ACTIVE_BUILD.txt`
- Persisted runtime evidence: `RuntimeEvidence/<build>/<timestamp>/`

## Future profile builds

ChatGPT should:

1. verify the exact base profile and its SHA-256 in `Profiles/`;
2. edit `BuildSpecs/current.json` directly on GitHub;
3. let GitHub Actions build the new profile;
4. inspect the workflow result/logs;
5. verify `Current/AUTO_BUILD_RESULT.*` and `ProfileSources/<build_id>/`;
6. continue project work from the generated GitHub profile.

The user should not need to download a base profile, edit an archive, run PowerShell, maintain a local repo clone, or calculate hashes.

The builder supports:
- internal Gale profile-name changes;
- exact enable/disable changes for existing Thunderstore packages;
- adding/removing exact Thunderstore package versions in `export.r2x`;
- BepInEx INI/config edits;
- repository-hosted file injection;
- building repository-hosted local .NET patches and injecting their output;
- exact base-hash guarding;
- member-delta verification;
- readable config/export snapshots.

## Runtime evidence

Game runtime itself necessarily happens on the user's PC. That is the remaining unavoidable local step.

After a test, the user should upload the generated evidence through GitHub's web UI to `RuntimeInbox/Current/`. The ingestion workflow then persists and extracts it online so ChatGPT can read it from GitHub.

The user should not need to rename `.cfg` to `.txt` merely for ChatGPT compatibility.

## Binary accessibility rule

Binary `.r2z`, `.zip`, and `.dll` artifacts may not be directly UTF-8-readable through the GitHub connector. Therefore every generated profile must also have:
- a readable `ProfileSources/<build_id>/` snapshot for text/config inspection;
- a file index containing member hashes;
- a GitHub Actions artifact for binary retrieval when required.

Binary manipulation should happen inside GitHub Actions, where repository checkout provides byte-accurate access.

## One-time migration — complete

The local-only gap has been closed.

Exact accepted S1.40B and canonical S1.41 were uploaded to `Profiles/` and automatically verified/indexed by GitHub Actions.

Verified online profiles:
- `Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z` — SHA-256 `fd303f73f0f2223a6375fcf2b7ed209dae77e1934e3b4e8139932a89e7de7eb9`
- `Profiles/LC V1 S1.41 BCMER Reactivation.r2z` — SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Readable snapshots:
- `ProfileSources/S1.40B/`
- `ProfileSources/S1.41/`

Future profile generation must default to GitHub-only automation. A local build chain is no longer required.
