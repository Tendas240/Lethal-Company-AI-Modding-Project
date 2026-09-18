<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AK candidate=S1.42AK runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-17

## Current position

Accepted gameplay baseline: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK**. Latest built balanced artifact and active runtime candidate is **S1.42AK — LC Office Camera Enemy Balance — STATIC VALIDATED / NOT ACCEPTED**.

The second exact S1.42AJ-DIAG2 Offense run is ingested and closes the planned camera-render A/B for project purposes: the characteristic DIAG1 repeated stutter did not recur during a substantially longer LC Office run. DIAG2 remains diagnostic-only and is not accepted.

**S1.42AK — LC Office Camera Enemy Balance** has been built directly from exact S1.42AJ under `BuildSpecs/S1.42AK_PLAN.md` and is now the active full-normal runtime candidate. Static verification is recorded at `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`. One ordinary unforced Offense day plus the fresh S1.42AK runtime log is outstanding; S1.42AK remains not accepted.

## Active scope

**LC Office V81 Integration — diagnostic A/B complete; S1.42AK full-normal runtime validation active.**

The prepared successor carries only:
- LC Office `Camera Frame Speed = 0`;
- disable `YaBoiDucki-men_stalker 3.1.2`;
- Aloe `PowerLevel = 0`.

RandomEnemiesSize is explicitly unchanged. LC Office scrap is also unchanged in S1.42AK: the latest run logged 15 objects to spawn, while the user still perceived the interior as sparse or poorly distributed. Quantity versus spatial placement remains a separate evidence-driven follow-up.

S1.42AK must derive from exact S1.42AJ and must not inherit DIAG1/DIAG2 force-selection artifacts.

## Remaining deferred independent scopes

- LC Office scrap quantity/distribution investigation: distinguish generated count from room/floor placement and practical discoverability before changing any scrap tuning.
- Universal interior viability / equal availability: evaluate every registered interior for safe availability on every moon, preserve equal effective probability (`100`) whenever viable, and only remove LLL/author exclusions after compatibility proof including correct entrance/exit pairing, successful generation/traversal, and no door-socket, geometry, routing, elevator or NavMesh regression; document any technically unavoidable exception explicitly.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

LC Office is the sole selected scope until it is completed, rejected, or explicitly released. Do not combine another independent deferred scope into its successor.
