using System;
using System.Collections;
using System.Collections.Generic;
using S142AKBMDSFix1Diag1;

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
        return SelectionPolicy.FindDeepSewers(
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

    static void ExpectInvalid(Action action, string label)
    {
        bool refused = false;
        try
        {
            action();
        }
        catch (InvalidOperationException)
        {
            refused = true;
        }
        Require(refused, "expected fail-closed refusal: " + label);
    }

    static void ExpectSelectionRefusal(
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

        ExpectInvalid(
            () => Decide(pool, selectionCaller: selectionCaller, simulationCaller: simulationCaller),
            "selection");

        if (pool != null)
        {
            Require(pool.Count == before.Length, "refusal changed pool count");
            for (int i = 0; i < before.Length; i++)
                Require(object.ReferenceEquals(pool[i], before[i]), "refusal changed pool identity/order");
        }
    }

    static void Main()
    {
        var deepSewers = new Entry("Deep Sewers", "DeepSewersFlow", 100);
        var substation = new Entry("Substation", "SubstationFlow", 100);
        var mansion = new Entry("Haunted Mansion", "Level3Flow", 100);
        var pool = new List<Entry> { substation, deepSewers, mansion };

        Require(Decide(pool) == 1, "exact Deep Sewers target index");
        Require(pool.Count == 3 && object.ReferenceEquals(pool[1], deepSewers), "pure policy mutated input");
        Require(Decide(pool, debug: false) == -1, "debugResults=false must remain normal");
        Require(Decide(pool, moon: "Offense") == -1, "other moon must remain normal");
        Require(Decide(pool, simulationCaller: true) == -1, "terminal simulation must remain normal");
        Require(Decide(pool, selectionCaller: false, simulationCaller: true) == -1,
            "terminal simulation exclusion must win without forcing a selection-caller refusal");

        ExpectSelectionRefusal(pool, selectionCaller: false, simulationCaller: false);
        ExpectSelectionRefusal(null);
        ExpectSelectionRefusal(new List<Entry>());
        ExpectSelectionRefusal(new List<Entry> { substation, mansion });
        ExpectSelectionRefusal(new List<Entry> { deepSewers, deepSewers });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Deep Sewers", "OtherFlow", 100) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Deep Sewers", "DeepSewersFlow", 65) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Deep Sewers", "DeepSewersFlow", 0) });
        ExpectSelectionRefusal(new List<Entry> { null, deepSewers });
        ExpectSelectionRefusal(new List<Entry> { deepSewers, null });

        var independentA = new List<Entry>
        {
            new Entry("Substation", "SubstationFlow", 100),
            new Entry("Deep Sewers", "DeepSewersFlow", 100)
        };
        var independentB = new List<Entry>
        {
            new Entry("Deep Sewers", "DeepSewersFlow", 100),
            new Entry("Haunted Mansion", "Level3Flow", 100)
        };
        Require(Decide(independentA) == 1 && Decide(independentB) == 0, "independent repeated pools");
        Require(independentA.Count == 2 && independentB.Count == 2, "repeated decisions mutated pools");

        Console.WriteLine("PASS: S1.42AK-BMDSFIX1-DIAG1 pure Deep Sewers selector fail-closed policy.");
    }
}
