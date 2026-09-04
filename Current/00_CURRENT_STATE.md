# 00 — Current State

**Updated:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Current canonical state

Newest fully accepted full-normal-stack gameplay baseline and newest runtime-accepted technical descendant:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Runtime evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Verdict:

**PASS — exact BCMER 1.71.0 restored, normal enemy population retained, no critical compatibility/lifecycle regression, no gameplay-visible technical problem reported.**

S1.41 is now historical as the previous accepted full-normal-stack baseline. S1.42T remains the accepted BCMER-off comparison baseline for the restoration chain but no longer holds the newest accepted role.

## S1.42U runtime facts

Confirmed:

- `Loading [BrutalCompanyMinusExtraReborn 1.71.0]`;
- `BrutalCompanyMinusExtraReborn 1.71.0 is done patching.`;
- `Loading [S1.39 Compatibility Fixes 1.3.14]`;
- EnemyIsolation disabled;
- `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- Fatal = 0;
- no old disconnect NoticeZone/NetworkObjectReference marker;
- no crash/freeze;
- known setup SoundAPI/SoftMask exception classes did not become a gameplay cascade.

Direct power evidence from the run:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1.

## Permanent compatibility state to preserve

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Preserve:

- exact BCMER 1.71.0 enabled;
- EnemyIsolation off;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native PikminEnemy death/unlatch lifecycle;
- Pikmin -> Baboon Hawk attacks;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist.

## Moon power-count / spawn restore verification

Current S1.42U:

`ProfileSources/S1.42U/BepInEx/config/LethalLevelLoader.cfg`

is byte-identical to the canonical S1.42C restore baseline file.

Therefore all stored per-moon:

- maximum inside enemy power counts;
- maximum outside daytime power counts;
- maximum outside nighttime power counts;
- inside/daytime/nighttime enemy spawn lists

remain restored exactly to the intended canonical baseline.

Do not wholesale regenerate or normalize this file.

## Enemy spawn timing

Current:

`BepInEx/config/butterystancakes.lethalcompany.spawncyclefixes.cfg`

retains:

`Consistent Spawn Times = true`

and is byte-identical to S1.42C.

This preserves the intended standardized first spawn wave at about 7:39 AM. In particular, outside/daytime enemies are not forced to wait for the vanilla vent-empty delay before participating in the first wave. Indoor enemies still use their vent timing/lifecycle.

## Current tuning observations

### Immortal Snail

Current config:

`BepInEx/config/dev.idjut.SnailFork.cfg`

- `Rarity = 80`
- `Max Snails = 2`

Requested next value:

`Rarity = 40`

This halves the configured spawn weight, not necessarily the final absolute probability after the full weighted pool is evaluated.

### CodeRebirth Functional Microwave

Current config already contains:

`Functional Microwave | Volume = 0.7`

The previous volume reduction therefore did survive into S1.42U, but the user still perceived the microwave as too loud.

Proposed next value:

`Functional Microwave | Volume = 0.5`

### Jetpack acceleration

Current ButteRyBalance Jetpack handling:

`Control Scheme = V49`

Do not switch this broad handling/inertia mode merely to approximate a small acceleration buff.

More Ship Upgrades contains the actual `Jet Fuel` acceleration upgrade:

- `Initial Acceleration Increase = 20`
- `Incremental Acceleration Increase = 20`

Those values only affect the purchased Jet Fuel upgrade. A requested always-on base acceleration increase needs an exact narrow implementation and must not be guessed.

## Next planned stage

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed**

Confirmed next tuning items:

- Immortal Snail rarity/weight `80 -> 40`;
- Functional Microwave volume `0.7 -> 0.5` proposed;
- modest Jetpack acceleration increase requested, exact implementation still to be frozen.

Do not silently mix the older broader backlog (interior equalization, CullFactory exceptions, Mausoleum fog, BCMER EventType rebalance, microwave rarity) unless each exact delta is deliberately included before arming.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U;
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

No successor build is currently armed.

## Monitor-only issues

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception. It did not recur in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message. No gameplay impact established.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local "current" wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains older comments that do not perfectly describe accepted v1.3.14 behavior.

Actual code/config/runtime evidence and chronologically newer canonical documents are authoritative. Cleanup remains separate maintenance.
