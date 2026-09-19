<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `RuntimeEvidence/S1.42AK/20260918T172838Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `RuntimeEvidence/S1.42AK-SCRAPDIAG1/20260918T200602Z/`, `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`, `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`, `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`, `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`, `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`  
**Last-Validated:** 2026-09-19

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

Phases A, B1, B2 and B3 are complete. Phase C1 is complete under `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`. The fixed 30×53 availability matrix remains unchanged at 1,590 cells: 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. C1 mines existing technical runtime proof separately: 15 interiors have Offense generation plus recorded player enter/exit, 4 more have generation/tile/entrance-pair evidence only, and 34 have no trusted actual-generation proof in the conservative scan. Existing proof is Offense-only and therefore does not establish moon-side compatibility on the other 29 target moons.

## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK**.
- Active gameplay candidate: **none**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **no**.
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C1 complete / Phase C2 owner-hard-block reason analysis outstanding**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No successor build or runtime test is armed.

## Exact next project action

Phase C2: extract and reconcile the technical/author reason for the 14 current `AUTHOR_OR_OWNER_HARD_BLOCK` cells before any override is proposed. Start with the 12 Offense owner-rejected flows plus Shatteredrooms × Experimentation and × Embrion. Use package/config/source evidence to distinguish explicit compatibility safeguards from author balancing/default targeting or unexplained owner exclusions. No universal override, gameplay build or runtime test is authorized yet.

## Permanent Gale workflow

The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. With runtime attribution returned to accepted S1.42AK, the normal exact `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id` path applies.
