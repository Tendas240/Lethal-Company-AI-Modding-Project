using System;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace S142XJetpackAcceleration
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(ButteRyBalanceGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(JetpackFixesGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(MoreShipUpgradesGuid, BepInDependency.DependencyFlags.SoftDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142xjetpackacceleration";
        internal const string PluginName = "S1.42X Jetpack Acceleration";
        internal const string PluginVersion = "1.0.0";

        internal const string ButteRyBalanceGuid = "butterystancakes.lethalcompany.butterybalance";
        internal const string JetpackFixesGuid = "butterystancakes.lethalcompany.jetpackfixes";
        internal const string MoreShipUpgradesGuid = "com.malco.lethalcompany.moreshipupgrades";

        private const string ExpectedButteRyBalanceVersion = "0.7.0";
        private const string ExpectedJetpackFixesVersion = "1.6.3";
        private const string ExpectedMoreShipUpgradesVersion = "3.14.1";

        internal static ManualLogSource Log;
        private Harmony harmony;

        private void Awake()
        {
            Log = Logger;

            if (!ValidatePluginVersion(ButteRyBalanceGuid, ExpectedButteRyBalanceVersion, required: true) ||
                !ValidatePluginVersion(JetpackFixesGuid, ExpectedJetpackFixesVersion, required: true) ||
                !ValidatePluginVersion(MoreShipUpgradesGuid, ExpectedMoreShipUpgradesVersion, required: false))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch refused to arm because the validated dependency set does not match the frozen full-stack baseline.");
                return;
            }

            MethodInfo target = AccessTools.DeclaredMethod(typeof(JetpackItem), nameof(JetpackItem.Update), Type.EmptyTypes);
            if (target == null || target.ReturnType != typeof(void))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch refused to arm: exact JetpackItem.Update() target was not found with the expected void signature.");
                return;
            }

            Patches existing = Harmony.GetPatchInfo(target);
            if (existing == null || !existing.Prefixes.Any(p => p.owner == ButteRyBalanceGuid))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch refused to arm: expected ButteRyBalance JetpackItem.Update prefix owner is missing.");
                return;
            }

            if (!existing.Transpilers.Any(p => p.owner == JetpackFixesGuid))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch refused to arm: expected JetpackFixes JetpackItem.Update transpiler owner is missing.");
                return;
            }

            if (Chainloader.PluginInfos.ContainsKey(MoreShipUpgradesGuid) &&
                !existing.Transpilers.Any(p => p.owner == MoreShipUpgradesGuid))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch refused to arm: More Ship Upgrades is loaded but its expected JetpackItem.Update transpiler owner is missing.");
                return;
            }

            harmony = new Harmony(PluginGuid);
            harmony.PatchAll();

            Patches patched = Harmony.GetPatchInfo(target);
            if (patched == null || !patched.Prefixes.Any(p => p.owner == PluginGuid))
            {
                Logger.LogError("S1.42X Jetpack acceleration patch failed post-patch verification; removing project-local patches.");
                harmony.UnpatchSelf();
                return;
            }

            Logger.LogInfo(
                "S1.42X Jetpack acceleration diagnostic patch armed: JetpackItem.Update() local-player base acceleration 10 -> 32, " +
                "ordered after ButteRyBalance; V49 handling/deceleration, maximum power/speed, battery, price and JetpackFixes safety logic are untouched.");
        }

        private bool ValidatePluginVersion(string guid, string expectedVersion, bool required)
        {
            if (!Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info))
            {
                if (required)
                {
                    Logger.LogError($"Required dependency {guid} is not loaded; expected version {expectedVersion}.");
                    return false;
                }

                Logger.LogInfo($"Optional dependency {guid} is not loaded; no compatibility-layer validation is required for it.");
                return true;
            }

            string actualVersion = info.Metadata.Version.ToString();
            if (!string.Equals(actualVersion, expectedVersion, StringComparison.Ordinal))
            {
                Logger.LogError($"Dependency {guid} version mismatch: expected {expectedVersion}, got {actualVersion}.");
                return false;
            }

            Logger.LogInfo($"Validated dependency {guid} v{actualVersion}.");
            return true;
        }
    }

    [HarmonyPatch(typeof(JetpackItem), nameof(JetpackItem.Update))]
    internal static class JetpackAccelerationPatch
    {
        private const float ExpectedBaseAcceleration = 10f;
        private const float TargetBaseAcceleration = 32f;

        [HarmonyPrefix]
        [HarmonyAfter(Plugin.ButteRyBalanceGuid)]
        [HarmonyPriority(Priority.Last)]
        private static void Prefix(JetpackItem __instance)
        {
            if (__instance.playerHeldBy == null ||
                __instance.playerHeldBy != GameNetworkManager.Instance?.localPlayerController)
            {
                return;
            }

            // Diagnostic magnitude: ButteRyBalance v0.7.0 with V49 + Warmup=false writes exactly
            // 10f before the original Update body. Only that proven owner-written baseline is
            // replaced. If 32f still does not materially change vertical lift-off, stop increasing
            // this field and investigate the force/ramp path instead.
            if (Mathf.Approximately(__instance.jetpackAcceleration, ExpectedBaseAcceleration))
            {
                __instance.jetpackAcceleration = TargetBaseAcceleration;
            }
        }
    }
}
