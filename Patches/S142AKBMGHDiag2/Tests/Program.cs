using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using S142AKBMGHDiag2;

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

        ExpectInvalid(() => Decide(pool, selectionCaller: selectionCaller, simulationCaller: simulationCaller), "selection");
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

    static string Hash(byte[] data)
    {
        using SHA256 sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(data)).ToLowerInvariant();
    }

    static void TestProvenance()
    {
        string root = Path.Combine(Path.GetTempPath(), "s142ak-bmghdiag2-" + Guid.NewGuid().ToString("N"));
        string nestedOnly = Path.Combine(Path.GetTempPath(), "s142ak-bmghdiag2-nested-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(root);
        Directory.CreateDirectory(Path.Combine(nestedOnly, "nested"));
        try
        {
            byte[] bytes = Encoding.UTF8.GetBytes("installed-v81-test-bytes");
            string expected = Hash(bytes);
            File.WriteAllBytes(Path.Combine(root, "Assembly-CSharp.dll"), bytes);
            File.WriteAllBytes(Path.Combine(nestedOnly, "nested", "Assembly-CSharp.dll"), bytes);

            Require(GameAssemblyProvenance.Validate(root, expected) == expected, "valid exact managed source path/hash");
            ExpectInvalid(() => GameAssemblyProvenance.Validate("", expected), "blank managed path");
            ExpectInvalid(() => GameAssemblyProvenance.Validate(Path.Combine(root, "missing-dir"), expected), "missing managed directory");
            ExpectInvalid(() => GameAssemblyProvenance.Validate(nestedOnly, expected), "no recursive/fallback assembly search");
            ExpectInvalid(() => GameAssemblyProvenance.Validate(root, new string('0', 64)), "wrong installed SHA");
            ExpectInvalid(() => GameAssemblyProvenance.Validate(root, expected, _ => throw new UnauthorizedAccessException("test")), "unreadable exact file");
        }
        finally
        {
            Directory.Delete(root, true);
            Directory.Delete(nestedOnly, true);
        }
    }

    static void TestRuntimeIdentity()
    {
        RuntimeIdentityPolicy.ValidateAssemblyIdentity("EntranceTeleport", "Assembly-CSharp", false, "Assembly-CSharp.dll");
        RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(true, false, 0, "System.Void", true);

        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateAssemblyIdentity("Other", "Assembly-CSharp", false, "Assembly-CSharp.dll"), "wrong runtime type");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateAssemblyIdentity("EntranceTeleport", "Other", false, "Assembly-CSharp.dll"), "wrong runtime assembly");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateAssemblyIdentity("EntranceTeleport", "Assembly-CSharp", true, "Assembly-CSharp.dll"), "dynamic runtime assembly");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateAssemblyIdentity("EntranceTeleport", "Assembly-CSharp", false, "Other.dll"), "wrong manifest module");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(false, false, 0, "System.Void", true), "non-public TeleportPlayer");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(true, true, 0, "System.Void", true), "static TeleportPlayer");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(true, false, 1, "System.Void", true), "TeleportPlayer parameters");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(true, false, 0, "System.Boolean", true), "TeleportPlayer return type");
        ExpectInvalid(() => RuntimeIdentityPolicy.ValidateTeleportMethodIdentity(true, false, 0, "System.Void", false), "TeleportPlayer body missing");
    }

    static void Main()
    {
        TestProvenance();
        TestRuntimeIdentity();

        var greenhouse = new Entry("Greenhouse", "GreenhouseFlow", 100);
        var facility = new Entry("Facility", "Level1Flow", 100);
        var pool = new List<Entry> { facility, greenhouse };

        Require(Decide(pool) == 1, "exact Greenhouse target index");
        Require(pool.Count == 2 && greenhouse.Rarity == 100, "pure selection policy mutated input");
        Require(Decide(pool, debug: false) == -1, "debugResults=false must remain normal");
        Require(Decide(pool, moon: "Offense") == -1, "other moon must remain normal");
        Require(Decide(pool, simulationCaller: true) == -1, "terminal simulation must remain normal");
        ExpectSelectionRefusal(pool, selectionCaller: false, simulationCaller: false);
        ExpectSelectionRefusal(null);
        ExpectSelectionRefusal(new List<Entry>());
        ExpectSelectionRefusal(new List<Entry> { facility });
        ExpectSelectionRefusal(new List<Entry> { greenhouse, greenhouse });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Greenhouse", "OtherFlow", 100) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Greenhouse", "GreenhouseFlow", 65) });
        ExpectSelectionRefusal(new List<Entry> { new Entry("Greenhouse", "GreenhouseFlow", 0) });
        ExpectSelectionRefusal(new List<Entry> { null, greenhouse });

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

        Console.WriteLine("PASS: C3F18 BMGHDIAG2 provenance/runtime-identity plus preserved selection/traversal/topology policies.");
    }
}
