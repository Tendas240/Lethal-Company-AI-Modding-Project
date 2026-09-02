# 13 — Runtime Evidence: S1.42A Interior Config Seed

**Evidence:** `RuntimeEvidence/S1.42A/20260902T224318Z/`  
**Candidate:** `Profiles/LC V1 S1.42A Interior Config Seed.r2z`  
**Candidate SHA-256:** `70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

## Seed result

The S1.42A runtime seed successfully reached Main Menu / host / landing / dungeon generation and produced a complete config archive plus LogOutput.

Runtime-generated files:
- `LogOutput.log` — SHA-256 `8d66e1dbc898ecb80938553ac7e1acc0f094f4e7bd27420dfff43122d00cd7f4`
- `config.zip` — SHA-256 `3334c4482960da9e89981eca660f41f8ee008a1485fffcd63460efb4ebac38c2`

The seed fulfilled its primary purpose: real dungeon registrations, flow IDs, weights and generated configs now exist.

## Registered dungeon delta

S1.41 registered 26 ExtendedDungeonFlows.

S1.42A registered 52 ExtendedDungeonFlows.

Exactly 26 new flows were added:

- Abandoned Foundry — `FoundryFlow`
- ACF Site — `ResearchStationFlow`
- DeepcoreMines — `deepmines`
- LiminalHouse — `LiminalHouseFlow`
- Supermarket — `Supermarket`
- Gray Apartments — `GrayApartmentsFlow`
- Zeranos Gray Apartments — `GrayApartmentsFlowZ`
- junkrooms — `junkrooms`
- Belleville Appartements — `BellevilleApp`
- Crimson Keep — `CrimsonKeep`
- Treatement Amenity — `DungeonTreatementAnemity`
- Goldstay Hotel — `GoldenHotel`
- Lead Factory — `LeadFactory`
- Lantern Manor — `LanternManor`
- Mausoleum — `MelanieMausoleum`
- Museum — `MelanieMuseum`
- Raven Manor — `RavenFlow`
- Shatteredrooms — `shatteredrooms`
- Spelunkers Caverns (Random) — `Spelunk_RandomFlow`
- Spelunkers Caverns (Basic) — `Spelunk_BasicFlow`
- Spelunkers Caverns (Crystal) — `Spelunk_CrystalFlow`
- Spelunkers Caverns (Frozen) — `Spelunk_FrozenFlow`
- Spelunkers Caverns (Magmatic) — `Spelunk_MagmaFlow`
- Spelunkers Caverns (Overgrown) — `Spelunk_OvergrownFlow`
- Studio Floor — `StudioFlow`
- Sub Systems — `SubSysFlow`

## Actual generation

On Offense, LethalLevelLoader selected and generated:

`Mausoleum (MelanieMausoleum)`

The log records:
- viable/unviable dungeon matching;
- New Day History: Offense / Mausoleum;
- CullFactory preparing tile information for `MelanieMausoleum`;
- normal runtime activity inside the generated interior.

No dungeon-generation crash occurred.

## Generated weights are not normalized yet

The Offense matching report demonstrates why S1.42 tuning is required.

Examples:
- LiminalHouse = 300
- Abandoned Foundry = 250
- Mausoleum = 100
- Museum = 100
- Shatteredrooms = 75
- Lead Factory = 70
- DeepcoreMines = 25
- Belleville Appartements = 20
- Goldstay Hotel = 20

Some interiors are intentionally unviable on Offense based on author defaults.

Shatteredrooms generated configuration confirms the author restriction is preserved:
- Experimentation = 0
- Embrion = 0

Do not overwrite such explicit safety restrictions when normalizing ordinary weights.

## CullFactory

Generated `com.fumiko.CullFactory.cfg` currently has:

`Disable culling for interiors =`

empty.

Exact runtime flow IDs are now known:
- Junkrooms: `junkrooms`
- Shatteredrooms: `shatteredrooms`

Therefore the final S1.42 tuning can use the exact disable-culling list without guessing.

## LethalModDataLib regression — important

`MaxWasUnavailable.LethalModDataLib 1.2.2` loaded, patched, and then failed during initialization:

`System.NullReferenceException`

in:

`LethalModDataLib.Features.ModDataAttributeCollector.RegisterModDataAttributes()`

via:

`LethalModDataLib.Patches.InitializeGamePatches.StartPostfix()`

This error did not exist in accepted S1.41 because LethalModDataLib was absent there.

DULL interiors still registered, but save/mod-data behavior cannot be considered cleanly validated while this initialization failure exists.

Treat as a blocking S1.42 design issue, not as an accepted warning.

## Other log comparison

The SoundAPI `TypeLoadException` during `RoundManager.GenerateNewFloor` also occurs in accepted S1.41 and is therefore not a new S1.42A regression.

A new AdditionalNetworking fatal was logged during disconnect:

`NetworkObjectReference can only be created from spawned NetworkObjects.`

It occurred while the scene was tearing down. Track it, but do not attribute it to LethalModDataLib or the interiors without additional evidence.

Unity duplicate NetworkPrefab hash errors increased with the expanded interior content. The run continued and LLL explicitly skipped already-registered NetworkObjects. Track only if a corresponding gameplay/network failure appears.

## Boom_Scraps

A generated JLL config file named:

`JLL/BoomsMods.BoomScraps.cfg`

exists, but the S1.42A manifest does not contain Boom_Scraps and the runtime log does not show a Boom_Scraps plugin load.

Therefore the presence of this config file alone is not evidence that Boom_Scraps is installed.

## BCMER follow-up requirement

User now requires fixed global EventType probabilities independent of moon and elapsed days.

Keep:

`Use custom weights? = false`

because BCMER's EventType-weight path is the desired mechanism.

For each EventType, use a constant scale:

`P, 0, P, P`

where P is the user-selected global percentage/weight.

Pending user values:
- Insane
- VeryBad
- Bad
- Neutral
- Good
- VeryGood
- Rare
- Remove

Prefer values summing to 100.

Do not switch `Use custom weights?` to true; that switches BCMER to per-event Custom Weight values rather than global EventType distribution.

## Current decision

S1.42A is a successful **config-generation seed**, but it is **not a clean accepted gameplay baseline**.

Accepted gameplay baseline remains S1.41.

Before S1.42 final:
1. decide how to handle the LethalModDataLib initialization NRE / DULL dependency;
2. set exact user-selected BCMER fixed EventType percentages;
3. tune new interior weights using generated IDs/configs;
4. set CullFactory exceptions for `junkrooms` and `shatteredrooms`;
5. preserve explicit author safety restrictions;
6. build and runtime-test S1.42.
