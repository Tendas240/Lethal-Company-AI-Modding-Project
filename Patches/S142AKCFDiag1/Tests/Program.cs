using System;
using System.Collections;
using System.Collections.Generic;
using S142AKCFDiag1;

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
        string moon = "Offense",
        bool selectionCaller = true,
        bool simulationCaller = false)
    {
        return SelectionPolicy.FindCircusFacility(
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
        var circusFacility = new Entry("Circus Facility", "CircusFacilityFlow", 100);
        var substation = new Entry("Substation", "SubstationFlow", 100);
        var mansion = new Entry("Haunted Mansion", "Level3Flow", 100);
        var pool = new List<Entry> { substation, circusFacility, mansion };

        int selectedIndex = Decide(pool);
        Require(selectedIndex == 1, "exact Circus Facility target index");
        Require(object.ReferenceEquals(pool[selectedIndex], circusFacility), "selected index must retain existing wrapper identity");
        Require(pool.Count == 3 && object.ReferenceEquals(pool[1], circusFacility), "pure policy mutated input");

        Require(Decide(pool, debug: false) == -1, "debugResults=false must remain normal");
        Require(Decide(pool, moon: "March") == -1, "non-Offense moon must remain normal");
        Require(Decide(pool, simulationCaller: true) == -1, "terminal simulation must remain normal");
        Require(Decide(pool, selectionCaller: false, simulationCaller: true) == -1,
            "terminal simulation exclusion must win without forcing a selection-caller refusal");

        ExpectSelectionRefusal(pool, selectionCaller: false, simulationCaller: false);
        ExpectSelectionRefusal(null);
        ExpectSelectionRefusal(new List<Entry>());
        ExpectSelectionRefusal(new List<Entry> { substation, mansion });
        ExpectSelectionRefusal(new List<Entry>
        {
            new Entry("Circus Facility", "CircusFacilityFlow", 100),
            new Entry("Circus Facility", "CircusFacilityFlow", 100)
        });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Circus Facility", "OtherFlow", 100) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Circus Facility", "CircusFacilityFlow", 65) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Circus Facility", "CircusFacilityFlow", 0) });
        ExpectSelectionRefusal(new List<Entry> { null, circusFacility });
        ExpectSelectionRefusal(new List<Entry> { circusFacility, null });

        ExpectInvalid(
            () => SelectionPolicy.FindCircusFacility(pool, true, "Offense", true, false, null,
                value => ((Entry)value).Asset, value => ((Entry)value).Rarity),
            "missing dungeon-name accessor");
        ExpectInvalid(
            () => SelectionPolicy.FindCircusFacility(pool, true, "Offense", true, false,
                value => ((Entry)value).Name, null, value => ((Entry)value).Rarity),
            "missing asset accessor");
        ExpectInvalid(
            () => SelectionPolicy.FindCircusFacility(pool, true, "Offense", true, false,
                value => ((Entry)value).Name, value => ((Entry)value).Asset, null),
            "missing rarity accessor");

        var independentA = new List<Entry>
        {
            new Entry("Substation", "SubstationFlow", 100),
            new Entry("Circus Facility", "CircusFacilityFlow", 100)
        };
        var independentB = new List<Entry>
        {
            new Entry("Circus Facility", "CircusFacilityFlow", 100),
            new Entry("Haunted Mansion", "Level3Flow", 100)
        };
        Require(Decide(independentA) == 1 && Decide(independentB) == 0, "independent repeated pools");
        Require(independentA.Count == 2 && independentB.Count == 2, "repeated decisions mutated pools");

        Console.WriteLine("PASS: S1.42AK-CFDIAG1 pure Circus Facility selector fail-closed policy.");
    }
}
