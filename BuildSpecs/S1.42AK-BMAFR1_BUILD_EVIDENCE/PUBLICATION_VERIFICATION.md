# S1.42AK-BMAFR1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES MATERIALIZED ON PUBLICATION BRANCH / MAIN INTEGRATION PENDING / NOT INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-02  
**Reviewed source/build head:** `5d069538ab4f75a52a7ab2a998cee4edc01a7797`  
**Review workflow run:** `36986031171` (run `7`)  
**Frozen Actions artifact:** `11218000891`  
**Artifact name:** `S1.42AK-BMAFR1-review-4e1427deebd9af960e9ed606391bf8326d168212`  
**Artifact ZIP SHA-256:** `49e9402bb2521a2a56c3634563f1ed6a9d8bb3fc98895dd23ad936ec5ca2ad4c`  
**Artifact size:** `1084579` bytes  
**Published profile SHA-256:** `8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5`  
**Profile identity:** `LC V1 S1.42AK-BMAFR1`  
**Publication PR:** `#218`  
**Successful publication transport run:** `36987697299` (run `2`) — success  
**Exact materialization commit:** `780b4c3766cd398e8181d15bdb4160b1366eeb11`

The profile at `Profiles/LC V1 S1.42AK-BMAFR1.r2z` and the readable snapshot at `ProfileSources/S1.42AK-BMAFR1/` were copied byte-for-byte from frozen Actions artifact `11218000891`. No profile, diagnostic DLL, package, config source or gameplay component was rebuilt during publication.

Before materialization, the successful one-shot publication transport re-downloaded artifact `11218000891` and revalidated the exact artifact ZIP digest and exact profile digest. It also revalidated the 337-member archive contract, byte-exact BMAFDIAG1 diagnostic DLL reuse, accepted S1.42AB InteriorWeightNormalization identity, reviewed LLL 1.7.12 provenance, readable snapshot member/index identity, Gale path-length budget, controller boundary and the repaired raw Foundry owner-binding contract.

The repaired raw Foundry contract remains exact:

- exactly one visible-equivalent `Custom Dungeon:  Abandoned Foundry` section;
- that exact section begins with exactly nine U+200B sorting characters;
- no plain zero-U+200B visible-equivalent Foundry section exists;
- `Enable Content Configuration = true`;
- `Black Mesa:100` occurs exactly once in the preserved Manual Level Names mapping;
- all other reviewed Foundry owner values remain preserved;
- diagnostic DLL SHA-256 remains `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`;
- accepted normalizer SHA-256 remains `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- reviewed LLL 1.7.12 provenance remains SHA-256 `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- canonical projected critical runtime paths remain `217 / 219` under the `255`-character budget.

Relative to exact accepted S1.42AK SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`, the reviewed/publication contract remains:

- archive members: exactly `337`;
- added members: exactly `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`;
- removed members: none;
- changed existing members: exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- package changes: `0`;
- config changes: `1`;
- diagnostic DLL rebuilt during publication: no.

`ProfileSources/S1.42AK-BMAFR1/FILE_INDEX.json` remains the reviewed 337-row archive index. No `PROFILE_INDEX_RESULT.json` exists at this publication gate and `Profiles/EXPECTED_HASHES.json` has not been changed; profile-index mapping/reconciliation is intentionally a later bounded lifecycle step.

The first transport attempt, run `36987635092` / #1, failed closed before materialization because the temporary publication validator incorrectly expected the LLL DLL as an embedded profile member. No publication bytes were written by that failed attempt. The temporary validator was corrected to verify the reviewed LLL provenance from artifact evidence, and run `36987697299` / #2 then passed all publication checks and materialized the exact frozen bytes.

Publication leaves `BuildSpecs/current.json`, `Current/AUTO_BUILD_RESULT.*` and `RuntimeInbox/ACTIVE_BUILD.txt` unchanged. S1.42AK remains accepted. S1.42AK-BMDSFIX1 remains the active gameplay candidate / **NOT ACCEPTED** with its regular Black Mesa x `DeepSewersFlow` qualification passive, outstanding and unwaived. BMAFDIAG1PATH1 remains immutable failed diagnostic provenance / **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT**. BMAFR1 is not indexed, not Gale-imported, not runtime-armed and not a gameplay/acceptance candidate. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; no gameplay run is authorized by this publication checkpoint.
