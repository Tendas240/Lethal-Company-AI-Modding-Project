# S1.42AK-LFDIAG1 inactive review-build checkpoint

Date: 2026-10-06.  
Status: PASS ON REVIEW BRANCH / INDEPENDENT FROZEN-ARTIFACT REHASH PASS / FINAL PR-HEAD FREEZE VERIFICATION PENDING.  
Authority: `Current/280_S1.42AK_LFDIAG1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md`.  
Classification: **DIAGNOSTIC ONLY / NEVER ACCEPT**.

## Exact successful build

The exact main-integrated LFDIAG1 source was compiled on PR #291 at build head
`1a57702777eb63e7f1fd4571a67f09e705457c6f`.

- Review workflow run: `37435859117` / #1 / `pull_request` — success.
- Review job: `112177366658` — success.
- Knowledge Architecture at the same build head: `37435858991` / #1183 — success.
- Compiler result: **0 warnings / 0 errors**.
- Assembly identity: `S142AKLFDiag1`.
- DLL SHA-256: `13fd01cba6d30a0c9044d43df813b17adf352139f723c9444f8db14403a0a474`.

The same review job reran the pure fail-closed Liminal Facility policy and
`AnalysisTools/validate_s142ak_lfdiag1_source.py`; both passed before archive construction.

## Exact archive contract

Parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

Review identity: `LC V1 S1.42AK-LFD1`  
Review profile SHA-256: `ce6835944f90e1972caebf52dc344bdf660283c9a074ac07899486ce0b4564f4`

The validator proved the exact **337 -> 338** archive contract, adding only
`BepInEx/plugins/S142AKLFDiag1/S142AKLFDiag1.dll`; only `export.r2x` changed,
limited to the profile-name identity. Removed/package/config counts are zero.
The inherited BMDSFIX1 DLL remains
`f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
the accepted normalizer remains
`901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
All eight deliberate negative mutations were rejected. The permanent Gale path guard
passed at **217/255**.

## Frozen Actions artifact and independent rehash

Authoritative frozen artifact:

- artifact ID: `11399366599`;
- name: `S1.42AK-LFDIAG1-review-1a57702777eb63e7f1fd4571a67f09e705457c6f`;
- size: **536867 bytes**;
- Actions ZIP SHA-256: `ca1922b3b59666cfd5f8a6105dec9e1dfddf367874be4d3a324bfd8dfacf0b93`;
- retention expiry: `2027-01-04T08:24:09Z`.

The artifact was downloaded independently into a separate assistant workspace.
Its actual ZIP bytes exactly matched the Actions upload digest. ZIP CRC validation
passed. The downloaded ZIP contains exactly four files; the downloaded profile and
DLL independently match the hashes above.

`BUILD_RESULT.json` and `STATIC_VERIFICATION.json` are preserved as the exact
chronological bytes uploaded by the successful job. `REVIEW_BUILD_CHECKPOINT.json`
closes the later independent-rehash requirement without rewriting those historical bytes.

One pre-freeze evidence-write race produced a later **superseded/non-authoritative** artifact:
- artifact ID `11398652708`;
- run `37436398066` / #2;
- head `d443351b34af437c73f31507801c7471cc24f67b`;
- Actions digest SHA-256 `73c4278ff5da3b3dc27b697deed84da83cba676c3639ccb3431f5c996ea11535`;
- size **536884 bytes**.

It was created before `REVIEW_BUILD_CHECKPOINT.json` existed and was **not** independently rehashed or selected as authority. It must never be published, imported, armed, or substituted for artifact `11399366599`. The committed freeze checkpoint makes subsequent review runs refuse recompilation, reconstruction and upload.

## Lifecycle boundary

This checkpoint does **not** publish or activate LFDIAG1.

- No LFDIAG1 review profile is committed.
- No `ProfileSources/S1.42AK-LFDIAG1/` exists.
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
- No Gale replacement/import occurred.
- No runtime activation or gameplay test is authorized or performed.
- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED** with its passive, outstanding,
  unwaived selector-free Black Mesa x `DeepSewersFlow` gate.
- Phase-C residual remains **28**; Liminal Facility still lacks runtime generation proof.

The next work after final PR-head freeze verification and main integration is a separately
bounded exact-byte publication-authorization decision. Do not reconstruct different review bytes.
