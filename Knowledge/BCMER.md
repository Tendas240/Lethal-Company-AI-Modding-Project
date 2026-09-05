# BCMER — BrutalCompanyMinusExtraReborn

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current BCMER package/config/weight-model interpretation  
**Canonical-For:** `bcmer`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`, `Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md`, `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json`, `Current/INTEGRITY_ERRATA_REGISTRY.json`, S1.42AC ProfileSources/runtime evidence  
**Related:** `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Version invariant

Use exact Thunderstore package:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not silently migrate to 2.x. Any 2.x adoption is a separate explicit compatibility project.

Exact upstream source used for the current weight-model analysis:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `BrutalCompanyMinus/Plugin.cs` declares `VERSION = "1.71.0"`.

## Permanent ownership/config guards

Keep BCMER event operation active while preventing it from silently owning the project's normal spawn/power architecture outside events:

- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Accepted BCMER rain-event routes remain disabled:

- `Raining`
- `HeavyRain`
- `AllWeather`
- `Hurricane`

Natural vanilla Rainy weather remains allowed. The requirement concerns BCMER event routes, not all rain in the game.

## Accepted equal EventType static model — S1.42AC

The accepted static base distribution is eight EventTypes at equal probability. S1.42AC implements constant scales:

`12.5, 0.0, 12.5, 12.5`

for every type with:

- `Use custom weights? = false`
- BCMER randomizer disabled
- `Randomize Event Weights? = false`

BCMER 1.71.0 then computes:

```text
p_i = computedScale_i / sum(computedScales)
perEventWeight_i = int((eventTypeSum / fix(eventTypeCount[i])) * p_i * 1000)
```

The logged `Set eventType weight for <type> to <value>` value is a **per-event** weight assigned to every enabled event of that type. It is not the aggregate EventType mass.

With all eight scales at 12.5, `p_i = 0.125` for every EventType. Unequal per-event log values are expected because the number of enabled events per type differs.

## S1.42AC corrected interpretation and acceptance

Observed and freshly reproduced per-event values:

- Insane 6843
- VeryBad 506
- Bad 355
- Neutral 1368
- Good 1244
- VeryGood 2737
- Rare 27375
- Remove 883

are consistent with enabled counts `4 / 54 / 77 / 20 / 22 / 10 / 1 / 31` (219 total). Count × per-event-weight gives aggregate static shares approximately `12.4837%` through `12.5070%`; the small spread is integer truncation.

Therefore the original S1.42AC rejection criterion requiring the eight logged values to be equal was technically invalid. `Current/106...` remains historical evidence of that original decision; `Current/109...` corrected its interpretation, and `Current/118...` explicitly accepted S1.42AC after fresh runtime confirmation.

Do **not**:

- inverse-compensate the config scales to make those log values match;
- patch BCMER to force equal per-event values;
- infer a massive EventType imbalance directly from the raw per-event values.

Either approach would bias types with more individual events.

## S1.42AC runtime byte provenance

### Original runtime evidence

The authoritative raw `LogOutput.log` SHA-256 for:

`RuntimeEvidence/S1.42AC/20260904T181854Z/`

is:

`fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`

Authority: `RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json` plus direct byte recomputation in permanent CI.

The older `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0` value is **superseded incorrect historical metadata**, not current byte authority. Its retained occurrences are classified by `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json` and the central `Current/INTEGRITY_ERRATA_REGISTRY.json`.

### Fresh acceptance runtime evidence

The fresh corrected-model confirmation run is:

`RuntimeEvidence/S1.42AC/20260904T235720Z/`

with raw-log SHA-256:

`98170374c4ffb6f40322a8019ad7f7f807e900525717dfdf7e70698bd7f28fa8`

It loaded exact BCMER `1.71.0`, reproduced the expected inverse-population per-event weights, retained project-critical regression markers at zero, and had no user-reported problematic gameplay behavior. Detailed acceptance is `Current/118...`.

## Accepted S1.42AC gate

S1.42AC passed the corrected acceptance model:

1. exact BCMER 1.71.0 loaded;
2. `Use custom weights? = false`;
3. randomization disabled for the deterministic target;
4. all eight computed scales resolve to 12.5;
5. emitted per-event weights satisfy the exact formula for the enabled event counts;
6. aggregate count × per-event-weight masses are approximately equal with only integer-truncation error;
7. rain disables, ordinary eligibility and inherited S1.42AB invariants remain healthy.

S1.42AC is therefore the current accepted full-normal-stack baseline for this static EventType probability requirement.

## Static probability versus executed frequency

Final executed EventType frequency can differ from the static configured probability because `ChooseEvents()` applies event-specific/runtime behavior including:

- `AddEventIfOnly()`;
- moon whitelist/blacklist;
- Special/Beta gating;
- forced-event removal;
- removal after selection / without-replacement draws;
- `EventsToRemove` incompatibilities;
- `EventsToSpawnWith` side-event handling;
- multiple draws per round.

A requirement for mathematically exact long-run 12.5% **executed** frequency after all such filters is a separate algorithm-design scope. Do not treat it as a config correction to the accepted static weighting path.
