using System;
using System.Collections.Generic;

namespace S142AKBMGHDiag1
{
    internal enum TraversalDecision
    {
        Inactive,
        OutOfScope,
        MissingPair,
        InvalidPair,
        Valid
    }

    internal readonly struct TeleportTopologyEntry
    {
        internal int Id { get; }
        internal bool IsEntranceToBuilding { get; }

        internal TeleportTopologyEntry(int id, bool isEntranceToBuilding)
        {
            Id = id;
            IsEntranceToBuilding = isEntranceToBuilding;
        }
    }

    internal sealed class TopologyCheck
    {
        internal bool IsOk { get; }
        internal string Summary { get; }

        internal TopologyCheck(bool isOk, string summary)
        {
            IsOk = isOk;
            Summary = summary;
        }
    }

    internal sealed class TraversalCoverage
    {
        private readonly bool[,] coverage = new bool[4, 2];

        internal void Record(int id, bool sourceIsEntranceToBuilding)
        {
            if (id < 0 || id > 3)
                throw new InvalidOperationException("Coverage ID is outside 0..3.");
            coverage[id, sourceIsEntranceToBuilding ? 0 : 1] = true;
        }

        internal bool Has(int id, bool sourceIsEntranceToBuilding)
        {
            if (id < 0 || id > 3)
                return false;
            return coverage[id, sourceIsEntranceToBuilding ? 0 : 1];
        }

        internal string Summary()
        {
            var parts = new List<string>();
            for (int id = 0; id <= 3; id++)
            {
                parts.Add("id" + id + "=outside>inside:" + Flag(coverage[id, 0])
                    + ",inside>outside:" + Flag(coverage[id, 1]));
            }
            return string.Join(";", parts);
        }

        private static string Flag(bool value)
        {
            return value ? "1" : "0";
        }
    }

    // Pure observation policy. It classifies already-completed native state and never mutates game objects.
    internal static class ObservationPolicy
    {
        internal static TraversalDecision ClassifyTraversal(
            bool active,
            int sourceId,
            bool sourceIsEntranceToBuilding,
            bool hasTarget,
            int targetId,
            bool targetIsEntranceToBuilding)
        {
            if (!active)
                return TraversalDecision.Inactive;
            if (sourceId < 0 || sourceId > 3)
                return TraversalDecision.OutOfScope;
            if (!hasTarget)
                return TraversalDecision.MissingPair;
            if (targetId != sourceId || targetIsEntranceToBuilding == sourceIsEntranceToBuilding)
                return TraversalDecision.InvalidPair;
            return TraversalDecision.Valid;
        }

        internal static TopologyCheck CheckTopology(IEnumerable<TeleportTopologyEntry> entries)
        {
            if (entries == null)
                throw new InvalidOperationException("Topology entries are null.");

            int[,] counts = new int[4, 2];
            foreach (TeleportTopologyEntry entry in entries)
            {
                if (entry.Id < 0 || entry.Id > 3)
                    continue;
                counts[entry.Id, entry.IsEntranceToBuilding ? 0 : 1]++;
            }

            bool ok = true;
            var parts = new List<string>();
            for (int id = 0; id <= 3; id++)
            {
                int outside = counts[id, 0];
                int inside = counts[id, 1];
                if (outside != 1 || inside != 1)
                    ok = false;
                parts.Add("id" + id + "=outside:" + outside + ",inside:" + inside);
            }

            return new TopologyCheck(ok, string.Join(";", parts));
        }
    }
}
