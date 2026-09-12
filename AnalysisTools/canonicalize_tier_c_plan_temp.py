#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE = "94be00f2ca31cb2caa4d0125e2bebb7573d22a50"
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)

review = Path("SourceEvidence/NativeSpawnOwners/20260912T181805Z-TierCExact/REVIEW.md")
verification = Path("SourceEvidence/NativeSpawnOwners/20260912T181805Z-TierCExact/VERIFICATION.json")
if not review.is_file() or not verification.is_file():
    raise SystemExit("Tier-C canonical evidence files are missing")

path = Path("BuildSpecs/S1.42AI_PLAN.md")
text = path.read_text(encoding="utf-8")
old = """Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **31** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
new = """## Exact Tier-C remaining-candidate review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T181805Z-TierCExact/REVIEW.md` records the next bounded six-package exact escalation from the remaining discovery-positive inventory. Successful Actions run `34710724733` re-fetched exact package bytes, required the prior ZIP/DLL/complete-source SHA gates to match, and preserved complete C#/IL in artifact `10303047183` (`sha256:369f15e556017cde234b312c00728ab434c0e286271ed7813d767f3ddeab464e`).

The tranche resolves Poltergeist as downstream `EnemyAI.Start` interactor infrastructure; SellBodiesFixed as enemy-death body/scrap replacement infrastructure; JPOGRaptor as a custom EnemyAI implementation whose only direct creation primitive here is a scrap drop; ScienceBird Tweaks as downstream enemy patches plus networked gameplay/support infrastructure; GeneralImprovements as an EnemyAI power observer plus ship/UI infrastructure; and LethalThingsReloaded as custom EnemyAI implementations plus item/projectile/support creation. None of the six exact assemblies contains `EnemyType`, `SpawnEnemyOnServer`, `SpawnEnemyGameObject`, or a direct enemy-instance creation primitive. That negative claim is deliberately assembly-local: JPOGRaptor and LethalThings enemy definitions may still enter native/framework registration and pool-instantiation paths outside these DLLs' direct creation code.

This reduces the still-unreviewed discovery-positive inventory from 31 to **25**. It further confirms that broad `EnemyAI.Start` or shared `NetworkObject.Spawn` suppression is unsafe because this tranche uses those surfaces for downstream enemy bookkeeping, interactors, bodies, scrap, ship infrastructure, projectiles and other required non-enemy network objects.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **25** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exact 31-candidate checkpoint once, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("Updated exact Tier-C planning checkpoint: 31 -> 25")
