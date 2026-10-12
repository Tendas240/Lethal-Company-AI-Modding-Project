# GoldenHotel / Goldstay Hotel — Original serialized-asset evidence reconciliation

**Status:** PR-STAGED / STATIC ORIGINAL-ASSET EVIDENCE ONLY / NOT GENERATION PASS.
**Source:** original locked `BLB_Thunderstore_Mods_LOL-Lead_Interiors` version `0.0.7`, exact original Actions capture from PR #453, workflow run `38302364814`, artifact ID `11770647482`.
**Main integration prerequisite:** PR #453 merged as `99fa9f33564c607bb8ae30e64b868d75ac4a64fa`; permanent exact-main Knowledge Architecture `38304029346` / #1657 passed.
**Independent JSON:** `GOLDENHOTEL_CAPTURE.json`, **6,657 bytes**, SHA-256 `fe92fe0767fe3789d6c53ece6d0fe8768c3275c117cd52216eaeebfc678e6bef`, byte-equal to the sole member of the downloaded Actions artifact ZIP.
**Provenance:** `CAPTURE_PROVENANCE.json` in this directory.

## Strict original-package identity

The capture preserves the historical `SourceEvidence/UniversalInteriorViability/PhaseC3OwnerMatching/PACKAGE_LOCK.json` in full, including its original Lead flow list `BellevilleApp`, `CrimsonKeep` (which is *not* extended with `GoldenHotel`). The original ZIP is 208,890,187 bytes at SHA-256 `0e605a7280b3c14d52049c5b42c7a85d3001dc98a7fa61f5822364686d13e16b`; the single UnityFS member `BepInEx/plugins/boomsinterior.lethalbundle` is 208,728,335 bytes at SHA-256 `bf3ddb70d42084c5847a1038abffb759956fe3e9cb4cfc1bbb657b746a14895b`. The locked full ZIP inventory has five members. Original upstream ZIP/member were verified by the reviewed original-byte Capture CI; this later independent reconciliation re-hashed the downloaded JSON, **not** the 208MB original ZIP a second time.

Accepted authority-file SHA-256: `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md` = `80f7b57c09defa48ab99444dfd8d0e1091fa32781e3dc5e44df225d440471fe0`; `ProfileSources/S1.42AK/export.r2x` = `19935c1afc98de1562fda8b299d7d23d09c3555eac88f9de7992eb3d6e2b46b8`. The Capture runner used Python 3.11.17, UnityPy 1.25.3, PyYAML 6.0.2 and exact original PR-Head `93582c2844ad08c483fb4205fc702a84c7ecf5dd`.

## Original serialized object graph (one CAB; one original UnityFS bundle)

All three descriptors refer to `CAB-38a1e9912a4e0bf00320c85779ae5f69`, to the exact original `BepInEx/plugins/boomsinterior.lethalbundle`, and to MonoBehaviour objects with verified original raw-object SHA-256 values.

| Asset and class | Original signed path ID | Original raw-object SHA-256 |
|---|---:|---|
| `GoldenHotel` — `DunGen.Graph.DungeonFlow` | `-8301055780377321559` | `f6336d3ed6bb7a81a5d74e454bbb64d552d8cc42c8420678569a5b8e409efc70` |
| `GHExtended` — `LethalLevelLoader.ExtendedDungeonFlow` | `-604959431411346682` | `b704e9a255147183f2a44bb7822d95cd03e6d367e1a6ab68a3aa6094ac1ccea6` |
| `GHMatchingProperties` — `LethalLevelLoader.LevelMatchingProperties` | `-7406144614243962228` | `b7c54c3d15bb181ed4f751d41e6de9b65a555644ac02c2b6953337a40c3ce75e` |

The owner has exact display `DungeonName = Goldstay Hotel` and mandatory original serialized pointer fields `<DungeonFlow>k__BackingField` and `<LevelMatchingProperties>k__BackingField`, which the original probe resolves to the same original identified flow and matching objects. The JSON retains the **field names**, not the raw backing-field pointer numeric values: do not claim independent reproduction of the raw owner pointer bytes solely from this JSON.

The original matching asset has tags `Canyon:20`, `Desert:5`, `Valley:15`, `City:45`, `Taiga:10`, `Tundra:10`; eight planet-name entries (`Assurance:5`, `Vow:15`, `March:5`, `Adamance:20`, `Titan:75`, `Malice:15`, `Kronodile:300`, `Revenant:20`). `currentRoutePrice` and `currentWeather` are empty. The only non-script matching-asset direct-reference inventory entry is the original null `m_GameObject` pointer. The `m_Script` pointer is script metadata, not a missing matching-content pointer.

## Evidence tier and next action

**Accepted here for subsequent integration consideration:** the independently re-hashed, unchanged derived JSON as **STATIC_SERIALIZED_ORIGINAL_ASSET_ONLY / NOT_GENERATION_PASS**, with exact captured original identity and explicit original acquisition provenance. This does **not** establish dynamic runtime owner/managed-instance identity, generation, CullFactory, entrance relationship, player traversal, NavMesh or equal selection probability. It is neither a source safety waiver for CKDIAG1 nor permission to modify owner matching or selector behavior.

Offense residual **21 = 9 VIABLE_EQUAL_100 actual-generation proof gaps (including GoldenHotel) + 12 unchanged OWNER_HARD_BLOCK cases**. No residual reduction, gameplay acceptance or all-moons closure. `S1.42AK` alone ACCEPTED; `S1.42AK-BMDSFIX1` active/NOT ACCEPTED with passive selector-free Black Mesa x `DeepSewersFlow` gate outstanding/unwaived. TSDIAG1 remains inactive/NEVER ACCEPT. Build controller disabled/IDLE; runtime controller BMDSFIX1.

**Next separated gate after evidence PR exact-final-head CI:** independently authorize a pinned-head merge and verify permanent exact-new-main Knowledge Architecture CI. Only afterward decide on the next narrow GoldenHotel generation-proof *method/safety prerequisite*, not automatic selector construction, build, Gale import or runtime attempt. Historical C3 captures, package lock and provenance must remain byte-identical, and no independent roadmap scope may displace Interior-first completion.
