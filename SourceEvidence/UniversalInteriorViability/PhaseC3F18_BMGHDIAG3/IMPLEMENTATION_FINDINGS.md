# C3F18 BMGHDIAG3 Source/Static Implementation Findings

**Date:** 2026-09-27  
**Status:** IMPLEMENTED ON DEDICATED SOURCE BRANCH / STATIC PR GATE PENDING / NO BUILD / NO PUBLICATION / NOT RUNTIME-ARMED  
**Scope:** Black Mesa x Greenhouse diagnostic successor only  
**Root-cause authority:** `Current/193_S1.42AK_BMGHDIAG2_RUNTIME_IDENTITY_ROOT_CAUSE_RECONCILIATION.md`

## Implemented successor

A separately versioned `S1.42AK-BMGHDIAG3` source tree is prepared under `Patches/S142AKBMGHDiag3/`.

Its external successor identity is:

- assembly/project: `S142AKBMGHDiag3`;
- BepInEx GUID: `tendas.lethalcompany.s142akbmghdiag3`;
- marker prefix: `[BMGHDIAG3]`;
- version: `1.0.0`.

Any later profile construction, if separately authorized, must derive directly from exact accepted S1.42AK SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`. BMGHDIAG2 bytes and BMDSFIX1 bytes are not profile parents for this diagnostic line.

## Exact behavioral delta

The BMGHDIAG2 runtime observation contract previously passed `runtimeAssembly.ManifestModule.Name` into `RuntimeIdentityPolicy.ValidateAssemblyIdentity(...)`, which then required exact equality with `Assembly-CSharp.dll`.

BMGHDIAG3 removes only that argument and equality.

The runtime observation contract still requires:

- non-null `EntranceTeleport` runtime type;
- non-null declaring runtime assembly;
- non-null `runtimeAssembly.ManifestModule`;
- exact type full name `EntranceTeleport`;
- exact declaring assembly simple name `Assembly-CSharp`;
- non-dynamic declaring assembly;
- exact declared public instance `TeleportPlayer()` / zero parameters / `void` / method body;
- exact fields `entranceId : int`, `isEntranceToBuilding : bool`, `exitScript : EntranceTeleport`.

No observed/guessed module-name replacement, `ScopeName`, MVID/`ModuleVersionId`, metadata token, loaded-game `Assembly.Location`, `CodeBase`, process-module identity or other substitute runtime predicate is introduced.

## Preserved physical provenance

Physical installed V81 source provenance remains separate and unchanged:

- canonical source: `Paths.ManagedPath/Assembly-CSharp.dll`;
- expected SHA-256: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- no recursive search, current-directory probing, guessed Steam path or loaded-game Location/CodeBase fallback.

## Preserved diagnostic behavior

BMGHDIAG3 retains the predecessor contracts for:

- exact LethalLevelLoader `1.7.12` / SHA-256 `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted normalizer `1.0.0` / SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- exact `GetValidExtendedDungeonFlows(ExtendedLevel, bool)` contract;
- server-selection caller requirement and terminal-simulation exclusion;
- one unique existing `Greenhouse` / `GreenhouseFlow` wrapper at normalized rarity 100;
- post-normalizer `Priority.Last` selection ordering;
- same-wrapper fresh-list reduction only after all validation succeeds;
- exact declared `EntranceTeleport.TeleportPlayer()` read-only postfix;
- IDs 0..3 traversal coverage and topology observation;
- exactly two Harmony postfix surfaces;
- diagnostic-only / NEVER ACCEPT semantics.

## Repository-only static guard

`AnalysisTools/validate_s142ak_bmghdiag3_source.py` is prepared to verify the successor as a deterministic transformation of BMGHDIAG2 source:

- provenance/selection/observation helpers may differ only by successor namespace;
- `RuntimeIdentityPolicy.cs` may differ only by successor namespace plus removal of the manifest-module filename argument/guard;
- `Plugin.cs` may differ only by successor namespace/identity markers plus removal of the corresponding call-site argument;
- no broader Harmony/reflection mutation surface is permitted;
- live controllers must remain unchanged.

The companion PR workflow runs only that Python repository-text validator. It intentionally does not invoke a compiler, profile builder, artifact publication, Gale operation or runtime action.

## Live-state preservation

This implementation does not change live lifecycle/controller ownership:

- accepted baseline remains `S1.42AK`;
- active gameplay candidate remains `S1.42AK-BMDSFIX1` / not accepted;
- BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding but passive;
- `BuildSpecs/current.json` remains disabled on `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- BMGHDIAG3 is not built, not published, not Gale-imported and not runtime-armed.

No CI/static PASS is claimed by this file. That result belongs to the subsequent pull-request validation checkpoint.
