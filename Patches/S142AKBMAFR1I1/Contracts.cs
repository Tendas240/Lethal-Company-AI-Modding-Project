using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using System.Security.Cryptography;
using BepInEx;
using BepInEx.Bootstrap;
using HarmonyLib;
using UnityEngine;

namespace S142AKBMAFR1I1
{
    internal sealed class MethodContract
    {
        internal string Owner, Name, Access, Return, IlHash;
        internal bool Static;
        internal string[] Parameters;
        internal string[] Locals;
        internal int MaxStack;
        internal bool InitLocals;
        internal int[][] ExceptionRegions;
        internal MethodInfo Method;
        internal MethodContract(string owner, string name, string access, bool isStatic, string returns, string[] parameters, string ilHash, string[] locals, int maxStack, bool initLocals, int[][] regions)
        { Owner = owner; Name = name; Access = access; Static = isStatic; Return = returns; Parameters = parameters; IlHash = ilHash; Locals = locals; MaxStack = maxStack; InitLocals = initLocals; ExceptionRegions = regions; }
    }

    internal static class Contracts
    {
        internal const BindingFlags Declared = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
        internal static Type Janitor, SpringMan, Definition, Hierarchy, MeshAction;
        internal static MethodInfo Selector, MeshTransfer, Materials, ApplyOperand;
        internal static readonly List<MethodInfo> Writes = new List<MethodInfo>();
        internal static FieldInfo DefaultField;
        internal static PropertyInfo Replacements, SkinName, HierarchyPath, ReplacementRenderer;
        private static Assembly code, dusk, hooks;

        internal static void Require(bool ok, string message)
        { if (!ok) throw new InvalidOperationException(message); }

        private static string Hash(byte[] bytes)
        { using (var sha = SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(bytes)).Replace("-", "").ToLowerInvariant(); }

        private static Assembly Dependency(string guid, string version, string name, string sha)
        {
            Require(Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info) && info.Instance != null && info.Metadata.Version.ToString() == version,
                "Required plugin/version mismatch: " + guid);
            Assembly result = info.Instance.GetType().Assembly;
            Require(!result.IsDynamic && result.GetName().Name == name && result.ManifestModule != null,
                "Dependency assembly identity mismatch: " + name);
            Require(!string.IsNullOrEmpty(result.Location) && File.Exists(result.Location), "Dependency provenance unavailable: " + name);
            Require(Hash(File.ReadAllBytes(result.Location)) == sha, "Dependency SHA-256 mismatch: " + name);
            return result;
        }

        internal static void Resolve()
        {
            GameAssemblyProvenance.Validate(Paths.ManagedPath, "5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731");
            Require(typeof(EnemyAI).FullName == "EnemyAI" && typeof(EnemyAI).Assembly.GetName().Name == "Assembly-CSharp" && !typeof(EnemyAI).Assembly.IsDynamic,
                "Loaded EnemyAI identity mismatch");
            code = Dependency("CodeRebirth", "1.6.9", "CodeRebirth", "a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36");
            dusk = Dependency("com.github.teamxiaolan.dawnlib.dusk", "0.9.25", "com.github.teamxiaolan.dawnlib.dusk", "3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03");
            var matches = AppDomain.CurrentDomain.GetAssemblies().Where(a => a.GetName().Name == "MMHOOK_Assembly-CSharp" && !a.IsDynamic).ToArray();
            Require(matches.Length == 1, "Exact MMHOOK assembly must be unique");
            hooks = matches[0];
            Janitor = code.GetType("CodeRebirth.src.Content.Enemies.Janitor", true);
            Require(Janitor.BaseType == code.GetType("CodeRebirth.src.Content.Enemies.CodeRebirthEnemyAI", true) && Janitor.BaseType.BaseType == typeof(EnemyAI), "Janitor inheritance mismatch");
            SpringMan = typeof(EnemyAI).Assembly.GetType("SpringManAI", true);
            Require(SpringMan.IsSubclassOf(typeof(EnemyAI)), "SpringMan exact type mismatch");
            Definition = dusk.GetType("Dusk.DuskEntityReplacementDefinition", true);
            Hierarchy = dusk.GetType("Dusk.Hierarchy", true);
            MeshAction = dusk.GetType("Dusk.SkinnedMeshReplacement", true);
            foreach (MethodContract spec in ContractData.Methods)
            {
                Type owner = spec.Owner.StartsWith("CodeRebirth.", StringComparison.Ordinal) ? code.GetType(spec.Owner, true) : dusk.GetType(spec.Owner, true);
                Type[] args = spec.Parameters.Select(ResolveParameter).ToArray();
                MethodInfo m = owner.GetMethod(spec.Name, Declared, null, args, null);
                Require(m != null && m.DeclaringType == owner && m.IsStatic == spec.Static && !m.ContainsGenericParameters && TypeName(m.ReturnType) == spec.Return,
                    "Exact declared signature mismatch: " + spec.Owner + "." + spec.Name);
                Require((spec.Access == "public" && m.IsPublic) || (spec.Access == "private" && m.IsPrivate) || (spec.Access == "assembly" && m.IsAssembly), "Visibility mismatch: " + spec.Name);
                Require(m.GetMethodBody() != null && Hash(m.GetMethodBody().GetILAsByteArray()) == spec.IlHash, "Exact IL body mismatch: " + spec.Name);
                MethodBody body = m.GetMethodBody();
                Require(body.MaxStackSize == spec.MaxStack && body.InitLocals == spec.InitLocals && body.LocalVariables.Select(x => TypeName(x.LocalType)).SequenceEqual(spec.Locals)
                    && body.LocalVariables.All(x => !x.IsPinned), "Exact local/stack contract mismatch: " + spec.Name);
                Require(body.ExceptionHandlingClauses.Count == spec.ExceptionRegions.Length, "Exception region count mismatch: " + spec.Name);
                for (int i = 0; i < spec.ExceptionRegions.Length; i++)
                {
                    ExceptionHandlingClause clause = body.ExceptionHandlingClauses[i]; int[] region = spec.ExceptionRegions[i];
                    Require(clause.Flags == ExceptionHandlingClauseOptions.Finally && (int)clause.Flags == region[0]
                        && clause.TryOffset == region[1] && clause.TryLength == region[2]
                        && clause.HandlerOffset == region[3] && clause.HandlerLength == region[4], "Exact exception region mismatch: " + spec.Name);
                }
                spec.Method = m;
            }
            Selector = Find("Dusk.Internal.EntityReplacementRegistrationPatch", "ReplaceEnemyEntity");
            MeshTransfer = Find("Dusk.SkinnedMeshReplacement", "ReplaceSkinnedMeshRenderer");
            Materials = Find("Dusk.MaterialsReplacement", "CopyOrResizeMaterials");
            foreach (string name in new[] { "SetBlendShapeWeightClientRpc", "KillEnemy", "KeepPlayerAttachedDuringZoom", "SwitchToChaseState" })
                Writes.Add(Find(Janitor.FullName, name));
            Require(Writes[1].IsVirtual && Writes[1].GetParameters()[0].IsOptional && Equals(Writes[1].GetParameters()[0].DefaultValue, false), "KillEnemy bool/default contract mismatch");
            DefaultField = Definition.GetField("IsDefault", Declared);
            Require(DefaultField != null && DefaultField.DeclaringType == Definition && !DefaultField.IsStatic && DefaultField.IsAssembly && DefaultField.FieldType == typeof(bool), "IsDefault field mismatch");
            Replacements = Property(Definition, "Replacements", typeof(List<>).MakeGenericType(Hierarchy));
            SkinName = Property(Definition, "SkinName", typeof(string));
            HierarchyPath = Property(Hierarchy, "HierarchyPath", typeof(string));
            ReplacementRenderer = Property(MeshAction, "ReplacementRenderer", typeof(SkinnedMeshRenderer));
            Type baseApply = dusk.GetType("Dusk.DuskEntityReplacementDefinition`1", true).MakeGenericType(typeof(EnemyAI));
            ApplyOperand = baseApply.GetMethod("Apply", Declared, null, new[] { typeof(EnemyAI), typeof(bool) }, null);
            Require(ApplyOperand != null && ApplyOperand.DeclaringType == baseApply && !ApplyOperand.IsStatic && ApplyOperand.ReturnType == typeof(IEnumerator), "Exact generic Apply operand mismatch");
            foreach (MethodInfo target in PatchTargets())
            {
                Patches prior = Harmony.GetPatchInfo(target);
                Require(prior == null || prior.Transpilers.Count == 0, "Foreign transpiler present; refuse ambiguous IL: " + target.Name);
            }
        }

        private static Type ResolveParameter(string name)
        {
            switch (name)
            {
                case "System.Boolean": return typeof(bool);
                case "System.Int32": return typeof(int);
                case "EnemyAI": return typeof(EnemyAI);
                case "GameNetcodeStuff.PlayerControllerB": return typeof(GameNetcodeStuff.PlayerControllerB);
                case "On.EnemyAI+orig_Start": return hooks.GetType(name, true);
                case "UnityEngine.SkinnedMeshRenderer": return typeof(SkinnedMeshRenderer);
                case "UnityEngine.Renderer": return typeof(Renderer);
                case "UnityEngine.Material[]": return typeof(Material[]);
                case "UnityEngine.Transform": return typeof(Transform);
                default: throw new InvalidOperationException("Unlisted exact parameter contract: " + name);
            }
        }

        internal static string TypeName(Type t)
        {
            if (t.IsArray) return TypeName(t.GetElementType()) + "[]";
            if (t.IsGenericType) return t.GetGenericTypeDefinition().FullName + "<" + string.Join(",", t.GetGenericArguments().Select(TypeName)) + ">";
            return t.FullName;
        }

        private static MethodInfo Find(string owner, string name)
        { return ContractData.Methods.Single(x => x.Owner == owner && x.Name == name).Method; }

        private static PropertyInfo Property(Type owner, string name, Type type)
        {
            PropertyInfo p = owner.GetProperty(name, Declared);
            Require(p != null && p.DeclaringType == owner && p.PropertyType == type && p.GetIndexParameters().Length == 0 && p.GetGetMethod(true) == Find(owner.FullName, "get_" + name), "Exact read-only property mismatch: " + name);
            return p;
        }

        internal static IEnumerable<MethodInfo> PatchTargets()
        { return Writes.Concat(new[] { MeshTransfer, Materials, Selector }); }
    }
}
