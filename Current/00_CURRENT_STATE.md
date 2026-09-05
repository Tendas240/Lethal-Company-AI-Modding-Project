<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-06  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  
Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`

## Latest built artifact

**S1.42AF — Path-Length-Safe Microwave Packaging — RUNTIME ACCEPTED**

Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  
Candidate record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AF_ACCEPTANCE_MOUTHDOG_ANALYSIS`)
- Guarded build base: `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`

## Exact next action

Analyze the confirmed MouthDog/EyelessDog -> Pikmin targeting/bite/grab path from Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md under Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md and Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md. Inspect the exact LethalMin owner/method/inheritance/config contract and Patches/S139CompatibilityFixes/Plugin.cs; determine whether native configuration can prevent targeting or whether the existing exact PikminAI.GrabPikmin(Transform,float,int) prevention-only guard can safely cover MouthDog/EyelessDog. Preserve Pikmin -> Mouth Dog native behavior. Do not arm or build a successor until the exact contract is proved.

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
