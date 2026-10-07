using System;
using System.Collections;

namespace S142AKAGDiag1
{
    // Pure decision only. The caller performs the final local-list mutation only after this returns an index.
    internal static class SelectionPolicy
    {
        internal static int FindArtGallery(
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

            int artGallery = -1;
            for (int i = 0; i < pool.Count; i++)
            {
                object entry = pool[i];
                if (entry == null)
                    throw new InvalidOperationException("Null viable wrapper.");
                if (dungeonName(entry) != "Art Gallery")
                    continue;
                if (artGallery != -1)
                    throw new InvalidOperationException("Duplicate viable Art Gallery entries.");
                artGallery = i;
            }

            if (artGallery == -1)
                throw new InvalidOperationException("Art Gallery not returned as viable.");
            if (assetName(pool[artGallery]) != "MuseumInteriorFlow")
                throw new InvalidOperationException("Art Gallery flow asset mismatch.");
            if (rarity(pool[artGallery]) != 100)
                throw new InvalidOperationException("Art Gallery has not reached accepted normalized rarity 100.");

            return artGallery;
        }
    }
}
