using System;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Threading;
using BepInEx;
using HarmonyLib;
using UnityEngine;

namespace S142AKBMAFR1I1
{
    [BepInPlugin(Guid, "S1.42AK-BMAFR1I1 Read-only Attribution Diagnostic", "1.0.0")]
    [BepInDependency("CodeRebirth", "1.6.9")]
    [BepInDependency("com.github.teamxiaolan.dawnlib.dusk", "0.9.25")]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string Guid = "tendas.lethalcompany.s142akbmafr1i1";
        private static Plugin self;
        private static int faulted, records;
        private Harmony harmony;
        private bool subscribed;

        private void Awake()
        {
            self = this;
            Observers.MainThread = Thread.CurrentThread.ManagedThreadId;
            try
            {
                Contracts.Resolve();
                harmony = new Harmony(Guid);
                foreach (MethodInfo target in Contracts.Writes)
                    harmony.Patch(target, transpiler: Hook(typeof(Probes), nameof(Probes.JanitorWrite)));
                harmony.Patch(Contracts.MeshTransfer, prefix: Hook(typeof(Observers), nameof(Observers.MeshPrefix)), postfix: Hook(typeof(Observers), nameof(Observers.MeshPostfix)));
                harmony.Patch(Contracts.Materials, prefix: Hook(typeof(Observers), nameof(Observers.MaterialPrefix)), postfix: Hook(typeof(Observers), nameof(Observers.MaterialPostfix)));
                harmony.Patch(Contracts.Selector, prefix: Hook(typeof(Observers), nameof(Observers.SelectorPrefix)), postfix: Hook(typeof(Observers), nameof(Observers.SelectorPostfix)), transpiler: Hook(typeof(Probes), nameof(Probes.Selector)));
                foreach (MethodInfo target in Contracts.PatchTargets())
                {
                    Patches p = Harmony.GetPatchInfo(target);
                    int expected = target == Contracts.Selector ? 3 : Contracts.Writes.Contains(target) ? 1 : 2;
                    Contracts.Require(p != null && p.Prefixes.Concat(p.Postfixes).Concat(p.Transpilers).Count(x => x.owner == Guid) == expected, "Installed owner/patch count mismatch: " + target.Name);
                }
                Application.logMessageReceivedThreaded += ArrayAnchor.Capture;
                subscribed = true;
                Volatile.Write(ref ArrayAnchor.Active, 1);
                Observers.Ready = true;
                Marker("ARMED", "exact dependencies, declared signatures, IL bodies and seven targets validated; DIAGNOSTIC ONLY / NEVER ACCEPT; selection absence is INCONCLUSIVE");
            }
            catch (Exception ex)
            {
                Observers.Ready = false;
                Volatile.Write(ref ArrayAnchor.Active, 0);
                if (subscribed) { Application.logMessageReceivedThreaded -= ArrayAnchor.Capture; subscribed = false; }
                try { harmony?.UnpatchSelf(); }
                catch (Exception rollback) { SafeLog("[BMAFR1I1] INCONCLUSIVE rollback failure: " + rollback.GetType().Name); }
                SafeLog("[BMAFR1I1] REFUSED TO ARM; normal behavior preserved: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static HarmonyMethod Hook(Type type, string name)
        {
            MethodInfo m = type.GetMethod(name, Contracts.Declared);
            Contracts.Require(m != null && m.IsStatic, "Diagnostic hook missing: " + name);
            return new HarmonyMethod(m) { priority = Priority.Last };
        }

        private void Update() { Observers.Tick(); }

        private void OnDestroy()
        {
            Observers.Ready = false;
            Volatile.Write(ref ArrayAnchor.Active, 0);
            try
            {
                if (subscribed) { Application.logMessageReceivedThreaded -= ArrayAnchor.Capture; subscribed = false; }
                SafeLog("[BMAFR1I1] ARRAY_FINAL " + ArrayAnchor.Summary());
                harmony?.UnpatchSelf();
            }
            catch (Exception ex) { SafeLog("[BMAFR1I1] INCONCLUSIVE teardown: " + ex.GetType().Name); }
        }

        internal static void Marker(string kind, string details)
        {
            if (!Observers.Ready) return;
            Contracts.Require(Thread.CurrentThread.ManagedThreadId == Observers.MainThread, "Marker requires main thread");
            Contracts.Require(++records <= 2048 && details.Length <= 32768, "Diagnostic output budget exceeded");
            DateTime utc = DateTime.UtcNow;
            string line = "[BMAFR1I1] " + kind + " utc=" + utc.ToString("O", CultureInfo.InvariantCulture)
                + " local=" + utc.ToLocalTime().ToString("O", CultureInfo.InvariantCulture) + " mono=" + Stopwatch.GetTimestamp()
                + " frame=" + Time.frameCount + " arrayCount=" + Interlocked.Read(ref ArrayAnchor.Count) + " " + details;
            SafeLog(line);
        }

        internal static void Fault(string surface, Exception error)
        {
            Observers.Ready = false;
            Volatile.Write(ref ArrayAnchor.Active, 0);
            if (Interlocked.Exchange(ref faulted, 1) == 0)
                SafeLog("[BMAFR1I1] INCONCLUSIVE observer=" + surface + " reason=" + error.GetType().Name + ": " + error.Message + "; original gameplay preserved");
        }

        private static void SafeLog(string line)
        {
            try { if (self != null) self.Logger.LogInfo(line); }
            catch { Observers.Ready = false; Volatile.Write(ref ArrayAnchor.Active, 0); }
        }
    }
}
