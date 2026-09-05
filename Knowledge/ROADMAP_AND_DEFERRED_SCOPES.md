# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Runtime acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`. There is no active candidate and no runtime test outstanding. Successor armed: **no**. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`; `BuildSpecs/current.json` is disabled and guards the accepted S1.42AF base.

S1.42AD remains runtime-rejected historical provider-contract evidence. S1.42AE remains superseded for packaging after its physically present SoundAPI binding was blocked through a 262-character runtime path. S1.42AF reused the corrected source on a 226-character path and passed both normal startup and the exact 18 Moon / 18 Interior Functional Microwave runtime contract.

## Exact next scope

The selected work is **Mouth Dog / Eyeless Dog -> Pikmin compatibility source-contract analysis**, not a build yet.

The S1.42AF acceptance run proves that a Mouth Dog can currently bite/grab Pikmin and start their death timers. Invincibility prevents the final kill but does not prevent harmful state mutation; the two affected White Pikmin then produced 707 `Work state with no task assigned!` warnings. This is a separate baseline-resident compatibility finding, not an S1.42AF regression. Authority: `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`.

The next ChatGPT must inspect the exact LethalMin MouthDog/EyelessDog owner/method/inheritance/config path and the current exact `PikminAI.GrabPikmin(Transform,float,int)` prevention-only guard in `Patches/S139CompatibilityFixes/Plugin.cs`. The intended one-way rule is Mouth Dog -> Pikmin targeting/bite/grab/kill blocked before state mutation while Pikmin -> Mouth Dog combat remains native unless exact source evidence proves otherwise. Follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. **Do not arm or build a successor until the exact contract is proved.**

## Remaining deferred independent gameplay/compatibility scopes

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- broader LethalMin teardown/despawn repair only with stronger evidence beyond the now-selected Mouth Dog interaction.

## BCMER scope boundary

S1.42AC remains the accepted historical BCMER 1.71.0 static EventType-probability implementation inherited by S1.42AF. Exact long-run executed EventType frequency after runtime eligibility filters is a broader algorithm-design scope and is not armed.

## Interior scope boundary

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AF does not alter that path. Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
