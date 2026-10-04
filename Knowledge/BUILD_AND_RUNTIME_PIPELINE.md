# Build and Runtime Evidence Pipeline

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic routing summary; implementation/policy evidence remains repository-native  
**Canonical-For:** `build_pipeline`, `runtime_upload_and_ingest`  
**Evidence:** `Current/09_REPOSITORY_FIRST_AUTOMATION.md`, `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`  
**Related:** `BuildSpecs/README.md`, `BuildSystem/`, `.github/workflows/`, `RuntimeInbox/`, `RuntimeEvidence/`, `Knowledge/GALE_PROFILE_WORKFLOW.md`  
**Last-Validated:** 2026-09-06

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

## Gale runtime path-length preflight

Every new profile/review identity must pass `RepositoryTools/gale_profile_path_length_guard.py`. Permanent Knowledge Architecture CI scans repository BuildSpecs, while `.github/workflows/profile-build.yml` validates the current requested spec before a canonical build. The guard projects the known deepest LC Office preloader and SoundAPI binding runtime paths against the observed project-machine Gale root and permits at most 255 characters.

Exact historical specs already proven preloader-blocked may remain in the repository as evidence, but they are not valid new build targets. The canonical Gale launcher independently checks the actual local profile root before destructive replacement, so a different local root cannot silently invalidate the repository-side projection.

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

For the create-or-replace probe, **HTTP 404 for a missing inbox file is the normal first-create case**. The uploader must suppress/handle that probe without allowing PowerShell native-command stderr or `$ErrorActionPreference` behavior to abort before the subsequent PUT. A real upload failure must still fail closed.

When `runtime-ingest.yml` creates a bot-generated evidence commit with `GITHUB_TOKEN`, normal push-triggered workflows are suppressed. The ingest workflow must therefore verify that remote `main` still equals the exact generated commit and explicitly dispatch `Knowledge Architecture` for that exact head, mirroring the profile-index bot-follow-up contract. Handover may treat that exact-head `workflow_dispatch` run as the permanent gate only when its `head_sha` exactly equals final `main`.

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

## Branch lifecycle and merged-PR cleanup

Normal project work should use a short-lived same-repository working branch plus PR/CI/merge when a repository change is non-trivial or when an existing project procedure requires a PR. The merged working branch is not historical authority: merged commits, PR metadata, build/runtime records and explicit archival tags provide the durable provenance.

`.github/workflows/merged-branch-cleanup.yml` automatically deletes the head branch after a **merged** same-repository pull request. It deliberately does not delete:

- `main`;
- `runtime-large`, because the very-large-runtime workflow actively uses it as a disposable transport branch;
- `pre-overhaul-freeze-20260904-5dbd0e6`, because it is an explicit recovery/provenance branch.

The cleanup workflow ignores fork PRs and closed-but-unmerged PRs. Before deletion it verifies that the branch still points at the exact merged PR head SHA; any ref drift fails closed instead of deleting a moved/reused branch.

If a temporary branch contains unique historical staging lineage that should remain directly addressable even though the branch itself is obsolete, preserve the exact head with an explicit annotated archival tag before deleting the branch. Do not keep ordinary merged feature/build/handover branches indefinitely merely as informal history.

If a new permanent infrastructure or recovery branch is introduced in the future, add it to the retained-branch list in `.github/workflows/merged-branch-cleanup.yml` as part of the same change that establishes that branch's permanent role.

## AGDIAG1 frozen inactive review artifact

The S1.42AK-AGDIAG1 review-build path is now main-integrated under
`Current/257_S1.42AK_AGDIAG1_INACTIVE_REVIEW_BUILD_INTEGRATION_RECONCILIATION.md`.

The dedicated workflow/build validator established compiler/archive validity and froze one authoritative Actions artifact without publishing it:

- build head: `46a5924ae142b0c00ff9fbbc6fecec5e2a4badae`;
- build run: `37199874193` / #4;
- artifact ID: `11302468045`;
- Actions ZIP SHA-256: `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`;
- profile SHA-256: `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`;
- DLL SHA-256: `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`;
- independent artifact rehash / ZIP CRC: **PASS**;
- Gale projected runtime path: **217/255 PASS**.

The committed checkpoint/freeze guard makes those exact bytes authoritative and skips later reconstruction. Intermediate race artifact `11302835640` is explicitly superseded and has no publication/import/activation authority.

A later publication step, if separately authorized, must materialize **only** artifact `11302468045` and verify its exact hashes; it must never rebuild the candidate or choose an artifact by recency/name prefix. No profile publication, `ProfileSources` indexing, Gale import, runtime activation or gameplay is currently authorized.

## AGDIAG1 exact-byte publication authorization

Publication transport is now authorized by `Current/258_S1.42AK_AGDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`, but no publication bytes have yet been written.

A valid publication checkpoint must:

- fetch Actions artifact **11302468045 by exact ID**;
- reject artifact `11302835640` and any other artifact;
- verify ZIP SHA-256 `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`;
- verify profile SHA-256 `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`;
- verify DLL SHA-256 `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`;
- perform those checks immediately before byte-for-byte materialization;
- never rebuild, reconstruct or substitute the reviewed bytes.

The future publication branch may materialize `Profiles/LC V1 S1.42AK-AGD1.r2z` plus deterministic readable `ProfileSources/S1.42AK-AGDIAG1/` snapshot/evidence. Canonical profile-index mapping and `Profiles/EXPECTED_HASHES.json` remain outside that checkpoint, as do Gale import, controller changes, runtime activation and gameplay.

