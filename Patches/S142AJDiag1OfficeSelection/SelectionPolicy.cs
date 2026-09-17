using System;
using System.Collections;

namespace S142AJDiag1OfficeSelection
{
    // Pure decision only: no list mutation until every gate has succeeded.
    internal static class SelectionPolicy
    {
        internal static int FindOffice(IList pool, bool debugResults, string moon,
            bool selectionCaller, Func<object, string> dungeonName,
            Func<object, string> assetName, Func<object, int> rarity)
        {
            if (!debugResults || moon != "Offense" || !selectionCaller)
                return -1; // Not the diagnostic selection path.
            if (pool == null || pool.Count == 0)
                throw new InvalidOperationException("Empty/null viable pool.");
            int office = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable entry.");
                if (dungeonName(entry) != "LC Office") continue;
                if (office != -1)
                    throw new InvalidOperationException("Duplicate viable LC Office entries.");
                office = i;
            }
            if (office == -1)
                throw new InvalidOperationException("LC Office not returned as viable.");
            if (assetName(pool[office]) != "OfficeDungeonFlow")
                throw new InvalidOperationException("LC Office flow asset mismatch.");
            if (rarity(pool[office]) != 100)
                throw new InvalidOperationException("LC Office has not reached accepted normalized rarity 100.");
            return office;
        }
    }
}
