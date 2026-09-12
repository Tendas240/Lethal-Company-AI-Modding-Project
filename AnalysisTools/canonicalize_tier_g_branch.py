#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plan = root / "BuildSpecs/S1.42AI_PLAN.md"
text = plan.read_text(encoding="utf-8")
needle = """Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) exact-review the other **7** discovery-positive packages, plus trace SnowyLib and Interactive Terminal API cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT.
"""
replacement = """## Exact Tier-G final discovery-positive review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T194125Z-TierGExact/REVIEW.md` records the final bounded seven-package / eight-DLL exact escalation of the remaining discovery-positive inventory. Successful Actions run `34714900794` re-fetched exact package bytes, required prior ZIP/DLL/discovery-IL and complete-source SHA gates for all seven positive DLLs, additionally reviewed CullFactory's second managed DLL, and preserved complete C#/IL in artifact `10304018023` (`sha256:179f35e60d4020ad6033320bab93c8e6d6f440e248e19c06984ca49ff8f49d65`).

The tranche resolves ImmersiveScrap as downstream existing-enemy teleport/hit plus explosion-effect handling; TooManyEmotes as downstream Masked emote/RPC/visual/UI infrastructure; ModelReplacementAPI as downstream player/Masked model replacement plus EnemyAI hit observation; LobbyControl as lobby/network control plus dead-enemy AI path guards; darmuhsTerminalStuff as bioscan/terminal UI over `RoundManager.SpawnedEnemies`; Beanie_Lib as downstream enemy interaction plus one generic uncalled `LaunchObject(GameObject)` instantiate helper with no enemy-specific or network-spawn evidence; and CullFactory (including `CullFactoryBurstPlugin.dll`) as downstream enemy/item culling plus Burst/geometry infrastructure. None of the eight reviewed assemblies contains `EnemyType`, `enemyPrefab`, `SpawnEnemyOnServer`, `SpawnEnemyGameObject` or a confirmed direct EnemyAI-instance creation route.

This reduces the still-unreviewed discovery-positive inventory from 7 to **0** and completes the exact review of the canonical 53-package discovery-positive inventory. This completion is inventory-bounded only: it does not close public/generic cross-assembly consumer gates already identified elsewhere.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) trace SnowyLib and `InteractiveTerminalAPI.Tools.SpawnMob` cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT.
"""
if text.count(needle) != 1:
    raise SystemExit(f"Expected exactly one Tier-F remaining-work paragraph, found {text.count(needle)}")
plan.write_text(text.replace(needle, replacement), encoding="utf-8")
(root / ".github/workflows/tier-g-canonicalize-branch.yml").unlink()
Path(__file__).unlink()
