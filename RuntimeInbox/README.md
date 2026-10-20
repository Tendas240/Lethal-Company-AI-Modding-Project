# RuntimeInbox

This is the only intended handoff point for files that are created locally by actually running Lethal Company.

The project is repository-first. Do not keep a local repository clone for ChatGPT handovers or profile builds.

## User action after a runtime test

Navigate on GitHub to:

`RuntimeInbox/Current/`

Use **Add file -> Upload files** and drag in the evidence from the exact tested profile, normally:
- `LogOutput.log`
- relevant post-run `.cfg` files, or preferably a config ZIP when a whole config tree is requested
- screenshots only when they materially document a runtime observation

The active build is declared in `RuntimeInbox/ACTIVE_BUILD.txt`; ChatGPT should keep that file current before asking for evidence.

A GitHub Actions workflow automatically:
1. hashes the uploaded files;
2. stores the originals under `RuntimeEvidence/<build>/<timestamp>/raw/`;
3. safely extracts ZIP/R2Z archives under `RuntimeEvidence/<build>/<timestamp>/extracted/`;
4. writes an `INDEX.json`;
5. clears the inbox files after the evidence is committed.

After upload, the evidence is online and readable from GitHub. The user should not need to convert CFG files to TXT just for ChatGPT.

## Reserved historical S1.42AK Offense original (no current upload permission)

After a separate explicit approval of the single-use uploader, **only**
`RuntimeInbox/Current/S1.42AK_OFFENSE_20261020_LogOutput.log`
may hold the historical completed S1.42AK original named in
`Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json`.
Never upload that original as `RuntimeInbox/Current/LogOutput.log`
while `RuntimeInbox/ACTIVE_BUILD.txt` names BMDSFIX1.
The contract checks exact SHA-256 and size, consumes once and persists the
raw under S1.42AK. A completed run does not require new gameplay.
This documentation is not permission to upload, build, import, merge,
activate or test anything.
