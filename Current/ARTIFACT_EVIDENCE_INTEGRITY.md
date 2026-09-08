<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Authority:** active/accepted/profile-decision readability, important DLL provenance, critical runtime-evidence retrieval  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-08

## Current accepted profile: S1.42AF

- Artifact: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Readable snapshot: `ProfileSources/S1.42AF/`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime index: `RuntimeEvidence/S1.42AF/20260905T223738Z/INDEX.json`
- Runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`

S1.42AF remains the sole accepted gameplay base.

## Active runtime candidate: S1.42AH

- Status: **ACTIVE_RUNTIME_CANDIDATE_PENDING / NOT ACCEPTED**
- Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- Readable snapshot: `ProfileSources/S1.42AH/`
- File index: `ProfileSources/S1.42AH/FILE_INDEX.json`
- Export: `ProfileSources/S1.42AH/export.r2x`
- Candidate record: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Project status: `Current/Projektstatus_S1.42AH_CANDIDATE.json`
- Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`

Runtime test outstanding: **yes**. No S1.42AH runtime index or runtime-log SHA is expected yet. The byte-integrity gate must verify the candidate profile and readable snapshot now; runtime evidence becomes mandatory only after an explicit runtime decision.

## Rejected predecessor: S1.42AG

S1.42AG remains preserved as `RUNTIME_REJECTED_PARTIAL_FIX` with profile SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee` and runtime evidence `RuntimeEvidence/S1.42AG/20260906T085500Z/`. It must not be used as a gameplay/build base.

## Accepted historical predecessors

- S1.42AC: corrected accepted BCMER evidence at `RuntimeEvidence/S1.42AC/20260904T235720Z/`; rejection-era provenance remains separately preserved.
- S1.42AB: accepted interior-normalization evidence at `RuntimeEvidence/S1.42AB/20260904T174010Z/`.

## Important DLL provenance

### S139CompatibilityFixes.dll

Accepted historical binary provenance remains SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960` from the earlier accepted compatibility lifecycle. S1.42AH rebuilds the cumulative DLL as candidate SHA-256 `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`; this candidate SHA does not become accepted-binary authority until runtime acceptance.

### S1.42AB interior normalization DLL

Accepted injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

### S1.42AF Functional Microwave spawn-tuning DLL

Accepted DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`. S1.42AH does not alter it.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also be represented in at least one readable indexed form: `ProfileSources`, `FILE_INDEX`, runtime `INDEX/analysis`, project source, build record, or canonical current-state/Knowledge documentation.

For an `ACTIVE_RUNTIME_CANDIDATE_PENDING`, profile bytes and readable snapshot are current-critical before runtime. Runtime `INDEX`/raw-log bytes become mandatory after the first explicit runtime decision.
