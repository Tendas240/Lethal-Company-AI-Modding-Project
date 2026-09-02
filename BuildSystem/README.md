# BuildSystem

GitHub-native automation used by ChatGPT.

- `profile_builder.py`: deterministic .r2z build engine. It verifies the exact base SHA-256, edits `export.r2x`, applies BepInEx config changes, can add/remove/toggle exact Thunderstore packages, can compile repository-hosted .NET patch projects, can inject files, checks archive-member deltas, and writes readable snapshots.
- `index_profile.py`: verifies and indexes .r2z files uploaded directly to `Profiles/`.
- `runtime_ingest.py`: persists, hashes, and extracts runtime evidence uploaded to `RuntimeInbox/Current/`.
- `test_profile_builder.py`: self-tests Gale `export.r2x` package addition against the accepted S1.41 readable export before any automated profile build. This guards the list indentation/version/enabled/source serialization needed by S1.42A.

These scripts run in GitHub Actions. They are not intended to be downloaded and executed manually by the user.
