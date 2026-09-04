# Atomic Current-State Transition Policy

**Status:** CURRENT / CANONICAL REPOSITORY STATE POLICY  
**Authority:** acceptance/rejection/build transition synchronization  
**Canonical-For:** atomic current-state transition discipline  
**Last-Validated:** 2026-09-04

## Single structured source

`Current/CURRENT_STATE.json` is the structured source for the compact global state and generated bootstrap navigation.

Generated from it by `RepositoryTools/render_current_navigation.py`:

- `README.md`
- `START_HERE_ChatGPT_Masterprompt.txt`
- `Current/00_CURRENT_STATE.md`
- `Current/01_HANDOVER_CORE.md`

CI runs the renderer in `--check` mode. A state transition is invalid if those generated mirrors drift.

## Controller/lineage coupling

`RepositoryTools/knowledge_architecture_validator.py` additionally requires consistency among:

- `Current/CURRENT_STATE.json`;
- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `Current/AUTO_BUILD_RESULT.json` for the latest built artifact;
- `Current/BUILD_LINEAGE.json`;
- accepted/latest profile paths and SHA-256 values;
- readable `ProfileSources/.../FILE_INDEX.json` snapshots;
- runtime evidence roots.

This converts previously manual prose synchronization into a machine-enforced transition gate.

## Required order for a future build-state change

When accepting, rejecting, arming or retiring a candidate:

1. update the evidence/decision record first;
2. update `Current/CURRENT_STATE.json` to the intended new state;
3. update the relevant controller (`BuildSpecs/current.json` and/or `RuntimeInbox/ACTIVE_BUILD.txt`);
4. update `Current/BUILD_LINEAGE.json` and its human mirror;
5. update any topic-specific machine status referenced by the Knowledge Map;
6. run `python RepositoryTools/render_current_navigation.py`;
7. run `python RepositoryTools/knowledge_architecture_validator.py`;
8. run `python RepositoryTools/answerability_regression.py`;
9. commit the complete logical transition together whenever practical.

If GitHub API tooling necessarily emits multiple commits, the transition is not considered complete until the final validation commit is green. Intermediate drift is a migration/work-in-progress state, not authoritative acceptance.

## Runtime-test transition

If `runtime_test_outstanding` becomes true, the associated candidate/build evidence must identify the exact canonical uploader. User-facing test instructions must include that build-specific PowerShell one-liner in the same response.

## Fail closed

Do not promote a build when the current-state renderer, controller consistency checks, lineage checks, ProfileSources checks, or answerability/knowledge validation fails. Fix the state graph first.
