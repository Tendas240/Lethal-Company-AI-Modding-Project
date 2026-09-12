#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE = "a7a6958d9e82ee657aea65a72011eb7e0d44b86b"
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)

review = Path("SourceEvidence/NativeSpawnOwners/20260912T175808Z-TierBExact/REVIEW.md")
verification = Path("SourceEvidence/NativeSpawnOwners/20260912T175808Z-TierBExact/VERIFICATION.json")
if not review.is_file() or not verification.is_file():
    raise SystemExit("Tier-B canonical evidence files are missing")

path = Path("BuildSpecs/S1.42AI_PLAN.md")
text = path.read_text(encoding="utf-8")
old = """Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **37** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""
new = """## Exact Tier-B remaining-candidate review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T175808Z-TierBExact/REVIEW.md` records the next bounded six-package exact escalation from the remaining discovery-positive inventory. Successful Actions run `34709775849` re-fetched exact package bytes, required the prior ZIP/DLL/complete-source SHA gates to match, and preserved complete C#/IL in artifact `10303095900` (`sha256:a5a33c57fec7c9f81d6b97fc335d5c4d6f6c697c175aa778d5d2200ed9014b7c`).

The tranche resolves `Mirage_v81` as a conditional Masked spawn-pool mutator whose spawn-control branch is disabled by the exact S1.42AI config; `DungeonGenerationPlus` as a discovery context false positive for enemy ownership; `Remnants` as networked remnant/body/scrap infrastructure rather than EnemyAI creation; `Bozoros` as a real but provider-gated direct Puffer/Butler prefab network owner behind its Emergency Dice compatibility path; `EnemySkinRegistry` as a downstream `EnemyAI.Start`/nest/lifecycle observer rather than creator; and `EnemySoundFixes` as an audio/lifecycle patch set rather than creator. The exact package inventory does not identify a `Theronguard`/`EmergencyDice` provider package, but that package-name observation is not promoted into a universal proof that the plugin GUID can never be supplied under another identity.

This reduces the still-unreviewed discovery-positive inventory from 37 to **31**. It also strengthens the prohibition on broad `EnemyAI.Start` or shared `NetworkObject.Spawn` suppression: those surfaces are used by downstream/non-enemy infrastructure even among this tranche.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) triage and exact-review the other **31** discovery-positive packages according to signature strength and relevance, plus trace SnowyLib cross-assembly consumers; (2) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (3) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (4) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT."""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exact 37-candidate checkpoint once, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("Updated exact Tier-B planning checkpoint: 37 -> 31")
