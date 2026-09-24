using System;

namespace S142AKBMDSFix1
{
    internal static class SizeClampPolicy
    {
        internal const string TargetMoon = "Black Mesa";
        internal const string TargetDungeonFlow = "DeepSewersFlow";
        internal const float TargetMultiplier = 1.0f;

        internal static float Apply(string moonName, string dungeonFlowName, float currentMultiplier, out bool applied)
        {
            applied = false;

            if (!string.Equals(moonName, TargetMoon, StringComparison.Ordinal) ||
                !string.Equals(dungeonFlowName, TargetDungeonFlow, StringComparison.Ordinal))
                return currentMultiplier;

            if (float.IsNaN(currentMultiplier) || float.IsInfinity(currentMultiplier) || currentMultiplier <= TargetMultiplier)
                return currentMultiplier;

            applied = true;
            return TargetMultiplier;
        }
    }
}
