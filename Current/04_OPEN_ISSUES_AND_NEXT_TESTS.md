# 04 — Open Issues and Next Tests

## Accepted baseline — S1.42AB

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

S1.42AB remains the canonical accepted gameplay baseline.

## S1.42AC — formal status and corrected interpretation

**S1.42AC — BCMER EventType Equal Distribution — FORMALLY REJECTED / NOT ACCEPTED / NOT PROMOTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Original rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Completed analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`

The rejection decision remains historical evidence, but the original primary gate interpretation is superseded.

### Exact BCMER 1.71.0 path

Exact upstream commit:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `Plugin.cs` declares `VERSION = "1.71.0"`.

BCMER calculates normalized EventType probabilities and then assigns a per-event weight:

```text
perEventWeight_i = int((eventTypeSum / fix(eventTypeCount[i])) * eventTypeProbability_i * 1000)
```

The logged `Set eventType weight for <type> to <value>` value is therefore a **per-event** weight, not aggregate type mass.

S1.42AC uses eight constant scales of `12.5`, so BCMER's static target probabilities are `0.125` each. The observed unequal values:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

are expected inverse-count weights for EventTypes containing different numbers of enabled events.

The 219-event solution reconstructs type counts `4 / 54 / 77 / 20 / 22 / 10 / 1 / 31`. After multiplying count × per-event weight, aggregate static shares are approximately `12.4837%` to `12.5070%`; the small spread is integer truncation.

### Corrected implementation decision

Do **not**:

- build a successor that gives the eight EventType scales different inverse-compensation values merely to equalize the log numbers;
- patch BCMER to force the eight per-event log values equal;
- treat unequal per-event values as failure of equal EventType probability.

No successor implementation is justified by this analysis. The existing S1.42AC equal-scale concept is the correct static EventType-probability approach under BCMER ownership.

S1.42AC is still not silently promoted. S1.42AB remains the accepted baseline until an explicit corrected acceptance decision is made.

### Dynamic selection caveat

Final executed frequencies can be affected after static weighting by:

- `AddEventIfOnly()`;
- moon whitelist/blacklist;
- Special/Beta gating;
- forced-event removal;
- event removal after selection;
- `EventsToRemove`;
- `EventsToSpawnWith`;
- repeated without-replacement draws.

Therefore exact long-run `12.5%` executed frequency after all eligibility filters is a separate broader requirement, not the same as equal static BCMER EventType probability.

## Current next work

**No runtime test is currently outstanding. No successor is armed. No compensation build should be created.**

If the BCMER EventType scope continues, the next action is to apply the corrected acceptance model in `Current/109` to the **existing S1.42AC artifact and evidence**. The eight per-event log values must not be required to be identical.

No PowerShell uploader is required now because there is no pending runtime test.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`;
- guarded base = accepted S1.42AB;
- output = `Profiles/DO_NOT_BUILD.r2z`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## AC preserved regression evidence

The existing AC runtime still showed:

- normal BCMER event execution active;
- S1.42AB interior normalization healthy;
- Offense final viable pool 40 entries, all positive effective rarities `100`;
- `Mausoleum` generated successfully;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference regression `0`;
- PikminNoticeZone regression `0`;
- Fatal `0`.

Secondary AC evidence still contains 43 dominant NavMeshAgent:SetDestination error signatures and 26 LethalMin route-failure signatures. Treat these separately as interior/Pikmin routing evidence; do not attribute them causally to the BCMER config-only change without reproducibility.

## Deferred separate scopes

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.

## Planned repository information-architecture overhaul

Planned/binding but **not executed**. Entry: `OVERHAUL_START_HERE_ChatGPT.txt`. Re-resolve the then-current state and create/verify the required separate standalone pre-overhaul backup repository before structural migration.

## Permanent invariants

Preserve exact BCMER `1.71.0`, accepted rain disables, EnemyIsolation off, Compatibility Fixes `1.3.14`, BaboonBirdPikminEnemy enabled, narrow Hawk -> Pikmin prevention only, inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack, Puffer protection, Thumper Bite Limit `3`, Crawler absent from Attack Blacklist, accepted S1.42C moon power/spawn baseline, `Consistent Spawn Times = true`, accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning, and accepted S1.42AB post-viability interior normalization.

Never repeat S1.42R's whole-component disable approach.
