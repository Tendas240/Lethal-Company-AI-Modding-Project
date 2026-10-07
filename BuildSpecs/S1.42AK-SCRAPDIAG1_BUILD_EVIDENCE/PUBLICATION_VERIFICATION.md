# S1.42AK-SCRAPDIAG1 reviewed-artifact publication verification

- Source implementation PR: #127; merged implementation commit `b9a949ec1c5b1bde5bcd059fb82f7791bc59225b`.
- Primary static/build gate: run `35383680389`; reviewed implementation head `758816b6ce09a3406f256b1a9376ccb66d996afa`.
- Exact pinned review artifact: `S1.42AK-SCRAPDIAG1-review`, artifact ID `10563033130`.
- Artifact ZIP SHA-256: `08c676c2a0f9c7a3df3a0cd58854dbcc0b53ba21dd514a7c7d661cfcfe231bc3`.
- Published diagnostic profile SHA-256: `233bcc058a3fa95d63e0577c4ff74b5a0dc137db49757b50376e447dd082d3b1`.
- Published AJDIAG1 selector DLL SHA-256: `51d8927838f003f8ea00d69942d21dda3937d46c0cff5b220e99651c3a61a191`.
- Published scrap-placement logger DLL SHA-256: `f1c0b7450d60b8c0400c342779abcae8dfb11c34d9112d2e945a02349610df7b`.
- Accepted S139 Compatibility Fixes remains byte-identical at `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`.
- Accepted Interior Weight Normalization remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
- Member-by-member verification proves zero changed existing members, zero removed members and exactly two added members:
  - `BepInEx/plugins/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.dll`;
  - `BepInEx/plugins/S142AKDiagScrapPlacement/S142AKDiagScrapPlacement.dll`.
- Exact-artifact publisher run: `35386344614` / publisher run #4 — **SUCCESS**.
- Atomic exact-profile publication commit: `d7a1ff76c6a9a2301f1bb19d87c3309b4a9d0df5`.
- The publisher revalidated the original Actions artifact ID/run/name/digest before download, revalidated the exact S1.42AK base SHA, exact output SHA, exact DLL hashes, exact archive delta and every `FILE_INDEX` member against the published `.r2z`.
- The original review-artifact upload used the default `include-hidden-files: false`. Consequently its readable snapshot omitted the hidden text snapshot `BepInEx/config/.LCMaxSoundsFix.cfg` even though the exact `.r2z` and `FILE_INDEX` both contained that unchanged member. Publication reconstructed only that hidden readable snapshot from the already SHA-verified diagnostic archive bytes; no profile/archive bytes were changed or rebuilt.
- Publisher runs #1-#3 failed closed before any artifact commit while tightening path/snapshot checks. They published no profile bytes.
- `Current/AUTO_BUILD_RESULT.*` and `BuildSpecs/current.json` remain bound to accepted S1.42AK. Publication itself does not promote or accept the diagnostic.

**Publication status:** exact pinned S1.42AK-SCRAPDIAG1 artifact is repository-published. Runtime activation is a separate state transition.
