using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Bootstrap;
using HarmonyLib;
using UnityEngine;

namespace S142AKDiagScrapPlacement
{
    [BepInPlugin(Guid, "S1.42AK-SCRAPDIAG1 Scrap Placement Diagnostic", "1.0.0")]
    [BepInDependency(SelectionGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(S139Guid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string Guid = "tendas.lethalcompany.s142akdiagscrapplacement";
        internal const string SelectionGuid = "tendas.lethalcompany.s142ajdiag1officeselection";
        internal const string S139Guid = "tendas.s139.compatibilityfixes";

        private const float SnapshotADelaySeconds = 16f;
        private const float SnapshotBDelaySeconds = 4f;
        private const float SupportRayStartOffset = 0.25f;
        private const float SupportRayDistance = 3f;

        private const BindingFlags InstanceDeclared =
            BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        private const BindingFlags StaticDeclared =
            BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;

        private static Plugin self;
        private static bool captureScheduled;
        private Harmony harmony;

        private void Awake()
        {
            self = this;

            try
            {
                RequireDependency(SelectionGuid);
                RequireDependency(S139Guid);

                MethodInfo target = typeof(RoundManager).GetMethod(
                    "SpawnScrapInLevel",
                    InstanceDeclared,
                    null,
                    Type.EmptyTypes,
                    null);

                Require(
                    target != null &&
                    target.DeclaringType == typeof(RoundManager) &&
                    target.Name == "SpawnScrapInLevel" &&
                    !target.IsStatic &&
                    target.GetParameters().Length == 0 &&
                    target.ReturnType == typeof(void) &&
                    target.GetMethodBody() != null,
                    "Exact declared RoundManager.SpawnScrapInLevel() contract mismatch");

                Patches prior = Harmony.GetPatchInfo(target);
                Require(
                    prior != null && prior.Postfixes.Count(p => p.owner == S139Guid) == 1,
                    "Accepted S139 SpawnScrapInLevel postfix is not uniquely installed");

                MethodInfo postfix = typeof(Plugin).GetMethod(nameof(Postfix), StaticDeclared);
                Require(
                    postfix != null &&
                    postfix.DeclaringType == typeof(Plugin) &&
                    postfix.IsStatic &&
                    postfix.ReturnType == typeof(void),
                    "Diagnostic postfix method contract mismatch");

                harmony = new Harmony(Guid);
                harmony.Patch(
                    target,
                    postfix: new HarmonyMethod(postfix)
                    {
                        after = new[] { S139Guid },
                        priority = Priority.Last
                    });

                Patches installed = Harmony.GetPatchInfo(target);
                Require(installed != null, "Harmony patch metadata unavailable after installation");

                Patch ours = installed.Postfixes.SingleOrDefault(p => p.owner == Guid);
                Require(
                    ours != null &&
                    ours.after != null &&
                    ours.after.Contains(S139Guid) &&
                    ours.priority == Priority.Last,
                    "Diagnostic postfix ownership/order declaration mismatch");

                Logger.LogInfo("[ScrapPlacementDiag] ARMED exact RoundManager.SpawnScrapInLevel read-only postfix");
            }
            catch (Exception ex)
            {
                harmony?.UnpatchSelf();
                Logger.LogError("[ScrapPlacementDiag] REFUSED " + ex);
            }
        }

        private static void RequireDependency(string guid)
        {
            Require(
                Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info) &&
                info != null &&
                info.Instance != null,
                "Required dependency is not loaded: " + guid);
        }

        private static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidOperationException(message);
        }

        // The only Harmony interception in this plugin.
        // It performs no scan and mutates no gameplay/network state; it only schedules bounded observation.
        private static void Postfix()
        {
            if (self == null || captureScheduled)
                return;

            captureScheduled = true;

            try
            {
                self.StartCoroutine(self.CapturePlacementSnapshots());
            }
            catch (Exception ex)
            {
                captureScheduled = false;
                self.Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE failed to schedule snapshots: " + ex);
            }
        }

        private IEnumerator CapturePlacementSnapshots()
        {
            yield return new WaitForSecondsRealtime(SnapshotADelaySeconds);

            List<GrabbableObject> snapshotA;
            try
            {
                snapshotA = FindScrapObjects();
                Logger.LogInfo("[ScrapPlacementDiag] SNAPSHOT A count=" + snapshotA.Count);
            }
            catch (Exception ex)
            {
                captureScheduled = false;
                Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE snapshot A failed: " + ex);
                yield break;
            }

            yield return new WaitForSecondsRealtime(SnapshotBDelaySeconds);

            List<GrabbableObject> snapshotB;
            try
            {
                snapshotB = FindScrapObjects();
                Logger.LogInfo("[ScrapPlacementDiag] SNAPSHOT B count=" + snapshotB.Count);
            }
            catch (Exception ex)
            {
                captureScheduled = false;
                Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE snapshot B failed: " + ex);
                yield break;
            }

            HashSet<int> idsA = new HashSet<int>(snapshotA.Select(x => x.GetInstanceID()));
            HashSet<int> idsB = new HashSet<int>(snapshotB.Select(x => x.GetInstanceID()));

            if (!idsA.SetEquals(idsB))
            {
                captureScheduled = false;
                Logger.LogWarning(
                    "[ScrapPlacementDiag] INCONCLUSIVE unstable spawned set A=" +
                    idsA.Count + " B=" + idsB.Count);
                yield break;
            }

            Logger.LogInfo("[ScrapPlacementDiag] STABLE id-set count=" + snapshotB.Count);

            EntranceTeleport[] anchors;
            try
            {
                anchors = UnityEngine.Object.FindObjectsOfType<EntranceTeleport>()
                    .Where(x => x != null)
                    .OrderBy(x => x.GetInstanceID())
                    .ToArray();
            }
            catch (Exception ex)
            {
                captureScheduled = false;
                Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE anchor scan failed: " + ex);
                yield break;
            }

            if (anchors.Length == 0)
            {
                captureScheduled = false;
                Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE no EntranceTeleport anchors");
                yield break;
            }

            try
            {
                foreach (EntranceTeleport anchor in anchors)
                {
                    Logger.LogInfo(
                        "[ScrapPlacementDiag][ANCHOR] name=" + Quote(anchor.gameObject.name) +
                        " path=" + Quote(TransformPath(anchor.transform)) +
                        " pos=" + Vector(anchor.transform.position));
                }

                foreach (GrabbableObject scrap in snapshotB)
                    LogScrap(scrap, anchors);

                Logger.LogInfo("[ScrapPlacementDiag] COMPLETE stable=" + snapshotB.Count);
            }
            catch (Exception ex)
            {
                Logger.LogWarning("[ScrapPlacementDiag] INCONCLUSIVE placement logging failed: " + ex);
            }

            captureScheduled = false;
        }

        private static List<GrabbableObject> FindScrapObjects()
        {
            return UnityEngine.Object.FindObjectsOfType<GrabbableObject>()
                .Where(x =>
                    x != null &&
                    x.itemProperties != null &&
                    x.itemProperties.isScrap)
                .OrderBy(x => x.GetInstanceID())
                .ToList();
        }

        private void LogScrap(GrabbableObject scrap, EntranceTeleport[] anchors)
        {
            Require(scrap != null, "Stable scrap object became null before logging");
            Require(scrap.itemProperties != null, "Stable scrap object lost itemProperties before logging");

            Vector3 position = scrap.transform.position;

            EntranceTeleport nearest = anchors
                .OrderBy(x => Mathf.Abs(x.transform.position.y - position.y))
                .ThenBy(x => x.GetInstanceID())
                .First();

            float deltaY = Mathf.Abs(nearest.transform.position.y - position.y);
            Collider support = FindSupportCollider(scrap);

            Logger.LogInfo(
                "[ScrapPlacementDiag][ITEM] id=" + scrap.GetInstanceID() +
                " item=" + Quote(scrap.itemProperties.itemName) +
                " gameObject=" + Quote(scrap.gameObject.name) +
                " scrapValue=" + scrap.scrapValue +
                " pos=" + Vector(position) +
                " parentPath=" + Quote(TransformPath(scrap.transform)) +
                " nearestAnchorName=" + Quote(nearest.gameObject.name) +
                " nearestAnchorPath=" + Quote(TransformPath(nearest.transform)) +
                " nearestAnchorPos=" + Vector(nearest.transform.position) +
                " deltaY=" + deltaY.ToString("F3", CultureInfo.InvariantCulture) +
                " supportCollider=" + Quote(support == null ? "<none>" : support.gameObject.name) +
                " supportPath=" + Quote(support == null ? "<none>" : TransformPath(support.transform)));
        }

        private static Collider FindSupportCollider(GrabbableObject scrap)
        {
            Vector3 origin = scrap.transform.position + Vector3.up * SupportRayStartOffset;

            RaycastHit[] hits = Physics.RaycastAll(
                origin,
                Vector3.down,
                SupportRayDistance,
                Physics.DefaultRaycastLayers,
                QueryTriggerInteraction.Ignore);

            Array.Sort(hits, (a, b) => a.distance.CompareTo(b.distance));

            foreach (RaycastHit hit in hits)
            {
                Collider collider = hit.collider;
                if (collider == null)
                    continue;

                GrabbableObject owner = collider.GetComponentInParent<GrabbableObject>();
                if (owner == scrap)
                    continue;

                return collider;
            }

            return null;
        }

        private static string TransformPath(Transform transform)
        {
            if (transform == null)
                return "<null>";

            var parts = new Stack<string>();
            Transform current = transform;

            while (current != null)
            {
                parts.Push(current.name ?? "<unnamed>");
                current = current.parent;
            }

            return string.Join("/", parts);
        }

        private static string Vector(Vector3 value)
        {
            return string.Format(
                CultureInfo.InvariantCulture,
                "({0:F3},{1:F3},{2:F3})",
                value.x,
                value.y,
                value.z);
        }

        private static string Quote(string value)
        {
            string safe = (value ?? "<null>")
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\r", "\\r")
                .Replace("\n", "\\n");

            return "\"" + safe + "\"";
        }
    }
}
