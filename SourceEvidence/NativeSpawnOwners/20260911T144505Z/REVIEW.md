# S1.42AI-DIAG1 native spawn-owner discovery: batch 1

**Status:** DISCOVERY_COMPLETE_FOR_SEVEN_PACKAGES / PATCH_SAFETY_OPEN / NOT_BUILT
**Date:** 2026-09-11
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`

## Scope and provenance

Read-only analysis run [34611826588](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/34611826588)
completed successfully on `71973b25c395cef4d0022a0054975cdab44e37d2`.
Artifact `10268522778` has ZIP SHA-256
`40d5c51d3211f8a31388e91592ca08d07c61a9a792247307f90a14b10b660e06`.

The analysis verifies the active S1.42AI profile SHA, exact archive export versus
ProfileSources and export SHA versus FILE_INDEX before deriving every package version.
It records all 188 export entries: 183 enabled and five disabled. Five embedded
project DLLs are separately inventoried. An enabled export entry is profile intent,
not proof of a successful live load.

This bounded batch follows the canonical native-owner examples, Pikmin/CodeRebirth
topics and the newly reviewed V81 nest/scheduling surfaces. It captures all DLLs in
seven selected package archives: 11 assemblies and 12 reports including the package
inventory, plus the manifest. It is not a full-repository audit or a complete scan
of all enabled package code.

The connector produced an artifact reference but its temporary download could not
be consumed in this workspace. Scoped preservation run
[34612304735](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/34612304735)
therefore fetched the original artifact through GitHub Actions, verified its run,
source commit, ZIP digest, exact 13-file inventory and each declared report hash,
and committed its original UTF-8 text files on the analysis branch only.
Publication commit: `7ebd8b41a0fe5b7b0d8604a43657251e43819936`.
CAPTURE_INDEX.json records all retained byte lengths and SHA-256 values.
After repository retrieval, all 13 persisted file hashes and byte lengths were
independently recomputed and matched that index.

## Source findings and next exact owners

References below are discovery report names and original decompile line numbers.
They identify source locations, not fully reviewed method bodies.

| Exact package | Observed source surface | Required consequence |
| --- | --- | --- |
| NotezyTeam-LethalMinNightly 1.1.108 | PikminAI and PuffminAI derive from EnemyAI (21960, 42052); PikminManager derives from NetworkBehaviour (36164). Direct enemy-prefab instantiation appears at 28365, 38273, 38315 and 52140; SpawnPikminServerRpc appears at 38206. | Review PikminManager creation, PikminAI conversion and the source owner around 52140. A blanket family exemption cannot establish Shy-Guy-only isolation. Do not disable PikminManager, Onion or compatibility-adapter lifecycles wholesale. |
| XuXiaolan-CodeRebirth 1.6.9 | EnemyLevelSpawner (8219) calls SpawnEnemyGameObject with explicit EnemyType (8324); many other calls supply exact enemy registry entries. CodeRebirthEnemyAI derives from EnemyAI (50213). | Inspect explicit-type consumers and their return-value expectations before denying creation. Several calls are item/hazard/AI driven, so normal spawn weights alone are insufficient. |
| XuXiaolan-CodeRebirth 1.6.9, companion DLL | Package additionally includes com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll with DuskEnemyReplacementDefinition subclasses. | Include this DLL in prefab/identity and replacement-owner review. The package is not represented by CodeRebirth.dll alone. |
| TeamXiaolan-DawnLib 0.9.25 | Four DLLs are present, including Dusk. Dusk report exposes DuskEnemyReplacementDefinition, EnemyAIExtensions, EnemyAINestSpawnObjectExtensions and EntityReplacementRegistrationPatch. | Trace actual replacement/registration behavior before assuming that the initially registered prefab/type is the final runtime identity. These declarations do not prove an extra spawn by themselves. |
| SoftDiamond-RollingGiant 2.6.3 | RollingGiantAI derives from EnemyAI (594). EnemyPatches registers through StartOfRound.Awake / RoundManager.Start (2484, 2494). The direct Instantiate/Spawn hits at 2741-2742 use _networkPrefab in NetworkPatches. | Separate registration and network infrastructure from enemy creation. These generic spawn tokens do not justify disabling the network helper. |
| Ccode_lang-SirenHead 2.0.7 | Plugin calls Enemies.RegisterEnemy (107), and SirenHeadAI derives from EnemyAI (199). | Follow registration/list ownership in the exact plugin. A single registration hit is not proof that every possible spawn path has been covered. |
| PureFPSZac-NestFix 1.3.0 | Harmony target RoundManager.SpawnNestObjectForOutsideEnemy (259), bool prefix declaration (260), direct nest Instantiate (325), NetworkObject.Spawn (333) and nest registration (341). | The installed package patches the exact native method reviewed earlier and contains its own creation code. Review complete prefix responsibilities and ordering before choosing a diagnostic hook. |
| ButteryStancakes-SpawnCycleFixes 1.2.2 | Targets include AssignRandomEnemyToVent, SpawnRandomOutsideEnemy, BeginEnemySpawning, PlotOutEnemiesForNextHour, PredictAllOutsideEnemies and outside/daytime/weed batch methods. EnemyAI.SubtractFromPowerLevel is also patched. | The original V81 bodies are not the whole installed execution contract. Inspect exact patches, ordering and power/schedule effects. Zero direct spawn-pattern hits do not mean no spawn influence. |

The exact namespace-qualified class inventory, package archive hashes, DLL hashes,
source hashes and all matched lines are retained in the corresponding DISCOVERY.json
files. Candidate patch ownership is not inferred merely from a type or method name.

## Important limitations

The collector records class/namespace declarations and matching source lines, not
complete bodies or a verified call graph. Its patterns can match declarations,
comments, non-enemy infrastructure and inactive code; absence of a match cannot
establish absence of spawning. Some decompile output contains unresolved-reference
annotations, including attribute decoding limits. Resolve dependencies and inspect
complete exact methods before installing Harmony hooks.

Other enabled packages remain listed in PROFILE_PACKAGE_INVENTORY.json under
excluded_from_this_batch. This means outside this batch, not approved or irrelevant.
The five embedded project DLLs are inventoried but not newly decompiled here.
Scopophobia/BCMER and the installed V81 capture retain their separate prior evidence.

In particular, no global NetworkObject.Spawn interception, EnemyAI lifecycle
suppression, post-spawn cleanup or new arbitrary exemption is approved.
Unexpected exterior Shy Guy remains observable under the canonical diagnostic contract.

## Next bounded work

After merging this evidence and analysis tooling, review the complete exact NestFix
and SpawnCycleFixes patches first: they already overlap proposed vanilla interception
surfaces. Then use the retained LethalMin/CodeRebirth/Dusk locations to close direct
creation, return-value and replacement ownership, followed by the remaining package
inventory and native vent/nest gaps. Preserve the BCMER forced/side-event gate.

No gameplay test, local capture rerun, build trigger, controller transition or
acceptance decision is made by this discovery checkpoint.
