# BuildSpecs

This directory is the online control plane for profile builds.

`current.json` is the build request consumed by GitHub Actions. ChatGPT should edit this file in GitHub instead of asking the user to run local PowerShell build scripts.

## Operating model

1. The exact base `.r2z` lives under `Profiles/`.
2. ChatGPT edits `BuildSpecs/current.json`.
3. A push to `current.json` triggers `.github/workflows/profile-build.yml`.
4. GitHub Actions builds and verifies the new `.r2z` entirely on GitHub.
5. The workflow commits the generated profile to `Profiles/`, a readable text snapshot to `ProfileSources/<build_id>/`, and machine-readable results to `Current/AUTO_BUILD_RESULT.*`.
6. ChatGPT reads the result and continues without a local repository copy or local build script.

`enabled: false` means no build is requested. This is intentional during the one-time migration of the current S1.41 binary into GitHub.

## Spec fields

- `build_id`: unique build identifier, for example `S1.42A`.
- `base_profile`: exact repository path of the base `.r2z`.
- `base_sha256`: mandatory SHA-256 guard.
- `output_profile`: new repository profile path.
- `profile_name`: internal Gale profile name.
- `mod_state_changes`: exact package/version enable/disable changes.
- `config_patches`: INI/BepInEx section-key-value edits.
- `text_assertions`: post-build verification.

Never point a gameplay build at a diagnostic-only profile.

## Supported automated changes

The current builder supports:
- `mod_state_changes`: enable/disable an existing exact package version;
- `mod_additions`: add an exact Thunderstore package/version to the Gale export;
- `mod_removals`: remove an exact package/version;
- `config_patches`: change or create BepInEx section/key values;
- `file_injections`: inject a repository-hosted binary/text file into the profile;
- `local_plugin_builds`: compile a repository-hosted .NET project on GitHub Actions and inject its output;
- `text_assertions`: verify required/forbidden output text.

For new Thunderstore content, ChatGPT should research and pin the intended package plus any dependencies required by the chosen build architecture. The user should not have to install those packages manually before the profile is built.
