using System;
using System.Collections;

namespace S142AKTWDiag1
{
    // Pure decision only. The caller performs the final local-list mutation only after this returns an index.
    internal static class SelectionPolicy
    {
        internal static int FindTower(
            IList pool,
            bool debugResults,
            string moon,
            bool selectionCaller,
            bool simulationCaller,
            Func<object, string> dungeonName,
            Func<object, string> assetName,
            Func<object, int> rarity)
        {
            if (!debugResults || moon != "Offense")
                return -1;
            if (simulationCaller)
                return -1;
            if (!selectionCaller)
                throw new InvalidOperationException("Unrecognized Offense debug-results caller.");
            if (pool == null || pool.Count == 0)
                throw new InvalidOperationException("Empty/null viable pool.");
            if (dungeonName == null || assetName == null || rarity == null)
                throw new InvalidOperationException("Selection accessors are missing.");

            int storehouse = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                if (dungeonName(entry) != "Tower")
                    continue;
                if (storehouse != -1)
                    throw new InvalidOperationException("Duplicate viable Tower entries.");
                storehouse = i;
            }

            if (storehouse == -1)
                throw new InvalidOperationException("Tower not returned as viable.");
            if (assetName(pool[storehouse]) != "TowerFlow")
                throw new InvalidOperationException("Tower flow asset mismatch.");
            if (rarity(pool[storehouse]) != 100)
                throw new InvalidOperationException("Tower has not reached accepted normalized rarity 100.");

            return storehouse;
        }
    }
}
