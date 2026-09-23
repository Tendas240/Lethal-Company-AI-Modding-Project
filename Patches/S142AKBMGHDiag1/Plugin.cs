using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using BepInEx;
using BepInEx.Bootstrap;
using HarmonyLib;
using UnityEngine;

namespace S142AKBMGHDiag1
{
    [BepInPlugin(Guid, "S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic", "1.0.0")]
    [BepInDependency(LllGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(NormalizerGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string Guid = "tendas.lethalcompany.s142akbmghdiag1";
        internal const string LllGuid = "imabatby.lethallevelloader";
        internal const string NormalizerGuid = "tendas.lethalcompany.s142abinteriorweightnormalization";

        private const string LllVersion = "1.7.12";
        private const string LllSha = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c";
        private const string NormalizerVersion = "1.0.0";
        private const string NormalizerSha = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06";
        private const string GameAssemblySha = "5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731";

        private const BindingFlags StaticDeclared = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        private const BindingFlags InstanceDeclared = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;

        private static Plugin self;
        private static Type levelType;
        private static Type resultType;
        private static Type entranceTeleportType;
        private static MethodInfo selectionTarget;
        private static MethodInfo selectionCaller;
        private static MethodInfo simulationCaller;
        private static MethodInfo teleportTarget;
        private static MethodInfo findObjectsOfTypeMethod;
        private static FieldInfo flowField;
        private static FieldInfo rarityField;
        private static FieldInfo entranceIdField;
        private static FieldInfo entranceSideField;
        private static FieldInfo exitScriptField;
        private static PropertyInfo dungeonNameProperty;
        private static PropertyInfo dungeonAssetProperty;
        private static PropertyInfo moonNameProperty;

        private static bool runtimeRefused;
        private static bool targetSelectionSucceeded;
        private static bool topologySnapshotDone;
        private static bool observerFaulted;
        private static readonly TraversalCoverage coverage = new TraversalCoverage();

        private Harmony harmony;

        private void Awake()
        {
            self = this;
            try
            {
                Assembly lll = Dependency(LllGuid, LllVersion, LllSha);
                Dependency(NormalizerGuid, NormalizerVersion, NormalizerSha);
                ResolveSelectionContract(lll);
                ResolveObservationContract();

                Patches priorSelection = Harmony.GetPatchInfo(selectionTarget);
                Require(priorSelection != null && priorSelection.Postfixes.Count(p => p.owner == NormalizerGuid) == 1,
                    "Accepted normalizer postfix is not uniquely installed on the exact LLL selection target.");

                MethodInfo selectionPostfix = typeof(Plugin).GetMethod(nameof(SelectionPostfix), StaticDeclared);
                MethodInfo teleportPostfix = typeof(Plugin).GetMethod(nameof(TeleportPostfix), StaticDeclared);
                Require(selectionPostfix != null && teleportPostfix != null, "Diagnostic postfix methods are missing.");

                harmony = new Harmony(Guid);
                harmony.Patch(selectionTarget, postfix: new HarmonyMethod(selectionPostfix)
                {
                    after = new[] { NormalizerGuid },
                    priority = Priority.Last
                });
                harmony.Patch(teleportTarget, postfix: new HarmonyMethod(teleportPostfix)
                {
                    priority = Priority.Last
                });

                Patches installedSelection = Harmony.GetPatchInfo(selectionTarget);
                Require(installedSelection != null && installedSelection.Postfixes.Count(p => p.owner == Guid) == 1,
                    "Diagnostic selection postfix is not uniquely installed.");
                Patch diagnosticSelection = installedSelection.Postfixes.Single(p => p.owner == Guid);
                Require(diagnosticSelection.after != null && diagnosticSelection.after.Contains(NormalizerGuid),
                    "Diagnostic selection postfix lost its after-normalizer ordering declaration.");

                Patches installedTeleport = Harmony.GetPatchInfo(teleportTarget);
                Require(installedTeleport != null && installedTeleport.Postfixes.Count(p => p.owner == Guid) == 1,
                    "Diagnostic TeleportPlayer observer postfix is not uniquely installed.");

                Logger.LogInfo("[BMGHDIAG1] ARMED exact LLL selection + V81 TeleportPlayer observer contracts; Black Mesa / Greenhouse only; DIAGNOSTIC ONLY, NEVER ACCEPT.");
                Logger.LogInfo("[BMGHDIAG1] Selection postfix owners: " + string.Join(", ", installedSelection.Postfixes.Select(p => p.owner)));
                Logger.LogInfo("[BMGHDIAG1] TeleportPlayer postfix owners: " + string.Join(", ", installedTeleport.Postfixes.Select(p => p.owner)));
            }
            catch (Exception ex)
            {
                harmony?.UnpatchSelf();
                Logger.LogError("[BMGHDIAG1] REFUSED TO ARM; normal behavior preserved: " + ex);
            }
        }

        private static void ResolveSelectionContract(Assembly lll)
        {
            Type manager = lll.GetType("LethalLevelLoader.DungeonManager", true);
            levelType = lll.GetType("LethalLevelLoader.ExtendedLevel", true);
            Type weighted = lll.GetType("LethalLevelLoader.ExtendedDungeonFlowWithRarity", true);
            Type flow = lll.GetType("LethalLevelLoader.ExtendedDungeonFlow", true);
            resultType = typeof(List<>).MakeGenericType(weighted);

            selectionTarget = manager.GetMethod("GetValidExtendedDungeonFlows", StaticDeclared, null, new[] { levelType, typeof(bool) }, null);
            Require(selectionTarget != null && selectionTarget.DeclaringType == manager && selectionTarget.IsStatic
                && selectionTarget.ReturnType == resultType && !selectionTarget.ContainsGenericParameters
                && selectionTarget.GetMethodBody() != null,
                "Exact static LLL GetValidExtendedDungeonFlows contract/body mismatch.");

            flowField = weighted.GetField("extendedDungeonFlow", InstanceDeclared);
            rarityField = weighted.GetField("rarity", InstanceDeclared);
            Require(flowField != null && flowField.FieldType == flow && rarityField != null && rarityField.FieldType == typeof(int),
                "Weighted LLL flow fields mismatch.");

            dungeonNameProperty = ReadableProperty(flow, "DungeonName", typeof(string));
            moonNameProperty = ReadableProperty(levelType, "NumberlessPlanetName", typeof(string));
            dungeonAssetProperty = flow.GetProperty("DungeonFlow", InstanceDeclared);
            Require(dungeonAssetProperty != null && dungeonAssetProperty.PropertyType.Name == "DungeonFlow"
                && typeof(UnityEngine.Object).IsAssignableFrom(dungeonAssetProperty.PropertyType)
                && dungeonAssetProperty.GetGetMethod(true) != null && dungeonAssetProperty.GetIndexParameters().Length == 0,
                "Exact LLL DungeonFlow asset property/type mismatch.");

            Type network = lll.GetType("LethalLevelLoader.LethalLevelLoaderNetworkManager", true);
            selectionCaller = network.GetMethod("GetRandomExtendedDungeonFlowServerRpc", InstanceDeclared, null, Type.EmptyTypes, null);
            Require(selectionCaller != null && selectionCaller.DeclaringType == network && selectionCaller.ReturnType == typeof(void)
                && selectionCaller.GetMethodBody() != null,
                "Exact LLL server selection caller contract mismatch.");

            Type terminal = lll.GetType("LethalLevelLoader.TerminalManager", true);
            simulationCaller = terminal.GetMethod("GetSimulationResultsText", StaticDeclared, null, new[] { levelType }, null);
            Require(simulationCaller != null && simulationCaller.DeclaringType == terminal && simulationCaller.ReturnType == typeof(string)
                && simulationCaller.GetMethodBody() != null,
                "Exact LLL terminal simulation caller contract mismatch.");
        }

        private static void ResolveObservationContract()
        {
            entranceTeleportType = AccessTools.TypeByName("EntranceTeleport");
            Require(entranceTeleportType != null && entranceTeleportType.FullName == "EntranceTeleport"
                && entranceTeleportType.Assembly.GetName().Name == "Assembly-CSharp",
                "Exact EntranceTeleport type/declaring assembly identity mismatch.");
            ValidateAssemblyHash(entranceTeleportType.Assembly, GameAssemblySha, "Assembly-CSharp.dll");

            teleportTarget = entranceTeleportType.GetMethod("TeleportPlayer", InstanceDeclared, null, Type.EmptyTypes, null);
            Require(teleportTarget != null && teleportTarget.DeclaringType == entranceTeleportType
                && teleportTarget.IsPublic && teleportTarget.ReturnType == typeof(void)
                && teleportTarget.GetMethodBody() != null,
                "Exact installed-V81 EntranceTeleport.TeleportPlayer() contract/body mismatch.");

            entranceIdField = entranceTeleportType.GetField("entranceId", InstanceDeclared);
            entranceSideField = entranceTeleportType.GetField("isEntranceToBuilding", InstanceDeclared);
            exitScriptField = entranceTeleportType.GetField("exitScript", InstanceDeclared);
            Require(entranceIdField != null && entranceIdField.FieldType == typeof(int), "EntranceTeleport.entranceId field mismatch.");
            Require(entranceSideField != null && entranceSideField.FieldType == typeof(bool), "EntranceTeleport.isEntranceToBuilding field mismatch.");
            Require(exitScriptField != null && exitScriptField.FieldType == entranceTeleportType, "EntranceTeleport.exitScript field mismatch.");

            findObjectsOfTypeMethod = typeof(UnityEngine.Object).GetMethod(
                "FindObjectsOfType",
                BindingFlags.Static | BindingFlags.Public,
                null,
                new[] { typeof(Type) },
                null);
            Require(findObjectsOfTypeMethod != null && findObjectsOfTypeMethod.ReturnType == typeof(UnityEngine.Object[]),
                "Unity Object.FindObjectsOfType(Type) observation contract mismatch.");
        }

        private static Assembly Dependency(string guid, string version, string hash)
        {
            Require(Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info)
                && info.Metadata.Version.ToString() == version && info.Instance != null,
                "Dependency mismatch: " + guid + " expected version " + version);
            Assembly assembly = info.Instance.GetType().Assembly;
            ValidateAssemblyHash(assembly, hash, guid);
            return assembly;
        }

        private static void ValidateAssemblyHash(Assembly assembly, string expected, string label)
        {
            string location = assembly.Location;
            Require(!string.IsNullOrWhiteSpace(location) && File.Exists(location), "Cannot hash loaded assembly: " + label);
            using (SHA256 sha = SHA256.Create())
            using (FileStream stream = File.OpenRead(location))
            {
                string actual = BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "").ToLowerInvariant();
                Require(actual == expected, "Loaded assembly SHA-256 mismatch: " + label + " got " + actual);
            }
        }

        private static PropertyInfo ReadableProperty(Type owner, string name, Type type)
        {
            PropertyInfo property = owner.GetProperty(name, InstanceDeclared);
            Require(property != null && property.PropertyType == type && property.GetGetMethod(true) != null
                && property.GetIndexParameters().Length == 0,
                "Property mismatch: " + owner.FullName + "." + name);
            return property;
        }

        private static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidOperationException(message);
        }

        // Sole gameplay mutation: post-filter only the fresh, already-normalized LLL return list.
        private static void SelectionPostfix(object __result, object __0, bool __1)
        {
            if (!__1 || runtimeRefused)
                return;

            try
            {
                Require(__0 != null && __0.GetType() == levelType, "ExtendedLevel runtime identity mismatch.");
                string moon = (string)moonNameProperty.GetValue(__0);
                if (moon != "Black Mesa")
                    return;

                StackFrame[] frames = new StackTrace(false).GetFrames();
                Require(frames != null, "Cannot identify managed caller stack.");
                bool isSimulation = frames.Any(frame => frame.GetMethod() == simulationCaller);
                bool isSelection = frames.Any(frame => frame.GetMethod() == selectionCaller);

                Require(__result != null && __result.GetType() == resultType, "Returned viable-pool type mismatch.");
                IList pool = (IList)__result;
                int index = SelectionPolicy.FindGreenhouse(
                    pool,
                    __1,
                    moon,
                    isSelection,
                    isSimulation,
                    entry =>
                    {
                        object flow = flowField.GetValue(entry);
                        Require(flow != null, "Null ExtendedDungeonFlow in viable wrapper.");
                        return (string)dungeonNameProperty.GetValue(flow);
                    },
                    entry =>
                    {
                        object flow = flowField.GetValue(entry);
                        Require(flow != null, "Null ExtendedDungeonFlow in Greenhouse wrapper.");
                        UnityEngine.Object asset = dungeonAssetProperty.GetValue(flow) as UnityEngine.Object;
                        return asset == null ? null : asset.name;
                    },
                    entry => (int)rarityField.GetValue(entry));

                if (index < 0)
                    return;

                object greenhouse = pool[index];
                int count = pool.Count;
                pool.Clear();
                pool.Add(greenhouse);
                targetSelectionSucceeded = true;
                self.Logger.LogInfo("[BMGHDIAG1] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool="
                    + count + "->1; same viable wrapper; normalizer -> diagnostic singleton; DIAGNOSTIC ONLY.");
            }
            catch (Exception ex)
            {
                runtimeRefused = true;
                self.Logger.LogError("[BMGHDIAG1] REFUSED selection; diagnostic invalid, returned list left unmodified unless all validation had already completed: " + ex);
            }
        }

        // Observation only: original TeleportPlayer() always runs first and remains sole gameplay owner.
        private static void TeleportPostfix(object __instance)
        {
            if (!targetSelectionSucceeded || runtimeRefused || observerFaulted)
                return;

            try
            {
                Require(__instance != null && __instance.GetType() == entranceTeleportType, "Teleport observer instance identity mismatch.");
                int sourceId = (int)entranceIdField.GetValue(__instance);
                bool sourceOutside = (bool)entranceSideField.GetValue(__instance);
                object target = exitScriptField.GetValue(__instance);
                bool hasTarget = target != null;
                int targetId = hasTarget ? (int)entranceIdField.GetValue(target) : -1;
                bool targetOutside = hasTarget && (bool)entranceSideField.GetValue(target);

                TraversalDecision decision = ObservationPolicy.ClassifyTraversal(
                    active: true,
                    sourceId: sourceId,
                    sourceIsEntranceToBuilding: sourceOutside,
                    hasTarget: hasTarget,
                    targetId: targetId,
                    targetIsEntranceToBuilding: targetOutside);

                if (decision == TraversalDecision.OutOfScope)
                {
                    self.Logger.LogInfo("[BMGHDIAG1] TRAVERSAL_IGNORED id=" + sourceId + " outside required diagnostic IDs 0..3.");
                    return;
                }
                if (decision == TraversalDecision.MissingPair)
                {
                    self.Logger.LogWarning("[BMGHDIAG1] TRAVERSAL_INCONCLUSIVE id=" + sourceId + " native exitScript is null after TeleportPlayer(); no success bit recorded.");
                    return;
                }
                if (decision == TraversalDecision.InvalidPair)
                {
                    self.Logger.LogError("[BMGHDIAG1] TRAVERSAL_INCONCLUSIVE sourceId=" + sourceId + " targetId=" + targetId
                        + " sourceSide=" + Side(sourceOutside) + " targetSide=" + Side(targetOutside)
                        + "; native post-state is not an opposite-side same-ID pair; no success bit recorded.");
                    return;
                }
                if (decision != TraversalDecision.Valid)
                    return;

                coverage.Record(sourceId, sourceOutside);
                self.Logger.LogInfo("[BMGHDIAG1] TRAVERSED id=" + sourceId
                    + " sourceSide=" + Side(sourceOutside)
                    + " targetSide=" + Side(targetOutside)
                    + " source=" + ObjectName(__instance)
                    + " target=" + ObjectName(target)
                    + " sourcePos=" + Position(__instance)
                    + " targetPos=" + Position(target));
                self.Logger.LogInfo("[BMGHDIAG1] COVERAGE " + coverage.Summary());

                if (!topologySnapshotDone)
                {
                    topologySnapshotDone = true;
                    LogTopologySnapshot();
                }
            }
            catch (Exception ex)
            {
                observerFaulted = true;
                self.Logger.LogError("[BMGHDIAG1] OBSERVER_INCONCLUSIVE; observation disabled, native gameplay left untouched: " + ex);
            }
        }

        private static void LogTopologySnapshot()
        {
            Array objects = findObjectsOfTypeMethod.Invoke(null, new object[] { entranceTeleportType }) as Array;
            Require(objects != null, "Active EntranceTeleport enumeration returned null.");

            var entries = new List<TeleportTopologyEntry>();
            var details = new List<string>();
            foreach (object item in objects)
            {
                if (item == null || item.GetType() != entranceTeleportType)
                    continue;
                Component component = item as Component;
                if (component == null || component.gameObject == null || !component.gameObject.activeInHierarchy)
                    continue;

                int id = (int)entranceIdField.GetValue(item);
                bool outside = (bool)entranceSideField.GetValue(item);
                entries.Add(new TeleportTopologyEntry(id, outside));
                if (id >= 0 && id <= 3)
                    details.Add("id=" + id + ",side=" + Side(outside) + ",name=" + ObjectName(item) + ",pos=" + Position(item));
            }

            TopologyCheck topology = ObservationPolicy.CheckTopology(entries);
            string orderedDetails = string.Join(" | ", details.OrderBy(value => value, StringComparer.Ordinal));
            if (topology.IsOk)
            {
                self.Logger.LogInfo("[BMGHDIAG1] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4; " + topology.Summary
                    + "; active=" + orderedDetails);
            }
            else
            {
                self.Logger.LogError("[BMGHDIAG1] TOPOLOGY_INCONCLUSIVE " + topology.Summary + "; active=" + orderedDetails
                    + "; no repair attempted.");
            }
        }

        private static string Side(bool isEntranceToBuilding)
        {
            return isEntranceToBuilding ? "outside" : "inside";
        }

        private static string ObjectName(object value)
        {
            Component component = value as Component;
            return component == null || component.gameObject == null ? "<unknown>" : component.gameObject.name;
        }

        private static string Position(object value)
        {
            Component component = value as Component;
            if (component == null || component.transform == null)
                return "<unknown>";
            Vector3 position = component.transform.position;
            return "(" + position.x.ToString("R", CultureInfo.InvariantCulture)
                + "," + position.y.ToString("R", CultureInfo.InvariantCulture)
                + "," + position.z.ToString("R", CultureInfo.InvariantCulture) + ")";
        }
    }
}
