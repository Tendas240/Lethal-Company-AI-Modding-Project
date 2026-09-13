using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    /// <summary>
    /// Exact package-owner guards whose reviewed contract can be expressed as a
    /// declared-method Prefix or an IEnumerator replacement. Complex IL branch/call
    /// replacements live in a separate implementation segment.
    ///
    /// This file deliberately has no automatic entry point. Plugin.cs keeps the
    /// implementation-complete latch false until every approved layer is present.
    /// </summary>
    internal static class PackageOwnerGuardInstaller
    {
        private sealed class Target
        {
            internal string Label;
            internal MethodInfo Original;
            internal HarmonyMethod Prefix;
        }

        internal static bool InstallSimpleGuards(Harmony harmony)
        {
            if (harmony == null)
            {
                Plugin.Log.LogError("[DIAG1_OWNER_TARGET_INVALID] Harmony instance is null.");
                return false;
            }

            List<Target> targets = new List<Target>();
            bool valid = true;

            // FacelessStalker 1.2.1
            valid &= AddVoidBlock(
                targets,
                "FacelessStalker SpawnSlenderman",
                "SlendermanMod.Behaviours.SpawnSlendermanEnemyItem",
                "SpawnSlenderman",
                Type.EmptyTypes,
                expectedStatic: false);

            // Football 1.1.14
            valid &= AddVoidBlock(
                targets,
                "Football TrainProp ForceSpawnEnemy",
                "Kittenji.FootballEntity.TrainProp",
                "ForceSpawnEnemy",
                Type.EmptyTypes,
                expectedStatic: false);

            // Herobrine 1.3.9
            valid &= AddVoidBlock(
                targets,
                "Herobrine RedstoneTorch ForceSpawnEnemy",
                "Kittenji.HerobrineMod.RedstoneTorchProp",
                "ForceSpawnEnemy",
                Type.EmptyTypes,
                expectedStatic: false);

            valid &= AddVoidBlock(
                targets,
                "Herobrine developer cmd_Spawn",
                "Kittenji.HerobrineMod.Networking.HerobrineNetworking",
                "cmd_Spawn",
                new[] { typeof(string) },
                expectedStatic: false);

            // Lategame Upgrades 3.14.1. Its false return triggers a Crawler fallback,
            // therefore denied/non-resolved requests must return true.
            valid &= AddCustomPrefix(
                targets,
                "Lategame Upgrades Tools.SpawnMob(string,Vector3,int)",
                "MoreShipUpgrades.Misc.Util.Tools",
                "SpawnMob",
                new[] { typeof(string), typeof(Vector3), typeof(int) },
                typeof(bool),
                expectedStatic: true,
                nameof(SimpleOwnerGuardPatches.LategameSpawnMobPrefix));

            // PremiumScraps 2.5.0: only the dedicated HarryDoll RPC belongs in this
            // simple-prefix tranche. The central Effects.Spawn/SpawnMaskedOfPlayer
            // contracts remain coupled to their exact return/caller static gate.
            valid &= AddVoidBlock(
                targets,
                "PremiumScraps HarryDoll enemy RPC",
                "PremiumScraps.CustomEffects.HarryDoll",
                "SpawnEnemyServerRpc",
                new[] { typeof(Vector3), typeof(bool), typeof(bool) },
                expectedStatic: false);

            // ChillaxScraps 1.6.6: Ocarina consumes returned references downstream, so
            // deny at this dedicated owner RPC rather than fabricating a helper result.
            valid &= AddVoidBlock(
                targets,
                "ChillaxScraps Ocarina enemy-dispatch RPC",
                "ChillaxScraps.CustomEffects.Ocarina",
                "SpawnSpecialEnemyServerRpc",
                new[] { typeof(int), typeof(Vector3), typeof(ulong) },
                expectedStatic: false);

            // CodeRebirth 1.6.9 simple owner surfaces. The spawner/FakeSnailCat/Xui
            // paths require exact branch/callsite transpilers and are intentionally not
            // represented here.
            valid &= AddVoidBlock(
                targets,
                "CodeRebirth TornadoWeather.SpawnTornado",
                "CodeRebirth.src.Content.Weathers.TornadoWeather",
                "SpawnTornado",
                new[] { typeof(Vector3) },
                expectedStatic: false);

            valid &= AddIteratorBlock(
                targets,
                "CodeRebirth GuardPhone.SpawnWithDelay",
                "CodeRebirth.src.Content.Items.GuardPhone",
                "SpawnWithDelay",
                new[] { typeof(Vector3) },
                expectedStatic: false);

            valid &= AddVoidBlock(
                targets,
                "CodeRebirth BoxChute.SpawnEnemy",
                "CodeRebirth.src.Content.Enemies.BoxChute",
                "SpawnEnemy",
                Type.EmptyTypes,
                expectedStatic: false);

            // LethalMinNightly 1.1.108. Resolve foreign argument types exactly from the
            // loaded assembly; never fall back to name-fragment method scans.
            Type pikminType = ResolveRequiredType("LethalMin.PikminType");
            Type leaderType = ResolveRequiredType("LethalMin.Leader");
            Type enemyGrabbableType = ResolveRequiredType("LethalMin.EnemyGrabbableObject");
            Type playerControllerType = ResolveRequiredType("GameNetcodeStuff.PlayerControllerB");

            if (pikminType == null || leaderType == null || enemyGrabbableType == null || playerControllerType == null)
            {
                valid = false;
            }
            else
            {
                Type pikminListType = typeof(List<>).MakeGenericType(pikminType);

                valid &= AddIteratorBlock(
                    targets,
                    "LethalMin Onion.WithdrawPikminFromOnion",
                    "LethalMin.Onion",
                    "WithdrawPikminFromOnion",
                    new[] { pikminListType, typeof(int[]), leaderType },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin Onion.SetEnemyToBeRevived",
                    "LethalMin.Onion",
                    "SetEnemyToBeRevived",
                    new[] { enemyGrabbableType },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin GlowSeed.SpawnGlowPikminServerRpc",
                    "LethalMin.GlowSeed",
                    "SpawnGlowPikminServerRpc",
                    new[] { typeof(ulong) },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin Lumiknull.DepositeItem",
                    "LethalMin.Lumiknull",
                    "DepositeItem",
                    new[] { typeof(float), leaderType },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin Triknull.DepositeItem",
                    "LethalMin.Triknull",
                    "DepositeItem",
                    new[] { typeof(float), leaderType },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin Sprout.PluckAndDespawnServerRpc",
                    "LethalMin.Sprout",
                    "PluckAndDespawnServerRpc",
                    new[] { typeof(ulong) },
                    expectedStatic: false);

                valid &= AddVoidBlock(
                    targets,
                    "LethalMin Sprout.OnInteractEarlyOnOtherClients",
                    "LethalMin.Sprout",
                    "OnInteractEarlyOnOtherClients",
                    new[] { playerControllerType },
                    expectedStatic: false);
            }

            // EndlessElevatorPatch.WaitRespawnPikmin is intentionally deferred until
            // its exact foreign parameter type is anchored by the static target gate;
            // guessing an EndlessElevator namespace would violate the patch-safety rule.

            if (!valid)
            {
                Plugin.Log.LogError(
                    "[DIAG1_OWNER_TARGET_INVALID] At least one simple package-owner target failed exact prevalidation. No simple owner Prefixes were installed.");
                return false;
            }

            foreach (Target target in targets)
            {
                try
                {
                    harmony.Patch(target.Original, prefix: target.Prefix);
                    Plugin.Log.LogInfo($"[DIAG1_OWNER_TARGET_INSTALLED] {target.Label}");
                }
                catch (Exception ex)
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_OWNER_TARGET_INVALID] Failed to install {target.Label}: {ex.GetType().Name}: {ex.Message}");
                    return false;
                }
            }

            return true;
        }

        private static bool AddVoidBlock(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            bool? expectedStatic)
        {
            return AddCustomPrefix(
                targets,
                label,
                ownerTypeName,
                methodName,
                parameters,
                typeof(void),
                expectedStatic,
                nameof(SimpleOwnerGuardPatches.BlockVoidOwnerPrefix));
        }

        private static bool AddIteratorBlock(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            bool? expectedStatic)
        {
            return AddCustomPrefix(
                targets,
                label,
                ownerTypeName,
                methodName,
                parameters,
                typeof(IEnumerator),
                expectedStatic,
                nameof(SimpleOwnerGuardPatches.BlockIteratorOwnerPrefix));
        }

        private static bool AddCustomPrefix(
            List<Target> targets,
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            bool? expectedStatic,
            string prefixName)
        {
            MethodInfo original = ResolveExactDeclaredMethod(
                label,
                ownerTypeName,
                methodName,
                parameters,
                returnType,
                expectedStatic);

            if (original == null)
                return false;

            MethodInfo prefix = typeof(SimpleOwnerGuardPatches).GetMethod(
                prefixName,
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

            if (prefix == null || prefix.GetMethodBody() == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] Internal Prefix {typeof(SimpleOwnerGuardPatches).FullName}.{prefixName} did not validate.");
                return false;
            }

            targets.Add(new Target
            {
                Label = label,
                Original = original,
                Prefix = new HarmonyMethod(prefix) { priority = Priority.First }
            });
            return true;
        }

        private static MethodInfo ResolveExactDeclaredMethod(
            string label,
            string ownerTypeName,
            string methodName,
            Type[] parameters,
            Type returnType,
            bool? expectedStatic)
        {
            Type owner = ResolveRequiredType(ownerTypeName);
            if (owner == null)
                return null;

            MethodInfo method = owner.GetMethod(
                methodName,
                BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                parameters,
                null);

            if (method == null ||
                method.DeclaringType != owner ||
                method.ReturnType != returnType ||
                method.GetMethodBody() == null ||
                (expectedStatic.HasValue && method.IsStatic != expectedStatic.Value))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] {label}: exact declared {ownerTypeName}.{methodName}({DescribeTypes(parameters)}) -> {returnType.FullName} did not validate; expectedStatic={(expectedStatic.HasValue ? expectedStatic.Value.ToString() : "<any>")}.");
                return null;
            }

            ParameterInfo[] actual = method.GetParameters();
            if (actual.Length != parameters.Length)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_OWNER_TARGET_INVALID] {label}: parameter-count mismatch {actual.Length} != {parameters.Length}.");
                return null;
            }

            for (int i = 0; i < actual.Length; i++)
            {
                if (actual[i].ParameterType != parameters[i])
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_OWNER_TARGET_INVALID] {label}: parameter {i} mismatch; expected {parameters[i].FullName}, got {actual[i].ParameterType.FullName}.");
                    return null;
                }
            }

            return method;
        }

        private static Type ResolveRequiredType(string fullName)
        {
            Type type = AccessTools.TypeByName(fullName);
            if (type == null)
            {
                Plugin.Log.LogError($"[DIAG1_OWNER_TARGET_INVALID] Required exact type '{fullName}' was not found.");
            }
            return type;
        }

        private static string DescribeTypes(Type[] types)
        {
            return string.Join(",", (types ?? Type.EmptyTypes).Select(t => t?.FullName ?? "<null>"));
        }
    }

    internal static class SimpleOwnerGuardPatches
    {
        public static bool BlockVoidOwnerPrefix(MethodBase __originalMethod)
        {
            OwnerGuardLog.Blocked(__originalMethod, "dedicated enemy owner transaction");
            return false;
        }

        public static bool BlockIteratorOwnerPrefix(ref IEnumerator __result, MethodBase __originalMethod)
        {
            __result = EmptyIterator();
            OwnerGuardLog.Blocked(__originalMethod, "dedicated enemy/persistence iterator replaced with empty iterator before destructive state");
            return false;
        }

        public static bool LategameSpawnMobPrefix(string __0, ref bool __result, MethodBase __originalMethod)
        {
            string requestedMob = __0 ?? string.Empty;

            // Resolve/reassert exact identity before consulting the exact current indoor table.
            DiagnosticIsolation.QuarantineIndoorPool(
                "LategameUpgrades.Tools.SpawnMob/Prefix",
                terminalIdentityCheck: true);

            RoundManager manager = RoundManager.Instance;
            if (manager == null || manager.currentLevel == null)
            {
                DiagnosticIsolation.MarkInvalid(
                    "LategameUpgrades.Tools.SpawnMob/Prefix: RoundManager/currentLevel unavailable.");
                __result = true;
                OwnerGuardLog.Blocked(__originalMethod, $"mob='{requestedMob}', no current indoor table");
                return false;
            }

            List<EnemyType> matches = new List<EnemyType>();
            foreach (SpawnableEnemyWithRarity entry in manager.currentLevel.Enemies)
            {
                EnemyType enemyType = entry?.enemyType;
                if (enemyType != null &&
                    string.Equals(enemyType.enemyName, requestedMob, StringComparison.OrdinalIgnoreCase))
                {
                    matches.Add(enemyType);
                }
            }

            bool allowed = matches.Count == 1 && DiagnosticIsolation.IsAllowed(matches[0]);
            if (allowed)
                return true;

            // The reviewed Exorcism caller treats false as permission to spawn Crawler.
            // A denied request must therefore report handled/success=true while skipping
            // the original helper, so no fallback enemy is introduced.
            __result = true;
            OwnerGuardLog.Blocked(
                __originalMethod,
                $"mob='{requestedMob}', matches={matches.Count}, exactShyGuy={(matches.Count == 1 && DiagnosticIsolation.IsAllowed(matches[0]))}");
            return false;
        }

        private static IEnumerator EmptyIterator()
        {
            yield break;
        }
    }

    internal static class OwnerGuardLog
    {
        private const int MaxMarkersPerOwner = 8;
        private static readonly Dictionary<string, int> Counts =
            new Dictionary<string, int>(StringComparer.Ordinal);

        internal static void Blocked(MethodBase method, string detail)
        {
            string owner = method?.DeclaringType?.FullName ?? "<unknown-type>";
            string name = method?.Name ?? "<unknown-method>";
            string key = owner + "." + name;

            int count;
            Counts.TryGetValue(key, out count);
            if (count >= MaxMarkersPerOwner)
                return;

            count++;
            Counts[key] = count;
            Plugin.Log.LogWarning(
                $"[DIAG1_OWNER_BLOCKED] owner='{key}', detail='{detail}', marker={count}/{MaxMarkersPerOwner}.");
        }
    }
}
