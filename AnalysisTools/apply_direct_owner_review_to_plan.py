#!/usr/bin/env python3
from pathlib import Path

path = Path('BuildSpecs/S1.42AI_PLAN.md')
text = path.read_text(encoding='utf-8')
old = "Patch safety remains **PARTIAL / NOT_BUILD_READY**. Next close the LethalMin/CodeRebirth/Dusk direct-creation, replacement and return-value gaps together with the exact native `AssignRandomEnemyToVent`/`specialEnemyRarity` body and `EnemyAINestSpawnObject` downstream lifecycle, then finish remaining enabled spawn-owner/BCMER forced-side coverage. No new user capture, gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."
new = """## Exact LethalMin / CodeRebirth / Dusk direct-owner review — 2026-09-11

`SourceEvidence/NativeSpawnOwners/20260911T152805Z-DirectOwnersNativeGaps/REVIEW.md` records the complete exact-package review of the previously identified LethalMin 1.1.108, CodeRebirth 1.6.9 and DawnLib/Dusk 0.9.25 creation/replacement/return-value gaps. Read-only Actions run `34616289395` re-fetched the already SHA-anchored package/DLL bytes and reproduced all five prior complete-decompile source hashes with pinned ILSpy 11.0.0.9375; full C#/IL remains in artifact `10270990899` while `VERIFICATION.json` retains hashes and provenance.

LethalMin directly creates Pikmin/Puffmin EnemyAI in stateful conversion, Onion, wild-map, Sprout/elevator and revival transactions. Callee-only denial can remove Onion/persistence data, despawn the source entity without replacement or violate a caller's non-null return contract. Therefore the legacy blanket Pikmin-family exemption is forbidden, but a blanket shared creation denial is also not patch-safe: prevention must occur at reviewed owner transactions before destructive mutations.

CodeRebirth has fourteen explicit `RoundManager.SpawnEnemyGameObject` calls across nine owner methods. Several consumers pre-increment counters, immediately dereference the returned NetworkObject, copy state and/or later perform unrelated lifecycle transitions. This rules out a blanket central `SpawnEnemyGameObject` denial. The CodeRebirth Dusk companion itself defines typed replacement behavior rather than a second EnemyAI creation path. DawnLib/Dusk applies replacements to already-created EnemyAI/nests and can network-spawn replacement addon infrastructure, so shared `NetworkObject.Spawn` suppression is likewise forbidden.

DawnLib additionally detours `AssignRandomEnemyToVent`, temporarily owns `spawningDisabled` state during rush assignment and alters return semantics; DawnLib core and Dusk both hook `EnemyAINestSpawnObject.Awake`, while Dusk also detours `EnemyAI.UseNestSpawnObject`. The exact project V81 NuGet reference still supplies only stubs for the missing native bodies. Patch safety therefore remains **PARTIAL / NOT_BUILD_READY** pending a narrow supplemental installed-V81 capture of `RoundManager.AssignRandomEnemyToVent(EnemyVent,float)`, the declared `EnemyAINestSpawnObject` lifecycle including `Awake`, and `EnemyAI.UseNestSpawnObject(EnemyAINestSpawnObject)` with the smallest required caller context. This supplements rather than repeats the completed 27-method RoundManager capture. After that, finish the remaining enabled spawn-owner inventory and BCMER forced/side-event coverage. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
if text.count(old) != 1:
    raise SystemExit(f'expected exact prior checkpoint once, found {text.count(old)}')
path.write_text(text.replace(old, new), encoding='utf-8')
print('Updated canonical S1.42AI plan with exact direct-owner review and native source blocker')
