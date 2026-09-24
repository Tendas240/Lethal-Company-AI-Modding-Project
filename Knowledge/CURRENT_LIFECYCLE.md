<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `RuntimeEvidence/S1.42AK/20260918T172838Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `RuntimeEvidence/S1.42AK-SCRAPDIAG1/20260918T200602Z/`, `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`, `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`, `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`, `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`, `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`, `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`, `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`, `SourceEvidence/UniversalInteriorViability/PhaseC3F18/FINDINGS.md`, `SourceEvidence/UniversalInteriorViability/PhaseC3F18/IMPLEMENTATION_FINDINGS.md`, `BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md`  
**Last-Validated:** 2026-09-24

## Accepted gameplay baseline

**S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK** remains the sole current accepted gameplay baseline and latest normal built artifact.

Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`

S1.42AI remains the accepted predecessor and rollback provenance baseline.

## Accepted contract

S1.42AK preserves LC Office `Camera Frame Speed = 0`, exact Men-stalker disablement, Biodiversity Aloe `PowerLevel = 0`, unchanged RandomEnemiesSize, unchanged LC Office scrap tuning, and no diagnostic force-selection artifacts.

The accepted full-normal Offense gate remains valid. Its limited hostile-indoor coverage is preserved as a qualification rather than a spawn-regression finding.

## Completed LC Office scrap investigation

`Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md` closes the LC Office Scrap Quantity/Distribution Investigation.

Exact diagnostic evidence:

- profile `Profiles/LC V1 S1.42AK-SCRAPDIAG1 LC Office Scrap Placement Diagnostic.r2z`;
- SHA-256 `233bcc058a3fa95d63e0577c4ff74b5a0dc137db49757b50376e447dd082d3b1`;
- runtime evidence `RuntimeEvidence/S1.42AK-SCRAPDIAG1/20260918T200602Z/`;
- raw log SHA-256 `e32e7d9b858fd78c046d5206c519a7709b3dcd5b2b8c432500233f51c6f13348`;
- valid selector/logger arming, LC Office selection, snapshot A/B 23/23, stable ID-set 23, anchor/item records and `COMPLETE stable=23`, with no diagnostic `REFUSED` or `INCONCLUSIVE`.

Base generation was 18 and replication was 18+3. After separating the LC Office Upturned Apparatus and ship Crisp Dollar Bill, 21 relevant interior scrap objects span three height bands (4 lower, 11 middle, 6 upper) and 13 support-tile roots. No low-count regression, strong one-floor/one-room concentration or near-identical-position clustering is reproduced.

The user's sparse-local-density impression is compatible with a large multi-level interior whose scrap is globally distributed. No narrow faulty placement owner is established. The scope closes with **no gameplay delta**: no quantity increase and no placement patch. S1.42AK-SCRAPDIAG1 remains diagnostic-only evidence.

## Selected scope — Universal Interior Viability / Equal Availability

The next selected independent scope is **Universal Interior Viability / Equal Availability**. Investigation contract: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

The accepted S1.42AB normalizer remains unchanged: it equalizes every positive viable rarity to `100` only after LLL viability filtering. The selected scope therefore targets the earlier viability/availability layer, not the accepted weighting layer.

Phases A through C1 are complete. Phase C2 is complete under `Current/169_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C2_OWNER_HARD_BLOCK_REASON_ANALYSIS.md`. The fixed 30×53 availability matrix remains unchanged at 1,590 cells: 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. C2 reason-classifies the 14 hard blocks: 12 Offense exclusions are package/asset default targeting or balance rules; Shatteredrooms × Experimentation and × Embrion remain explicit owner exclusions whose technical cause is unproven. No hard-block cell is currently proven to be a technical compatibility safeguard.

## BMGHDIAG1 runtime attempt — inconclusive diagnostic refusal

The first exact published `S1.42AK-BMGHDIAG1` Black Mesa run is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`. The plugin loaded but emitted `[BMGHDIAG1] REFUSED TO ARM` because `ValidateAssemblyHash` could not hash the loaded `Assembly-CSharp.dll`; its fail-closed contract preserved normal dungeon selection.

The same run nevertheless proves that normal LethalLevelLoader matching on Black Mesa includes `Greenhouse (100)` and that accepted S1.42AB normalization leaves Greenhouse at effective rarity 100. The actual normal selection was `Decrepit store`. The user's successful main-entrance and two distinct fire-exit in/out traversals therefore apply to Decrepit store, not Greenhouse.

Black Mesa x Greenhouse remains `NOT_YET_PROVEN`; this is diagnostic-tool failure evidence, not a demonstrated Greenhouse incompatibility. Decision authority: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`. Do not rerun the same BMGHDIAG1 bytes.

## BMGHDIAG2 inactive review build — pass

C3F18 first established and source/static-verified the provenance-safe `S1.42AK-BMGHDIAG2` successor: the physical installed V81 `Assembly-CSharp.dll` is hashed through BepInEx `Paths.ManagedPath`, while the loaded `EntranceTeleport` assembly/type/method contract is checked structurally. The selection and read-only observation Harmony surfaces remain unchanged from the reviewed successor design.

A separate inactive review build has now also passed. PR #142 exact head `e45c695a5f75dd8e304f0434cd21bce3e0a30da3` produced review run `35990294162` / Actions artifact `10803912824`. The review profile SHA-256 is `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2` and the compiled/injected BMGHDIAG2 DLL SHA-256 is `51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775`. All 337 archive members were verified: exactly one diagnostic DLL was added, only `export.r2x` identity metadata changed, package/config changes are zero, LLL remains `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`, and the accepted normalizer remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. Persisted evidence: `BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md`.

BMGHDIAG2 is **review-built but not published, not runtime-armed and not accepted**. The review artifact is not a gameplay target. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built/published normal artifact: **S1.42AK**.
- Active gameplay candidate: **none**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **no**.
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 inactive review build passed; exact publication checkpoint next**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No gameplay successor or universal override is armed.

## Exact next project action

Publish the exact reviewed S1.42AK-BMGHDIAG2 bytes from review run 35990294162 / artifact 10803912824, pinning profile SHA-256 56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2 and diagnostic DLL SHA-256 51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775, and verify the published archive/ProfileSources against the passed review-build delta. Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Do not Gale-import or arm gameplay/runtime in the publication checkpoint.

## Permanent Gale workflow

The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. No diagnostic is currently runtime-armed. BMGHDIAG2 remains source/static-only until a later review build, publication, and explicit atomic activation step; only that later activation may authorize another gameplay run.
