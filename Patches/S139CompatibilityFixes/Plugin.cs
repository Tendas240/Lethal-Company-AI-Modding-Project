using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using BepInEx;
using BepInEx.Logging;
using GameNetcodeStuff;
using HarmonyLib;
using UnityEngine;

namespace S139CompatibilityFixes
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency("299792458.EnemyScan")]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "tendas.s139.compatibilityfixes";
        public const string PluginName = "S1.39 Compatibility Fixes";
        public const string PluginVersion = "1.0.0";

        internal static ManualLogSource Log;
        internal static Harmony Harmony;

        private void Awake()
        {
            Log = Logger;
            Harmony = new Harmony(PluginGuid);

            Harmony.PatchAll(typeof(ShipDoorPatches));
            Harmony.PatchAll(typeof(NaturalScrapFilterPatches));
            Harmony.PatchAll(typeof(NaturalMapObjectFilterPatches));

            PatchEnemyScan();
            PatchCodeRebirthPikminKillShield();

            Logger.LogInfo(
                "S1.39 Compatibility Fixes loaded. Ship-door anti-lockout, complete EnemyScan output, " +
                "natural CodeRebirth currency/map-object filtering, Flash Turret suppression, and " +
                "CodeRebirth kill-RPC Pikmin protection are active.");
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
