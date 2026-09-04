# 00 — Current State

**Updated:** 2026-09-04 — S1.42AB accepted; S1.42AC formally rejected/not promoted; BCMER 1.71.0 weight-path analysis complete  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the Source of Truth.**

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Accepted interior architecture: LethalLevelLoader `1.7.12` owns viable/excluded flow membership first; S1.42AB then normalizes every positive rarity in the returned viable list to exactly `100` without adding/removing/re-registering flows. Accepted Offense runtime preserved all 40 viable entries, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

Authoritative marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## S1.42AC formal status

**S1.42AC — BCMER EventType Equal Distribution — FORMALLY REJECTED / NOT ACCEPTED / NOT PROMOTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Original rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Completed source-path analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`

The historical rejection decision is preserved. However, its **primary acceptance interpretation has been superseded** by exact BCMER `1.71.0` source analysis.

## Exact BCMER 1.71.0 finding

Exact upstream source commit:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `Plugin.cs` declares `VERSION = "1.71.0"`.

With `Use custom weights? = false`, BCMER computes:

```text
p_i = computedScale_i / sum(computedScales)
perEventWeight_i = int((eventTypeSum / fix(eventTypeCount[i])) * p_i * 1000)
```

`eventTypeCount[i]` is the number of enabled individual events of the EventType; `eventTypeSum` is the total enabled-event count. BCMER assigns the resulting value to **every individual event of that type**.

Therefore the logged line:

`Set eventType weight for <type> to <value>`

reports a **per-event** weight, not the aggregate EventType probability mass.

S1.42AC configured all eight scales to constant `12.5`, so BCMER computes `p_i = 0.125` for all eight EventTypes. Unequal emitted per-event values are expected because types contain different numbers of enabled individual events.

Observed AC values:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

are consistent with inverse event-count normalization. The 219-event solution reconstructs counts `4 / 54 / 77 / 20 / 22 / 10 / 1 / 31`; aggregate integer type shares are approximately `12.4837%` through `12.5070%`, with only integer-truncation spread.

Full derivation: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.

## Corrected implementation decision

Do **not** inverse-compensate the config scales and do **not** patch BCMER to make the eight per-event log values equal. Equal per-event weights would bias populous EventTypes.

No new successor implementation is justified by this analysis. The existing S1.42AC equal-scale concept is the correct **static EventType-probability** approach under BCMER ownership.

S1.42AC remains formally rejected/not promoted until an explicit corrected acceptance decision is made. S1.42AB therefore remains the gameplay baseline.

## Selection-stage caveat

Final executed event frequencies can still differ from the static EventType probability model because `ChooseEvents()` applies event-specific and dynamic behavior including `AddEventIfOnly`, moon whitelist/blacklist, Special/Beta gating, forced-event removal, incompatibility removal, side-event handling and without-replacement repeated draws.

A requirement for exact long-run `12.5%` **executed** EventType frequency after those filters would be a separate broader algorithm-design scope.

## Exact next action

**No runtime test is currently outstanding. No successor is armed. No compensation build should be created.**

If the BCMER EventType scope continues, apply the corrected acceptance model from `Current/109` to the existing S1.42AC artifact/runtime evidence. Do not use equality of the eight per-event log values as the gate.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`;
- guarded base = accepted S1.42AB;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## Permanent anti-regression state

Preserve exact BCMER `1.71.0`; accepted BCMER rain disables; EnemyIsolation disabled; Compatibility Fixes `1.3.14`; BaboonBirdPikminEnemy enabled; narrow Hawk -> Pikmin prevention only; native inherited PikminEnemy lifecycle; Pikmin -> Baboon Hawk attack allowed; Puffer protection; Thumper Bite Limit `3`; Crawler absent from LethalMin Attack Blacklist; accepted S1.42C moon power/spawn baseline; `Consistent Spawn Times = true`; Jetpack `18`; Jet Fuel `18/18`; Thrusters `25/20`; Indoor Pikmin `0.09`; CarryStrength `3 / 30`; CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`; Functional Microwave volume `0.15`; Immortal Snail `40 / 2`; accepted S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach. Project-local patches must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

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

Planned/binding, **not executed**. Entry: `OVERHAUL_START_HERE_ChatGPT.txt`. Re-resolve then-current state and create/verify the required separate standalone pre-overhaul backup repository before structural migration.
