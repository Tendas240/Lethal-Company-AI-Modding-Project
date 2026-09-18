<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
**Last-Validated:** 2026-09-18

## Current position

Accepted gameplay baseline and latest built artifact: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

The LC Office V81 integration scope is closed by `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`. The accepted profile carries LC Office `Camera Frame Speed = 0`, Men-stalker disabled and Aloe `PowerLevel = 0`; RandomEnemiesSize and LC Office scrap tuning remain unchanged.

The accepted full-normal evidence has one explicit coverage limit: the first attempt ended before interior entry, while the second selected Spooky Manor and supplied roughly three minutes of played interior coverage with no hostile enemy sighting. This does not establish an indoor-spawn regression and does not create another mandatory runtime test.

## Active scope

**LC Office Scrap Quantity/Distribution Investigation — implemented diagnostic / static pass / not published / not armed.** Canonical investigation plan: `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md`; topic authority: `Knowledge/INTERIORS_AND_LLL.md`.

The existing count comparison is complete: LC Office's 14-15 generated/final count is comparable to nearby normal Offense evidence, while the S1.42AJ Facility high final count was BCMER `PlentyOutsideScrap` event-inflated. No LC Office-specific low-count regression is established. Spatial room/floor placement and practical discoverability remain unresolved. S1.42AK-SCRAPDIAG1 now implements the approved exact-S1.42AK diagnostic with reviewed deterministic Office selection and a bounded read-only `RoundManager.SpawnScrapInLevel` placement logger. Repository-native static validation passed with exactly two added diagnostic DLLs and no changed/removed existing archive members. `Current/161_S1.42AK_SCRAPDIAG1_STATIC_VALIDATION_CLEARANCE.md` pins the exact review artifact for a later explicit publication/arming transition. There is still no active runtime candidate, no outstanding runtime test and no armed successor.

## Remaining deferred independent scopes

- Universal interior viability / equal availability: evaluate every registered interior for safe availability on every moon, preserve equal effective probability (`100`) whenever viable, and only remove LLL/author exclusions after compatibility proof including correct entrance/exit pairing, successful generation/traversal, and no door-socket, geometry, routing, elevator or NavMesh regression; document any technically unavoidable exception explicitly.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.


LC Office scrap quantity/distribution is the sole selected scope until this investigation is completed, rejected or explicitly released. Do not combine another independent deferred scope into it.

