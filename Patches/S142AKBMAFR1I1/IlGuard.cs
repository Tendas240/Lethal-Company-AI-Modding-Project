using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;

namespace S142AKBMAFR1I1
{
    // Compares the complete incoming Harmony instruction stream with the validated
    // original body, including branch destinations. It does not transform gameplay.
    internal static class IlGuard
    {
        private sealed class Instruction
        { internal int Offset; internal OpCode Code; internal object Operand; }
        private static readonly Dictionary<short, OpCode> Opcodes = typeof(OpCodes).GetFields(BindingFlags.Public | BindingFlags.Static)
            .Where(f => f.FieldType == typeof(OpCode)).Select(f => (OpCode)f.GetValue(null)).ToDictionary(o => o.Value);

        internal static List<CodeInstruction> Check(IEnumerable<CodeInstruction> input, MethodBase method)
        {
            List<CodeInstruction> actual = input.ToList();
            List<Instruction> expected = Read(method);
            Contracts.Require(expected.Count == actual.Count, "Incoming IL count changed: " + method.Name);
            var offsets = expected.Select((x, i) => new { x.Offset, Index = i }).ToDictionary(x => x.Offset, x => x.Index);
            var labels = new Dictionary<Label, int>();
            for (int i = 0; i < actual.Count; i++)
                foreach (Label label in actual[i].labels) labels.Add(label, i);
            for (int i = 0; i < actual.Count; i++)
            {
                Instruction e = expected[i]; CodeInstruction a = actual[i];
                Contracts.Require(a.opcode == NormalizeBranch(e.Code), "Incoming opcode drift: " + method.Name + ":" + i);
                bool equal;
                switch (e.Code.OperandType)
                {
                    case OperandType.InlineBrTarget:
                    case OperandType.ShortInlineBrTarget:
                        equal = a.operand is Label label && labels.TryGetValue(label, out int dest) && offsets.TryGetValue((int)e.Operand, out int want) && dest == want; break;
                    case OperandType.InlineSwitch:
                        equal = a.operand is Label[] branches && branches.Length == ((int[])e.Operand).Length;
                        if (equal)
                        {
                            Label[] bs = (Label[])a.operand; int[] es = (int[])e.Operand;
                            for (int j = 0; j < bs.Length; j++)
                                equal &= labels.TryGetValue(bs[j], out int dst) && offsets.TryGetValue(es[j], out int exp) && dst == exp;
                        }
                        break;
                    case OperandType.InlineVar:
                    case OperandType.ShortInlineVar:
                        equal = Slot(a.operand) == (int)e.Operand; break;
                    case OperandType.ShortInlineI:
                        equal = Convert.ToInt32(a.operand) == Convert.ToInt32(e.Operand); break;
                    default: equal = Equals(a.operand, e.Operand); break;
                }
                Contracts.Require(equal, "Incoming operand/branch drift: " + method.Name + ":" + i);
            }
            return actual;
        }

        // HarmonyX 2.10.2 ILManipulator.NormalizeInstructions widens these exact
        // short branches BEFORE invoking a transpiler. Destinations are still
        // checked against the original body; this is an encoding adapter only.
        private static OpCode NormalizeBranch(OpCode code)
        {
            if (code == OpCodes.Beq_S) return OpCodes.Beq;
            if (code == OpCodes.Bge_S) return OpCodes.Bge;
            if (code == OpCodes.Bge_Un_S) return OpCodes.Bge_Un;
            if (code == OpCodes.Bgt_S) return OpCodes.Bgt;
            if (code == OpCodes.Bgt_Un_S) return OpCodes.Bgt_Un;
            if (code == OpCodes.Ble_S) return OpCodes.Ble;
            if (code == OpCodes.Ble_Un_S) return OpCodes.Ble_Un;
            if (code == OpCodes.Blt_S) return OpCodes.Blt;
            if (code == OpCodes.Blt_Un_S) return OpCodes.Blt_Un;
            if (code == OpCodes.Bne_Un_S) return OpCodes.Bne_Un;
            if (code == OpCodes.Brfalse_S) return OpCodes.Brfalse;
            if (code == OpCodes.Brtrue_S) return OpCodes.Brtrue;
            if (code == OpCodes.Br_S) return OpCodes.Br;
            if (code == OpCodes.Leave_S) return OpCodes.Leave;
            return code;
        }

        internal static int Slot(object operand)
        {
            if (operand is LocalBuilder local) return local.LocalIndex;
            if (operand is LocalVariableInfo variable) return variable.LocalIndex;
            return Convert.ToInt32(operand);
        }

        private static List<Instruction> Read(MethodBase m)
        {
            byte[] bytes = m.GetMethodBody().GetILAsByteArray();
            var result = new List<Instruction>(); int p = 0;
            Type[] typeArgs = m.DeclaringType.IsGenericType ? m.DeclaringType.GetGenericArguments() : null;
            Type[] methodArgs = m.IsGenericMethod ? m.GetGenericArguments() : null;
            while (p < bytes.Length)
            {
                int offset = p; short value = bytes[p++];
                if (value == 0xfe) value = (short)(0xfe00 | bytes[p++]);
                OpCode code = Opcodes[value]; object arg = null;
                switch (code.OperandType)
                {
                    case OperandType.InlineNone: break;
                    case OperandType.ShortInlineI: arg = (sbyte)bytes[p++]; break;
                    case OperandType.InlineI: arg = BitConverter.ToInt32(bytes, p); p += 4; break;
                    case OperandType.InlineI8: arg = BitConverter.ToInt64(bytes, p); p += 8; break;
                    case OperandType.ShortInlineR: arg = BitConverter.ToSingle(bytes, p); p += 4; break;
                    case OperandType.InlineR: arg = BitConverter.ToDouble(bytes, p); p += 8; break;
                    case OperandType.ShortInlineVar: arg = (int)bytes[p++]; break;
                    case OperandType.InlineVar: arg = (int)BitConverter.ToUInt16(bytes, p); p += 2; break;
                    case OperandType.ShortInlineBrTarget: int small = (sbyte)bytes[p++]; arg = p + small; break;
                    case OperandType.InlineBrTarget: int rel = BitConverter.ToInt32(bytes, p); p += 4; arg = p + rel; break;
                    case OperandType.InlineSwitch:
                        int count = BitConverter.ToInt32(bytes, p); p += 4;
                        int end = p + count * 4; int[] targets = new int[count];
                        for (int i = 0; i < count; i++) { targets[i] = end + BitConverter.ToInt32(bytes, p); p += 4; }
                        arg = targets; break;
                    case OperandType.InlineString: arg = m.Module.ResolveString(BitConverter.ToInt32(bytes, p)); p += 4; break;
                    case OperandType.InlineMethod:
                    case OperandType.InlineField:
                    case OperandType.InlineType:
                    case OperandType.InlineTok:
                        arg = m.Module.ResolveMember(BitConverter.ToInt32(bytes, p), typeArgs, methodArgs); p += 4; break;
                    default: throw new InvalidOperationException("Unsupported exact IL operand: " + code.OperandType);
                }
                result.Add(new Instruction { Offset = offset, Code = code, Operand = arg });
            }
            return result;
        }
    }
}
