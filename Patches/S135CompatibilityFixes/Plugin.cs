using System;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using BepInEx;
using BepInEx.Logging;
using GameNetcodeStuff;
using HarmonyLib;
using UnityEngine;

namespace S135CompatibilityFixes
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency("299792458.EnemyScan")]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "tendas.s135.compatibilityfixes";
        public const string PluginName = "S1.35 Compatibility Fixes";
        public const string PluginVersion = "1.0.0";

        internal static ManualLogSource Log;
        internal static Harmony Harmony;

        private void Awake()
        {
            Log = Logger;
            Harmony = new Harmony(PluginGuid);
            Harmony.PatchAll(typeof(ShipDoorPatches));

            MethodInfo enemyScanBuilder = AccessTools.Method(
                AccessTools.TypeByName("EnemyScan.EnemyScan"),
                "BuildEnemyCountString");

            if (enemyScanBuilder == null)
            {
                Logger.LogError("[EnemyScanFix] Could not locate EnemyScan.EnemyScan.BuildEnemyCountString; complete enemy listing patch was not applied.");
            }
            else
            {
                Harmony.Patch(
                    enemyScanBuilder,
                    prefix: new HarmonyMethod(typeof(EnemyScanPatch), nameof(EnemyScanPatch.Prefix)));
                Logger.LogInfo("[EnemyScanFix] Patched EnemyScan to list every active EnemyAI regardless of ScanNodeProperties.");
            }

            Logger.LogInfo(
                "S1.35 Compatibility Fixes loaded. Ship door power is frozen only while a living player is actually inside the landed ship; " +
                "when all living players are outside, vanilla hydraulic drain/open behavior is preserved.");
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

            // Do not interfere in orbit, while launching/landing, or when the door is already open.
            if (!closed || !round.shipHasLanded || round.shipIsLeaving || round.inShipPhase)
            {
                _failsafeWasActive = false;
                return;
            }

            CountLivingPlayers(round, out int livingPlayers, out int livingInsideShip);

            // No living controlled players: preserve game-over/end-of-round behavior.
            if (livingPlayers == 0)
            {
                _failsafeWasActive = false;
                return;
            }

            if (livingInsideShip > 0)
            {
                // Preserve the intended "door can stay closed indefinitely" behavior while
                // somebody living is actually inside and can operate the ship controls.
                __instance.doorPower = 1f;

                if (_failsafeWasActive)
                {
                    Plugin.Log.LogInfo(
                        "[DoorFailsafe] A living player is inside the ship again; hydraulic power freeze restored to 100%.");
                    _failsafeWasActive = false;
                }

                return;
            }

            // Everyone living is outside. Do not refill doorPower.
            // Vanilla HangarShipDoor.Update has already run this frame and continues its
            // normal ~20 second drain. At zero, the server opens the door automatically.
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
