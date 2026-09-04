# Build and Runtime Evidence Pipeline

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic routing summary; implementation/policy evidence remains repository-native  
**Canonical-For:** `build_pipeline`, `runtime_upload_and_ingest`  
**Evidence:** `Current/09_REPOSITORY_FIRST_AUTOMATION.md`, `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`  
**Related:** `BuildSpecs/README.md`, `BuildSystem/`, `.github/workflows/`, `RuntimeInbox/`, `RuntimeEvidence/`, `Knowledge/GALE_PROFILE_WORKFLOW.md`  
**Last-Validated:** 2026-09-05

## Repository-first rule

GitHub is the durable Source of Truth and build workspace. Do not require the user to keep a local clone or run local profile-build scripts when the required base artifacts are already in the repository.

Canonical build control:

- request/controller: `BuildSpecs/current.json`
- build engine: `BuildSystem/profile_builder.py`
- build workflow: `.github/workflows/profile-build.yml`
- latest result: `Current/AUTO_BUILD_RESULT.json` and `.md`
- readable output snapshot: `ProfileSources/<build_id>/`
- final profile: `Profiles/*.r2z`

A build must be guarded by its exact base profile path and SHA-256. Binary profile facts required for future reasoning must also exist in readable ProfileSources evidence.

## Runtime control and evidence

- runtime-active/evidence-attribution pointer: `RuntimeInbox/ACTIVE_BUILD.txt`
- normal upload inbox: `RuntimeInbox/Current/`
- normal ingest workflow: `.github/workflows/runtime-ingest.yml`
- persisted evidence: `RuntimeEvidence/<build>/<timestamp>/`
- log analyzer: `BuildSystem/runtime_log_analyzer.py`

`BuildSystem/runtime_ingest.py` reads `RuntimeInbox/ACTIVE_BUILD.txt` and uses that build ID as the destination namespace under `RuntimeEvidence/`. Therefore the pointer must identify the profile whose completed runtime evidence is being uploaded.

`ACTIVE_BUILD` is **not acceptance authority**. It may identify a currently installed/tested artifact that is rejected or not promoted while `Current/CURRENT_STATE.json.accepted_baseline` remains a different build. Such a pointer does not create an active candidate and does not promote the artifact.

The ingest process records source hashes and bounded analysis instead of requiring ChatGPT to load an entire raw log at once.

## Very-large logs

When a raw log is too large for the normal GitHub Contents path, use the dedicated disposable `runtime-large` branch and the contract in `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`.

Large-log tooling includes compression/splitting, streaming analysis, a 14-day raw Actions artifact, compact evidence committed to `main`, and targeted raw-log query extraction through `RuntimeAnalysis/QUERY.json`.

Do not commit a >100 MiB raw log as a normal main-branch blob.

## Mandatory ready-to-test response contract

When a future build/profile is ready for user runtime testing, ChatGPT must provide in the same response:

1. the canonical repository-driven Gale replacement PowerShell one-liner;
2. the exact build-specific self-contained PowerShell one-line runtime-log uploader.

The uploader must bootstrap/resolve `gh`, authenticate when required, verify the exact local `LogOutput.log`, and create/replace `RuntimeInbox/Current/LogOutput.log` on `main` without requiring a local repository clone.

If the log is unusually large, provide the corresponding self-contained large-log PowerShell path instead.

A separate but equally important case is a **completed test whose log has not yet been ingested**. In that case, do not infer from `runtime_test_outstanding = false` that no uploader is needed. Provide the uploader for the build named by `RuntimeInbox/ACTIVE_BUILD.txt` and do not require the user to repeat the run solely for evidence submission.

## Lifecycle consistency

For a ready candidate, the following must agree:

- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `Current/AUTO_BUILD_RESULT.json.build_id`;
- candidate/project-state record;
- `BuildSpecs/current.json` lifecycle state.

For an idle/no-successor state, `BuildSpecs/current.json` may remain disabled while `ACTIVE_BUILD` identifies either the accepted baseline or another known build that is currently installed/tested for runtime-evidence attribution. `Current/CURRENT_STATE.json.controllers.runtime_active_build` must match the pointer. This does not alter the accepted baseline, candidate status, or promotion state.

`Knowledge/CURRENT_LIFECYCLE.md` is the human router for the current combination of accepted baseline, runtime-active build and next action.
