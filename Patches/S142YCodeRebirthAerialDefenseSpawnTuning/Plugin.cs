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

namespace S142YCodeRebirthAerialDefenseSpawnTuning
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency(CodeRebirthGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DawnGuid, BepInDependency.DependencyFlags.HardDependency)]
    [BepInDependency(DuskGuid, BepInDependency.DependencyFlags.HardDependency)]
    public sealed class Plugin : BaseUnityPlugin
    {
        internal const string PluginGuid = "tendas.lethalcompany.s142ycoderebirthaerialdefensespawntuning";
        internal const string PluginName = "S1.42Y CodeRebirth Aerial Defense Spawn Tuning";
        internal const string PluginVersion = "1.0.0";

        internal const string CodeRebirthGuid = "CodeRebirth";
        internal const string DawnGuid = "com.github.teamxiaolan.dawnlib";
        internal const string DuskGuid = "com.github.teamxiaolan.dawnlib.dusk";

        private const string ExpectedCodeRebirthVersion = "1.6.9";
        private const string ExpectedDawnVersion = "0.9.25";
        private const float SpawnScale = 0.5f;

        private static readonly string[] CommonCurveKeys =
        {
            "lethal_company:vanilla",
            "lethal_company:custom",
            "code_rebirth:oxyde",
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

        private static readonly TargetSpec[] Targets =
        {
            new TargetSpec(
                "Air Control Unit",
                "air_control_unit",
                "air_control_unit_none",
                "air_control_unit_low",
                "air_control_unit_medium",
                "air_control_unit_high"),
            new TargetSpec(
                "G.R.E.G. / Advanced Airspace Control",
                "gunslinger_greg",
                "gunslinger_greg_none",
                "gunslinger_greg_low",
                "gunslinger_greg_medium",
                "gunslinger_greg_high")
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
                Logger.LogError("S1.42Y aerial-defense spawn tuning refused to arm because the validated CodeRebirth/DawnLib dependency set does not match the frozen baseline.");
                return;
            }

            if (LethalContent.Moons.IsFrozen)
            {
                ApplyAerialDefenseSpawnScale();
                return;
            }

            LethalContent.Moons.OnFreeze += ApplyAerialDefenseSpawnScale;
            Logger.LogInfo("S1.42Y aerial-defense spawn tuning armed; waiting for DawnLib moon-registry freeze to validate and scale both code_rebirth:air_control_unit and code_rebirth:gunslinger_greg curves by 0.5.");
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

        private void ApplyAerialDefenseSpawnScale()
        {
            if (applied)
            {
                return;
            }

            if (!LethalContent.MapObjects.IsFrozen)
            {
                Logger.LogError("S1.42Y aerial-defense spawn tuning refused to apply: DawnLib MapObjects registry was not frozen when the moon-freeze callback ran.");
                return;
            }

            List<ValidatedTarget> validatedTargets = new();
            foreach (TargetSpec target in Targets)
            {
                if (!TryValidateTarget(target, out ValidatedTarget validated))
                {
                    Logger.LogError("S1.42Y aerial-defense spawn tuning made no changes because the complete two-target contract did not validate.");
                    return;
                }
                validatedTargets.Add(validated);
            }

            foreach (ValidatedTarget validated in validatedTargets)
            {
                ScaleCurves(validated.Curves);
            }

            applied = true;
            Logger.LogInfo(
                "S1.42Y aerial-defense spawn tuning applied transactionally: " +
                "scaled all 18 code_rebirth:air_control_unit curves and all 18 code_rebirth:gunslinger_greg curves by 0.5; " +
                "no other map-object provider was modified.");
        }

        private bool TryValidateTarget(TargetSpec target, out ValidatedTarget validated)
        {
            validated = null;

            NamespacedKey targetKey = NamespacedKey.From("code_rebirth", target.MapObjectKey);
            if (!LethalContent.MapObjects.TryGetValue(targetKey, out DawnMapObjectInfo info) || info?.OutsideInfo == null)
            {
                Logger.LogError($"S1.42Y aerial-defense spawn tuning contract failure: exact DawnLib map object code_rebirth:{target.MapObjectKey} ({target.Label}) with OutsideInfo was not found.");
                return false;
            }

            object spawnWeights = info.OutsideInfo.SpawnWeights;
            FieldInfo providersField = spawnWeights.GetType().GetField("_providers", BindingFlags.Instance | BindingFlags.NonPublic);
            if (providersField == null || providersField.GetValue(spawnWeights) is not IEnumerable providers)
            {
                Logger.LogError($"S1.42Y aerial-defense spawn tuning contract failure for {target.Label}: expected DawnLib ProviderTable private provider list was not found.");
                return false;
            }

            List<MapObjectSpawnMechanics> mechanics = providers.Cast<object>().OfType<MapObjectSpawnMechanics>().ToList();
            if (mechanics.Count != 1)
            {
                Logger.LogError($"S1.42Y aerial-defense spawn tuning contract failure for {target.Label}: expected exactly one Dusk MapObjectSpawnMechanics provider, found {mechanics.Count}.");
                return false;
            }

            Dictionary<NamespacedKey, AnimationCurve> curves = mechanics[0].CurvesByMoonOrTagName;
            HashSet<string> actualKeys = curves.Keys.Select(key => key.ToString()).ToHashSet(StringComparer.Ordinal);
            if (!actualKeys.SetEquals(target.ExpectedCurveKeys))
            {
                string missing = string.Join(", ", target.ExpectedCurveKeys.Except(actualKeys).OrderBy(x => x));
                string extra = string.Join(", ", actualKeys.Except(target.ExpectedCurveKeys).OrderBy(x => x));
                Logger.LogError($"S1.42Y aerial-defense spawn tuning contract failure for {target.Label}: curve-key contract drifted. Missing=[{missing}] Extra=[{extra}].");
                return false;
            }

            if (curves.Values.Any(curve => curve == null || curve.keys == null || curve.keys.Length == 0))
            {
                Logger.LogError($"S1.42Y aerial-defense spawn tuning contract failure for {target.Label}: one or more expected curves were null or empty.");
                return false;
            }

            validated = new ValidatedTarget(target, curves);
            Logger.LogInfo($"Validated {target.Label} spawn provider contract: code_rebirth:{target.MapObjectKey}, {curves.Count} exact moon/tag curves.");
            return true;
        }

        private static void ScaleCurves(Dictionary<NamespacedKey, AnimationCurve> curves)
        {
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
        }

        private sealed class TargetSpec
        {
            public string Label { get; }
            public string MapObjectKey { get; }
            public HashSet<string> ExpectedCurveKeys { get; }

            public TargetSpec(string label, string mapObjectKey, params string[] targetTagKeys)
            {
                Label = label;
                MapObjectKey = mapObjectKey;
                ExpectedCurveKeys = CommonCurveKeys
                    .Concat(targetTagKeys.Select(key => $"code_rebirth:{key}"))
                    .ToHashSet(StringComparer.Ordinal);
            }
        }

        private sealed class ValidatedTarget
        {
            public TargetSpec Spec { get; }
            public Dictionary<NamespacedKey, AnimationCurve> Curves { get; }

            public ValidatedTarget(TargetSpec spec, Dictionary<NamespacedKey, AnimationCurve> curves)
            {
                Spec = spec;
                Curves = curves;
            }
        }
    }
}
