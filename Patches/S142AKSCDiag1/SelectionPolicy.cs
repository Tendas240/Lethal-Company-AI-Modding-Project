using System;
using System.Collections;
using System.Collections.Generic;

namespace S142AKSCDiag1
{
    // Pure fail-closed policy: only returns an index into the original viable list.
    internal static class SelectionPolicy
    {
        internal static int FindStorageComplex(
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

            if (pool.IsReadOnly || pool.IsFixedSize)
                throw new InvalidOperationException("Unwritable normalized viable pool.");

            // Reject even non-target duplicate identities and wrapper aliases before selection.
            var names = new HashSet<string>(StringComparer.Ordinal);
            var assets = new HashSet<string>(StringComparer.Ordinal);
            int selected = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                for (int j = 0; j < i; j++)
                    if (object.ReferenceEquals(pool[j], entry))
                        throw new InvalidOperationException("Repeated viable wrapper reference.");
                string name = dungeonName(entry);
                string asset = assetName(entry);
                if (string.IsNullOrEmpty(name) || string.IsNullOrEmpty(asset))
                    throw new InvalidOperationException("Invalid viable wrapper name/asset.");
                if (!names.Add(name) || !assets.Add(asset))
                    throw new InvalidOperationException("Duplicate name/asset identity in viable pool.");
                int effectiveRarity = rarity(entry);
                if (effectiveRarity <= 0)
                    throw new InvalidOperationException("Invalid normalized viable rarity.");

                bool nameMatches = string.Equals(name, "Storage Complex", StringComparison.Ordinal);
                bool assetMatches = string.Equals(asset, "StorageComplex", StringComparison.Ordinal);
                if (nameMatches != assetMatches)
                    throw new InvalidOperationException("Storage Complex name/asset identity mismatch.");
                if (!nameMatches)
                    continue;
                if (selected != -1)
                    throw new InvalidOperationException("Duplicate viable Storage Complex entries.");
                if (effectiveRarity != 100)
                    throw new InvalidOperationException("Storage Complex has not reached accepted normalized rarity 100.");
                selected = i;
            }
            if (selected == -1)
                throw new InvalidOperationException("Storage Complex not returned as viable.");
            return selected;
        }
    }
}
