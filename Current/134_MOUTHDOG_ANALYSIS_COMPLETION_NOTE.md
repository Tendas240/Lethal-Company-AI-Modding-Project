# Mouth Dog / Eyeless Dog -> Pikmin Analysis Completion Note

**Status:** SOURCE/CONFIG OWNERSHIP ANALYSIS COMPLETE  
**Baseline:** S1.42AF  
**Planned successor:** S1.42AG — Mouth Dog Pikmin One-Way Protection  
**Build status:** NOT BUILT  
**Runtime test:** NONE OUTSTANDING

The repository's required pre-build investigation for the S1.42AF Mouth Dog / Eyeless Dog -> Pikmin compatibility gap is complete.

Resolved questions:

- no native LethalMin 1.1.108 boolean config exists for one-way Mouth Dog -> Pikmin disable;
- `Eyeless Dog Bite Limit = 0` is not a valid disable contract;
- exact owner is `LethalMin.MouthDogPikminEnemy : PikminEnemy` mapped from `MouthDogAI`;
- exact harmful path reaches `PikminAI.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`;
- the common exact `PikminAI.GrabPikmin(Transform,float,int)` guard is before core Pikmin mutation but is later than MouthDog adapter-local `GrabbedPikmin.Add` and bite animation dispatch;
- preferred primary prevention boundary is exact declared `MouthDogPikminEnemy.DoCheckInterval()`;
- keeping the MouthDog adapter enabled preserves the opposite-direction native Pikmin combat/lifecycle path;
- the proposed patch boundary passes the project-local patch safety review.

Authorities:

- `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`
- `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`
- `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`
- `BuildSpecs/S1.42AG_PLAN.md`
- `Current/133_S1.42AG_PLANNING_STATE.md`

Exact next project action is implementation/build preparation for S1.42AG in a later explicit segment. This note does not arm the controller or create a candidate.
