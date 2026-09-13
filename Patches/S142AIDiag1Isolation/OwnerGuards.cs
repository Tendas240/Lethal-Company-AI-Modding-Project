using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    // Direct-owner guard layer from MINIMAL_GUARD_CONTRACT.md.
    // This file deliberately implements only exact Prefix/iterator-wrapper targets.
    // It is not wired into Plugin.Awake yet; the source-level ImplementationComplete
    // latch in Plugin.cs remains false until every approved owner guard, transpiler,
    // runtime assertion and config overlay has been implemented and statically checked.
    internal static class OwnerGuardInstaller
    {
        internal static bool InstallDirectOwnerGuards(Harmony harmony)
        {
            bool ok = true;

            ok &= PatchPrefix(
                harmony,
                "SlendermanMod.Behaviours.SpawnSlendermanEnemyItem",
                "SpawnSlenderman",
                Type.EmptyTypes,
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "FacelessStalker page spawn owner");

            ok &= PatchPrefix(
                harmony,
                "Kittenji.FootballEntity.TrainProp",
                "ForceSpawnEnemy",
                Type.EmptyTypes,
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "Football train spawn owner");

            ok &= PatchPrefix(
                harmony,
                "Kittenji.HerobrineMod.RedstoneTorchProp",
                "ForceSpawnEnemy",
                Type.EmptyTypes,
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "Herobrine redstone-torch spawn owner");

            ok &= PatchPrefix(
                harmony,
                "Kittenji.HerobrineMod.Networking.HerobrineNetworking",
                "cmd_Spawn",
                new[] { typeof(string) },
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "Herobrine developer spawn command");

            ok &= PatchPrefix(
                harmony,
                "MoreShipUpgrades.Misc.Util.Tools",
                "SpawnMob",
                new[] { typeof(string), typeof(Vector3), typeof(int) },
                typeof(bool),
                nameof(OwnerGuardPatches.LategameUpgradesSpawnMobPrefix),
                "Lategame Upgrades SpawnMob owner");

            ok &= PatchPrefix(
                harmony,
                "CodeRebirth.src.Content.Weathers.TornadoWeather",
                "SpawnTornado",
                new[] { typeof(Vector3) },
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "CodeRebirth Tornado owner");

            ok &= PatchPrefix(
                harmony,
                "CodeRebirth.src.Content.Items.GuardPhone",
                "SpawnWithDelay",
                new[] { typeof(Vector3) },
                typeof(IEnumerator),
                nameof(OwnerGuardPatches.EmptyIteratorOwnerPrefix),
                "CodeRebirth GuardPhone delayed Guardsman owner");

            ok &= PatchPrefix(
                harmony,
                "CodeRebirth.src.Content.Enemies.BoxChute",
                "SpawnEnemy",
                Type.EmptyTypes,
                typeof(void),
                nameof(OwnerGuardPatches.BlockDedicatedOwnerPrefix),
                "CodeRebirth BoxChute DebtCollector owner");

            return ok;
        }

        private static bool PatchPrefix(
            Harmony harmony,
            string typeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            string prefixName,
            string label)
        {
            MethodInfo original = ExactOwnerTargetResolver.ResolveDeclaredMethod(
                typeName,
                methodName,
                parameters,
                returnType);

            if (original == null)
                return false;

            MethodInfo prefix = typeof(OwnerGuardPatches).GetMethod(
                prefixName,
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic,
                null,
                null,
                null);

            if (prefix == null)
            {
                Plugin.Log.LogError($"[DIAG1_OWNER_TARGET_INVALID] Prefix implementation '{prefixName}' is missing.");
                return false;
            }

            try
            {
                harmony.Patch(
                    original,
                    prefix: new HarmonyMethod(prefix) { priority = Priority.First });

                Plugin.Log.LogInfo(
                    $"[DIAG1_OWNER_TARGET_INSTALLED] {label}: {ExactOwnerTargetResolver.Describe(original)}");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] Failed to install {label}: {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }
    }

    internal static class ExactOwnerTargetResolver
    {
        internal static MethodInfo ResolveDeclaredMethod(
            string typeName,
            string methodName,
            Type[] parameters,
            Type returnType)
        {
            Type owner = AccessTools.TypeByName(typeName);
            if (owner == null)
            {
                Plugin.Log.LogError($"[DIAG1_OWNER_TARGET_INVALID] Exact declaring type '{typeName}' was not found.");
                return null;
            }

            if (parameters == null || parameters.Any(p => p == null))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] One or more exact parameter types for {typeName}.{methodName} could not be resolved.");
                return null;
            }

            MethodInfo[] matches = owner
                .GetMethods(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly)
                .Where(m => string.Equals(m.Name, methodName, StringComparison.Ordinal))
                .Where(m => ParametersExactlyMatch(m.GetParameters(), parameters))
                .Where(m => m.ReturnType == returnType)
                .ToArray();

            if (matches.Length != 1)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] Expected exactly one declared target {typeName}.{methodName}({DescribeTypes(parameters)}) -> {returnType.FullName}; found {matches.Length}. No fallback is permitted.");
                return null;
            }

            MethodInfo method = matches[0];
            if (method.DeclaringType != owner || method.IsAbstract || method.ContainsGenericParameters || method.GetMethodBody() == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] Exact target failed declaring-type/body validation: {Describe(method)}.");
                return null;
            }

            Plugin.Log.LogInfo(
                $"[DIAG1_OWNER_TARGET_VALIDATED] {Describe(method)}; static={method.IsStatic}.");
            return method;
        }

        internal static string Describe(MethodInfo method)
        {
            if (method == null)
                return "<null>";

            return $"{method.DeclaringType?.FullName}.{method.Name}({DescribeTypes(method.GetParameters().Select(p => p.ParameterType).ToArray())}) -> {method.ReturnType.FullName}";
        }

        private static bool ParametersExactlyMatch(ParameterInfo[] actual, Type[] expected)
        {
            if (actual.Length != expected.Length)
                return false;

            for (int i = 0; i < actual.Length; i++)
            {
                if (actual[i].ParameterType != expected[i])
                    return false;
            }

            return true;
        }

        private static string DescribeTypes(Type[] types)
        {
            return string.Join(",", types.Select(t => t?.FullName ?? "<null>"));
        }
    }

    internal static class OwnerGuardPatches
    {
        private const int MaxLogsPerOwner = 8;
        private static readonly Dictionary<string, int> OwnerLogCounts =
            new Dictionary<string, int>(StringComparer.Ordinal);

        public static bool BlockDedicatedOwnerPrefix(MethodBase __originalMethod)
        {
            LogPrevented(__originalMethod, "fixed/non-ShyGuy dedicated owner transaction blocked before enemy creation");
            return false;
        }

        public static bool EmptyIteratorOwnerPrefix(ref IEnumerator __result, MethodBase __originalMethod)
        {
            __result = EmptyIterator();
            LogPrevented(__originalMethod, "dedicated delayed enemy iterator replaced with an empty iterator before enemy creation");
            return false;
        }

        public static bool LategameUpgradesSpawnMobPrefix(
            string __0,
            ref bool __result,
            MethodBase __originalMethod)
        {
            EnemyType requested = DirectOwnerIdentityGate.ResolveIndoorRequest(__0);
            if (requested != null && DirectOwnerIdentityGate.IsExactShyGuy(requested))
            {
                Plugin.Log.LogInfo(
                    $"[DIAG1_OWNER_ALLOWED] {DescribeOwner(__originalMethod)} requested exact Shy Guy '{__0}'. Original SpawnMob transaction remains enabled.");
                return true;
            }

            // Contract requirement: false means "try Crawler fallback" to Exorcism.
            // A denied request must therefore report handled/successful while skipping
            // the actual enemy spawn transaction.
            __result = true;
            LogPrevented(
                __originalMethod,
                $"requested mob='{__0 ?? "<null>"}' did not resolve to the exact Shy Guy identity; returning true to suppress Exorcism fallback");
            return false;
        }

        private static IEnumerator EmptyIterator()
        {
            yield break;
        }

        private static void LogPrevented(MethodBase original, string detail)
        {
            string owner = DescribeOwner(original);
            int count = 0;
            OwnerLogCounts.TryGetValue(owner, out count);
            if (count >= MaxLogsPerOwner)
                return;

            count++;
            OwnerLogCounts[owner] = count;
            Plugin.Log.LogWarning(
                $"[DIAG1_OWNER_PREVENTED] {owner}: {detail}. marker={count}/{MaxLogsPerOwner}");
        }

        private static string DescribeOwner(MethodBase original)
        {
            if (original == null)
                return "<unknown-owner>";

            return $"{original.DeclaringType?.FullName}.{original.Name}";
        }
    }

    internal static class DirectOwnerIdentityGate
    {
        private const string ExpectedAssetName = "ShyGuyDef";
        private const string ExpectedEnemyName = "Shy Guy";
        private const string ExpectedAiType = "ShyGuy.AI.ShyGuyAI";

        private static EnemyType _allowed;
        private static bool _resolved;
        private static bool _terminalFailure;

        internal static EnemyType ResolveIndoorRequest(string requestedName)
        {
            if (string.IsNullOrWhiteSpace(requestedName))
                return null;

            RoundManager manager = RoundManager.Instance;
            if (manager?.currentLevel?.Enemies == null)
            {
                DiagnosticIsolation.MarkInvalid(
                    $"Direct-owner request '{requestedName}' arrived without an available current indoor enemy table.");
                return null;
            }

            List<EnemyType> matches = manager.currentLevel.Enemies
                .Where(entry => entry != null && entry.enemyType != null)
                .Select(entry => entry.enemyType)
                .Where(enemy => string.Equals(enemy.enemyName, requestedName, StringComparison.OrdinalIgnoreCase))
                .Distinct()
                .ToList();

            if (matches.Count > 1)
            {
                DiagnosticIsolation.MarkInvalid(
                    $"Direct-owner mob name '{requestedName}' resolved ambiguously to {matches.Count} indoor EnemyType references.");
                return null;
            }

            return matches.Count == 1 ? matches[0] : null;
        }

        internal static bool IsExactShyGuy(EnemyType candidate)
        {
            if (candidate == null)
                return false;

            EnemyType allowed = ResolveExactIdentity();
            return allowed != null && ReferenceEquals(candidate, allowed);
        }

        private static EnemyType ResolveExactIdentity()
        {
            if (_resolved)
                return _allowed;

            if (_terminalFailure)
                return null;

            EnemyType[] all = Resources.FindObjectsOfTypeAll<EnemyType>();
            List<EnemyType> related = new List<EnemyType>();
            List<EnemyType> exact = new List<EnemyType>();

            foreach (EnemyType candidate in all)
            {
                if (candidate == null)
                    continue;

                bool assetMatch = string.Equals(candidate.name, ExpectedAssetName, StringComparison.Ordinal);
                bool enemyNameMatch = string.Equals(candidate.enemyName, ExpectedEnemyName, StringComparison.Ordinal);
                bool aiMatch = PrefabHasExactAiType(candidate);

                if (assetMatch || enemyNameMatch || aiMatch)
                    related.Add(candidate);

                if (assetMatch && enemyNameMatch && aiMatch)
                    exact.Add(candidate);
            }

            bool contradiction =
                exact.Count > 1 ||
                (exact.Count == 1 && related.Any(candidate => !ReferenceEquals(candidate, exact[0])));

            if (contradiction || exact.Count != 1)
            {
                _terminalFailure = true;
                DiagnosticIsolation.MarkInvalid(
                    $"Direct-owner exact Shy Guy identity failed closed: related={related.Count}, exact={exact.Count}; expected asset='{ExpectedAssetName}', enemyName='{ExpectedEnemyName}', aiType='{ExpectedAiType}'.");
                return null;
            }

            _allowed = exact[0];
            _resolved = true;
            Plugin.Log.LogInfo(
                $"[DIAG1_OWNER_IDENTITY_RESOLVED] asset='{_allowed.name}', enemyName='{_allowed.enemyName}', aiType='{ExpectedAiType}', instanceId={_allowed.GetInstanceID()}.");
            return _allowed;
        }

        private static bool PrefabHasExactAiType(EnemyType enemyType)
        {
            if (enemyType?.enemyPrefab == null)
                return false;

            try
            {
                Component[] components = enemyType.enemyPrefab.GetComponents<Component>();
                return components.Any(component =>
                    component != null &&
                    string.Equals(component.GetType().FullName, ExpectedAiType, StringComparison.Ordinal));
            }
            catch (Exception ex)
            {
                DiagnosticIsolation.MarkInvalid(
                    $"Direct-owner Shy Guy prefab identity scan failed for '{enemyType.name}': {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }
    }
}
