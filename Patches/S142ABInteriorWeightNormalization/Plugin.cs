using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Logging;
using HarmonyLib;

namespace S142ABInteriorWeightNormalization
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(LethalLevelLoaderGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142abinteriorweightnormalization";
        internal const string PluginName = "S1.42AB Interior Weight Normalization";
        internal const string PluginVersion = "1.0.0";

        internal const string LethalLevelLoaderGuid = "imabatby.lethallevelloader";
        private const string ExpectedLethalLevelLoaderVersion = "1.7.12";
        internal const int TargetRarity = 100;

        internal static ManualLogSource Log;
        internal static FieldInfo RarityField;
        internal static FieldInfo ExtendedDungeonFlowField;
        internal static PropertyInfo DungeonNameProperty;

        private Harmony harmony;

        private void Awake()
        {
            Log = Logger;

            if (!ValidateLethalLevelLoaderVersion())
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm because the validated LethalLevelLoader dependency does not match the frozen S1.42Z baseline.");
                return;
            }

            Type dungeonManagerType = AccessTools.TypeByName("LethalLevelLoader.DungeonManager");
            Type extendedLevelType = AccessTools.TypeByName("LethalLevelLoader.ExtendedLevel");
            Type weightedFlowType = AccessTools.TypeByName("LethalLevelLoader.ExtendedDungeonFlowWithRarity");
            Type extendedDungeonFlowType = AccessTools.TypeByName("LethalLevelLoader.ExtendedDungeonFlow");

            if (dungeonManagerType == null || extendedLevelType == null || weightedFlowType == null || extendedDungeonFlowType == null)
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: required LethalLevelLoader runtime types were not found.");
                return;
            }

            MethodInfo target = AccessTools.DeclaredMethod(
                dungeonManagerType,
                "GetValidExtendedDungeonFlows",
                new[] { extendedLevelType, typeof(bool) });

            if (!ValidateTargetContract(target, weightedFlowType, extendedDungeonFlowType))
            {
                return;
            }

            MethodInfo postfix = AccessTools.DeclaredMethod(typeof(DungeonWeightPostfix), nameof(DungeonWeightPostfix.Postfix));
            if (postfix == null)
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: project-local postfix method was not found.");
                return;
            }

            harmony = new Harmony(PluginGuid);
            harmony.Patch(target, postfix: new HarmonyMethod(postfix));

            Patches patched = Harmony.GetPatchInfo(target);
            if (patched == null || !patched.Postfixes.Any(p => p.owner == PluginGuid))
            {
                Logger.LogError("S1.42AB interior weight normalization failed post-patch verification; removing project-local patches.");
                harmony.UnpatchSelf();
                return;
            }

            Logger.LogInfo(
                "S1.42AB interior weight normalization armed: LethalLevelLoader keeps full ownership of viability/exclusion matching; " +
                "only positive rarities in the already-returned viable dungeon list are normalized to 100. " +
                "No dungeon is added, removed, deduplicated, re-registered or config-rewritten by this patch.");
        }

        private bool ValidateLethalLevelLoaderVersion()
        {
            if (!Chainloader.PluginInfos.TryGetValue(LethalLevelLoaderGuid, out PluginInfo info))
            {
                Logger.LogError($"Required dependency {LethalLevelLoaderGuid} is not loaded; expected version {ExpectedLethalLevelLoaderVersion}.");
                return false;
            }

            string actualVersion = info.Metadata.Version.ToString();
            if (!string.Equals(actualVersion, ExpectedLethalLevelLoaderVersion, StringComparison.Ordinal))
            {
                Logger.LogError($"Dependency {LethalLevelLoaderGuid} version mismatch: expected {ExpectedLethalLevelLoaderVersion}, got {actualVersion}.");
                return false;
            }

            Logger.LogInfo($"Validated dependency {LethalLevelLoaderGuid} v{actualVersion}.");
            return true;
        }

        private bool ValidateTargetContract(MethodInfo target, Type weightedFlowType, Type extendedDungeonFlowType)
        {
            if (target == null || !target.IsStatic)
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: exact static DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool) target was not found.");
                return false;
            }

            Type returnType = target.ReturnType;
            if (!returnType.IsGenericType ||
                returnType.GetGenericTypeDefinition() != typeof(List<>) ||
                returnType.GetGenericArguments().Length != 1 ||
                returnType.GetGenericArguments()[0] != weightedFlowType)
            {
                Logger.LogError($"S1.42AB interior weight normalization refused to arm: unexpected target return type {returnType.FullName}.");
                return false;
            }

            FieldInfo rarityField = AccessTools.DeclaredField(weightedFlowType, "rarity");
            FieldInfo flowField = AccessTools.DeclaredField(weightedFlowType, "extendedDungeonFlow");
            PropertyInfo nameProperty = AccessTools.DeclaredProperty(extendedDungeonFlowType, "DungeonName");

            if (rarityField == null || rarityField.FieldType != typeof(int))
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: ExtendedDungeonFlowWithRarity.rarity is missing or is not Int32.");
                return false;
            }

            if (flowField == null || flowField.FieldType != extendedDungeonFlowType)
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: ExtendedDungeonFlowWithRarity.extendedDungeonFlow contract changed.");
                return false;
            }

            if (nameProperty == null || nameProperty.PropertyType != typeof(string) || !nameProperty.CanRead)
            {
                Logger.LogError("S1.42AB interior weight normalization refused to arm: ExtendedDungeonFlow.DungeonName readable string property was not found.");
                return false;
            }

            RarityField = rarityField;
            ExtendedDungeonFlowField = flowField;
            DungeonNameProperty = nameProperty;

            Logger.LogInfo("Validated exact LethalLevelLoader dungeon-selection contract for post-viability rarity normalization.");
            return true;
        }
    }

    internal static class DungeonWeightPostfix
    {
        internal static void Postfix(object __result, object __0, bool __1)
        {
            if (__result == null || Plugin.RarityField == null || Plugin.ExtendedDungeonFlowField == null || Plugin.DungeonNameProperty == null)
            {
                return;
            }

            if (!(__result is IEnumerable entries))
            {
                Plugin.Log.LogError("[InteriorWeightNormalization] Unexpected non-enumerable result; no weights were changed.");
                return;
            }

            int count = 0;
            int changed = 0;
            int minBefore = int.MaxValue;
            int maxBefore = int.MinValue;
            bool sawNonPositive = false;
            var finalPool = new List<string>();

            foreach (object entry in entries)
            {
                if (entry == null)
                {
                    Plugin.Log.LogError("[InteriorWeightNormalization] Null entry in viable dungeon list; skipped without altering list structure.");
                    continue;
                }

                int rarity = (int)Plugin.RarityField.GetValue(entry);
                object flow = Plugin.ExtendedDungeonFlowField.GetValue(entry);
                string name = flow == null ? "<null-flow>" : (Plugin.DungeonNameProperty.GetValue(flow) as string ?? "<unnamed>");

                count++;
                minBefore = Math.Min(minBefore, rarity);
                maxBefore = Math.Max(maxBefore, rarity);

                if (rarity <= 0)
                {
                    sawNonPositive = true;
                    finalPool.Add($"{name}({rarity}:preserved)");
                    continue;
                }

                if (rarity != Plugin.TargetRarity)
                {
                    Plugin.RarityField.SetValue(entry, Plugin.TargetRarity);
                    changed++;
                }

                finalPool.Add($"{name}({Plugin.TargetRarity})");
            }

            if (count == 0)
            {
                Plugin.Log.LogWarning("[InteriorWeightNormalization] LethalLevelLoader returned an empty viable dungeon list; nothing was normalized.");
                return;
            }

            string levelName = TryGetLevelName(__0);
            Plugin.Log.LogInfo(
                $"[InteriorWeightNormalization] Final effective viable pool for {levelName}: {string.Join(", ", finalPool)}");
            Plugin.Log.LogInfo(
                $"[InteriorWeightNormalization] Normalized {changed}/{count} returned viable dungeon weights to {Plugin.TargetRarity}; " +
                $"pre-normalization range was {minBefore}..{maxBefore}; debugResults={__1}.");

            if (sawNonPositive)
            {
                Plugin.Log.LogError("[InteriorWeightNormalization] At least one already-returned viable dungeon had a non-positive rarity. It was preserved instead of being promoted; candidate must not be accepted without investigation.");
            }
        }

        private static string TryGetLevelName(object extendedLevel)
        {
            if (extendedLevel == null)
            {
                return "<null-level>";
            }

            try
            {
                PropertyInfo property = AccessTools.Property(extendedLevel.GetType(), "NumberlessPlanetName");
                if (property != null && property.CanRead && property.PropertyType == typeof(string))
                {
                    return property.GetValue(extendedLevel) as string ?? "<unnamed-level>";
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[InteriorWeightNormalization] Could not read level name for diagnostics: {ex.GetType().Name}: {ex.Message}");
            }

            return extendedLevel.GetType().Name;
        }
    }
}
