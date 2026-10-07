# ProfileSources

Readable mirrors of text/config content extracted from canonical or imported Gale `.r2z` profiles.

This directory exists because the GitHub connector can inspect UTF-8 repository files reliably, while binary `.r2z` archives are intentionally handled by GitHub Actions.

Each build/index snapshot includes `FILE_INDEX.json` with archive member SHA-256 hashes. Generated builds also write the latest result to `Current/AUTO_BUILD_RESULT.*`.

Do not treat a snapshot as a standalone installable profile. The installable artifact remains under `Profiles/`.
