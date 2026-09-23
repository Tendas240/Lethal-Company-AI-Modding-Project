# S1.42AK-BMGHDIAG1 reviewed-artifact publication verification

- Source PR: #138.
- Reviewed branch head: `f01b6d4f456d3ee133b30ac62f432de75ef3830b`.
- Reviewed PR synthetic merge SHA: `d3ba56820a8bbcf2aca545fd4005ae3f03e90ffa`; it has the same tree as the reviewed branch head.
- Static/build gate: run `35849491391` (#2).
- Review artifact: `S1.42AK-BMGHDIAG1-review-d3ba56820a8bbcf2aca545fd4005ae3f03e90ffa`, artifact ID `10745290545`.
- Artifact ZIP SHA-256: `f34ee6dcf06d2f803159554c1cef2e9f587ca0e38f837f96e287c28c13151947`.
- Published profile SHA-256: `7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90`.
- Published diagnostic DLL SHA-256: `4a1f304a716bf7cacb6496f5047bb0e498ed68bde00fc9f4128fa001adaa30b2`.
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`.
- Accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
- The reviewed profile was revalidated against exact accepted S1.42AK, all 337 FILE_INDEX rows, the exact one-DLL archive delta, package/config stability, diagnostic DLL identity, LLL identity and normalizer identity immediately before publication.
- Separate CI rebuilds are not byte-identical for the locally compiled diagnostic DLL; publication therefore pins these exact reviewed artifact bytes rather than rebuilding.
- `Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged.
- This publication exists on the open C3 PR branch only. It is not merged to `main`, not a current Gale runtime target, not accepted, and not runtime-armed.

Status: `PUBLISHED_STATIC_PASS_NOT_RUNTIME_ARMED`.
