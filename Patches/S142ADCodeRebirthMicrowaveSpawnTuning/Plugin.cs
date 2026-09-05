using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Logging;
using Dawn;
using Dusk;
using UnityEngine;

namespace S142ADCodeRebirthMicrowaveSpawnTuning
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(CodeRebirthGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DawnGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DuskGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142adcoderebirthmicrowavespawntuning";
        internal const string PluginName = "S1.42AD CodeRebirth Microwave Spawn Tuning";
        internal const string PluginVersion = "1.0.0";

        internal const string CodeRebirthGuid = "CodeRebirth";
        internal const string DawnGuid = "com.github.teamxiaolan.dawnlib";
        internal const string DuskGuid = "com.github.teamxiaolan.dawnlib.dusk";

        private const string ExpectedCodeRebirthVersion = "1.6.9";
        private const string ExpectedDawnVersion = "0.9.25";
        private const float SpawnScale = 0.5f;

        private static readonly HashSet<string> ExpectedCurveKeys = new(StringComparer.Ordinal)
        {
            "lethal_company:vanilla",
            "lethal_company:custom",
            "code_rebirth:oxyde",
            "code_rebirth:functional_microwave_none",
            "code_rebirth:functional_microwave_low",
            "code_rebirth:functional_microwave_medium",
            "code_rebirth:functional_microwave_high",
            "lethal_company:experimentation",
            "lethal_company:vow",
            "lethal_company:march",
            "lethal_company:assurance",
            "lethal_company:offense",
            "lethal_company:adamance",
            "lethal_company:embrion",
            "lethal_company:rend",
            "lethal_company:dine",
            "lethal_company:titan",
            "lethal_company:artifice"
        };

        internal static ManualLogSource Log;
        private bool applied;

        private void Awake()
        {
            Log = Logger;

            if (!ValidatePluginVersion(CodeRebirthGuid, ExpectedCodeRebirthVersion) ||
                !ValidatePluginVersion(DawnGuid, ExpectedDawnVersion) ||
                !ValidatePluginVersion(DuskGuid, ExpectedDawnVersion))
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to arm because the validated CodeRebirth/DawnLib dependency set does not match the frozen baseline.");
                return;
            }

            if (LethalContent.Moons.IsFrozen)
            {
                ApplyMicrowaveSpawnScale();
                return;
            }

            LethalContent.Moons.OnFreeze += ApplyMicrowaveSpawnScale;
            Logger.LogInfo("S1.42AD microwave spawn tuning armed; waiting for DawnLib moon-registry freeze to scale code_rebirth:functional_microwave curves by 0.5.");
        }

        private bool ValidatePluginVersion(string guid, string expectedVersion)
        {
            if (!Chainloader.PluginInfos.TryGetValue(guid, out PluginInfo info))
            {
                Logger.LogError($"Required dependency {guid} is not loaded; expected version {expectedVersion}.");
                return false;
            }

            string actualVersion = info.Metadata.Version.ToString();
            if (!string.Equals(actualVersion, expectedVersion, StringComparison.Ordinal))
            {
                Logger.LogError($"Dependency {guid} version mismatch: expected {expectedVersion}, got {actualVersion}.");
                return false;
            }

            Logger.LogInfo($"Validated dependency {guid} v{actualVersion}.");
            return true;
        }

        private void ApplyMicrowaveSpawnScale()
        {
            if (applied)
            {
                return;
            }

            if (!LethalContent.MapObjects.IsFrozen)
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to apply: DawnLib MapObjects registry was not frozen when the moon-freeze callback ran.");
                return;
            }

            NamespacedKey microwaveKey = NamespacedKey.From("code_rebirth", "functional_microwave");
            if (!LethalContent.MapObjects.TryGetValue(microwaveKey, out DawnMapObjectInfo microwaveInfo) || microwaveInfo?.InsideInfo == null)
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to apply: exact DawnLib map object code_rebirth:functional_microwave with InsideInfo was not found.");
                return;
            }

            object spawnWeights = microwaveInfo.InsideInfo.SpawnWeights;
            FieldInfo providersField = spawnWeights.GetType().GetField("_providers", BindingFlags.Instance | BindingFlags.NonPublic);
            if (providersField == null || providersField.GetValue(spawnWeights) is not IEnumerable providers)
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to apply: expected DawnLib ProviderTable private provider list was not found.");
                return;
            }

            List<MapObjectSpawnMechanics> mechanics = providers.Cast<object>().OfType<MapObjectSpawnMechanics>().ToList();
            if (mechanics.Count != 1)
            {
                Logger.LogError($"S1.42AD microwave spawn tuning refused to apply: expected exactly one Dusk MapObjectSpawnMechanics provider, found {mechanics.Count}.");
                return;
            }

            MapObjectSpawnMechanics mechanic = mechanics[0];
            if (!mechanic.PrioritiseMoons)
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to apply: expected Functional Microwave provider to prioritise Moon curves, but PrioritiseMoons was false.");
                return;
            }

            Dictionary<NamespacedKey, AnimationCurve> interiorCurves = mechanic.CurvesByInteriorOrTagName;
            if (interiorCurves.Count != 0)
            {
                string interiorKeys = string.Join(", ", interiorCurves.Keys.Select(key => key.ToString()).OrderBy(x => x));
                Logger.LogError($"S1.42AD microwave spawn tuning refused to apply: expected zero Functional Microwave interior curves, found {interiorCurves.Count}: [{interiorKeys}].");
                return;
            }

            Dictionary<NamespacedKey, AnimationCurve> curves = mechanic.CurvesByMoonOrTagName;
            HashSet<string> actualKeys = curves.Keys.Select(key => key.ToString()).ToHashSet(StringComparer.Ordinal);
            if (!actualKeys.SetEquals(ExpectedCurveKeys))
            {
                string missing = string.Join(", ", ExpectedCurveKeys.Except(actualKeys).OrderBy(x => x));
                string extra = string.Join(", ", actualKeys.Except(ExpectedCurveKeys).OrderBy(x => x));
                Logger.LogError($"S1.42AD microwave spawn tuning refused to apply: microwave curve-key contract drifted. Missing=[{missing}] Extra=[{extra}].");
                return;
            }

            if (curves.Values.Any(curve => curve == null || curve.keys == null || curve.keys.Length == 0))
            {
                Logger.LogError("S1.42AD microwave spawn tuning refused to apply: one or more expected microwave curves were null or empty.");
                return;
            }

            Logger.LogInfo($"S1.42AD microwave provider contract validated: PrioritiseMoons=true, MoonCurves={curves.Count}, InteriorCurves={interiorCurves.Count}.");

            foreach (AnimationCurve curve in curves.Values)
            {
                Keyframe[] keys = curve.keys;
                for (int i = 0; i < keys.Length; i++)
                {
                    Keyframe key = keys[i];
                    key.value *= SpawnScale;
                    key.inTangent *= SpawnScale;
                    key.outTangent *= SpawnScale;
                    keys[i] = key;
                }
                curve.keys = keys;
            }

            applied = true;
            Logger.LogInfo($"S1.42AD microwave spawn tuning applied: scaled all {curves.Count} code_rebirth:functional_microwave moon/tag curves by {SpawnScale:0.0}; no other map-object provider was modified.");
        }
    }
}
