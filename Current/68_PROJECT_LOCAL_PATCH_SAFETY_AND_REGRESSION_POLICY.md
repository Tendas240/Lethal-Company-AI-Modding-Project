# 68 — Mandatory Project-Local Patch Safety and Regression Policy

**Status:** permanent engineering rule
**Applies to:** every project-local Harmony patch, runtime shim, reflection hook, compatibility guard, component toggle, state mutation, RPC interception, config-enforcement patch, and future custom DLL injected into the profile.

## Purpose

Project-local patches are allowed only when they are sufficiently understood and sufficiently narrow that they do not silently break unrelated game/mod behavior.

A patch is **not considered safe merely because it compiles, the game reaches the main menu, or the directly targeted symptom disappears**.

Every future custom patch must be treated as a potential cross-mod lifecycle change and must pass the checks below before it can be promoted.

## Non-negotiable default

**Prefer the smallest exact interception point that prevents only the unwanted behavior.**

Do not disable a whole component, suppress an entire Update/Start/LateUpdate lifecycle, replace a broad method, or mutate shared state when one exact entry point can be blocked instead.

If a component or method has more than one responsibility, disabling/skipping it is presumed unsafe until the complete responsibility set has been proven harmless to suppress.

## Required pre-patch analysis

Before implementing a custom patch, establish all of the following as far as the available code/evidence permits:

1. **Exact owner of the unwanted behavior**
   - exact type;
   - exact declared method;
   - exact call site;
   - exact state/RPC/event involved.

2. **Inheritance and lifecycle map**
   - base classes;
   - inherited `Awake`, `Start`, `Update`, `LateUpdate`, `FixedUpdate`, `OnEnable`, `OnDisable`, `OnDestroy`;
   - `OnNetworkSpawn` / `OnNetworkDespawn`;
   - inherited cleanup/death/task/latch/carry logic;
   - overridden methods that still call `base.*`.

3. **Secondary responsibilities of the target**
   - cleanup;
   - state transitions;
   - event/listener registration;
   - network ownership;
   - task completion;
   - collider/latch management;
   - despawn behavior;
   - persistence/save behavior;
   - compatibility behavior with other mods.

4. **Callers and downstream effects**
   - what invokes the target;
   - what the target invokes;
   - whether other mods Harmony-patch the same method;
   - whether the method is used for both harmful and required behavior.

5. **State ownership**
   - which mod/game system is authoritative for the state being changed;
   - whether a project patch would duplicate or fight a native lifecycle.

If this analysis cannot be completed with reasonable confidence, do **not** compensate with a broader patch. Use a narrower diagnostic build first.

## Harmony/reflection safety rules

- Prefer exact declared methods over broad inheritance/reflection scans.
- Use `BindingFlags.DeclaredOnly` when the intended contract is a declared adapter method.
- Validate target signature, return type, parameter types, declaring type, and method body before installing a patch.
- Refuse guessed fallback targets when the exact contract is absent.
- Avoid patching inherited base methods through multiple derived types.
- Avoid scanning and patching every method containing a name fragment.
- Avoid global object scans from per-frame code.
- Avoid repeated reflection from `Update`/`LateUpdate`.
- Do not assume a method named for one feature has only that responsibility.

## Component-disable rule

**Never set an entire foreign mod component to `enabled = false` solely to suppress one interaction unless its complete lifecycle has been inspected and every lost responsibility is known to be safe to remove.**

Before disabling a component, explicitly inspect:

- inherited Update/cleanup behavior;
- network callbacks;
- event registration/removal;
- state-machine transitions;
- death/despawn cleanup;
- latch/collider cleanup;
- task completion;
- owner/client synchronization.

If any required behavior lives on that component, block only the offending method/entry point instead.

This rule exists specifically to prevent a repeat of S1.42R, where disabling `LethalMin.BaboonBirdPikminEnemy` also disabled inherited `PikminEnemy.Update()` and therefore native death/unlatch cleanup.

## State mutation rule

Project-local code should not manually repair state that the owning mod already knows how to restore.

Before adding:
- manual leader reassignment;
- forced task removal;
- forced unlatch;
- direct state-index changes;
- custom despawn;
- custom carry restoration;
- delayed state snapshots/restores;

first prove that the native owner cannot perform the lifecycle correctly once the offending interaction is prevented.

Prefer **prevention before mutation**.

## One-variable test rule for risky patches

High-risk patch changes must be isolated from unrelated gameplay/config/package changes wherever practical.

Examples of high-risk changes:
- Harmony patches on AI lifecycle methods;
- RPC interception;
- network ownership changes;
- enemy death handling;
- task/latch/grab systems;
- disabling components;
- reflection-driven compatibility;
- save/persistence hooks.

For such changes:
- keep package versions unchanged;
- keep unrelated configs unchanged;
- document the exact archive delta;
- use a dedicated candidate build;
- compare against the latest relevant accepted baseline.

## Mandatory build gate

Before runtime testing, verify:

1. source compiles cleanly;
2. exact intended Harmony targets validate;
3. no broad fallback silently installs;
4. generated profile contains the expected DLL;
5. expected DLL SHA-256 is recorded;
6. archive diff contains only intended files;
7. unrelated configs/packages are unchanged;
8. startup diagnostic markers prove the intended patch path loaded;
9. old/forbidden patch markers are absent.

Passing this gate means only **build-safe**, not gameplay-safe.

## Mandatory runtime regression gate

A custom patch cannot be promoted to accepted gameplay state until runtime evidence covers:

### A. Target behavior
The bug/undesired interaction is actually fixed.

### B. Adjacent native lifecycle
Behavior immediately before and after the patched method still works.

Examples:
- attack -> death -> unlatch -> task finish -> follow;
- grab attempt -> prevention -> leader/follow remains valid;
- object filtering -> normal item spawn remains intact;
- kill prevention -> ordinary despawn/death still works.

### C. Reverse direction
For asymmetric compatibility rules, test both directions where relevant.

Example:
- Enemy -> Pikmin blocked;
- Pikmin -> Enemy still works.

### D. Repetition
Repeat the interaction when state persistence/reuse is plausible. A first successful occurrence is not enough if the object/type is reused later in the round or after lobby restart.

### E. Neighbor behavior
Check the closest related behavior that could have been accidentally suppressed.

Examples:
- corpse carrying after enemy combat patch;
- ordinary enemy death after kill protection;
- player interaction after Pikmin interaction patch;
- other enemies using the same base method.

### F. Logs
Confirm:
- intended patch marker appears;
- native completion markers appear when expected;
- no new exception/flood;
- no stale task/leader/work-state warnings;
- no hidden repeated retries.

## Promotion rule

A candidate with a new project-local patch remains **awaiting runtime validation** until the targeted and adjacent regression checks pass.

Do not promote a patch simply because:
- the compiler succeeded;
- GitHub Actions passed;
- Gale imported the profile;
- the main menu loaded;
- the original error message disappeared.

## Failure handling

When a project-local patch causes collateral damage:

1. mark the candidate failed;
2. preserve the runtime evidence;
3. identify which responsibility was unintentionally suppressed/changed;
4. document the failed approach in `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`;
5. add a permanent anti-regression rule if the failure pattern is generalizable;
6. prefer rollback/narrowing over adding another compensating repair layer.

## Required documentation for future patch builds

Every future patch-build plan should include a short **Patch Safety Review** section containing:

- exact method/component being patched;
- why that is the smallest safe surface;
- inherited/base lifecycle reviewed;
- known secondary responsibilities;
- reverse/adjacent behavior that must remain working;
- forbidden broader alternative;
- runtime acceptance checks.

If a build plan introducing a new custom patch lacks this review, it is incomplete.

## Project principle

**Custom compatibility code must fix less than it understands, never more.**

When there is a choice between:
- a narrow prevention-only hook with native lifecycle ownership preserved; and
- a broad replacement/disable/repair layer;

default to the narrow prevention-only hook unless evidence proves it insufficient.
