# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Authority:** active/accepted/profile-decision readability, important DLL provenance, critical runtime-evidence retrieval  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-06

## Current accepted profile: S1.42AF

- Artifact: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Readable snapshot: `ProfileSources/S1.42AF/`
- File index: `ProfileSources/S1.42AF/FILE_INDEX.json`
- Readable manifest/export: `ProfileSources/S1.42AF/export.r2x`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime index: `RuntimeEvidence/S1.42AF/20260905T223738Z/INDEX.json`
- Raw runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`
- Build-specific Functional Microwave DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`

The accepted runtime evidence proves the shortened nested SoundAPI LethalCompany binding path at 226 characters, normal BepInEx/game startup, and the exact Functional Microwave provider contract: CodeRebirth `1.6.9`, DawnLib/Dusk `0.9.25`, `PrioritiseMoons=true`, 18 Moon/tag curves and 18 Interior/tag curves, with only the 18 Moon/tag curves scaled by `0.5`.

## Latest built artifact: S1.42AG — runtime rejected partial fix

- Artifact: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Readable snapshot: `ProfileSources/S1.42AG/`
- File index: `ProfileSources/S1.42AG/FILE_INDEX.json`
- Readable manifest/export: `ProfileSources/S1.42AG/export.r2x`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Project status: `Current/Projektstatus_S1.42AG_REJECTED.json`
- Runtime index: `RuntimeEvidence/S1.42AG/20260906T085500Z/INDEX.json`
- Raw runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`
- Candidate compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`

This evidence proves a **partial fix only**. The S1.42AG `Priority.First` prevention guard on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` armed and executed, the prior LethalMin bite/grab/death-timer mutation signature was absent, and `Work state with no task assigned!` fell from 707 in the S1.42AF exposure run to 0. However, the user directly observed a Mouth Dog still visibly targeting and attacking a scrap-carrying Purple Pikmin, and reverse-direction Pikmin -> Mouth Dog combat/latch preservation was not positively proven. S1.42AG is therefore not accepted and is not a safe gameplay base.

The S1.42AG candidate compatibility DLL SHA above is retained as rejected-build provenance only. It does **not** replace any accepted DLL authority below.

## Accepted predecessor: S1.42AC

- Artifact: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Readable snapshot: `ProfileSources/S1.42AC/`
- File index: `ProfileSources/S1.42AC/FILE_INDEX.json`
- Readable manifest/export: `ProfileSources/S1.42AC/export.r2x`
- Corrected acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Fresh acceptance runtime index: `RuntimeEvidence/S1.42AC/20260904T235720Z/INDEX.json`
- Fresh raw runtime log SHA-256: `98170374c4ffb6f40322a8019ad7f7f807e900525717dfdf7e70698bd7f28fa8`
- Historical rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Corrected source analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`
- Historical rejection-era runtime index: `RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json`
- Historical rejection-era authoritative raw-log SHA-256: `fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`

The older S1.42AC rejection-era runtime root remains preserved for provenance analysis; its SHA erratum remains governed by `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json` and `Current/INTEGRITY_ERRATA_REGISTRY.json`.

## Earlier accepted predecessor: S1.42AB

- Artifact: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Readable snapshot: `ProfileSources/S1.42AB/`
- File index: `ProfileSources/S1.42AB/FILE_INDEX.json`
- Readable manifest/export: `ProfileSources/S1.42AB/export.r2x`
- Runtime index: `RuntimeEvidence/S1.42AB/20260904T174010Z/INDEX.json`
- Raw runtime log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`
- Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

## Important project DLL provenance

### S139 Compatibility Fixes 1.3.14

Source: `Patches/S139CompatibilityFixes/`  
Accepted DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`  
Runtime acceptance reference: `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

S1.42AG rebuilt the cumulative compatibility DLL as a rejected candidate. Its candidate SHA is retained above and in `Current/133` / `Current/134`; it does not silently replace this accepted-binary provenance entry.

### S1.42AB interior-normalization DLL inherited through S1.42AF

Accepted injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`  
Build record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

### S1.42AF Functional Microwave spawn-tuning DLL

Source root: `Patches/S142AEFunctionalMicrowaveSpawnTuning/`  
Accepted DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`  
Build record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`

The source contract was established for S1.42AE and reused under S1.42AF path-length-safe packaging; the preserved runtime plugin identity therefore intentionally contains `S1.42AE`.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also be represented in at least one readable indexed form: `ProfileSources`, `FILE_INDEX`, runtime `INDEX/analysis`, project source, build record, or canonical Knowledge/current-state documentation.

Git blob SHAs are not substitutes for project SHA-256 artifact provenance.
