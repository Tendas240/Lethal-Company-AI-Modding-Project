# C3F6 — Black Mesa row GlobalProp 1231 evidence-availability inventory

**Status:** REPOSITORY-HELD COVERAGE INVENTORIED / 23 CURRENT SELECTION-SUPPORTED BLACK-MESA PAIRINGS NARROWED TO SEVEN OWNER PACKAGES / GLOBALPROP 1231 ASSET DATA MISSING FOR SIX CUSTOM PACKAGE GROUPS / NEW FAIL-CLOSED ASSET CAPTURE REQUIRED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3F6 performs only the repository-held evidence inventory required after C3F5.

C3F5 proved the exact installed-V81 pairing and numbering semantics and reduced Black Mesa topology clearance to a per-selected-flow requirement: the selected DungeonFlow must expose the standard fire-exit mechanism needed for Dawn to request three exits and for V81 to number/pair the generated inside teleports.

This checkpoint asks only:

1. which Black Mesa-row pairings are already selection-supported and therefore need topology evaluation now;
2. which exact current package/version owns those flows;
3. whether the repository already contains enough exact serialized DungeonFlow / GlobalProp / fire-exit-template evidence to decide them.

No new package download, gameplay run, build or matrix rewrite is performed here.

## Fresh repository state

At the start of this checkpoint:

- `main` remains `56355ff518ae4301a38d370be9561251f6f963c1`;
- PR #138 is open, draft, unmerged;
- PR head is `eeae9951b73a0b1f9190f2593cf23fc26a247a24`;
- all exact-head workflows from C3F5 are green, including Knowledge Architecture and the V81 entrance-pairing helper validation;
- no gameplay candidate or runtime test is armed.

## Immediate Black Mesa-row topology cohort

C3B/C3D already establish selection-layer support on Black Mesa for:

- the 22 `DIRECT_LLL_UNIVERSAL_TAG_OVERRIDE` custom flows; and
- Black Mesa's own Dawn/native flow.

That yields **23 selection-supported Black Mesa-row pairings** whose topology question is presently meaningful.

The other 30 selectable interiors remain selection-unproven on the Black Mesa External row. Their GlobalProp topology does not need to be treated as already-gated Black Mesa availability evidence in this bounded step.

## Exact 22-flow direct-LLL package grouping

The authoritative Phase-A/B2 inventory groups the 22 direct project-controlled flows into only six exact current Thunderstore packages:

### Generic_GMD-Generic_Interiors 5.2.0 — 6 flows

- `BunkerFlow`
- `DrainsFlow`
- `SubstationFlow`
- `BackroomsFlow`
- `SHFlow`
- `TowerFlow`

### LethalMatt-Bozoros 2.9.3 — 1 flow

- `CircusFacilityFlow`

### Magic_Wesley-WesleysInteriors 4.1.15 — 12 flows

- `AquaticDungeonFlow`
- `DeepSewersFlow`
- `FracturedComplexFlow`
- `GreenhouseFlow`
- `MuseumInteriorFlow`
- `StoreFlow`
- `ExpandedFacility`
- `Level3ButCoolFlow`
- `GrandArmoryFlow`
- `SpookyManorFlow`
- `RubberRoomsFlow`
- `ToystoreFlow`

### Tolian-Scoopy_Castle 1.0.1 — 1 flow

- `CastleFlow`

### Nikki-Slaughterhouse 1.2.1 — 1 flow

- `SlaughterhouseFlow`

### Beaniebe-Storage_Complex 1.2.5 — 1 flow

- `StorageComplex`

Together these six packages own all **22** direct-LLL flows.

The 23rd current selection-supported pairing is:

### Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior 3.4.4 — 1 flow

- `Black Mesa`

## What exact repository-held evidence exists

### Flow identity and package version

Repository authority is already sufficient to bind every one of the 23 flows to its exact current display/flow ID and current package/version through:

- `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`;
- `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`;
- the accepted-profile package inventory.

This is registration/version provenance, not serialized asset proof.

### Accepted-profile snapshot boundary

The committed `ProfileSources/S1.42AK/` tree is a text/configuration snapshot plus `FILE_INDEX.json` provenance.

The repository tree contains no committed DLL, Unity bundle, asset-bundle, `.assets`, package ZIP or `.r2z` payload under that ProfileSources directory. Binary files are represented by file-index metadata/hashes rather than by committed payload bytes.

Therefore the accepted ProfileSources tree cannot itself be parsed to recover DungeonFlow GlobalProps or fire-exit prefab templates.

### Black Mesa exact package

C3F2 is the one relevant exact-package exception already captured for this 23-flow cohort.

It binds exact Black Mesa 3.4.4 package/archive/DLL/UnityFS bytes and proves the serialized moon/dungeon EntranceTeleport surface.

However its committed compact result, `BLACK_MESA_344_STATIC_TOPOLOGY.json`, does **not** inventory the `Black Mesa` DungeonFlow GlobalProps or resolve GlobalProp ID `1231` to a fire-exit prefab/template.

The C3F2 inspector is nevertheless directly reusable infrastructure: it already performs fail-closed exact-package acquisition, SHA binding, UnityPy 1.25.3 static parsing, cross-file pointer resolution and complete MonoScript/MonoBehaviour coverage for selected bundle surfaces.

### Six direct-LLL owner packages

A full recursive inventory of committed `SourceEvidence/` at the current PR head contains no package-specific exact asset capture for:

- Generic_GMD-Generic_Interiors;
- Magic_Wesley-WesleysInteriors;
- LethalMatt-Bozoros;
- Tolian-Scoopy_Castle;
- Nikki-Slaughterhouse;
- Beaniebe-Storage_Complex.

Existing project records for those packages prove current versions, registration/configuration and some runtime behavior, but not their serialized DungeonFlow GlobalProp tables.

## Runtime evidence boundary

C1 contains positive Offense generation/traversal evidence for a subset of these flows and repeatedly records four PathfindingLib entrance connections.

That runtime evidence is useful generation/traversal qualification for the observed Offense runs, but it does not establish the asset-level conditions now required for Black Mesa's three alternate exits:

- presence of DungeonFlow GlobalProp ID `1231`;
- the effective serialized count/range structure of that prop;
- whether its matching generated GlobalProp object is the standard fire-exit template;
- whether each generated template produces an inside-side `EntranceTeleport` entering V81 numbering as ID `1`;
- whether count `3` is supported.

Therefore C1 cannot be used as a substitute for the missing GlobalProp/template asset evidence.

## C3F6 decision

Repository-held evidence is **insufficient** to classify the 23 current selection-supported Black Mesa pairings as topologically cleared.

The evidence gap is narrower than a 53-flow audit:

- **1 flow / Black Mesa package:** exact package already captured, but GlobalProp/template extraction is missing;
- **22 flows / six custom packages:** exact current package versions are known, but no exact package/bundle capture currently exposes their DungeonFlow GlobalProps/templates.

A new repository-native, fail-closed **asset capture** is therefore required.

No local game assembly is required for these six custom packages: their exact Thunderstore package versions can be acquired and inspected in GitHub Actions, following the already-established C3F2 provenance pattern.

Black Mesa 3.4.4 can be re-read through the same exact-package contract already established by C3F2.

## Required next capture contract

The next helper should remain bounded to the **23 currently selection-supported Black Mesa-row flows**.

For every target flow it must, fail-closed:

1. acquire exactly the current package/version;
2. record archive size/SHA-256 and relevant UnityFS-member hashes;
3. resolve exactly one intended DungeonFlow asset by the authoritative current flow identity;
4. enumerate the full serialized DungeonFlow GlobalProp table;
5. report whether GlobalProp ID `1231` is present, absent or unresolved;
6. preserve the serialized settings associated with ID `1231`, including its count/range fields where exposed;
7. identify serialized GlobalProp components/templates using ID `1231`;
8. resolve enough GameObject/component context to determine whether the template exposes an inside-side `EntranceTeleport` and its serialized pre-numbering `entranceId`;
9. fail closed on ambiguous flow identity, unresolved non-null pointers, parser failures affecting the target surface or package/provenance drift.

The capture must distinguish:

- **PROP_AND_TEMPLATE_PROVEN**;
- **PROP_PRESENT_TEMPLATE_UNRESOLVED**;
- **PROP_1231_ABSENT**;
- **CAPTURE_UNRESOLVED**.

Presence of ID `1231` alone is not sufficient to claim count-3 topology compatibility.

## Proof boundary

C3F6 does not prove that any additional pairing is viable.

It does not infer GlobalProp presence from DunGen convention, author similarity, successful one-fire-exit generation on another moon or package family membership.

It also does not authorize:

- a B3 matrix change;
- universal availability implementation;
- duplicate Black Mesa LLL registration;
- S1.42AB normalizer changes;
- a gameplay build or runtime test.

## Next bounded segment

Implement and CI-validate the fail-closed C3F7 GlobalProp-1231/package-asset capture helper for the 23 current selection-supported Black Mesa-row flows, reusing the C3F2 exact-package/UnityPy pattern rather than inventing a separate acquisition mechanism.

Do not perform gameplay analysis or matrix promotion in the helper-implementation segment.
