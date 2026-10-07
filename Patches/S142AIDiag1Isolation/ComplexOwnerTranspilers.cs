using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;
using Unity.Netcode;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    internal static class ComplexOwnerTranspilers
    {
        internal static IEnumerable<CodeInstruction> InsertJllDecisionGuard(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            List<CodeInstruction> codes = instructions.ToList();
            MethodInfo objectInequality = ExactUnityObjectOperator("op_Inequality");
            MethodInfo nativeSpawn = ExactNativeSpawnMethod();
            MethodInfo gate = ExactRuntimeMethod(nameof(ComplexOwnerGuardRuntime.IsJllEnemyAllowed));

            int spawnCount = CountCalls(codes, nativeSpawn, requireCallvirt: true);
            List<int> decisionRegions = FindLocalNullComparisonRegions(codes, localIndex: 1, objectInequality);
            if (spawnCount != 1 || decisionRegions.Count != 1)
            {
                throw Fail(
                    "JLL.Components.EnemySpawner.SpawnEnemy",
                    $"expected spawnCalls=1 and resolved-enemy decisionRegions=1; got spawnCalls={spawnCount}, decisionRegions={decisionRegions.Count}");
            }

            InsertVoidReturnGuard(codes, decisionRegions[0], localIndex: 1, gate, generator);
            LogMatch("JLL.Components.EnemySpawner.SpawnEnemy", "decisionRegions=1, downstreamSpawnCalls=1");
            return codes;
        }

        internal static IEnumerable<CodeInstruction> InsertCodeRebirthSpawnerDecisionGuard(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            List<CodeInstruction> codes = instructions.ToList();
            MethodInfo objectEquality = ExactUnityObjectOperator("op_Equality");
            MethodInfo nativeSpawn = ExactNativeSpawnMethod();
            MethodInfo gate = ExactRuntimeMethod(nameof(ComplexOwnerGuardRuntime.IsCodeRebirthSpawnerEnemyAllowed));

            int spawnCount = CountCalls(codes, nativeSpawn, requireCallvirt: true);
            List<int> decisionRegions = FindLocalNullComparisonRegions(codes, localIndex: 0, objectEquality);
            if (spawnCount != 1 || decisionRegions.Count != 1)
            {
                throw Fail(
                    "CodeRebirth.src.MiscScripts.EnemyLevelSpawner.SpawnRandomEnemy",
                    $"expected spawnCalls=1 and weighted-enemy decisionRegions=1; got spawnCalls={spawnCount}, decisionRegions={decisionRegions.Count}");
            }

            InsertNullReturnGuard(codes, decisionRegions[0], localIndex: 0, gate, generator);
            LogMatch("CodeRebirth.src.MiscScripts.EnemyLevelSpawner.SpawnRandomEnemy", "decisionRegions=1, downstreamSpawnCalls=1");
            return codes;
        }

        internal static IEnumerable<CodeInstruction> BypassCodeRebirthFakeSnailConversion(
            IEnumerable<CodeInstruction> instructions,
            ILGenerator generator)
        {
            List<CodeInstruction> codes = instructions.ToList();
            MethodInfo nativeSpawn = ExactNativeSpawnMethod();
            MethodInfo log = ExactRuntimeMethod(nameof(ComplexOwnerGuardRuntime.LogCodeRebirthFakeSnailBlocked));

            int spawnCount = CountCalls(codes, nativeSpawn, requireCallvirt: true);
            List<int> anchors = new List<int>();
            for (int i = 0; i + 2 < codes.Count; i++)
            {
                if (codes[i].opcode == OpCodes.Ldarg_0 &&
                    codes[i + 1].opcode == OpCodes.Ldc_I4_1 &&
                    codes[i + 2].opcode == OpCodes.Stfld &&
                    codes[i + 2].operand is FieldInfo field &&
                    field.Name == "destroyed" &&
                    field.DeclaringType?.FullName == "CodeRebirth.src.Content.Items.FakeSnailCat")
                {
                    anchors.Add(i);
                }
            }

            int finalRet = FindFinalRet(codes);
            if (spawnCount != 1 || anchors.Count != 1 || finalRet < 0)
            {
                throw Fail(
                    "CodeRebirth.src.Content.Items.FakeSnailCat.Update",
                    $"expected spawnCalls=1, destroyed-write anchors=1 and finalRet; got spawnCalls={spawnCount}, anchors={anchors.Count}, finalRet={finalRet}");
            }

            int anchorIndex = anchors[0];
            CodeInstruction anchor = codes[anchorIndex];
            RequireNoExceptionBoundary(anchor, "CodeRebirth FakeSnail anchor");
            RequireNoExceptionBoundary(codes[finalRet], "CodeRebirth FakeSnail final ret");

            Label exit = generator.DefineLabel();
            codes[finalRet].labels.Add(exit);

            CodeInstruction logCall = new CodeInstruction(OpCodes.Call, log);
            MoveLabels(anchor, logCall);
            codes.InsertRange(anchorIndex, new[]
            {
                logCall,
                new CodeInstruction(OpCodes.Br, exit)
            });

            LogMatch(
                "CodeRebirth.src.Content.Items.FakeSnailCat.Update",
                "destroyed-write anchors=1, downstreamSpawnCalls=1; conversion branch exits before destroyed=true");
            return codes;
        }

        internal static IEnumerable<CodeInstruction> ReplaceIgnoredSpawnCalls(
            IEnumerable<CodeInstruction> instructions,
            string wrapperName,
            int expectedCount,
            string label)
        {
            List<CodeInstruction> codes = instructions.ToList();
            MethodInfo nativeSpawn = ExactNativeSpawnMethod();
            MethodInfo wrapper = ExactRuntimeMethod(wrapperName);
            ValidateSpawnWrapper(wrapper, label);

            int count = 0;
            for (int i = 0; i < codes.Count; i++)
            {
                CodeInstruction code = codes[i];
                if (code.opcode != OpCodes.Callvirt || !SameMethod(code.operand as MethodInfo, nativeSpawn))
                    continue;

                if (i + 1 >= codes.Count || codes[i + 1].opcode != OpCodes.Pop)
                {
                    throw Fail(label, "matched SpawnEnemyGameObject return is not immediately ignored with pop");
                }

                code.opcode = OpCodes.Call;
                code.operand = wrapper;
                count++;
            }

            if (count != expectedCount)
                throw Fail(label, $"expected exactly {expectedCount} ignored-result SpawnEnemyGameObject replacement(s); got {count}");

            LogMatch(label, $"ignored-result SpawnEnemyGameObject replacements={count}");
            return codes;
        }

        private static void InsertVoidReturnGuard(
            List<CodeInstruction> codes,
            int anchorIndex,
            int localIndex,
            MethodInfo gate,
            ILGenerator generator)
        {
            CodeInstruction anchor = codes[anchorIndex];
            RequireNoExceptionBoundary(anchor, "void-return guard anchor");
            Label allowed = generator.DefineLabel();
            anchor.labels.Add(allowed);

            CodeInstruction load = LoadLocal(localIndex);
            MoveLabelsExcept(anchor, load, allowed);
            codes.InsertRange(anchorIndex, new[]
            {
                load,
                new CodeInstruction(OpCodes.Call, gate),
                new CodeInstruction(OpCodes.Brtrue, allowed),
                new CodeInstruction(OpCodes.Ret)
            });
        }

        private static void InsertNullReturnGuard(
            List<CodeInstruction> codes,
            int anchorIndex,
            int localIndex,
            MethodInfo gate,
            ILGenerator generator)
        {
            CodeInstruction anchor = codes[anchorIndex];
            RequireNoExceptionBoundary(anchor, "null-return guard anchor");
            Label allowed = generator.DefineLabel();
            anchor.labels.Add(allowed);

            CodeInstruction load = LoadLocal(localIndex);
            MoveLabelsExcept(anchor, load, allowed);
            codes.InsertRange(anchorIndex, new[]
            {
                load,
                new CodeInstruction(OpCodes.Call, gate),
                new CodeInstruction(OpCodes.Brtrue, allowed),
                new CodeInstruction(OpCodes.Ldnull),
                new CodeInstruction(OpCodes.Ret)
            });
        }

        private static List<int> FindLocalNullComparisonRegions(
            List<CodeInstruction> codes,
            int localIndex,
            MethodInfo comparison)
        {
            List<int> matches = new List<int>();
            for (int i = 0; i + 2 < codes.Count; i++)
            {
                if (IsLoadLocal(codes[i], localIndex) &&
                    codes[i + 1].opcode == OpCodes.Ldnull &&
                    (codes[i + 2].opcode == OpCodes.Call || codes[i + 2].opcode == OpCodes.Callvirt) &&
                    SameMethod(codes[i + 2].operand as MethodInfo, comparison))
                {
                    matches.Add(i);
                }
            }
            return matches;
        }

        private static CodeInstruction LoadLocal(int index)
        {
            switch (index)
            {
                case 0: return new CodeInstruction(OpCodes.Ldloc_0);
                case 1: return new CodeInstruction(OpCodes.Ldloc_1);
                case 2: return new CodeInstruction(OpCodes.Ldloc_2);
                case 3: return new CodeInstruction(OpCodes.Ldloc_3);
                default: return new CodeInstruction(OpCodes.Ldloc, index);
            }
        }

        private static bool IsLoadLocal(CodeInstruction code, int expectedIndex)
        {
            if (expectedIndex == 0 && code.opcode == OpCodes.Ldloc_0) return true;
            if (expectedIndex == 1 && code.opcode == OpCodes.Ldloc_1) return true;
            if (expectedIndex == 2 && code.opcode == OpCodes.Ldloc_2) return true;
            if (expectedIndex == 3 && code.opcode == OpCodes.Ldloc_3) return true;

            if (code.opcode != OpCodes.Ldloc && code.opcode != OpCodes.Ldloc_S)
                return false;

            if (code.operand is LocalBuilder builder)
                return builder.LocalIndex == expectedIndex;
            if (code.operand is int intIndex)
                return intIndex == expectedIndex;
            if (code.operand is byte byteIndex)
                return byteIndex == expectedIndex;
            if (code.operand is sbyte sbyteIndex)
                return sbyteIndex == expectedIndex;
            return false;
        }

        private static int FindFinalRet(List<CodeInstruction> codes)
        {
            for (int i = codes.Count - 1; i >= 0; i--)
            {
                if (codes[i].opcode == OpCodes.Nop)
                    continue;
                return codes[i].opcode == OpCodes.Ret ? i : -1;
            }
            return -1;
        }

        private static int CountCalls(List<CodeInstruction> codes, MethodInfo method, bool requireCallvirt)
        {
            int count = 0;
            foreach (CodeInstruction code in codes)
            {
                if (requireCallvirt && code.opcode != OpCodes.Callvirt)
                    continue;
                if (!requireCallvirt && code.opcode != OpCodes.Call && code.opcode != OpCodes.Callvirt)
                    continue;
                if (SameMethod(code.operand as MethodInfo, method))
                    count++;
            }
            return count;
        }

        private static MethodInfo ExactNativeSpawnMethod()
        {
            MethodInfo method = typeof(RoundManager).GetMethod(
                "SpawnEnemyGameObject",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                new[] { typeof(Vector3), typeof(float), typeof(int), typeof(EnemyType) },
                null);
            if (method == null || method.ReturnType != typeof(NetworkObjectReference) || method.GetMethodBody() == null)
                throw Fail("RoundManager.SpawnEnemyGameObject", "exact V81 method signature/body did not validate for transpiler matching");
            return method;
        }

        private static MethodInfo ExactUnityObjectOperator(string name)
        {
            MethodInfo method = typeof(UnityEngine.Object).GetMethod(
                name,
                BindingFlags.Static | BindingFlags.Public | BindingFlags.DeclaredOnly,
                null,
                new[] { typeof(UnityEngine.Object), typeof(UnityEngine.Object) },
                null);
            if (method == null || method.ReturnType != typeof(bool))
                throw Fail("UnityEngine.Object." + name, "exact operator signature did not validate");
            return method;
        }

        private static MethodInfo ExactRuntimeMethod(string name)
        {
            MethodInfo method = typeof(ComplexOwnerGuardRuntime).GetMethod(
                name,
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);
            if (method == null || method.GetMethodBody() == null)
                throw Fail("ComplexOwnerGuardRuntime." + name, "helper method did not validate");
            return method;
        }

        private static void ValidateSpawnWrapper(MethodInfo wrapper, string label)
        {
            Type[] expected =
            {
                typeof(RoundManager), typeof(Vector3), typeof(float), typeof(int), typeof(EnemyType)
            };
            ParameterInfo[] actual = wrapper.GetParameters();
            if (!wrapper.IsStatic || wrapper.ReturnType != typeof(NetworkObjectReference) || actual.Length != expected.Length)
                throw Fail(label, "spawn wrapper does not have exact static replacement signature");
            for (int i = 0; i < expected.Length; i++)
            {
                if (actual[i].ParameterType != expected[i])
                    throw Fail(label, $"spawn wrapper parameter {i} mismatch: {actual[i].ParameterType.FullName} != {expected[i].FullName}");
            }
        }

        private static bool SameMethod(MethodInfo left, MethodInfo right)
        {
            if (left == null || right == null)
                return false;
            return left.Module == right.Module && left.MetadataToken == right.MetadataToken;
        }

        private static void RequireNoExceptionBoundary(CodeInstruction instruction, string label)
        {
            if (instruction.blocks != null && instruction.blocks.Count != 0)
                throw Fail(label, "anchor carries an exception-block boundary; exact insertion contract changed");
        }

        private static void MoveLabels(CodeInstruction from, CodeInstruction to)
        {
            if (from.labels == null || from.labels.Count == 0)
                return;
            to.labels.AddRange(from.labels);
            from.labels.Clear();
        }

        private static void MoveLabelsExcept(CodeInstruction from, CodeInstruction to, Label keep)
        {
            if (from.labels == null || from.labels.Count == 0)
                return;

            List<Label> move = from.labels.Where(label => !label.Equals(keep)).ToList();
            foreach (Label label in move)
            {
                to.labels.Add(label);
                from.labels.Remove(label);
            }
        }

        private static InvalidOperationException Fail(string label, string detail)
        {
            string message = $"[DIAG1_TRANSPILER_INVALID] {label}: {detail}. No fallback patch is permitted.";
            Plugin.Log.LogError(message);
            DiagnosticIsolation.MarkInvalid(message);
            return new InvalidOperationException(message);
        }

        private static void LogMatch(string label, string detail)
        {
            Plugin.Log.LogInfo($"[DIAG1_TRANSPILER_MATCH] {label}: {detail}.");
        }
    }
}
