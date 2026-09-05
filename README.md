<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/PROJECT_KNOWLEDGE_MAP.md`

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

Current-chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`. When the user requests transfer to a new ChatGPT chat, the active chat must execute that procedure and generate a fresh new-chat prompt from current repository authority.

## Current state

Accepted baseline: **S1.42AC — BCMER EventType Equal Distribution**  
Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Latest built artifact: **S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Active candidate: **none**. Runtime test outstanding: **no**. Build successor armed: **no**.

Exact next action: S1.42AD Functional Microwave spawn-rarity reduction is the explicitly selected next scope. A source-only draft exists at Patches/S142ADCodeRebirthMicrowaveSpawnTuning/, but no profile has been built or armed. Before building, independently review the draft against Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md, verify the exact CodeRebirth/DawnLib owner and 19-curve contract, and resolve the exact reduction magnitude: the draft uses 0.5 while current canonical requirements specify only that the Microwave should be rarer. Do not build or runtime-test until the target is explicitly confirmed and a build spec is armed.

## Semantic navigation

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
