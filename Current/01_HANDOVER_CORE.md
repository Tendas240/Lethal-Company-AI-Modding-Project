# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the Source of Truth and canonical build/handover workspace.

Do not require a local repository clone or local profile build while repository-native artifacts and automation are available.

## Read first

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`
4. `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`
5. `Current/108_REPOSITORY_HANDOVER_AUDIT_S1.42AC_REJECTED.md`
6. `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
7. `Current/Projektstatus_S1.42AC_REJECTED.json`
8. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
9. `Current/00_CURRENT_STATE.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical rejection/candidate records remain evidence. `Current/109` supersedes the old interpretation of the S1.42AC primary gate without erasing the historical rejection decision.

## Accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Accepted architecture: LethalLevelLoader determines viable/excluded dungeon membership first; project-local S1.42AB changes only positive rarities in the returned viable list to `100`. Accepted Offense runtime preserved 40 viable entries, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

## S1.42AC formal status

**S1.42AC — BCMER EventType Equal Distribution — FORMALLY REJECTED / NOT ACCEPTED / NOT PROMOTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Original rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Completed analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`

Do not silently promote S1.42AC. S1.42AB remains the accepted gameplay baseline.

## Corrected BCMER 1.71.0 model

Exact upstream source commit:

`TheSoftDiamond/BrutalCompanyMinusExtraReborn@e2ca64b9954b7076e75e9a9ff97d76232c4086b0`

At that commit `Plugin.cs` declares `VERSION = "1.71.0"`.

When `Use custom weights? = false`, BCMER computes normalized EventType probabilities from the eight configured scales, then derives a **per-event** weight:

```text
perEventWeight_i = int((eventTypeSum / fix(eventTypeCount[i])) * eventTypeProbability_i * 1000)
```

`eventTypeCount[i]` is the count of enabled individual events of the type. `eventTypeSum` is the total enabled-event count. The resulting value is assigned to every individual event of that type.

Therefore the runtime lines:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

are **not aggregate EventType weights**. They are intentionally unequal per-event weights that compensate for unequal type populations.

S1.42AC's eight constant `12.5` scales produce BCMER target probabilities `0.125` each. The observed values are consistent with a 219-enabled-event pool with counts `4 / 54 / 77 / 20 / 22 / 10 / 1 / 31`; aggregate static shares are approximately `12.4837%` to `12.5070%`, with residual spread from integer truncation.

Full derivation and dynamic eligibility caveats are in `Current/109`.

## Implementation decision

Do not inverse-compensate the config scales and do not add a local patch that forces the eight logged per-event weights equal. That would bias EventTypes with more individual events.

No new successor implementation is justified by the weight-path analysis. The existing S1.42AC equal-scale concept is the correct **static EventType-probability** approach under BCMER ownership.

## Exact next action

No runtime test is outstanding and no successor is armed.

If the BCMER EventType scope continues, apply the corrected acceptance model from `Current/109` to the existing S1.42AC artifact/evidence. The eight per-event log values are expected to differ and must not be used as an equality gate.

If exact long-run `12.5%` executed EventType frequency after `AddEventIfOnly`, moon filters, Special/Beta gating, forced/incompatible removals and without-replacement selection is required, treat that as a separate broader algorithm-design scope.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`, guarded by accepted S1.42AB.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## Mandatory runtime-test UX

Whenever a future runtime test is outstanding, the response that explains the test must also include the exact build-specific PowerShell one-line log uploader. There is no uploader to run now because no runtime test is pending.

## Permanent invariants

Preserve exact BCMER `1.71.0`; accepted BCMER rain disables; EnemyIsolation disabled; Compatibility Fixes `1.3.14`; BaboonBirdPikminEnemy enabled; narrow Hawk -> Pikmin prevention only; inherited PikminEnemy lifecycle; Pikmin -> Baboon Hawk attack allowed; Puffer protection; Thumper Bite Limit `3`; Crawler absent from Attack Blacklist; accepted S1.42C moon power/spawn baseline; `Consistent Spawn Times = true`; Jetpack `18`; Jet Fuel `18/18`; Thrusters `25/20`; Indoor Pikmin `0.09`; CarryStrength `3 / 30`; CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`; Functional Microwave volume `0.15`; Immortal Snail `40 / 2`; accepted S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach. Follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` for project-local patches.

## Deferred scopes

Keep separate unless explicitly selected/grouped:

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.

## Repository overhaul continuity

Planned but not executed. Dedicated entry: `OVERHAUL_START_HERE_ChatGPT.txt`. Re-resolve the then-current state and create/verify the required separate standalone pre-overhaul backup repository before structural migration.
