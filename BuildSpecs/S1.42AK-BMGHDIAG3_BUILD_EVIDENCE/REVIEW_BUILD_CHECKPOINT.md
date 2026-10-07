# S1.42AK-BMGHDIAG3 Review Build Checkpoint

**Date:** 2026-09-27  
**Status:** REVIEW BUILD PASS / ACTIONS ARTIFACT ONLY / NOT PUBLISHED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT

## Exact reviewed provenance

- Review PR: `#182`
- Reviewed source/build head: `4462ced77519b34f6d55181fc33692b298434833`
- PR merge ref used by Actions: `cd1b684b4aa7bcdc68789e6edd1d8c99cffab2bb`
- Review workflow: `S1.42AK BMGHDIAG3 inactive review-build archive-delta gate`
- Review run: `36311706288`
- Run number: `1`
- Exact-head Knowledge Architecture: `36311706234` / `#809` — success
- Actions artifact ID: `10929208327`
- Artifact name: `S1.42AK-BMGHDIAG3-review-cd1b684b4aa7bcdc68789e6edd1d8c99cffab2bb`
- Artifact ZIP SHA-256: `20f616e85585e10631c31e09844a27bb6bb7649843a98655ed70e37b89152198`

The downloaded final Actions artifact was independently rehashed. Its ZIP digest matched GitHub artifact metadata, and the contained review profile, BMGHDIAG3 DLL and accepted normalizer were independently recomputed and matched the gate output.

## Exact reviewed identities

- Exact accepted S1.42AK direct parent SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`
- BMGHDIAG3 review profile SHA-256: `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`
- BMGHDIAG3 DLL SHA-256: `d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352`
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`
- Accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

## Exact archive delta

The reviewed profile contains `337` archive members.

Relative to exact accepted S1.42AK:

- added members: exactly `BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll`;
- removed members: `0`;
- only changed existing member: `export.r2x`;
- the `export.r2x` change is limited to profile identity metadata;
- package changes: `0`;
- config changes: `0`;
- accepted normalizer bytes: unchanged;
- freshly compiled BMGHDIAG3 DLL and injected review-profile DLL: byte-identical.

The separate policy-test harness passed the preserved physical provenance, runtime type/assembly/method, exact Greenhouse selection, traversal coverage and topology contracts. The disproven BMGHDIAG2 `ManifestModule.Name == "Assembly-CSharp.dll"` refusal is not part of the successor contract and was not reintroduced.

## Integration verification

PR `#182` merged to `main` at:

`e08f0225de8441c13395b9a8a9157ec640673a37`

Permanent exact-main Knowledge Architecture gate:

- run `36312331849`;
- run number `810`;
- event `push`;
- head SHA `e08f0225de8441c13395b9a8a9157ec640673a37`;
- result **success**.

## Preserved lifecycle/controller state

This review checkpoint is state-neutral:

- accepted gameplay baseline remains `S1.42AK`;
- active gameplay candidate remains `S1.42AK-BMDSFIX1` / not accepted;
- the regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and passive;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- BMGHDIAG3 is not published, Gale-imported, indexed, runtime-armed or gameplay-authorized;
- Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

## Acceptance boundary

BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**. A successful inactive review build proves compiler/policy/archive validity only. It is not runtime evidence and cannot itself prove Black Mesa x Greenhouse compatibility or alter BMDSFIX1 acceptance.

## Next bounded gate

After canonical lifecycle reconciliation, the next possible gate is a separately bounded **S1.42AK-BMGHDIAG3 exact-byte publication checkpoint** that materializes only the exact reviewed profile bytes SHA-256 `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace` from Actions artifact `10929208327` and independently revalidates those bytes.

That publication checkpoint must not rebuild the diagnostic, import or modify Gale, change `RuntimeInbox/ACTIVE_BUILD.txt`, enable/repoint `BuildSpecs/current.json`, arm runtime, start gameplay, or claim Black Mesa x Greenhouse qualification.
