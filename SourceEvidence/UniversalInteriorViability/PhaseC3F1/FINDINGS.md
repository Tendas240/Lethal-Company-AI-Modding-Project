# C3F1 — Black Mesa 3.4.4 exact-package provenance and topology acquisition boundary

**Status:** EXACT ACCEPTED PACKAGE IDENTITY PROVEN / EXACT 3.4.4 PACKAGE+SCENE BYTES NOT REPOSITORY-HELD / HISTORICAL ENTRANCE RUNTIME IS OFFENSE / BLACK MESA TOPOLOGY STILL OPEN  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Parent PR checkpoint:** `cbf2b456931d43b797b53039f922809e7fb8a4fd`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3F1 attempts to establish the exact accepted Black Mesa 3.4.4 package/scene evidence surface before any entrance-ID or topology inference.

The required standard is deliberately strict:

- use the accepted S1.42AK package identity, not the obsolete public Black Mesa 0.9.0/direct-LLL source;
- prefer exact package/archive/scene bytes;
- do not infer Black Mesa moon topology from runtime logs unless the observed moon is actually Black Mesa;
- do not change the B3 matrix from source/provenance evidence alone.

## Exact accepted package identity

The accepted S1.42AK profile establishes one unambiguous enabled Thunderstore package identity:

- package: `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior`;
- version: **3.4.4**;
- enabled: **true**;
- source: Thunderstore.

This is independently present in:

1. `ProfileSources/S1.42AK/export.r2x` — Git blob `669cf2bf096544de84be9475de8f3f9eb594ce14`;
2. `SourceEvidence/NativeSpawnOwners/20260911T144505Z/PROFILE_PACKAGE_INVENTORY.json` — Git blob `fd8ee5a4147a5284ce6edf00e083353c8da2ca92`.

The accepted Black Mesa config is:

`ProfileSources/S1.42AK/BepInEx/config/Black Mesa Team.Black Mesa Half Life Moon Interior.cfg`

- Git blob: `1d2fcfc590493d4f9d8ab656c156b596ea7102e6`;
- FILE_INDEX SHA-256: `ce558f510956c04d25b41c59b11f88e38040cd57e5129db1f86ec91a29da9f44`;
- size: 11,125 bytes.

Its generated header says plugin v3.4.1, while the accepted profile package identity is 3.4.4. This mismatch was already preserved by C3C and is not interpreted as package downgrade evidence.

Relevant current config state remains:

- `BlackMesaDungeon Options / Enabled = true`;
- `Black Mesa | Allow Editing Config = true`;
- `Black Mesa | Preset Moon Weights = lethal_company:vanilla=+100,lethal_company:custom=+100`;
- `BlackMesaMoon Options / Enabled = true`;
- `BlackMesaScene | Allow Editing Config = false`.

## Exact package bytes are not preserved by the current repository evidence

The native-owner snapshot proves the package namespace/version/enabled state, but its manifest contains no Black Mesa 3.4.4 ZIP or DLL hash equivalent to the exact CodeRebirth package binding used for Oxyde C3E3A-C3E3H.

The accepted profile archive was therefore inspected as the next repository-native byte source.

### Accepted S1.42AK .r2z archive

`Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`

- Git blob: `b820ad507d39f4430cf7c3aa0fca94efd9d4d250`;
- exact uncompressed repository blob size: 559,988 bytes;
- accepted external SHA-256 from canonical lifecycle: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

Its ZIP central directory was parsed from the GitHub base64 blob in this checkpoint:

- 336 archive entries;
- Black-Mesa-named package payload match: only the 11,125-byte config file;
- no Black Mesa DLL or Black Mesa asset/scene bundle entry is present.

The archive therefore cannot supply the missing exact Black Mesa 3.4.4 implementation/scene bytes.

### S1.42AK build workflow artifact

Canonical build run: `35366580975`.

Its still-valid Actions artifact is:

- artifact ID: `10557020000`;
- name: `S1.42AK`;
- artifact ZIP size: 512,197 bytes;
- artifact digest: `sha256:1ff829e245bddf6699d69fb2c97d0d3c1060ab8c4a1e9d39661ad14a1db8199c`.

Build job `105670397815` explicitly records the upload path as only:

`Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`

Therefore the workflow artifact is only a wrapper around the same profile archive and does not retain the Black Mesa package staging bytes.

## Public source boundary remains unchanged

C3C already established that the public `PlasteredCrab/BlackMesaLethalCompany` source is historical:

- public source still declares 0.9.0;
- it predates the v81 3.4.x DawnLib migration;
- it directly uses the old LethalLevelLoader path.

It remains invalid as exact 3.4.4 implementation or scene-topology evidence.

C3C's author-level description of the current package mentions a custom exterior, a main entrance, fire exits and a secret fire-exit shortcut. Those descriptions are useful intent/context only. They do not establish exact `EntranceTeleport` counts, IDs, `isEntranceToBuilding` flags, scene objects or pairing.

## Historical runtime entrance evidence does not observe Black Mesa moon

Repository-native S1.42AA/S1.42AC logs contain substantial `EntranceTeleportA(Clone)` / `EntranceTeleportB(Clone)` routing evidence. C3F1 specifically checked whether that could substitute for unavailable Black Mesa scene bytes.

It cannot.

### S1.42AA

The relevant exact chunk is:

`RuntimeEvidence/S1.42AA/20260904T153744Z/analysis/raw__LogOutput/chat_chunks/chunk_0006_L00013096-L00015731.log`

Git blob: `713939fca036fbf18c16dc1c9c16fd26c1406db8`.

Before the entrance-routing block it records:

- `moonType(Offense)=0.250`;
- the current entrance mapping includes `EntranceTeleportA` and a manually added `EntranceTeleportB` destination.

Later the same Offense context produces the repeated A/B reachability failures. The presence of `LethalLevelLoader/BlackMesa/Xen Crystal` in nearby item setup is package-content registration, not evidence that the active moon is Black Mesa.

### S1.42AC

The relevant exact chunk is:

`RuntimeEvidence/S1.42AC/20260904T181854Z/analysis/raw__LogOutput/chat_chunks/chunk_0008_L00018723-L00020460.log`

Git blob: `c8b7bd1e9714280cb1e180f51fa664ccbc0b4fbf`.

This run contains many A/B entrance route checks around raw lines 18,898-19,824. Raw line 19,801 explicitly records:

`current planet: 21 Offense`

Thus the AC entrance evidence is also an Offense observation, not Black Mesa moon topology.

The existing Black Mesa/Pikmin routing topic remains a separate deferred scope. These logs are not repurposed here as proof of Black Mesa entrance geometry or pairing.

## C3F1 decision

The evidence boundary is now exact:

### Proven

- accepted Black Mesa package namespace/version/enabled state = **3.4.4**;
- accepted Black Mesa owner config and native Dawn-owned selection rule;
- the current repository/profile/build artifact does **not** preserve the Black Mesa 3.4.4 package archive or its scene/asset-bundle bytes;
- the obsolete public 0.9.0 source is not a valid substitute;
- the historical A/B runtime entrance observations examined here are Offense, not Black Mesa.

### Not yet proven

- exact Black Mesa 3.4.4 ZIP SHA-256;
- exact current Black Mesa implementation DLL SHA-256;
- exact current moon scene/asset-bundle identity and hashes;
- main-entrance / fire-exit count;
- `EntranceTeleport.entranceId` values;
- `isEntranceToBuilding` values;
- outside/inside teleport pairing;
- whether any special shortcut entrance has ordinary or owner-specific pairing semantics;
- Black Mesa-moon compatibility with arbitrary registered interiors.

Accordingly, **Black Mesa 3.4.4 moon-side topology remains `NOT_YET_PROVEN`**. No matrix reclassification follows from C3F1.

## Required acquisition path

The next evidence step must obtain the exact 3.4.4 package bytes in a reproducible, fail-closed way and publish only compact derived evidence into the repository.

A suitable bounded capture must:

1. require exact package `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior` version `3.4.4`;
2. download that exact archive from the package distribution source;
3. record archive size and SHA-256;
4. inventory all members and hash the implementation DLL(s) and Black-Mesa scene/asset bundles;
5. identify the exact Dawn/Dusk moon definition and scene bundle;
6. statically parse the scene/asset surface for `EntranceTeleport` components and pairing fields where type information permits;
7. fail closed on unexpected package identity/layout or parser ambiguity;
8. publish no gameplay profile and start no gameplay runtime test.

This should use repository-native CI/helper infrastructure so that the evidence becomes reproducible rather than depending on a transient local download.

## Preserved project state

Nothing in gameplay/configuration changes:

- authoritative B3 matrix remains unchanged;
- the 46 External selection-supported pairings remain selection-layer evidence only;
- Black Mesa remains single-registered through its current owner path;
- Shatteredrooms Experimentation/Embrion exclusions remain intact;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest;
- no candidate or runtime test is armed;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Next bounded segment

Next **C3F2**: implement and validate a fail-closed repository-native Black Mesa 3.4.4 package/topology capture helper and GitHub Actions workflow. The helper should acquire the exact package, hash/inventory the relevant bytes and produce a compact static topology report suitable for ingestion into PR #138.

Do not modify the B3 matrix, do not duplicate-register Black Mesa, and do not request a gameplay run.
