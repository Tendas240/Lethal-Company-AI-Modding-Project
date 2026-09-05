# 129 — Mouth Dog / Pikmin Baseline Compatibility Gap — Next Analysis Contract

**Date:** 2026-09-06  
**Status:** CURRENT SELECTED ANALYSIS / NO SUCCESSOR ARMED  
**Parent lifecycle decision:** `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`

## Problem statement

During the completed S1.42AF normal runtime run, a Mouth Dog / Eyeless Dog was directly observed interacting with Pikmin through the enemy bite/grab path. The same run later produced a large `Work state with no task assigned!` burst from LethalMin.

The project requirement is not merely to prevent Pikmin death after the grab has already mutated state. The required behavior is stronger and prevention-oriented:

**Mouth Dog / Eyeless Dog -> Pikmin bite/grab interaction must not begin at all.**

The reverse direction remains intentionally native:

**Pikmin -> Mouth Dog combat remains owned by LethalMin**, including enemy death handling, unlatch/task completion, corpse behavior and all existing native lifecycle unless exact analysis proves a separate defect.

## Why this is classified as a baseline gap rather than an S1.42AF regression

S1.42AF was built directly from accepted S1.42AC and its automated archive delta is isolated to:

- changed existing member: `export.r2x`;
- added member: `BepInEx/plugins/S142AECodeRebirthMicrowaveSpawnTuning/S142AECodeRebirthMicrowaveSpawnTuning.dll`;
- mod-state changes: `0`;
- mod additions: `0`;
- mod removals: `0`;
- config changes: `0`.

The existing cumulative compatibility DLL is byte-identical between S1.42AC and S1.42AF:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

- size: `57344` bytes;
- SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`.

Current source in `Patches/S139CompatibilityFixes/Plugin.cs` installs a prevention-only prefix on exact declared `LethalMin.PikminAI.GrabPikmin(Transform,float,int)`, but its current source classification blocks only:

- Crawler / Thumper snap positions;
- Baboon Hawk / Baboon Bird snap positions.

Mouth Dog is not part of that guard. Therefore the currently accepted compatibility contract already lacks a Mouth-Dog-specific prevention branch; S1.42AF did not introduce that omission.

## Required investigation order

Follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and do not guess from class names.

1. **Inspect LethalMin 1.1.108 configuration first.** Determine whether a native setting already exists that disables Mouth Dog / Eyeless Dog interaction with Pikmin in the required one-way direction without disabling Pikmin attacks on the dog.
2. **If configuration is insufficient, inspect exact runtime/source ownership.** Identify the LethalMin Mouth Dog adapter type(s), their exact declared collision/bite/grab methods, and whether they ultimately call the common `PikminAI.GrabPikmin(Transform,float,int)` path.
3. **Determine the earliest safe prevention point.** Prefer a prefix that returns before leader/grab/death-timer/task state mutates. Do not repair follower state after mutation if a deterministic prevention point exists.
4. **Preserve native reverse-direction lifecycle.** Do not disable an entire `PikminEnemy`-derived adapter or its inherited `Update()` path merely to stop dog bites; S1.42R already proved why broad component disable is unsafe for Baboon Hawk death/unlatch behavior.
5. **Only after the exact contract is proven, prepare an isolated build plan.** Do not name or arm a successor before the delta, base, compile references, validation assertions and focused runtime gate are explicit.

## Candidate implementation shapes — not yet authorized as a build

The preferred order is:

1. native LethalMin config solution, if it exactly satisfies the asymmetric contract;
2. otherwise, a narrow extension of the existing `LethalMinEnemyGrabPrevention` / exact Mouth-Dog adapter prevention architecture in `Patches/S139CompatibilityFixes/Plugin.cs`;
3. avoid broad enemy disable, delayed state restoration, continuous global scanning, or guessed reflection fallback.

A common `GrabPikmin` snap-position classification may be sufficient **only if exact source/runtime analysis proves Mouth Dog uses that path and the snap transform can be identified unambiguously**. If the Mouth Dog has a separate pre-grab bite/collision entry point, that entry point may also need a narrow prefix analogous to the accepted Baboon Hawk design.

## Focused runtime acceptance contract for any future fix

A future build should not be considered accepted from startup/compile success alone. The focused gate must prove at minimum:

- Mouth Dog encounters Pikmin repeatedly without grabbing, biting or starting the broken held/death-timer state;
- no `Work state with no task assigned!` burst is produced by the tested dog interaction;
- Pikmin can still attack Mouth Dogs normally;
- Mouth Dog death while Pikmin are attacking does not leave Pikmin latched or task-stuck;
- normal leader/follow, throw, item carry and Onion/task behavior still work after the encounter;
- existing Thumper/Crawler, Puffer and Baboon Hawk one-way protections remain intact;
- Compatibility Fixes Error marker remains zero;
- Fatal remains zero.

## Current lifecycle while this analysis is open

- accepted baseline: **S1.42AC**;
- latest built artifact / active candidate: **S1.42AF**;
- S1.42AF targeted Microwave/path-length runtime gate: **PASS**;
- S1.42AF formal full-stack acceptance: **deferred, not rejected**;
- runtime test outstanding: **no**;
- successor armed: **no**;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`;
- `BuildSpecs/current.json`: disabled, guarded against accepted S1.42AC.

The next ChatGPT chat should begin with this analysis rather than rerunning S1.42AF or inventing a successor ID.
