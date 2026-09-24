using System;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Logging;
using HarmonyLib;

namespace S142AKBMDSFix1
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(LethalLevelLoaderGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "com.tendas240.s142ak.bmdsfix1";
        internal const string PluginName = "S1.42AK Black Mesa Deep Sewers Size Fix";
        internal const string PluginVersion = "1.0.0";
        internal const string LethalLevelLoaderGuid = "imabatby.lethallevelloader";
        internal const string ExpectedLethalLevelLoaderVersion = "1.7.12";
        internal const string ExpectedLethalLevelLoaderSha256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c";

        private Harmony _harmony;
        private static ManualLogSource RuntimeLogger;
        private static bool Armed;

        private void Awake()
        {
            RuntimeLogger = Logger;
            try
            {
                MethodInfo target = ResolveAndValidateTarget();
                MethodInfo postfix = AccessTools.Method(typeof(Plugin), nameof(GetClampedDungeonSizePostfix));
                if (postfix == null || !postfix.IsStatic)
                    throw new InvalidOperationException("BMDSFIX1 static postfix method could not be resolved.");

                _harmony = new Harmony(PluginGuid);
                _harmony.Patch(target, postfix: new HarmonyMethod(postfix));
                Armed = true;
                Logger.LogInfo("[BMDSFIX1] ARMED exact LethalLevelLoader 1.7.12 GetClampedDungeonSize postfix; target=Black Mesa/DeepSewersFlow; clamp=1.0");
            }
            catch (Exception ex)
            {
                Armed = false;
                if (_harmony != null)
                    _harmony.UnpatchSelf();
                Logger.LogError("[BMDSFIX1] REFUSED TO ARM; normal behavior preserved: " + ex);
            }
        }

        private MethodInfo ResolveAndValidateTarget()
        {
            if (!Chainloader.PluginInfos.TryGetValue(LethalLevelLoaderGuid, out var pluginInfo) || pluginInfo == null)
                throw new InvalidOperationException("Exact LethalLevelLoader dependency is absent.");

            string actualVersion = pluginInfo.Metadata?.Version?.ToString();
            if (!string.Equals(actualVersion, ExpectedLethalLevelLoaderVersion, StringComparison.Ordinal))
                throw new InvalidOperationException("LethalLevelLoader version mismatch: " + (actualVersion ?? "<null>"));

            if (string.IsNullOrWhiteSpace(pluginInfo.Location) || !File.Exists(pluginInfo.Location))
                throw new InvalidOperationException("LethalLevelLoader assembly path is unavailable.");

            string actualSha = ComputeSha256(pluginInfo.Location);
            if (!string.Equals(actualSha, ExpectedLethalLevelLoaderSha256, StringComparison.Ordinal))
                throw new InvalidOperationException("LethalLevelLoader assembly SHA-256 mismatch: " + actualSha);

            Type dungeonLoaderType = AccessTools.TypeByName("LethalLevelLoader.DungeonLoader");
            if (dungeonLoaderType == null)
                throw new InvalidOperationException("LethalLevelLoader.DungeonLoader type is absent.");

            MethodInfo target = AccessTools.Method(dungeonLoaderType, "GetClampedDungeonSize", Type.EmptyTypes);
            if (target == null || !target.IsPublic || !target.IsStatic || target.ReturnType != typeof(float) || target.GetParameters().Length != 0 || target.GetMethodBody() == null)
                throw new InvalidOperationException("Exact GetClampedDungeonSize() contract/body mismatch.");

            return target;
        }

        private static string ComputeSha256(string path)
        {
            using (FileStream stream = File.OpenRead(path))
            using (SHA256 sha = SHA256.Create())
            {
                byte[] hash = sha.ComputeHash(stream);
                return BitConverter.ToString(hash).Replace("-", string.Empty).ToLowerInvariant();
            }
        }

        private static void GetClampedDungeonSizePostfix(ref float __result)
        {
            if (!Armed)
                return;

            try
            {
                RoundManager roundManager = RoundManager.Instance;
                string moonName = roundManager?.currentLevel?.PlanetName;
                string dungeonFlowName = roundManager?.dungeonGenerator?.Generator?.DungeonFlow?.name;

                float original = __result;
                float adjusted = SizeClampPolicy.Apply(moonName, dungeonFlowName, original, out bool applied);
                if (!applied)
                    return;

                RuntimeLogger?.LogInfo($"[BMDSFIX1] APPLIED {moonName} / {dungeonFlowName} multiplier={original:R}->{adjusted:R}");
                __result = adjusted;
            }
            catch (Exception ex)
            {
                RuntimeLogger?.LogError("[BMDSFIX1] Runtime observation failed; preserving LLL result: " + ex);
            }
        }
    }
}
