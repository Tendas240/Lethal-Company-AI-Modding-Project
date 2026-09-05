# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-05

## Current gameplay gate

Accepted baseline remains **S1.42AC — BCMER EventType Equal Distribution**, `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`, SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`. Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

Active runtime candidate is **S1.42AF — Path-Length-Safe Microwave Packaging — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**. Profile `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`, build run `33993880634`, build commit `2cab9044579e74739669440699c763a32f0fe379`, DLL SHA-256 `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`. Candidate authority: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`.

S1.42AE is superseded for packaging/path-length reasons, not gameplay-rejected. Its provider code never ran; the exact SoundAPI LC-binding DLL remained physically present at 40960 bytes before and after the failed launch, while the full path measured 262 characters and BepInEx/Mono failed before chainloader startup. Decision: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`.

## Exact next action

Import S1.42AF through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, require the positive export plus two-SoundAPI materialization proof, confirm the shortened LC-binding path is below 260, then start the game. If startup is healthy, play one normal run far enough for ordinary moon/interior generation and upload the complete fresh S1.42AF `LogOutput.log` with the exact uploader in `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`. Evaluate the intentionally preserved `S1.42AE CodeRebirth Microwave Spawn Tuning 1.0.0` marker, CodeRebirth 1.6.9 / DawnLib-Dusk 0.9.25, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keysets, final 18 Moon curves x0.5 / 18 Interior validation-only marker, and regression/fatal markers before lifecycle promotion.

Current controllers: `BuildSpecs/current.json` disabled with id `IDLE_AFTER_S1.42AF_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded base S1.42AF, and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`. No successor is armed.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items remain CullFactory junkrooms/shatteredrooms exceptions, Mausoleum fog, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, and evidence-driven LethalMin teardown repair.
