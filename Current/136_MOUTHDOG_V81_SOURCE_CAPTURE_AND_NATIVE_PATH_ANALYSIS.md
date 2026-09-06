# MouthDog V81 Source Capture and Native Path Analysis

**Status:** CURRENT / HANDOVER-CRITICAL ANALYSIS STATE  
**Authority:** current provenance-safe Vanilla V81 MouthDogAI evidence result and remaining pre-successor proof boundary  
**Supersedes execution state:** `Current/135_MOUTHDOG_V81_SOURCE_CAPTURE_TOOL_WINDOWS_HARDENING_STATE.md`  
**Related lifecycle:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`  
**Patch safety:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-06

## Capture result

The hardened Windows capture completed successfully on the user's actual Lethal Company installation.

Authoritative provenance:

- evidence branch: `source-evidence/mouthdog-v81-20260906t121738z`;
- evidence commit: `a618b19bfc30234ca556c924d681d43b2c13d1d9`;
- capture base / repository `main` at capture: `3049b0fa52af79db39efb075d94684d229eed3c6`;
- capture UTC: `2026-09-06T12:17:38Z`;
- source assembly: `Lethal Company_Data/Managed/Assembly-CSharp.dll`;
- source assembly SHA-256: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- source assembly size: `2034688` bytes;
- Lethal Company executable SHA-256: `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam app id: `1966720`;
- Steam buildid: `22825947`;
- Steam appmanifest SHA-256: `fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432`;
- decompiler: `ilspycmd 11.0.0.9375`;
- full local `MouthDogAI` type-decompile SHA-256: `d00491dcffd4b91c60cb9c43e8108f558da69ee6dba6f0b71f53c8f0035892bd`;
- published focused report SHA-256: `0768404f72cb2c7a56b78e63519f6ed03610e6046c6d21fed7ba0c2668864097`.

Authoritative files:

- `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`;
- `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`.

The evidence commit contains only those two publication-safe files. It does not publish `Assembly-CSharp.dll`, a full Assembly-CSharp decompile, absolute local paths, or the Windows user name.

## What the Vanilla V81 source now proves

### Noise perception is position-based

`MouthDogAI.DetectNoise(Vector3 noisePosition, float noiseLoudness, ...)` receives a world-space `Vector3` noise position. The native method computes distance from the dog to that position, applies loudness/occlusion/suspicion logic, and drives the dog through the noise-position path.

`EnrageDogOnLocalClient(Vector3 targetPosition, ...)` writes the resulting world-space target into `noisePositionGuess`, sets the NavMesh destination to that position when not already lunging, and records `lastHeardNoisePosition`.

In chase state, the native AI calls `EnterLunge()` when the dog is within less than 4 units of `noisePositionGuess` and the lunge cooldown permits it.

Therefore the native noise path does not require a Pikmin-specific target handle. The runtime `targetPos` / `lastheardnoisePosition` diagnostics are consistent with a world-position pursuit path, not proof that Vanilla `MouthDogAI` semantically selected a Pikmin object.

### Generic EnemyAI collision is a separate native attack surface

Vanilla V81 declares:

`MouthDogAI.OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)`

The focused source proves that this override first calls `base.OnCollideWithEnemy(other, collidedEnemy)`. For a different enemy type and after the one-second other-enemy cooldown, it can:

- rotate toward the collided enemy while in chase state;
- set `inLunge = true` and call `EnterLunge()`;
- reset the other-enemy hit cooldown;
- call `collidedEnemy.HitEnemy(2, null, playHitSFX: true)`.

Exact LethalMin 1.1.108 source evidence already preserved in `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt` proves `PikminAI : EnemyAI`.

That means a Pikmin can enter this Vanilla collision path solely because it is an `EnemyAI`; Vanilla `MouthDogAI` does not need Pikmin-specific knowledge for this route.

## Relationship to the S1.42AG partial fix

S1.42AG remains runtime rejected and is not promoted.

Its `Priority.First` prefix on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` still has a proven useful effect: it prevents the LethalMin-specific Pikmin selector/bite/grab/death-timer mutation path before `GrabbedPikmin` bookkeeping and `PikminAI.GrabPikmin(...)`. The prior `Work state with no task assigned!` burst fell to zero.

The successful native capture proves that the blocked LethalMin dispatcher is not the only interaction surface. Vanilla noise-position pursuit and generic `EnemyAI` collision/lunge/damage remain independent of that dispatcher.

## Pikmin audible-noise evidence

Exact LethalMin 1.1.108 evidence also proves that `PikminAI.PlayAudioOnLocalClient(...)` calls `RoundManager.Instance.PlayAudibleNoise(...)` at the Pikmin transform position when `DontMakeAudibleNoisesCheat` is false. Singing uses the same audible-noise mechanism.

The accepted S1.42AF/S1.42AG configuration has:

`Dont Make Audible Noises = false`

Therefore a Pikmin itself is a proved possible audible-noise emitter in the current stack.

## Carried-scrap hypothesis — current verdict

The S1.42AG runtime evidence proves that Purple Pikmin transported `GoldBar(Clone)` during the relevant run. LethalMin's item-carry path sets the item as held by an enemy, parents it to the primary Pikmin hold position, disables normal physics, and starts `PikminItem.CarryNumerator()`.

However, the current evidence does **not** prove that the carried GoldBar itself emitted the noise that triggered the observed Mouth Dog pursuit. It also does not yet prove that carried GoldBar noise is impossible.

The stronger hypothesis that Vanilla `MouthDogAI` selects a Purple Pikmin specifically because it carries scrap is rejected by the native source model: the proved perception path consumes positions, and the proved collision path consumes generic `EnemyAI` objects.

The narrower causal question — whether the carried GoldBar contributed an audible-noise event at or near the Pikmin — remains open.

## Remaining proof boundary before any successor

Two targeted source proofs are still required.

### 1. Vanilla `EnemyAI.OnCollideWithEnemy()` base contract

`MouthDogAI.OnCollideWithEnemy()` begins by calling the base implementation. Before considering any Harmony prefix that could skip the MouthDog override for Pikmin, inspect the exact V81 `EnemyAI.OnCollideWithEnemy()` implementation and inheritance/side-effect contract.

Do not return `false` from a guessed prefix until it is proved that bypassing the override will not incorrectly suppress required base responsibilities.

### 2. LethalMin `PikminItem.CarryNumerator()` / carry-audio-noise contract

Extend exact LethalMin 1.1.108 evidence around:

- `PikminItem.CarryNumerator()`;
- item grab/drop/carry audio paths;
- any `RoundManager.PlayAudibleNoise(...)` callsites associated specifically with carrying an item;
- the relationship between `PikminAI`'s own audible sounds and carried-item sounds.

This proof must either establish or reject the narrower carried-scrap/noise causality. Do not infer causality from temporal correlation alone.

## Exact next action

Perform a targeted repository-native source-evidence extension for the two remaining boundaries above. Do not re-run the already successful `InspectMouthDogV81.ps1` capture merely to reproduce existing evidence.

After those two source contracts are proved, apply `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and complete a successor-specific safety review before arming or building anything.

## Still forbidden until that proof completes

- no new gameplay build;
- no successor arm;
- no new runtime test;
- no repeat S1.42AG run or log upload;
- no broad `EnemyAI` scan/fallback;
- no guessed Harmony target;
- no whole `MouthDogPikminEnemy` disable;
- no manual Pikmin state reconstruction;
- no change to native Mouth Dog -> player behavior;
- no suppression of native Pikmin -> Mouth Dog attack/latch/death-unlatch ownership;
- no claim that the carried GoldBar caused the noise until source evidence proves it.

Reverse-direction Pikmin -> Mouth Dog combat remains a future deliberate runtime gate for a later candidate. Passive follower non-aggression is normal behavior and is not that test.
