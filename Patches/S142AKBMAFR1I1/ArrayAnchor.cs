using System;
using System.Diagnostics;
using System.Threading;
using UnityEngine;

namespace S142AKBMAFR1I1
{
    internal static class ArrayAnchor
    {
        internal const string Signature = "Array index (0) is out of bounds (size=0)";
        internal static int Active;
        internal static long Count, FirstUtc, LastUtc, FirstMono, LastMono, EmptyStacks, NonemptyStacks;
        internal static int TypeMask;

        // This threaded callback must remain atomic capture only. No Unity-object
        // APIs, logging, observer invocation, or gameplay code is permitted here.
        internal static void Capture(string condition, string stackTrace, LogType type)
        {
            if (Volatile.Read(ref Active) == 0 || condition != Signature) return;
            long utc = DateTime.UtcNow.Ticks;
            long mono = Stopwatch.GetTimestamp();
            Min(ref FirstUtc, utc); Max(ref LastUtc, utc);
            Min(ref FirstMono, mono); Max(ref LastMono, mono);
            if (string.IsNullOrEmpty(stackTrace)) Interlocked.Increment(ref EmptyStacks);
            else Interlocked.Increment(ref NonemptyStacks);
            int before, after;
            do { before = Volatile.Read(ref TypeMask); after = before | (1 << (int)type); }
            while (Interlocked.CompareExchange(ref TypeMask, after, before) != before);
            Interlocked.Increment(ref Count);
        }

        private static void Min(ref long field, long value)
        {
            long before;
            do { before = Interlocked.Read(ref field); if (before != 0 && before <= value) return; }
            while (Interlocked.CompareExchange(ref field, value, before) != before);
        }
        private static void Max(ref long field, long value)
        {
            long before;
            do { before = Interlocked.Read(ref field); if (before >= value) return; }
            while (Interlocked.CompareExchange(ref field, value, before) != before);
        }

        internal static string Summary()
        {
            return "count=" + Interlocked.Read(ref Count) + " firstUtcTicks=" + Interlocked.Read(ref FirstUtc)
                + " lastUtcTicks=" + Interlocked.Read(ref LastUtc) + " firstMono=" + Interlocked.Read(ref FirstMono)
                + " lastMono=" + Interlocked.Read(ref LastMono) + " logTypeMask=" + Volatile.Read(ref TypeMask)
                + " emptyStacks=" + Interlocked.Read(ref EmptyStacks) + " nonemptyStacks=" + Interlocked.Read(ref NonemptyStacks)
                + " timestampFields=independent_atomic_extrema emitter=UNPROVEN";
        }
    }
}
