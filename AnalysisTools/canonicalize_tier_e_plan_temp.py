#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE = "fce6d19de0a8810fe457b0436a44f948c51701cf"
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)

review = Path("SourceEvidence/NativeSpawnOwners/20260912T190358Z-TierEExact/REVIEW.md")
verification = Path("SourceEvidence/NativeSpawnOwners/20260912T190358Z-TierEExact/VERIFICATION.json")
if not review.is_file() or not verification.is_file():
    raise SystemExit("Tier-E canonical evidence files are missing")

path = Path("BuildSpecs/S1.42AI_PLAN.md")
text = path.read_text(encoding="utf-8")
old = """Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **19** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib and Interactive Terminal API cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
new = """## Exact Tier-E remaining-candidate review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T190358Z-TierEExact/REVIEW.md` records the next bounded six-package / eight-DLL exact escalation from the remaining discovery-positive inventory. Successful Actions run `34713018420` re-fetched exact package bytes, required prior ZIP/DLL/discovery-IL SHA gates to match, and preserved complete C#/IL in artifact `10304290416` (`sha256:a4c61ef958aba55a2573c296f0ab16904693d1f4e96b156ba6d48802fae0348a`).

The tranche resolves LethalPerformance as performance caching/transpiler infrastructure that actively touches shared enemy lifecycle/bookkeeping surfaces including `EnemyVent.Start` and `RoundManager.SpawnedEnemies`; LethalSponge as cleanup/audio-dedup infrastructure over existing EnemyVent/EnemyType assets; BarberFixes as a conditional server-side ClaySurgeon `EnemyType` spawn-parameter mutator before native batch spawning; RandomEnemiesSize as downstream `EnemyAI.Start`/`MaskedPlayerEnemy.Start` scaling plus RPC synchronization; FairAI as downstream enemy combat/hazard compatibility whose sole creation site is an explosion effect; and MaskFixes as downstream Masked start/state/visual repair that can add an already-existing instance to `RoundManager.SpawnedEnemies`. None of the eight reviewed assemblies contains `SpawnEnemyOnServer`, `SpawnEnemyGameObject`, `enemyPrefab`, or a direct EnemyAI-instance creation primitive.

This reduces the still-unreviewed discovery-positive inventory from 19 to **13**. It further confirms that broad `EnemyAI.Start`, `MaskedPlayerEnemy.Start`, `EnemyVent.Start`, `RoundManager.SpawnedEnemies` manipulation or blanket `AdvanceHourAndSpawnNewBatchOfEnemies` denial are unsafe substitutes for exact owner interception.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **13** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib and Interactive Terminal API cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exact 19-candidate checkpoint once, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("Updated exact Tier-E planning checkpoint: 19 -> 13")
