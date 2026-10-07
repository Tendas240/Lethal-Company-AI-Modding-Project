# 06 — Recent Work: S1.42N through S1.42Z

**Purpose:** compact chronology continuation after the older `Current/03_PROJECT_CHRONOLOGY.md` coverage.  
**Updated:** 2026-09-04 — S1.42Z accepted  
**Authority rule:** dedicated per-build Current files and RuntimeEvidence remain the detailed primary records; this file summarizes the sequence without replacing them.

## S1.42N — Baboon Hawk death-target resolver

The N stage narrowed the Baboon Hawk/Pikmin problem to dead-target cleanup and target resolution.

Repository history records:

- plan: Baboon Hawk death target resolver;
- implementation: Hawk-death Pikmin registry resolver;
- runtime result: native task finalization was still not correct.

The important lesson was that locating the affected Pikmin was not by itself sufficient: the repair still had to respect LethalMin's own task/lifecycle contract.

## S1.42O — native Pikmin task-finalization attempt

O moved the repair toward LethalMin-native task completion instead of project-owned cleanup.

Repository history records:

- native Pikmin task finalization plan;
- use of native `TaskFinished` in the death-cleanup path;
- runtime analysis showing that this still did not provide the required cleanup/finalization semantics.

This reinforced the rule that a method name suggesting task completion cannot be assumed to cover the full lifecycle without inspecting its exact behavior and callers.

## S1.42P — exact `FinishTask` recovery

P refined the repair again around the exact LethalMin `FinishTask` path.

Repository history records:

- exact `FinishTask` recovery plan;
- exact LethalMin `FinishTask` use;
- build/runtime gate and dedicated handover evidence.

P remained part of the iterative root-cause chain rather than the final accepted solution. Its diagnostic value is retained because it established which LethalMin task-finalization entry points were and were not sufficient.

## S1.42Q — minimal LethalMin-native rollback and exact co-attacker root cause

Q deliberately reduced project-owned behavior and returned toward a minimal LethalMin-native architecture.

Repository history records:

- minimal native rollback architecture;
- rollback build and verification;
- later exact root-cause analysis identifying the latched co-attacker/dead-target interaction.

This was the key transition from compensating cleanup attempts toward understanding the exact interaction path.

## S1.42R — exact latched dead-target completion attempt; unsafe lifecycle suppression identified

R targeted the exact latched dead-target completion path after Q's root-cause work.

The R-era investigation also exposed a critical anti-regression rule: disabling the complete `LethalMin.BaboonBirdPikminEnemy` component to stop one Hawk/Pikmin interaction suppresses unrelated inherited responsibilities, including normal Pikmin work/carry/death/task lifecycle behavior.

That broad component-disable strategy is permanently superseded. It must not be reintroduced merely because it blocks the immediate interaction symptom.

The permanent engineering rule derived from this failure is captured in:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## S1.42S — Baboon adapter lifecycle restore

S replaced the unsafe broad suppression with a narrow compatibility repair.

Canonical acceptance record:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Runtime result:

- Pikmin followed and worked again;
- carrying behavior returned;
- Pikmin could attack normally;
- Pikmin death/unlatch/task lifecycle behaved correctly;
- catastrophic Work/no-task spam was absent;
- only the narrow Hawk -> Pikmin interaction entry points remained blocked;
- the inherited `PikminEnemy` lifecycle was preserved.

Two disconnect/post-round exception families remained monitor-only because no active-gameplay regression was established.

S was the successful repair of the Baboon/Pikmin lifecycle regression, but normal enemy population restoration still remained as a separate gate.

## S1.42T — normal enemy restore

T restored the ordinary enemy population while preserving the S lifecycle repair.

Repository commit history records the S1.42T normal-enemy restore build and a runtime PASS, followed by promotion as the current technical state and closure of the T gate.

This separated the compatibility repair from enemy-spawn restoration rather than changing both at once.

A one-off AloeChase/FSB load-state message later remained monitor-only rather than becoming a speculative patch target.

## S1.42U — BCMER 1.71.0 full-normal-stack acceptance

U reactivated the exact intended BCMER version on the restored normal stack and became the accepted pre-retune rollback baseline.

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

U confirmed:

- exact BCMER 1.71.0 enabled;
- EnemyIsolation disabled;
- Compatibility Fixes 1.3.14 healthy;
- normal enemy population present;
- accepted Baboon/Pikmin lifecycle repair retained;
- S1.42C-derived moon power/spawn baseline retained;
- SpawnCycleFixes `Consistent Spawn Times = true` retained;
- Work/no-task, Leader-null and the project-specific compatibility regression markers absent.

After S1.42Z acceptance, U remains an important rollback artifact but is no longer the latest accepted baseline.

## S1.42V — first post-BCMER balance tuning

Profile:

`Profiles/LC V1 S1.42V Post-BCMER Balance Tuning.r2z`

SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Main tuning:

- Jetpack base acceleration `10 -> 12`;
- Functional Microwave volume `0.5`;
- Immortal Snail Rarity `40`, Max `2`.

The Jetpack patch architecture worked technically, but 12f was too subtle. V therefore remained a tuning experiment, not a promoted baseline.

V Jetpack DLL SHA-256:

`084fe47b5e47d3637fbb6d4fdd735429a37934993fc190fb4b6abbc51eada00c`

## S1.42W — stronger lift-off / quieter Microwave retune

Profile:

`Profiles/LC V1 S1.42W Lift-Off Microwave Retune.r2z`

SHA-256:

`f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`

Main tuning:

- Jetpack `16f`;
- Jet Fuel `20 / 20`;
- Jetpack Thrusters `25 / 20`;
- Microwave volume `0.15`;
- Snail Rarity `40`, Max `2`.

W's technical path passed, but 16f was still too subtle. Microwave volume could not be judged in that run because no Microwave appeared.

W Jetpack DLL SHA-256:

`95b7e689f68246ebda2fa6a0cab9fbe2ead206a00d85e6cbf64653d1f69d1fa8`

One `PikminManager.DespawnLumiknulls()` collection-modified exception occurred during teardown/despawn and remains monitor-only because no active-gameplay cascade was established.

## S1.42X — diagnostic Jetpack 32f / Pikmin carry / first ACU provider tuning

Profile:

`Profiles/LC V1 S1.42X Jetpack Pikmin ACU Retune.r2z`

SHA-256:

`57d8f9251236cf40eacf4366a21646ae8c51500b9ed6fa79cbc9b56c8daa611d`

Main tuning:

- Jetpack `32f`;
- Jet Fuel `10 / 10`;
- Thrusters `30 / 20`;
- Indoor Pikmin Spawn Chance `0.08`;
- configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- Functional Microwave `0.15`;
- Snail `40 / 2`;
- `code_rebirth:air_control_unit` exact provider curve set ×0.5.

X proved that `jetpackAcceleration` is a real perceptible tuning lever: 32f was unmistakably stronger but far too strong for normal play.

The CarryStrength values were accepted.

The DawnLib provider-level Air Control Unit scaling architecture worked, but X's scope was incomplete because CodeRebirth's separate G.R.E.G. / Advanced Airspace Control map object was not yet included.

## S1.42Y — complete aerial-defense scope / 22f tuning

Profile:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Runtime evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Main tuning:

- Jetpack `22f`;
- Jet Fuel `15 / 15`;
- Thrusters `25 / 20`;
- Indoor Pikmin `0.08`;
- CarryStrength `3` / Purple `30`;
- Microwave `0.15`;
- both Air Control Unit and G.R.E.G. exact 18-curve provider sets ×0.5.

Verdict:

**TECHNICAL PATHS PASS / MICROWAVE + CARRY ACCEPTED / JETPACK + INDOOR PIKMIN RETUNE REQUIRED / NOT ACCEPTED**

Y proved the complete two-target aerial-defense transaction:

- ACU exact 18 curves validated;
- G.R.E.G. exact 18 curves validated;
- both complete contracts validated before mutation;
- both sets scaled ×0.5;
- normal enemies remained active;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- Fatal = 0.

User accepted Microwave `0.15` and CarryStrength `3 / 30`, then selected Jetpack `18f` and Indoor Pikmin `0.09` for the next candidate.

Canonical assessment:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

## S1.42Z — Jetpack/Pikmin retune — ACCEPTED

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Build run:

`33874737048` — success

Automated build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

Exact tuning:

- Jetpack `18f`;
- Jet Fuel `18 / 18`;
- Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- CarryStrength `3` / Purple `30`;
- Microwave `0.15`;
- Snail Rarity `40`, Max `2`;
- ACU exact 18 curves ×0.5;
- G.R.E.G. exact 18 curves ×0.5.

DLL SHA-256:

- Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

Z was rebuilt directly from S1.42U; earlier tuning DLLs are not stacked.

Candidate record:

`Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

Raw log SHA-256:

`ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

Coverage:

- 1,586,159 bytes;
- 16,094 lines;
- 15,325 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

Fresh runtime validation confirmed:

- both Z project-local plugins loaded;
- exact Jetpack `10 -> 18` path armed;
- CodeRebirth 1.6.9 / DawnLib 0.9.25 / Dusk 0.9.25 validated;
- ACU exact 18-curve provider validated;
- G.R.E.G. exact 18-curve provider validated;
- both complete provider sets transactionally scaled ×0.5;
- no aerial-defense contract refusal;
- EnemyIsolation disabled at runtime;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0;
- no Error-severity output from either project-local Z plugin.

The user reported that everything is in order from their side. S1.42Z is therefore promoted to the canonical accepted full-normal-stack baseline.

Canonical acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Machine status:

`Current/Projektstatus_S1.42Z_ACCEPTED.json`

## Current next state

**No successor build is armed.**

Accepted base:

`S1.42Z`

The next planned gameplay/config stage, when explicitly requested, is equal effective probability for all installed interiors, with the same equal-probability rule preserved for future added interiors unless explicitly overridden.

Later deferred scopes remain separate unless the user explicitly combines them:

- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Permanent lessons from N–Z

- Fix the exact interaction/call path; do not compensate by suppressing a complete foreign lifecycle.
- Never disable the whole `BaboonBirdPikminEnemy` adapter merely to stop one interaction.
- Keep gameplay changes isolated from unrelated cleanup.
- Build tuning candidates directly from a known accepted baseline rather than stacking experimental DLLs.
- Treat build/compile success as technical evidence only; gameplay promotion requires fresh runtime evidence.
- Keep monitor-only teardown/setup exceptions separate until they are reproducible or user-facing.
- DawnLib aerial-defense ×0.5 is an exact curve-amplitude/spawn-weight reduction, not a promise of exact half-counts in a short runtime sample because DawnLib evaluates and rounds the resulting amount.
