<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-05  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

## Latest built artifact

**S1.42AD — Functional Microwave Spawn Rarity Reduction — BUILD PASS RUNTIME VALIDATION OPEN NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`  
SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`  
Candidate record: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AD**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AD_BUILD_AWAITING_RUNTIME_VALIDATION`)
- Guarded build base: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z` / `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AD`

## Exact next action

S1.42AD is built and is the active runtime candidate. Replace/import the Gale profile with LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction using the canonical repository helper, run one normal gameplay round far enough for normal moon/interior generation, then upload the complete fresh LogOutput.log using the exact S1.42AD uploader in Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md. Runtime acceptance must confirm dependency validation, PrioritiseMoons=true with 18 Moon curves and 0 Interior curves, the final x0.5 application marker, normal gameplay and no contract-refusal/fatal regression. Do not build a successor before this evidence is analyzed.

A runtime test is pending for S1.42AD. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
