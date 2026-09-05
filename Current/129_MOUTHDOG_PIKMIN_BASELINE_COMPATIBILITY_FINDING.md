# Mouth Dog / Pikmin Baseline Compatibility Finding

**Date:** 2026-09-06  
**Status:** CURRENT OPEN COMPATIBILITY FINDING / SOURCE-CONTRACT ANALYSIS REQUIRED / NO SUCCESSOR ARMED  
**Observed in:** S1.42AF accepted-runtime run  
**Runtime evidence:** `RuntimeEvidence/S1.42AF/20260905T223738Z/`  
**Related acceptance:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`

## User-visible observation

During the otherwise successful S1.42AF normal run, a Mouth Dog appeared to have two White Pikmin in its mouth. The intended project behavior is stricter: Mouth Dogs / Eyeless Dogs must not target, bite, grab or kill Pikmin at all.

## Runtime evidence

The runtime log confirms that this was a real enemy-to-Pikmin interaction rather than a harmless visual overlap.

At approximately `22:35:06` LethalMin logged:

- `Biting 2 Pikmin`;
- White Pikmin `KpfIK7` and `bBAu3I` grabbing onto `EnemyAttackMouth`;
- a `2.5` second death timer for both Pikmin.

When the death timer expired, LethalMin attempted the enemy-attack kill path for each Pikmin. Each attempt then logged `Has Invincible mode when trying to kill`, so the configured Pikmin invincibility prevented the final death itself.

The run nevertheless entered a broken post-grab state. Runtime analysis records `707` `Work state with no task assigned!` warnings, split across the two affected White Pikmin, beginning immediately after the bite/death-timer sequence.

Therefore the existing invincibility setting is not an adequate compatibility solution: it can prevent the final kill while still allowing MouthDog targeting/grab/death-timer state mutation and leaving Pikmin in an invalid work state.

## Classification

This finding is **not classified as an S1.42AF regression**.

S1.42AF was built directly from accepted S1.42AC. Automated archive QC for S1.42AF reported no mod-state changes, additions/removals or config patches; the intended functional delta was the already-reviewed Functional Microwave plugin plus shortened Gale profile identity. No LethalMin package/config or S1.39 Compatibility Fixes behavior was changed by S1.42AF.

The Mouth Dog interaction is therefore treated as a newly observed **baseline-resident compatibility gap** in the inherited full-normal stack. S1.42AF remains accepted for its isolated Microwave/path-length scope.

## Binding gameplay target

The required asymmetric interaction rule is:

- Mouth Dog / Eyeless Dog -> Pikmin targeting/bite/grab/kill: **blocked before Pikmin grab/death-timer state mutation**;
- Pikmin -> Mouth Dog combat: remain native LethalMin behavior unless later source evidence proves a separate reason to change it;
- do not solve this by relying on Pikmin invincibility after a grab;
- do not broadly disable an enemy adapter or reconstruct Pikmin follower/task state after mutation unless exact upstream ownership evidence leaves no safer prevention point.

This follows the existing project principle in `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`: native LethalMin owns normal Pikmin -> enemy combat/lifecycle, while project-local compatibility code blocks only proven Enemy -> Pikmin gaps as narrowly as possible.

## Existing project-local guard

`Patches/S139CompatibilityFixes/Plugin.cs` already installs a `Priority.First` prevention-only prefix on exact declared:

`LethalMin.PikminAI.GrabPikmin(Transform,float,int)`

The current guard blocks proven Crawler/Thumper and Baboon Hawk snap-position paths before leader/grab/death-timer mutation. It does **not** currently identify MouthDog/EyelessDog snap positions, which is consistent with the observed runtime interaction.

This does not yet prove that simply adding MouthDog name matching is the correct fix. The exact LethalMin MouthDog adapter/owner/method/inheritance/config path must be inspected first.

## Exact next project action

Perform a focused source/contract analysis under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`:

1. inspect the exact LethalMin MouthDog/EyelessDog compatibility owner, method and inheritance path responsible for targeting, bite and `GrabPikmin`;
2. inspect whether LethalMin exposes a native configuration switch that can disable MouthDog -> Pikmin targeting without disabling Pikmin -> MouthDog combat;
3. confirm whether the observed bite path reaches the existing exact `PikminAI.GrabPikmin(Transform,float,int)` prevention point before all harmful state mutation;
4. if a project-local patch is required, prefer extending an exact prevention-before-mutation boundary rather than delayed state repair or whole-component disable;
5. define adjacent regression checks, including normal Pikmin -> MouthDog attack, repeated encounters and normal enemy/Pikmin lifecycle;
6. only after the exact contract is proved may a successor plan/build be armed.

**No successor build is currently authorized or armed.**
