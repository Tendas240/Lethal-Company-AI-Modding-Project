# S1.42AK-AGDIAG1 inactive review-build checkpoint

Date: 2026-10-04.  
Status: PASS ON REVIEW BRANCH / INDEPENDENT FROZEN-ARTIFACT REHASH PASS / MAIN INTEGRATION OUTSTANDING.  
Authority: `Current/256_S1.42AK_AGDIAG1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md`.  
Classification: **DIAGNOSTIC ONLY / NEVER ACCEPT**.

## Exact successful build

The exact main-integrated AGDIAG1 source was compiled on PR #259 at build head
`46a5924ae142b0c00ff9fbbc6fecec5e2a4badae`.

- Review workflow run: `37199874193` / #4 / `pull_request` — success.
- Review job: `111429183786` — success.
- Knowledge Architecture at the same build head: `37199874237` / #1072 — success.
- Compiler result: **0 warnings / 0 errors**.
- Assembly identity: `S142AKAGDiag1`.
- DLL SHA-256: `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`.

The same review job reran the pure fail-closed Art Gallery policy and the existing
`AnalysisTools/validate_s142ak_agdiag1_source.py`; both passed before the archive
was constructed.

Three earlier Actions runs (`37199764686`, `37199815703`, `37199840728`)
failed before job creation while the new workflow definition was being aligned to the
proven frozen-artifact precedent. They compiled or constructed nothing and are not
candidate artifacts.

## Exact archive contract

Parent: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`  
Parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

Review identity: `LC V1 S1.42AK-AGD1`  
Review profile SHA-256: `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`

The validator proved:

- archive members: **337 -> 338**;
- added exactly `BepInEx/plugins/S142AKAGDiag1/S142AKAGDiag1.dll`;
- changed existing member exactly `export.r2x`, limited to the exact profile-name identity replacement;
- removed members: **0**;
- package changes: **0**;
- config changes: **0**;
- inherited BMDSFIX1 DLL preserved at `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB normalizer preserved at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- eight explicit negative mutation cases rejected;
- permanent Gale path-length guard and self-test passed at **217/255**.

## Frozen Actions artifact and independent rehash

Authoritative frozen artifact:

- artifact ID: `11302468045`;
- name: `S1.42AK-AGDIAG1-review-46a5924ae142b0c00ff9fbbc6fecec5e2a4badae`;
- size: **536850 bytes**;
- Actions ZIP SHA-256: `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`;
- retention expiry: `2027-01-02T11:46:39Z`.

The artifact was downloaded independently into a separate assistant workspace.
Its actual ZIP bytes were rehashed with Python `hashlib` and produced the exact same
SHA-256 `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`.
ZIP CRC validation passed. The downloaded ZIP contains exactly four files; the
downloaded profile and DLL independently rehash to the exact profile/DLL hashes above.

`BUILD_RESULT.json` and `STATIC_VERIFICATION.json` are preserved as the exact
chronological bytes uploaded by the successful job. Their earlier
`AWAITING...` / `OUTSTANDING_AFTER_ARTIFACT_FREEZE` labels describe their point
in the pipeline. `REVIEW_BUILD_CHECKPOINT.json` is the later evidence that closes
the independent Actions-artifact rehash requirement without rewriting history.

## Lifecycle boundary

This checkpoint does **not** publish or activate AGDIAG1.

- No `Profiles/LC V1 S1.42AK-AGD1.r2z` is committed.
- No `ProfileSources/S1.42AK-AGDIAG1/` exists.
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
- No Gale replacement/import occurred.
- No runtime activation or gameplay test is authorized or performed.
- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED**; its normal selector-free
  Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived.

The next work after this branch checkpoint is review of PR #259's final changed-file
set and exact final-head CI, followed by main integration/canonical lifecycle
reconciliation only if those gates remain green. Exact-byte publication remains a
separate later authorization decision. Do not reconstruct different review bytes.
