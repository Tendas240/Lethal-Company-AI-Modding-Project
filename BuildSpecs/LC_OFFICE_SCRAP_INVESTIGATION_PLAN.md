# LC Office Scrap Quantity / Distribution Investigation Plan

**Status:** COUNT COMPARABLE / PLACEMENT DIAGNOSTIC DESIGNED / NOT IMPLEMENTED / NOT ARMED  
**Date:** 2026-09-18  
**Accepted baseline:** S1.42AK — `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z` / `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Topic authority:** `Knowledge/INTERIORS_AND_LLL.md`  
**Lifecycle authority:** `Current/CURRENT_STATE.json`

## Objective

Determine whether the user's repeated impression of sparse LC Office scrap is caused by an actually low generated item count, spatial room/floor clustering or poor practical discoverability. Do not change scrap tuning until those causes are separated.

This is an investigation contract only. It does not authorize a successor build, diagnostic runtime test or gameplay/config delta.

## Established evidence

- S1.42AJ-DIAG1 generated LC Office and produced 15 total scrap values.
- S1.42AJ-DIAG2 generated LC Office and reported `clientRPC scrap values length: 15`.
- The user nevertheless perceived relatively little scrap or poor distribution in LC Office.
- S1.42AK accepted LC Office camera/enemy balance without changing LC Office scrap tuning.
- The accepted S1.42AK `BepInEx/config/Piggy.LCOffice.cfg` only overrides `[General] Camera Frame Speed = 0`; it contains no project-authored scrap quantity/distribution override.

These facts show that scrap generation exists and that the camera A/B did not reduce the generated count.

## Existing-evidence comparison result

The focused comparison is recorded in `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`.

- normal S1.42AJ Facility: base generation target 14; final result inflated by BCMER `PlentyOutsideScrap`;
- S1.42AJ-DIAG1 LC Office: base target 14; 15 tracked after the additional replicated object;
- S1.42AJ-DIAG2 LC Office: base/final count 15;
- accepted S1.42AK Spooky Manor: base target 14; final replicated/tracked count 15.

**Conclusion:** LC Office does not show a material low-count regression in the existing evidence. Quantity tuning is therefore not authorized.

The remaining uncertainty is spatial distribution/discoverability. Existing tracking logs do not provide complete final world positions plus room/floor ownership for all 15 Office objects. Matty's Fixes exposes only partial position-adjustment evidence, and the available LethalMin floor/teleport coordinates do not map each scrap item to a floor.

The diagnostic design is now fixed by `Current/160_LC_OFFICE_SCRAP_PLACEMENT_DIAGNOSTIC_DESIGN.md` and implementation plan `BuildSpecs/S1.42AK-SCRAPDIAG1_PLAN.md`. It uses exact accepted S1.42AK, the already reviewed LC Office selector, and one new read-only `RoundManager.SpawnScrapInLevel` postfix that performs only two bounded delayed snapshots and logs world/floor/support-surface context.

## Diagnostic dimensions

### 1. Generated count

Use repository runtime evidence to compare the LC Office generated count with comparable Offense non-Office runs under the same or closest accepted stack. Do not assume that 15 is intrinsically normal or abnormal without a comparator.

Record separately:

- selected interior;
- logged generated scrap count/value-array length;
- moon and relevant round context where evidenced;
- whether the run is normal-stack or diagnostic force-selection;
- any evidence that a config/build delta could affect scrap generation.

### 2. Spatial placement / distribution

Existing logs may not encode exact object coordinates or room/floor ownership. Search repository-owned evidence/config/source artifacts for placement-specific information before proposing instrumentation.

If placement cannot be resolved from existing evidence, define a **diagnostic-only** artifact derived from exact accepted S1.42AK that logs enough information to distinguish clustering/inaccessibility from count scarcity. The diagnostic must not alter scrap quantity, rarity, value or placement and must not be promotable as the balanced gameplay baseline.

### 3. Practical discoverability

Treat the user's observation as valid runtime evidence of discoverability, but not by itself as proof of a count regression. Correlate visible/collected scrap observations with generated-count and placement evidence where possible.

## Decision gate

No gameplay tuning is authorized until the investigation supports one of these outcomes:

1. **Count comparable / placement unproven:** do not increase quantity; obtain placement/discoverability evidence if the problem remains reproducible.
2. **Count normal but placement/discoverability abnormal:** target the proven placement mechanism if one exists; do not mask it with a blind global quantity increase.
3. **Generated count materially low versus suitable comparators:** identify the owning count/rarity mechanism first, then propose the narrowest configuration or code change.
4. **No reproducible LC Office-specific problem:** close the scope without a gameplay delta.

Any later candidate must be based on exact accepted S1.42AK or a later accepted baseline, never on S1.42AJ-DIAG1/DIAG2 diagnostic bytes.

## Scope boundaries

Do not combine this investigation with:

- universal interior viability/equal availability;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- MelanieMausoleum fog tuning;
- Black Mesa/Pikmin routing;
- LethalEscapeUpdated evaluation;
- AdditionalNetworking or broader LethalMin repairs;
- unrelated enemy or item balance changes.

## Exact next action

Implement Patches/S142AKDiagScrapPlacement and the separate non-active BuildSpecs/S1.42AK-SCRAPDIAG1.json request exactly to the approved diagnostic design, then run static source/archive validation. Do not arm a runtime test yet.
