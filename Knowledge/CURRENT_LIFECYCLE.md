# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/125_S1.42AE_V23_FALSE_POSITIVE_AND_S1.42AC_CONTROL_CONFIRMATION.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/Projektstatus_S1.42AF_CANDIDATE.json`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AF_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/CODEREBIRTH.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Knowledge/GALE_PROFILE_WORKFLOW.md`  
**Last-Validated:** 2026-09-05

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the accepted full-normal-stack gameplay/rollback baseline.

## Rejected predecessor

**S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED.**

S1.42AD failed closed because it expected `InteriorCurves=0`, while runtime exposed 18 Interior/tag curves. No `0.5` mutation executed. Rejection authority: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`.

## Superseded S1.42AE candidate

**S1.42AE — Functional Microwave Provider Contract Correction — SUPERSEDED FOR PATH-LENGTH-SAFE PACKAGING / NOT GAMEPLAY-REJECTED.**

The corrected provider code was never reached during the failing launches. v2.4 positively verified both SoundAPI materialization contracts, and direct pre-launch plus post-failure filesystem checks showed the exact nested `me.loaforc.soundapi.lethalcompany.dll` still present and non-empty at `40960` bytes. The full S1.42AE binding path measured `262` characters. BepInEx/Mono nevertheless failed before chainloader startup with `DirectoryNotFoundException` / `FileNotFoundException` for that path.

Accepted S1.42AC passed the same SoundAPI dependency family with a corresponding path length of `247`. Path-length compatibility is therefore the leading root-cause classification. This is packaging/preloader evidence, not a rejection of the corrected Microwave provider logic. Decision: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`.

## Active candidate

**S1.42AF — Path-Length-Safe Microwave Packaging — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- Gale profile name: `LC V1 S1.42AF Microwave Fix`
- Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Build workflow run: `33993880634` — SUCCESS
- Automated build commit: `2cab9044579e74739669440699c763a32f0fe379`
- Candidate record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Project status: `Current/Projektstatus_S1.42AF_CANDIDATE.json`
- Plan: `BuildSpecs/S1.42AF_PLAN.md`
- Snapshot: `ProfileSources/S1.42AF/`

S1.42AF was built directly from accepted S1.42AC, not from S1.42AE. The only intended packaging variable is the shorter Gale profile identity. Automated QC reports exactly `export.r2x` changed and exactly the unchanged-source Microwave plugin DLL added, with no package/config drift.

The source contract is unchanged from S1.42AE: validate CodeRebirth `1.6.9`, DawnLib/Dusk `0.9.25`, one Functional Microwave `MapObjectSpawnMechanics` provider, `PrioritiseMoons=true`, exact 18 Moon/tag curves and exact 18 Interior/tag curves, then scale only the 18 Moon/tag curves by `0.5`; Interior curves are validation-only. Runtime plugin markers intentionally still identify `S1.42AE CodeRebirth Microwave Spawn Tuning 1.0.0`.

## Current controllers

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`
- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AF_BUILD_AWAITING_RUNTIME_VALIDATION`.
- Guarded base: `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- No successor is armed.

## Exact next project action

Canonical Gale helper: `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`.

1. Import S1.42AF with the canonical v2.4 Gale launcher and require the final positive import/materialization proof.
2. Confirm the nested LC-binding DLL is non-empty under the short S1.42AF profile path and that the full path is below 260 characters.
3. Start the game. The path-length hypothesis passes its first gate only if BepInEx reaches normal preloader/chainloader/main-menu/lobby startup.
4. Play one normal run far enough for ordinary moon/interior generation.
5. Upload the complete fresh S1.42AF `LogOutput.log` with the exact uploader in `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`.
6. Evaluate the preserved S1.42AE plugin marker, dependency versions, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keysets, final 18 Moon curves x0.5 / 18 Interior validation-only marker, and fatal/project-critical regressions before ACCEPT or REJECT.

Canonical Gale one-liner:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Exact S1.42AF log uploader is frozen in `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md` and must be used after the run.
