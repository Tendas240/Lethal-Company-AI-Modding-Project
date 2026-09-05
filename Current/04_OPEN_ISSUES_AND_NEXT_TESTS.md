# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay gate

Accepted baseline remains **S1.42AC — BCMER EventType Equal Distribution**, `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`, SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`. Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

Latest built artifact / active candidate is **S1.42AF — Path-Length-Safe Microwave Packaging**. Its targeted Microwave/provider/path-length runtime gate is **PASS**, but formal full-stack acceptance is **deferred, not rejected** because the same normal run exposed a separate Mouth Dog / Eyeless Dog -> Pikmin compatibility gap. Runtime decision: `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`.

S1.42AF profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`  
Raw-log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`

The exact Microwave contract passed at runtime: `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`; both keysets were present; all 18 Moon/tag curves were scaled by `0.5`; all 18 Interior/tag curves were validation-only; Fatal = `0`.

No further S1.42AF runtime test is currently pending.

## Exact next action

Open `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md` and investigate LethalMin `1.1.108` ownership for Mouth Dog / Eyeless Dog -> Pikmin bite/grab.

1. Check native LethalMin configuration first for an exact one-way noninteraction option.
2. If config cannot fully block Dog -> Pikmin bite/grab while keeping Pikmin -> Dog combat native, inspect the exact Mouth-Dog adapter/collision/bite/grab method path.
3. Identify the earliest prevention-before-mutation point under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.
4. Preserve native LethalMin reverse-direction combat and enemy death/unlatch/task lifecycle.
5. Only after the owner/method contract is proven, prepare an isolated build plan. Do not invent or arm a successor ID before that point.

The current source gap is concrete: `Patches/S139CompatibilityFixes/Plugin.cs` protects Crawler/Thumper and Baboon Hawk through the prevention-only `PikminAI.GrabPikmin(Transform,float,int)` path, but has no Mouth-Dog branch. The cumulative compatibility DLL is byte-identical in S1.42AC and S1.42AF (`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`), so this is classified as a baseline gap exposed during S1.42AF, not an S1.42AF Microwave regression.

Current controllers: `BuildSpecs/current.json` disabled with id `IDLE_AFTER_S1.42AF_RUNTIME_GATE_PASS_MOUTH_DOG_ANALYSIS_SELECTED`, guarded base S1.42AC, and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`. No successor is armed.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items remain CullFactory junkrooms/shatteredrooms exceptions, Mausoleum fog, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, and broader evidence-driven LethalMin teardown repair.
