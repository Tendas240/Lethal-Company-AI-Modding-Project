# Interiors, LethalLevelLoader and Equal Effective Weighting

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interior-selection architecture and deferred compatibility exceptions  
**Canonical-For:** `interiors_and_lll`  
**Evidence:** `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `RuntimeEvidence/S1.42AF/20260905T223738Z/raw/LogOutput.log`, `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`, `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md`, `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`, `Current/160_LC_OFFICE_SCRAP_PLACEMENT_DIAGNOSTIC_DESIGN.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`, `Current/165_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B1_MOON_INVENTORY_OFFENSE_BASELINE.md`, `Current/166_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B2_OWNER_CONFIG_MECHANISM_MAP.md`, `Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.md`, `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`, `Current/169_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C2_OWNER_HARD_BLOCK_REASON_ANALYSIS.md`, `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md`, `Current/206_S1.42AK_EXTERNAL_OWNER_RULE_APPLICABILITY_CLOSURE_RECONCILIATION.md`  
**Related:** `ProfileSources/S1.42AG/`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-10-02

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

The separately versioned `S1.42AK-BMGHDIAG2` attempt is now completed failed diagnostic evidence: it refused before arming on `EntranceTeleport manifest module identity mismatch`, so Black Mesa x Greenhouse remains `NOT_YET_PROVEN` and those exact bytes must not be rerun as if they can qualify the pair. The same normal-fallback run separately exposed Black Mesa x Deep Sewers generation pressure at multiplier 4.875.

The exact pair-scoped `S1.42AK-BMDSFIX1` mitigation is now the active gameplay runtime candidate, profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`, BMDSFIX1 DLL SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`. Its only behavior change is Black Mesa x `DeepSewersFlow` clamping an LLL-calculated multiplier greater than 1 to exactly 1.0. The runtime gate must prove arming/application, successful generation and landing without the previous persistent retry/atmosphere failure, plus a non-target generation with no unintended application. Activation authority: `Current/174_S1.42AK_BMDSFIX1_RUNTIME_ACTIVATION.md`.

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

The 22 direct LLL universal-tag flows and Black Mesa's native Vanilla/Custom rule establish 23 equal-weight interiors on each Vanilla/Custom target moon. Offense remains the only fully observed row. Both External target moons remain entirely unproven in the historical Phase-B3 snapshot, and owner-controlled cells outside exact evidence remain unproven. This matrix is availability evidence only; generation/traversal compatibility still belongs to Phase C.

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

Phase C3 has now exhausted the already-ingested concrete External-moon pair evidence available without a new run and separately closed the External owner-rule applicability / External semantics gate from existing source/owner/config evidence. No build or runtime test is authorized by that closure.

## Phase C3 External owner-rule applicability closure

`Current/206_S1.42AK_EXTERNAL_OWNER_RULE_APPLICABILITY_CLOSURE_RECONCILIATION.md` is the current Phase-C3 applicability authority.

Black Mesa current applicability is **31 MATCH / 22 NON-MATCH / 0 UNRESOLVED**. `MATCH` means the current owner/matching semantics support the interior on Black Mesa at the selection/availability layer; it is not a runtime-compatibility pass. `NON-MATCH` means the current positive owner/matching rule does not target Black Mesa; it is not a technical-incompatibility finding or a permanent prohibition.

The accepted S1.42AB normalizer creates neither the 31 matches nor the 22 non-matches. It only normalizes already-positive non-100 rarities after viability filtering. No duplicate Black Mesa registration is needed or authorized.

The historical Phase-B3 matrix remains unchanged at **662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, 914 `NOT_YET_PROVEN`**. The Black Mesa 31/22/0 result is a Phase-C3 current-applicability finding, not a retroactive rewrite of the historical B3 External row.

`Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` remains the concrete pair-evidence boundary. Black Mesa's already-ingested pair set is exhausted after Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. Only Greenhouse has the stronger full all-four-ID bidirectional traversal plus visual geometry qualification; the other pair records retain their narrower topology/traversal proof boundaries. None is generalized to all 31 current matches.

Oxyde remains asymmetric: C3E3H preserves 23 positive selection/metadata matches, but exact V81 ordinary generation is skipped while `spawnEnemiesAndScrap=false`, and no independent inspected ordinary dungeon/entrance-construction path is established. Selection support is therefore not executable ordinary pair proof under the current architecture.

The next compatibility step is pair-specific, not a universal override. Before authoring a candidate that newly enables an absent pairing, identify that exact pairing/restriction and satisfy the investigation plan's generation, entrance/topology, traversal, routing/NavMesh and duplicate-registration safety obligations. Preserve Shatteredrooms × Experimentation/Embrion until their safety is established, preserve the Oxyde ordinary-generation exception, and keep the regular BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification passive/outstanding/unwaived.


## Black Mesa x Abandoned Foundry PATH1 runtime/config-binding finding

Exact PATH1 evidence is `RuntimeEvidence/S1.42AK-BMAFDIAG1PATH1/20261001T195721Z/`, raw LogOutput SHA-256 `ccb38f7173a109a103f5dbc67e06d4acf60f86f95652a2db566f8b2c63a98521`. BMAFDIAG1 armed, but LLL classified Abandoned Foundry as unviable on Black Mesa; the fail-closed diagnostic refused because Foundry was absent from the viable pool. No Foundry generation/topology/traversal occurred.

The intended Foundry availability override failed at config binding, not at the accepted S1.42AB normalization layer. LLL 1.7.12's Custom Dungeon category identity includes nine leading U+200B sorting characters. The published Foundry config section has a plain category with none. The project builder created that different category, and the BMAFDIAG1 validator's Unicode-Cf-stripping header comparison incorrectly treated it as equivalent. The textual `Enable Content Configuration = true` / `Black Mesa:100` values therefore did not prove live LLL binding.

Canonical reconciliation: `Current/219_S1.42AK_BMAFDIAG1PATH1_RUNTIME_REFUSAL_AND_CONFIG_BINDING_ROOT_CAUSE_RECONCILIATION.md`.

Do not rerun PATH1. The separately versioned repair successor S1.42AK-BMAFR1 has now passed inactive review with exactly one raw nine-U+200B Foundry category, no plain visible-equivalent category, preserved owner values except `Enable Content Configuration=true` plus exact `Black Mesa:100`, and the exact BMAFDIAG1 diagnostic DLL reused byte-for-byte. Review artifact `11218000891` / profile SHA-256 `8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5` remains Actions-only and is not published/indexed/imported/armed. The accepted normalizer remains unchanged. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN` because no BMAFR1 runtime test has occurred; the next bounded step is exact-byte publication from the frozen review artifact without rebuilding.

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


## BMAFR1I1 attribution closure and Phase C3 resumption

`Current/241_S1.42AK_BMAFR1I1_POST_RUNTIME_ATTRIBUTION_DECISION.md` closes the BMAFR1I1 repeat-run question without changing the Black Mesa x Abandoned Foundry compatibility PASS.

The correctly armed BMAFR1I1 run did not reproduce the exact array flood and did not observe the required tracked Janitor/SpringMan instances. No further BMAFR1I1 runtime attempt is authorized because another unchanged run would remain stochastic, while forcing the target conditions would materially change the experiment and requires a separate diagnostic design.

Performance attribution therefore remains unresolved and is no longer the immediate Phase C3 blocker. Phase C3 returns to selecting the next exact External-moon pairing/restriction for compatibility/safety investigation from existing repository evidence before any new build or runtime acquisition is considered.


## Phase C3 current priority — Oxyde ordinary-generation semantic restriction

`Current/242_S1.42AK_PHASE_C3_OXYDE_ORDINARY_GENERATION_PRIORITY_SELECTION.md` selects the current Oxyde ordinary-generation restriction as the next compatibility/safety analysis target.

Oxyde's 23 selection-supported metadata pairings do not currently provide executable ordinary interior pairing proof because `spawnEnemiesAndScrap=false` returns exact V81 before the normal dungeon-generation callsite and no inspected independent dungeon/entrance-construction path is established. This whole-row prerequisite takes priority over selecting another arbitrary unseen Black Mesa `MATCH`.

The next checkpoint is evidence-only: resolve exact ownership and impact of the false flag, the vanilla/LLL/Dawn paths that would become reachable if ordinary generation were enabled, CodeRebirth Oxyde-specific lifecycle assumptions, and whether entrance topology would still require another mechanism. No override, build or runtime test is authorized by the priority selection.


## Oxyde static safety decision — current exception preserved

`Current/243_S1.42AK_OXYDE_ORDINARY_GENERATION_STATIC_SAFETY_DECISION.md` completes the bounded source/static analysis selected by record 242 and supersedes its analysis-next instruction. No safe config/single-flag conversion is established: normal generation requires live generator and exterior entrance proof, while CodeRebirth retains the crane dungeon-type writer, outside-enemy classification and special ship/time semantics. Oxyde remains an explicit current-architecture exception, not a proven permanently incompatible or broken moon. Its 23 metadata matches and the historical B3 matrix remain unchanged.

Perform one bounded Phase-C3 remaining compatibility/safety priority reassessment using existing repository evidence, with the Oxyde current-architecture exception preserved under Current/243_S1.42AK_OXYDE_ORDINARY_GENERATION_STATIC_SAFETY_DECISION.md. Select and justify the next exact unresolved pairing/restriction or evidence prerequisite; do not reopen the completed Oxyde flag analysis without new evidence, implement a change, build/publish a candidate, or authorize/start a runtime run in that reassessment. Preserve BMDSFIX1 passive/outstanding/unwaived DeepSewersFlow and the closed-unresolved BMAFR1I1 attribution.

S1.42AK remains accepted; BMDSFIX1 remains active / NOT ACCEPTED with its passive, outstanding and unwaived DeepSewersFlow gate. No further BMAFR1I1 run is authorized. Build and runtime controllers are unchanged.

## Phase-C3 remaining-priority reassessment — interior-side existing-evidence refresh next

`Current/244_S1.42AK_PHASE_C3_REMAINING_PRIORITY_REASSESSMENT_INTERIOR_PROOF_REFRESH.md` completes the requested remaining compatibility/safety priority reassessment without authorizing gameplay work.

The External-moon branch is sufficiently bounded for the current architecture: Black Mesa applicability is closed at 31 MATCH / 22 NON-MATCH / 0 UNRESOLVED with existing pair-specific evidence exhausted unless new evidence is acquired, while Oxyde remains the explicit ordinary-generation exception from record 243. C2 already classified the 14 owner hard blocks without authorizing their removal.

The next prerequisite therefore returns to C1 Priority 2: refresh the exact 34 flows that record 168 listed as lacking trusted actual-generation proof against all already-ingested later/omitted repository evidence. That list is demonstrably historical rather than a current residual set because later Black Mesa work supplies concrete post-C1 proof for at least Slaughterhouse and Decrepit store. Do not select a new runtime target until the refreshed residual set is known. C1 Priority 3 route/NavMesh attribution remains subsequent and separate.

No new runtime acquisition, implementation, candidate build/publication, owner-restriction removal or controller change is authorized. Oxyde, Shatteredrooms/CullFactory, Black Mesa/Pikmin, Herobrine, BMAFR1I1 and the passive/outstanding/unwaived BMDSFIX1 DeepSewersFlow gate remain separate and unchanged.

Exact next action: Perform one bounded Phase-C interior-side existing-evidence refresh over the exact 34 flows listed in Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md as having no trusted actual-generation proof at C1. Reconcile only already-ingested repository evidence acquired after or omitted by C1; classify each flow's current generation/traversal proof status, preserve route/NavMesh signals as separate obligations, and produce a current residual proof-gap set before selecting any new runtime target. Do not acquire new runtime evidence, implement changes, build/publish a candidate, remove owner restrictions, reopen Oxyde, or turn BMDSFIX1 DeepSewersFlow into a dedicated reroll. Preserve separate Shatteredrooms/CullFactory, Black Mesa/Pikmin, Herobrine and BMAFR1I1 scopes.

## Phase-C interior-side existing-evidence refresh — residual 31

`Current/245_S1.42AK_PHASE_C_INTERIOR_EXISTING_EVIDENCE_REFRESH.md` completes the evidence-only refresh selected by record 244.

Of the exact 34 flows that C1 listed without trusted actual-generation proof, three now have positive later runtime evidence:

- `DeepSewersFlow`: DIAG1PATH1 completed generation after the exact BMDSFIX1 4.875->1 clamp and continued into normal post-generation player activity. This is bounded actual-generation evidence only; the regular selector-free BMDSFIX1 Black Mesa x Deep Sewers gameplay gate remains passive, outstanding and unwaived.
- `SlaughterhouseFlow`: two natural regular Black Mesa generations completed and materialized all three alternate inside counterparts; no direct player-traversal proof is retained.
- `StoreFlow` / Decrepit store: completed generation, four logical entrance relationships, three distinct alternate counterparts and direct bidirectional traversal of the main entrance plus two of three fire exits; RuntimeNavMeshBuilder noise remains a separate attribution signal.

The current residual set is therefore **31 flows without trusted actual-generation proof**: 19 currently viable/equal-100 flows and 12 C2 owner-hard-block flows. Black Mesa the interior remains in that residual set; later evidence about the Black Mesa moon must not be conflated with generation of the `Black Mesa` interior flow itself.

No Phase-B3 classification, owner restriction, Oxyde exception, route/NavMesh obligation, accepted/candidate lifecycle or build/runtime controller changes.

Exact next action: Perform one bounded Phase-C residual interior-proof priority-selection checkpoint over the 31 flows remaining without trusted actual-generation proof in Current/245_S1.42AK_PHASE_C_INTERIOR_EXISTING_EVIDENCE_REFRESH.md. Separate the 19 currently viable/equal-100 residual flows from the 12 C2 owner-hard-block flows, preserve each flow's owner/availability and known technical signals, and select exactly one next evidence target or prerequisite based on safety, leverage and existing-evidence availability. Do not authorize a runtime run, implementation, availability override, owner-block removal, Oxyde reopening, dedicated BMDSFIX1 DeepSewersFlow reroll, or any Black Mesa/Pikmin, Herobrine or BMAFR1I1 work in that selection checkpoint.


## Phase-C residual interior-proof priority selection — Art Gallery next

`Current/246_S1.42AK_PHASE_C_RESIDUAL_INTERIOR_PROOF_PRIORITY_SELECTION.md` completes the bounded selection checkpoint over record 245's 31 residual no-generation-proof flows.

The 19 currently viable/equal-100 residual flows remain separate from the 12 C2 owner-hard-block flows. Their existing owner/availability mechanisms and known special signals are preserved without changing Phase-B3 classifications or owner restrictions.

**Art Gallery / `MuseumInteriorFlow` on Offense** is selected as the next generation-proof evidence target. It is already `VIABLE_EQUAL_100` through the direct LLL `Vanilla:100,Custom:100` override; exact DawnLib flow resolution and accepted-runtime viable/final effective 100 presence are already proven, and current evidence preserves no Art-Gallery-specific technical warning. That leaves actual completed generation as a narrowly isolated missing proof dimension.

The 12 owner-hard-block flows are not selected because testing them on Offense would first require a separate availability/safety decision and would couple owner-block removal with generation qualification. Black Mesa interior and Shatteredrooms also carry distinct owner/scope boundaries that make them less clean as the immediate proof target.

No runtime run, implementation, availability change, owner-block removal, Oxyde reopening, BMDSFIX1 DeepSewers reroll, Black Mesa/Pikmin work, Herobrine work or BMAFR1I1 work is authorized.

Exact next action: Perform one bounded Phase-C Art Gallery (`MuseumInteriorFlow`) generation-proof acquisition preflight using existing repository/source/config/runtime-observability evidence only. Define the minimum proof contract for ordinary Offense selection, completed generation and generated entrance/materialization evidence, and determine whether existing normal-stack logging is sufficient or whether a separately versioned read-only diagnostic would be required. Do not authorize or start a runtime run, implement instrumentation, build/publish a candidate, change availability, alter owner restrictions, reopen Oxyde, reroll BMDSFIX1 DeepSewersFlow, or begin Black Mesa/Pikmin, Herobrine or BMAFR1I1 work.


## Phase-C Art Gallery generation-proof acquisition preflight — normal observability sufficient

`Current/247_S1.42AK_PHASE_C_ART_GALLERY_GENERATION_PROOF_ACQUISITION_PREFLIGHT.md` completes the bounded evidence-acquisition preflight for the selected Art Gallery / `MuseumInteriorFlow` target.

Existing normal-stack observability is sufficient; no read-only diagnostic is currently justified. The minimum proof contract is ordinary Offense selection attributable to Art Gallery, exact post-generation `MuseumInteriorFlow` identity through CullFactory tile preparation or equivalent exact-flow materialization, completed floor generation including `Players finished generating the new floor`, and the ordinary PathfindingLib four-logical-connection entrance relationship set. C1 already uses these normal observability dimensions for generated-only qualification.

Player facility entry/exit is optional for a stronger traversal tier and is not required to close the current basic no-actual-generation-proof gap. Route/NavMesh warnings remain separate proof obligations unless they concretely prevent generation/materialization.

This preflight does not authorize a runtime attempt. It also does not authorize force-selection, diagnostic instrumentation, availability changes, owner-block removal, Oxyde reopening, a dedicated BMDSFIX1 Deep Sewers reroll, or any Black Mesa/Pikmin, Herobrine or BMAFR1I1 work.

Exact next action: Perform one bounded Phase-C Art Gallery (`MuseumInteriorFlow`) ordinary-runtime acquisition authorization decision. Use the proof contract from Current/247_S1.42AK_PHASE_C_ART_GALLERY_GENERATION_PROOF_ACQUISITION_PREFLIGHT.md to decide whether one ordinary Offense acquisition attempt is justified with existing gameplay bytes and existing normal-stack observability only. Do not force-select Art Gallery, implement a diagnostic, change availability, alter owner restrictions, reopen Oxyde, dedicate a BMDSFIX1 DeepSewers reroll, or begin Black Mesa/Pikmin, Herobrine or BMAFR1I1 work. If and only if a runtime attempt is authorized, the same response must include the repository-driven Gale replacement/import PowerShell one-liner when required and the exact build-specific one-line PowerShell log uploader.


## Phase-C Art Gallery ordinary-runtime acquisition — one Offense attempt authorized

`Current/248_S1.42AK_PHASE_C_ART_GALLERY_ORDINARY_RUNTIME_ACQUISITION_AUTHORIZATION.md` authorizes exactly **one** ordinary Offense generation attempt on the unchanged exact active `S1.42AK-BMDSFIX1` gameplay profile.

This is a natural acquisition attempt only:

- no Art Gallery force-selector or target diagnostic;
- no new build/profile/config/package/DLL bytes;
- no availability or owner-block change;
- no automatic reroll if Art Gallery does not select;
- exact resulting `LogOutput.log` must be uploaded once even after a non-target roll.

The safety basis is that BMDSFIX1 applies only to Black Mesa × `DeepSewersFlow`; its application path is therefore outside the intended Offense test condition. Any unexpected `[BMDSFIX1] APPLIED` marker on Offense is a separate severe non-target finding.

Art Gallery remains stochastic in the observed 41-entry equal-effective Offense pool. A miss is not negative evidence. If `MuseumInteriorFlow` naturally selects, reconcile it against the exact record-247 generation/materialization contract; player traversal remains optional for the basic proof tier. If another flow selects, preserve only the evidence actually established for that flow.

Exact next action: Execute exactly one ordinary Offense generation attempt with the exact active S1.42AK-BMDSFIX1 profile and no Art-Gallery selector/diagnostic. Upload the resulting exact LogOutput.log once using the build-specific uploader whether or not Art Gallery selects. Do not reroll automatically if Art Gallery does not select. After ingestion, perform one bounded Phase-C runtime-evidence reconciliation: apply the Current/247 proof contract if MuseumInteriorFlow selected; otherwise treat the run as non-target evidence and assess only whatever naturally selected flow the log actually proves.

## Phase-C Art Gallery ordinary-runtime non-target reconciliation — Belleville proven, residual 30

`Current/249_S1.42AK_PHASE_C_ART_GALLERY_ORDINARY_RUNTIME_NON_TARGET_RECONCILIATION.md` reconciles the exact ingested `S1.42AK-BMDSFIX1` Offense evidence at `RuntimeEvidence/S1.42AK-BMDSFIX1/20261004T092417Z/` (raw `LogOutput.log` SHA-256 `b376bc0ff6e64b4c1ba4f99feda4cf245c2811d5c434d57cc414b7a7c3475b83`; 4,677,491 bytes / 55,259 lines).

Art Gallery / `MuseumInteriorFlow` did **not** naturally select. The first completed Offense generation selected Spelunkers Caverns (Random), so the single record-248 acquisition authorization is consumed; the target miss is not negative Art Gallery evidence and authorizes no automatic reroll. The same captured log contains later natural Offense generations of Belleville Appartements and LC Office; these are retained as incidental evidence and do not expand the authorized attempt count.

Belleville Appartements / `BellevilleApp` now has trusted ordinary Offense actual-generation/materialization proof: exact day-history selection, `Players finished generating the new floor`, CullFactory generation completion plus exact `BellevilleApp` tile preparation, and four logical PathfindingLib entrance relationships. The later player death by Spike Trap occurred after that proof chain and does not invalidate it. Belleville therefore leaves the residual no-generation-proof set. The current residual is **30 flows**: **18** currently viable/equal-100 plus the unchanged **12** C2 owner-hard-block flows. Art Gallery remains among the 18 viable residual flows.

BMDSFIX1 emitted `ARMED` but no `APPLIED` marker on Offense, so the record-248 non-target safety condition passes. This does not satisfy or waive the separate regular Black Mesa x `DeepSewersFlow` gameplay gate.

The log also strengthens a separate BCMER x LethalMin/Pikmin compatibility signal. On the SafeOutside episode, BCMER selected `SafeOutside` and logged `Outside spawning prevented by OutsideSafe`; Onion withdrawal still instantiated Pikmin, after which they were rapidly reported dead from the exterior enemy list. Later non-SafeOutside Offense episodes show the same recurring Onion staging-position NavMesh-agent warnings while Onion Pikmin nevertheless persist. The NavMesh warning is therefore a separate recurring problem rather than sufficient explanation for the SafeOutside-correlated immediate death. Exact cleanup ownership is not yet proven; a later bounded source/static compatibility analysis should identify the responsible BCMER/vanilla/Starlancer/LethalMin path before considering a narrow player-owned-Pikmin exemption. No such patch is authorized by record 249.

Exact next action: Perform one bounded Phase-C residual interior-proof priority reassessment over the updated 30-flow no-trusted-actual-generation-proof set established by Current/249_S1.42AK_PHASE_C_ART_GALLERY_ORDINARY_RUNTIME_NON_TARGET_RECONCILIATION.md. Preserve Art Gallery / MuseumInteriorFlow as unproven after the natural target miss, remove Belleville Appartements / BellevilleApp from the residual set based on its completed ordinary Offense generation/materialization proof, keep the 12 C2 owner-hard-block flows unchanged, and select exactly one next evidence target or prerequisite. Do not authorize or start another runtime run, force-select Art Gallery, implement gameplay/config changes, alter availability/owner restrictions, reopen Oxyde, reroll BMDSFIX1 DeepSewersFlow, or begin the separate BCMER x LethalMin/Pikmin compatibility work in that reassessment.

## Deterministic single-interior runtime qualification strategy

`Current/250_PHASE_C_DETERMINISTIC_INTERIOR_TEST_STRATEGY_AND_DEFERRED_BCMER_PIKMIN_DIRECTIVE.md` records the user-directed test-method rule for the remaining Phase-C interior work.

When a specific interior is selected and separately authorized for runtime qualification, do **not** rely on stochastic dungeon selection. Use a separately versioned diagnostic-only selector or equivalent narrowly scoped mechanism that deterministically selects the exact target flow while preserving the target's normal generation/materialization semantics as far as possible.

This does not authorize bypassing owner/availability restrictions. An `AUTHOR_OR_OWNER_HARD_BLOCK` flow still requires a separate explicit availability/safety authorization before any deterministic selector may make that flow executable for the test.

If Art Gallery / `MuseumInteriorFlow` is selected again after the current residual-priority reassessment, its next runtime acquisition should therefore force `MuseumInteriorFlow` rather than repeat an ordinary random Offense roll.

The same directive preserves BCMER x LethalMin/Pikmin as a **deferred-but-mandatory follow-up scope**. Before implementing a fix, attribute the exact cleanup/suppression path across BCMER, LethalMin, vanilla outside-enemy/list handling and observed interceptors such as Starlancer AI Fix. If supported, prefer a narrow player-owned-Pikmin exemption from hostile outside-enemy suppression/cleanup over globally disabling BCMER events.

## BCMER x LethalMin scope correction — all Pikmin, not ownership-limited

`Current/251_BCMER_LETHALMIN_ALL_PIKMIN_EXEMPTION_SCOPE_CORRECTION.md` supersedes only the player-ownership limitation in the earlier deferred BCMER/Pikmin wording.

The eventual compatibility target is now explicit: **Pikmins generally** should be exempt from BCMER outside-enemy suppression/cleanup that would otherwise kill, remove, block or invalidate them solely because they participate in an exterior-enemy path/list. The exemption should be based on Pikmin identity/classification, not whether a Pikmin is currently player-owned, following a player, idle, Onion-withdrawn, plucked or otherwise assigned.

Ordinary hostile non-Pikmin outside-enemy suppression should remain intact if a narrow safe exemption can be implemented. The exact destructive owner remains unresolved and still requires bounded source/static attribution before any patch.

This correction does not authorize implementation or a runtime test and does not change the current 30-flow Phase-C priority-reassessment next action.

## Phase-C residual-30 priority reassessment — deterministic Art Gallery selector preflight next

`Current/252_S1.42AK_PHASE_C_RESIDUAL_30_PRIORITY_REASSESSMENT.md` completes the bounded reassessment over the record-249 residual set.

The residual remains **30 flows**: **18** currently viable/equal-100 and the unchanged **12** C2 owner-hard-block flows. Belleville Appartements / `BellevilleApp` remains outside the residual on its trusted ordinary Offense generation/materialization proof. Art Gallery / `MuseumInteriorFlow` remains unproven because the earlier natural attempt did not select it; that stochastic miss is not negative compatibility evidence.

The previous Art Gallery priority is therefore retained. Its availability is already valid on Offense, its exact flow/pool evidence and record-247 proof contract are unusually mature, and no Art-Gallery-specific technical warning is preserved. Switching to another viable residual solely because the random roll missed would not reduce the new method prerequisite: record 250 requires deterministic exact-target selection for every future single-interior qualification.

The exact selected next prerequisite is a **bounded source/static reuse/design preflight for a separately versioned diagnostic-only deterministic `MuseumInteriorFlow` selector on Offense**. The preflight must identify the narrowest safe existing selector precedent, preserve normal generation/materialization semantics, define fail-closed guards and diagnostic identity, and must not implement or activate the selector.

The 12 owner-hard-block flows remain unavailable for incidental selector bypass. Their availability/safety question must be separately authorized before any deterministic qualification.

No runtime run, build/profile/config/DLL/package change, availability change, owner-block removal, Oxyde reopening, BMDSFIX1 Deep Sewers reroll, BCMER × Pikmin work, Herobrine work or BMAFR1I1 work is authorized.

Exact next action: Perform one bounded Phase-C Art Gallery deterministic-selector source/static reuse/design preflight for `MuseumInteriorFlow` on Offense using existing repository evidence only. Identify the narrowest separately versioned diagnostic-only mechanism that can deterministically select the exact flow while preserving the already-valid Offense availability and normal generation/materialization semantics. Reuse existing selector precedent where safe, define fail-closed guards and diagnostic identity requirements, and decide whether a target-specific successor can be designed without unrelated gameplay changes. Do not implement/build/publish/activate a selector, authorize/start a runtime run, change availability or owner restrictions, reopen Oxyde, reroll BMDSFIX1 DeepSewersFlow, or begin BCMER × Pikmin, Herobrine or BMAFR1I1 work.

## Phase-C Art Gallery deterministic-selector preflight — selector-only BMDSFIX1-DIAG1 pattern selected

`Current/253_S1.42AK_PHASE_C_ART_GALLERY_DETERMINISTIC_SELECTOR_PREFLIGHT.md` completes the bounded source/static reuse/design preflight selected by record 252.

The narrowest safe mechanism is the proven **BMDSFIX1-DIAG1 selector-only architecture**: exactly one postfix on LLL's exact `GetValidExtendedDungeonFlows(ExtendedLevel, bool)`, ordered after the accepted S1.42AB normalizer at `Priority.Last`. On the real server-selection path and exact moon `Offense`, it must verify that one already-viable `Art Gallery` wrapper exists, its exact flow asset is `MuseumInteriorFlow`, and its post-normalizer rarity is exactly `100`; only then may it reduce that fresh returned list to the same wrapper as a singleton.

No `EntranceTeleport` observer is required. Record 247 already proves normal-stack logging is sufficient for the basic generation/materialization proof, so the larger Greenhouse/Foundry traversal-observer architecture would add unnecessary interception surface.

Record 250 supersedes only record 247's earlier natural/no-force-selection clause for future single-interior qualification. A later deterministic run still must satisfy the record-247 generation-completion, exact-flow materialization and normal PathfindingLib entrance-relationship requirements. A pass may close Art Gallery's no-trusted-actual-generation-proof gap at a **diagnostic-generated** tier, analogous to the project's Deep Sewers treatment; it does not prove natural selection frequency or make the selector acceptable gameplay content.

No implementation, build, publication, Gale import or runtime is authorized. The selector may not alter availability, owner restrictions, rarity, registration, RNG, RPC ownership, generation size, entrances, NavMesh, scrap/enemies or BCMER semantics. Any later diagnostic profile should derive from exact active `S1.42AK-BMDSFIX1`; BMDSFIX1 remains NOT ACCEPTED and any unexpected `[BMDSFIX1] APPLIED` on Offense remains an isolation failure. A future Gale profile identity should be deliberately short from its first review build to avoid the already-proven Windows diagnostic path-length problem.

Exact next action: Perform one bounded Art Gallery deterministic-selector source/static implementation authorization decision. Freeze the separately versioned diagnostic build/plugin/marker identity, confirm exact parent provenance and the selector-only one-postfix contract from Current/253_S1.42AK_PHASE_C_ART_GALLERY_DETERMINISTIC_SELECTOR_PREFLIGHT.md, and decide whether to authorize source/static implementation plus pure fail-closed tests/validator infrastructure. Do not implement/compile/build/publish/import/activate/run the diagnostic in that authorization decision, do not change availability or owner restrictions, and do not begin BMDSFIX1 Deep Sewers, BCMER x Pikmin, Herobrine or BMAFR1I1 work.

