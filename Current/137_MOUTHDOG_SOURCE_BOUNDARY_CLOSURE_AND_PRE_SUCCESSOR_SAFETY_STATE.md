# MouthDog Source-Boundary Closure and Pre-Successor Safety State

**Status:** CURRENT / HANDOVER-CRITICAL ANALYSIS STATE  
**Authority:** current MouthDog source-boundary conclusion and pre-successor safety-review entry point  
**Supersedes current-analysis role of:** `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`  
**Related lifecycle:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`  
**Patch safety:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-06

## Current lifecycle position

- Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**.
- Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- Successor armed: **no**.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains evidence-attribution only.

S1.42AG remains rejected because it blocked only the LethalMin-specific MouthDog -> Pikmin bite/grab/death-timer dispatcher while the user still observed a Mouth Dog pursue/attack a scrap-carrying Purple Pikmin through another path.

## Closed Vanilla V81 base-collision proof

The targeted provenance-pinned capture is complete and integrated.

Authoritative evidence:

- capture branch: `source-evidence/enemyai-collision-v81-20260906t204535z`;
- evidence commit: `131ba3f33d443466b6f122eadb35e83064e5d59d`;
- capture base: `9cff45e603ca3f06118868ac1c1f899ef0292d1f`;
- integrated main merge: `bc84c9d33ab632c1b48207112a3485878e9129e2`;
- assembly SHA-256: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Steam buildid: `22825947`;
- report: `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/ENEMYAI_ONCOLLIDEWITHENEMY_FOCUSED_DECOMPILE.txt`;
- manifest: `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/MANIFEST.json`;
- published report SHA-256: `7ee45c2dd113b413ba1614a51b453b1c7b2953cd055f82ff75debf824a1da2b6`.

Exact V81 base behavior:

```csharp
public virtual void OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)
{
    if (base.IsServer && debugEnemyAI)
    {
        Debug.Log(base.gameObject.name + " collided with enemy!: " + other.gameObject.name);
    }
}
```

Therefore `EnemyAI.OnCollideWithEnemy()` has no gameplay, navigation, targeting, damage, grab, cleanup or lifecycle mutation in this exact V81 assembly. Its only effect is optional server-side debug logging.

This closes the prior uncertainty around a future exact MouthDog collision Prefix: skipping the MouthDog override for an exactly identified Pikmin collision would not suppress hidden base gameplay responsibilities; the lost base effect would only be the optional debug line unless a chosen patch design deliberately preserves it.

## Closed LethalMin 1.1.108 carry/noise proof

Existing exact LethalMin 1.1.108 repository evidence already contains the required `PikminItem` carry path.

`PikminItem.GrabPikminItemOnLocalClient()`:

- stops any prior carry-sound coroutine;
- starts `CarryNumerator()`;
- parents the item to the primary carrier's `HoldPosition`;
- marks the item as held by an enemy;
- calls `GrabItemFromEnemy((EnemyAI)PrimaryPikminOnItem)`;
- disables ordinary item physics.

`PikminItem.CarryNumerator()` repeatedly iterates the current carriers and calls:

`pikmin.PlayAudioOnLocalClient("ItemCarry", PlayOnVoice: true, vol);`

Exact `PikminAI.PlayAudioOnLocalClient(...)` evidence proves that, when audible-noise suppression is disabled, it calls `RoundManager.Instance.PlayAudibleNoise(...)` at the Pikmin's own transform position. The accepted S1.42AF configuration has:

`Dont Make Audible Noises = false`

Therefore item carrying is source-proven to generate recurring audible noise **through the carrying Pikmin at the carrying Pikmin's world position**.

The stronger hypothesis that Vanilla MouthDogAI semantically selects a Purple Pikmin because it carries `GoldBar(Clone)`, or that the GoldBar itself is the proved recurring carry-noise emitter, is rejected by the available source model. The source does **not** establish which exact audible event caused the observed S1.42AG pursuit, and it does not rule out every unrelated `GrabbableObject` grab/drop sound path; runtime causality remains narrower than the source capability proof.

## Combined proven interaction surfaces

The project now has source proof for all pre-successor boundaries required by the previous analysis state:

1. **LethalMin-specific bite/grab dispatcher** — exact `MouthDogPikminEnemy.DoCheckInterval()`; S1.42AG proved prevention-before-mutation works there.
2. **Vanilla MouthDog noise-position pursuit** — `DetectNoise(...)` and `noisePositionGuess` consume world-space positions and can drive chase/lunge behavior.
3. **Vanilla generic enemy collision attack** — `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` can lunge and call `collidedEnemy.HitEnemy(2, ...)`; `PikminAI : EnemyAI` makes Pikmin eligible through inheritance.
4. **Vanilla base collision contract** — `EnemyAI.OnCollideWithEnemy()` is debug-only in the exact V81 assembly.
5. **LethalMin carry-noise capability** — `CarryNumerator()` repeatedly plays `ItemCarry` through each carrier, and current config allows those Pikmin sounds to emit audible noise at carrier position.

No further local Vanilla source capture is required before the successor-specific safety review.

## Exact next action

Perform the **successor-specific Patch Safety Review** required by `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

The review must establish, before any build is armed:

- the exact smallest Harmony interception surface for the remaining MouthDog -> Pikmin interaction;
- exact declaring type, method, signature and Pikmin identification boundary;
- inherited/base behavior and secondary responsibilities;
- whether the existing S1.42AG `MouthDogPikminEnemy.DoCheckInterval()` prevention guard remains part of the successor;
- preservation of MouthDog -> player behavior;
- preservation of native Pikmin -> MouthDog attack/latch/death/unlatch/task lifecycle;
- no broad `EnemyAI` scan or fallback;
- no whole `MouthDogPikminEnemy` disable;
- no manual Pikmin state reconstruction;
- one-variable build delta against accepted S1.42AF;
- exact build and runtime regression gates, including a deliberate reverse-direction Pikmin -> MouthDog test rather than passive follower observation.

Only after this review closes may the project arm/build a successor candidate.

## Currently irrelevant / forbidden actions

- Do not repeat `InspectMouthDogV81.ps1`.
- Do not repeat `InspectEnemyAICollisionV81.ps1` merely to reproduce the integrated evidence.
- Do not ask the user for `Assembly-CSharp.dll`, a full decompile, `-AssemblyPath`, a local repository clone, or manual .NET/ILSpy installation for these already closed proofs.
- Do not repeat the S1.42AG gameplay run or request another S1.42AG log upload.
- Do not arm/build a successor yet.
- Do not start a gameplay/runtime test yet.
