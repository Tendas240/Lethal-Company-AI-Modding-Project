using System;
using System.Collections;

namespace S142AKCFDiag1
{
    // Pure decision only. The caller performs the final local-list mutation only after this returns an index.
    internal static class SelectionPolicy
    {
        internal static int FindCircusFacility(
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

            int circusFacility = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                if (dungeonName(entry) != "Circus Facility")
                    continue;
                if (circusFacility != -1)
                    throw new InvalidOperationException("Duplicate viable Circus Facility entries.");
                circusFacility = i;
            }

            if (circusFacility == -1)
                throw new InvalidOperationException("Circus Facility not returned as viable.");
            if (assetName(pool[circusFacility]) != "CircusFacilityFlow")
                throw new InvalidOperationException("Circus Facility flow asset mismatch.");
            if (rarity(pool[circusFacility]) != 100)
                throw new InvalidOperationException("Circus Facility has not reached accepted normalized rarity 100.");

            return circusFacility;
        }
    }
}
