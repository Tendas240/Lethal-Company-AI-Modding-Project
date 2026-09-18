# Universal Interior Viability / Equal Availability Investigation Plan

**Status:** SELECTED / PHASE A INVENTORY COMPLETE / PHASE B MATRIX OUTSTANDING / NOT IMPLEMENTED / NOT ARMED  
**Date:** 2026-09-18  
**Accepted baseline:** S1.42AK — `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z` / `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Topic authority:** `Knowledge/INTERIORS_AND_LLL.md`  
**Lifecycle authority:** `Current/CURRENT_STATE.json`

## Objective

Reach the project's long-term interior-selection target: every registered interior should be available on every gameplay moon with equal effective probability whenever that pairing is technically safe.

This investigation does **not** authorize a universal override yet. It must first prove which flows are currently registered, who owns their viability rules, which moon/flow pairings are absent, and whether any restriction is technically necessary.

## Already accepted architecture

S1.42AB remains the accepted equality mechanism:

1. LethalLevelLoader determines the viable dungeon pool first.
2. The project-local normalizer runs after that viability decision.
3. Every positive rarity returned by LLL is normalized to exactly `100`.
4. The patch does not add, remove, register or deduplicate dungeon flows.
5. Native/JLL/DawnLib ownership is not replaced by duplicate LLL registration.

Therefore the unresolved problem is **availability/viability**, not weighting after viability.

## Current S1.42AK baseline observations

Exact accepted S1.42AK contains `ProfileSources/S1.42AK/BepInEx/config/LethalLevelLoader.cfg`.

Repository-native extraction from that file shows:

- **28** `Custom Dungeon` configuration sections;
- **27/28** use `Enable Content Configuration = true`;
- those same 27 sections use `Dungeon Injection Settings - Dynamic Level Tags List = Vanilla:100,Custom:100`;
- **Black Mesa** is the only one of the 28 with `Enable Content Configuration = false`; its owner path remains native/DawnLib and must not be duplicate-registered merely to force availability.

This is only an LLL-config-section inventory, not yet the authoritative complete registered-flow inventory. Historical S1.42A evidence reported **52 total dungeon flows**, while accepted/later Offense runtime normalization evidence exposed viable pools of roughly **40-41** entries. Those counts must be reconciled against current S1.42AK rather than treated as interchangeable.

Known restriction/qualification examples already preserved by current authority:

- Shatteredrooms explicitly excludes **Experimentation** and **Embrion**; the restriction remains until its technical reason is proven safe to remove.
- LC Office is proven viable on **Offense**, but universal-moon availability is not yet proven.
- Art Gallery and Rubber Rooms are proven registered and viable on Offense at final effective rarity `100`.
- Black Mesa is single-registered through its own owner path and already receives final effective `100` when viable.

## Phase A — authoritative current inventory

**COMPLETE.** Authority: `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`.

Exact reconciliation:

- 55 DawnLib-registered DungeonFlow assets;
- 53 LLL ExtendedDungeonFlow selection entries: 3 Vanilla, 49 Custom, 1 External Black Mesa;
- two additional Dawn-only vanilla assets: `Level1FlowExtraLarge` and `Level1Flow3Exits`;
- exact S1.42AF pre-LC inventory: 52 LLL entries;
- exact S1.42AK delta: `LC Office / OfficeDungeonFlow`;
- 28 LLL `Custom Dungeon` config sections are non-cardinal;
- only 22 unique current Custom flows have active direct LLL config coverage;
- three enabled sections are aliases and two are stale/orphaned;
- 27 current Custom flows therefore remain governed by owner/author matching data rather than a direct project LLL config override;
- no separate JLL-only registered dungeon flow was found in the exact current Dawn/LLL inventories.

Registration proof is not treated as generation/traversal proof.

## Phase B — moon/flow viability matrix

For every current gameplay moon and every registered flow, classify the pairing as one of:

- **VIABLE_EQUAL_100** — pairing is currently viable and reaches effective rarity `100`;
- **CONFIG_GAP** — owner supports the pairing but current project configuration does not inject it;
- **AUTHOR_OR_OWNER_HARD_BLOCK** — the content owner rejects the pairing before normalization;
- **KNOWN_TECHNICAL_RESTRICTION** — a documented geometry/generation/route constraint exists;
- **NOT_YET_PROVEN** — repository evidence is insufficient.

The matrix must distinguish vanilla and custom moons and must not infer universal safety merely from the presence of `Vanilla:100,Custom:100`.

## Phase C — compatibility proof for proposed restriction removal

Before changing any absent pairing, establish the narrow owning mechanism and prove compatibility relevant to that interior:

- correct main entrance / fire-exit or equivalent entrance pairing;
- no entrance/exit mismatch or stranded teleport target;
- dungeon generation completes without exhausted retries or fatal errors;
- entrance and normal traversal are possible;
- door/socket geometry is valid;
- no severe clipping or inaccessible required geometry;
- elevators/ladders/special traversal work where present;
- routing and NavMesh remain usable enough for normal gameplay;
- no duplicate dungeon registration is introduced.

High-risk or explicitly blocked pairings require targeted runtime proof before their restriction is removed.

## Phase D — candidate rule

Only after Phases A-C identify safe changes may a gameplay candidate be authored.

A future candidate must:

- derive from exact accepted S1.42AK or a later accepted baseline;
- preserve the accepted S1.42AB normalizer unchanged unless evidence proves a defect in it;
- use the owning system's supported configuration/registration route;
- avoid duplicate registration;
- retain any technically unavoidable exception explicitly in canonical documentation;
- keep every successfully viable flow at effective rarity `100`.

## Scope boundaries

Do not combine this investigation with:

- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction;
- Black Mesa/Pikmin route recovery;
- LethalEscapeUpdated evaluation;
- AdditionalNetworking repair;
- broader LethalMin teardown/despawn repair;
- unrelated enemy, scrap or item tuning.

Black Mesa **availability/registration ownership** is in scope only as required for the universal viability matrix; its Pikmin routing defect remains a separate deferred scope.

## Decision gate

No build or runtime test is armed at scope selection.

The next repository decision must be based on the completed owner/flow/moon matrix:

1. if all currently absent pairings are simple supported configuration gaps, design the narrow configuration candidate;
2. if hard blocks exist, research/inspect their owning implementation and target only those whose safety can be proven;
3. if a restriction is technically necessary, preserve it as an explicit documented exception rather than masking it with duplicate registration or unsafe patches;
4. if current configuration already provides universal safe availability for a flow, leave it unchanged.

## Exact next action

Build the **Phase-B moon/flow viability matrix** from `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md` plus current owner/runtime evidence. Classify every current selectable moon/flow pairing as `VIABLE_EQUAL_100`, `CONFIG_GAP`, `AUTHOR_OR_OWNER_HARD_BLOCK`, `KNOWN_TECHNICAL_RESTRICTION`, or `NOT_YET_PROVEN`.

No build or runtime test is authorized yet.
