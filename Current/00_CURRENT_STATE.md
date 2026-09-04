# 00 — Current State

**Updated:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Current canonical state

Newest fully accepted full-normal-stack gameplay baseline and newest runtime-accepted technical descendant:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Profile SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Final handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

Runtime evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Raw size / lines:

- `1,959,356 bytes`;
- `19,939` lines.

GitHub Actions build run:

`33818241873` = **success**

Build commit:

`29e7b36c3d09ff37551894438744d67089d7aba4`

Verdict:

**PASS — exact BCMER 1.71.0 restored, normal enemy population retained, no critical compatibility/lifecycle regression, no gameplay-visible technical problem reported.**

There is **no newer built candidate**. S1.42V is plan-only and must not be described as built.

S1.41 is historical as the previous accepted full-normal-stack baseline. S1.42T remains the accepted BCMER-off comparison baseline for the restoration chain but no longer holds the newest accepted role.

## S1.42U runtime facts

Confirmed from the complete accepted runtime log:

- `Loading [BrutalCompanyMinusExtraReborn 1.71.0]`;
- `BrutalCompanyMinusExtraReborn 1.71.0 is done patching.`;
- `Loading [S1.39 Compatibility Fixes 1.3.14]`;
- EnemyIsolation disabled;
- `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- Fatal = 0;
- historical disconnect NoticeZone / unspawned NetworkObjectReference marker = 0;
- no crash/freeze;
- known setup SoundAPI/SoftMask exception classes did not become a gameplay cascade;
- user reported no gameplay-visible technical problem.

Direct runtime power evidence:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1;
- Crawler = 3;
- Bunker Spider = 2.

## Permanent compatibility state to preserve

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Preserve:

- exact BCMER 1.71.0 enabled unless a deliberate diagnostic gate says otherwise;
- EnemyIsolation off;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- Pikmin -> Baboon Hawk attacks;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- restored normal enemy population.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Never-repeat root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Never disable the complete `LethalMin.BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction.

## Moon power-count / spawn restore verification

Current S1.42U:

`ProfileSources/S1.42U/BepInEx/config/LethalLevelLoader.cfg`

is byte-identical to the canonical S1.42C restore file:

`ProfileSources/S1.42C/BepInEx/config/LethalLevelLoader.cfg`

Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

Therefore all stored per-moon:

- maximum inside enemy power counts;
- maximum outside daytime power counts;
- maximum outside nighttime power counts;
- inside/daytime/nighttime enemy spawn lists

remain exactly on the intended restore baseline.

Do not wholesale regenerate or normalize this file.

## Enemy spawn timing

S1.42U SpawnCycleFixes remains byte-identical to S1.42C with:

`Consistent Spawn Times = true`

This preserves the standardized first spawn wave at about 07:39 and prevents the vanilla vent-empty dependency from delaying outside/daytime participation in the first wave.

## Immediate next stage — S1.42V

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed / no S1.42V profile exists.**

Confirmed/requested tuning:

- ImmortalSnail `Rarity = 80 -> 40`;
- keep `Max Snails = 2`;
- CodeRebirth Functional Microwave current volume = `0.7`; proposed next value = `0.5` because 0.7 still sounds too loud;
- modest **always-on base Jetpack acceleration increase** requested.

### Exact next technical action

Do **not** arm S1.42V yet.

First resolve the exact owner and narrow implementation for the always-on Jetpack acceleration increase:

1. identify exact runtime owner/method/field;
2. preserve ButteRyBalance `Control Scheme = V49` unless direct evidence justifies otherwise;
3. account for JetpackFixes interaction;
4. do not substitute More Ship Upgrades `Jet Fuel` unless the intended change is explicitly purchase-gated — current `Jet Fuel` is `20` initial / `20` incremental and only applies after purchase;
5. if custom code is required, perform a dedicated Patch Safety Review and isolate the risky patch from unrelated tuning if practical;
6. freeze the exact S1.42V delta, then arm the GitHub-native build controller.

## Planned stages after S1.42V

Later stage IDs are intentionally **not assigned yet**.

### Environment / Interior tuning

Pending:

- equal probability for all installed interiors; newly added interiors should follow the same equal-probability project rule;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

Testing:

- deterministic config/delta checks;
- multiple landings/reroutes;
- targeted `junkrooms` / `shatteredrooms` behavior check;
- visual Mausoleum fog check;
- Microwave functionality plus reduced occurrence over repeated normal play.

### BCMER EventType balancing

Pending:

- fixed equal distribution: **8 x 12.5% EventTypes**.

Testing:

- deterministic equal-weight config verification;
- BCMER exact 1.71.0 preserved;
- repeated runtime/event coverage without pretending a small sample statistically proves 12.5%.

### Final S1.42 full-stack acceptance

After the tuning stages pass independently:

- longer normal gameplay run;
- varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth systems;
- complete log ingest and critical-marker comparison;
- promote the resulting profile as final S1.42 baseline only if clean.

Do not reopen isolated-enemy diagnostics or heavy Baboon-Hawk stress unless a later change touches that path or new evidence reopens the issue.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U;
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`;
- no successor delta armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

No successor build is currently armed.

## Monitor-only issues

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception. It did not recur in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message. No gameplay impact established.
3. Known setup loaforcsSoundAPI/HarmonyX and SoftMaskKiller-handled exception classes remain non-blocking unless they change behavior, flood or become user-facing.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains older comments that do not perfectly describe accepted v1.3.14 behavior.

Actual current code/config/runtime evidence and chronologically newer canonical documents are authoritative. Cleanup remains separate maintenance and must not be mixed into risky gameplay patches.
