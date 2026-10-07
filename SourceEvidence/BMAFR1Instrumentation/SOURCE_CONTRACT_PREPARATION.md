# S1.42AK-BMAFR1I1 exact dependency contract preparation

Date: 2026-10-03
Status: PREPARATION COMPLETE / IMPLEMENTATION PENDING / NOT A SOURCE-STATIC PASS
Classification: DIAGNOSTIC ONLY / NEVER ACCEPT
Authorization: Current/230_S1.42AK_BMAFR1_INSTRUMENTATION_SOURCE_STATIC_AUTHORIZATION_DECISION.md
Design: Current/229_S1.42AK_BMAFR1_NARROW_INSTRUMENTATION_DESIGN.md, as refined by Current/230
Analysis base: 7c1df95d3698b2b7e98b820c90370e89ace9970e

## Verified starting point and segment boundary

The mandatory policy, CURRENT_STATE and knowledge-map bootstrap was read from main in that order. Main remains the authorization merge above. Knowledge Architecture push run 37072180898 (#978) completed successfully for that exact head; its permanent validate-knowledge-architecture job 111053930778 passed. No open PRs were found at bootstrap.

This is the first execution segment in the current chat: focused contract preparation before implementation. The two-segment chat limit remains binding. A continuation may implement a bounded source/static unit, but must not bundle unrelated CI repair, merge, lifecycle reconciliation and handover merely to fit that limit.

These preparation files do not complete the requested source/static checkpoint, change canonical next_action, authorize any build, or qualify any runtime result. They are retained on the implementation branch for the following source work; main and its controllers remain unchanged.

## Reproducible exact-byte inspection

AnalysisTools/inspect_s142ak_bmafr1i1_contracts.py reads existing PE/CLI metadata and IL using dnfile 0.17.0 and dncil 1.0.2. It never loads/executes a DLL, compiles code, downloads packages, or writes input files. It checks both exact DLL hashes before inspection and refuses missing or ambiguous declared targets.

The two packages were downloaded for static inspection only and independently rehashed against the existing NativeSpawnOwners manifest and BMAFR1 performance/asset evidence:

| Input | SHA-256 |
|---|---|
| XuXiaolan-CodeRebirth-1.6.9.zip | a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6 |
| CodeRebirth.dll | a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36 |
| com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll | 308ddf095d807b719c204c48bee3ce26795281c6b399baf3ac105e6b9d258163 |
| TeamXiaolan-DawnLib-0.9.25.zip | c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3 |
| com.github.teamxiaolan.dawnlib.dusk.dll | 3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03 |

EXACT_DEPENDENCY_CONTRACTS.json preserves signatures, declared owners, visibility, parameter metadata, local types, normalized IL offsets, exception-region offsets and raw method-body hashes for 13 narrowly selected methods. MemberRef generic parameters retain their CLI !0 notation; their constructed declaring owner is recorded separately. These are installed-package static facts, not observed loaded-process method identities.

Reproduction after obtaining the two already-pinned DLLs:
`python AnalysisTools/inspect_s142ak_bmafr1i1_contracts.py <existing-dll-directory>`

The output is deterministic for these DLLs. Python dependencies are analysis tools only and introduce no game/profile dependency or plugin package change. Existing DLL downloads are not newly built diagnostic DLLs.

## Exact Janitor contracts resolved

Declared owner: CodeRebirth.src.Content.Enemies.Janitor.
Inheritance corroborated by pinned upstream source: Janitor -> CodeRebirthEnemyAI -> EnemyAI.

| Declared method | Visibility | Parameters | Direct Unity write count | IL offset |
|---|---|---|---|---|
| SetBlendShapeWeightClientRpc | public instance | System.Int32 weight | 1 | 238 |
| KillEnemy | public virtual instance | System.Boolean destroy, optional | 1 | 327 |
| KeepPlayerAttachedDuringZoom | private instance | none | 1 | 87 |
| SwitchToChaseState | private instance | GameNetcodeStuff.PlayerControllerB player | 1 | 47 |

All return System.Void. KillEnemy's version-anchored source declares `public override void KillEnemy(bool destroy = false)`; the exact package metadata independently confirms the declared bool signature and optional parameter. There is no need for a guessed overload or inherited fallback.

All four exact direct calls are `UnityEngine.SkinnedMeshRenderer.SetBlendShapeWeight(System.Int32, System.Single)`. Their producer is EnemyAI.skinnedMeshRenderers[0], followed by blendshape index zero. The RPC converts its int argument to float; KillEnemy and KeepPlayerAttachedDuringZoom use 0f; SwitchToChaseState uses 100f.

The RPC contains its native transport/receive guards; observe only the direct receive-side write. KillEnemy includes native base cleanup, carried scrap/player cleanup, audio and light changes. KeepPlayerAttachedDuringZoom includes player attachment/reset and AI transitions. SwitchToChaseState includes chase/animation changes. No responsibility may be skipped or replaced. Observer exceptions must not escape into any of these original methods.

## Exact selector nuance: optional argument and generic declaring owner

Exact declared patch target:
`private static void Dusk.Internal.EntityReplacementRegistrationPatch.ReplaceEnemyEntity(On.EnemyAI.orig_Start orig, EnemyAI self)`.

The deployed IL contains exactly one selected non-default Apply call, inside an enumerator try/finally:

- IL 469: Dawn.Internal.StartOfRoundRefs.get_Instance();
- IL 474: load selected local 11;
- IL 476: load self;
- IL 477: load false for the optional immediate argument;
- IL 478: callvirt Apply on constructed owner Dusk.DuskEntityReplacementDefinition<EnemyAI>;
- IL 483: MonoBehaviour.StartCoroutine(IEnumerator);
- IL 488: pop Coroutine result.

The selected-definition Apply operand is a MemberRef on the constructed generic base, with signature `IEnumerator Apply(!0, bool)`. Pinned source also declares `DuskEnemyReplacementDefinition.Apply(EnemyAI ai, bool immediate = false)`. The shorthand `Apply(self)` must NEVER become a guessed one-parameter reflection target. The observation point remains the selector callsite authorized by Current/230, not a separately patched Apply method.

The transpiler must preserve the existing coroutine receiver, definition, self, immediate=false argument, original Apply and StartCoroutine calls, branches and exception-region boundaries. It may read the already selected definition and self through an inserted pure observer only. Do not replay candidate filtering, weights or RNG.

DuskEntityReplacementDefinition declares IsDefault as an instance bool field. It declares the auto-property getters SkinName and Replacements; Replacements is List<Dusk.Hierarchy>. Dusk.Hierarchy declares the string HierarchyPath getter. Resolve these members on their actual declared owners, not by scanning derived member names.

For selector invocations without proven selected non-default observation, use SELECTION_STATE_INCONCLUSIVE unless a separate exact side-effect-free lookup or branch contract is validated. Absence of a callback is not DEFAULT, NO_DUSK_DEFINITION or ALREADY_REPLACED evidence. Invoke no RNG/selection code to improve classification.

## Dusk renderer/material contracts and read-only boundary

- Dusk.SkinnedMeshReplacement.ReplaceSkinnedMeshRenderer(UnityEngine.SkinnedMeshRenderer): private instance void.
- Dusk.MaterialsReplacement.CopyOrResizeMaterials(UnityEngine.Renderer, UnityEngine.Material[], System.Int32): assembly-visible static void.
- Dusk.SkinnedMeshReplacement.get_ReplacementRenderer(): public instance SkinnedMeshRenderer.
- Dusk.SkinnedMeshReplacement.BuildBoneLookup(Transform): private static Dictionary<string, Transform>, inspected only as the bone-mapping rule; not an additional patch target.

The bone lookup visits descendants including inactive objects under the original root bone and retains the first Transform for each exact name. Blank/missing source bone names fall back to the original root. Prediction must reproduce this read-only naming rule under the correlated root and must not mutate bones or call the foreign mutation helper.

Use sharedMesh/sharedMaterials reads, avoiding Renderer.material/materials getters that can instantiate materials. Do not suppress Dusk's warning. Filter material probes to previously correlated targets. Full renderer snapshots remain Janitor/SpringMan-only; lightweight selection/action records cover other selected Dusk enemies.

## Implementation work remaining

1. Add separately versioned Patches/S142AKBMAFR1I1 source and project metadata, exact runtime resolution/body/callsite validation, ordered explicit Harmony installation and rollback via UnpatchSelf.
2. Implement selector and four Janitor stack-preserving observers, Dusk mesh/material prefix/postfix observers, bounded instance tracking and identical Janitor/SpringMan snapshot schemas.
3. Add atomic/minimal exact-signature Unity log correlation, main-thread bounded summaries, common identity/time envelope, and fail-closed/inconclusive observer handling.
4. Add the source/static validator with meaningful negative cases for dangerous deltas and ambiguous contracts, a static-only workflow, source plan and patch-safety documentation.
5. Review exact PR-head gates and integrate/reconcile only after successful verification. Any CURRENT_STATE edit must regenerate renderer-owned navigation. This preparation has not performed those steps.

The static gate must distinguish evidence of an exact dependency body from proof that the new injection preserves stack/branches/original calls. A list of required source strings alone cannot establish the latter. No DLL build, compiled test harness, profile construction or runtime execution is permitted.

## Preserved lifecycle and attribution boundary

S1.42AK remains accepted. S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED; its DeepSewersFlow gate remains passive, outstanding and unwaived, with no dedicated reroll. BMAFR1 Black Mesa x Abandoned Foundry retains its bounded compatibility PASS; BMAFR1 remains DIAGNOSTIC ONLY / NEVER ACCEPT / inactive. BMAFDIAG1 and PATH1 remain DO NOT RERUN.

BuildSpecs/current.json is still disabled at IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS. RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK-BMDSFIX1 and is only evidence attribution. No new runtime run is authorized.

Observed Princess selection, live Janitor blendShapeCount==0, exact array emitter, native Unity ownership and root cause remain unproven. SpringMan remains a contemporaneous alternative.
