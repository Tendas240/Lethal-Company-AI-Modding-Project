# S1.42AK-DRDIAG1 inactive review-build checkpoint

Date: 2026-10-05.  
Status: PASS ON REVIEW BRANCH / INDEPENDENT FROZEN-ARTIFACT REHASH PASS / MAIN INTEGRATION OUTSTANDING.  
Authority: `Current/268_S1.42AK_DRDIAG1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md`.  
Classification: **DIAGNOSTIC ONLY / NEVER ACCEPT**.

## Exact successful build

The exact main-integrated DRDIAG1 source was compiled on PR #274 at build head
`5e10e1084425ee7152761d919a0b0ccc57282ff5`.

- Review workflow run: `37273709334` / #1 / `pull_request` — success.
- Review job: `111646002290` — success.
- Knowledge Architecture at the same build head: `37273709257` / #1134 — success.
- Compiler result: **0 warnings / 0 errors**.
- Assembly identity: `S142AKDRDiag1`.
- DLL SHA-256: `512b3085619852ba723163522860cf64f4ace53a6ae09356ae0ad943a59adf3b`.

The same review job reran the pure fail-closed Drains policy and the existing
`AnalysisTools/validate_s142ak_drdiag1_source.py`; both passed before archive construction.

## Exact archive contract

Parent: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`  
Parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

Review identity: `LC V1 S1.42AK-DRD1`  
Review profile SHA-256: `15587975580ea9de38f995ff2e2a64586977c4c1a32f2c87534011375394c3d4`

The validator proved the exact **337 -> 338** archive contract, adding only
`BepInEx/plugins/S142AKDRDiag1/S142AKDRDiag1.dll`; only `export.r2x` changed,
limited to the profile-name identity. Removed/package/config counts are zero.
The inherited BMDSFIX1 DLL remains
`f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
the accepted normalizer remains
`901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
All eight deliberate negative mutations were rejected. The permanent Gale path guard
passed at **217/255**.

## Frozen Actions artifact and independent rehash

Authoritative frozen artifact:

- artifact ID: `11329346796`;
- name: `S1.42AK-DRDIAG1-review-5e10e1084425ee7152761d919a0b0ccc57282ff5`;
- size: **536836 bytes**;
- Actions ZIP SHA-256: `6a6ec13a36f9c3f655f025b73ec477e02394caac4831cee3fe395fe2ec24bf63`;
- retention expiry: `2027-01-03T06:41:38Z`.

The artifact was downloaded independently into a separate assistant workspace.
Its actual ZIP bytes exactly matched the Actions upload digest. ZIP CRC validation
passed. The downloaded ZIP contains exactly four files; the downloaded profile and
DLL independently match the hashes above.

`BUILD_RESULT.json` and `STATIC_VERIFICATION.json` are preserved as the exact
chronological bytes uploaded by the successful job. `REVIEW_BUILD_CHECKPOINT.json`
closes the later independent-rehash requirement without rewriting those historical bytes.

No intermediate or superseded review artifact exists for this checkpoint. The committed
freeze checkpoint makes subsequent review runs refuse recompilation, reconstruction and upload.

## Lifecycle boundary

This checkpoint does **not** publish or activate DRDIAG1.

- No DRDIAG1 review profile is committed.
- No `ProfileSources/S1.42AK-DRDIAG1/` exists.
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
- No Gale replacement/import occurred.
- No runtime activation or gameplay test is authorized or performed.
- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED** with its passive, outstanding,
  unwaived selector-free Black Mesa x `DeepSewersFlow` gate.
- Phase-C residual remains **29**; Drains still lacks runtime generation proof.

The next work after this branch checkpoint is final PR-head freeze verification,
main integration and canonical lifecycle reconciliation. Exact-byte publication remains
a separate later authorization decision. Do not reconstruct different review bytes.
