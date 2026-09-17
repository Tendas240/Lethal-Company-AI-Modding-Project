<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-17

## Current position

Accepted gameplay baseline: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK**, SHA-256 `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`. Latest built artifact: **S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / RUNTIME NOT ARMED**, SHA-256 `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`.

S1.42AJ is the sole active runtime candidate and full-normal runtime validation is outstanding. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` provides runtime-evidence attribution; S1.42AI remains the accepted gameplay baseline.

## Active scope

**LC Office V81 Integration — S1.42AJ built / static validated / active runtime candidate.** Canonical plan: `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`; static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`; topic authority: `Knowledge/INTERIORS_AND_LLL.md`.

S1.42AJ is compatibility-first and preserves modern IAmBatby LLL ownership plus accepted equal-effective-weight behavior. Static validation and runtime arming are complete; the outstanding gate is full-normal runtime proof of LC Office registration/viability/generation/traversal/elevator behavior and the rest of the canonical acceptance contract. Universal moon availability plus all unrelated interior work remain outside this scope.

## Remaining deferred independent scopes

- Universal interior viability / equal availability: evaluate every registered interior for safe availability on every moon, preserve equal effective probability (`100`) whenever viable, and only remove LLL/author exclusions after compatibility proof including correct entrance/exit pairing, successful generation/traversal, and no door-socket, geometry, routing, elevator or NavMesh regression; document any technically unavoidable exception explicitly.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

LC Office is the sole selected scope until it is completed, rejected, or explicitly released. Do not combine another independent deferred scope into its successor.
