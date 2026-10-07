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

namespace S142AECodeRebirthMicrowaveSpawnTuning
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(CodeRebirthGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DawnGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DuskGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142aecoderebirthmicrowavespawntuning";
        internal const string PluginName = "S1.42AE CodeRebirth Microwave Spawn Tuning";
        internal const string PluginVersion = "1.0.0";

        internal const string CodeRebirthGuid = "CodeRebirth";
        internal const string DawnGuid = "com.github.teamxiaolan.dawnlib";
        internal const string DuskGuid = "com.github.teamxiaolan.dawnlib.dusk";

        private const string ExpectedCodeRebirthVersion = "1.6.9";
        private const string ExpectedDawnVersion = "0.9.25";
        private const float SpawnScale = 0.5f;

        private static readonly HashSet<string> ExpectedMoonCurveKeys = new(StringComparer.Ordinal)
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

        private static readonly HashSet<string> ExpectedInteriorCurveKeys = new(StringComparer.Ordinal)
        {
            "lethal_company:vanilla",
            "lethal_company:custom",
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
            "lethal_company:artifice",
            "code_rebirth:functional_microwave_none",
            "code_rebirth:functional_microwave_low",
            "code_rebirth:functional_microwave_medium",
            "code_rebirth:functional_microwave_high",
            "code_rebirth:functional_microwave_ultra_high"
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
                Logger.LogError("S1.42AE microwave spawn tuning refused to arm because the validated CodeRebirth/DawnLib dependency set does not match the frozen baseline.");
                return;
            }

            if (LethalContent.Moons.IsFrozen)
            {
                ApplyMicrowaveSpawnScale();
                return;
            }

            LethalContent.Moons.OnFreeze += ApplyMicrowaveSpawnScale;
            Logger.LogInfo("S1.42AE microwave spawn tuning armed; waiting for DawnLib moon-registry freeze to validate the 18 Moon / 18 Interior provider contract and scale only effective Moon/tag curves by 0.5.");
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
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: DawnLib MapObjects registry was not frozen when the moon-freeze callback ran.");
                return;
            }

            NamespacedKey microwaveKey = NamespacedKey.From("code_rebirth", "functional_microwave");
            if (!LethalContent.MapObjects.TryGetValue(microwaveKey, out DawnMapObjectInfo microwaveInfo) || microwaveInfo?.InsideInfo == null)
            {
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: exact DawnLib map object code_rebirth:functional_microwave with InsideInfo was not found.");
                return;
            }

            object spawnWeights = microwaveInfo.InsideInfo.SpawnWeights;
            FieldInfo providersField = spawnWeights.GetType().GetField("_providers", BindingFlags.Instance | BindingFlags.NonPublic);
            if (providersField == null || providersField.GetValue(spawnWeights) is not IEnumerable providers)
            {
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: expected DawnLib ProviderTable private provider list was not found.");
                return;
            }

            List<MapObjectSpawnMechanics> mechanics = providers.Cast<object>().OfType<MapObjectSpawnMechanics>().ToList();
            if (mechanics.Count != 1)
            {
                Logger.LogError($"S1.42AE microwave spawn tuning refused to apply: expected exactly one Dusk MapObjectSpawnMechanics provider, found {mechanics.Count}.");
                return;
            }

            MapObjectSpawnMechanics mechanic = mechanics[0];
            if (!mechanic.PrioritiseMoons)
            {
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: expected Functional Microwave provider to prioritise Moon curves, but PrioritiseMoons was false.");
                return;
            }

            Dictionary<NamespacedKey, AnimationCurve> moonCurves = mechanic.CurvesByMoonOrTagName;
            Dictionary<NamespacedKey, AnimationCurve> interiorCurves = mechanic.CurvesByInteriorOrTagName;

            HashSet<string> actualMoonKeys = moonCurves.Keys.Select(key => key.ToString()).ToHashSet(StringComparer.Ordinal);
            if (!actualMoonKeys.SetEquals(ExpectedMoonCurveKeys))
            {
                string missing = string.Join(", ", ExpectedMoonCurveKeys.Except(actualMoonKeys).OrderBy(x => x));
                string extra = string.Join(", ", actualMoonKeys.Except(ExpectedMoonCurveKeys).OrderBy(x => x));
                Logger.LogError($"S1.42AE microwave spawn tuning refused to apply: Moon curve-key contract drifted. Missing=[{missing}] Extra=[{extra}].");
                return;
            }

            HashSet<string> actualInteriorKeys = interiorCurves.Keys.Select(key => key.ToString()).ToHashSet(StringComparer.Ordinal);
            if (!actualInteriorKeys.SetEquals(ExpectedInteriorCurveKeys))
            {
                string missing = string.Join(", ", ExpectedInteriorCurveKeys.Except(actualInteriorKeys).OrderBy(x => x));
                string extra = string.Join(", ", actualInteriorKeys.Except(ExpectedInteriorCurveKeys).OrderBy(x => x));
                Logger.LogError($"S1.42AE microwave spawn tuning refused to apply: Interior curve-key contract drifted. Missing=[{missing}] Extra=[{extra}].");
                return;
            }

            if (moonCurves.Values.Any(curve => curve == null || curve.keys == null || curve.keys.Length == 0))
            {
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: one or more expected Moon/tag curves were null or empty.");
                return;
            }

            if (interiorCurves.Values.Any(curve => curve == null || curve.keys == null || curve.keys.Length == 0))
            {
                Logger.LogError("S1.42AE microwave spawn tuning refused to apply: one or more expected Interior/tag curves were null or empty.");
                return;
            }

            string moonKeys = string.Join(", ", actualMoonKeys.OrderBy(x => x));
            string interiorKeys = string.Join(", ", actualInteriorKeys.OrderBy(x => x));
            Logger.LogInfo($"S1.42AE microwave provider contract validated: PrioritiseMoons=true, MoonCurves={moonCurves.Count}, InteriorCurves={interiorCurves.Count}.");
            Logger.LogInfo($"S1.42AE microwave provider Moon keys: [{moonKeys}].");
            Logger.LogInfo($"S1.42AE microwave provider Interior keys: [{interiorKeys}]. Interior curves are validation-only and will not be mutated.");

            foreach (AnimationCurve curve in moonCurves.Values)
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
            Logger.LogInfo($"S1.42AE microwave spawn tuning applied: scaled all {moonCurves.Count} code_rebirth:functional_microwave Moon/tag curves by {SpawnScale:0.0}; validated but did not mutate {interiorCurves.Count} Interior/tag curves; no other map-object provider was modified.");
        }
    }
}
