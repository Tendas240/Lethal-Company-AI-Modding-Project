using System;
using System.Collections;

namespace S142AKFXDiag1
{
    // Pure fail-closed policy: only returns an index into the original viable list.
    internal static class SelectionPolicy
    {
        internal static int FindFracturedComplex(
            IList pool,
            bool debugResults,
            string moon,
            bool selectionCaller,
            bool simulationCaller,
            Func<object, string> dungeonName,
            Func<object, string> assetName,
            Func<object, int> rarity)
        {
            if (!debugResults || !string.Equals(moon, "Offense", StringComparison.Ordinal))
                return -1;
            if (simulationCaller)
                return -1;
            if (!selectionCaller)
                throw new InvalidOperationException("Unrecognized Offense debug-results caller.");
            if (pool == null || pool.Count == 0)
                throw new InvalidOperationException("Empty/null viable pool.");
            if (dungeonName == null || assetName == null || rarity == null)
                throw new InvalidOperationException("Selection accessors are missing.");

            int selected = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                string name = dungeonName(entry);
                string asset = assetName(entry);
                if (string.IsNullOrEmpty(name) || string.IsNullOrEmpty(asset))
                    throw new InvalidOperationException("Invalid viable wrapper name/asset.");

                bool nameMatches = string.Equals(name, "Fractured Complex", StringComparison.Ordinal);
                bool assetMatches = string.Equals(asset, "FracturedComplexFlow", StringComparison.Ordinal);
                if (nameMatches != assetMatches)
                    throw new InvalidOperationException("Fractured Complex name/asset identity mismatch.");
                if (!nameMatches)
                    continue;
                if (selected != -1)
                    throw new InvalidOperationException("Duplicate viable Fractured Complex entries.");
                if (rarity(entry) != 100)
                    throw new InvalidOperationException("Fractured Complex has not reached accepted normalized rarity 100.");
                selected = i;
            }
            if (selected == -1)
                throw new InvalidOperationException("Fractured Complex not returned as viable.");
            return selected;
        }
    }
}
