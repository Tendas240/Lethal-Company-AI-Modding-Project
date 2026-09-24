using System;
using S142AKBMDSFix1;

static class Program
{
    private static int _tests;

    private static void Main()
    {
        Expect("target 4.875 clamps", "Black Mesa", "DeepSewersFlow", 4.875f, 1.0f, true);
        Expect("target 1.01 clamps", "Black Mesa", "DeepSewersFlow", 1.01f, 1.0f, true);
        Expect("target 1 unchanged", "Black Mesa", "DeepSewersFlow", 1.0f, 1.0f, false);
        Expect("target below 1 unchanged", "Black Mesa", "DeepSewersFlow", 0.8f, 0.8f, false);
        Expect("other moon unchanged", "Offense", "DeepSewersFlow", 4.875f, 4.875f, false);
        Expect("other flow unchanged", "Black Mesa", "GreenhouseFlow", 4.875f, 4.875f, false);
        Expect("moon comparison is exact", "black mesa", "DeepSewersFlow", 4.875f, 4.875f, false);
        Expect("flow comparison is exact", "Black Mesa", "deepsewersflow", 4.875f, 4.875f, false);
        ExpectSpecial("NaN preserved", float.NaN);
        ExpectSpecial("positive infinity preserved", float.PositiveInfinity);
        ExpectSpecial("negative infinity preserved", float.NegativeInfinity);

        Console.WriteLine($"BMDSFIX1 policy tests passed: {_tests}");
    }

    private static void Expect(string name, string moon, string flow, float input, float expected, bool expectedApplied)
    {
        float actual = SizeClampPolicy.Apply(moon, flow, input, out bool applied);
        _tests++;
        if (actual != expected || applied != expectedApplied)
            throw new InvalidOperationException($"{name}: expected value={expected:R}, applied={expectedApplied}; actual value={actual:R}, applied={applied}");
    }

    private static void ExpectSpecial(string name, float input)
    {
        float actual = SizeClampPolicy.Apply("Black Mesa", "DeepSewersFlow", input, out bool applied);
        _tests++;
        if (applied || (float.IsNaN(input) ? !float.IsNaN(actual) : actual != input))
            throw new InvalidOperationException($"{name}: special value was not preserved.");
    }
}
