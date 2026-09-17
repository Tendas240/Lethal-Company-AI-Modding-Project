# Interiors, LethalLevelLoader and Equal Effective Weighting

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interior-selection architecture and deferred compatibility exceptions  
**Canonical-For:** `interiors_and_lll`  
**Evidence:** `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `RuntimeEvidence/S1.42AF/20260905T223738Z/raw/LogOutput.log`, `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Related:** `ProfileSources/S1.42AG/`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-17

## Accepted architecture

S1.42AB established the accepted permanent rule:

1. LethalLevelLoader `1.7.12` remains authoritative for whether a dungeon flow is viable/excluded on the current moon.
2. The project-local normalization runs **after** LLL's viability determination.
3. Every returned positive rarity is normalized to exactly `100`.
4. The patch does not add, remove, re-register or deduplicate flows.
5. Enemy, Scrap and MapObject rarity systems are untouched.

This means newly installed interiors automatically inherit effective rarity `100` whenever LLL itself returns them as viable.

## Runtime proof

Accepted S1.42AB Offense evidence:

- viable entries before normalization: 40;
- viable entries after normalization: 40;
- changed rarities: 12/40;
- pre-normalization range: 20..300;
- all positive final effective rarities: 100;
- Black Mesa appears exactly once;
- no excluded flow was inserted;
- `Expanded facility` generated successfully;
- no user-visible S1.42AB regression was reported.

Later S1.42AF full-normal-stack runtime evidence preserved the same architecture and exposed a 41-entry viable Offense pool. Both Wesley interiors in question were present before and after project-local normalization:

- `Art Gallery (MuseumInteriorFlow)` -> viable `100` -> final effective `100`;
- `Rubber Rooms (RubberRoomsFlow)` -> viable `100` -> final effective `100`.

DawnLib also resolved both exact flow assets in the same runtime:

- `magic_wesleysmod:museuminteriorflow -> MuseumInteriorFlow`;
- `therubberrooms:rubberroomsflow -> RubberRoomsFlow`.

This proves that the current profile does not suppress Art Gallery or Rubber Rooms through a bad rarity setting or failed registration. A lack of observed player rolls is compatible with a very large equal-weight pool and is not, by itself, evidence of a configuration bug.

Authoritative runtime marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## Equality rule

The project target is equal **effective** probability for every viable registered interior, not equal package shares and not theme-weighted author defaults. A package containing multiple flows contributes multiple independently normalized flows.

A technical author hard block is not a desired balancing exception. Do not blindly override one until its compatibility reason is understood and runtime-tested.

## Wesley's Interiors boundary

Current package state includes `Magic_Wesley-WesleysInteriors 4.1.15` and `Zaggy1024-DunGenReferenceFixer 0.0.1` under the full normal stack.

For Art Gallery and Rubber Rooms specifically, current repository runtime evidence proves:

- registration succeeds;
- exact flows are resolved;
- both are viable on Offense;
- both reach the final normalized pool at effective rarity `100`.

Therefore do **not** increase their weights or add Wesley-specific compatibility packages merely because the user has not yet encountered them naturally.

Actual successful generation of each exact Wesley flow is a stronger compatibility question than registration/weighting and requires a real selected dungeon run. Keep that separate from spawn-weight diagnosis.

Do not fold any replacement/fork evaluation for DunGenReferenceFixer into unrelated interior additions without a reproducible need.

## LC Office selected integration

LC Office V81 Integration is the currently selected compatibility/integration scope under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`. Exact S1.42AJ is **built, static validated and armed as the sole active runtime candidate**; `BuildSpecs/current.json` remains disabled and full-normal runtime validation is outstanding.

S1.42AJ package contract (statically verified):

- add `Piggy-LC_Office 2.3.4`;
- add `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`;
- add `JacobG5-DestroyItemInSlotFix 1.0.0`;
- transition `Alice-DungeonGenerationPlus 1.5.0 -> 1.5.1`;
- preserve `IAmBatby-LethalLevelLoader 1.7.12` as the sole LLL owner;
- explicitly forbid `pacoito-LethalLevelLoaderUpdated` from the final profile/export.

The active compatibility candidate does not force LC Office onto all moons. Runtime must now prove registration, default/modern-LLL viability, effective normalization to `100`, actual dungeon generation, traversal, elevator/power behavior and ordinary enemy navigation. Any later universal-availability tuning is a separate balance/configuration scope.

The exact accepted S1.42AI package/dependency baseline was re-verified on 2026-09-17. The required infrastructure versions are already enabled; `Alice-DungeonGenerationPlus 1.5.0` is the version to transition; the three LC Office target additions are absent; `pacoito-LethalLevelLoaderUpdated` is absent; and the accepted `S142ABInteriorWeightNormalization.dll` remains present at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. The minimal package delta is therefore fixed in `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`; build-time dependency resolution must still prove no unintended cascade or second LLL owner.

## Shatteredrooms restriction

Shatteredrooms is explicitly restricted on Experimentation and Embrion. S1.42AB intentionally preserves that LLL-side restriction because the project-local patch changes rarity only after viability filtering.

Desired long-term architecture is still equal availability/effective probability everywhere **if** the restriction can later be proven technically safe to remove. Until then, preserve it.

## CullFactory compatibility

Historically generated/confirmed exact interior IDs:

- Junkrooms: `junkrooms`
- Shatteredrooms: `shatteredrooms`

The deferred CullFactory compatibility scope is to add/validate disable-culling exceptions for those exact IDs. Do not guess alternate identifiers.

## Black Mesa ownership

Black Mesa uses its own DawnLib/native owner path. Do not duplicate-register it through LLL merely to force equal weighting. S1.42AB runtime confirms it remains single-registered and receives final effective rarity 100 in the viable list.

## Duplicate-registration rule

Avoid:

- pack + standalone duplication;
- LLL registration for content already owned by DawnLib/JLL/native configuration;
- duplicate Black Mesa registration;
- parallel `IAmBatby-LethalLevelLoader` plus `pacoito-LethalLevelLoaderUpdated` ownership.

## Remaining deferred interior work

Keep separate from the selected LC Office compatibility scope and the already accepted S1.42AB weighting architecture:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- any future attempt to remove the Shatteredrooms Experimentation/Embrion safety restriction;
- any future LC Office universal-moon availability tuning after compatibility acceptance.

Package-specific historical research remains in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`; this topic file is the current authority for the live interior-selection rule.
