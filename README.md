<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/PROJECT_KNOWLEDGE_MAP.md`

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`: execute one bounded segment, report the checkpoint, then stop and wait for explicit user continuation before the next non-final segment. Short atomic work may be one segment.

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

Current-chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`. Handover work is also continuation-gated by `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

## Current state

Accepted baseline: **S1.42AF — Path-Length-Safe Microwave Packaging**  
Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED PARTIAL FIX**  
SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`

Active candidate: **none**. Runtime test outstanding: **no**. Build successor armed: **no**.

Exact next action: Re-run the currently hardened AnalysisTools/InspectMouthDogV81.ps1 from repository main against the user's installed Lethal Company_Data/Managed/Assembly-CSharp.dll using default Steam auto-detection. Three real Windows bootstrap failures are already fixed in repository history and must not be re-investigated unless they recur: disabled/missing NuGet sources, dotnet-install.ps1 output contaminating the helper return value, and the generated ilspycmd.exe shim failing to resolve the temporary .NET runtime. The current tool revision instead uses an isolated nuget.org-only config, output isolation, and an explicit launcher for ilspycmd.dll through the selected/bootstrapped dotnet.exe. No authoritative SourceEvidence/VanillaV81/MouthDogAI evidence exists yet. After a successful run creates source-evidence/mouthdog-v81-*, verify its branch/commit plus MANIFEST.json and MOUTHDOGAI_FOCUSED_DECOMPILE.txt, then prove the exact native perception/noise/target/lunge/collision owner/method boundary and the scrap/noise hypothesis before proposing or arming any successor. Do not build or start a runtime test before that boundary is proved.

## Semantic navigation

- ChatGPT segmented execution: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
- Topic router: `Current/PROJECT_KNOWLEDGE_MAP.md` / `.json`
- Chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`
- Build history: `Current/BUILD_LINEAGE.md` / `.json`
- Authority/history classification: `Current/DOCUMENT_AUTHORITY.md` / `.json`
- Artifact/runtime-evidence integrity: `Current/ARTIFACT_EVIDENCE_INTEGRITY.md` / `.json`
- Deferred work: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical handovers, candidate notes, rejection records and runtime decisions are preserved as evidence, but they do not override the current state/topic authority graph or a later explicit acceptance decision.

## Repository overhaul

Status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified pre-overhaul recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904` at frozen source commit `5dbd0e637a480d8591773e422bbca4b0654cad20`.  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.

No local repository clone or local profile build should be required from the user while repository-native artifacts and automation are sufficient.
