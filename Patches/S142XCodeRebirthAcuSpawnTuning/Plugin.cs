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

namespace S142XCodeRebirthAcuSpawnTuning
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(CodeRebirthGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DawnGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DuskGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142xcoderebirthacuspawntuning";
        internal const string PluginName = "S1.42X CodeRebirth ACU Spawn Tuning";
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
            "code_rebirth:air_control_unit_none",
            "code_rebirth:air_control_unit_low",
            "code_rebirth:air_control_unit_medium",
            "code_rebirth:air_control_unit_high",
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
                Logger.LogError("S1.42X ACU spawn tuning refused to arm because the validated CodeRebirth/DawnLib dependency set does not match the frozen baseline.");
                return;
            }

            if (LethalContent.Moons.IsFrozen)
            {
                ApplyAcuSpawnScale();
                return;
            }

            // CodeRebirth is a hard dependency, so its Dusk definitions and MapObjectSpawnMechanics
            // providers have already been registered before this plugin subscribes. DawnLib rebuilds
            // those moon curves during Moons.OnFreeze; subscribing here ensures this callback runs
            // after that registration/rebuild path and scales only the final ACU provider curves.
            LethalContent.Moons.OnFreeze += ApplyAcuSpawnScale;
            Logger.LogInfo("S1.42X ACU spawn tuning armed; waiting for DawnLib moon-registry freeze to scale code_rebirth:air_control_unit curves by 0.5.");
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

        private void ApplyAcuSpawnScale()
        {
            if (applied)
            {
                return;
            }

            if (!LethalContent.MapObjects.IsFrozen)
            {
                Logger.LogError("S1.42X ACU spawn tuning refused to apply: DawnLib MapObjects registry was not frozen when the moon-freeze callback ran.");
                return;
            }

            NamespacedKey acuKey = NamespacedKey.From("code_rebirth", "air_control_unit");
            if (!LethalContent.MapObjects.TryGetValue(acuKey, out DawnMapObjectInfo acuInfo) || acuInfo?.OutsideInfo == null)
            {
                Logger.LogError("S1.42X ACU spawn tuning refused to apply: exact DawnLib map object code_rebirth:air_control_unit with OutsideInfo was not found.");
                return;
            }

            object spawnWeights = acuInfo.OutsideInfo.SpawnWeights;
            FieldInfo providersField = spawnWeights.GetType().GetField("_providers", BindingFlags.Instance | BindingFlags.NonPublic);
            if (providersField == null || providersField.GetValue(spawnWeights) is not IEnumerable providers)
            {
                Logger.LogError("S1.42X ACU spawn tuning refused to apply: expected DawnLib ProviderTable private provider list was not found.");
                return;
            }

            List<MapObjectSpawnMechanics> mechanics = providers.Cast<object>().OfType<MapObjectSpawnMechanics>().ToList();
            if (mechanics.Count != 1)
            {
                Logger.LogError($"S1.42X ACU spawn tuning refused to apply: expected exactly one Dusk MapObjectSpawnMechanics provider, found {mechanics.Count}.");
                return;
            }

            Dictionary<NamespacedKey, AnimationCurve> curves = mechanics[0].CurvesByMoonOrTagName;
            HashSet<string> actualKeys = curves.Keys.Select(key => key.ToString()).ToHashSet(StringComparer.Ordinal);
            if (!actualKeys.SetEquals(ExpectedCurveKeys))
            {
                string missing = string.Join(", ", ExpectedCurveKeys.Except(actualKeys).OrderBy(x => x));
                string extra = string.Join(", ", actualKeys.Except(ExpectedCurveKeys).OrderBy(x => x));
                Logger.LogError($"S1.42X ACU spawn tuning refused to apply: ACU curve-key contract drifted. Missing=[{missing}] Extra=[{extra}].");
                return;
            }

            if (curves.Values.Any(curve => curve == null || curve.keys == null || curve.keys.Length == 0))
            {
                Logger.LogError("S1.42X ACU spawn tuning refused to apply: one or more expected ACU curves were null or empty.");
                return;
            }

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
            Logger.LogInfo($"S1.42X ACU spawn tuning applied: scaled all {curves.Count} code_rebirth:air_control_unit moon/tag curves by {SpawnScale:0.0}; no other map-object provider was modified.");
        }
    }
}
