using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Threading;
using UnityEngine;

namespace S142AKBMAFR1I1
{
    internal sealed class TrackedEnemy
    {
        internal EnemyAI Enemy;
        internal bool Peer;
        internal int NextFrame = -1, OnsetFrame = -1;
        internal long Identity;
        internal string Selection = "SELECTION_STATE_INCONCLUSIVE";
        internal readonly Dictionary<string, WriteSample> Writes = new Dictionary<string, WriteSample>();
    }
    internal sealed class WriteSample
    { internal long Count, LastTick; internal int Emitted; }
    internal sealed class MeshObservation
    {
        internal TrackedEnemy Track;
        internal SkinnedMeshRenderer Target;
        internal string Action;
        internal int BeforeMeshId;
    }
    internal sealed class MaterialObservation
    { internal TrackedEnemy Track; internal Renderer Target; }

    internal static class Observers
    {
        internal const int MaxPeers = 16, MaxOther = 32, MaxRenderers = 16, MaxBones = 256, MaxShapes = 128, MaxActions = 32, MaxTransforms = 512;
        private static readonly Dictionary<int, TrackedEnemy> Tracked = new Dictionary<int, TrackedEnemy>();
        private static long sequence, lastSummary;
        private static bool onset;
        internal static int MainThread;
        internal static bool Ready;

        private static bool Begin()
        {
            if (!Ready) return false;
            Contracts.Require(Thread.CurrentThread.ManagedThreadId == MainThread, "Observer called outside main thread");
            return true;
        }
        private static bool IsPeer(EnemyAI enemy)
        { return enemy.GetType() == Contracts.Janitor || enemy.GetType() == Contracts.SpringMan; }

        private static TrackedEnemy Track(EnemyAI enemy, bool allowOther)
        {
            if (enemy == null) return null;
            int id = enemy.GetInstanceID();
            if (Tracked.TryGetValue(id, out TrackedEnemy prior) && ReferenceEquals(prior.Enemy, enemy)) return prior;
            bool peer = IsPeer(enemy);
            if (!peer && !allowOther) return null;
            Contracts.Require(Tracked.Values.Count(x => x.Peer == peer) < (peer ? MaxPeers : MaxOther), "Tracked instance budget exceeded");
            var entry = new TrackedEnemy { Enemy = enemy, Peer = peer, Identity = ++sequence };
            Tracked[id] = entry;
            return entry;
        }

        private static TrackedEnemy Find(Renderer renderer)
        {
            if (renderer == null) return null;
            TrackedEnemy result = null;
            foreach (TrackedEnemy t in Tracked.Values)
            {
                if (t.Enemy == null || !renderer.transform.IsChildOf(t.Enemy.transform)) continue;
                Contracts.Require(result == null, "Renderer belongs to ambiguous tracked roots");
                result = t;
            }
            return result;
        }

        // __1 is the existing EnemyAI argument; never a ref/out gameplay argument.
        internal static void SelectorPrefix(EnemyAI __1)
        {
            try
            {
                if (!Begin()) return;
                TrackedEnemy t = Track(__1, false);
                if (t != null) t.Selection = "SELECTION_STATE_INCONCLUSIVE";
            }
            catch (Exception ex) { Plugin.Fault("selector-prefix", ex); }
        }

        internal static void Selected(object selected, EnemyAI enemy)
        {
            try
            {
                if (!Begin()) return;
                Contracts.Require(selected != null && Contracts.Definition.IsInstanceOfType(selected), "Selected definition type mismatch");
                bool isDefault = (bool)Contracts.DefaultField.GetValue(selected);
                Contracts.Require(!isDefault, "Non-default selector anchor observed a default definition");
                var asset = selected as UnityEngine.Object;
                Contracts.Require(asset != null, "Selected definition Unity identity missing");
                var actions = (IList)Contracts.Replacements.GetValue(selected);
                Contracts.Require(actions != null && actions.Count <= MaxActions, "Replacement action manifest missing/over budget");
                var manifest = new List<string>();
                foreach (object action in actions)
                {
                    Contracts.Require(action != null && Contracts.Hierarchy.IsInstanceOfType(action), "Action hierarchy contract mismatch");
                    manifest.Add(Text(action.GetType().FullName) + ":" + Text((string)Contracts.HierarchyPath.GetValue(action)));
                }
                TrackedEnemy t = Track(enemy, true);
                Contracts.Require(t != null, "Selected enemy identity missing");
                t.Selection = "SELECTED_NONDEFAULT definitionId=" + asset.GetInstanceID() + " definitionName=" + Text(asset.name)
                    + " definitionType=" + Text(selected.GetType().FullName) + " skinName=" + Text((string)Contracts.SkinName.GetValue(selected))
                    + " IsDefault=false stableKey=NOT_READ";
                Emit("DUSK_SELECTED", t, null, t.Selection + " actions=" + string.Join("|", manifest));
            }
            catch (Exception ex) { Plugin.Fault("selected", ex); }
        }

        internal static void SelectorPostfix(EnemyAI __1)
        {
            try
            {
                if (!Begin()) return;
                TrackedEnemy t = Track(__1, false);
                if (t == null) return;
                Emit("SELECTION_COMPLETE", t, null, t.Selection);
                if (t.Peer)
                {
                    Snapshot(t, "selection-complete");
                    t.NextFrame = Time.frameCount + 1;
                }
            }
            catch (Exception ex) { Plugin.Fault("selector-postfix", ex); }
        }

        internal static void MeshPrefix(object __instance, SkinnedMeshRenderer __0, out MeshObservation __state)
        {
            __state = null;
            try
            {
                if (!Begin()) return;
                TrackedEnemy t = Find(__0);
                if (t == null || !t.Peer) return;
                Contracts.Require(Contracts.MeshAction.IsInstanceOfType(__instance), "Mesh action identity mismatch");
                var replacement = (SkinnedMeshRenderer)Contracts.ReplacementRenderer.GetValue(__instance);
                Contracts.Require(replacement != null, "Replacement renderer missing");
                string action = "action=" + Text(__instance.GetType().FullName) + " HierarchyPath=" + Text((string)Contracts.HierarchyPath.GetValue(__instance));
                var state = new MeshObservation { Track = t, Target = __0, Action = action, BeforeMeshId = __0.sharedMesh == null ? 0 : __0.sharedMesh.GetInstanceID() };
                Emit("MESH_PRE", t, __0, action + " " + MeshFacts(__0, t.Enemy.transform));
                Emit("MESH_REPLACEMENT", t, __0, action + " replacementRenderer=" + replacement.GetInstanceID() + " " + MeshFacts(replacement, t.Enemy.transform));
                Emit("BONE_MAP_PREDICTION", t, __0, BoneMap(__0, replacement, t.Enemy.transform));
                __state = state;
            }
            catch (Exception ex) { Plugin.Fault("mesh-prefix", ex); }
        }

        internal static void MeshPostfix(MeshObservation __state)
        {
            try
            {
                if (!Begin() || __state == null) return;
                MeshObservation s = __state;
                Emit("MESH_POST", s.Track, s.Target, s.Action + " originalMeshId=" + s.BeforeMeshId + " " + MeshFacts(s.Target, s.Track.Enemy.transform));
            }
            catch (Exception ex) { Plugin.Fault("mesh-postfix", ex); }
        }

        internal static void MaterialPrefix(Renderer __0, Material[] __1, int __2, out MaterialObservation __state)
        {
            __state = null;
            try
            {
                if (!Begin()) return;
                TrackedEnemy t = Find(__0);
                if (t == null) return;
                __state = new MaterialObservation { Track = t, Target = __0 };
                var skinned = __0 as SkinnedMeshRenderer;
                string mesh = skinned != null && skinned.sharedMesh != null ? " meshId=" + skinned.sharedMesh.GetInstanceID() + " mesh=" + Text(skinned.sharedMesh.name) + " subMeshCount=" + skinned.sharedMesh.subMeshCount : " mesh=NOT_SKINNED_OR_NULL";
                Emit("MATERIAL_PRE", t, __0, "sourceCount=" + (__1 == null ? -1 : __1.Length) + " requiredCount=" + __2 + mesh + " selection=" + t.Selection);
            }
            catch (Exception ex) { Plugin.Fault("material-prefix", ex); }
        }

        internal static void MaterialPostfix(MaterialObservation __state)
        {
            try
            {
                if (!Begin() || __state == null) return;
                Emit("MATERIAL_POST", __state.Track, __state.Target, "materialCount=" + __state.Target.sharedMaterials.Length + " selection=" + __state.Track.Selection);
            }
            catch (Exception ex) { Plugin.Fault("material-postfix", ex); }
        }

        internal static void BeforeWrite(EnemyAI enemy, SkinnedMeshRenderer renderer, int index, float weight, string callsite)
        {
            try
            {
                if (!Begin()) return;
                Contracts.Require(enemy != null && enemy.GetType() == Contracts.Janitor && index == 0, "Janitor write identity/index drift");
                TrackedEnemy t = Track(enemy, false);
                Contracts.Require(renderer != null && renderer.transform.IsChildOf(enemy.transform), "Janitor write renderer outside tracked root");
                if (!t.Writes.TryGetValue(callsite, out WriteSample sample)) t.Writes[callsite] = sample = new WriteSample();
                sample.Count++;
                long now = Stopwatch.GetTimestamp();
                if (sample.Emitted >= 8 && now - sample.LastTick < Stopwatch.Frequency) return;
                sample.LastTick = now; sample.Emitted++;
                Emit("JANITOR_WRITE", t, renderer, "callsite=" + callsite + " invocationCount=" + sample.Count + " emittedSamples=" + sample.Emitted
                    + " index=" + index + " weight=" + weight.ToString("R", CultureInfo.InvariantCulture) + " selection=" + t.Selection + " " + MeshFacts(renderer, enemy.transform));
            }
            catch (Exception ex) { Plugin.Fault("janitor-write", ex); }
        }

        internal static void Tick()
        {
            try
            {
                if (!Begin()) return;
                int frame = Time.frameCount; long now = Stopwatch.GetTimestamp();
                if (!onset && Interlocked.Read(ref ArrayAnchor.Count) > 0)
                {
                    onset = true;
                    Plugin.Marker("ARRAY_BEGIN", ArrayAnchor.Summary());
                    foreach (TrackedEnemy t in Tracked.Values.Where(x => x.Peer)) t.OnsetFrame = frame + 1;
                }
                foreach (var pair in Tracked.ToArray())
                {
                    TrackedEnemy t = pair.Value;
                    if (t.Enemy == null) { Tracked.Remove(pair.Key); continue; }
                    if (t.NextFrame >= 0 && frame >= t.NextFrame) { t.NextFrame = -1; Snapshot(t, "next-frame"); }
                    if (t.OnsetFrame >= 0 && frame >= t.OnsetFrame) { t.OnsetFrame = -1; Snapshot(t, "array-onset"); }
                }
                if (onset && now - lastSummary >= 5L * Stopwatch.Frequency)
                { lastSummary = now; Plugin.Marker("ARRAY_SUMMARY", ArrayAnchor.Summary()); }
            }
            catch (Exception ex) { Plugin.Fault("main-thread-tick", ex); }
        }

        private static void Snapshot(TrackedEnemy t, string reason)
        {
            Contracts.Require(t.Peer && t.Enemy != null, "Full snapshot requires tracked Janitor/SpringMan root");
            SkinnedMeshRenderer[] renderers = t.Enemy.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            Contracts.Require(renderers.Length <= MaxRenderers, "Renderer subtree budget exceeded");
            Emit("SNAPSHOT_BEGIN", t, null, "reason=" + reason + " rendererCount=" + renderers.Length + " selection=" + t.Selection);
            foreach (SkinnedMeshRenderer r in renderers)
                Emit("RENDERER_SNAPSHOT", t, r, "reason=" + reason + " janitorActionPath=" + (Path(r.transform, t.Enemy.transform) == "Janitor") + " " + MeshFacts(r, t.Enemy.transform));
        }

        private static string MeshFacts(SkinnedMeshRenderer r, Transform root)
        {
            Contracts.Require(r != null, "Renderer no longer exists");
            Mesh mesh = r.sharedMesh; Transform[] bones = r.bones;
            Contracts.Require(bones != null && bones.Length <= MaxBones, "Bone count missing/over budget");
            var names = new List<string>();
            if (mesh != null)
            {
                Contracts.Require(mesh.blendShapeCount <= MaxShapes, "Blendshape count over budget");
                for (int i = 0; i < mesh.blendShapeCount; i++) names.Add(Text(mesh.GetBlendShapeName(i)));
            }
            return "rendererName=" + Text(r.name) + " rendererPath=" + Text(Path(r.transform, root)) + " enabled=" + r.enabled
                + " meshId=" + (mesh == null ? "null" : mesh.GetInstanceID().ToString()) + " meshName=" + Text(mesh == null ? null : mesh.name)
                + " blendShapeCount=" + (mesh == null ? "null" : mesh.blendShapeCount.ToString()) + " blendShapeNames=" + string.Join("|", names)
                + " materialCount=" + r.sharedMaterials.Length + " subMeshCount=" + (mesh == null ? "null" : mesh.subMeshCount.ToString())
                + " rootBone=" + Bone(r.rootBone, root) + " bones=" + string.Join("|", bones.Select(b => Bone(b, root)));
        }

        private static string BoneMap(SkinnedMeshRenderer target, SkinnedMeshRenderer replacement, Transform enemyRoot)
        {
            Transform originalRoot = target.rootBone;
            var lookup = new Dictionary<string, Transform>(StringComparer.Ordinal);
            var pending = new Stack<Transform>();
            if (originalRoot != null)
            {
                Contracts.Require(originalRoot.IsChildOf(enemyRoot), "Bone root outside tracked enemy subtree");
                pending.Push(originalRoot);
            }
            int visited = 0;
            while (pending.Count > 0)
            {
                Contracts.Require(++visited <= MaxTransforms, "Bone subtree budget exceeded");
                Transform node = pending.Pop();
                if (!lookup.ContainsKey(node.name)) lookup.Add(node.name, node);
                Contracts.Require(pending.Count + node.childCount <= MaxTransforms, "Bone traversal queue budget exceeded");
                for (int i = node.childCount - 1; i >= 0; i--) pending.Push(node.GetChild(i));
            }
            Transform[] source = replacement.bones;
            Contracts.Require(source != null && source.Length <= MaxBones, "Replacement bone budget exceeded");
            var mapped = new List<string>(); var unmapped = new List<string>();
            foreach (Transform bone in source)
            {
                string name = bone == null ? null : bone.name;
                if (!string.IsNullOrWhiteSpace(name) && lookup.TryGetValue(name, out Transform found)) mapped.Add(Text(name) + ":" + Bone(found, enemyRoot));
                else unmapped.Add(Text(name) + ":fallback=" + Bone(originalRoot, enemyRoot));
            }
            return "rule=exact-name-first-depth-first mapped=" + string.Join("|", mapped) + " unmapped=" + string.Join("|", unmapped);
        }

        private static string Bone(Transform bone, Transform root)
        { return bone == null ? "null" : Text(bone.name) + ":" + bone.GetInstanceID() + ":" + Text(Path(bone, root)); }

        private static string Path(Transform node, Transform root)
        {
            var parts = new List<string>(); int depth = 0;
            while (node != null && node != root)
            {
                Contracts.Require(++depth <= 64, "Hierarchy depth budget exceeded");
                parts.Add(node.name); node = node.parent;
            }
            parts.Reverse();
            return (node == root ? "" : "OUTSIDE_ROOT/") + string.Join("/", parts);
        }

        private static string Text(string value)
        {
            if (value == null) return "null";
            Contracts.Require(value.Length <= 1024, "String capture budget exceeded");
            return Uri.EscapeDataString(value);
        }

        private static void Emit(string kind, TrackedEnemy t, Renderer renderer, string details)
        {
            EnemyAI enemy = t.Enemy;
            Contracts.Require(enemy != null, "Enemy correlation identity unavailable");
            var network = enemy.NetworkObject;
            string net = network != null && network.IsSpawned ? network.NetworkObjectId.ToString() : "null/unspawned";
            string owner = network != null && network.IsSpawned ? network.OwnerClientId.ToString() : "null/unspawned";
            Plugin.Marker(kind, "track=" + t.Identity + " enemyId=" + enemy.GetInstanceID() + " gameObjectId=" + enemy.gameObject.GetInstanceID()
                + " enemyType=" + Text(enemy.GetType().FullName) + " enemyName=" + Text(enemy.enemyType == null ? null : enemy.enemyType.enemyName)
                + " networkObjectId=" + net + " ownerClientId=" + owner + " rendererId=" + (renderer == null ? "null" : renderer.GetInstanceID().ToString()) + " " + details);
        }
    }
}
