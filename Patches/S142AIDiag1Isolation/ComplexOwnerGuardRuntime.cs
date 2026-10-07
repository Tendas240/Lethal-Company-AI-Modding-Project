using System;
using System.Collections.Generic;
using Unity.Netcode;
using UnityEngine;

namespace S142AIDiag1Isolation
{
    internal static class ComplexOwnerGuardRuntime
    {
        private const int MaxMarkersPerOwner = 8;
        private static readonly Dictionary<string, int> BlockedCounts =
            new Dictionary<string, int>(StringComparer.Ordinal);

        internal static bool AllowExplicitEnemy(EnemyType enemyType, string owner)
        {
            // This is lifecycle-bound spawn handling, not a per-frame scan. Reusing the
            // native indoor quarantine establishes the canonical exact identity triple
            // and leaves the candidate fail-closed if identity resolution is absent.
            DiagnosticIsolation.QuarantineIndoorPool(owner + "/Identity", terminalIdentityCheck: true);
            return DiagnosticIsolation.IsAllowed(enemyType);
        }

        internal static bool IsJllEnemyAllowed(EnemyType enemyType)
        {
            bool allowed = AllowExplicitEnemy(enemyType, "JLL.Components.EnemySpawner.SpawnEnemy");
            if (!allowed)
                LogBlocked("JLL.Components.EnemySpawner.SpawnEnemy", "resolved EnemyType is not exact Shy Guy; returning before cap/power/navmesh/nest/spawn work");
            return allowed;
        }

        internal static bool IsCodeRebirthSpawnerEnemyAllowed(EnemyType enemyType)
        {
            bool allowed = AllowExplicitEnemy(enemyType, "CodeRebirth.src.MiscScripts.EnemyLevelSpawner.SpawnRandomEnemy");
            if (!allowed)
                LogBlocked("CodeRebirth.src.MiscScripts.EnemyLevelSpawner.SpawnRandomEnemy", "weighted EnemyType is not exact Shy Guy; returning null before counters mutate");
            return allowed;
        }

        internal static void LogCodeRebirthFakeSnailBlocked()
        {
            LogBlocked(
                "CodeRebirth.src.Content.Items.FakeSnailCat.Update",
                "fixed RealEnemySnailCat conversion branch skipped before destroyed=true; base item Update remains intact");
        }

        internal static NetworkObjectReference KenjiPermanentPowerOffSpawn(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType)
        {
            return GuardedSpawnEnemyGameObject(
                manager, position, yRot, enemyIndex, enemyType,
                "KenjiLib.Scripts.KLightsEvent.PermanentPowerOffRoutine");
        }

        internal static NetworkObjectReference KenjiTriggerAppySpawn(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType)
        {
            return GuardedSpawnEnemyGameObject(
                manager, position, yRot, enemyIndex, enemyType,
                "KenjiLib.Scripts.KLightsEvent.TriggerAppyEventRoutine");
        }

        internal static NetworkObjectReference ItolibEventfulSpawn(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType)
        {
            return GuardedSpawnEnemyGameObject(
                manager, position, yRot, enemyIndex, enemyType,
                "itolib.Behaviours.Grabbables.EventfulApparatus.HandleDisconnect");
        }

        internal static NetworkObjectReference ItolibTwinSpawn(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType)
        {
            return GuardedSpawnEnemyGameObject(
                manager, position, yRot, enemyIndex, enemyType,
                "itolib.PlayZone.TwinApparatus.HandleDisconnect");
        }

        internal static NetworkObjectReference CodeRebirthXuiSpawn(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType)
        {
            return GuardedSpawnEnemyGameObject(
                manager, position, yRot, enemyIndex, enemyType,
                "CodeRebirth.src.Content.Items.Xui.OnNetworkDespawn");
        }

        private static NetworkObjectReference GuardedSpawnEnemyGameObject(
            RoundManager manager,
            Vector3 position,
            float yRot,
            int enemyIndex,
            EnemyType enemyType,
            string owner)
        {
            if (!AllowExplicitEnemy(enemyType, owner))
            {
                LogBlocked(owner, $"ignored-result SpawnEnemyGameObject denied enemy='{DescribeEnemy(enemyType)}'");
                return default(NetworkObjectReference);
            }

            if (manager == null)
            {
                DiagnosticIsolation.MarkInvalid(owner + ": RoundManager instance was null at guarded spawn call.");
                LogBlocked(owner, "RoundManager instance null; guarded spawn failed closed");
                return default(NetworkObjectReference);
            }

            return manager.SpawnEnemyGameObject(position, yRot, enemyIndex, enemyType);
        }

        internal static void LogBlocked(string owner, string detail)
        {
            owner = string.IsNullOrEmpty(owner) ? "<unknown-owner>" : owner;
            int count;
            BlockedCounts.TryGetValue(owner, out count);
            if (count >= MaxMarkersPerOwner)
                return;

            count++;
            BlockedCounts[owner] = count;
            Plugin.Log.LogWarning(
                $"[DIAG1_OWNER_BLOCKED] owner='{owner}', detail='{detail}', marker={count}/{MaxMarkersPerOwner}.");
        }

        internal static string DescribeEnemy(EnemyType enemyType)
        {
            return enemyType == null ? "<null>" : enemyType.name + "/" + enemyType.enemyName;
        }
    }
}
