# C3F17.4 — BMGHDIAG1 exact reviewed-artifact publication findings

**Status:** EXACT REVIEWED ARTIFACT PUBLISHED ON C3 PR / STATIC PASS / NOT RUNTIME ARMED

The exact reviewed artifact from build/archive gate run `35849491391` is published byte-for-byte on PR #138 rather than rebuilt. The bound profile SHA-256 is `7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90`; the injected diagnostic DLL SHA-256 is `4a1f304a716bf7cacb6496f5047bb0e498ed68bde00fc9f4128fa001adaa30b2`.

Publication preserves exact accepted S1.42AK as parent and changes only `export.r2x` profile identity metadata plus the single new `BepInEx/plugins/S142AKBMGHDiag1/S142AKBMGHDiag1.dll` archive member. The accepted normalizer, LLL 1.7.12 identity, package state, config state, Black Mesa ownership and Greenhouse availability remain unchanged.

The publication is deliberately PR-local. `Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` remain unchanged. Therefore no candidate is active, no runtime test is outstanding, the canonical Gale helper still resolves S1.42AK from `main`, and no gameplay/Gale action is authorized by this checkpoint.

## Main-integration preflight

Before this publication may be merged to `main`, the exact current PR head must receive a normal CI pass rather than relying on the publication commit's `[skip ci]` marker. This preflight text is intentionally state-neutral and exists to produce that exact-head validation surface. It does not alter the published profile, build result, static verification, diagnostic DLL, accepted S1.42AK baseline, build controller, runtime pointer, matrix, Gale state or runtime authorization.

A later separate atomic main/lifecycle transition may only arm this diagnostic after the exact published profile/build_result/static/publication identities are made visible on `main` consistently with `CURRENT_STATE.selected_scope.diagnostic_revision` and `RuntimeInbox/ACTIVE_BUILD.txt`.
