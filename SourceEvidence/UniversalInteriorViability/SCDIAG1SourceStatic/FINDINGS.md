# S1.42AK SCDIAG1 Storage Complex Source/Pure-Static Findings

**Date:** 2026-10-08
**Status:** SOURCE IMPLEMENTATION STAGED / EXACT-PR-HEAD CI PENDING / DIAGNOSTIC ONLY / NEVER ACCEPT
**Authorization:** `Current/342_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`
**Implementation base:** `d2b0db1108a52a3e3b088433fd5e16593e537d71`

The separately authorized independent `S1.42AK-SCDIAG1` source is staged with GUID `tendas.lethalcompany.s142akscdiag1`, project `S142AKSCDiag1`, marker `[SCDIAG1]`, version `1.0.0` and **future, not published** profile identity `LC V1 S1.42AK-SCD1`. It is classified **DIAGNOSTIC ONLY / NEVER ACCEPT**.

Exactly one Harmony postfix on `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` uses `Priority.Last` after the accepted S1.42AB normalizer. Fail-closed dependency GUID/version/hash checks, exact reflection and body/signature checks, normalizer-postfix presence/order, server-RPC caller and terminal simulation exclusion, Offense-only moon, and identity checks precede any list reduction. Only an already-viable matching `ExtendedDungeonFlow.DungeonName == "Storage Complex"` with Unity `DungeonFlow.name == "StorageComplex"` and effective rarity `100` is selected by existing object reference. Source follows the previously validated FXDIAG1 pattern without modifying or activating FXDIAG1.

SCDIAG1 additionally rejects duplicate references and duplicate dungeon-name / asset identities anywhere in the returned pool, wrong case, mismatched name/asset aliases, zero or negative rarity, and read-only or fixed-size lists. The pure tests check successful reference-preserving selection, caller/moon/simulation inertness and a wide range of negative inputs while preserving original input identity/order on any refusal. Runtime reflection dependencies, actual Harmony order and plugin startup refusal must remain independently verified by later runtime evidence; pure tests cannot simulate actual BepInEx/Harmony startup. A dedicated head-pinned PR workflow runs pure tests, compiles plugin source only and enforces deterministic source/controller checks.

**No PR-head success is claimed in this staged document.** A passing source/static workflow is evidence only of source and policy, **not** a review-build/profile/packaged DLL, publication, Gale import, activation, target generation, gameplay safety or acceptance. A later independent integration segment must first verify all mandatory CI on the final exact source PR head, then merge with expected head and verify permanent main-head push CI.

The Offense Storage Complex actual-generation/materialization and observed PathfindingLib relationships remain unproven. Phase C residual remains **23 = 11 viable/equal-100 + 12 unchanged owner-hard-block**. Baseline S1.42AK accepted; BMDSFIX1 active **NOT ACCEPTED**, passive Black Mesa x DeepSewersFlow gate unwaived. Controllers remain idle and runtime points to BMDSFIX1. Current/312's unresolved 2,547-array-error attribution, inherited LethalMin/SoundAPI boundaries and Oxyde, Shatteredrooms/CullFactory, BCMER x all Pikmin, Herobrine/BMAFR1I1 workstreams remain separate.
