# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`, `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`  
**Related:** `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline remains **S1.42AC — BCMER EventType Equal Distribution**.

Latest built artifact and active candidate is **S1.42AF — Path-Length-Safe Microwave Packaging**. Its targeted Microwave/provider/path-length runtime gate is complete and **PASS**. S1.42AF is not runtime-rejected, but formal full-stack acceptance is deferred because the same normal run exposed a separate Mouth Dog / Eyeless Dog -> Pikmin compatibility gap and a large `Work state with no task assigned!` burst.

No new S1.42AF runtime test is pending. No successor is armed or named.

## Exact next scope

The selected work is **Mouth Dog / Eyeless Dog -> Pikmin baseline compatibility analysis**.

Authority: `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`.

Required behavior:

- Mouth Dog / Eyeless Dog must not grab or bite Pikmin at all;
- Pikmin -> Mouth Dog combat remains native LethalMin behavior;
- native enemy death, unlatch, task completion and related lifecycle must remain intact.

Investigation order is binding:

1. inspect LethalMin `1.1.108` configuration for an exact native one-way noninteraction contract;
2. if configuration is insufficient, identify the exact Mouth-Dog adapter/collision/bite/grab owner and method path;
3. prefer prevention before `GrabPikmin` or equivalent state mutation;
4. follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
5. only after the exact contract is proven, prepare an isolated build plan and then choose a successor ID.

Do not rerun S1.42AF just to repeat its completed Microwave gate, and do not invent `S1.42AG` or any other successor before analysis establishes a buildable delta.

## Why the Mouth-Dog issue is separate from S1.42AF's Microwave delta

S1.42AF was built directly from accepted S1.42AC. Automated archive verification found only the Gale profile-name change in `export.r2x` plus the added Microwave tuning DLL; there were no mod or config changes.

The cumulative compatibility DLL is byte-identical in S1.42AC and S1.42AF: `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`, SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`. Current source has prevention branches for Crawler/Thumper and Baboon Hawk but none for Mouth Dog. The current classification is therefore a pre-existing/baseline compatibility gap exposed during S1.42AF, not evidence that the Microwave tuning caused it.

## Remaining deferred independent gameplay/compatibility scopes

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- broader LethalMin teardown/despawn repair only with stronger evidence beyond the currently selected Mouth-Dog interaction gap.

## BCMER scope boundary

S1.42AC remains the accepted BCMER `1.71.0` static EventType-probability implementation. Exact long-run executed EventType frequency after runtime eligibility filters is a broader algorithm-design scope and is not armed.

## Interior scope boundary

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AC and S1.42AF do not alter that path. Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
