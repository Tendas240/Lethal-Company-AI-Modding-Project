using System;
using System.Collections;
using System.Collections.Generic;
using S142AJDiag1OfficeSelection;

static class Program
{
    sealed class Entry
    {
        internal string Name, Asset;
        internal int Rarity;
        internal Entry(string name, string asset, int rarity) { Name=name; Asset=asset; Rarity=rarity; }
    }
    static int Decide(IList pool, bool debug=true, string moon="Offense", bool caller=true)
        => SelectionPolicy.FindOffice(pool, debug, moon, caller,
            x => ((Entry)x).Name, x => ((Entry)x).Asset, x => ((Entry)x).Rarity);
    static void Require(bool ok) { if (!ok) throw new Exception("Regression assertion failed"); }
    static void Refuse(IList pool)
    {
        var before=new object[pool.Count]; pool.CopyTo(before,0);
        bool refused=false;
        try { Decide(pool); } catch (InvalidOperationException) { refused=true; }
        Require(refused && pool.Count==before.Length);
        for(int i=0;i<before.Length;i++) Require(Object.ReferenceEquals(pool[i],before[i]));
    }
    static void Main()
    {
        var office=new Entry("LC Office","OfficeDungeonFlow",100);
        var facility=new Entry("Facility","Level1Flow",100);
        var pool=new List<Entry>{facility,office};
        Require(Decide(pool)==1 && pool.Count==2 && office.Rarity==100);
        Require(Decide(pool,debug:false)==-1);
        Require(Decide(pool,moon:"Experimentation")==-1);
        Require(Decide(pool,caller:false)==-1); // Terminal simulation.
        Refuse(new List<Entry>{facility});
        Refuse(new List<Entry>{office,office});
        Refuse(new List<Entry>{new Entry("LC Office","OtherFlow",100)});
        Refuse(new List<Entry>{new Entry("LC Office","OfficeDungeonFlow",65)});
        Refuse(new List<Entry>{new Entry("LC Office","OfficeDungeonFlow",0)});
        Refuse(new List<Entry>{null,office});
        Refuse(new List<Entry>());
        Require(Decide(pool)==1); // Repeated invocation retains input.
        Console.WriteLine("PASS: selection boundary, duplicate/missing/identity/rarity refusal, input preservation and repetition.");
    }
}
