# 04 — Open Issues and Next Tests

## Highest priority — S1.42A runtime config-generation seed

S1.41 is accepted and remains the canonical gameplay baseline.

S1.42A has been built and automation-verified:
- `Profiles/LC V1 S1.42A Interior Config Seed.r2z`
- SHA-256 `70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`
- 188 total / 183 enabled / 5 disabled packages
- only `export.r2x` changed versus S1.41

Next isolated stage:
**run S1.42A to generate its real configs/registrations.**

Purpose:
- allow LLL/JLL/DawnLib/content mods to generate their real config sections and IDs;
- collect actual CullFactory identifiers and dependency/runtime behavior;
- regression-check the isolated LethalModDataLib reintroduction;
- avoid speculative deep tuning before that evidence exists.

Use the exact binding package list and rules in:
`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`

## S1.42A runtime procedure

After importing the generated S1.42A profile with Gale:

**Advanced options -> Import all files**

then:
1. reach Main Menu;
2. host/load a save;
3. land on at least one normal moon;
4. allow a dungeon to actually generate;
5. exit game.

Then upload to:
`RuntimeInbox/Current/`

Preferred evidence:
- complete `BepInEx/config/` directory as ZIP;
- full `LogOutput.log`;
- screenshots only for meaningful visual/runtime failures.

## New open issue — Mineshaft elevator + Pikmin crowding

Observed once in S1.41:
- many Pikmin were in the Mineshaft elevator with the player;
- player clipped through the elevator floor while descending;
- player died from fall damage;
- nearby log window contains many NavMesh-agent creation failures.

Current interpretation:
- real runtime issue worth tracking;
- not yet reproducible/proven;
- no evidence BCMER caused it;
- no proof yet that Pikmin collision physically pushed the player through the floor.

During future interior/elevator tests, specifically watch:
- large Pikmin groups entering moving elevators;
- player floor clipping;
- Pikmin NavMesh/agent failures during elevator movement.

## Monitor-only — outdoor Pikmin Sprout density

User reported a subjective impression that fewer outdoor Pikmin Sprouts may appear since CodeRebirth.

Current evidence does not support an immediate balance change:
- recent Offense runs were broadly consistent with the configured spawn chance;
- more Pikmin types and wider spatial distribution can make the same total feel sparser.

Only investigate statistically if the concern persists. Do not change spawn values from the impression alone.

## Monitor-only warning — BCMER ButlerSword

S1.41 emitted a ButlerSword missing-script warning. It did not prevent BCMER 1.71.0 from loading, selecting events, or passing the intended acceptance gate.

Only escalate if a Butler/ButlerSword-related event produces an actual gameplay failure.

## Carry-forward regression guards

Continue checking when naturally encountered:
- no natural Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- BCMER 1.71.0 stays pinned until a deliberate future migration;
- BCMER rain routes remain disabled;
- Ogopogo absent;
- Vermin absent;
- Autonomous Crane cannot kill Pikmin/Puffmin through CodeRebirth utility-kill path;
- GeneralImprovements recharge station performs desired full heal;
- Old Bird Resonance replacement works in a real encounter;
- Mirage `neverDeleteRecordings=true` remains active after import.

## Do not do yet

During S1.42A:
- do not upgrade BCMER to 2.0.0;
- do not fabricate interior IDs;
- do not normalize/tune guessed interior weights before generated configs exist;
- do not guess CullFactory identifiers;
- do not mix unrelated gameplay balancing into the config-seed build.


## Blocking — LethalModDataLib S1.42A initialization NRE

S1.42A runtime evidence reproduced a direct LethalModDataLib 1.2.2 initialization failure:

`NullReferenceException` in `ModDataAttributeCollector.RegisterModDataAttributes()`.

DULL content registered, but save/mod-data behavior is not cleanly validated. Resolve this before S1.42 final acceptance.

## S1.42 tuning inputs now available

- 26 new dungeon flow IDs captured.
- Total registered ExtendedDungeonFlows: 52.
- Exact CullFactory exception IDs: `junkrooms`, `shatteredrooms`.
- Generated LLL weights are available and need normalization where appropriate.
- Preserve explicit author restrictions, especially Shatteredrooms Experimentation/Embrion = 0.
- BCMER EventType distribution must be converted to fixed global user-selected percentages; exact values pending.

See `Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md`.


## Binding architecture — equal interior probability everywhere

User requirement:
- every registered interior should have the same effective selection probability as every other interior on every moon;
- future interior additions must be normalized into this architecture automatically;
- use common Weight 100 where the owning system supports it;
- package defaults/thematic preferences are not desired rarity rules.

Explicit hard blocks are compatibility questions, not desired balancing exceptions. Shatteredrooms' Experimentation/Embrion block remains protected until its technical necessity is understood and tested.

## Visual tuning — Melanie Mausoleum fog

Observed in S1.42A:
- `Mausoleum (MelanieMausoleum)` generated successfully;
- indoor fog was far too dense for the user; visibility was severely reduced.

Requirement:
- reduce fog **specifically inside MelanieMausoleum**;
- preserve some atmosphere if practical, but gameplay visibility takes priority;
- do not globally reduce fog in every interior.

The generated `MelanieMelicious.interior0.cfg` exposes interior/item toggles and values but no fog-density setting. Expect a targeted runtime/HDRP-volume compatibility patch or another interior-specific mechanism rather than a simple Melanie config edit. Investigate after the LethalModDataLib blocker.

## BCMER fixed EventType distribution

User selected a completely even global EventType distribution:
- Insane = 12.5
- VeryBad = 12.5
- Bad = 12.5
- Neutral = 12.5
- Good = 12.5
- VeryGood = 12.5
- Rare = 12.5
- Remove = 12.5

Keep `Use custom weights? = false`.

Use constant scales:
`12.5, 0, 12.5, 12.5`

for all eight EventTypes.

This removes difficulty/moon/day-based drift from the EventType base distribution. Event-specific eligibility, disabled events, incompatibilities, and mutual exclusions can still alter the effective pool in a particular run.
