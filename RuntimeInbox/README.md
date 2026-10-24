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

## S1.42AK Offense random-batch V2 (contract only, NOT upload approval)

The separately versioned contract is `Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_INGEST_V1.json`.
It is bound to exactly 10,906,072 original bytes with SHA-256
`969044ab459387c3a509134c4c56a10ae1736b46af9fc76d3ac8cf01c25ec07d`,
user-attested unchanged S1.42AK profile and unchanged S1.42AK-BMDSFIX1 runtime pointer.
Only after **separate express raw/public repository upload approval**, the reserved inbox
the reserved filename `S1.42AK_OFFENSE_RANDOM_BATCH_20261021_LogOutput.log` inside the existing `RuntimeInbox/Current/` directory
may hold these verified bytes as the **only inbox source**. Do not use ordinary
`RuntimeInbox/Current/LogOutput.log` or the disposable `runtime-large` pipeline.
A completed gameplay batch must not be replayed merely to upload evidence.
Pre-publication review for secrets/personal information, local hash/size re-check,
current contract/controller/head preflight and separate retention decision are required.
The V2 raw must be retained until a separate P0-P6/retention decision; a successful
Ingest/CI does not certify any Interior generation, P0/P1, or baseline acceptance.

## S1.42AK exploratory Offense V3 (PREPARED_UNARMED)

The unique future reserved source is `RuntimeInbox/Current/S1.42AK_OFFENSE_EXPLORATORY_V3_LogOutput.log`.
The versioned contract is `Current/S1.42AK_OFFENSE_EXPLORATORY_V3_INGEST_V1.json`, initially
`PREPARED_UNARMED` with unknown size/SHA-256 and no upload authorization.
**Do not upload anything yet.** Only a later separately reviewed, exact-original-byte-bound
`PENDING` contract with `upload_authorized=true` can permit one source and
S1.42AK attribution without changing the active BMDSFIX1 controller.
The existing V1/V2 contracts are CONSUMED and cannot be reused.
Ordinary `LogOutput.log` and disposable `runtime-large` are not V3 routes.
Raw original retention and P0-P6/owner/safety gates remain in force.
