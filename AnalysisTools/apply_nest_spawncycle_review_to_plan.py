#!/usr/bin/env python3
from pathlib import Path

path = Path('BuildSpecs/S1.42AI_PLAN.md')
text = path.read_text(encoding='utf-8')
old = "Next source-review segment: inspect complete exact NestFix and SpawnCycleFixes patch bodies and ordering, then close the identified LethalMin/CodeRebirth/Dusk direct-creation and return-value gaps. No new user capture or gameplay run is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT and the patch safety gate remains open."
new = """## Exact NestFix / SpawnCycleFixes review — 2026-09-11

`SourceEvidence/NativeSpawnOwners/20260911T150936Z-NestSpawnCycleExact/REVIEW.md` records the complete exact-body and Harmony-order review for PureFPSZac-NestFix 1.3.0 and ButteryStancakes-SpawnCycleFixes 1.2.2. Actions run `34614454120` re-fetched the already SHA-anchored package/DLL bytes, reproduced both prior complete-decompile source hashes with pinned ILSpy 11.0.0.9375, and retained full C#/IL in artifact `10269567481`; `VERIFICATION.json` anchors the hashes without copying full third-party decompiles into the repository.

NestFix has one default-priority prefix on `RoundManager.SpawnNestObjectForOutsideEnemy`: non-BaboonHawk types pass to V81, while Baboon Hawk nest creation is fully replaced but still performs network spawn, nest-list registration and `nestsSpawned` bookkeeping. Do not compete on this target with another unordered prefix or suppress nest infrastructure as a generic enemy-spawn shortcut; `EnemyAINestSpawnObject` downstream ownership remains to be reviewed.

SpawnCycleFixes has 15 patch methods. With the exact S1.42AI config, `Consistent Spawn Times = true` and `Limit Old Birds = true`: its default-priority `PredictAllOutsideEnemies` prefix replaces vanilla prediction, its `BeginEnemySpawning` prefix performs early daytime/outside/weed batches, vent prefix/postfix logic can reassign and fan out grouped enemies while reserving power, and its LungProp transpiler performs Old Bird spawn bookkeeping after `SpawnEnemyGameObject`. The existing project diagnostic's `Priority.First` prefixes on prediction/begin-spawning deterministically run before these default-priority SpawnCycleFixes prefixes, but pool reassertion still does not cover explicit/direct spawn owners. A blanket central `SpawnEnemyGameObject` denial is specifically unsafe for the LungProp path because SpawnCycleFixes can still increment counts/power after the denied call.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Next close the LethalMin/CodeRebirth/Dusk direct-creation, replacement and return-value gaps together with the exact native `AssignRandomEnemyToVent`/`specialEnemyRarity` body and `EnemyAINestSpawnObject` downstream lifecycle, then finish remaining enabled spawn-owner/BCMER forced-side coverage. No new user capture, gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
if text.count(old) != 1:
    raise SystemExit(f'expected exact old checkpoint once, found {text.count(old)}')
text = text.replace(old, new)
path.write_text(text, encoding='utf-8')
print('Updated canonical S1.42AI plan with exact NestFix/SpawnCycleFixes review')
