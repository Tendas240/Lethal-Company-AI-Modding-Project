# Universal Interior Viability / Equal Availability Investigation Plan

**Status:** SELECTED / PHASE A + B1 + B2 + B3 + C1 COMPLETE / PHASE C2 OWNER-HARD-BLOCK REASON ANALYSIS OUTSTANDING / NOT IMPLEMENTED / NOT ARMED  
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

### Phase B1 — moon universe and first observed row

**COMPLETE.** Authority: `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`.

Exact S1.42AK establishes:

- 32 Dawn moon assets;
- 31 LLL ExtendedLevels: 13 Vanilla, 16 Custom, 2 External;
- `lethal_company:test` is Dawn-only and excluded from the selection matrix;
- `71 Gordion` is retained in the moon inventory but excluded from interior-pairing cells because exact runtime identifies it as `CompanyBuildingLevel` with `CompanyMoonRouteConfirmCommand`;
- 30 pairing-target moons remain: 12 Vanilla, 16 Custom, 2 External;
- with 53 LLL-selectable interiors, the matrix contains **1,590 pairing cells**;
- exact S1.42AK Offense runtime accounts for all 53 interiors: 41 `VIABLE_EQUAL_100`, 12 currently `NOT_YET_PROVEN` pending owner-cause analysis.

### Phase B2 — owner/config mechanism extraction

**COMPLETE.** Authority: `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`.

Every selectable interior now has an availability-owner mechanism:

- 22 `DIRECT_LLL_UNIVERSAL_TAG_OVERRIDE` flows with actual active `Vanilla:100,Custom:100`;
- 27 `OWNER_ASSET_MATCHING_NO_DIRECT_LLL_CONFIG` Custom flows;
- 3 `VANILLA_NATIVE_LLL_MATCHING` flows;
- 1 `DAWNLIB_NATIVE_BLACK_MESA_WEIGHT_RULE` flow.

Current JLL configs contain no dungeon injection, moon-weight, rarity, Level Names, Level Tags or Route Price availability controls; they remain auxiliary behavior configs rather than a separate availability owner.

Exact S1.42AK Offense is fully cause-classified at 41 `VIABLE_EQUAL_100` + 12 `AUTHOR_OR_OWNER_HARD_BLOCK`. Those 12 labels mean current owner-metadata rejection before normalization, not proven technical incompatibility. Shatteredrooms × Experimentation and × Embrion are also explicit owner hard blocks until a technical reason is established.

### Phase B3 — matrix materialization

**COMPLETE.** Authority: `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`; complete 1,590-cell machine matrix: `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.csv`.

Current matrix totals:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

The 22 direct LLL `Vanilla:100,Custom:100` flows plus Black Mesa's native `lethal_company:vanilla/custom` rule establish 23 equal-weight interiors on every Vanilla/Custom target moon. Exact Offense runtime establishes the complete 41 viable + 12 owner-hard-block row. Shatteredrooms × Experimentation and × Embrion are the two additional explicit owner hard blocks. The two External target-moon rows remain fully unproven because the broad Vanilla/Custom rules are not extrapolated onto them.

A `VIABLE_EQUAL_100` cell is current availability/effective-weight evidence, not generation/traversal compatibility proof.

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

### Phase C1 — existing runtime compatibility triage

**COMPLETE.** Authority: `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`.

Conservative repository-native mining of runtime-pass / accepted / accepted-focused evidence plus the explicitly authorized LC Office DIAG2 A/B establishes:

- **15** current selectable interiors with actual Offense generation plus recorded player enter/exit;
- **4** additional interiors with actual Offense generation, tile preparation and four PathfindingLib entrance connections but no recorded player entry;
- **34** interiors with no positive actual-generation proof in the conservative trusted scan.

All C1 observed generation is on **Offense**. This reduces interior-side uncertainty but does not prove moon-side entrance compatibility on the other 29 target moons and does not change the Phase-B3 availability matrix.

C1 also preserves unresolved route/NavMesh proof obligations rather than promoting them to technical restrictions. Notable signals include Spooky manor and Expanded Mineshaft B-side route reachability gaps, LiminalHouse/Rubber Rooms route or NavMesh ambiguity, and known LC Office/DeepcoreMines generation-time NavMesh noise.

### Phase C2 — owner-hard-block technical reason extraction

Reconcile the **14 current `AUTHOR_OR_OWNER_HARD_BLOCK` cells** before proposing any removal. Determine from current package/config/source evidence whether each exclusion is:

- an explicit technical/compatibility safeguard;
- author balancing/default targeting with no proven technical necessity;
- or an unexplained owner exclusion.

The C2 starting set is the 12 Offense owner-rejected flows plus Shatteredrooms × Experimentation and Shatteredrooms × Embrion. Do not authorize a build or runtime test until the owner reason is understood well enough to design the narrow proof.

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

Execute **Phase C2 owner-hard-block technical reason extraction** using `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md` plus the Phase-B2/B3 owner and matrix authorities. Start with the 12 Offense owner-rejected flows and Shatteredrooms × Experimentation/Embrion. Classify a block only where repository package/config/source evidence proves its reason.

No universal override, gameplay build or runtime test is authorized yet.
