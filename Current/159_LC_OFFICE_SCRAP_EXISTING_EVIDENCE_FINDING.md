# LC Office Scrap Existing-Evidence Finding

**Date:** 2026-09-18  
**Status:** COUNT COMPARISON COMPLETE / NO LOW-COUNT REGRESSION ESTABLISHED / PLACEMENT DIAGNOSTIC REQUIRED / NOT ARMED  
**Accepted baseline:** S1.42AK — LC Office Camera Enemy Balance  
**Selected scope:** LC Office Scrap Quantity/Distribution Investigation

## Question

Determine whether the repeated player impression of sparse LC Office scrap is explained by a materially low generated scrap count or whether the remaining problem is spatial placement / practical discoverability.

## Comparable Offense evidence

### S1.42AJ normal — Facility

Runtime evidence: `RuntimeEvidence/S1.42AJ/20260917T171109Z/`

- selected interior: `Facility`;
- BCMER `scrapAmountMultiplier = 1.093287`;
- base generation log: `Number of scrap to spawn: 14`;
- BCMER selected `PlentyOutsideScrap` and later logged `Transmuting 26 scrap`;
- final replication logged `clientRPC scrap values length: 28` plus a later length `1`;
- Buttery Fixes tracked 29 resulting objects.

The final 29-object result is intentionally event-inflated and is **not** a clean final-count baseline for LC Office. The useful comparator is the pre-event generation target of 14.

### S1.42AJ-DIAG1 — LC Office

Runtime evidence: `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/`

- selected interior: `LC Office`;
- `scrapAmountMultiplier = 1`;
- base generation log: `Number of scrap to spawn: 14`;
- final replication: length `14` plus a separate length `1`;
- Buttery Fixes tracked 15 resulting scrap objects.

### S1.42AJ-DIAG2 — LC Office

Runtime evidence: `RuntimeEvidence/S1.42AJ-DIAG2/20260918T144306Z/`

- selected interior: `LC Office`;
- `scrapAmountMultiplier = 1`;
- base generation log: `Number of scrap to spawn: 15`;
- final replication: `clientRPC scrap values length: 15`.

### S1.42AK normal — Spooky manor

Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`

- selected interior: `Spooky manor`;
- BCMER `scrapAmountMultiplier = 1.085188`;
- base generation log: `Number of scrap to spawn: 14`;
- BCMER later logged `Transmuting 10 scrap`;
- final replication: `clientRPC scrap values length: 15`;
- Buttery Fixes tracked 15 resulting objects.

## Count conclusion

The two targeted LC Office runs generate **14-15 base scrap objects**. The nearest normal non-Office Offense runs also begin from a **14-object** generation target, and the accepted S1.42AK Spooky Manor run ends at **15** final replicated/tracked objects.

Therefore the current repository evidence does **not** establish an LC Office-specific low generated-count regression. A blind quantity increase is not justified.

The S1.42AJ Facility final count of 29 must not be used to claim LC Office is low because that run selected the explicit BCMER `PlentyOutsideScrap` event.

## Placement / discoverability evidence

Existing logs do not provide a complete item-to-room or item-to-floor map for the 15 LC Office objects.

- Buttery Fixes scrap tracking records object name and value, not world position or room/floor ownership.
- Matty's Fixes logs some item vertical-offset adjustments. Most pre-placement entries are at local/origin coordinates and therefore do not identify final room distribution.
- DIAG2 contains an isolated final world-position correction for one item (`Toy Revolver`), but not positions for the complete 15-item set.
- LethalMin records LC Office entrance/elevator floor positions, but does not associate each scrap object with one of those floors.

This evidence is insufficient to determine whether scrap is clustered on one floor, hidden in low-traffic rooms, placed far from the normal traversal path, or otherwise difficult to discover.

## Decision

The investigation advances to **count comparable / placement unproven**.

No gameplay tuning is authorized. The next step is to design isolated diagnostic-only instrumentation derived from exact accepted S1.42AK that records the final spawned scrap set with enough spatial context to evaluate distribution and practical discoverability without changing quantity, rarity, value or placement.

The diagnostic must remain non-promotable and must not include unrelated deferred scopes.
