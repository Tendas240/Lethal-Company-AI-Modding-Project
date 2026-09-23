# C3F18 — BMGHDIAG1 Startup Refusal Root Cause / BMGHDIAG2 Provenance-Safe Successor Design

**Status:** ROOT CAUSE ESTABLISHED / MINIMAL SUCCESSOR DESIGN FIXED / NOT BUILT / NOT PUBLISHED / NOT RUNTIME-ARMED  
**Date:** 2026-09-23  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Starting main HEAD:** `595a5c1600ef7f79f76fe35734c45b5c14071d68`  
**Failed diagnostic evidence:** `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`  
**Failed diagnostic decision:** `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`  
**Failed implementation:** `Patches/S142AKBMGHDiag1/Plugin.cs`  
**Installed-V81 provenance:** `SourceEvidence/VanillaV81/EntrancePairing/20260920T201535Z-930a43a4/MANIFEST.json`

## Bounded objective

Determine why exact published `S1.42AK-BMGHDIAG1` refused before arming and fix only that provenance-resolution defect without weakening the installed-V81 observation guard or changing the Black Mesa x Greenhouse selection/observation scope.

No gameplay candidate, Gale profile replacement, runtime test, universal-interior override, Black Mesa ownership change, Greenhouse availability change, S1.42AB normalization change, B3 change, Shatteredrooms change or Black-Mesa/Pikmin routing change is authorized by C3F18.

## Root cause established

`BMGHDIAG1` resolves `EntranceTeleport` from the loaded runtime assembly and then calls:

`ValidateAssemblyHash(entranceTeleportType.Assembly, GameAssemblySha, "Assembly-CSharp.dll")`.

`ValidateAssemblyHash` obtains only `assembly.Location`, requires that string to be non-empty and an existing file, and hashes that file. The ingested runtime refusal is exactly:

`Cannot hash loaded assembly: Assembly-CSharp.dll`.

Therefore the failure occurs before SHA-256 comparison. The runtime evidence does not show a wrong V81 hash and does not show an `EntranceTeleport` signature mismatch.

The exact installed-V81 evidence binds SHA-256

`5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`

to the physical source file:

`Lethal Company_Data/Managed/Assembly-CSharp.dll`

for Steam build ID `22825947`.

The modded runtime log separately proves that `Assembly-CSharp.dll` is processed by the BepInEx/preloader/MonoMod stack before normal plugins initialize. The installed capture never established that the later reflection `Assembly` object must preserve a usable `Assembly.Location` pointing back to that physical source file.

**Root cause:** BMGHDIAG1 incorrectly conflates two distinct provenance objects:

1. the physical installed V81 source binary whose hash is known; and
2. the runtime-loaded `Assembly-CSharp` reflection assembly after the preloader/assembly-loading pipeline.

The original fail-closed behavior was correct. The defect is only the assumption that object (2) must provide a hashable path to object (1) through `Assembly.Location`.

## Minimal successor identity

The separately versioned successor is fixed as:

- build ID: `S1.42AK-BMGHDIAG2`;
- assembly/project namespace: `S142AKBMGHDiag2`;
- plugin GUID: `tendas.lethalcompany.s142akbmghdiag2`;
- plugin version: `1.0.0`;
- marker prefix: `[BMGHDIAG2]`;
- parent: exact accepted S1.42AK only.

BMGHDIAG1 remains failed diagnostic evidence and is never reused as a gameplay or diagnostic binary parent.

## Provenance-safe split contract

BMGHDIAG2 must validate **installed binary provenance** and **loaded runtime target identity** separately.

### A. Installed binary provenance gate

The exact source binary to hash is the canonical BepInEx managed-directory path, not `entranceTeleportType.Assembly.Location`.

Implementation contract:

1. obtain the repository-pinned BepInEx `Paths.ManagedPath` value;
2. canonicalize it with `Path.GetFullPath`;
3. require that managed directory to exist;
4. construct exactly `Path.Combine(managedPath, "Assembly-CSharp.dll")`;
5. require that exact file to exist;
6. compute SHA-256 of that exact file;
7. require exact match with `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
8. fail closed on any missing path/file, I/O exception or hash mismatch.

No current-directory probe, recursive filesystem search, Steam-library guessing, `Assembly.CodeBase` fallback, loaded-module path guessing or silent alternate file is permitted.

The implementation compile gate must prove the pinned `BepInEx.Core 5.4.21` API exposes the required managed-path surface before any profile build is authorized.

### B. Loaded runtime target identity gate

The runtime `EntranceTeleport` target remains resolved from the actually loaded process state and must independently satisfy all of the following before Harmony installation:

- `AccessTools.TypeByName("EntranceTeleport")` resolves exactly one usable type;
- `FullName == "EntranceTeleport"`;
- declaring assembly simple name is exactly `Assembly-CSharp`;
- the loaded assembly is not dynamic;
- `ManifestModule.Name == "Assembly-CSharp.dll"`;
- exact declared public instance `TeleportPlayer()` exists;
- zero parameters;
- return type `void`;
- method body present;
- exact `entranceId : Int32`, `isEntranceToBuilding : Boolean`, and `exitScript : EntranceTeleport` declared fields remain present.

This gate does **not** claim that the preloader-processed runtime assembly is byte-identical to the physical source file. It establishes instead that the installed base binary is exact V81 while the actual loaded target still exposes the exact observation contract required by the diagnostic.

No unverified MVID, metadata-token, `CodeBase`, process-module or substring identity is introduced as a substitute.

## Dependency-hash boundary

The existing BMGHDIAG1 file-backed hash checks for ordinary BepInEx plugin dependencies may remain file-location based where their loaded plugin assemblies actually expose stable on-disk locations:

- LethalLevelLoader 1.7.12 SHA-256 `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

The successor must use a distinct installed-game-binary validator so the `Assembly-CSharp` fix cannot silently weaken these dependency checks.

## Gameplay and observation behavior retained unchanged

Other than the startup provenance fix and successor identity/markers, BMGHDIAG2 retains the BMGHDIAG1 behavior contract:

- exact LLL `GetValidExtendedDungeonFlows(ExtendedLevel, bool)` postfix only;
- exact server-selection caller gate;
- terminal simulation exclusion;
- Black Mesa exact `NumberlessPlanetName` guard;
- exactly one already-viable `Greenhouse / GreenhouseFlow` wrapper at final rarity `100`;
- singleton reduction only after all validations pass;
- exact accepted normalizer ordering;
- read-only `EntranceTeleport.TeleportPlayer()` postfix only;
- observer inert until targeted selection succeeds;
- IDs 0..3 traversal coverage and one-time topology snapshot;
- no field writes, manual teleport, retry, RPC replacement, registration mutation or availability mutation.

The two Harmony surfaces and one-gameplay-mutation/one-read-only-observation boundary remain unchanged.

## Required source/static tests before any build

The successor source gate must fail unless all of the following are covered:

### Installed path/hash policy

- exact managed path + existing exact `Assembly-CSharp.dll` + expected hash -> pass;
- missing/blank managed path -> fail closed;
- nonexistent managed directory -> fail closed;
- missing `Assembly-CSharp.dll` -> fail closed;
- file read failure -> fail closed;
- wrong hash -> fail closed;
- no recursive/alternate search path exists;
- game assembly provenance code does not depend on `Assembly.Location` or `Assembly.CodeBase`.

### Loaded runtime identity

- exact Assembly-CSharp name + exact manifest module + non-dynamic assembly + exact `EntranceTeleport` target contract -> pass;
- wrong assembly name -> fail;
- dynamic assembly -> fail;
- wrong module name -> fail;
- missing/wrong `TeleportPlayer()` contract -> fail;
- missing/wrong observation fields -> fail.

### Existing diagnostic policy

All BMGHDIAG1 selection/observation policy tests must be ported with only successor namespace/marker identity changes. The accepted normalizer ordering check, exact LLL dependency checks, no-prefix/no-transpiler/no-PatchAll rules and exactly-two-Harmony-surface rule remain mandatory.

## Build/publication boundary

C3F18 design does not create or enable a candidate build request and does not modify live controllers.

Before BMGHDIAG2 may be built for review, a later bounded implementation checkpoint must:

1. implement the successor in a new `Patches/S142AKBMGHDiag2/` project;
2. add pure/static tests and a successor-specific source gate;
3. compile successfully against repository-pinned dependencies;
4. re-confirm exact S1.42AK parent, LLL and normalizer provenance;
5. prove the source delta is limited to the diagnostic successor and its validation infrastructure;
6. keep `BuildSpecs/current.json` disabled and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.

Only after source/static review passes may a separate inactive review-build request be authorized. Static success still does not authorize gameplay.

## Preserved project state

- accepted/latest gameplay baseline: exact S1.42AK;
- `active_candidate = null`;
- `runtime_test_outstanding = false`;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`;
- Black Mesa x Greenhouse remains `NOT_YET_PROVEN`;
- accepted S1.42AB InteriorWeightNormalization unchanged;
- Black Mesa remains Dawn/native-owned with no duplicate registration;
- Greenhouse availability unchanged;
- B3 30x53 matrix unchanged;
- Shatteredrooms x Experimentation/Embrion untouched;
- Black-Mesa/Pikmin routing remains separate scope.

## Next bounded action

Implement only the separately versioned BMGHDIAG2 source/static successor described here, including the split installed-binary/runtime-target provenance gates and pure negative tests. Do not build a Gale profile or arm runtime in the same source-implementation checkpoint unless a later freshly read lifecycle explicitly authorizes that separate atomic step.
