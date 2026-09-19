# S1.42AK universal interior viability — Phase C3B Dawn → LLL bridge checkpoint

**Status:** PARTIAL C3 EVIDENCE / BRIDGE TAG PROPAGATION RESOLVED / NO GAMEPLAY BUILD OR RUNTIME AUTHORIZATION
**Date:** 2026-09-19
**Repository source commit:** `56355ff518ae4301a38d370be9561251f6f963c1`
**Parent checkpoint:** `SourceEvidence/UniversalInteriorViability/PhaseC3A/FINDINGS.md`
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Result

LethalLevelLoader 1.7.12 has an explicit DawnLib compatibility bridge for moons. For every eligible non-vanilla Dawn moon it creates an `ExtendedLevel`, sets `ContentType = External`, seeds the LLL tag list with `Custom`, copies the Dawn tag list into LLL tag names, and registers the result under an LLL `ExtendedMod` derived from the Dawn namespace.

This resolves the key C3A bridge gap: **LLL's `External` category is not mutually exclusive with LLL's `Custom` matching tag.** In the 1.7.12 bridge, Dawn-backed External levels are explicitly given the LLL `Custom` tag.

For the two exact S1.42AK target moons, C3A already proved from the SHA-256-bound DawnLib 0.9.25 DLL that `black_mesa:black_mesa` and `code_rebirth:oxyde` are non-vanilla Dawn keys, receive Dawn's automatic `lethal_company:custom` tag, and receive Dawn's universal `lethal_company:all` tag. The LLL bridge independently seeds `Custom` and copies Dawn tags by their key component, so the bridge guarantees at least:

- Black Mesa: LLL `Custom`, LLL `All`;
- Oxyde: LLL `Custom`, LLL `All`.

Additional owner-supplied Dawn tags can also reach LLL, but this bridge-only segment does not enumerate them. The bridge takes the Dawn tag's key component and discards the namespace before converting underscore-separated words to LLL PascalCase. `Vanilla` is not guaranteed by the automatic non-vanilla path; this checkpoint does not claim it is absent from every possible owner-supplied final tag list.

## How External ExtendedLevels arise

The pinned 1.7.12 release source shows the following setup chain:

1. LLL initializes vanilla and custom ExtendedContent.
2. If DawnLib is present, LLL invokes `RegisterDawnExtendedLevels()` during initial setup.
3. That method iterates `LethalContent.Moons.Values`, skipping null entries, Dawn-vanilla keys, and entries tagged `dawn_lib:is_external`.
4. For each remaining Dawn moon it creates an `ExtendedLevel` from the Dawn `SelectableLevel`, carries over route assets/price and scene names, disables LLL automatic moon configuration, and calls `RegisterDawnExtendedContent()`.
5. `RegisterDawnExtendedContent()` removes any prior vanilla registration if necessary, sets `ContentType = External`, assigns `[Custom]` as the starting ContentTags list, copies Dawn tags, creates/reuses an ExtendedMod for the Dawn namespace, and registers the ExtendedLevel there.
6. LLL then populates its content dictionaries and later binds configuration. External levels are included in `PatchedContent.CustomExtendedLevels`, while `PatchVanillaLevelLists()` deliberately excludes `ContentType.External` from LLL's rewritten base-game level list to avoid duplicate injection because Dawn remains the owner.

The accepted S1.42AK runtime listing of Black Mesa and 745 Oxyde as `External` is consistent with this exact bridge path.

## What reaches LLL

`CopyContentTags()` enumerates Dawn `AllTags()`. For each `NamespacedKey`, LLL takes only `.Key`, converts it to LLL's PascalCase tag format, and calls `TryAddTag()`. Because `RegisterDawnExtendedContent()` seeds `Custom` first, the Dawn `lethal_company:custom` copy is naturally deduplicated.

C3A's exact Dawn binary establishes that `AllAutoTagger` always applies and `CustomAutoTagger` applies to non-`lethal_company` keys. Therefore the current target moons have a bridge-backed minimum LLL tag set of `Custom` + `All`. This is stronger than the earlier inference from the `External` inventory label alone.

## Selection-layer availability now supported

Phase B2 canonically established **22** current interiors with `DIRECT_LLL_UNIVERSAL_TAG_OVERRIDE` and the active setting `Vanilla:100,Custom:100`.

LLL 1.7.12 `LevelMatchingProperties.GetDynamicRarity()` compares those configured level-tag rarities directly against the target ExtendedLevel's `ContentTags`; `DungeonManager` retains a dungeon flow when the resulting rarity is non-zero. Because both External target moons are guaranteed to carry LLL `Custom`, each of those 22 direct flows matches each External moon at rarity `100`.

That yields **44 selection-layer pairings** (22 flows × Black Mesa/Oxyde) supported as `VIABLE_EQUAL_100` under the existing matrix definition. S1.42AB remains the accepted post-viability normalizer, so positive viable entries have final effective rarity 100.

`PROPOSED_SELECTION_AVAILABILITY_DELTA.csv` records exactly those 44 currently-`NOT_YET_PROVEN` cells. The authoritative B3 matrix itself is intentionally not rewritten in this intermediate source checkpoint; C3 still has owner/native-rule and topology segments outstanding, and this draft PR has not been merged to main.

## Proof boundary

This checkpoint proves LLL bridge construction, tag propagation semantics and the resulting direct-LLL **selection availability**. It does **not** prove:

- actual generation of any of the 44 pairings;
- main-entrance/fire-exit IDs or pairing;
- scene topology, traversal, geometry, elevators, ladders, routing or NavMesh;
- the 27 owner/asset-matched interiors on either External moon;
- Facility/Haunted Mansion/Mineshaft native matching on either External moon;
- Black Mesa's Dawn-owned dungeon selection rule on either External moon.

The LLL part of this checkpoint is pinned to the upstream `Release v1.7.12` source commit and exact Git blob SHAs. Unlike the Dawn C3A evidence, the accepted LLL package DLL is not SHA-256-bound in current repository evidence. That qualification is preserved in `LLL_DAWN_BRIDGE_SOURCE.json`; no unqualified binary-identity claim is made.

## Required next bounded analysis

Continue C3 with exact owner evidence for `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior` 3.4.4 and `XuXiaolan-CodeRebirth` 1.6.9. Establish their moon registration metadata, additional tags, scene identities and entrance/fire-exit information, then trace the relevant native selection rules only as far as needed for the still-unresolved External-moon cells.

Do not duplicate-register Black Mesa, do not alter Shatteredrooms exclusions, and do not convert selection availability into a generation/traversal claim.

## Checkpoint decision

Phase C3 remains open. No gameplay/config/controller bytes are changed. S1.42AK remains accepted, no Candidate or runtime test is created, and the existing S1.42AB normalization architecture remains unchanged.
