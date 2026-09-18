<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `RuntimeEvidence/S1.42AK/20260918T172838Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/157_S1.42AK_BUILD_CANDIDATE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `Current/156_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_CONFIRMATION_AND_S1.42AK_SUCCESSOR_DECISION.md`, `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md`, `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline

**S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK** is the sole current accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`

S1.42AI remains the accepted predecessor and rollback provenance baseline.

## Acceptance result

S1.42AK passed its full-normal Offense gate. The uploaded session contains two runs: the first was aborted shortly after landing before interior entry; the second naturally selected `Spooky manor` and was played inside for roughly three minutes until the user died.

The user saw no hostile indoor enemy during the played Spooky Manor window. This is a coverage limitation, not a proven spawn regression. The log still proves normal stack startup/gameplay flow, ordinary exterior enemy activity, normal Interior Weight Normalization, interior generation, scrap generation/interactions and zero project-critical markers named by the candidate gate.

Men-stalker produced no package/runtime/spawn signature, consistent with the verified disabled state. Aloe remained registered without a new runtime regression; an Aloe spawn was not required. LC Office was not naturally selected, which is explicitly valid under the candidate contract because the completed S1.42AJ-DIAG2 A/B already provides deterministic LC Office generation, repeated elevator operation and the camera-render comparison.

The one-shot LethalMin `PiggyMetalDetectorPatch` failure is retained as real compatibility evidence. The identical signature predates S1.42AK in the normal S1.42AJ run and both LC Office diagnostics; DIAG2 subsequently exercised LC Office for roughly twelve minutes. No current user-facing metal-detector/Pikmin regression is established.

## Accepted contract

S1.42AK was built directly from exact S1.42AJ and accepts only the statically verified balanced delta:

- LC Office `Camera Frame Speed = 0`;
- exact `YaBoiDucki-men_stalker 3.1.2` disabled;
- Biodiversity Aloe `PowerLevel = 0`;
- RandomEnemiesSize byte-identical to S1.42AJ;
- LC Office scrap tuning unchanged;
- no diagnostic force-selection artifacts.

## Parent and diagnostic evidence

**S1.42AJ — LC Office V81 Integration** remains the exact unaccepted parent of S1.42AK. It is not a gameplay baseline.

**S1.42AJ-DIAG1** and **S1.42AJ-DIAG2** remain diagnostic-only evidence. DIAG2's longer confirmation run retained `Camera Frame Speed = 0`, covered roughly twelve minutes after LC Office generation, included repeated elevator operation and did not reproduce the characteristic repeated DIAG1 stutter reported by the user.

## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK**.
- Active runtime candidate: **none**.
- Runtime test outstanding: **no**.
- Selected scope: **LC Office Scrap Quantity/Distribution Investigation — SELECTED / INVESTIGATION / NOT ARMED**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AK_ACCEPTANCE_INVESTIGATE_LC_OFFICE_SCRAP`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK` remains the runtime-evidence attribution build.
- No successor build is armed.

## Selected investigation scope

LC Office scrap quantity/distribution is explicitly selected under `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md` and `Knowledge/INTERIORS_AND_LLL.md`. Selection changes no gameplay bytes, assigns no successor build ID, leaves `BuildSpecs/current.json` disabled, leaves `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, and creates no runtime test.

The existing-evidence count comparison is complete. LC Office produced a 14-object base target in DIAG1 and 15 in DIAG2; accepted S1.42AK Spooky Manor also began at 14 and finalized at 15. The normal S1.42AJ Facility run finalized much higher only because BCMER selected `PlentyOutsideScrap`, so that event-inflated result is not a normal comparator. No LC Office-specific low-count regression is established. Existing logs still lack a complete item-to-room/floor map, so placement/discoverability remains unresolved. See `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`.

## Exact next project action

Design the minimal diagnostic-only LC Office scrap placement instrumentation from exact accepted S1.42AK. Do not arm a runtime test or change gameplay tuning until the diagnostic implementation and static review are complete.

## Permanent Gale workflow

For any future explicitly armed runtime candidate, use the canonical repository-driven Gale replacement/import helper in `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain` under the current fail-closed diagnostic-aware v2.4 contract. No runtime test is presently outstanding, so no import or log upload is required now.
