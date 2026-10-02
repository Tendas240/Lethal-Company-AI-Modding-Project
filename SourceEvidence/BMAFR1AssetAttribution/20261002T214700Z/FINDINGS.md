# BMAFR1 supplemental array-index flood: bounded asset-level attribution

Date: 2026-10-02
Status: STATIC ASSET-LEVEL ATTRIBUTION COMPLETE; JANITOR/PRINCESS ZERO-BLENDSHAPE MECHANISM SUBSTANTIALLY STRENGTHENED; OBSERVED INSTANCE SELECTION / ARRAY EMITTER / ROOT CAUSE UNPROVEN
Analysis base: main c5e93ac674f7913795af90567e21be82e36734f6
Authority boundary: evidence-only static attribution. No gameplay/config/profile/DLL/package/controller changes. No build or runtime authorization.

## Result

The bounded static asset layer materially strengthens the Janitor/DawnLib.Dusk hypothesis without crossing the root-cause boundary.

Version-anchored CodeRebirth 1.6.9 source contains one Janitor-targeted Dusk skin definition, "Princess". Its ordered replacement actions target hierarchy path "Janitor" first with SkinnedMeshReplacement, then with MaterialsReplacement. The original Janitor prefab renderer at that path serializes one blendshape-weight slot, three materials, mesh GUID 8a1ede2ad9c4ad246910ced9abe8be7b, and root bone Root. The Princess replacement source points at PrettyPrincess.fbx GUID 5843902a38d026d4ea12797ccd49ffe5; its Unity importer has importBlendShapes: 0.

Exact DawnLib 0.9.25 source replaces the target renderer's sharedMesh, remaps bones only by transform name, then resizes original materials to the replacement mesh's subMeshCount. It contains no blendshape compatibility check/remap in that path. CodeRebirth Janitor source, already preserved in the prior checkpoint, contains direct SetBlendShapeWeight(0, ...) calls without a local blendShapeCount guard. Thus a concrete index-0 / zero-imported-blendshape compatibility mechanism is statically established for the Princess candidate.

This still does not prove that Princess was selected in the observed supplemental run, that the live package asset had exactly the source-state mesh properties at runtime, or that the Unity array message came from the blendshape subsystem.

## Provenance

Prior exact deployed-package identities remain inherited from SourceEvidence/BMAFR1Performance/20261002T173617Z/FINDINGS.md:
- XuXiaolan-CodeRebirth 1.6.9 ZIP SHA-256 a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6.
- CodeRebirth.dll SHA-256 a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36.
- com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll SHA-256 308ddf095d807b719c204c48bee3ce26795281c6b399baf3ac105e6b9d258163.
- TeamXiaolan-DawnLib 0.9.25 ZIP SHA-256 c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3.
- com.github.teamxiaolan.dawnlib.dusk.dll SHA-256 3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03.

Version-anchored upstream source used for the asset/source layer:
- CodeRebirth commit 3aec94f6f737c86d5e1eb59a57396740317b210f; Plugin/Directory.Build.props states version 1.6.9.
- DawnLib commit 810613e556ecc357eac25e97c25a3bb90516f071; Directory.Build.props states version 0.9.25.

This source anchoring is intentionally weaker than decoding the exact deployed asset bundle byte-for-byte. Do not convert source metadata into a claim that the observed live mesh was inspected directly.

## Janitor / Princess definition

CodeRebirth 1.6.9 PrincessEnemyReplacementDefinition.asset:
- skin key: code_rebirth:princess
- entity to replace: code_rebirth:janitor
- replacement action order: PrincessSkinnedMeshReplacement, then PrincessMaterialsReplacement
- date predicate: shared Halloween predicate
- preset moon weights: lethal_company:vanilla = 9999; lethal_company:custom = 9999

The complete CodeRebirth 1.6.9 Skins/**/EnemyReplacementDefinition.asset set contains 15 enemy definitions. Within that set, Princess is the Janitor-targeted definition and no definition targets SpringMan / Coilhead.

### Target hierarchy and original renderer

PrincessSkinnedMeshReplacement.asset uses HierarchyPath = Janitor and replacement renderer source PrettyPrincess.fbx, GUID 5843902a38d026d4ea12797ccd49ffe5.

PrincessMaterialsReplacement.asset uses HierarchyPath = Janitor and replacement material index 3.

The CodeRebirth Janitor prefab contains a child GameObject named Janitor with a SkinnedMeshRenderer:
- three original material slots;
- mesh GUID 8a1ede2ad9c4ad246910ced9abe8be7b;
- exactly one serialized m_BlendShapeWeights entry, value 0;
- m_RootBone resolves to transform Root;
- the next major skeleton node is Fullbody.

The original Janitor.fbx.meta has importBlendShapes: 1. The exact original blendshape name was not recovered from repository-native text evidence.

### Replacement mesh / blendshape boundary

PrettyPrincess.fbx.meta has importBlendShapes: 0, one externally mapped material named PrettyPrincess, and no imported animation clips.

This establishes a zero-imported-blendshape source definition for the Princess mesh. The binary FBX is Git-LFS-backed and the exact deployed package asset bundle was not decoded in this segment, so the evidence must not be restated as direct inspection of the observed live Mesh.blendShapeCount.

### Bone behavior

DawnLib 0.9.25 SkinnedMeshReplacement.ReplaceSkinnedMeshRenderer builds a target-bone lookup under the original renderer's root bone, maps every replacement bone by name, falls back to the original root bone when a replacement bone name cannot be mapped, attempts to map the replacement root-bone name, assigns targetSkinned.sharedMesh = newMesh, assigns mapped bones/root bone, and performs no blendshape-name/count validation or remap.

The source therefore supports a mesh/skeleton transfer mechanism, but no static bone-name mismatch was proven from the text-only source layer because the replacement FBX binary bone list was not recovered.

### Animator / AnimationClip bindings

The CodeRebirth 1.6.9 Janitor animation directory was checked across all .anim assets.
- No blendShape.* binding was found.
- Animation paths are under JanitorArmature/..., including JanitorArmature/Root/Fullbody/....
- No animation binding was found on the separate renderer node path Janitor.

The blendshape risk in the reviewed Janitor path therefore comes from direct Janitor code writes, not from a recovered Janitor AnimationClip blendshape binding.

## Runtime-warning fingerprint

The supplemental run contains: TransferRenderer: Material count mismatch (got 3, need 4). Resized with fallback materials.

Exact DawnLib 0.9.25 source defines got = originalMaterials.Length and need = newMesh.subMeshCount.

The Janitor target renderer statically has three original material slots, matching got 3. Princess then contains a second ordered action that replaces material index 3 (the fourth material slot). This is structurally consistent with a Princess replacement mesh whose applied renderer has at least four material slots. The observed got 3, need 4 warning is therefore a strong fingerprint match for the Janitor/Princess action shape.

Limits:
- the warning does not log the target object, replacement key or mesh name;
- the source FBX metadata does not expose the replacement mesh's exact subMeshCount;
- another replacement could theoretically produce the same 3 -> 4 count pair.

Accordingly, this materially strengthens but does not prove observed Princess selection.

## Date / weight / seed selection boundary

The Princess Halloween predicate uses Month | Day flags and spans October 1 through November 10. October 2 is inside the default date window. If the generated disable-date config is enabled, the predicate is bypassed rather than becoming an exclusion.

Dusk registers a default replacement at global weight 100 and registers non-default replacements through their weight tables. Princess declares preset moon-category weights 9999 for vanilla and custom categories.

Dusk replacement RNG is initialized from mapSeed + 234780. For supplemental seed 18486762, the initial seed value is 18721542. This is not enough to reconstruct the Janitor draw: the RNG instance is shared through replacement selection and the exact preceding draw count/order/runtime candidate context is not preserved in the available evidence. Do not claim deterministic Princess selection from the map seed alone.

## SpringMan equal-scope attribution

SpringMan was kept in scope rather than excluded by Janitor findings.

Within the routed/version-anchored CodeRebirth 1.6.9 Dusk skin set, no replacement definition targets SpringMan / Coilhead. Repository searches of the current project do not expose a repository-indexed vanilla SpringMan prefab/mesh/animation asset with exact provenance. The profile's separate AntlerShed.EnemySkinRegistry/config.json lists LethalCompany.Coilhead with activeSkins: [], but that only constrains that separate skin system and does not prove the absence of every possible runtime renderer mutation.

Therefore:
- no concrete Dusk SpringMan replacement action/hierarchy/mesh incompatibility is statically established from the routed evidence;
- exact SpringMan original SkinnedMeshRenderer, blendshape names/count, bones/root bone and animation bindings remain unavailable under current repository-native provenance;
- SpringMan remains a contemporaneous runtime alternative candidate and must not be excluded solely because Janitor now has a stronger mechanism.

## Reassessment

Static attribution is exhausted to the useful boundary available from current repository/package/source provenance.

A concrete Janitor/Princess zero-imported-blendshape mechanism is now established and the observed Dusk 3 -> 4 material-warning fingerprint materially strengthens instance-level suspicion. However, the missing observed replacement key/target/live mesh state and stackless array signature still prevent root-cause closure.

Narrowly instrumented runtime evidence is now technically justified for attribution, but is NOT authorized by this evidence checkpoint. A future design must log, at minimum, for Janitor and SpringMan:
- enemy instance identity / network object identity;
- selected Dusk replacement key and skin name, or explicit default/no-replacement state;
- replacement action type and hierarchy path;
- target renderer name/path before and after replacement;
- original and replacement mesh names;
- live blendShapeCount, blendshape names and material/submesh counts;
- root bone and mapped/unmapped bone names;
- every Janitor index-0 blendshape write with current live mesh identity/count;
- enough timestamp/instance correlation to associate any array signature without assuming native Unity ownership.

No patch, inactive review build, runtime activation or runtime run is released here.

## Lifecycle preservation

Preserved unchanged:
- S1.42AK remains accepted.
- S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED.
- BMDSFIX1 Black Mesa x DeepSewersFlow remains passive, outstanding and unwaived.
- No dedicated BMDSFIX1 reroll is released.
- BMAFR1 Black Mesa x Abandoned Foundry bounded compatibility PASS remains valid.
- BMAFR1 remains DIAGNOSTIC ONLY / NEVER ACCEPT / inactive.
- No further BMAFR1 qualification run is released.
- BMAFDIAG1 and BMAFDIAG1PATH1 remain DO NOT RERUN.
- BuildSpecs/current.json remains disabled at IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS.
