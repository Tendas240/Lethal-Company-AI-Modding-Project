using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "tendas.s142ai.diag1.isolation";
        public const string PluginName = "S1.42AI-DIAG1 ShyGuy Isolation";
        public const string PluginVersion = "0.1.0";

        // Build-ready safety latch. This may be true only after the approved DIAG1 config
        // overlay, config assertions and repository-native compile/static gate have passed.
        // Diagnostic activation still remains default-off and config-gated at runtime.
        private const bool ImplementationComplete = true;

        internal static ManualLogSource Log;
        internal static Harmony Harmony;
        internal static ConfigEntry<bool> DiagnosticEnabled;

        private void Awake()
        {
            Log = Logger;
            DiagnosticEnabled = Config.Bind(
                "Diagnostics",
                "S1.42AI-DIAG1 Enabled",
                false,
                "TEMPORARY DIAGNOSTIC ONLY. Default off. When the implementation is complete, enables exact Shy Guy-only spawn isolation for S1.42AI-DIAG1.");

            if (!DiagnosticEnabled.Value)
            {
                Logger.LogInfo("[DIAG1_DISABLED] S1.42AI-DIAG1 diagnostic mode is disabled; no Harmony hooks are installed.");
                return;
            }

            if (!ImplementationComplete)
            {
                Logger.LogError(
                    "[DIAG1_IMPLEMENTATION_INCOMPLETE] Diagnostic enable was requested on a source revision that has not passed the full approved config-overlay/static-build gate. No Harmony hooks are installed.");
                return;
            }

            Logger.LogWarning("[DIAG1_ENABLED] Temporary S1.42AI-DIAG1 Shy Guy isolation is enabled.");

            Harmony = new Harmony(PluginGuid);
            try
            {
                bool nativeInstalled = NativeGuardInstaller.InstallAll(Harmony);
                if (!nativeInstalled)
                {
                    AbortInstallation(
                        "One or more exact V81 native guard targets failed validation/installation. No fallback target is permitted.");
                    return;
                }

                bool simpleInstalled = PackageOwnerGuardInstaller.InstallSimpleGuards(Harmony);
                if (!simpleInstalled)
                {
                    AbortInstallation(
                        "One or more exact simple package-owner targets failed validation/installation. No fallback target is permitted.");
                    return;
                }

                bool complexInstalled = ComplexOwnerGuardInstaller.InstallComplexGuards(Harmony);
                if (!complexInstalled)
                {
                    AbortInstallation(
                        "One or more exact complex package-owner targets/transpilers failed validation/installation. No fallback target is permitted.");
                    return;
                }

                Logger.LogInfo(
                    "[DIAG1_GUARD_LAYERS_INSTALLED] native=true, simpleOwners=true, complexOwners=true; " +
                    "all hooks belong only to the DIAG1 Harmony instance.");

                StartCoroutine(DiagnosticStartupAssertions.RunAfterPluginAwake());
            }
            catch (Exception ex)
            {
                AbortInstallation(
                    $"Unexpected exception during exact DIAG1 guard installation: {ex.GetType().Name}: {ex.Message}");
            }
        }

        private void AbortInstallation(string reason)
        {
            DiagnosticIsolation.MarkInvalid(reason);

            if (Harmony == null)
                return;

            try
            {
                Harmony.UnpatchSelf();
                Logger.LogError(
                    "[DIAG1_INSTALL_ROLLED_BACK] Removed all Harmony hooks owned by the DIAG1 Harmony instance after incomplete installation.");
            }
            catch (Exception rollbackEx)
            {
                Logger.LogError(
                    $"[DIAG1_INSTALL_ROLLBACK_FAILED] Failed to remove the partially installed DIAG1 Harmony set: " +
                    $"{rollbackEx.GetType().Name}: {rollbackEx.Message}");
            }
        }
    }

    internal static class NativeGuardInstaller
    {
        internal static bool InstallAll(Harmony harmony)
        {
            bool ok = true;

            ok &= PatchExact(
                harmony,
                "RoundManager.PredictAllOutsideEnemies()",
                ExactDeclaredMethod(typeof(RoundManager), "PredictAllOutsideEnemies", Type.EmptyTypes, typeof(void)),
                prefix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.PredictAllOutsideEnemiesPrefix), Priority.First));

            ok &= PatchExact(
                harmony,
                "RoundManager.BeginEnemySpawning()",
                ExactDeclaredMethod(typeof(RoundManager), "BeginEnemySpawning", Type.EmptyTypes, typeof(void)),
                prefix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.BeginEnemySpawningPrefix), Priority.First));

            ok &= PatchExact(
                harmony,
                "RoundManager.PlotOutEnemiesForNextHour()",
                ExactDeclaredMethod(typeof(RoundManager), "PlotOutEnemiesForNextHour", Type.EmptyTypes, typeof(void)),
                prefix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.PlotOutEnemiesForNextHourPrefix), Priority.First));

            ok &= PatchExact(
                harmony,
                "RoundManager.FinishGeneratingNewLevelClientRpc()",
                ExactDeclaredMethod(typeof(RoundManager), "FinishGeneratingNewLevelClientRpc", Type.EmptyTypes, typeof(void)),
                postfix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.FinishGeneratingNewLevelClientRpcPostfix), Priority.Last));

            MethodInfo assign = ExactDeclaredMethod(
                typeof(RoundManager),
                "AssignRandomEnemyToVent",
                new[] { typeof(EnemyVent), typeof(float) },
                typeof(bool));

            ok &= PatchExact(
                harmony,
                "RoundManager.AssignRandomEnemyToVent(EnemyVent,float)",
                assign,
                prefix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.AssignRandomEnemyToVentPrefix), Priority.First),
                postfix: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.AssignRandomEnemyToVentPostfix), Priority.Last),
                finalizer: HarmonyMethod(typeof(NativeGuardPatches), nameof(NativeGuardPatches.AssignRandomEnemyToVentFinalizer), Priority.Last));

            return ok;
        }

        private static HarmonyMethod HarmonyMethod(Type owner, string methodName, int priority)
        {
            const BindingFlags flags =
                BindingFlags.Static |
                BindingFlags.Public |
                BindingFlags.NonPublic |
                BindingFlags.DeclaredOnly;

            MethodInfo[] matches = owner
                .GetMethods(flags)
                .Where(method => string.Equals(method.Name, methodName, StringComparison.Ordinal))
                .ToArray();

            if (matches.Length != 1 ||
                matches[0].DeclaringType != owner ||
                !matches[0].IsStatic ||
                matches[0].GetMethodBody() == null)
            {
                throw new MissingMethodException(
                    $"Exact local Harmony patch method {owner.FullName}.{methodName} did not resolve to exactly one declared static method with a body; matches={matches.Length}.");
            }

            return new HarmonyMethod(matches[0]) { priority = priority };
        }

        private static MethodInfo ExactDeclaredMethod(Type owner, string name, Type[] parameters, Type returnType)
        {
            MethodInfo method = owner.GetMethod(
                name,
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly,
                null,
                parameters,
                null);

            if (method == null ||
                method.DeclaringType != owner ||
                method.IsStatic ||
                method.ReturnType != returnType ||
                method.GetMethodBody() == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_TARGET_INVALID] Exact declared target {owner.FullName}.{name}({string.Join(",", parameters.Select(p => p.FullName))}) -> {returnType.FullName} did not validate.");
                return null;
            }

            ParameterInfo[] actual = method.GetParameters();
            if (actual.Length != parameters.Length)
            {
                Plugin.Log.LogError($"[DIAG1_TARGET_INVALID] Parameter-count mismatch on {owner.FullName}.{name}.");
                return null;
            }

            for (int i = 0; i < actual.Length; i++)
            {
                if (actual[i].ParameterType != parameters[i])
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_TARGET_INVALID] Parameter {i} mismatch on {owner.FullName}.{name}: expected {parameters[i].FullName}, got {actual[i].ParameterType.FullName}.");
                    return null;
                }
            }

            return method;
        }

        private static bool PatchExact(
            Harmony harmony,
            string label,
            MethodInfo original,
            HarmonyMethod prefix = null,
            HarmonyMethod postfix = null,
            HarmonyMethod finalizer = null)
        {
            if (original == null)
                return false;

            try
            {
                harmony.Patch(original, prefix, postfix, null, finalizer, null);
                Plugin.Log.LogInfo($"[DIAG1_TARGET_INSTALLED] {label}");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_TARGET_INVALID] Failed to install exact target {label}: {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }
    }

    internal static class NativeGuardPatches
    {
        public static void PredictAllOutsideEnemiesPrefix()
        {
            DiagnosticIsolation.QuarantineAllPools("PredictAllOutsideEnemies/Prefix", terminalIdentityCheck: false);
        }

        public static void BeginEnemySpawningPrefix()
        {
            DiagnosticIsolation.QuarantineAllPools("BeginEnemySpawning/Prefix", terminalIdentityCheck: true);
        }

        public static void PlotOutEnemiesForNextHourPrefix()
        {
            DiagnosticIsolation.QuarantineIndoorPool("PlotOutEnemiesForNextHour/Prefix", terminalIdentityCheck: true);
        }

        public static void FinishGeneratingNewLevelClientRpcPostfix()
        {
            DiagnosticIsolation.QuarantineAllPools("FinishGeneratingNewLevelClientRpc/Postfix", terminalIdentityCheck: true);
            DiagnosticIsolation.AssertNoLiveBypass("FinishGeneratingNewLevelClientRpc/Postfix");
        }

        public static void AssignRandomEnemyToVentPrefix(ref SpecialOverrideState __state)
        {
            DiagnosticIsolation.QuarantineIndoorPool("AssignRandomEnemyToVent/Prefix", terminalIdentityCheck: true);
            __state = DiagnosticIsolation.NeutralizeDeniedSpecialOverride();
        }

        public static void AssignRandomEnemyToVentPostfix(SpecialOverrideState __state)
        {
            DiagnosticIsolation.RestoreSpecialOverride(__state);
        }

        public static Exception AssignRandomEnemyToVentFinalizer(Exception __exception, SpecialOverrideState __state)
        {
            DiagnosticIsolation.RestoreSpecialOverride(__state);
            return __exception;
        }
    }

    internal sealed class SpecialOverrideState
    {
        internal object Level;
        internal MemberInfo SpecialMember;
        internal MemberInfo OverrideMember;
        internal EnemyType PreviousOverride;
        internal bool Changed;
        internal bool Restored;
    }

    internal static class DiagnosticIsolation
    {
        private const string ExpectedAssetName = "ShyGuyDef";
        private const string ExpectedEnemyName = "Shy Guy";
        private const string ExpectedAiType = "ShyGuy.AI.ShyGuyAI";

        private static readonly HashSet<string> LoggedIdentityFailures =
            new HashSet<string>(StringComparer.Ordinal);

        private static EnemyType _allowedEnemy;
        private static bool _identityResolved;
        private static bool _invalid;
        private static int _bypassMarkers;
        private const int MaxBypassMarkers = 16;

        internal static void MarkInvalid(string reason)
        {
            _invalid = true;
            Plugin.Log.LogError($"[DIAG1_INVALID] {reason}");
        }

        internal static void QuarantineAllPools(string stage, bool terminalIdentityCheck)
        {
            RoundManager manager = RoundManager.Instance;
            if (manager == null || manager.currentLevel == null)
            {
                MarkInvalid($"{stage}: RoundManager/currentLevel is unavailable.");
                return;
            }

            ResolveAllowedIdentity(stage, terminalIdentityCheck);

            int removedIndoor = FilterPool(manager.currentLevel, "Enemies");
            int removedOutside = FilterPool(manager.currentLevel, "OutsideEnemies");
            int removedDaytime = FilterPool(manager.currentLevel, "DaytimeEnemies");
            int removedWeed = FilterPool(manager, "WeedEnemies");

            Plugin.Log.LogInfo(
                $"[DIAG1_POOL_GUARD] {stage}: allowed={DescribeAllowed()}; removed indoor={removedIndoor}, outside={removedOutside}, daytime={removedDaytime}, weed={removedWeed}.");
        }

        internal static void QuarantineIndoorPool(string stage, bool terminalIdentityCheck)
        {
            RoundManager manager = RoundManager.Instance;
            if (manager == null || manager.currentLevel == null)
            {
                MarkInvalid($"{stage}: RoundManager/currentLevel is unavailable.");
                return;
            }

            ResolveAllowedIdentity(stage, terminalIdentityCheck);
            int removed = FilterPool(manager.currentLevel, "Enemies");
            Plugin.Log.LogInfo(
                $"[DIAG1_POOL_GUARD] {stage}: allowed={DescribeAllowed()}; removed indoor={removed}.");
        }

        internal static SpecialOverrideState NeutralizeDeniedSpecialOverride()
        {
            SpecialOverrideState state = new SpecialOverrideState();
            RoundManager manager = RoundManager.Instance;
            object level = manager?.currentLevel;
            if (level == null)
            {
                MarkInvalid("AssignRandomEnemyToVent/Prefix: currentLevel unavailable while guarding specialEnemyRarity.");
                return state;
            }

            MemberInfo specialMember = FindInstanceMember(level.GetType(), "specialEnemyRarity");
            if (specialMember == null)
            {
                MarkInvalid("Exact currentLevel.specialEnemyRarity member was not found.");
                return state;
            }

            object special = ReadMember(level, specialMember);
            if (special == null)
            {
                MarkInvalid("currentLevel.specialEnemyRarity unexpectedly resolved to null.");
                return state;
            }

            MemberInfo overrideMember = FindInstanceMember(special.GetType(), "overrideEnemy");
            if (overrideMember == null)
            {
                MarkInvalid("Exact specialEnemyRarity.overrideEnemy member was not found.");
                return state;
            }

            EnemyType previous = ReadMember(special, overrideMember) as EnemyType;
            state.Level = level;
            state.SpecialMember = specialMember;
            state.OverrideMember = overrideMember;
            state.PreviousOverride = previous;

            if (previous == null || IsAllowed(previous))
                return state;

            if (!WriteNestedMember(level, specialMember, special, overrideMember, null))
            {
                MarkInvalid("Failed to temporarily neutralize denied specialEnemyRarity.overrideEnemy.");
                return state;
            }

            state.Changed = true;
            Plugin.Log.LogWarning(
                $"[DIAG1_SPECIAL_OVERRIDE_BLOCKED] Temporarily neutralized non-ShyGuy special override '{DescribeEnemy(previous)}' for AssignRandomEnemyToVent.");
            return state;
        }

        internal static void RestoreSpecialOverride(SpecialOverrideState state)
        {
            if (state == null || !state.Changed || state.Restored)
                return;

            state.Restored = true;
            try
            {
                object special = ReadMember(state.Level, state.SpecialMember);
                if (special == null ||
                    !WriteNestedMember(
                        state.Level,
                        state.SpecialMember,
                        special,
                        state.OverrideMember,
                        state.PreviousOverride))
                {
                    MarkInvalid("Failed to restore exact prior specialEnemyRarity.overrideEnemy reference.");
                    return;
                }

                Plugin.Log.LogInfo(
                    $"[DIAG1_SPECIAL_OVERRIDE_RESTORED] Restored '{DescribeEnemy(state.PreviousOverride)}'.");
            }
            catch (Exception ex)
            {
                MarkInvalid(
                    $"Exception while restoring specialEnemyRarity.overrideEnemy: {ex.GetType().Name}: {ex.Message}");
            }
        }

        internal static void AssertNoLiveBypass(string stage)
        {
            if (!IsServer())
                return;

            EnemyAI[] live = UnityEngine.Object.FindObjectsOfType<EnemyAI>();
            foreach (EnemyAI enemy in live)
            {
                if (enemy == null || IsAllowed(enemy.enemyType))
                    continue;

                _invalid = true;
                if (_bypassMarkers >= MaxBypassMarkers)
                    continue;

                _bypassMarkers++;
                Plugin.Log.LogError(
                    $"[DIAG1_ISOLATION_BYPASS] {stage}: live non-ShyGuy EnemyAI type='{enemy.GetType().FullName}', enemyType='{DescribeEnemy(enemy.enemyType)}', instanceId={enemy.GetInstanceID()}. No cleanup or repair was attempted. marker={_bypassMarkers}/{MaxBypassMarkers}");
            }
        }

        internal static bool IsAllowed(EnemyType enemyType)
        {
            return _identityResolved &&
                   _allowedEnemy != null &&
                   enemyType != null &&
                   ReferenceEquals(enemyType, _allowedEnemy);
        }

        private static void ResolveAllowedIdentity(string stage, bool terminal)
        {
            if (_identityResolved || _invalid)
                return;

            EnemyType[] all = Resources.FindObjectsOfTypeAll<EnemyType>();
            List<EnemyType> related = new List<EnemyType>();
            List<EnemyType> exact = new List<EnemyType>();

            foreach (EnemyType candidate in all)
            {
                if (candidate == null)
                    continue;

                bool assetMatch = string.Equals(candidate.name, ExpectedAssetName, StringComparison.Ordinal);
                bool enemyNameMatch = string.Equals(candidate.enemyName, ExpectedEnemyName, StringComparison.Ordinal);
                bool aiMatch = PrefabHasExactAiType(candidate, ExpectedAiType);

                if (assetMatch || enemyNameMatch || aiMatch)
                    related.Add(candidate);

                if (assetMatch && enemyNameMatch && aiMatch)
                    exact.Add(candidate);
            }

            bool contradiction =
                exact.Count > 1 ||
                (exact.Count == 1 && related.Any(candidate => !ReferenceEquals(candidate, exact[0])));

            if (contradiction)
            {
                string detail = string.Join(" | ", related.Select(DescribeIdentityTriple));
                MarkInvalid(
                    $"[DIAG1_IDENTITY_INVALID] {stage}: Shy Guy identity is ambiguous/contradictory. related={related.Count}, exact={exact.Count}; {detail}");
                return;
            }

            if (exact.Count == 1)
            {
                _allowedEnemy = exact[0];
                _identityResolved = true;
                Plugin.Log.LogInfo(
                    $"[DIAG1_IDENTITY_RESOLVED] asset='{_allowedEnemy.name}', enemyName='{_allowedEnemy.enemyName}', aiType='{ExpectedAiType}', instanceId={_allowedEnemy.GetInstanceID()}.");
                return;
            }

            string key = stage + ":" + terminal;
            if (LoggedIdentityFailures.Add(key))
            {
                string marker = terminal ? "DIAG1_IDENTITY_INVALID" : "DIAG1_IDENTITY_PENDING";
                Plugin.Log.LogError(
                    $"[{marker}] {stage}: exact identity triple asset='{ExpectedAssetName}', enemyName='{ExpectedEnemyName}', aiType='{ExpectedAiType}' was not resolved. Pools remain fail-closed to zero verified identities.");
            }

            if (terminal)
                _invalid = true;
        }

        private static bool PrefabHasExactAiType(EnemyType enemyType, string expectedFullName)
        {
            if (enemyType?.enemyPrefab == null)
                return false;

            try
            {
                Component[] components = enemyType.enemyPrefab.GetComponents<Component>();
                foreach (Component component in components)
                {
                    if (component != null &&
                        string.Equals(component.GetType().FullName, expectedFullName, StringComparison.Ordinal))
                        return true;
                }
            }
            catch (Exception ex)
            {
                string key = "prefab-scan:" + (enemyType.name ?? "<null>");
                if (LoggedIdentityFailures.Add(key))
                {
                    Plugin.Log.LogError(
                        $"[DIAG1_IDENTITY_SCAN_ERROR] Failed to inspect prefab for '{enemyType.name}': {ex.GetType().Name}: {ex.Message}");
                }
            }

            return false;
        }

        private static int FilterPool(object owner, string memberName)
        {
            MemberInfo member = FindInstanceMember(owner.GetType(), memberName);
            if (member == null)
            {
                MarkInvalid($"Exact pool member '{owner.GetType().FullName}.{memberName}' was not found.");
                return 0;
            }

            IList list = ReadMember(owner, member) as IList;
            if (list == null)
            {
                MarkInvalid($"Exact pool member '{owner.GetType().FullName}.{memberName}' is not an IList.");
                return 0;
            }

            int removed = 0;
            for (int i = list.Count - 1; i >= 0; i--)
            {
                EnemyType enemyType = GetEnemyType(list[i]);
                if (IsAllowed(enemyType))
                    continue;

                list.RemoveAt(i);
                removed++;
            }

            return removed;
        }

        private static EnemyType GetEnemyType(object entry)
        {
            if (entry == null)
                return null;

            MemberInfo member = FindInstanceMember(entry.GetType(), "enemyType") ??
                                FindInstanceMember(entry.GetType(), "EnemyType");
            return member == null ? null : ReadMember(entry, member) as EnemyType;
        }

        private static MemberInfo FindInstanceMember(Type type, string name)
        {
            FieldInfo field = type.GetField(
                name,
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            if (field != null)
                return field;

            PropertyInfo property = type.GetProperty(
                name,
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            return property;
        }

        private static object ReadMember(object owner, MemberInfo member)
        {
            if (owner == null || member == null)
                return null;

            if (member is FieldInfo field)
                return field.GetValue(owner);

            if (member is PropertyInfo property && property.CanRead)
                return property.GetValue(owner, null);

            return null;
        }

        private static bool WriteMember(object owner, MemberInfo member, object value)
        {
            if (owner == null || member == null)
                return false;

            try
            {
                if (member is FieldInfo field)
                {
                    if (field.IsInitOnly)
                        return false;
                    field.SetValue(owner, value);
                    return true;
                }

                if (member is PropertyInfo property && property.CanWrite)
                {
                    property.SetValue(owner, value, null);
                    return true;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_MEMBER_WRITE_FAILED] {member.DeclaringType?.FullName}.{member.Name}: {ex.GetType().Name}: {ex.Message}");
            }

            return false;
        }

        private static bool WriteNestedMember(
            object root,
            MemberInfo containerMember,
            object containerValue,
            MemberInfo nestedMember,
            object nestedValue)
        {
            if (!WriteMember(containerValue, nestedMember, nestedValue))
                return false;

            Type containerType = containerValue.GetType();
            if (containerType.IsValueType)
                return WriteMember(root, containerMember, containerValue);

            return true;
        }

        private static string DescribeAllowed()
        {
            return _identityResolved && _allowedEnemy != null
                ? DescribeEnemy(_allowedEnemy)
                : "<none-resolved>";
        }

        private static string DescribeEnemy(EnemyType enemyType)
        {
            if (enemyType == null)
                return "<null>";

            return $"{enemyType.name}/{enemyType.enemyName}";
        }

        private static string DescribeIdentityTriple(EnemyType enemyType)
        {
            if (enemyType == null)
                return "<null>";

            bool ai = PrefabHasExactAiType(enemyType, ExpectedAiType);
            return $"asset='{enemyType.name}', enemyName='{enemyType.enemyName}', aiMatch={ai}";
        }

        private static bool IsServer()
        {
            Type managerType = AccessTools.TypeByName("Unity.Netcode.NetworkManager");
            if (managerType == null)
                return false;

            PropertyInfo singletonProperty = managerType.GetProperty(
                "Singleton",
                BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
            object singleton = singletonProperty?.GetValue(null, null);
            if (singleton == null)
                return false;

            PropertyInfo isServerProperty = managerType.GetProperty(
                "IsServer",
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            if (isServerProperty == null)
                return false;

            try
            {
                return (bool)isServerProperty.GetValue(singleton, null);
            }
            catch
            {
                return false;
            }
        }
    }
}
