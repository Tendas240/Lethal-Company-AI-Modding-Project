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

namespace S142AKBMDSFix1Diag1
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(LethalLevelLoaderGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(NormalizerGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "com.tendas240.s142ak.bmdsfix1.diag1";
        internal const string PluginName = "S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector";
        internal const string PluginVersion = "1.0.0";
        internal const string LethalLevelLoaderGuid = "imabatby.lethallevelloader";
        internal const string NormalizerGuid = "tendas.lethalcompany.s142abinteriorweightnormalization";

        private const string ExpectedLethalLevelLoaderVersion = "1.7.12";
        private const string ExpectedLethalLevelLoaderSha256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c";
        private const string ExpectedNormalizerVersion = "1.0.0";
        private const string ExpectedNormalizerSha256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06";

        private const BindingFlags StaticDeclared = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        private const BindingFlags InstanceDeclared = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;

        private static Plugin _self;
        private static Type _levelType;
        private static Type _resultType;
        private static MethodInfo _selectionTarget;
        private static MethodInfo _selectionCaller;
        private static MethodInfo _simulationCaller;
        private static FieldInfo _flowField;
        private static FieldInfo _rarityField;
        private static PropertyInfo _dungeonNameProperty;
        private static PropertyInfo _dungeonAssetProperty;
        private static PropertyInfo _moonNameProperty;
        private static bool _runtimeRefused;

        private Harmony _harmony;

        private void Awake()
        {
            _self = this;
            try
            {
                Assembly lll = RequireDependency(
                    LethalLevelLoaderGuid,
                    ExpectedLethalLevelLoaderVersion,
                    ExpectedLethalLevelLoaderSha256);
                RequireDependency(
                    NormalizerGuid,
                    ExpectedNormalizerVersion,
                    ExpectedNormalizerSha256);
                ResolveSelectionContract(lll);

                Patches prior = Harmony.GetPatchInfo(_selectionTarget);
                Require(prior != null && prior.Postfixes.Count(p => p.owner == NormalizerGuid) == 1,
                    "Accepted S1.42AB normalizer postfix is not uniquely installed on the exact LLL selection target.");

                MethodInfo postfix = typeof(Plugin).GetMethod(nameof(SelectionPostfix), StaticDeclared);
                Require(postfix != null && postfix.IsStatic,
                    "Diagnostic selection postfix method is missing or non-static.");

                _harmony = new Harmony(PluginGuid);
                _harmony.Patch(_selectionTarget, postfix: new HarmonyMethod(postfix)
                {
                    after = new[] { NormalizerGuid },
                    priority = Priority.Last
                });

                Patches installed = Harmony.GetPatchInfo(_selectionTarget);
                Require(installed != null && installed.Postfixes.Count(p => p.owner == PluginGuid) == 1,
                    "Diagnostic selection postfix is not uniquely installed.");
                Patch diagnostic = installed.Postfixes.Single(p => p.owner == PluginGuid);
                Require(diagnostic.after != null && diagnostic.after.Contains(NormalizerGuid),
                    "Diagnostic selection postfix lost its after-normalizer ordering declaration.");
                Require(diagnostic.priority == Priority.Last,
                    "Diagnostic selection postfix lost Priority.Last.");

                Logger.LogInfo("[BMDSFIX1-DIAG1] ARMED exact LLL 1.7.12 + accepted S1.42AB normalizer; exact GetValidExtendedDungeonFlows postfix after normalizer at Priority.Last; Black Mesa / DeepSewersFlow only; DIAGNOSTIC ONLY, NEVER ACCEPT.");
                Logger.LogInfo("[BMDSFIX1-DIAG1] Selection postfix owners: " + string.Join(", ", installed.Postfixes.Select(p => p.owner)));
            }
            catch (Exception ex)
            {
                _harmony?.UnpatchSelf();
                Logger.LogError("[BMDSFIX1-DIAG1] REFUSED TO ARM; normal behavior preserved: " + ex);
            }
        }

        private static void ResolveSelectionContract(Assembly lll)
        {
            Type manager = lll.GetType("LethalLevelLoader.DungeonManager", true);
            _levelType = lll.GetType("LethalLevelLoader.ExtendedLevel", true);
            Type weighted = lll.GetType("LethalLevelLoader.ExtendedDungeonFlowWithRarity", true);
            Type flow = lll.GetType("LethalLevelLoader.ExtendedDungeonFlow", true);
            _resultType = typeof(List<>).MakeGenericType(weighted);

            _selectionTarget = manager.GetMethod(
                "GetValidExtendedDungeonFlows",
                StaticDeclared,
                null,
                new[] { _levelType, typeof(bool) },
                null);
            Require(_selectionTarget != null
                    && _selectionTarget.DeclaringType == manager
                    && _selectionTarget.IsStatic
                    && _selectionTarget.ReturnType == _resultType
                    && !_selectionTarget.ContainsGenericParameters
                    && _selectionTarget.GetMethodBody() != null,
                "Exact static LLL GetValidExtendedDungeonFlows contract/body mismatch.");

            _flowField = weighted.GetField("extendedDungeonFlow", InstanceDeclared);
            _rarityField = weighted.GetField("rarity", InstanceDeclared);
            Require(_flowField != null && _flowField.FieldType == flow,
                "ExtendedDungeonFlowWithRarity.extendedDungeonFlow field mismatch.");
            Require(_rarityField != null && _rarityField.FieldType == typeof(int),
                "ExtendedDungeonFlowWithRarity.rarity field mismatch.");

            _dungeonNameProperty = ReadableProperty(flow, "DungeonName", typeof(string));
            _moonNameProperty = ReadableProperty(_levelType, "NumberlessPlanetName", typeof(string));
            _dungeonAssetProperty = flow.GetProperty("DungeonFlow", InstanceDeclared);
            Require(_dungeonAssetProperty != null
                    && _dungeonAssetProperty.PropertyType.Name == "DungeonFlow"
                    && typeof(UnityEngine.Object).IsAssignableFrom(_dungeonAssetProperty.PropertyType)
                    && _dungeonAssetProperty.GetGetMethod(true) != null
                    && _dungeonAssetProperty.GetIndexParameters().Length == 0,
                "Exact LLL DungeonFlow asset property/type mismatch.");

            Type network = lll.GetType("LethalLevelLoader.LethalLevelLoaderNetworkManager", true);
            _selectionCaller = network.GetMethod(
                "GetRandomExtendedDungeonFlowServerRpc",
                InstanceDeclared,
                null,
                Type.EmptyTypes,
                null);
            Require(_selectionCaller != null
                    && _selectionCaller.DeclaringType == network
                    && !_selectionCaller.IsStatic
                    && _selectionCaller.ReturnType == typeof(void)
                    && _selectionCaller.GetMethodBody() != null,
                "Exact LLL server selection caller contract mismatch.");

            Type terminal = lll.GetType("LethalLevelLoader.TerminalManager", true);
            _simulationCaller = terminal.GetMethod(
                "GetSimulationResultsText",
                StaticDeclared,
                null,
                new[] { _levelType },
                null);
            Require(_simulationCaller != null
                    && _simulationCaller.DeclaringType == terminal
                    && _simulationCaller.IsStatic
                    && _simulationCaller.ReturnType == typeof(string)
                    && _simulationCaller.GetMethodBody() != null,
                "Exact LLL terminal simulation caller contract mismatch.");
        }

        private static Assembly RequireDependency(string guid, string expectedVersion, string expectedSha256)
        {
            Require(Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info)
                    && info != null
                    && info.Metadata != null
                    && info.Metadata.Version != null
                    && string.Equals(info.Metadata.Version.ToString(), expectedVersion, StringComparison.Ordinal)
                    && info.Instance != null,
                "Dependency mismatch: " + guid + " expected version " + expectedVersion);

            Require(!string.IsNullOrWhiteSpace(info.Location) && File.Exists(info.Location),
                "Dependency assembly path is unavailable: " + guid);
            string actualSha256 = ComputeSha256(info.Location);
            Require(string.Equals(actualSha256, expectedSha256, StringComparison.Ordinal),
                "Dependency assembly SHA-256 mismatch: " + guid + " got " + actualSha256);

            return info.Instance.GetType().Assembly;
        }

        private static string ComputeSha256(string path)
        {
            using (FileStream stream = File.OpenRead(path))
            using (SHA256 sha = SHA256.Create())
            {
                return BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", string.Empty).ToLowerInvariant();
            }
        }

        private static PropertyInfo ReadableProperty(Type owner, string name, Type type)
        {
            PropertyInfo property = owner.GetProperty(name, InstanceDeclared);
            Require(property != null
                    && property.PropertyType == type
                    && property.GetGetMethod(true) != null
                    && property.GetIndexParameters().Length == 0,
                "Property mismatch: " + owner.FullName + "." + name);
            return property;
        }

        private static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidOperationException(message);
        }

        // Sole gameplay mutation: reduce only the fresh, already viability-filtered and normalized local LLL return list.
        private static void SelectionPostfix(object __result, object __0, bool __1)
        {
            if (!__1 || _runtimeRefused)
                return;

            IList pool;
            object selected;
            int originalCount;

            try
            {
                Require(__0 != null && __0.GetType() == _levelType,
                    "ExtendedLevel runtime identity mismatch.");
                string moon = (string)_moonNameProperty.GetValue(__0);
                if (moon != "Black Mesa")
                    return;

                StackFrame[] frames = new StackTrace(false).GetFrames();
                Require(frames != null, "Cannot identify managed caller stack.");
                bool simulationCaller = frames.Any(frame => frame.GetMethod() == _simulationCaller);
                bool selectionCaller = frames.Any(frame => frame.GetMethod() == _selectionCaller);

                Require(__result != null && __result.GetType() == _resultType,
                    "Returned viable-pool type mismatch.");
                pool = (IList)__result;

                int index = SelectionPolicy.FindDeepSewers(
                    pool,
                    __1,
                    moon,
                    selectionCaller,
                    simulationCaller,
                    entry =>
                    {
                        object extendedFlow = _flowField.GetValue(entry);
                        Require(extendedFlow != null, "Null ExtendedDungeonFlow in viable wrapper.");
                        return (string)_dungeonNameProperty.GetValue(extendedFlow);
                    },
                    entry =>
                    {
                        object extendedFlow = _flowField.GetValue(entry);
                        Require(extendedFlow != null, "Null ExtendedDungeonFlow in Deep Sewers wrapper.");
                        UnityEngine.Object asset = _dungeonAssetProperty.GetValue(extendedFlow) as UnityEngine.Object;
                        return asset == null ? null : asset.name;
                    },
                    entry => (int)_rarityField.GetValue(entry));

                if (index < 0)
                    return;

                Require(!pool.IsReadOnly && !pool.IsFixedSize,
                    "Exact viable result list unexpectedly reports read-only/fixed-size semantics.");
                selected = pool[index];
                originalCount = pool.Count;
            }
            catch (Exception ex)
            {
                _runtimeRefused = true;
                _self.Logger.LogError("[BMDSFIX1-DIAG1] REFUSED selection; normal viable pool preserved: " + ex);
                return;
            }

            // At this point every identity/caller/pool/target/asset/rarity check has completed.
            // The exact runtime type was already proven to be List<ExtendedDungeonFlowWithRarity>.
            pool.Clear();
            pool.Add(selected);
            _self.Logger.LogInfo("[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow; normalized rarity=100; pool="
                + originalCount + "->1; same viable wrapper; DIAGNOSTIC ONLY, NEVER ACCEPT.");
        }
    }
}
