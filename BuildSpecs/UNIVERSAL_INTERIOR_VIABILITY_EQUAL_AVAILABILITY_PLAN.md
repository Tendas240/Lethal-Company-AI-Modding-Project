# Universal Interior Viability / Equal Availability Investigation Plan

**Status:** SELECTED / BASELINE INVENTORY OUTSTANDING / NOT IMPLEMENTED / NOT ARMED  
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

Build a current S1.42AK inventory containing every registered dungeon flow, not merely every LLL config section.

For each flow record:

- human display name;
- exact runtime/asset flow identifier;
- package/mod owner;
- registration owner: LLL, JLL, DawnLib/native, or another explicit owner;
- whether an LLL `Custom Dungeon` config section exists;
- whether `Enable Content Configuration` is active;
- current manual level-name injection;
- current dynamic tag injection;
- current route-price injection;
- known package/author exclusions;
- existing runtime proof of successful registration/generation.

Reconcile the current total against the historical 52-flow observation and explain every difference.

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

Create the authoritative S1.42AK registered-interior/owner inventory and moon-viability matrix from `ProfileSources/S1.42AK/` plus accepted runtime evidence. Reconcile the 28 LLL custom sections, historical 52-flow count, owner-specific registrations and known exclusions before proposing any build.
