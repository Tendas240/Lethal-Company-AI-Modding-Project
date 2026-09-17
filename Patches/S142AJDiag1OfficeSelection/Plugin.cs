using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using BepInEx;
using BepInEx.Bootstrap;
using HarmonyLib;
using UnityEngine;

namespace S142AJDiag1OfficeSelection
{
    [BepInPlugin(Guid, "S1.42AJ-DIAG1 LC Office Selection", "1.0.0")]
    [BepInDependency(LllGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(NormalizerGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string Guid = "tendas.lethalcompany.s142ajdiag1officeselection";
        internal const string LllGuid = "imabatby.lethallevelloader";
        internal const string NormalizerGuid = "tendas.lethalcompany.s142abinteriorweightnormalization";
        private const string LllSha = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c";
        private const string NormalizerSha = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06";
        private const BindingFlags Static = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        private const BindingFlags Instance = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        private static Plugin self;
        private static MethodInfo target, selectionCaller, simulationCaller;
        private static FieldInfo flowField, rarityField;
        private static PropertyInfo nameProperty, assetProperty, moonProperty;
        private static Type resultType;
        private static bool runtimeRefused;
        private Harmony harmony;

        private void Awake()
        {
            self = this;
            try
            {
                Assembly lll = Dependency(LllGuid, "1.7.12", LllSha);
                Dependency(NormalizerGuid, "1.0.0", NormalizerSha);
                Type manager = lll.GetType("LethalLevelLoader.DungeonManager", true);
                Type level = lll.GetType("LethalLevelLoader.ExtendedLevel", true);
                Type weighted = lll.GetType("LethalLevelLoader.ExtendedDungeonFlowWithRarity", true);
                Type flow = lll.GetType("LethalLevelLoader.ExtendedDungeonFlow", true);
                resultType = typeof(List<>).MakeGenericType(weighted);
                target = manager.GetMethod("GetValidExtendedDungeonFlows", Static, null, new[] {level, typeof(bool)}, null);
                Require(target != null && target.DeclaringType == manager && target.ReturnType == resultType
                    && !target.ContainsGenericParameters && target.GetMethodBody() != null, "Exact static selection target/body mismatch");
                flowField = weighted.GetField("extendedDungeonFlow", Instance);
                rarityField = weighted.GetField("rarity", Instance);
                Require(flowField != null && flowField.FieldType == flow && rarityField != null
                    && rarityField.FieldType == typeof(int), "Weighted entry fields mismatch");
                nameProperty = Property(flow, "DungeonName", typeof(string));
                moonProperty = Property(level, "NumberlessPlanetName", typeof(string));
                assetProperty = flow.GetProperty("DungeonFlow", Instance);
                Require(assetProperty != null && assetProperty.PropertyType.Name == "DungeonFlow"
                    && typeof(UnityEngine.Object).IsAssignableFrom(assetProperty.PropertyType)
                    && assetProperty.GetGetMethod(true) != null && assetProperty.GetIndexParameters().Length == 0,
                    "Exact DungeonFlow readable property/type mismatch");
                Type network = lll.GetType("LethalLevelLoader.LethalLevelLoaderNetworkManager", true);
                selectionCaller = network.GetMethod("GetRandomExtendedDungeonFlowServerRpc", Instance, null, Type.EmptyTypes, null);
                Require(selectionCaller != null && selectionCaller.ReturnType == typeof(void)
                    && selectionCaller.GetMethodBody() != null, "Exact selection caller mismatch");
                Type terminal = lll.GetType("LethalLevelLoader.TerminalManager", true);
                simulationCaller = terminal.GetMethod("GetSimulationResultsText", Static, null, new[] {level}, null);
                Require(simulationCaller != null && simulationCaller.ReturnType == typeof(string)
                    && simulationCaller.GetMethodBody() != null, "Exact terminal caller mismatch");
                var prior = Harmony.GetPatchInfo(target);
                Require(prior != null && prior.Postfixes.Count(p => p.owner == NormalizerGuid) == 1,
                    "Accepted normalizer postfix not uniquely installed");
                var method = typeof(Plugin).GetMethod(nameof(Postfix), Static);
                harmony = new Harmony(Guid);
                harmony.Patch(target, postfix: new HarmonyMethod(method) {
                    after = new[] {NormalizerGuid}, priority = Priority.Last
                });
                var installed = Harmony.GetPatchInfo(target);
                Require(installed != null && installed.Postfixes.Count(p => p.owner == Guid) == 1
                    && installed.Postfixes.Single(p => p.owner == Guid).after.Contains(NormalizerGuid),
                    "Diagnostic postfix ownership/order declaration mismatch");
                Logger.LogInfo("[AJDIAG1] ARMED exact LLL/postfix/caller/asset contracts; Offense selection only; after accepted normalization; DIAGNOSTIC ONLY, NEVER ACCEPT.");
                Logger.LogInfo("[AJDIAG1] Target postfix owners: " + string.Join(", ", installed.Postfixes.Select(p => p.owner)));
            }
            catch (Exception ex)
            {
                harmony?.UnpatchSelf();
                Logger.LogError("[AJDIAG1] REFUSED TO ARM; normal behavior preserved: " + ex);
            }
        }

        private static Assembly Dependency(string guid, string version, string hash)
        {
            Require(Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info)
                && info.Metadata.Version.ToString() == version && info.Instance != null, "Dependency mismatch: " + guid);
            Assembly assembly = info.Instance.GetType().Assembly;
            using (var sha = SHA256.Create())
            using (var stream = File.OpenRead(assembly.Location))
                Require(BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "").ToLowerInvariant() == hash,
                    "Dependency DLL hash mismatch: " + guid);
            return assembly;
        }

        private static PropertyInfo Property(Type owner, string name, Type type)
        {
            var p = owner.GetProperty(name, Instance);
            Require(p != null && p.PropertyType == type && p.GetGetMethod(true) != null
                && p.GetIndexParameters().Length == 0, "Property mismatch: " + owner.FullName + "." + name);
            return p;
        }

        private static void Require(bool condition, string message)
        {
            if (!condition) throw new InvalidOperationException(message);
        }

        // Only one Harmony interception. No RPC, RNG, config or registration patch.
        private static void Postfix(object __result, object __0, bool __1)
        {
            if (!__1 || runtimeRefused) return;
            try
            {
                string moon = (string)moonProperty.GetValue(__0);
                if (moon != "Offense") return;
                var frames = new StackTrace(false).GetFrames();
                Require(frames != null, "Cannot identify caller");
                if (frames.Any(f => f.GetMethod() == simulationCaller)) return;
                Require(frames.Any(f => f.GetMethod() == selectionCaller),
                    "Unrecognized selection caller; no guessed stack/name fallback");
                Require(__result != null && __result.GetType() == resultType, "Result list type mismatch");
                var pool = (IList)__result;
                int index = SelectionPolicy.FindOffice(pool, __1, moon, true,
                    entry => (string)nameProperty.GetValue(flowField.GetValue(entry)),
                    entry => {
                        var asset = assetProperty.GetValue(flowField.GetValue(entry)) as UnityEngine.Object;
                        return asset == null ? null : asset.name;
                    },
                    entry => (int)rarityField.GetValue(entry));
                Require(index >= 0, "Selection policy did not return exact viable LC Office");
                object office = pool[index];
                int count = pool.Count;
                // All fallible validation precedes mutation. This exact concrete List owns its
                // freshly-created wrappers. Clear retains capacity; re-add reuses the same entry.
                pool.Clear();
                pool.Add(office);
                self.Logger.LogInfo("[AJDIAG1] SELECTED Offense LC Office / OfficeDungeonFlow; normalized rarity=100; pool="
                    + count + "->1; same viable entry; normalizer -> diagnostic singleton; DIAGNOSTIC ONLY.");
            }
            catch (Exception ex)
            {
                runtimeRefused = true; // One error, no repeated exception flood.
                self.Logger.LogError("[AJDIAG1] REFUSED selection; diagnostic invalid, do not accept this run: " + ex);
            }
        }
    }
}
