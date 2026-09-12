#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE = "ae1a4693d23e41fce6674380f6ff83631b0a1eb3"
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)

review = Path("SourceEvidence/NativeSpawnOwners/20260912T183808Z-TierDExact/REVIEW.md")
verification = Path("SourceEvidence/NativeSpawnOwners/20260912T183808Z-TierDExact/VERIFICATION.json")
if not review.is_file() or not verification.is_file():
    raise SystemExit("Tier-D canonical evidence files are missing")

path = Path("BuildSpecs/S1.42AI_PLAN.md")
text = path.read_text(encoding="utf-8")
old = """Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **25** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
new = """## Exact Tier-D remaining-candidate review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T183808Z-TierDExact/REVIEW.md` records the next bounded six-package / seven-DLL exact escalation from the remaining discovery-positive inventory. Successful Actions run `34711742173` re-fetched exact package bytes, required the prior ZIP/DLL/complete-source SHA gates to match, and preserved complete C#/IL in artifact `10303775401` (`sha256:e2255ba78b8605fdc96df4b480dbdae0a79bf015ccea1cfe52f9336a8c94134c`).

The tranche resolves ButteryFixes as downstream enemy asset/lifecycle fixes plus pool-state bookkeeping rather than a direct creator; LethalLib as a real EnemyType registry and level-pool owner whose exact DLL does not directly instantiate enemy instances; ShipWindows as downstream enemy visual/collision fixes plus ship network infrastructure; SellMyScrap as networked Scrap Eater/handler plus downstream enemy-hit infrastructure; and MisideItems as item/furniture/UI infrastructure with downstream enemy-hit logic. `InteractiveTerminalAPI.Tools.SpawnMob(string, Vector3, int)` is the one direct explicit enemy-spawn API in this tranche: it searches the current indoor enemy pool and calls `RoundManager.SpawnEnemyOnServer`, but the complete exact DLL contains no internal caller. Because that method is public, cross-assembly consumers are now an explicit open coverage gate rather than being assumed absent.

This reduces the still-unreviewed discovery-positive inventory from 25 to **19**. It further confirms that broad `EnemyAI.Start`, shared `NetworkObject.Spawn`, wholesale LethalLib registration suppression or blanket central spawn denial are unsafe substitutes for exact owner interception.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **19** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib and Interactive Terminal API cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exact 25-candidate checkpoint once, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("Updated exact Tier-D planning checkpoint: 25 -> 19")
