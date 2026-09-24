# Interiors, LethalLevelLoader and Equal Effective Weighting

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interior-selection architecture and deferred compatibility exceptions  
**Canonical-For:** `interiors_and_lll`  
**Evidence:** `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `RuntimeEvidence/S1.42AF/20260905T223738Z/raw/LogOutput.log`, `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`, `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md`, `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`, `Current/160_LC_OFFICE_SCRAP_PLACEMENT_DIAGNOSTIC_DESIGN.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`, `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`, `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`, `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`, `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`, `Current/169_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C2_OWNER_HARD_BLOCK_REASON_ANALYSIS.md`  
**Related:** `ProfileSources/S1.42AG/`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-19

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

## LC Office accepted integration

LC Office V81 Integration is now closed by accepted **S1.42AK — LC Office Camera Enemy Balance**. Acceptance authority is `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`; full-normal evidence is `RuntimeEvidence/S1.42AK/20260918T172838Z/`.

The accepted full-normal session contains two Offense attempts. The first was aborted shortly after landing before interior entry and is not treated as practical interior coverage. The second naturally selected `Spooky manor`; the player spent roughly three minutes inside before dying. The user observed no hostile indoor enemy during that interval. That observation is preserved as limited hostile-indoor coverage rather than interpreted as proof of an indoor spawn failure.

S1.42AK itself did not naturally select LC Office, which is explicitly acceptable under the candidate contract. The targeted LC Office behavior remains covered by S1.42AJ-DIAG1/DIAG2: DIAG2 changed only `[General] Camera Frame Speed = 0`, then ran roughly twelve minutes after LC Office generation with repeated elevator operation and no recurrence of the characteristic repeated DIAG1 stutter reported by the user.

S1.42AK was built directly from exact S1.42AJ, never from diagnostic bytes. Its accepted delta is limited to `Camera Frame Speed = 0`, disabling exact `YaBoiDucki-men_stalker 3.1.2`, and setting Biodiversity Aloe `PowerLevel = 0`. RandomEnemiesSize is explicitly unchanged. Men-stalker produced no package/runtime/spawn signature in the accepted S1.42AK evidence; Aloe remained registered without a new runtime regression.

The recurring one-shot LethalMin `PiggyMetalDetectorPatch` startup failure remains real compatibility evidence. It is identical in the normal S1.42AJ run and both targeted LC Office diagnostic runs; DIAG2 subsequently exercised LC Office for roughly twelve minutes. No current user-facing metal-detector/Pikmin regression is established, so it does not reopen the accepted integration by itself.

LC Office scrap tuning remains unchanged. **The LC Office Scrap Quantity/Distribution Investigation is complete with no gameplay delta.** `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md` already established that the earlier 14-15 Office counts were comparable to nearby normal Offense evidence. Exact S1.42AK-SCRAPDIAG1 then closed the placement gap with valid evidence at `RuntimeEvidence/S1.42AK-SCRAPDIAG1/20260918T200602Z/`: base target 18, replication batches 18+3, stable snapshot A/B 23/23, complete anchor/item records and `COMPLETE stable=23` with no `REFUSED`/`INCONCLUSIVE`. After separating the LC Office Upturned Apparatus and ship Crisp Dollar Bill, 21 relevant interior items span three clear height bands (4 lower, 11 middle, 6 upper) and 13 distinct LevelGenerationRoot support-tile roots, with no near-identical-position clustering. The runtime result establishes neither a low-count regression nor a strong one-floor/one-room placement defect. The sparse-local-density impression is compatible with the large multi-level layout, but no narrow faulty placement owner is proven. `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md` closes the scope without a quantity increase or placement patch. S1.42AK remains unchanged; SCRAPDIAG1 remains diagnostic-only evidence. Universal-moon availability and unrelated interior viability work remain separate scopes.

S1.42AJ package contract (statically verified):

- add `Piggy-LC_Office 2.3.4`;
- add `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`;
- add `JacobG5-DestroyItemInSlotFix 1.0.0`;
- transition `Alice-DungeonGenerationPlus 1.5.0 -> 1.5.1`;
- preserve `IAmBatby-LethalLevelLoader 1.7.12` as the sole LLL owner;
- explicitly forbid `pacoito-LethalLevelLoaderUpdated` from the final profile/export.

The accepted S1.42AK integration does not force LC Office onto all moons. The first ingested full-normal S1.42AJ evidence at `RuntimeEvidence/S1.42AJ/20260917T171109Z/` proves modern-LLL viability on Offense at author rarity `65` and final project-local normalized rarity `100`; that run selected Facility. S1.42AJ-DIAG1 then provided deterministic actual LC Office generation coverage on Offense and is ingested at `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/`; that run exposed the user-visible later-day performance concern at roughly 3-4 stutters per second. Exact reviewed S1.42AJ-DIAG2 adds only `BepInEx/config/Piggy.LCOffice.cfg` with `[General] Camera Frame Speed = 0` over DIAG1. Its first Offense runtime evidence is ingested at `RuntimeEvidence/S1.42AJ-DIAG2/20260918T144306Z/`: LC Office generated, entrance/traversal and elevator operation were evidenced, 15 scrap values were generated (matching the DIAG1 total), and interior vents spawned multiple enemies shortly before player death. The user reported no stutter before dying but did not visually observe an interior enemy. Because the run ended earlier than DIAG1's post-generation span, the camera-render hypothesis was supported but not causally confirmed. At that point, the next action was a longer confirmation run with the exact same DIAG2 artifact, not another build. See `Current/154_S1.42AJ_DIAG1_LC_OFFICE_RUNTIME_PERFORMANCE_FINDING.md`, `Current/155_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_PARTIAL_FINDING.md` and `BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`. Any later universal-availability tuning remains a separate balance/configuration scope.

The exact accepted S1.42AI package/dependency baseline was re-verified on 2026-09-17. The required infrastructure versions are already enabled; `Alice-DungeonGenerationPlus 1.5.0` is the version to transition; the three LC Office target additions are absent; `pacoito-LethalLevelLoaderUpdated` is absent; and the accepted `S142ABInteriorWeightNormalization.dll` remains present at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. The minimal package delta is therefore fixed in `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`; build-time dependency resolution must still prove no unintended cascade or second LLL owner.

## C3F17 Black Mesa x Greenhouse qualification status

The first exact published `S1.42AK-BMGHDIAG1` runtime attempt is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/` but is **not** a successful pair qualification. The diagnostic plugin refused before arming because its installed-V81 observation provenance gate could not hash the loaded `Assembly-CSharp.dll`; fail-closed behavior preserved normal dungeon selection.

The normal Black Mesa LLL matching report in that same run includes `Greenhouse (100)`, and accepted S1.42AB normalization retains `Greenhouse(100)` in the final effective viable pool. This directly proves current Black Mesa availability and equal effective weighting for Greenhouse. It does not prove Greenhouse generation, entrance topology or player traversal because normal selection chose `Decrepit store` after the diagnostic refusal.

The user's successful main-entrance and two distinct fire-exit round trips therefore qualify Decrepit store traversal only. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`. Canonical decision: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`.

That startup-provenance root cause has since been repaired by separately versioned `S1.42AK-BMGHDIAG2`, whose exact reviewed bytes are published on main and are now the active diagnostic runtime target. The bounded runtime test is outstanding: require `[BMGHDIAG2] ARMED`, exact Black Mesa Greenhouse selection, generation/topology evidence and direct entrance traversal before changing the matrix classification. Do not rerun BMGHDIAG1, change Greenhouse availability, duplicate-register Black Mesa, alter S1.42AB normalization, modify the B3 matrix, or open the separate Black-Mesa/Pikmin routing scope. Activation authority: `Current/172_S1.42AK_BMGHDIAG2_RUNTIME_ACTIVATION.md`.

## Selected universal viability / equal availability investigation

**Universal Interior Viability / Equal Availability** is now the selected independent scope. Canonical investigation plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

The accepted S1.42AB post-viability normalization remains authoritative and unchanged. The selected work is to resolve the layer **before** that normalizer: which registered flows are viable on which moons and why.

Phase-A authority: `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`.

Exact S1.42AK reconciliation now establishes:

- **55** DawnLib-registered DungeonFlow assets;
- **53** LLL ExtendedDungeonFlow selection entries: 3 Vanilla, 49 Custom, 1 External Black Mesa;
- the two extra Dawn-only assets are vanilla `Level1FlowExtraLarge` and `Level1Flow3Exits`;
- exact S1.42AF immediately before LC Office has **52** LLL entries; `LC Office / OfficeDungeonFlow` is the exact +1 in S1.42AK;
- the 28 LLL `Custom Dungeon` config sections are non-cardinal: only **22 unique current Custom flows** have active direct config coverage, three enabled sections are aliases, two are stale/orphaned, and Black Mesa is the disabled native/DawnLib-owner case;
- therefore **27 current Custom flows have no direct active LLL Custom Dungeon config section** and remain governed by owner/author matching data;
- JLL content-specific helper/config behavior exists, but no separate JLL-only registered dungeon flow appears in the exact current Dawn/LLL inventories.

Phase-B1 authority: `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`.

The exact moon universe is now fixed:

- DawnLib registers 32 moon assets;
- LLL exposes 31 ExtendedLevels: 13 Vanilla, 16 Custom, 2 External;
- Dawn-only `lethal_company:test` is not a matrix target;
- `71 Gordion` is retained as a current LLL level but excluded from dungeon/interior pairing cells because exact runtime identifies it as `CompanyBuildingLevel` and `CompanyMoonRouteConfirmCommand`;
- the resulting pairing universe is **30 target moons × 53 selectable interiors = 1,590 cells**;
- exact S1.42AK Offense runtime fully accounts for all 53 selectable interiors: 41 are `VIABLE_EQUAL_100`; 12 are absent/unviable and remain `NOT_YET_PROVEN` until the owning config/hard-block mechanism is identified.

Phase-B2 authority: `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`.

Availability ownership is now fully partitioned:

- 22 current Custom flows use a direct active LLL `Vanilla:100,Custom:100` tag override;
- 27 current Custom flows have no direct LLL Custom Dungeon availability override and remain owner/asset-matched;
- Facility, Haunted Mansion and Mineshaft remain vanilla/native LLL matches;
- Black Mesa remains the sole DawnLib/native availability-owner case with `lethal_company:vanilla=+100,lethal_company:custom=+100`;
- current JLL configs expose behavior/features but no moon/interior availability controls.

Exact Offense is now cause-classified as 41 `VIABLE_EQUAL_100` and 12 `AUTHOR_OR_OWNER_HARD_BLOCK`. That hard-block classification describes current owner-metadata rejection before normalization; it is not proof of technical incompatibility. Shatteredrooms × Experimentation and × Embrion are explicit owner hard blocks for the same reason until Phase C establishes a technical basis.

Phase-B3 authority: `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`; complete machine matrix: `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.csv`.

The full 30×53 matrix is now materialized at **1,590 cells**:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

The 22 direct LLL universal-tag flows and Black Mesa's native Vanilla/Custom rule establish 23 equal-weight interiors on each Vanilla/Custom target moon. Offense remains the only fully observed row. Both External target moons remain entirely unproven, and owner-controlled cells outside exact evidence remain unproven. This matrix is availability evidence only; generation/traversal compatibility still belongs to Phase C.

Phase-C1 authority: `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`.

Existing trusted runtime evidence now establishes **15** selectable interiors with actual Offense generation plus recorded player enter/exit and **4** additional interiors with generation/tile/entrance-pair evidence only. **34** selectable interiors still have no positive actual-generation proof in the conservative C1 scan. These are interior-side runtime qualifications on Offense; they do not prove moon-side compatibility across the other 29 target moons and do not alter any B3 availability classification.

C1 also preserves route/NavMesh proof obligations where the logs are ambiguous. Spooky manor and Expanded Mineshaft show B-side LethalMin reachability gaps in observed runs; LiminalHouse and Rubber Rooms have route/NavMesh ambiguity; LC Office and DeepcoreMines retain known generation-time NavMesh warning noise. None is promoted to `KNOWN_TECHNICAL_RESTRICTION` without owner/geometry/route attribution.

Phase-C2 authority: `Current/169_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C2_OWNER_HARD_BLOCK_REASON_ANALYSIS.md`.

C2 reason-reconciles all 14 current owner-hard-block cells without changing matrix membership:

- 12 Offense owner-rejected cells are explained by unchanged package/asset default moon/tag/route targeting or explicit zero rarity and are classified `AUTHOR_DEFAULT_TARGETING_OR_BALANCE`;
- Shatteredrooms × Experimentation and × Embrion are explicit author exclusions with no repository-proven technical cause and are classified `UNEXPLAINED_EXPLICIT_OWNER_EXCLUSION`;
- no current hard-block cell is proven to be an explicit technical compatibility safeguard;
- no current hard-block cell is promoted to `KNOWN_TECHNICAL_RESTRICTION`.

Junkrooms/Shatteredrooms CullFactory incompatibility remains a separate known technical risk. It is not retroactively treated as the cause of any exact moon exclusion without causal evidence.

Do not interpret broad `Vanilla:100,Custom:100` tag injection as automatic proof that every flow is safe on every moon. Owner hard blocks, non-LLL registrations and technical restrictions remain authoritative until specifically understood and tested. Shatteredrooms' Experimentation/Embrion restriction therefore remains in place during the analysis phase.

No build or runtime test is currently authorized by this selection. Phases C1 and C2 are complete. The exact next action is Phase C3: resolve Black Mesa moon and Oxyde External-level tags, entrance/fire-exit topology and owner matching semantics before any availability rule is extended onto their External rows.

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

Keep separate from the selected universal viability/equal-availability scope and the already accepted S1.42AB weighting architecture:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;

Package-specific historical research remains in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`; this topic file is the current authority for the live interior-selection rule.
