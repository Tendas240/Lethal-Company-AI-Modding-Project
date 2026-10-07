# C3F19 BMAFDIAG1 Source/Static Implementation Findings

**Date:** 2026-09-30  
**Status:** IMPLEMENTED ON DEDICATED SOURCE BRANCH / STATIC PR GATE PENDING / NO BUILD / NO PUBLICATION / NOT RUNTIME-ARMED  
**Scope:** Black Mesa x Abandoned Foundry pair-specific diagnostic only

## Implemented successor

A separately versioned `S1.42AK-BMAFDIAG1` source tree is prepared under `Patches/S142AKBMAFDiag1/`.

Its external identity is:

- assembly/project: `S142AKBMAFDiag1`;
- BepInEx GUID: `tendas.lethalcompany.s142akbmafdiag1`;
- marker prefix: `[BMAFDIAG1]`;
- version: `1.0.0`;
- target: exact `Black Mesa` x `Abandoned Foundry` / `FoundryFlow`.

Any later review profile, if separately authorized, must derive directly from exact accepted S1.42AK SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`. BMGHDIAG3 and BMDSFIX1 are not profile parents.

## Preserved diagnostic architecture

BMAFDIAG1 reuses the proven BMGHDIAG3 architecture at source-contract level:

- exact installed V81 `Assembly-CSharp.dll` provenance from `Paths.ManagedPath` with SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- exact LethalLevelLoader `1.7.12` hash contract;
- accepted S1.42AB normalizer hash contract and after-normalizer ordering;
- structural `EntranceTeleport` runtime identity without the disproven manifest-module filename equality;
- exactly two Harmony postfix surfaces;
- same-wrapper post-filter selection mutation only after validation;
- read-only post-native `TeleportPlayer()` observation;
- topology and traversal observation for required IDs 0..3;
- diagnostic-only / NEVER ACCEPT semantics.

The runtime plugin contains no LLL config writer, no availability insertion, no flow registration hook and no universal-availability logic.

## Foundry-specific target delta

The selection policy now requires exactly one viable wrapper whose:

- `DungeonName` is exactly `Abandoned Foundry`;
- exact flow asset name is `FoundryFlow`;
- already-normalized rarity is exactly `100`;
- current moon is exactly `Black Mesa`;
- call stack contains the exact LLL server-selection caller and not terminal simulation.

Only after all checks pass may the plugin retain that exact wrapper and reduce the fresh returned list to the singleton. No fixed pre-reduction pool size is asserted.

If Foundry is absent, duplicated, differently named, differently weighted or reached through an unrecognized caller, the diagnostic refuses selection rather than adding/fixing availability.

## Owner-config evidence boundary

Repository-native owner-default evidence comes from:

`RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg`

The owner-generated `Custom Dungeon:  Abandoned Foundry` section has content configuration disabled, dynamic-size restriction disabled, 1/1/1 size values, empty/default Mod Names and Route Price mappings, the owner Manual Level Names table, and `Murica:300,Canyon:50,Wasteland:150` tags.

The accepted S1.42AK LLL config has no direct Abandoned Foundry section. A later review build therefore requires a separately validated config-materialization step.

The only permitted semantic availability change for that future step is:

1. materialize the owner-default Foundry section without changing its owner values;
2. set `Enable Content Configuration = true`;
3. add exactly `Black Mesa:100` to the existing Manual Level Names mapping.

No `External:100`, new tag, Mod Names rule, Route Price rule, size-rule change, duplicate section or duplicate registration is authorized.

No config file is changed in this source/static checkpoint.

## Runtime proof boundary

Source/static validity is not pair compatibility. A later exact-byte runtime gate must still prove:

- BMAFDIAG1 arms without refusal;
- LLL returns Foundry as viable before diagnostic list reduction;
- accepted normalization has already produced rarity `100`;
- generation completes;
- topology IDs 0..3 form unique outside/inside pairs;
- player traverses ID 0 and IDs 1..3 in both directions;
- required entrance geometry is accessible without severe clipping/stranding;
- no severe persistent pair-attributable routing/NavMesh failure is established;
- no required diagnostic `REFUSED`, `TOPOLOGY_INCONCLUSIVE` or `TRAVERSAL_INCONCLUSIVE` condition occurs.

Historical Foundry-on-Offense traversal and BMGHDIAG3 Greenhouse-on-Black-Mesa evidence are supporting architecture evidence only; neither pre-qualifies this exact pair.

## Live-state preservation

This implementation does not change lifecycle/controller ownership:

- accepted baseline remains `S1.42AK`;
- active gameplay candidate remains `S1.42AK-BMDSFIX1` / not accepted;
- BMDSFIX1 Black Mesa x DeepSewersFlow gate remains outstanding/passive/unwaived;
- `BuildSpecs/current.json` remains disabled;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- BMAFDIAG1 is not built, published, Gale-imported or runtime-armed.

No CI/static PASS is claimed by this file. That result belongs to the subsequent PR validation checkpoint.
