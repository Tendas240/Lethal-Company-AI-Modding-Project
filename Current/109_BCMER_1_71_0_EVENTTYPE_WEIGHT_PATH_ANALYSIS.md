# 109 — BCMER 1.71.0 EventType Weight Path Analysis

**Date:** 2026-09-04  
**Status:** ANALYSIS COMPLETE  
**Accepted gameplay baseline remains:** S1.42AB  
**S1.42AC remains formally rejected / not promoted pending corrected acceptance interpretation**

## Scope

This document resolves the post-S1.42AC analysis gate defined by `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` and the current handover.

The question was: what exact BCMER `1.71.0` path produces:

`Set eventType weight for <type> to <value>`

and why did equal configured EventType scales produce unequal logged values?

## Exact upstream version resolved

The exact BCMER source commit corresponding to version `1.71.0` is:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `BrutalCompanyMinus/Plugin.cs` declares:

`VERSION = "1.71.0"`

The project profile independently contains exact Thunderstore package:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not substitute current upstream `2.x` source for this contract.

## Exact calculation path

In exact BCMER `1.71.0`, `EventManager.UpdateAllEventWeights()` performs the following when `Use custom weights? = false`:

1. Compute each configured EventType scale using `MEvent.Scale.Compute()`.
2. Sum all eight computed scales.
3. Normalize each scale into `eventTypeProbabilities[i]`.
4. Read `eventTypeCount[i]`, the number of enabled events of that type in `EventManager.events`.
5. Read `eventTypeSum`, the total number of enabled events across all eight types.
6. Compute one integer weight that is assigned to **every individual event of that type**:

```text
newEventWeights[i] = (int)(
    (eventTypeSum / fix(eventTypeCount[i]))
    * eventTypeProbabilities[i]
    * 1000.0f
)
```

7. Assign that per-event value to each enabled event:

```text
foreach (MEvent e in events)
    e.Weight = newEventWeights[(int)e.Type];
```

`UpdateEventTypeCounts()` proves the meaning of the two count terms:

```text
eventTypeCount[type] = number of enabled events of that type
eventTypeSum         = sum of all eventTypeCount values
```

The configuration loader builds `EventManager.events` from enabled events and places disabled entries in `disabledEvents` before the counts and weights are calculated.

## The key semantic correction

The log message:

`Set eventType weight for Rare to 27375`

is misleading if read as the **aggregate weight of the Rare EventType**.

It is actually the **per-event weight assigned to every enabled Rare event**.

BCMER's later `RandomWeightedEvent()` does not select an EventType object. It sums the `Weight` of every individual `MEvent` in the current candidate list and selects an individual event proportionally to that weight.

Therefore a type with many events must receive a smaller per-event weight than a type with few events if both types are intended to have the same aggregate probability mass.

This inverse-count factor is deliberate:

```text
perEventWeight_i ≈ (N / n_i) * p_i * 1000
aggregateTypeMass_i ≈ n_i * perEventWeight_i
                    ≈ N * p_i * 1000
```

where:

- `N = eventTypeSum`;
- `n_i = eventTypeCount[i]`;
- `p_i = eventTypeProbabilities[i]`.

The `n_i` term therefore cancels when the aggregate mass of the type is considered.

## S1.42AC specifically

S1.42AC configured all eight scales as:

`12.5, 0.0, 12.5, 12.5`

The BCMER randomizer is disabled in the S1.42AC profile, and `Use custom weights? = false` is preserved.

Therefore for every difficulty:

```text
computedScale_i = 12.5
sum             = 100
p_i             = 0.125
```

The observed AC values were:

| EventType | Logged per-event weight |
| --- | ---: |
| Insane | 6843 |
| VeryBad | 506 |
| Bad | 355 |
| Neutral | 1368 |
| Good | 1244 |
| VeryGood | 2737 |
| Rare | 27375 |
| Remove | 883 |

These values are not evidence that the eight EventTypes received those aggregate masses. They are exactly the kind of inverse-count weights this algorithm is designed to emit.

The observed values are consistent with the 219-event active-pool solution:

| EventType | Enabled events `n_i` | Per-event weight | Aggregate integer mass `n_i * weight` | Share of aggregate integer pool |
| --- | ---: | ---: | ---: | ---: |
| Insane | 4 | 6843 | 27372 | 12.5057% |
| VeryBad | 54 | 506 | 27324 | 12.4837% |
| Bad | 77 | 355 | 27335 | 12.4887% |
| Neutral | 20 | 1368 | 27360 | 12.5002% |
| Good | 22 | 1244 | 27368 | 12.5038% |
| VeryGood | 10 | 2737 | 27370 | 12.5047% |
| Rare | 1 | 27375 | 27375 | 12.5070% |
| Remove | 31 | 883 | 27373 | 12.5061% |

Counts sum to `219`; aggregate integer mass sums to `218877`.

The small residual spread (`12.4837%` to `12.5070%`, about `0.0233` percentage points) comes from the final integer cast/truncation of each per-event weight. It is not the huge category imbalance implied by comparing `6843` directly with `506` or `27375`.

## Additional factors identified

### Type-dependent factor that explains the AC log values

**`eventTypeCount[i]` — the number of enabled events of that type.**

This is the principal additional type-dependent factor missing from the original S1.42AC acceptance model.

### Global factors

- `eventTypeSum` — total enabled events;
- normalized `eventTypeProbabilities[i]` from the configured scales;
- `* 1000.0f` scale factor;
- integer truncation when converting to `int`.

### Difficulty

`MEvent.Scale.Compute()` normally uses:

`Base + Increment * difficulty`, clamped by Min/Max caps.

For S1.42AC this is neutralized by constant `12.5 / 0 / 12.5 / 12.5`, so difficulty cannot create the observed type differences.

### Randomizer

`UpdateAllEventWeights()` can randomize weights when the BCMER randomizer and weight randomization are enabled.

In the S1.42AC profile both are disabled, so this branch does not explain or perturb AC.

## Selection-stage factors after the static weights are assigned

`ChooseEvents()` starts from the weighted list of individual enabled events, but the final executed event set can still be altered by event-specific runtime eligibility and without-replacement behavior:

- `AddEventIfOnly()` rejection;
- moon whitelist/blacklist rejection;
- Special/Beta event gating;
- forced-event removals;
- removal of the event after it is chosen;
- `EventsToRemove` incompatibility removal;
- `EventsToSpawnWith` side-event handling;
- repeated draws for multiple events in the same round.

These factors mean that "configured EventType probability" and "long-run final executed EventType frequency under every moon/state/eligibility combination" are not mathematically identical concepts.

A patch that blindly forces the eight **per-event** logged weights to the same number would be wrong: types containing many events would then receive proportionally more aggregate probability mass.

## Corrected interpretation of S1.42AC

The original S1.42AC runtime gate treated equality of the eight logged `Set eventType weight ...` values as proof of equal EventType probability.

That gate was semantically incorrect.

For the static enabled-event pool, BCMER `1.71.0` intentionally uses unequal per-event weights to realize the normalized EventType probabilities while compensating for unequal EventType populations.

Therefore:

- equal EventType scales **do** produce equal target EventType probabilities (`12.5%` each) in BCMER's own probability model;
- unequal `Set eventType weight ...` log values are expected and necessary when type populations differ;
- the AC runtime values are consistent with the inverse-count normalization algorithm;
- the remaining static aggregate inequality is only integer-truncation noise, not the previously inferred major imbalance.

## Successor implementation decision

**Do not implement inverse config compensation.**

There is no hidden multiplier that needs to be counteracted by giving the eight config scales different values. Doing so would fight BCMER's deliberate type-population normalization.

**Do not implement a project-local patch that forces the eight logged per-event values equal.**

That would create a severe population bias in favor of EventTypes with many enabled events.

**Do not arm a new successor build for this purpose.**

The safest implementation for the intended BCMER EventType target remains the existing S1.42AC config concept: equal constant EventType scales with BCMER `1.71.0` retaining ownership of the per-event normalization.

S1.42AC is not silently promoted by this analysis. It remains formally rejected/not accepted until the project explicitly applies a **corrected acceptance interpretation** to the already-existing artifact and runtime evidence.

No new code/config successor is justified by the weight-path analysis itself.

## Correct future acceptance model

If S1.42AC is reconsidered, the primary gate must no longer require the eight per-event log values to be equal.

The correct checks are:

1. exact BCMER `1.71.0` loaded;
2. `Use custom weights? = false`;
3. randomizer/weight randomization disabled for this deterministic target;
4. all eight computed EventType scales resolve to `12.5`;
5. source/runtime event counts and emitted per-event weights satisfy the exact BCMER formula;
6. aggregate type masses `eventTypeCount[i] * emittedWeight[i]` are approximately equal, with only expected integer-truncation error;
7. ordinary event eligibility, rain-route disables and all S1.42AB invariants remain intact.

If the project later requires **exact long-run 12.5% final executed frequency after all event-specific eligibility filters**, that is a different and materially broader requirement. It would require redesigning/normalizing the dynamic eligible pool during `ChooseEvents()` and should not be attempted as a casual compensation patch.

## Current state after analysis

- canonical accepted gameplay baseline: `S1.42AB`;
- S1.42AC artifact remains rejected/not promoted for now;
- S1.42AC original rejection **interpretation is superseded by this source-path analysis**;
- no runtime test is currently outstanding;
- no successor is armed;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AB`;
- `BuildSpecs/current.json` must remain disabled.

## Source provenance

Exact upstream source used for this analysis:

- repository: `TheSoftDiamond/BrutalCompanyMinusExtraReborn`;
- commit: `e2ca64b9954b7076e75e9a9ff97d76232c4086b0`;
- `BrutalCompanyMinus/Plugin.cs` — confirms `VERSION = "1.71.0"`;
- `BrutalCompanyMinus/Minus/EventManager.cs` — `UpdateAllEventWeights()`, `UpdateEventTypeCounts()`, `RandomWeightedEvent()`, `ChooseEvents()`;
- `BrutalCompanyMinus/Minus/MEvent.cs` — `Scale.Compute()`.

Project-local evidence:

- `ProfileSources/S1.42AC/export.r2x` — exact BCMER package version;
- `ProfileSources/S1.42AC/BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg`;
- `ProfileSources/S1.42AC/BepInEx/config/BrutalCompanyMinusExtraReborn/CoreProperties.cfg`;
- `RuntimeEvidence/S1.42AC/20260904T181854Z/`;
- `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.
