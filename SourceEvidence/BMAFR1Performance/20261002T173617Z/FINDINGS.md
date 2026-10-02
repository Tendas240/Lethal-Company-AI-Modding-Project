# BMAFR1 supplemental array-index flood: bounded attribution checkpoint

Date: 2026-10-02
Status: BOUNDED LOG/SOURCE TRIAGE COMPLETE; ARRAY EMITTER/ROOT CAUSE UNPROVEN
Analysis base: main 1abac31f43bc4a78cf408c86eaa839952c1194c8
Authority boundary: evidence-only review checkpoint; does not supersede CURRENT_STATE.json or Current/226. No gameplay, controller, profile or package changes. No patch or runtime request.

## Result

The logs prove a sustained Unity Log error stream, not an identified plugin emitter. Janitor remains a plausible source/interaction candidate, but the apparent lifetime correlation is not a causal isolation experiment. In particular, the end occurs during shared lobby/network shutdown, and SpringMan spawns and is destroyed almost concurrently.

A concrete static candidate is a mesh/animation compatibility interaction: exact CodeRebirth 1.6.9 Janitor calls SkinnedMeshRenderer.SetBlendShapeWeight(0, ...), while exact DawnLib.Dusk 0.9.25 can replace a renderer's sharedMesh without validating blendshape compatibility. However:
- Janitor.Update has no unconditional per-frame direct blendshape write.
- Janitor.LateUpdate calls KeepPlayerAttachedDuringZoom only in state 3; its reset branch changes state to 0 before writing the blendshape.
- The other inspected writes are chase/reset/death-related methods and RPC handling, not proof of 6,696 recurring invocations.
- The logs do not identify the recipient of the material-mismatch warning, selected replacement asset, live mesh blendShapeCount, animation binding, or stack for the array signature.
- Therefore a Janitor/mesh-replacement defect is a hypothesis with a concrete static mechanism, not a proven cause.

## Provenance

Both raw logs were downloaded from the exact analysis-base GitHub commit and independently hashed:
- RuntimeEvidence/S1.42AK-BMAFR1/20261002T154834Z/raw/LogOutput.log: 1657720 bytes; SHA-256 3113a1c9df2e1db231cf6aa0e7dc20699894a8646da3eaf7fd1ce0c3d89ac42b.
- RuntimeEvidence/S1.42AK-BMAFR1/20261002T164741Z/raw/LogOutput.log: 2453449 bytes; SHA-256 ca2d83a56115f66623c3dfb38d2cdd47085b3c0a368efc3ace29321a323b4d90.

analyze_logs.py is read-only and accepts a repository root; it asserts both hashes. LOG_DIFFERENTIAL.json is its reproduced output. Timestamp calculations use logged wall-clock times, not instrumented frame or CPU measurements.

Package source routing: Knowledge/CODEREBIRTH.md, Knowledge/BCMER.md, SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json and the associated discovery reports. BMAFR1 export.r2x confirms the same enabled package versions; both logs have identical 163-entry loaded plugin identity lists. This does not independently hash every DLL in the user's process.

Two existing package releases were fetched solely for static inspection and matched repository-recorded ZIP and DLL hashes:
- XuXiaolan-CodeRebirth 1.6.9 ZIP a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6.
- CodeRebirth.dll a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36.
- com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll 308ddf095d807b719c204c48bee3ce26795281c6b399baf3ac105e6b9d258163.
- TeamXiaolan-DawnLib 0.9.25 ZIP c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3.
- com.github.teamxiaolan.dawnlib.dusk.dll 3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03.

These exact DLLs were inspected with ilspycmd 9.1.0.7988. This differs from the historical discovery tool version 11.0.0.9375; no equality of decompiled source hashes is claimed. Missing dependency annotations remain; source-level reading is qualified accordingly. SOURCE_EXCERPTS.json preserves source line numbers and hashes of the full transient decompiler outputs, omitting IL annotation comments from selected excerpts.

BCMER source is reused from existing Actions artifact 10304724235 / run 34716488701; downloaded artifact ZIP SHA-256 independently matched 35ca8ec171fc40f8d9b0c9d2a9f1af3ad062f54c56c63a22e1424012c20cc116. Canonical provenance: SourceEvidence/ShyGuyIsolation/20260912T202218Z-BCMERExecutionExact/VERIFICATION.json. Existing source hash ea8f0415d25cf5a468e6ba276ead7b4586819e531eaa6ed7b5ab6bafca6d3fb4; DLL c344d3fdddd1f4ac32c80d3ec24eee54810c4cfd91a13594d88579fa23bbf148. No workflow/build was dispatched for this analysis.

## Differential and temporal evidence

| Observation | First run | Supplemental |
|---|---|---|
| Exact array signature | 0 | 6696 |
| Map seed | 60312340 | 18486762 |
| Final length multiplier | 4.87 | 7.13 |
| Chosen BCMER events | ShipCoreFailure, BigBonus, PlentyOutsideScrap | Hell, GarbageLid, SafeOutside, Arachnophobia, SmallerMap |
| TransferRenderer warning | got 3, need 1 | got 3, need 4 |
| Logged Janitor live spawn | none found | successful BCMER indoor spawn |
| Logged plugin identities | same 163 | same 163 |

The same moon/interior/build control rules out the claim that every such pair execution necessarily floods, but is not a matched seed/event/AI-load/asset-selection A/B test.

Supplemental:
- L14995: SpringMan success 16:44:37.5266354.
- L15083: Janitor success 16:44:37.5446573.
- L15097: material-count mismatch 16:44:37.7115669.
- L15111: first array error 16:44:37.7205806.
- L25173: Leaving current lobby 16:47:06.2663563.
- L25182: host shutdown/disconnect 16:47:06.3019222.
- L25185: last array error 16:47:06.3389967.
- L25275: Janitor death/cleanup 16:47:06.5065782.
- L25279: SpringMan death/cleanup 16:47:06.5075777.

The first error follows Janitor success by 175.9233 ms, SpringMan by 193.9452 ms, and the renderer warning by 9.0137 ms. The last error is 72.6404 ms AFTER the lobby-leave marker and 167.5815 ms BEFORE Janitor cleanup. Many other enemies are cleaned up in the same window. Do not describe this as a selective Janitor removal that stopped the flood.

6696 errors span 148.6184161 seconds. Inter-arrival rate (N-1)/duration = 45.04825294/s; median gap 21.6262 ms; p95 27.1545 ms; max 328.2457 ms; no duplicate error timestamps; five gaps exceed 100 ms. Full 10-second windows contain 404–509 errors (last partial window excluded). No repeated multi-second silent periods. No attached nonempty continuation/stack lines on any exact signature event.

The flood begins before the first player entrance traversal and continues across all eight traversal markers. Previous/next 1-second counts are recorded in LOG_DIFFERENTIAL.json and do not show on/off gating. Later BCMER spawn cycles roughly 30 seconds apart are superimposed on a continuous stream, rather than producing all errors as periodic spawn bursts. No direct frame-count equivalence or FPS cost can be inferred.

## Exact source findings and owner distinctions

1. **BCMER spawn owner, not proven error owner.** EnemySpawnCycle.EnemySpawnInfo.AttemptSpawnInside invokes Manager.Spawn.InsideEnemies(enemy, 1), then DoSpawnInsideEnemies(), then emits the successful-spawn line. Hell builds an indoor cycle with a 30-second interval, includes modded eligible enemy prefabs at weight 8 / cap 2, activates via RefreshEnemiesList, and also changes factory/scrap/environment parameters. This explains a credible spawn/event route and confounds, not the array emission. The observed 30-second cycles do not match a direct per-error spawn-call pattern.

2. **Proven owner of the nearby warning.** Dusk.MaterialsReplacement.CopyOrResizeMaterials emits exactly the TransferRenderer warning. Both SkinnedMeshReplacement.ReplaceSkinnedMeshRenderer and MeshReplacement.ReplaceMeshRenderer call it after assigning sharedMesh. Its message omits recipient identity; material/submesh counts are not blendshape counts. The material fallback checks source lengths, and the output array has at least one element. The warning is not itself evidence of a zero-length material access.

3. **Proven owner of a DIFFERENT exception.** Supplemental L16561 at 16:44:38.6566066 has a NullReferenceException with Transform.Find -> Dusk.SkinnedMeshReplacement.<Apply>d__4.MoveNext -> SetupCoroutine.InvokeMoveNext. It follows the first array error by about 0.936 seconds, after daytime-enemy cleanup. It demonstrates a separate replacement-path failure. The target object and cause of the null are not identified. Do not attach this stack to the 6696 array messages.

4. **Conditional Janitor mechanism.** Janitor's four direct SetBlendShapeWeight call sites target skinnedMeshRenderers[0], blendshape index 0, without a local blendShapeCount check: ClientRpc, KillEnemy, KeepPlayerAttachedDuringZoom reset branch, SwitchToChaseState. Source excerpts retain conditions/call context. Dusk's mesh replacement changes the existing renderer's sharedMesh and bones; it does not check or remap blendshapes in the inspected method. A resulting incompatible mesh or animation binding is plausible, but actual replacement selection and a zero-blendshape live mesh remain unproven. The dedicated Janitor replacement subclass itself changes audio fields; its existence does not prove that a Janitor replacement was selected.

5. **Replacement selection is variable.** Dusk.EntityReplacementRegistrationPatch.ReplaceEnemyEntity runs after original EnemyAI.Start, filters replacement candidates, uses moon/interior/weather context, initializes its RNG with map seed + 234780, and starts current.Apply(self) only for a selected non-default entry. Thus identical package versions and same moon/interior do not by themselves fix selected replacement assets. The two map seeds differ. This is a static selection mechanism, not reconstruction of the actual draw.

6. **Other performance factors remain distinct.** SpringMan has synchronous pathfinding fallback observations at 16:44:48.0603093 (612.6556 ms cached path age) and 16:46:49.2226441 (3207.657 ms). These are path ages, NOT measured blocking times. Hell/Arachnophobia and the larger final multiplier confound overall performance attribution. The user's subjective whole-run symptom cannot be quantitatively assigned solely to the error logging overhead.

The exact array literal is absent from the inspected Janitor, Dusk and BCMER decompiled source. This limited search is not an exhaustive whole-stack or native-engine emitter search.

## Classification

| Claim | Classification |
|---|---|
| 6696 stackless Unity Log messages, onset/offset/count/cadence | Proven from exact raw log |
| BCMER generated the Janitor/SpringMan successful-spawn messages and corresponding source route exists | Proven log/source ownership |
| Dusk owns the material warning and separate SkinnedMeshReplacement NRE | Proven; separate signatures |
| Janitor/SpringMan/replacement timing aligns with onset | Strong temporal correlation |
| Janitor death independently terminates the flood | Not supported; shared disconnect confound |
| Janitor index-0 writes interacting with a replaced mesh/animation cause all array errors | Plausible concrete hypothesis; not proven |
| Native Unity blendshape subsystem is the exact emitter | Not established by available stacks |
| BCMER, Janitor, Black Mesa, Foundry or BMAFR1 is the root cause | Undecided |
| Error flood alone accounts for reported frame-rate degradation | Undecided; no CPU/GPU/frame profiling |

## Bounded stopping point / next action

No patch is justified by this checkpoint. No new build or runtime test is authorized or requested. Do not label this monitor-only: user-facing degraded fluidity and the massive frequency delta remain material.

The bounded log/candidate-method triage is complete with owner unresolved. Do NOT claim all static attribution is exhausted: if pursued, the next useful bounded static step is exact asset-level resolution of the relevant replacement definitions, target hierarchy, original/replacement mesh blendshape counts and animation bindings for Janitor AND the contemporaneous SpringMan. Reuse repository-indexed package identities and existing assets/evidence first. A mesh incompatibility would still need linking to the observed instance/signature; do not overclaim causal performance cost.

The original BMAFR1 generation/topology/traversal pair PASS remains intact. BMAFR1 stays DIAGNOSTIC ONLY / NEVER ACCEPT / inactive. S1.42AK remains accepted. BMDSFIX1 remains active/not accepted, with passive outstanding unwaived DeepSewersFlow gate and no dedicated reroll. Build controller remains disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS.

This evidence checkpoint is prepared for repository review/integration; canonical lifecycle routing has not been changed. The originating GPT-6 chat has consumed its two project segments. A follow-on chat must freshly execute the repository bootstrap, review this evidence checkpoint, and reconcile the appropriate next_action before further project work. No third execution segment belongs to the originating chat.
