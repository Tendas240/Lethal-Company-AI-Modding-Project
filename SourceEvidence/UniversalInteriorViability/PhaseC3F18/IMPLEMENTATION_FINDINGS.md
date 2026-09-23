# C3F18 — BMGHDIAG2 Source / Static Implementation Findings

**Status:** SOURCE IMPLEMENTED / SOURCE CI PENDING / NOT BUILT / NOT PUBLISHED / NOT RUNTIME-ARMED  
**Date:** 2026-09-23  
**Accepted baseline:** S1.42AK — unchanged  
**Design authority:** `SourceEvidence/UniversalInteriorViability/PhaseC3F18/FINDINGS.md`  
**Successor plan:** `BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md`

## Implemented bounded repair

Added a separately versioned `Patches/S142AKBMGHDiag2/` successor. The predecessor BMGHDIAG1 bytes are untouched and remain failed runtime evidence only.

The startup provenance repair is isolated from gameplay hooks:

- installed game source provenance hashes exactly `Path.Combine(Path.GetFullPath(Paths.ManagedPath), "Assembly-CSharp.dll")` through `GameAssemblyProvenance`;
- no recursive search, guessed Steam path, current-directory fallback, `Assembly.Location` or `CodeBase` is used for the game binary;
- loaded `EntranceTeleport` identity is checked separately through exact type name, declaring assembly simple name, non-dynamic assembly, manifest module `Assembly-CSharp.dll`, exact declared `TeleportPlayer()` shape/body, and exact observation fields;
- ordinary plugin dependencies retain their exact version and file-backed DLL SHA-256 gates.

The two Harmony surfaces remain unchanged in responsibility: one post-normalizer Black Mesa Greenhouse selection postfix and one read-only post-native `EntranceTeleport.TeleportPlayer()` observer.

## Pure test coverage

The successor test project ports the predecessor selection/traversal/topology suite and adds fail-closed cases for:

- valid exact managed source file/hash;
- blank managed path;
- missing managed directory;
- exact-file absence with nested same-name file present, proving no recursive fallback;
- wrong installed SHA;
- injected unreadable-file failure;
- exact runtime assembly/type/module identity;
- dynamic/wrong assembly identity rejection;
- exact TeleportPlayer shape and negative method-shape cases.

## Static gate

Added successor-specific source validator and pull-request workflow. They compile/test source only and explicitly require:

- exactly two Harmony patch installations;
- no prefix, transpiler, PatchAll, reflection field writes, manual FindExitPoint or manual TeleportPlayer call;
- game-binary provenance through BepInEx managed path only;
- `Assembly.Location` restricted to ordinary dependency hashing and absent from loaded-game observation identity;
- no BMGHDIAG2 build request;
- `BuildSpecs/current.json` disabled/idle;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`;
- no active candidate and no outstanding runtime test.

CI results are intentionally not claimed until exact-head workflows complete.

## Preserved boundaries

No `.r2z` is built by this checkpoint. No package/config/profile state changes, Gale import, runtime controller transition, B3 change, Black Mesa ownership change, Greenhouse availability change, normalizer change, Shatteredrooms change or Black-Mesa/Pikmin routing change is authorized.
