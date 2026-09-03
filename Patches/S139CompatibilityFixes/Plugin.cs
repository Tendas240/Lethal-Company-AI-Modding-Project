using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Configuration;
using BepInEx.Logging;
using GameNetcodeStuff;
using HarmonyLib;
using UnityEngine;

namespace S139CompatibilityFixes
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency("299792458.EnemyScan")]
    [BepInDependency("MaxWasUnavailable.LethalModDataLib", BepInDependency.DependencyFlags.SoftDependency)]
    [BepInDependency("com.elitemastereric.coroner", BepInDependency.DependencyFlags.SoftDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "tendas.s139.compatibilityfixes";
        public const string PluginName = "S1.39 Compatibility Fixes";
        public const string PluginVersion = "1.3.3";

        internal static ManualLogSource Log;
        internal static Harmony Harmony;
        internal static Plugin Instance;

        private SelectableLevel _lastDiagnosticIsolationLevel;
        private float _nextJetpackTargetTick;

        private void Awake()
        {
            Log = Logger;
            Instance = this;
            Harmony = new Harmony(PluginGuid);

            DiagnosticEnemyIsolation.Enabled = Config.Bind(
                "Diagnostics",
                "Isolated Enemy Regression",
                false,
                "TEST ONLY. When true, allow only Thumper/Crawler, Puffer/Spore Lizard, Baboon Hawk, and Pikmin-family enemies. Disable again after the focused enemy regression test.").Value;

            Harmony.PatchAll(typeof(ShipDoorPatches));
            Harmony.PatchAll(typeof(NaturalScrapFilterPatches));
            Harmony.PatchAll(typeof(NaturalMapObjectFilterPatches));

            PatchEnemyScan();
            PatchCodeRebirthPikminKillShield();
            PatchLethalModDataLibNullPluginGuard();
            PatchPufferSmokePikminEffectGuard();
            PatchDiagnosticEnemyIsolation();
            PatchCoronerJetpackUpdateSpamGuard();
            PatchJetpackCapacityTarget();
            StartCoroutine(DelayedLethalMinPatches());

            Logger.LogInfo(
                "S1.39 Compatibility Fixes loaded. Ship-door anti-lockout, complete EnemyScan output, " +
                "natural CodeRebirth currency/map-object filtering, Flash Turret suppression, " +
                "CodeRebirth kill-RPC Pikmin protection, the optional LethalModDataLib null-plugin guard, " +
                "Puffer smoke Pikmin-effect guard, generic LethalMin grab/bite state recovery, " +
                "Coroner Jetpack log-spam guard, the 140-second Jetpack target, and the optional isolated-enemy diagnostic are active.");
        }

        private IEnumerator DelayedLethalMinPatches()
        {
            // Wait one frame so all BepInEx plugin Awake methods have run. LethalMin
            // is an optional runtime dependency and does not need a compile-time DLL.
            yield return null;
            PatchLethalMinGrabBiteStateRepair();
        }

        private void Update()
        {
            if (!JetpackCapacityGuard.TargetApplied &&
                Time.unscaledTime >= _nextJetpackTargetTick)
            {
                _nextJetpackTargetTick = Time.unscaledTime + 1f;
                JetpackCapacityGuard.ApplyToLoadedItems(logIfMissing: false);
            }

            if (!DiagnosticEnemyIsolation.Enabled ||
                RoundManager.Instance == null ||
                RoundManager.Instance.currentLevel == null)
                return;

            SelectableLevel currentLevel = RoundManager.Instance.currentLevel;

            // S1.42F proved that even after the Gordion constructor loop was fixed,
            // doing a global EnemyAI scene scan once per second on a routed moon still
            // matched the user's periodic freeze cadence. The diagnostic spawn pools only
            // need to be rewritten when the SelectableLevel changes.
            if (ReferenceEquals(currentLevel, _lastDiagnosticIsolationLevel))
                return;

            _lastDiagnosticIsolationLevel = currentLevel;

            if (!DiagnosticEnemyIsolation.ShouldRunForCurrentLevel())
                return;

            DiagnosticEnemyIsolation.ApplyToCurrentLevel();

            Plugin.Log.LogInfo(
                "[EnemyIsolation] One-shot level isolation applied; continuous global EnemyAI scanning is disabled.");
        }

        private void PatchLethalMinGrabBiteStateRepair()
        {
            int patched = 0;

            foreach (Assembly assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                string assemblyName = assembly.GetName().Name ?? string.Empty;
                if (assemblyName.IndexOf("LethalMin", StringComparison.OrdinalIgnoreCase) < 0)
                    continue;

                IEnumerable<Type> types;
                try
                {
                    types = assembly.GetTypes();
                }
                catch (ReflectionTypeLoadException ex)
                {
                    types = ex.Types.Where(t => t != null);
                }
                catch (Exception ex)
                {
                    Logger.LogWarning(
                        $"[LethalMinStateGuard] Could not enumerate {assemblyName}: {ex.GetType().Name}: {ex.Message}");
                    continue;
                }

                foreach (Type type in types)
                {
                    if (type == null)
                        continue;

                    // S1.42D crashed because the broad scan also attempted to Harmony-patch
                    // inherited PikminAI/PikminItem methods through derived types. HarmonyX
                    // explicitly warned those were not declared/implemented methods.
                    //
                    // Only patch concrete LethalMin enemy-adapter classes, and only methods
                    // actually declared on that class. This still covers BaboonBird,
                    // BushWolf, ForestGiant, RadMech, and future *PikminEnemy adapters
                    // without touching generic PikminAI state-machine methods at startup.
                    string typeName = type.Name ?? string.Empty;
                    if (typeName.IndexOf("PikminEnemy", StringComparison.OrdinalIgnoreCase) < 0)
                        continue;

                    MethodInfo[] declared;
                    try
                    {
                        declared = type.GetMethods(
                            BindingFlags.Instance |
                            BindingFlags.Static |
                            BindingFlags.Public |
                            BindingFlags.NonPublic |
                            BindingFlags.DeclaredOnly);
                    }
                    catch (Exception ex)
                    {
                        Logger.LogWarning(
                            $"[LethalMinStateGuard] Could not inspect declared methods on {type.FullName}: " +
                            $"{ex.GetType().Name}: {ex.Message}");
                        continue;
                    }

                    foreach (MethodInfo method in declared)
                    {
                        if (method == null ||
                            method.IsAbstract ||
                            method.ContainsGenericParameters)
                            continue;

                        string name = method.Name ?? string.Empty;

                        // Patch the actual local interaction method, not generated
                        // ServerRpc/ClientRpc wrappers.
                        bool candidate =
                            string.Equals(name, "BitePikmin", StringComparison.OrdinalIgnoreCase) ||
                            string.Equals(name, "GrabPikmin", StringComparison.OrdinalIgnoreCase) ||
                            string.Equals(name, "GrabPikminWithTongue", StringComparison.OrdinalIgnoreCase);

                        if (!candidate)
                            continue;

                        try
                        {
                            if (method.GetMethodBody() == null)
                                continue;
                        }
                        catch
                        {
                            continue;
                        }

                        try
                        {
                            Harmony.Patch(
                                method,
                                prefix: new HarmonyMethod(typeof(LethalMinGrabBiteStateRepair), nameof(LethalMinGrabBiteStateRepair.Prefix)),
                                postfix: new HarmonyMethod(typeof(LethalMinGrabBiteStateRepair), nameof(LethalMinGrabBiteStateRepair.Postfix)));

                            patched++;
                            Logger.LogInfo(
                                $"[LethalMinStateGuard] Safely patched declared enemy interaction " +
                                $"{type.FullName}.{method.Name}.");
                        }
                        catch (Exception ex)
                        {
                            Logger.LogWarning(
                                $"[LethalMinStateGuard] Failed to patch {type.FullName}.{method.Name}: " +
                                $"{ex.GetType().Name}: {ex.Message}");
                        }
                    }
                }
            }

            if (patched == 0)
            {
                Logger.LogError(
                    "[LethalMinStateGuard] No declared LethalMin enemy BitePikmin/GrabPikmin methods were found. " +
                    "The generic state repair is NOT active; capture the startup log before testing.");
            }
            else
            {
                Logger.LogInfo(
                    $"[LethalMinStateGuard] Safe generic grab/bite state repair registered on {patched} declared enemy method(s).");
            }
        }

        private void PatchDiagnosticEnemyIsolation()
        {
            if (!DiagnosticEnemyIsolation.Enabled)
            {
                Logger.LogInfo("[EnemyIsolation] Diagnostic enemy isolation is disabled.");
                return;
            }

            Logger.LogWarning(
                "[EnemyIsolation] ISOLATED ENEMY TEST MODE ENABLED. Indoor allowlist: Crawler/Thumper + Puffer. " +
                "Outdoor allowlist: Baboon Hawk. Pikmin-family entities remain allowed. " +
                "Spawn pools are rewritten once per level change; no continuous global EnemyAI scene scan is used.");
        }

        private void PatchCoronerJetpackUpdateSpamGuard()
        {
            MethodInfo jetpackUpdate = AccessTools.Method(typeof(JetpackItem), "Update");
            if (jetpackUpdate == null)
            {
                Logger.LogWarning("[CoronerJetpackGuard] JetpackItem.Update was not found; Coroner spam guard not applied.");
                return;
            }

            Patches patchInfo = Harmony.GetPatchInfo(jetpackUpdate);
            if (patchInfo == null)
            {
                Logger.LogInfo("[CoronerJetpackGuard] JetpackItem.Update has no Harmony patches; nothing to remove.");
                return;
            }

            MethodInfo[] coronerPatchMethods = patchInfo.Prefixes
                .Concat(patchInfo.Postfixes)
                .Where(p =>
                    p != null &&
                    p.PatchMethod != null &&
                    p.PatchMethod.DeclaringType != null &&
                    string.Equals(
                        p.PatchMethod.DeclaringType.FullName,
                        "Coroner.Patch.JetpackItemUpdatePatch",
                        StringComparison.Ordinal))
                .Select(p => p.PatchMethod)
                .Distinct()
                .ToArray();

            if (coronerPatchMethods.Length == 0)
            {
                Logger.LogInfo("[CoronerJetpackGuard] Coroner JetpackItem.Update death hook was not present.");
                return;
            }

            int removed = 0;
            foreach (MethodInfo patchMethod in coronerPatchMethods)
            {
                try
                {
                    Harmony.Unpatch(jetpackUpdate, patchMethod);
                    removed++;
                }
                catch (Exception ex)
                {
                    Logger.LogWarning(
                        $"[CoronerJetpackGuard] Failed to remove {patchMethod.Name}: {ex.GetType().Name}: {ex.Message}");
                }
            }

            Logger.LogWarning(
                $"[CoronerJetpackGuard] Removed {removed}/{coronerPatchMethods.Length} Coroner JetpackItem.Update patch method(s). " +
                "Coroner remains enabled; only the per-frame Jetpack death detector is disabled to stop null-player log spam. " +
                "Jetpack-specific death text may fall back to Coroner/vanilla generic cause reporting.");
        }

        private void PatchJetpackCapacityTarget()
        {
            // S1.42D showed JetpackItem does not declare Start; AccessTools.Method
            // resolved inherited GrabbableObject.Start and HarmonyX warned about the
            // overly broad target. Do not patch an inherited lifecycle method.
            //
            // The battery duration lives on the loaded Jetpack Item asset, so retry
            // that narrow asset mutation from Update until the content is available.
            JetpackCapacityGuard.ApplyToLoadedItems(logIfMissing: true);
            Logger.LogInfo(
                "[Jetpack140] Using loaded Jetpack Item asset targeting only; no GrabbableObject.Start Harmony patch.");
        }

        private void PatchEnemyScan()
        {
            MethodInfo enemyScanBuilder = AccessTools.Method(
                AccessTools.TypeByName("EnemyScan.EnemyScan"),
                "BuildEnemyCountString");

            if (enemyScanBuilder == null)
            {
                Logger.LogError("[EnemyScanFix] Could not locate EnemyScan.EnemyScan.BuildEnemyCountString; complete enemy listing patch was not applied.");
                return;
            }

            Harmony.Patch(
                enemyScanBuilder,
                prefix: new HarmonyMethod(typeof(EnemyScanPatch), nameof(EnemyScanPatch.Prefix)));
            Logger.LogInfo("[EnemyScanFix] Patched EnemyScan to list every active EnemyAI regardless of ScanNodeProperties.");
        }

        private void PatchCodeRebirthPikminKillShield()
        {
            Type utilsType = AccessTools.TypeByName("CodeRebirth.src.Util.CodeRebirthUtils");
            MethodInfo killRpc = utilsType == null
                ? null
                : AccessTools.Method(utilsType, "KillEnemyOnOwnerClientRpc");

            if (killRpc == null)
            {
                Logger.LogWarning("[PikminCraneShield] CodeRebirth kill RPC was not found. Dynamic kill shield was not applied.");
                return;
            }

            MethodInfo enemyKill = typeof(EnemyAI)
                .GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
                .FirstOrDefault(m => string.Equals(m.Name, "KillEnemyOnOwnerClient", StringComparison.Ordinal));

            if (enemyKill == null)
            {
                Logger.LogError("[PikminCraneShield] EnemyAI.KillEnemyOnOwnerClient was not found.");
                return;
            }

            Harmony.Patch(
                killRpc,
                prefix: new HarmonyMethod(typeof(CodeRebirthKillContext), nameof(CodeRebirthKillContext.Enter)),
                finalizer: new HarmonyMethod(typeof(CodeRebirthKillContext), nameof(CodeRebirthKillContext.Exit)));

            Harmony.Patch(
                enemyKill,
                prefix: new HarmonyMethod(typeof(CodeRebirthKillContext), nameof(CodeRebirthKillContext.EnemyKillPrefix)));

            Logger.LogInfo(
                "[PikminCraneShield] Protected Pikmin/Puffmin from CodeRebirth utility kill RPCs. " +
                "This provides a direct failsafe for Autonomous Crane squish kills even when LethalMin's crane toggles are already false.");
        }

        private void PatchPufferSmokePikminEffectGuard()
        {
            MethodInfo pufferStart = AccessTools.Method(typeof(PufferAI), "Start");
            if (pufferStart == null)
            {
                Logger.LogError("[PufferPikminGuard] Could not locate PufferAI.Start; smoke-effect guard was not applied.");
                return;
            }

            Harmony.Patch(
                pufferStart,
                postfix: new HarmonyMethod(typeof(PufferSmokePikminEffectGuard), nameof(PufferSmokePikminEffectGuard.Postfix))
                {
                    priority = Priority.Last
                });

            Logger.LogInfo(
                "[PufferPikminGuard] Patched PufferAI.Start to remove LethalMin-injected Pikmin effect-trigger components from Puffer smoke only.");
        }

        private void PatchLethalModDataLibNullPluginGuard()
        {
            Type collectorType = AccessTools.TypeByName("LethalModDataLib.Features.ModDataAttributeCollector");
            if (collectorType == null)
            {
                Logger.LogInfo("[LMDLGuard] LethalModDataLib is not present; guard not needed.");
                return;
            }

            MethodInfo bulkRegister = AccessTools.Method(
                collectorType,
                "RegisterModDataAttributes",
                Type.EmptyTypes);

            MethodInfo registerPerType = collectorType
                .GetMethods(BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic)
                .FirstOrDefault(m =>
                    string.Equals(m.Name, "RegisterModDataAttributes", StringComparison.Ordinal) &&
                    m.GetParameters().Length == 4);

            if (bulkRegister == null || registerPerType == null)
            {
                Logger.LogError("[LMDLGuard] Could not resolve LethalModDataLib registration methods; NRE guard was not applied.");
                return;
            }

            LethalModDataLibNullPluginGuard.RegisterPerTypeMethod = registerPerType;
            Harmony.Patch(
                bulkRegister,
                prefix: new HarmonyMethod(typeof(LethalModDataLibNullPluginGuard), nameof(LethalModDataLibNullPluginGuard.Prefix)));

            Logger.LogInfo(
                "[LMDLGuard] Patched LethalModDataLib bulk ModDataAttribute registration to skip Chainloader PluginInfo entries with null Instance while preserving registration for valid plugins.");
        }
    }

    internal static class JetpackCapacityGuard
    {
        internal const float TargetSeconds = 140f;
        internal static bool TargetApplied;

        internal static void ApplyToLoadedItems(bool logIfMissing)
        {
            Item[] items = Resources.FindObjectsOfTypeAll<Item>();
            bool foundJetpack = false;

            foreach (Item item in items)
            {
                if (item == null || !string.Equals(item.itemName, "Jetpack", StringComparison.OrdinalIgnoreCase))
                    continue;

                foundJetpack = true;
                if (Apply(item, "loaded Item registry"))
                    TargetApplied = true;
                else if (ReadBatteryUsage(item, out float current) &&
                         Math.Abs(current - TargetSeconds) < 0.001f)
                    TargetApplied = true;
            }

            if (!foundJetpack && logIfMissing)
            {
                Plugin.Log.LogInfo(
                    "[Jetpack140] Jetpack Item asset is not loaded yet; narrow asset targeting will retry.");
            }
        }

        private static bool ReadBatteryUsage(Item item, out float value)
        {
            value = 0f;
            if (item == null)
                return false;

            FieldInfo field = AccessTools.Field(item.GetType(), "batteryUsage") ??
                              AccessTools.Field(typeof(Item), "batteryUsage");
            if (field == null)
                return false;

            try
            {
                value = Convert.ToSingle(field.GetValue(item));
                return true;
            }
            catch
            {
                return false;
            }
        }

        private static bool Apply(Item item, string source)
        {
            if (item == null)
                return false;

            FieldInfo field = AccessTools.Field(item.GetType(), "batteryUsage") ??
                              AccessTools.Field(typeof(Item), "batteryUsage");

            if (field == null)
            {
                Plugin.Log.LogError("[Jetpack140] Item.batteryUsage field was not found.");
                return false;
            }

            try
            {
                float before = Convert.ToSingle(field.GetValue(item));
                if (Math.Abs(before - TargetSeconds) < 0.001f)
                    return false;

                object value = Convert.ChangeType(TargetSeconds, field.FieldType);
                field.SetValue(item, value);

                Plugin.Log.LogInfo(
                    $"[Jetpack140] Jetpack battery duration changed {before:0.###} -> {TargetSeconds:0.###} seconds via {source}.");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogError(
                    $"[Jetpack140] Failed to set Jetpack battery duration via {source}: {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }
    }

    internal static class DiagnosticEnemyIsolation
    {
        internal static bool Enabled;

        private static readonly HashSet<string> IndoorTargets =
            new HashSet<string>(StringComparer.OrdinalIgnoreCase) { "crawler", "thumper", "puffer", "sporelizard" };

        private static readonly HashSet<string> OutdoorTargets =
            new HashSet<string>(StringComparer.OrdinalIgnoreCase) { "baboonhawk", "baboonbird" };

        private static readonly HashSet<int> RemovedLiveIds = new HashSet<int>();
        private static readonly HashSet<string> MissingTypeWarnings = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        private static bool LoggedGordionSkip;

        internal static bool ShouldRunForCurrentLevel()
        {
            if (!Enabled || RoundManager.Instance == null || RoundManager.Instance.currentLevel == null)
                return false;

            string planetName = RoundManager.Instance.currentLevel.PlanetName ?? string.Empty;
            if (planetName.IndexOf("Gordion", StringComparison.OrdinalIgnoreCase) >= 0)
            {
                if (!LoggedGordionSkip)
                {
                    LoggedGordionSkip = true;
                    Plugin.Log.LogInfo(
                        "[EnemyIsolation] Skipping diagnostic pool work on Gordion/Company while in orbit.");
                }
                return false;
            }

            return true;
        }

        internal static void ApplyToCurrentLevel()
        {
            if (!ShouldRunForCurrentLevel())
                return;

            SelectableLevel level = RoundManager.Instance.currentLevel;
            bool changed = false;

            changed |= FilterPool(level, "Enemies", IndoorTargets, ensureTargets: true);
            changed |= FilterPool(level, "OutsideEnemies", OutdoorTargets, ensureTargets: true);
            changed |= FilterPool(level, "DaytimeEnemies", new HashSet<string>(StringComparer.OrdinalIgnoreCase), ensureTargets: false);

            if (changed)
            {
                Plugin.Log.LogInfo(
                    $"[EnemyIsolation] Applied isolated enemy pools to '{level.PlanetName}'. " +
                    "Indoor=Crawler/Puffer; Outdoor=Baboon Hawk; Daytime=none (Pikmin-family entries, if any, are preserved).");
            }
        }

        private static bool FilterPool(
            SelectableLevel level,
            string memberName,
            HashSet<string> targetNames,
            bool ensureTargets)
        {
            object raw = null;
            Type levelType = level.GetType();

            FieldInfo field = AccessTools.Field(levelType, memberName);
            PropertyInfo property = field == null ? AccessTools.Property(levelType, memberName) : null;

            try
            {
                raw = field != null ? field.GetValue(level) : property?.GetValue(level, null);
            }
            catch
            {
                return false;
            }

            IList list = raw as IList;
            if (list == null)
                return false;

            bool changed = false;
            HashSet<string> present = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            object templateEntry = list.Count > 0 ? list[0] : null;

            for (int i = list.Count - 1; i >= 0; i--)
            {
                object entry = list[i];
                EnemyType enemyType = GetEnemyType(entry);
                string normalized = NormalizeEnemyName(enemyType != null ? enemyType.enemyName : null);

                if (IsPikminFamily(normalized))
                    continue;

                if (!targetNames.Contains(normalized))
                {
                    list.RemoveAt(i);
                    changed = true;
                    continue;
                }

                present.Add(normalized);
                SetRarity(entry, 100);
            }

            if (!ensureTargets)
                return changed;

            foreach (string targetName in targetNames)
            {
                // Alias pairs point to the same actual EnemyType. Do not add duplicates:
                // Crawler/Thumper, Puffer/SporeLizard, BaboonHawk/BaboonBird.
                if (present.Contains(targetName))
                    continue;

                if ((targetName == "thumper" && present.Contains("crawler")) ||
                    (targetName == "crawler" && present.Contains("thumper")) ||
                    (targetName == "sporelizard" && present.Contains("puffer")) ||
                    (targetName == "puffer" && present.Contains("sporelizard")) ||
                    (targetName == "baboonbird" && present.Contains("baboonhawk")) ||
                    (targetName == "baboonhawk" && present.Contains("baboonbird")))
                    continue;

                EnemyType found = FindEnemyType(targetName);
                if (found == null)
                    continue;

                object newEntry = CreateSpawnEntry(list, templateEntry, found, 100);
                if (newEntry == null)
                    continue;

                list.Add(newEntry);
                present.Add(NormalizeEnemyName(found.enemyName));
                changed = true;
            }

            return changed;
        }

        private static EnemyType GetEnemyType(object entry)
        {
            if (entry == null)
                return null;

            Type type = entry.GetType();
            FieldInfo field = AccessTools.Field(type, "enemyType");
            if (field != null)
                return field.GetValue(entry) as EnemyType;

            PropertyInfo property = AccessTools.Property(type, "enemyType") ??
                                    AccessTools.Property(type, "EnemyType");
            return property?.GetValue(entry, null) as EnemyType;
        }

        private static void SetRarity(object entry, int rarity)
        {
            if (entry == null)
                return;

            Type type = entry.GetType();
            FieldInfo field = AccessTools.Field(type, "rarity");
            if (field != null && !field.IsInitOnly)
            {
                try
                {
                    field.SetValue(entry, Convert.ChangeType(rarity, field.FieldType));
                }
                catch
                {
                }
                return;
            }

            PropertyInfo property = AccessTools.Property(type, "rarity") ??
                                    AccessTools.Property(type, "Rarity");
            if (property != null && property.CanWrite)
            {
                try
                {
                    property.SetValue(entry, Convert.ChangeType(rarity, property.PropertyType), null);
                }
                catch
                {
                }
            }
        }

        private static object CreateSpawnEntry(IList list, object templateEntry, EnemyType enemyType, int rarity)
        {
            Type listType = list.GetType();
            Type entryType = listType.IsGenericType ? listType.GetGenericArguments().FirstOrDefault() : null;
            if (entryType == null)
                return null;

            try
            {
                object entry = null;

                // V81 SpawnableEnemyWithRarity has no parameterless constructor. Prefer
                // its EnemyType/int constructor and fall back to cloning an existing
                // pool entry so the diagnostic layer never enters an exception loop.
                ConstructorInfo ctor = entryType.GetConstructor(
                    BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic,
                    null,
                    new Type[] { typeof(EnemyType), typeof(int) },
                    null);

                if (ctor != null)
                    entry = ctor.Invoke(new object[] { enemyType, rarity });

                if (entry == null && templateEntry != null && entryType.IsInstanceOfType(templateEntry))
                {
                    MethodInfo clone = typeof(object).GetMethod(
                        "MemberwiseClone",
                        BindingFlags.Instance | BindingFlags.NonPublic);
                    entry = clone?.Invoke(templateEntry, null);
                }

                if (entry == null)
                    throw new MissingMethodException(
                        $"No usable EnemyType/int constructor or clone template exists for {entryType.FullName}.");

                FieldInfo enemyField = AccessTools.Field(entryType, "enemyType");
                if (enemyField != null)
                    enemyField.SetValue(entry, enemyType);
                else
                {
                    PropertyInfo enemyProperty = AccessTools.Property(entryType, "enemyType") ??
                                                 AccessTools.Property(entryType, "EnemyType");
                    if (enemyProperty == null || !enemyProperty.CanWrite)
                        return null;
                    enemyProperty.SetValue(entry, enemyType, null);
                }

                SetRarity(entry, rarity);
                Plugin.Log.LogInfo(
                    $"[EnemyIsolation] Added '{enemyType.enemyName}' to diagnostic pool with rarity {rarity}.");
                return entry;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning(
                    $"[EnemyIsolation] Could not create diagnostic spawn entry for '{enemyType?.enemyName ?? "<unknown>"}': " +
                    $"{ex.GetType().Name}: {ex.Message}");
                return null;
            }
        }

        private static EnemyType FindEnemyType(string normalizedTarget)
        {
            EnemyType[] all = Resources.FindObjectsOfTypeAll<EnemyType>();
            foreach (EnemyType enemyType in all)
            {
                if (enemyType == null)
                    continue;

                string normalized = NormalizeEnemyName(enemyType.enemyName);
                if (string.Equals(normalized, normalizedTarget, StringComparison.OrdinalIgnoreCase))
                    return enemyType;

                if ((normalizedTarget == "crawler" || normalizedTarget == "thumper") &&
                    (normalized == "crawler" || normalized == "thumper"))
                    return enemyType;

                if ((normalizedTarget == "puffer" || normalizedTarget == "sporelizard") &&
                    (normalized == "puffer" || normalized == "sporelizard"))
                    return enemyType;

                if ((normalizedTarget == "baboonhawk" || normalizedTarget == "baboonbird") &&
                    (normalized == "baboonhawk" || normalized == "baboonbird"))
                    return enemyType;
            }

            if (MissingTypeWarnings.Add(normalizedTarget))
            {
                Plugin.Log.LogWarning(
                    $"[EnemyIsolation] EnemyType '{normalizedTarget}' is not loaded yet; the diagnostic filter will retry.");
            }
            return null;
        }

        internal static void RemoveEscapedLiveEnemies()
        {
            if (!Enabled || !IsServer())
                return;

            EnemyAI[] live = UnityEngine.Object.FindObjectsOfType<EnemyAI>();
            foreach (EnemyAI enemy in live)
            {
                if (enemy == null)
                    continue;

                string name = enemy.enemyType != null ? enemy.enemyType.enemyName : enemy.GetType().Name;
                string normalized = NormalizeEnemyName(name);

                if (IsAllowedLiveEnemy(normalized))
                    continue;

                int id = enemy.GetInstanceID();
                if (RemovedLiveIds.Contains(id))
                    continue;

                if (TryDespawn(enemy))
                {
                    RemovedLiveIds.Add(id);
                    Plugin.Log.LogWarning(
                        $"[EnemyIsolation] Despawned non-allowlisted live enemy '{name}' that bypassed the filtered spawn pools.");
                }
            }
        }

        private static bool TryDespawn(EnemyAI enemy)
        {
            Type networkObjectType = AccessTools.TypeByName("Unity.Netcode.NetworkObject");
            if (networkObjectType == null)
                return false;

            Component networkObject = enemy.GetComponent(networkObjectType);
            if (networkObject == null)
                return false;

            PropertyInfo isSpawnedProperty = AccessTools.Property(networkObjectType, "IsSpawned");
            if (isSpawnedProperty != null)
            {
                try
                {
                    if (!(bool)isSpawnedProperty.GetValue(networkObject, null))
                        return false;
                }
                catch
                {
                }
            }

            MethodInfo despawn = AccessTools.Method(networkObjectType, "Despawn", new Type[] { typeof(bool) });
            if (despawn == null)
                return false;

            try
            {
                despawn.Invoke(networkObject, new object[] { true });
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning(
                    $"[EnemyIsolation] Failed to despawn '{enemy?.name ?? "<unknown>"}': {ex.GetType().Name}: {ex.Message}");
                return false;
            }
        }

        private static bool IsServer()
        {
            Type managerType = AccessTools.TypeByName("Unity.Netcode.NetworkManager");
            if (managerType == null)
                return false;

            PropertyInfo singletonProperty = AccessTools.Property(managerType, "Singleton");
            object singleton = singletonProperty?.GetValue(null, null);
            if (singleton == null)
                return false;

            PropertyInfo isServerProperty = AccessTools.Property(managerType, "IsServer");
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

        internal static bool IsPikminFamily(string normalized)
        {
            if (string.IsNullOrEmpty(normalized))
                return false;

            return normalized.IndexOf("pikmin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   normalized.IndexOf("puffmin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   normalized.IndexOf("bulbmin", StringComparison.OrdinalIgnoreCase) >= 0;
        }

        private static bool IsAllowedLiveEnemy(string normalized)
        {
            return IndoorTargets.Contains(normalized) ||
                   OutdoorTargets.Contains(normalized) ||
                   IsPikminFamily(normalized);
        }

        internal static string NormalizeEnemyName(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
                return string.Empty;

            return new string(value.Where(char.IsLetterOrDigit).ToArray()).ToLowerInvariant();
        }
    }

    internal static class LethalMinGrabBiteStateRepair
    {
        internal sealed class MemberSnapshot
        {
            internal MemberInfo Member;
            internal object Value;
        }

        internal sealed class GrabSnapshot
        {
            internal object Pikmin;
            internal object Adapter;
            internal MethodBase BiteMethod;
            internal MethodInfo ReleaseMethod;
            internal Transform OriginalParent;
            internal readonly List<MemberSnapshot> Members = new List<MemberSnapshot>();
        }

        public static void Prefix(
            MethodBase __originalMethod,
            object __instance,
            object[] __args,
            ref GrabSnapshot __state)
        {
            object pikmin = FindPikminTarget(__args);
            if (!IsAlive(pikmin))
                return;

            __state = Capture(pikmin, __instance, __originalMethod);
        }

        public static void Postfix(GrabSnapshot __state)
        {
            if (__state == null || Plugin.Instance == null)
                return;

            Plugin.Instance.StartCoroutine(RepairAfterGrab(__state));
        }

        private static IEnumerator RepairAfterGrab(GrabSnapshot snapshot)
        {
            // LethalMin's runtime log says the grabbed Pikmin will die after 0.5s.
            // Wait slightly longer: if Invinceable Pikmin blocked that death but the
            // leader was cleared, the survivor is exactly the invalid state we need.
            yield return new WaitForSeconds(0.75f);

            if (!IsAlive(snapshot.Pikmin))
                yield break;

            if (!HasLostLeader(snapshot))
                yield break;

            bool releaseInvoked = false;
            if (snapshot.ReleaseMethod != null && snapshot.Adapter != null)
            {
                try
                {
                    snapshot.ReleaseMethod.Invoke(snapshot.Adapter, new object[] { snapshot.Pikmin });
                    releaseInvoked = true;
                    Plugin.Log.LogWarning(
                        $"[LethalMinStateGuard] Invoked existing release path " +
                        $"{snapshot.ReleaseMethod.DeclaringType?.FullName}.{snapshot.ReleaseMethod.Name} after " +
                        $"{snapshot.BiteMethod?.DeclaringType?.FullName}.{snapshot.BiteMethod?.Name} left a surviving Pikmin leader-less.");
                }
                catch (TargetInvocationException ex)
                {
                    Exception inner = ex.InnerException ?? ex;
                    Plugin.Log.LogWarning(
                        $"[LethalMinStateGuard] Existing release path failed: {inner.GetType().Name}: {inner.Message}. " +
                        "Falling back to pre-grab state restoration.");
                }
                catch (Exception ex)
                {
                    Plugin.Log.LogWarning(
                        $"[LethalMinStateGuard] Existing release path failed: {ex.GetType().Name}: {ex.Message}. " +
                        "Falling back to pre-grab state restoration.");
                }
            }

            if (releaseInvoked)
            {
                yield return null;
                if (!HasLostLeader(snapshot))
                {
                    Plugin.Log.LogInfo(
                        "[LethalMinStateGuard] Existing LethalMin release path restored a valid leader/follow state.");
                    yield break;
                }
            }

            int restored = RestorePreGrabState(snapshot);

            Component component = snapshot.Pikmin as Component;
            if (component != null && component.transform != null &&
                component.transform.parent != snapshot.OriginalParent)
            {
                component.transform.SetParent(snapshot.OriginalParent, true);
            }

            Plugin.Log.LogWarning(
                $"[LethalMinStateGuard] Repaired surviving grabbed Pikmin by restoring {restored} pre-grab " +
                "leader/follow/grab member(s). This prevents the Invincible-Pikmin 'Leader is null when following' loop.");
        }

        private static GrabSnapshot Capture(object pikmin, object adapter, MethodBase biteMethod)
        {
            GrabSnapshot snapshot = new GrabSnapshot
            {
                Pikmin = pikmin,
                Adapter = adapter,
                BiteMethod = biteMethod,
                ReleaseMethod = FindReleaseMethod(adapter?.GetType(), pikmin.GetType())
            };

            Component component = pikmin as Component;
            if (component != null && component.transform != null)
                snapshot.OriginalParent = component.transform.parent;

            foreach (FieldInfo field in GetFields(pikmin.GetType()))
            {
                if (field.IsStatic || field.IsLiteral || !ShouldCapture(field.Name))
                    continue;

                try
                {
                    snapshot.Members.Add(new MemberSnapshot { Member = field, Value = field.GetValue(pikmin) });
                }
                catch
                {
                }
            }

            foreach (PropertyInfo property in GetProperties(pikmin.GetType()))
            {
                if (!property.CanRead || property.GetIndexParameters().Length != 0 || !ShouldCapture(property.Name))
                    continue;

                try
                {
                    snapshot.Members.Add(new MemberSnapshot { Member = property, Value = property.GetValue(pikmin, null) });
                }
                catch
                {
                }
            }

            Plugin.Log.LogInfo(
                $"[LethalMinStateGuard] Captured pre-grab state for {pikmin.GetType().FullName} via " +
                $"{biteMethod?.DeclaringType?.FullName}.{biteMethod?.Name}; trackedMembers={snapshot.Members.Count}; " +
                $"releasePath={(snapshot.ReleaseMethod != null ? snapshot.ReleaseMethod.Name : "<fallback-reflection>")}.");

            return snapshot;
        }

        private static MethodInfo FindReleaseMethod(Type adapterType, Type pikminType)
        {
            if (adapterType == null || pikminType == null)
                return null;

            string[] releaseTokens = { "ReleasePikmin", "SavePikmin", "DropPikmin", "FreePikmin", "LetGoPikmin" };

            return adapterType
                .GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
                .Where(m => releaseTokens.Any(token =>
                    m.Name.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0))
                .Where(m =>
                {
                    ParameterInfo[] parameters = m.GetParameters();
                    return parameters.Length == 1 &&
                           parameters[0].ParameterType.IsAssignableFrom(pikminType);
                })
                .OrderBy(m => Array.FindIndex(
                    releaseTokens,
                    token => m.Name.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0))
                .FirstOrDefault();
        }

        private static object FindPikminTarget(object[] args)
        {
            if (args == null)
                return null;

            foreach (object arg in args)
            {
                if (arg == null)
                    continue;

                Type type = arg.GetType();
                string typeName = type.FullName ?? type.Name ?? string.Empty;
                if (typeName.IndexOf("Pikmin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    typeName.IndexOf("Puffmin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    typeName.IndexOf("Bulbmin", StringComparison.OrdinalIgnoreCase) >= 0)
                    return arg;

                EnemyAI enemy = arg as EnemyAI;
                if (enemy != null && enemy.enemyType != null)
                {
                    string normalized = DiagnosticEnemyIsolation.NormalizeEnemyName(enemy.enemyType.enemyName);
                    if (DiagnosticEnemyIsolation.IsPikminFamily(normalized))
                        return arg;
                }
            }

            return null;
        }

        private static bool HasLostLeader(GrabSnapshot snapshot)
        {
            foreach (MemberSnapshot member in snapshot.Members)
            {
                if (member.Member == null ||
                    member.Member.Name.IndexOf("leader", StringComparison.OrdinalIgnoreCase) < 0 ||
                    IsNullLike(member.Value))
                    continue;

                object current = ReadMember(snapshot.Pikmin, member.Member);
                if (IsNullLike(current))
                    return true;
            }

            return false;
        }

        private static int RestorePreGrabState(GrabSnapshot snapshot)
        {
            int restored = 0;

            foreach (MemberSnapshot member in snapshot.Members)
            {
                if (member.Member == null)
                    continue;

                string name = member.Member.Name ?? string.Empty;
                bool leader = name.IndexOf("leader", StringComparison.OrdinalIgnoreCase) >= 0;
                bool follow = name.IndexOf("follow", StringComparison.OrdinalIgnoreCase) >= 0;
                bool grab = name.IndexOf("grab", StringComparison.OrdinalIgnoreCase) >= 0;
                bool bitten = name.IndexOf("bitten", StringComparison.OrdinalIgnoreCase) >= 0;
                bool eaten = name.IndexOf("eaten", StringComparison.OrdinalIgnoreCase) >= 0;

                if (!(leader || follow || grab || bitten || eaten))
                    continue;

                if (leader && IsNullLike(member.Value))
                    continue;

                if (WriteMember(snapshot.Pikmin, member.Member, member.Value))
                    restored++;
            }

            return restored;
        }

        private static bool ShouldCapture(string name)
        {
            if (string.IsNullOrEmpty(name))
                return false;

            return name.IndexOf("leader", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   name.IndexOf("follow", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   name.IndexOf("grab", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   name.IndexOf("bitten", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   name.IndexOf("eaten", StringComparison.OrdinalIgnoreCase) >= 0;
        }

        private static IEnumerable<FieldInfo> GetFields(Type type)
        {
            for (Type current = type; current != null; current = current.BaseType)
            {
                foreach (FieldInfo field in current.GetFields(
                    BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly))
                    yield return field;
            }
        }

        private static IEnumerable<PropertyInfo> GetProperties(Type type)
        {
            for (Type current = type; current != null; current = current.BaseType)
            {
                foreach (PropertyInfo property in current.GetProperties(
                    BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly))
                    yield return property;
            }
        }

        private static object ReadMember(object target, MemberInfo member)
        {
            if (!IsAlive(target) || member == null)
                return null;

            try
            {
                if (member is FieldInfo field)
                    return field.GetValue(target);
                if (member is PropertyInfo property && property.CanRead)
                    return property.GetValue(target, null);
            }
            catch
            {
            }

            return null;
        }

        private static bool WriteMember(object target, MemberInfo member, object value)
        {
            if (!IsAlive(target) || member == null)
                return false;

            try
            {
                if (member is FieldInfo field)
                {
                    if (field.IsInitOnly || field.IsLiteral || field.IsStatic)
                        return false;
                    field.SetValue(target, value);
                    return true;
                }

                if (member is PropertyInfo property &&
                    property.CanWrite &&
                    property.GetIndexParameters().Length == 0)
                {
                    property.SetValue(target, value, null);
                    return true;
                }
            }
            catch
            {
            }

            return false;
        }

        private static bool IsNullLike(object value)
        {
            if (value == null)
                return true;

            if (value is UnityEngine.Object unityObject)
                return unityObject == null;

            return false;
        }

        private static bool IsAlive(object value)
        {
            if (value == null)
                return false;

            if (value is UnityEngine.Object unityObject)
                return unityObject != null;

            return true;
        }
    }

    internal static class PufferSmokePikminEffectGuard
    {
        public static void Postfix(PufferAI __instance)
        {
            if (__instance == null)
                return;

            int removed = 0;
            HashSet<GameObject> candidates = new HashSet<GameObject>();

            // The nightly LethalMin build injects a Pikmin effect trigger into the
            // Puffer's smoke prefab. Inspect smoke-named GameObject/Component fields
            // plus smoke-named children so this stays resilient to field-name changes.
            foreach (FieldInfo field in typeof(PufferAI).GetFields(
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
            {
                string fieldName = field.Name ?? string.Empty;
                if (fieldName.IndexOf("smoke", StringComparison.OrdinalIgnoreCase) < 0 &&
                    fieldName.IndexOf("puff", StringComparison.OrdinalIgnoreCase) < 0)
                    continue;

                object value;
                try
                {
                    value = field.GetValue(__instance);
                }
                catch
                {
                    continue;
                }

                if (value is GameObject go && go != null)
                    candidates.Add(go);
                else if (value is Component component && component != null)
                    candidates.Add(component.gameObject);
            }

            foreach (Transform child in __instance.GetComponentsInChildren<Transform>(true))
            {
                if (child == null || child.gameObject == null)
                    continue;

                string name = child.name ?? string.Empty;
                if (name.IndexOf("smoke", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    name.IndexOf("puff", StringComparison.OrdinalIgnoreCase) >= 0)
                    candidates.Add(child.gameObject);
            }

            foreach (GameObject candidate in candidates)
                removed += StripLethalMinEffectTriggers(candidate);

            if (removed > 0)
            {
                Plugin.Log.LogInfo(
                    $"[PufferPikminGuard] Removed {removed} LethalMin Pikmin effect-trigger component(s) from Puffer smoke. Player/vanilla Puffer behavior remains intact.");
            }
            else
            {
                Plugin.Log.LogWarning(
                    "[PufferPikminGuard] No LethalMin Pikmin effect-trigger component was found on Puffer smoke. " +
                    "If Pikmin are still affected, capture a fresh log for a narrower runtime patch.");
            }
        }

        private static int StripLethalMinEffectTriggers(GameObject root)
        {
            if (root == null)
                return 0;

            int removed = 0;
            MonoBehaviour[] behaviours = root.GetComponentsInChildren<MonoBehaviour>(true);
            foreach (MonoBehaviour behaviour in behaviours)
            {
                if (behaviour == null)
                    continue;

                Type type = behaviour.GetType();
                string fullName = type.FullName ?? type.Name ?? string.Empty;
                string assemblyName = type.Assembly.GetName().Name ?? string.Empty;

                bool belongsToLethalMin =
                    fullName.IndexOf("LethalMin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    assemblyName.IndexOf("LethalMin", StringComparison.OrdinalIgnoreCase) >= 0;

                bool isEffectTrigger =
                    fullName.IndexOf("Effect", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    fullName.IndexOf("Trigger", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    fullName.IndexOf("Hazard", StringComparison.OrdinalIgnoreCase) >= 0;

                if (!belongsToLethalMin || !isEffectTrigger)
                    continue;

                Plugin.Log.LogInfo(
                    $"[PufferPikminGuard] Removing {fullName} from smoke object '{behaviour.gameObject.name}'.");
                UnityEngine.Object.Destroy(behaviour);
                removed++;
            }

            return removed;
        }
    }

    internal static class LethalModDataLibNullPluginGuard
    {
        internal static MethodInfo RegisterPerTypeMethod;

        public static bool Prefix()
        {
            MethodInfo registerPerType = RegisterPerTypeMethod;
            if (registerPerType == null)
            {
                Plugin.Log.LogError("[LMDLGuard] Per-type registration method is unavailable; allowing original method to run.");
                return true;
            }

            int scannedPlugins = 0;
            int skippedNullInstances = 0;
            int scannedTypes = 0;

            foreach (PluginInfo pluginInfo in Chainloader.PluginInfos.Values)
            {
                if (pluginInfo == null || pluginInfo.Instance == null)
                {
                    skippedNullInstances++;
                    string skippedGuid = pluginInfo != null && pluginInfo.Metadata != null
                        ? pluginInfo.Metadata.GUID
                        : "<unknown>";
                    Plugin.Log.LogWarning(
                        $"[LMDLGuard] Skipping Chainloader PluginInfo with null Instance: {skippedGuid}");
                    continue;
                }

                string guid = pluginInfo.Metadata != null && !string.IsNullOrWhiteSpace(pluginInfo.Metadata.GUID)
                    ? pluginInfo.Metadata.GUID
                    : "<unknown>";

                Assembly assembly = pluginInfo.Instance.GetType().Assembly;
                IEnumerable<Type> types;
                try
                {
                    types = assembly.GetTypes();
                }
                catch (ReflectionTypeLoadException ex)
                {
                    types = ex.Types.Where(t => t != null);
                    Plugin.Log.LogWarning(
                        $"[LMDLGuard] Partial type-load failure while scanning {guid}; continuing with loadable types.");
                }
                catch (Exception ex)
                {
                    Plugin.Log.LogWarning(
                        $"[LMDLGuard] Could not enumerate types for {guid}: {ex.GetType().Name}: {ex.Message}");
                    continue;
                }

                scannedPlugins++;
                foreach (Type type in types)
                {
                    if (type == null)
                        continue;

                    try
                    {
                        registerPerType.Invoke(null, new object[] { guid, type, null, null });
                        scannedTypes++;
                    }
                    catch (TargetInvocationException ex)
                    {
                        Exception inner = ex.InnerException ?? ex;
                        Plugin.Log.LogError(
                            $"[LMDLGuard] Per-type registration failed for {guid}/{type.FullName}: {inner.GetType().Name}: {inner.Message}");
                    }
                    catch (Exception ex)
                    {
                        Plugin.Log.LogError(
                            $"[LMDLGuard] Per-type registration failed for {guid}/{type.FullName}: {ex.GetType().Name}: {ex.Message}");
                    }
                }
            }

            Plugin.Log.LogInfo(
                $"[LMDLGuard] Safe ModDataAttribute scan completed: plugins={scannedPlugins}, types={scannedTypes}, nullInstancesSkipped={skippedNullInstances}.");

            return false;
        }
    }

    internal static class EnemyScanPatch
    {
        public static bool Prefix(ref string __result)
        {
            EnemyAI[] found = UnityEngine.Object.FindObjectsOfType<EnemyAI>();
            var groups = found
                .Where(ai => ai != null && ai.enemyType != null)
                .GroupBy(ai =>
                {
                    string name = ai.enemyType.enemyName;
                    return string.IsNullOrWhiteSpace(name) ? ai.GetType().Name : name;
                })
                .OrderBy(g => g.Key, StringComparer.OrdinalIgnoreCase)
                .ToList();

            if (groups.Count == 0)
            {
                __result = "No Enemies Found.\n\n";
                return false;
            }

            StringBuilder sb = new StringBuilder();
            foreach (var group in groups)
            {
                sb.Append(group.Key);
                sb.Append(": ");
                sb.AppendLine(group.Count().ToString());
            }

            sb.AppendLine();
            __result = sb.ToString();
            return false;
        }
    }

    [HarmonyPatch]
    internal static class NaturalScrapFilterPatches
    {
        private static readonly HashSet<string> ExcludedNaturalScrapNames =
            new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            {
                "Coin",
                "Crisp Dollar Bill",
                "Wayfarer's Wallet",
                "Credit Pad 100cc",
                "Credit Pad 500cc",
                "Credit Pad 1000cc"
            };

        internal sealed class RemovedEntry
        {
            internal int Index;
            internal SpawnableItemWithRarity Entry;
        }

        [HarmonyPatch(typeof(RoundManager), "SpawnScrapInLevel")]
        [HarmonyPrefix]
        [HarmonyPriority(Priority.Last)]
        private static void SpawnScrapInLevelPrefix(RoundManager __instance, ref List<RemovedEntry> __state)
        {
            __state = new List<RemovedEntry>();

            SelectableLevel level = __instance != null ? __instance.currentLevel : null;
            if (level == null || level.spawnableScrap == null)
                return;

            for (int i = level.spawnableScrap.Count - 1; i >= 0; i--)
            {
                SpawnableItemWithRarity candidate = level.spawnableScrap[i];
                Item item = candidate != null ? candidate.spawnableItem : null;
                if (item == null || !ExcludedNaturalScrapNames.Contains(item.itemName))
                    continue;

                __state.Add(new RemovedEntry { Index = i, Entry = candidate });
                level.spawnableScrap.RemoveAt(i);
            }

            if (__state.Count > 0)
            {
                string removed = string.Join(
                    ", ",
                    __state
                        .OrderBy(x => x.Index)
                        .Select(x => $"{x.Entry.spawnableItem.itemName}(rarity={x.Entry.rarity})"));

                Plugin.Log.LogInfo(
                    $"[ScrapFilter] Excluded from natural scrap generation on {level.PlanetName}: {removed}. " +
                    "The items remain registered, so dedicated CodeRebirth mechanics can still spawn/use them.");
            }
        }

        [HarmonyPatch(typeof(RoundManager), "SpawnScrapInLevel")]
        [HarmonyPostfix]
        [HarmonyPriority(Priority.First)]
        private static void SpawnScrapInLevelPostfix(RoundManager __instance, List<RemovedEntry> __state)
        {
            SelectableLevel level = __instance != null ? __instance.currentLevel : null;
            if (level == null || level.spawnableScrap == null || __state == null || __state.Count == 0)
                return;

            foreach (RemovedEntry removed in __state.OrderBy(x => x.Index))
            {
                int index = Mathf.Clamp(removed.Index, 0, level.spawnableScrap.Count);
                level.spawnableScrap.Insert(index, removed.Entry);
            }
        }
    }

    [HarmonyPatch]
    internal static class NaturalMapObjectFilterPatches
    {
        private static readonly HashSet<string> ExcludedCurrencyNames =
            new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            {
                "Coin",
                "Crisp Dollar Bill",
                "Wayfarer's Wallet",
                "Credit Pad 100cc",
                "Credit Pad 500cc",
                "Credit Pad 1000cc"
            };

        internal sealed class FilterState
        {
            internal SpawnableMapObject[] LegacyMapObjects;
            internal IndoorMapHazard[] IndoorHazards;
        }

        [HarmonyPatch(typeof(RoundManager), "SpawnMapObjects")]
        [HarmonyPrefix]
        [HarmonyPriority(Priority.Last)]
        private static void SpawnMapObjectsPrefix(RoundManager __instance, ref FilterState __state)
        {
            __state = null;

            SelectableLevel level = __instance != null ? __instance.currentLevel : null;
            if (level == null)
                return;

            FilterState state = new FilterState();
            List<string> removed = new List<string>();

            // V81's active hazard path uses IndoorMapHazard[].
            if (level.indoorMapHazards != null && level.indoorMapHazards.Length > 0)
            {
                IndoorMapHazard[] originalHazards = level.indoorMapHazards;
                List<IndoorMapHazard> keptHazards = new List<IndoorMapHazard>(originalHazards.Length);

                foreach (IndoorMapHazard entry in originalHazards)
                {
                    GameObject prefab = entry != null && entry.hazardType != null
                        ? entry.hazardType.prefabToSpawn
                        : null;

                    if (ShouldSuppress(prefab, out string reason))
                    {
                        removed.Add(reason);
                        continue;
                    }

                    keptHazards.Add(entry);
                }

                if (keptHazards.Count != originalHazards.Length)
                {
                    state.IndoorHazards = originalHazards;
                    level.indoorMapHazards = keptHazards.ToArray();
                }
            }

            // Keep the legacy SpawnableMapObject[] path covered as well for mods/moons that still use it.
            if (level.spawnableMapObjects != null && level.spawnableMapObjects.Length > 0)
            {
                SpawnableMapObject[] originalLegacy = level.spawnableMapObjects;
                List<SpawnableMapObject> keptLegacy = new List<SpawnableMapObject>(originalLegacy.Length);

                foreach (SpawnableMapObject entry in originalLegacy)
                {
                    GameObject prefab = entry != null ? entry.prefabToSpawn : null;
                    if (ShouldSuppress(prefab, out string reason))
                    {
                        removed.Add(reason);
                        continue;
                    }

                    keptLegacy.Add(entry);
                }

                if (keptLegacy.Count != originalLegacy.Length)
                {
                    state.LegacyMapObjects = originalLegacy;
                    level.spawnableMapObjects = keptLegacy.ToArray();
                }
            }

            if (state.IndoorHazards == null && state.LegacyMapObjects == null)
                return;

            __state = state;
            Plugin.Log.LogInfo(
                "[MapObjectFilter] Suppressed natural dungeon map-object spawns for this generation: " +
                string.Join(", ", removed.Distinct(StringComparer.OrdinalIgnoreCase)) +
                ". Dedicated CodeRebirth item/enemy mechanics remain registered.");
        }

        [HarmonyPatch(typeof(RoundManager), "SpawnMapObjects")]
        [HarmonyPostfix]
        [HarmonyPriority(Priority.First)]
        private static void SpawnMapObjectsPostfix(RoundManager __instance, FilterState __state)
        {
            if (__state == null)
                return;

            SelectableLevel level = __instance != null ? __instance.currentLevel : null;
            if (level == null)
                return;

            if (__state.IndoorHazards != null)
                level.indoorMapHazards = __state.IndoorHazards;

            if (__state.LegacyMapObjects != null)
                level.spawnableMapObjects = __state.LegacyMapObjects;
        }

        private static bool ShouldSuppress(GameObject prefab, out string reason)
        {
            reason = string.Empty;
            if (prefab == null)
                return false;

            string prefabName = prefab.name ?? string.Empty;
            string normalizedPrefabName = Normalize(prefabName);

            if (string.Equals(normalizedPrefabName, "flashturret", StringComparison.OrdinalIgnoreCase))
            {
                reason = "Flash Turret";
                return true;
            }

            if (normalizedPrefabName == "coin" ||
                normalizedPrefabName.Contains("dollarbill") ||
                normalizedPrefabName.Contains("wayfarer") ||
                normalizedPrefabName == "wallet")
            {
                reason = prefabName;
                return true;
            }

            GrabbableObject grabbable = prefab.GetComponentInChildren<GrabbableObject>(true);
            if (grabbable != null &&
                grabbable.itemProperties != null &&
                ExcludedCurrencyNames.Contains(grabbable.itemProperties.itemName))
            {
                reason = grabbable.itemProperties.itemName;
                return true;
            }

            ScanNodeProperties[] scanNodes = prefab.GetComponentsInChildren<ScanNodeProperties>(true);
            foreach (ScanNodeProperties scan in scanNodes)
            {
                if (scan == null)
                    continue;

                string header = scan.headerText ?? string.Empty;
                if (ExcludedCurrencyNames.Contains(header))
                {
                    reason = header;
                    return true;
                }

                if (string.Equals(Normalize(header), "flashturret", StringComparison.OrdinalIgnoreCase))
                {
                    reason = "Flash Turret";
                    return true;
                }
            }

            return false;
        }

        private static string Normalize(string value)
        {
            if (string.IsNullOrEmpty(value))
                return string.Empty;

            return new string(value.Where(char.IsLetterOrDigit).ToArray()).ToLowerInvariant();
        }
    }

    internal static class CodeRebirthKillContext
    {
        [ThreadStatic]
        private static int _depth;

        public static void Enter()
        {
            _depth++;
        }

        public static Exception Exit(Exception __exception)
        {
            if (_depth > 0)
                _depth--;

            return __exception;
        }

        public static bool EnemyKillPrefix(EnemyAI __instance)
        {
            if (_depth <= 0 || !IsPikmin(__instance))
                return true;

            string enemyName = __instance != null && __instance.enemyType != null
                ? __instance.enemyType.enemyName
                : __instance?.GetType().FullName ?? "<unknown>";

            Plugin.Log.LogWarning(
                $"[PikminCraneShield] Blocked CodeRebirth kill RPC against {enemyName}. " +
                "LethalMin crane/CodeRebirth interaction toggles remain configured false.");
            return false;
        }

        private static bool IsPikmin(EnemyAI enemy)
        {
            if (enemy == null)
                return false;

            string enemyName = enemy.enemyType != null ? enemy.enemyType.enemyName : string.Empty;
            if (string.Equals(enemyName, "Pikmin", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(enemyName, "Puffmin", StringComparison.OrdinalIgnoreCase))
                return true;

            string typeName = enemy.GetType().FullName ?? enemy.GetType().Name;
            return typeName.IndexOf("Pikmin", StringComparison.OrdinalIgnoreCase) >= 0 ||
                   typeName.IndexOf("Puffmin", StringComparison.OrdinalIgnoreCase) >= 0;
        }
    }

    [HarmonyPatch]
    internal static class ShipDoorPatches
    {
        private static bool? _lastObservedClosed;
        private static bool _failsafeWasActive;

        [HarmonyPatch(typeof(HangarShipDoor), nameof(HangarShipDoor.Update))]
        [HarmonyPostfix]
        [HarmonyPriority(Priority.Last)]
        private static void HangarShipDoorUpdatePostfix(HangarShipDoor __instance)
        {
            StartOfRound round = StartOfRound.Instance;
            if (round == null)
                return;

            bool closed = round.hangarDoorsClosed;
            if (!_lastObservedClosed.HasValue || _lastObservedClosed.Value != closed)
            {
                CountLivingPlayers(round, out int living, out int livingInside);
                Plugin.Log.LogWarning(
                    $"[DoorAudit] Hangar state changed -> {(closed ? "CLOSED" : "OPEN")}; " +
                    $"doorPower={__instance.doorPower:0.000}; landed={round.shipHasLanded}; " +
                    $"leaving={round.shipIsLeaving}; living={living}; livingInsideShip={livingInside}");
                _lastObservedClosed = closed;
            }

            if (!closed || !round.shipHasLanded || round.shipIsLeaving || round.inShipPhase)
            {
                _failsafeWasActive = false;
                return;
            }

            CountLivingPlayers(round, out int livingPlayers, out int livingInsideShip);

            if (livingPlayers == 0)
            {
                _failsafeWasActive = false;
                return;
            }

            if (livingInsideShip > 0)
            {
                __instance.doorPower = 1f;

                if (_failsafeWasActive)
                {
                    Plugin.Log.LogInfo(
                        "[DoorFailsafe] A living player is inside the ship again; hydraulic power freeze restored to 100%.");
                    _failsafeWasActive = false;
                }

                return;
            }

            if (!_failsafeWasActive)
            {
                Plugin.Log.LogWarning(
                    $"[DoorFailsafe] All {livingPlayers} living player(s) are outside while the landed ship door is closed. " +
                    $"Allowing vanilla hydraulic countdown from {__instance.doorPower * 100f:0.0}% to prevent a permanent lockout.");
                _failsafeWasActive = true;
            }
        }

        private static void CountLivingPlayers(StartOfRound round, out int living, out int livingInsideShip)
        {
            living = 0;
            livingInsideShip = 0;

            PlayerControllerB[] players = round.allPlayerScripts;
            if (players == null)
                return;

            for (int i = 0; i < players.Length; i++)
            {
                PlayerControllerB player = players[i];
                if (player == null || !player.isPlayerControlled || player.isPlayerDead)
                    continue;

                living++;

                bool inside = player.isInHangarShipRoom;
                if (!inside && round.shipInnerRoomBounds != null)
                    inside = round.shipInnerRoomBounds.bounds.Contains(player.transform.position);

                if (inside)
                    livingInsideShip++;
            }
        }

        [HarmonyPatch(typeof(HangarShipDoor), nameof(HangarShipDoor.SetDoorClosed))]
        [HarmonyPrefix]
        private static void SetDoorClosedPrefix(HangarShipDoor __instance)
        {
            Plugin.Log.LogWarning(
                $"[DoorAudit] HangarShipDoor.SetDoorClosed called; currentPower={__instance.doorPower:0.000}\n" +
                $"Caller stack:\n{new StackTrace(1, false)}");
        }

        [HarmonyPatch(typeof(HangarShipDoor), nameof(HangarShipDoor.SetDoorOpen))]
        [HarmonyPrefix]
        private static void SetDoorOpenPrefix(HangarShipDoor __instance)
        {
            Plugin.Log.LogInfo(
                $"[DoorAudit] HangarShipDoor.SetDoorOpen called; currentPower={__instance.doorPower:0.000}\n" +
                $"Caller stack:\n{new StackTrace(1, false)}");
        }

        [HarmonyPatch(typeof(HangarShipDoor), nameof(HangarShipDoor.PlayDoorAnimation))]
        [HarmonyPrefix]
        private static void PlayDoorAnimationPrefix(HangarShipDoor __instance, bool closed)
        {
            Plugin.Log.LogWarning(
                $"[DoorAudit] HangarShipDoor.PlayDoorAnimation(closed={closed}) called; " +
                $"buttonsEnabled={__instance.buttonsEnabled}; currentPower={__instance.doorPower:0.000}\n" +
                $"Caller stack:\n{new StackTrace(1, false)}");
        }

        [HarmonyPatch]
        private static class ShipDoorButtonInteractionAudit
        {
            private static MethodBase TargetMethod()
            {
                return AccessTools.Method(typeof(InteractTrigger), nameof(InteractTrigger.Interact), new Type[] { typeof(Transform) });
            }

            private static void Prefix(InteractTrigger __instance, Transform playerTransform)
            {
                if (__instance == null || __instance.transform == null)
                    return;

                Transform parent = __instance.transform.parent;
                string parentName = parent != null ? parent.name : string.Empty;
                if (!string.Equals(parentName, "StartButton", StringComparison.Ordinal) &&
                    !string.Equals(parentName, "StopButton", StringComparison.Ordinal))
                    return;

                PlayerControllerB player = playerTransform != null
                    ? playerTransform.GetComponentInParent<PlayerControllerB>()
                    : null;

                string playerInfo = player != null
                    ? $"clientId={player.playerClientId}, controlled={player.isPlayerControlled}, dead={player.isPlayerDead}, inHangar={player.isInHangarShipRoom}"
                    : $"transform={playerTransform?.name ?? "<null>"}";

                Plugin.Log.LogWarning(
                    $"[DoorAudit] Ship door button interaction: triggerParent={parentName}; {playerInfo}\n" +
                    $"Caller stack:\n{new StackTrace(1, false)}");
            }
        }
    }
}
