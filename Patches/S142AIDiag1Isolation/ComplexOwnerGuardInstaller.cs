using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using BepInEx.Bootstrap;
using HarmonyLib;
using Unity.Netcode;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    internal static class ComplexOwnerGuardInstaller
    {
        private sealed class Target
        {
            internal string Label;
            internal MethodInfo Original;
            internal HarmonyMethod Prefix;
            internal HarmonyMethod Transpiler;
        }

        internal static bool InstallComplexGuards(Harmony harmony)
        {
            if (harmony == null)
            {
                Plugin.Log.LogError("[DIAG1_COMPLEX_TARGET_INVALID] Harmony instance is null.");
                return false;
            }

            List<Target> targets = new List<Target>();
            bool valid = true;

            // PremiumScraps 2.5.0: direct prefab/network helper. The build gate still
            // has to re-prove the reviewed ignored-return caller invariant before the
            // implementation-complete latch can be released.
            valid &= AddPrefix(
                targets,
                "PremiumScraps Effects.Spawn(SpawnableEnemyWithRarity,Vector3,float)",
                "PremiumScraps.Utils.Effects",
                "Spawn",
                new[] { typeof(SpawnableEnemyWithRarity), typeof(Vector3), typeof(float) },
                typeof(NetworkObjectReference),
                expectedStatic: true,
                nameof(ComplexOwnerGuardPatches.PremiumSpawnPrefix));

            valid &= AddPrefix(
                targets,
                "PremiumScraps Effects.SpawnMaskedOfPlayer(ulong,Vector3)",
                "PremiumScraps.Utils.Effects",
                "SpawnMaskedOfPlayer",
                new[] { typeof(ulong), typeof(Vector3) },
                typeof(void),
                expectedStatic: true,
                nameof(ComplexOwnerGuardPatches.BlockFixedVoidOwnerPrefix));

            // ChillaxScraps 1.6.6: the Ocarina owner RPC is already part of the simple
            // guard layer; this guard covers only the reviewed non-Ocarina helper
            // family whose callers must remain ignored-return at the static gate.
            valid &= AddPrefix(
                targets,
                "ChillaxScraps Effects.Spawn(SpawnableEnemyWithRarity,Vector3,float)",
                "ChillaxScraps.Utils.Effects",
                "Spawn",
                new[] { typeof(SpawnableEnemyWithRarity), typeof(Vector3), typeof(float) },
                typeof(NetworkObjectReference),
                expectedStatic: true,
                nameof(ComplexOwnerGuardPatches.ChillaxSpawnPrefix));

            // JLL 1.10.1: branch immediately after local EnemyType selection and before
            // cap/power/navmesh/nest/spawn work.
            valid &= AddTranspiler(
                targets,
                "JLL EnemySpawner.SpawnEnemy(Vector3)",
                "JLL.Components.EnemySpawner",
                "SpawnEnemy",
                new[] { typeof(Vector3) },
                typeof(void),
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.JllEnemySpawnerTranspiler));

            // KenjiLib 0.7.0: patch the compiler-emitted iterator MoveNext resolved from
            // IteratorStateMachineAttribute, never a guessed generated type name.
            valid &= AddIteratorTranspiler(
                targets,
                "KenjiLib KLightsEvent.PermanentPowerOffRoutine()",
                "KenjiLib.Scripts.KLightsEvent",
                "PermanentPowerOffRoutine",
                Type.EmptyTypes,
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.KenjiPermanentPowerOffTranspiler));

            valid &= AddIteratorTranspiler(
                targets,
                "KenjiLib KLightsEvent.TriggerAppyEventRoutine()",
                "KenjiLib.Scripts.KLightsEvent",
                "TriggerAppyEventRoutine",
                Type.EmptyTypes,
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.KenjiTriggerAppyTranspiler));

            // itolib 0.9.3: same exact iterator-state-machine resolution. Only the one
            // ignored-result Old Bird spawn call in each lifecycle is replaced.
            valid &= AddIteratorTranspiler(
                targets,
                "itolib EventfulApparatus.HandleDisconnect()",
                "itolib.Behaviours.Grabbables.EventfulApparatus",
                "HandleDisconnect",
                Type.EmptyTypes,
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.ItolibEventfulDisconnectTranspiler));

            valid &= AddIteratorTranspiler(
                targets,
                "itolib TwinApparatus.HandleDisconnect()",
                "itolib.PlayZone.TwinApparatus",
                "HandleDisconnect",
                Type.EmptyTypes,
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.ItolibTwinDisconnectTranspiler));

            // CodeRebirth 1.6.9 complex owner paths. Tornado, GuardPhone and BoxChute
            // are already covered by exact simple Prefixes.
            valid &= AddTranspiler(
                targets,
                "CodeRebirth EnemyLevelSpawner.SpawnRandomEnemy()",
                "CodeRebirth.src.MiscScripts.EnemyLevelSpawner",
                "SpawnRandomEnemy",
                Type.EmptyTypes,
                typeof(EnemyAI),
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.CodeRebirthEnemyLevelSpawnerTranspiler));

            valid &= AddTranspiler(
                targets,
                "CodeRebirth FakeSnailCat.Update()",
                "CodeRebirth.src.Content.Items.FakeSnailCat",
                "Update",
                Type.EmptyTypes,
                typeof(void),
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.CodeRebirthFakeSnailTranspiler));

            valid &= AddTranspiler(
                targets,
                "CodeRebirth Xui.OnNetworkDespawn()",
                "CodeRebirth.src.Content.Items.Xui",
                "OnNetworkDespawn",
                Type.EmptyTypes,
                typeof(void),
                expectedStatic: false,
                nameof(ComplexOwnerGuardPatches.CodeRebirthXuiTranspiler));

            // LethalMinNightly 1.1.108 compiles this compatibility owner even when its
            // foreign provider is absent. Mirror LethalMin's exact CompatClass gate:
            // kite.ZelevatorCode absent => NOT_APPLICABLE; present => exact target required.
            valid &= AddEndlessElevatorCompatTarget(targets);

            if (!valid)
            {
                Plugin.Log.LogError(
                    "[DIAG1_COMPLEX_TARGET_INVALID] At least one complex owner target failed exact prevalidation. No complex owner patches were installed.");
                return false;
            }

            foreach (Target target in targets)
            {
                try
                {
                    harmony.Patch(
                        target.Original,
                        prefix: target.Prefix,
                        postfix: null,
                        transpiler: target.Transpiler,
                        finalizer: null,
                        ilmanipulator: null);
                    Plugin.Log.LogInfo($"[DIAG1_COMPLEX_TARGET_INSTALLED] {target.Label}");
                }
                catch (Exception ex)
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_COMPLEX_TARGET_INVALID] Failed to install {target.Label}: {ex.GetType().Name}: {ex.Message}");
                    return false;
                }
            }

            return true;
        }

        private const string EndlessElevatorDependencyGuid = "kite.ZelevatorCode";
        private const string EndlessElevatorProviderAssemblyName = "kite.ZelevatorCode";
        private const string EndlessElevatorProviderTypeName = "ElevatorMod.Patches.EndlessElevator";
        private const string EndlessElevatorOwnerTypeName = "LethalMin.Compats.EndlessElevatorPatch";
        private const string EndlessElevatorOwnerAssemblyName = "NoteBoxz.LethalMin";

        private static bool AddEndlessElevatorCompatTarget(List<Target> targets)
        {
            const string label = "LethalMin EndlessElevatorPatch.WaitRespawnPikmin(EndlessElevator)";

            // Exact LethalMin 1.1.108 source uses CompatClass("kite.ZelevatorCode") and
            // IsDependencyLoaded -> Chainloader.PluginInfos.ContainsKey. Do not touch the
            // foreign CLR type unless that exact dependency is applicable in this runtime.
            if (!Chainloader.PluginInfos.TryGetValue(EndlessElevatorDependencyGuid, out var pluginInfo))
            {
                Plugin.Log.LogInfo(
                    $"[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE] {label}: exact LethalMin CompatClass dependency '{EndlessElevatorDependencyGuid}' is not loaded.");
                return true;
            }

            if (pluginInfo == null ||
                pluginInfo.Metadata == null ||
                !string.Equals(pluginInfo.Metadata.GUID, EndlessElevatorDependencyGuid, StringComparison.Ordinal) ||
                pluginInfo.Instance == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: dependency '{EndlessElevatorDependencyGuid}' is registered but its exact loaded PluginInfo/instance contract did not validate.");
                return false;
            }

            Assembly providerAssembly = pluginInfo.Instance.GetType().Assembly;
            string providerAssemblyName = providerAssembly.GetName().Name;
            if (!string.Equals(providerAssemblyName, EndlessElevatorProviderAssemblyName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: dependency '{EndlessElevatorDependencyGuid}' resolved from assembly '{providerAssemblyName}', expected exact provider assembly '{EndlessElevatorProviderAssemblyName}'.");
                return false;
            }

            Type endlessElevator = providerAssembly.GetType(
                EndlessElevatorProviderTypeName,
                throwOnError: false,
                ignoreCase: false);
            if (endlessElevator == null ||
                endlessElevator.Assembly != providerAssembly ||
                !string.Equals(endlessElevator.FullName, EndlessElevatorProviderTypeName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: applicable provider assembly '{EndlessElevatorProviderAssemblyName}' did not expose exact CLR type '{EndlessElevatorProviderTypeName}'.");
                return false;
            }

            Type owner = ResolveRequiredType(EndlessElevatorOwnerTypeName);
            if (owner == null ||
                !string.Equals(owner.Assembly.GetName().Name, EndlessElevatorOwnerAssemblyName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: exact owner '{EndlessElevatorOwnerTypeName}' was not resolved from assembly '{EndlessElevatorOwnerAssemblyName}'.");
                return false;
            }

            MethodInfo original = ResolveExactDeclaredMethod(
                label,
                EndlessElevatorOwnerTypeName,
                "WaitRespawnPikmin",
                new[] { endlessElevator },
                typeof(IEnumerator),
                expectedStatic: true);
            MethodInfo prefix = ResolveOwnPatchMethod(nameof(ComplexOwnerGuardPatches.BlockIteratorOwnerPrefix));
            if (original == null || original.DeclaringType != owner || prefix == null)
                return false;

            targets.Add(new Target
            {
                Label = label,
                Original = original,
                Prefix = new HarmonyMethod(prefix) { priority = Priority.First }
            });
            Plugin.Log.LogInfo(
                $"[DIAG1_COMPLEX_TARGET_APPLICABLE] {label}: dependency='{EndlessElevatorDependencyGuid}', providerAssembly='{providerAssemblyName}', providerType='{endlessElevator.FullName}'.");
            return true;
        }

        private static bool AddPrefix(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            bool? expectedStatic,
            string prefixName)
        {
            MethodInfo original = ResolveExactDeclaredMethod(
                label,
                ownerTypeName,
                methodName,
                parameters,
                returnType,
                expectedStatic);
            MethodInfo prefix = ResolveOwnPatchMethod(prefixName);
            if (original == null || prefix == null)
                return false;

            targets.Add(new Target
            {
                Label = label,
                Original = original,
                Prefix = new HarmonyMethod(prefix) { priority = Priority.First }
            });
            return true;
        }

        private static bool AddTranspiler(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            bool? expectedStatic,
            string transpilerName)
        {
            MethodInfo original = ResolveExactDeclaredMethod(
                label,
                ownerTypeName,
                methodName,
                parameters,
                returnType,
                expectedStatic);
            MethodInfo transpiler = ResolveOwnPatchMethod(transpilerName);
            if (original == null || transpiler == null)
                return false;

            targets.Add(new Target
            {
                Label = label,
                Original = original,
                Transpiler = new HarmonyMethod(transpiler) { priority = Priority.First }
            });
            return true;
        }

        private static bool AddIteratorTranspiler(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            bool? expectedStatic,
            string transpilerName)
        {
            MethodInfo semanticMethod = ResolveExactDeclaredMethod(
                label,
                ownerTypeName,
                methodName,
                parameters,
                typeof(IEnumerator),
                expectedStatic);
            MethodInfo transpiler = ResolveOwnPatchMethod(transpilerName);
            if (semanticMethod == null || transpiler == null)
                return false;

            MethodInfo moveNext = ResolveExactIteratorMoveNext(label, semanticMethod);
            if (moveNext == null)
                return false;

            targets.Add(new Target
            {
                Label = label + " -> exact iterator MoveNext",
                Original = moveNext,
                Transpiler = new HarmonyMethod(transpiler) { priority = Priority.First }
            });
            return true;
        }

        private static MethodInfo ResolveExactDeclaredMethod(
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            bool? expectedStatic)
        {
            Type owner = ResolveRequiredType(ownerTypeName);
            if (owner == null)
                return null;

            MethodInfo method = owner.GetMethod(
                methodName,
                BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                parameters ?? Type.EmptyTypes,
                null);

            if (method == null ||
                method.DeclaringType != owner ||
                method.ReturnType != returnType ||
                method.IsAbstract ||
                method.ContainsGenericParameters ||
                method.GetMethodBody() == null ||
                (expectedStatic.HasValue && method.IsStatic != expectedStatic.Value))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: exact declared {ownerTypeName}.{methodName}({DescribeTypes(parameters)}) -> {returnType.FullName} did not validate; expectedStatic={(expectedStatic.HasValue ? expectedStatic.Value.ToString() : "<any>")}.");
                return null;
            }

            ParameterInfo[] actual = method.GetParameters();
            Type[] expected = parameters ?? Type.EmptyTypes;
            if (actual.Length != expected.Length)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: parameter-count mismatch {actual.Length} != {expected.Length}.");
                return null;
            }

            for (int i = 0; i < actual.Length; i++)
            {
                if (actual[i].ParameterType != expected[i])
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: parameter {i} mismatch; expected {expected[i].FullName}, got {actual[i].ParameterType.FullName}.");
                    return null;
                }
            }

            return method;
        }

        private static MethodInfo ResolveExactIteratorMoveNext(string label, MethodInfo semanticMethod)
        {
            IteratorStateMachineAttribute attribute = semanticMethod.GetCustomAttribute<IteratorStateMachineAttribute>();
            Type stateMachineType = attribute?.StateMachineType;
            if (stateMachineType == null || stateMachineType.DeclaringType != semanticMethod.DeclaringType)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: IteratorStateMachineAttribute did not resolve an exact nested state-machine type.");
                return null;
            }

            MethodInfo moveNext = stateMachineType.GetMethod(
                "MoveNext",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                Type.EmptyTypes,
                null);

            if (moveNext == null ||
                moveNext.DeclaringType != stateMachineType ||
                moveNext.IsStatic ||
                moveNext.ReturnType != typeof(bool) ||
                moveNext.GetMethodBody() == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: exact iterator MoveNext failed signature/body validation.");
                return null;
            }

            Plugin.Log.LogInfo(
                $"[DIAG1_ITERATOR_TARGET_VALIDATED] {label}: stateMachine='{stateMachineType.FullName}', MoveNext token=0x{moveNext.MetadataToken:X8}.");
            return moveNext;
        }

        private static MethodInfo ResolveOwnPatchMethod(string name)
        {
            MethodInfo method = typeof(ComplexOwnerGuardPatches).GetMethod(
                name,
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);
            if (method == null || method.GetMethodBody() == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] Internal patch method {typeof(ComplexOwnerGuardPatches).FullName}.{name} did not validate.");
                return null;
            }
            return method;
        }

        private static Type ResolveRequiredType(string fullName)
        {
            Type type = AccessTools.TypeByName(fullName);
            if (type == null)
                Plugin.Log.LogError($"[DIAG1_COMPLEX_TARGET_INVALID] Required exact type '{fullName}' was not found.");
            return type;
        }

        private static string DescribeTypes(Type[] types)
        {
            return string.Join(",", (types ?? Type.EmptyTypes).Select(t => t?.FullName ?? "<null>"));
        }
    }

    internal static class ComplexOwnerGuardPatches
    {
        public static bool PremiumSpawnPrefix(
            SpawnableEnemyWithRarity __0,
            ref NetworkObjectReference __result,
            MethodBase __originalMethod)
        {
            return GuardDirectSpawnHelper(
                __0,
                ref __result,
                __originalMethod,
                "PremiumScraps.Utils.Effects.Spawn");
        }

        public static bool ChillaxSpawnPrefix(
            SpawnableEnemyWithRarity __0,
            ref NetworkObjectReference __result,
            MethodBase __originalMethod)
        {
            return GuardDirectSpawnHelper(
                __0,
                ref __result,
                __originalMethod,
                "ChillaxScraps.Utils.Effects.Spawn");
        }

        public static bool BlockFixedVoidOwnerPrefix(MethodBase __originalMethod)
        {
            ComplexOwnerGuardRuntime.LogBlocked(
                __originalMethod?.DeclaringType?.FullName + "." + __originalMethod?.Name,
                "fixed non-ShyGuy owner transaction blocked before spawn/state synchronization");
            return false;
        }

        public static bool BlockIteratorOwnerPrefix(ref IEnumerator __result, MethodBase __originalMethod)
        {
            __result = EmptyIterator();
            ComplexOwnerGuardRuntime.LogBlocked(
                __originalMethod?.DeclaringType?.FullName + "." + __originalMethod?.Name,
                "persistence iterator replaced with empty iterator before field-Pikmin creation/clear");
            return false;
        }

        public static IEnumerable<CodeInstruction> JllEnemySpawnerTranspiler(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            return ComplexOwnerTranspilers.InsertJllDecisionGuard(instructions, generator);
        }

        public static IEnumerable<CodeInstruction> KenjiPermanentPowerOffTranspiler(
            IEnumerable<CodeInstruction> instructions)
        {
            return ComplexOwnerTranspilers.ReplaceIgnoredSpawnCalls(
                instructions,
                nameof(ComplexOwnerGuardRuntime.KenjiPermanentPowerOffSpawn),
                expectedCount: 1,
                label: "KenjiLib KLightsEvent.PermanentPowerOffRoutine");
        }

        public static IEnumerable<CodeInstruction> KenjiTriggerAppyTranspiler(
            IEnumerable<CodeInstruction> instructions)
        {
            return ComplexOwnerTranspilers.ReplaceIgnoredSpawnCalls(
                instructions,
                nameof(ComplexOwnerGuardRuntime.KenjiTriggerAppySpawn),
                expectedCount: 1,
                label: "KenjiLib KLightsEvent.TriggerAppyEventRoutine");
        }

        public static IEnumerable<CodeInstruction> ItolibEventfulDisconnectTranspiler(
            IEnumerable<CodeInstruction> instructions)
        {
            return ComplexOwnerTranspilers.ReplaceIgnoredSpawnCalls(
                instructions,
                nameof(ComplexOwnerGuardRuntime.ItolibEventfulSpawn),
                expectedCount: 1,
                label: "itolib EventfulApparatus.HandleDisconnect");
        }

        public static IEnumerable<CodeInstruction> ItolibTwinDisconnectTranspiler(
            IEnumerable<CodeInstruction> instructions)
        {
            return ComplexOwnerTranspilers.ReplaceIgnoredSpawnCalls(
                instructions,
                nameof(ComplexOwnerGuardRuntime.ItolibTwinSpawn),
                expectedCount: 1,
                label: "itolib TwinApparatus.HandleDisconnect");
        }

        public static IEnumerable<CodeInstruction> CodeRebirthEnemyLevelSpawnerTranspiler(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            return ComplexOwnerTranspilers.InsertCodeRebirthSpawnerDecisionGuard(instructions, generator);
        }

        public static IEnumerable<CodeInstruction> CodeRebirthFakeSnailTranspiler(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            return ComplexOwnerTranspilers.BypassCodeRebirthFakeSnailConversion(instructions, generator);
        }

        public static IEnumerable<CodeInstruction> CodeRebirthXuiTranspiler(
            IEnumerable<CodeInstruction> instructions)
        {
            return ComplexOwnerTranspilers.ReplaceIgnoredSpawnCalls(
                instructions,
                nameof(ComplexOwnerGuardRuntime.CodeRebirthXuiSpawn),
                expectedCount: 2,
                label: "CodeRebirth Xui.OnNetworkDespawn");
        }

        private static bool GuardDirectSpawnHelper(
            SpawnableEnemyWithRarity request,
            ref NetworkObjectReference result,
            MethodBase original,
            string owner)
        {
            EnemyType enemyType = request?.enemyType;
            if (ComplexOwnerGuardRuntime.AllowExplicitEnemy(enemyType, owner))
                return true;

            result = default(NetworkObjectReference);
            ComplexOwnerGuardRuntime.LogBlocked(
                owner,
                $"direct helper denied enemy='{ComplexOwnerGuardRuntime.DescribeEnemy(enemyType)}'; returning default NetworkObjectReference per reviewed ignored-return contract");
            return false;
        }

        private static IEnumerator EmptyIterator()
        {
            yield break;
        }
    }
}
