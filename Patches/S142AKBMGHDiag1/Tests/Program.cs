using System;
using System.Collections;
using System.Collections.Generic;
using S142AKBMGHDiag1;

static class Program
{
    sealed class Entry
    {
        internal string Name;
        internal string Asset;
        internal int Rarity;

        internal Entry(string name, string asset, int rarity)
        {
            Name = name;
            Asset = asset;
            Rarity = rarity;
        }
    }

    static int Decide(
        IList pool,
        bool debug = true,
        string moon = "Black Mesa",
        bool selectionCaller = true,
        bool simulationCaller = false)
    {
        return SelectionPolicy.FindGreenhouse(
            pool,
            debug,
            moon,
            selectionCaller,
            simulationCaller,
            value => ((Entry)value).Name,
            value => ((Entry)value).Asset,
            value => ((Entry)value).Rarity);
    }

    static void Require(bool condition, string message)
    {
        if (!condition)
            throw new Exception("Regression assertion failed: " + message);
    }

    static void ExpectRefusal(
        IList pool,
        bool selectionCaller = true,
        bool simulationCaller = false)
    {
        object[] before = null;
        if (pool != null)
        {
            before = new object[pool.Count];
            pool.CopyTo(before, 0);
        }

        bool refused = false;
        try
        {
            Decide(pool, selectionCaller: selectionCaller, simulationCaller: simulationCaller);
        }
        catch (InvalidOperationException)
        {
            refused = true;
        }

        Require(refused, "expected selection refusal");
        if (pool != null)
        {
            Require(pool.Count == before.Length, "refusal changed pool count");
            for (int i = 0; i < before.Length; i++)
                Require(object.ReferenceEquals(pool[i], before[i]), "refusal changed pool identity/order");
        }
    }

    static List<TeleportTopologyEntry> ExactTopology()
    {
        var entries = new List<TeleportTopologyEntry>();
        for (int id = 0; id <= 3; id++)
        {
            entries.Add(new TeleportTopologyEntry(id, true));
            entries.Add(new TeleportTopologyEntry(id, false));
        }
        return entries;
    }

    static void Main()
    {
        var greenhouse = new Entry("Greenhouse", "GreenhouseFlow", 100);
        var facility = new Entry("Facility", "Level1Flow", 100);
        var pool = new List<Entry> { facility, greenhouse };

        Require(Decide(pool) == 1, "exact Greenhouse target index");
        Require(pool.Count == 2 && greenhouse.Rarity == 100, "pure selection policy mutated input");
        Require(Decide(pool, debug: false) == -1, "debugResults=false must remain normal");
        Require(Decide(pool, moon: "Offense") == -1, "other moon must remain normal");
        Require(Decide(pool, simulationCaller: true) == -1, "terminal simulation must remain normal");
        ExpectRefusal(pool, selectionCaller: false, simulationCaller: false);
        ExpectRefusal(null);
        ExpectRefusal(new List<Entry>());
        ExpectRefusal(new List<Entry> { facility });
        ExpectRefusal(new List<Entry> { greenhouse, greenhouse });
        ExpectRefusal(new List<Entry> { new Entry("Greenhouse", "OtherFlow", 100) });
        ExpectRefusal(new List<Entry> { new Entry("Greenhouse", "GreenhouseFlow", 65) });
        ExpectRefusal(new List<Entry> { new Entry("Greenhouse", "GreenhouseFlow", 0) });
        ExpectRefusal(new List<Entry> { null, greenhouse });

        var independentA = new List<Entry> { new Entry("Facility", "Level1Flow", 100), new Entry("Greenhouse", "GreenhouseFlow", 100) };
        var independentB = new List<Entry> { new Entry("Greenhouse", "GreenhouseFlow", 100), new Entry("Facility", "Level1Flow", 100) };
        Require(Decide(independentA) == 1 && Decide(independentB) == 0, "independent repeated pools");
        Require(independentA.Count == 2 && independentB.Count == 2, "repeated decisions mutated pools");

        Require(ObservationPolicy.ClassifyTraversal(false, 0, true, true, 0, false) == TraversalDecision.Inactive,
            "observer must be inactive before target selection");
        Require(ObservationPolicy.ClassifyTraversal(true, 0, true, false, -1, false) == TraversalDecision.MissingPair,
            "null native exitScript must not claim success");
        Require(ObservationPolicy.ClassifyTraversal(true, 1, true, true, 1, true) == TraversalDecision.InvalidPair,
            "same-side pair must be invalid");
        Require(ObservationPolicy.ClassifyTraversal(true, 1, true, true, 2, false) == TraversalDecision.InvalidPair,
            "different-ID pair must be invalid");
        Require(ObservationPolicy.ClassifyTraversal(true, 4, true, true, 4, false) == TraversalDecision.OutOfScope,
            "IDs outside 0..3 must not become required coverage");
        Require(ObservationPolicy.ClassifyTraversal(true, 1, true, true, 1, false) == TraversalDecision.Valid,
            "same-ID opposite-side pair must be valid");

        var coverage = new TraversalCoverage();
        Require(!coverage.Has(1, true) && !coverage.Has(1, false), "coverage must start empty");
        coverage.Record(1, true);
        Require(coverage.Has(1, true) && !coverage.Has(1, false), "outside->inside coverage bit only");
        coverage.Record(1, true);
        Require(coverage.Has(1, true) && !coverage.Has(1, false), "repeated traversal must be idempotent");
        coverage.Record(1, false);
        Require(coverage.Has(1, true) && coverage.Has(1, false), "bidirectional coverage tracking");
        Require(!coverage.Has(0, true) && !coverage.Has(2, true) && !coverage.Has(3, true), "coverage must not bleed across IDs");

        List<TeleportTopologyEntry> exact = ExactTopology();
        TopologyCheck exactCheck = ObservationPolicy.CheckTopology(exact);
        Require(exactCheck.IsOk, "exact unique opposite pairs for 0..3");
        Require(exact.Count == 8, "topology policy mutated exact input");

        var missingSide = ExactTopology();
        missingSide.RemoveAt(missingSide.Count - 1);
        Require(!ObservationPolicy.CheckTopology(missingSide).IsOk, "missing side must be inconclusive");

        var duplicateSide = ExactTopology();
        duplicateSide.Add(new TeleportTopologyEntry(2, true));
        Require(!ObservationPolicy.CheckTopology(duplicateSide).IsOk, "duplicate same-side entry must be inconclusive");

        var missingId = new List<TeleportTopologyEntry>();
        for (int id = 0; id <= 2; id++)
        {
            missingId.Add(new TeleportTopologyEntry(id, true));
            missingId.Add(new TeleportTopologyEntry(id, false));
        }
        Require(!ObservationPolicy.CheckTopology(missingId).IsOk, "missing required ID must be inconclusive");

        Console.WriteLine("PASS: C3F17.3 selection refusal/input-preservation and traversal/topology/coverage policies.");
    }
}
