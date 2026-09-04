# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for this project.

Game: **Lethal Company V81**

Do not require a local repository clone or local profile build while the required base artifacts and GitHub-native infrastructure are present.

## Current canonical state

### Accepted full-normal-stack baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Accepted AB behavior includes post-viability LethalLevelLoader normalization: LLL owns viable/excluded membership first, then every positive rarity in the returned list becomes exactly `100`. The accepted Offense run preserved all 40 viable flows, normalized 12/40 values from `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

Authoritative interior marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

### Latest built artifact — S1.42AC remains formally rejected/not promoted

**S1.42AC — BCMER EventType Equal Distribution**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Original rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Completed source-path analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`  
Machine state: `Current/Projektstatus_S1.42AC_REJECTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`

S1.42AC set all eight BCMER EventType scales to the same constant `12.5, 0.0, 12.5, 12.5`, with `Use custom weights? = false`, BCMER randomizer disabled, and exact BCMER `1.71.0` preserved.

The original runtime rejection compared these eight log values directly:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

That **acceptance interpretation is now superseded** by exact BCMER `1.71.0` source analysis.

## BCMER 1.71.0 weight-path finding

Exact upstream source commit:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `Plugin.cs` declares `VERSION = "1.71.0"`.

BCMER computes:

```text
p_i = computedScale_i / sum(computedScales)
perEventWeight_i = int((eventTypeSum / eventTypeCount_i) * p_i * 1000)
```

and then assigns `perEventWeight_i` to **every individual event of that EventType**.

Therefore `Set eventType weight for <type> to <value>` is a **per-event weight**, not the aggregate EventType mass. Types with many enabled events intentionally get lower per-event values than types with few events so their aggregate mass remains near the configured EventType probability.

For S1.42AC, all eight configured scales resolve to `12.5`, so BCMER's own normalized target is `p_i = 0.125` for all eight types. The observed values are consistent with inverse event-count normalization; aggregate type shares are approximately `12.5%` each, with only small integer-truncation spread.

Full derivation, event-count reconstruction, aggregate-mass table and dynamic eligibility caveats:

`Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`

### Consequence

Do **not**:

- inverse-compensate the eight config scales merely to make the logged per-event values match;
- patch BCMER to force the eight logged per-event values equal;
- build a new successor for that purpose.

Equal per-event values would strongly bias EventTypes that contain many events.

The existing S1.42AC equal-scale concept is the correct static EventType-probability approach under BCMER ownership. S1.42AC is nevertheless **not silently promoted** by this analysis; S1.42AB remains the accepted gameplay baseline until an explicit corrected acceptance decision is made.

## Exact next step

No runtime test is currently outstanding and no successor is armed.

If the BCMER EventType scope is continued, apply the **corrected acceptance model** from `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md` to the already-existing S1.42AC artifact/evidence. Do not require equality of the eight per-event log values.

A requirement for exact long-run `12.5%` **executed** EventType frequency after moon eligibility, `AddEventIfOnly`, Special/Beta gating, incompatibility removal and without-replacement selection would be a different, materially broader algorithm-design scope.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`;
- guarded base = accepted S1.42AB;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`
3. `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`
4. `Current/108_REPOSITORY_HANDOVER_AUDIT_S1.42AC_REJECTED.md`
5. `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
6. `Current/Projektstatus_S1.42AC_REJECTED.json`
7. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
8. `Current/00_CURRENT_STATE.md`
9. `Current/01_HANDOVER_CORE.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical candidate/build/rejection files remain evidence. Newer confirmed source-path analysis may supersede the **interpretation** of an older gate without erasing the historical decision itself.

## Planned repository information-architecture overhaul

The repository cleanup is planned/binding but **not executed yet**.

If explicitly started later, begin with `OVERHAUL_START_HERE_ChatGPT.txt`, re-resolve the then-current state, and create/verify the required separate standalone pre-overhaul backup repository before structural migration.

## Permanent anti-regression state

Preserve exact BCMER `1.71.0`, accepted BCMER rain disables, EnemyIsolation off, Compatibility Fixes `1.3.14`, `BaboonBirdPikminEnemy` enabled, narrow Hawk -> Pikmin prevention only, native inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack allowed, Puffer -> Pikmin protection, Thumper Bite Limit `3`, Crawler absent from LethalMin Attack Blacklist, accepted S1.42C-derived moon power/spawn baseline, `Consistent Spawn Times = true`, Jetpack base acceleration `18`, Jet Fuel `18/18`, Thrusters `25/20`, Indoor Pikmin `0.09`, CarryStrength `3 / 30`, CodeRebirth ACU + G.R.E.G. exact 18 curves ×`0.5`, Functional Microwave volume `0.15`, Immortal Snail `40 / 2`, and accepted S1.42AB interior normalization.

Never repeat the S1.42R whole-component disable approach.

## Deferred separate scopes

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.
