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
