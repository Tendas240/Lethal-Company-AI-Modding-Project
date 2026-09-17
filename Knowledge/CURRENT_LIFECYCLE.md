<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AI candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `RuntimeEvidence/S1.42AI/20260916T180452Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-17

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** is the sole current accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

S1.42AH remains the accepted predecessor and rollback provenance baseline, but it is no longer the current gameplay baseline.

## Acceptance result

The independent full-normal S1.42AI gate passed after the completed DIAG1/R1/R2/R3 diagnostic chain. The real BCMER `ShyGuy` event path was exercised; interior ShyGuy availability remained functional; `ShyGuyDef` stayed at zero exterior weight/spawn contribution; and no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker attributable to the event occurred.

Static evidence proves the semantic delta remains exactly the three `[ShyGuy]` exterior BCMER values while the event, EventType, interior values, package state and ordinary Scopophobia `SpawnOutside=false` contract are preserved.

The observed ShyGuy `InvalidOperationException` and disconnect/teardown AdditionalNetworking fatal are retained as real evidence. Attribution review found neither is caused by the S1.42AI three-value exterior-config delta, so neither fails the build-specific acceptance gate.

## Completed diagnostic evidence

**S1.42AI-DIAG1R3** remains diagnostic runtime-pass evidence only. DIAG1, R1 and R2 remain failed diagnostic predecessors. None of these diagnostic artifacts is a gameplay baseline or active candidate.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AI**.
- Active runtime candidate: **none**.
- Runtime test outstanding: **no**.
- Selected successor scope: **LC Office V81 Integration — READY FOR SUCCESSOR PREPARATION / NOT ARMED**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_ACCEPTANCE_PREP_LC_OFFICE_V81_SUCCESSOR`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` remains the runtime-evidence attribution build and does not arm a successor.
- No successor build is armed.

## Selected successor scope

LC Office V81 Integration is explicitly selected under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md` and `Knowledge/INTERIORS_AND_LLL.md`. Selection does not assign a successor build ID, enable `BuildSpecs/current.json`, alter `RuntimeInbox/ACTIVE_BUILD.txt`, or create a runtime test.

The initial integration remains compatibility-first: preserve modern `IAmBatby-LethalLevelLoader` ownership and the accepted post-viability normalization to effective rarity `100`; do not combine universal LC Office moon availability, Wesley changes, CullFactory work, or other deferred scopes into this successor.

## LC Office pre-build baseline verification

The focused accepted-S1.42AI package/dependency verification is complete.

Repository evidence from `ProfileSources/S1.42AI/export.r2x` confirms the required infrastructure is already enabled at the intended versions, including `BepInEx-BepInExPack 5.4.2305`, `Evaisa-FixPluginTypesSerialization 1.1.4`, `IAmBatby-LethalLevelLoader 1.7.12`, `MaxWasUnavailable-LethalModDataLib 1.2.2`, `JacobG5-JLL 1.10.1`, `Zaggy1024-SmartEnemyPathfinding 0.0.4` and `Zaggy1024-PathfindingLib 2.4.1`.

The accepted export also proves:

- `Alice-DungeonGenerationPlus 1.5.0` is enabled and is the version to transition to `1.5.1`;
- `Piggy-LC_Office`, `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix` and `JacobG5-DestroyItemInSlotFix` are absent and therefore remain the three additions;
- `pacoito-LethalLevelLoaderUpdated` is absent;
- `pacoito-itolib 0.9.3` is present/enabled and is unrelated to the forbidden LLL fork, so it must not be removed merely because of its author prefix;
- `ProfileSources/S1.42AI/FILE_INDEX.json` records `BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll` at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

This fixes the intended minimal successor delta to the three package additions plus the `DungeonGenerationPlus 1.5.0 -> 1.5.1` transition. Dependency resolution during the actual build must still prove that no unintended package cascade or second LLL owner was introduced.

## Permanent Gale profile replacement/import route

For any future runtime candidate that is explicitly armed, the canonical Gale profile replacement/import workflow remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, with the permanent fail-closed helper revision contract `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The detailed workflow authority is `Knowledge/GALE_PROFILE_WORKFLOW.md`.

The current S1.42AI state has no runtime test outstanding, so this permanent route does not itself instruct an import, arm a candidate, or require another gameplay run. It becomes operational only after a future candidate is explicitly prepared and armed by the repository lifecycle.

## Exact next project action

Read `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Current/BUILD_LINEAGE.md`, determine the next successor build ID and exact `BuildSpecs/current.json` schema, then prepare and arm exactly one LC Office successor from exact accepted S1.42AI. Do not arm a runtime test until the built candidate passes static validation, and do not combine universal interior availability or unrelated deferred scopes.
