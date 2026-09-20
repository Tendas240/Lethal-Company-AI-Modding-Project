# C3F7 — bounded GlobalProp asset-capture implementation

**Status:** HELPER IMPLEMENTED / EXACT-HEAD CI VALIDATED / NO GAMEPLAY OR MATRIX CHANGE  
**Date:** 2026-09-20  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Implementation parent:** `cd93e11c38e1563508a36fb8a982d3e8af984580`  
**Verified main:** `56355ff518ae4301a38d370be9561251f6f963c1`

## Scope and implementation

`AnalysisTools/inspect_universal_interior_c3f7.py` captures only the 23
selection-supported Black Mesa-row flows fixed by C3F6 and Phase A: six direct
LLL package groups (22 flows) and native Black Mesa (one flow). It checks the
accepted export's enabled exact versions and the authoritative Phase-A identities.

The helper reuses the C3F2 Thunderstore CDN, ZIP hashing/path checks and pinned
UnityPy 1.25.3 static-reader approach. It does not execute Unity, game binaries or
managed mod code. `PACKAGE_LOCK.json` binds all seven exact archives and all 38
UnityFS members, plus the complete non-directory member inventories. Black Mesa
also must match the already reviewed C3F2 archive size and SHA-256.

The other six archive bindings are new exact-version acquisitions. They are not
asserted byte-identical to historical installed payloads merely because the
accepted profile records the same version. CI independently re-downloads and
compares every archive/member byte binding. The optional `--record-provenance`
mode only emits an unreviewed candidate lock; it never performs a successful
asset capture or overwrites the reviewed lock.

Normal capture binds the helper, C3F2 helper, lock and authority-file SHA-256s;
CI additionally binds its exact checked-out PR commit and workflow run.

## Fail-closed extraction contract

- Exactly one case-sensitive DungeonFlow name, exact class/namespace and a
  supported serialized assembly layout must resolve within the pinned package.
  The actual script descriptor and raw object hash are preserved. DunGen.dll and
  the observed Assembly-CSharp exporter layout are distinguished in evidence;
  this is not an assertion of runtime assembly equivalence.
- The entire serialized flow and GlobalProps table are retained, including all
  ID-1231 Count/range fields. Missing/malformed tables are unresolved, never absent.
  Duplicate target ID 1231 is fatal. Duplicate unrelated IDs are recorded without
  interpreting their generation effects.
- Flow/archetype/TileSet pointers and tile hierarchy membership establish which
  GlobalProp components belong to the selected flow. A separate package-wide
  ID-1231 component inventory is not used as a substitute for that membership.
- GameObject/component/Transform context and explicit
  `SpawnSyncedObject.spawnPrefab` template chains are captured. The latter prove
  serialized references only, not that a runtime spawner executes. Repeated
  prefab references preserve multiplicity; siblings and unrelated package
  entrances cannot be counted as template descendants.
- Exact EntranceTeleport class/namespace descriptors, serialized side and
  pre-numbering entranceId are retained. A standard template result requires one
  inside-side ID-1 entrance per captured template path. All reachable ID-1231
  templates must satisfy this narrow static predicate for a positive flow result.
- Ambiguous identities, malformed or unresolved non-null pointers on the target
  surface, parent/child contradictions, relevant parser failures, unsupported
  graph references and provenance drift produce a failure artifact and nonzero
  exit. No partial capture can become an absence or positive result.
- Unity nonfinite curve values are retained as explicit tagged JSON values;
  invalid JSON or silent field loss is not permitted.

Result classes:

| Class | Narrow meaning |
|---|---|
| `PROP_AND_TEMPLATE_PROVEN` | Unique ID 1231 plus linked serialized inside-ID-1 template surface captured |
| `PROP_PRESENT_TEMPLATE_UNRESOLVED` | ID 1231 captured, but a standard linked template is not established |
| `PROP_1231_ABSENT` | Complete valid serialized table contains no ID 1231 |
| `CAPTURE_UNRESOLVED` | Flow/table/provenance capture cannot be established |

A fully readable surface can legitimately yield `PROP_PRESENT_TEMPLATE_UNRESOLVED`
without a parser error. CI success means that the capture contract completed,
not that every flow received a positive template result. Fatal ambiguities always
fail the capture job; artifact upload does not mask its exit status.

## Validation and reproduction

Exact-head implementation validation is complete for repair head
`9731159c2d7ffebbcf6db77b28e1233cf2af2b04`:

- `Capture C3F7 GlobalProp asset evidence` run `35537782662` / #2:
  **SUCCESS**. The focused validation job and all seven exact-package capture
  matrix jobs completed successfully.
- `Knowledge Architecture` run `35537782670` / #591: **SUCCESS**.
- The other exact-head PR workflows also completed successfully: Black Mesa
  topology, Black Mesa DLL metadata, V81 generation, V81 spawning and V81
  entrance-pairing helper validation.

The first implementation head
`c4e6a10de0f39b3136cc48030d90861bf0a09727` intentionally exposed two
fail-closed integration defects during CI rather than masking them:

- Generic Interiors stopped on a Backrooms template component with a serialized
  null `m_Script`. The repair keeps non-null pointer resolution strict and
  still fails when such an opaque component carries a target discriminator
  (`PropGroupID`, `entranceId`, `isEntranceToBuilding` or
  `spawnPrefab`), but preserves a true null-script component with none of
  those fields as opaque static context. Regression tests cover both cases.
- The repository cold-history validator interpreted the prior diagnostic wording,
  which began with a reserved legacy cold-root token, as a path reference. The
  diagnostic now says `ZIP/member provenance drift`; no provenance rule was relaxed.

Workflow: `.github/workflows/universal-interior-c3f7-asset-evidence.yml`.
It checks out the exact PR head (not the synthetic merge commit), runs the focused
proof-boundary tests, then independently captures the seven packages in a bounded
matrix. Only derived JSON reports are uploaded; package/bundle/game bytes are not.

```sh
python -m pip install UnityPy==1.25.3 PyYAML==6.0.2
python -m unittest discover -s AnalysisTools -p 'test_universal_interior_c3f7.py' -v
python AnalysisTools/inspect_universal_interior_c3f7.py --package Tolian-Scoopy_Castle --out c3f7-output
```

The tests cover unique identity, wrong namespaces/assemblies, full-table
preservation, absent versus unreadable tables, ambiguous target IDs, unrelated
duplicate IDs, parser faults, byte/authority drift, external-pointer ambiguity,
null scripts, dangling pointers, hierarchy conflicts/cycles, wrong entrance side
or initial ID, duplicate entrances, unrelated templates, explicit prefab chains
and strict JSON preservation of nonfinite Unity fields.

## Proof boundary and next gate

This checkpoint implements and validates capture infrastructure. It performs no
gameplay compatibility analysis. GlobalProp presence or a positive serialized
template result alone does not establish Black Mesa count-3 capacity, actual
generation, traversal, accessible geometry, routing or NavMesh safety.

The B3 matrix remains 662 / 14 / 0 / 0 / 914 across 1,590 cells. S1.42AK remains
accepted/latest; no active gameplay candidate or runtime test is armed.
BuildSpecs/current.json remains disabled at
`IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`; ACTIVE_BUILD remains S1.42AK.
S1.42AB normalization, native Black Mesa registration and Shatteredrooms
Experimentation/Embrion exclusions remain unchanged.

Next bounded segment, only after explicit continuation: ingest and review the
exact-head C3F7 derived captures, resolve any static asset/template evidence gaps,
and state the remaining count-3 proof obligations. Do not promote matrix cells
or start a build/runtime test merely from capture success.
