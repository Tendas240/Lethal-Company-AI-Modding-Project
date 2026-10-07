using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;
using UnityEngine;

namespace S142AKBMAFR1I1
{
    internal static class Probes
    {
        internal static IEnumerable<CodeInstruction> Selector(IEnumerable<CodeInstruction> instructions, ILGenerator generator, MethodBase original)
        {
            Contracts.Require(original == Contracts.Selector, "Unexpected selector target");
            List<CodeInstruction> code = IlGuard.Check(instructions, original);
            var sites = code.Select((x, i) => new { x, i }).Where(x => x.x.opcode == OpCodes.Callvirt && Equals(x.x.operand, Contracts.ApplyOperand)).ToArray();
            Contracts.Require(sites.Length == 1, "Expected exactly one non-default Apply callsite");
            int at = sites[0].i;
            Contracts.Require(at >= 3 && at + 1 < code.Count && code[at - 1].opcode == OpCodes.Ldc_I4_0 && code[at - 2].opcode == OpCodes.Ldarg_1
                && code[at - 3].opcode == OpCodes.Ldloc_S && IlGuard.Slot(code[at - 3].operand) == 11, "Selected current/self/immediate producer drift");
            MethodInfo coroutine = typeof(MonoBehaviour).GetMethod("StartCoroutine", new[] { typeof(System.Collections.IEnumerator) });
            Contracts.Require(code[at + 1].opcode == OpCodes.Callvirt && Equals(code[at + 1].operand, coroutine), "Apply/StartCoroutine adjacency drift");
            EmptyBoundary(code[at]);
            LocalBuilder immediate = generator.DeclareLocal(typeof(bool));
            LocalBuilder enemy = generator.DeclareLocal(typeof(EnemyAI));
            LocalBuilder selected = generator.DeclareLocal(Contracts.ApplyOperand.DeclaringType);
            var insert = new[] {
                new CodeInstruction(OpCodes.Stloc, immediate),
                new CodeInstruction(OpCodes.Stloc, enemy),
                new CodeInstruction(OpCodes.Stloc, selected),
                new CodeInstruction(OpCodes.Ldloc, selected),
                new CodeInstruction(OpCodes.Ldloc, enemy),
                new CodeInstruction(OpCodes.Call, Callback(nameof(Observers.Selected))),
                new CodeInstruction(OpCodes.Ldloc, selected),
                new CodeInstruction(OpCodes.Ldloc, enemy),
                new CodeInstruction(OpCodes.Ldloc, immediate)
            };
            code.InsertRange(at, insert);
            return code;
        }

        internal static IEnumerable<CodeInstruction> JanitorWrite(IEnumerable<CodeInstruction> instructions, ILGenerator generator, MethodBase original)
        {
            Contracts.Require(Contracts.Writes.Contains(original as MethodInfo), "Unexpected Janitor target");
            List<CodeInstruction> code = IlGuard.Check(instructions, original);
            MethodInfo write = typeof(SkinnedMeshRenderer).GetMethod("SetBlendShapeWeight", Contracts.Declared, null, new[] { typeof(int), typeof(float) }, null);
            var sites = code.Select((x, i) => new { x, i }).Where(x => x.x.opcode == OpCodes.Callvirt && Equals(x.x.operand, write)).ToArray();
            Contracts.Require(sites.Length == 1, "Expected exactly one Janitor direct write");
            int at = sites[0].i;
            bool rpc = original.Name == "SetBlendShapeWeightClientRpc";
            int zero = at - (rpc ? 3 : 2);
            Contracts.Require(zero >= 4 && code[zero].opcode == OpCodes.Ldc_I4_0 && code[zero - 1].opcode == OpCodes.Ldelem_Ref
                && code[zero - 2].opcode == OpCodes.Ldc_I4_0 && code[zero - 3].opcode == OpCodes.Ldfld && code[zero - 4].opcode == OpCodes.Ldarg_0
                && Equals(code[zero - 3].operand, typeof(EnemyAI).GetField("skinnedMeshRenderers", Contracts.Declared)), "Janitor renderer/index producer drift");
            if (rpc) Contracts.Require(code[at - 2].opcode == OpCodes.Ldarg_1 && code[at - 1].opcode == OpCodes.Conv_R4, "RPC weight producer drift");
            else Contracts.Require(code[at - 1].opcode == OpCodes.Ldc_R4 && Equals(code[at - 1].operand, original.Name == "SwitchToChaseState" ? 100f : 0f), "Reset/chase weight drift");
            EmptyBoundary(code[at]);
            LocalBuilder weight = generator.DeclareLocal(typeof(float));
            LocalBuilder index = generator.DeclareLocal(typeof(int));
            LocalBuilder renderer = generator.DeclareLocal(typeof(SkinnedMeshRenderer));
            var insert = new[] {
                new CodeInstruction(OpCodes.Stloc, weight),
                new CodeInstruction(OpCodes.Stloc, index),
                new CodeInstruction(OpCodes.Stloc, renderer),
                new CodeInstruction(OpCodes.Ldarg_0),
                new CodeInstruction(OpCodes.Ldloc, renderer),
                new CodeInstruction(OpCodes.Ldloc, index),
                new CodeInstruction(OpCodes.Ldloc, weight),
                new CodeInstruction(OpCodes.Ldstr, original.Name),
                new CodeInstruction(OpCodes.Call, Callback(nameof(Observers.BeforeWrite))),
                new CodeInstruction(OpCodes.Ldloc, renderer),
                new CodeInstruction(OpCodes.Ldloc, index),
                new CodeInstruction(OpCodes.Ldloc, weight)
            };
            code.InsertRange(at, insert);
            return code;
        }

        private static void EmptyBoundary(CodeInstruction call)
        { Contracts.Require(call.labels.Count == 0 && call.blocks.Count == 0, "Callsite label/exception boundary is ambiguous"); }

        private static MethodInfo Callback(string name)
        { return typeof(Observers).GetMethod(name, Contracts.Declared); }
    }
}
