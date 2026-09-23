using System;
using System.Collections;

namespace S142AKBMGHDiag1
{
    // Pure decision only. The caller performs the final List mutation only after this returns an index.
    internal static class SelectionPolicy
    {
        internal static int FindGreenhouse(
            IList pool,
            bool debugResults,
            string moon,
            bool selectionCaller,
            bool simulationCaller,
            Func<object, string> dungeonName,
            Func<object, string> assetName,
            Func<object, int> rarity)
        {
            if (!debugResults || moon != "Black Mesa")
                return -1;
            if (simulationCaller)
                return -1;
            if (!selectionCaller)
                throw new InvalidOperationException("Unrecognized Black Mesa debug-results caller.");
            if (pool == null || pool.Count == 0)
                throw new InvalidOperationException("Empty/null viable pool.");
            if (dungeonName == null || assetName == null || rarity == null)
                throw new InvalidOperationException("Selection accessors are missing.");

            int greenhouse = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                if (dungeonName(entry) != "Greenhouse")
                    continue;
                if (greenhouse != -1)
                    throw new InvalidOperationException("Duplicate viable Greenhouse entries.");
                greenhouse = i;
            }

            if (greenhouse == -1)
                throw new InvalidOperationException("Greenhouse not returned as viable.");
            if (assetName(pool[greenhouse]) != "GreenhouseFlow")
                throw new InvalidOperationException("Greenhouse flow asset mismatch.");
            if (rarity(pool[greenhouse]) != 100)
                throw new InvalidOperationException("Greenhouse has not reached accepted normalized rarity 100.");

            return greenhouse;
        }
    }
}
