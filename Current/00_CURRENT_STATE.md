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

**S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED PARTIAL FIX**

Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`  
SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`  
Candidate record: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AG_RUNTIME_REJECTION_AWAITING_TARGETED_ANALYSIS`)
- Guarded build base: `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG`

## Exact next action

Re-run the currently hardened AnalysisTools/InspectMouthDogV81.ps1 from repository main against the user's installed Lethal Company_Data/Managed/Assembly-CSharp.dll using default Steam auto-detection. Three real Windows bootstrap failures are already fixed in repository history and must not be re-investigated unless they recur: disabled/missing NuGet sources, dotnet-install.ps1 output contaminating the helper return value, and the generated ilspycmd.exe shim failing to resolve the temporary .NET runtime. The current tool revision instead uses an isolated nuget.org-only config, output isolation, and an explicit launcher for ilspycmd.dll through the selected/bootstrapped dotnet.exe. No authoritative SourceEvidence/VanillaV81/MouthDogAI evidence exists yet. After a successful run creates source-evidence/mouthdog-v81-*, verify its branch/commit plus MANIFEST.json and MOUTHDOGAI_FOCUSED_DECOMPILE.txt, then prove the exact native perception/noise/target/lunge/collision owner/method boundary and the scrap/noise hypothesis before proposing or arming any successor. Do not build or start a runtime test before that boundary is proved.

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
