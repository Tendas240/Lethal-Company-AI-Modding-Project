# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Authority:** active/accepted profile readability, important DLL provenance, critical runtime-evidence retrieval  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-05

## Current accepted profile: S1.42AC

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

The current byte-integrity validator verifies the S1.42AC profile bytes and the fresh acceptance runtime bytes. The older S1.42AC runtime root remains preserved for historical rejection/provenance analysis and its SHA erratum remains governed separately by `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json` and `Current/INTEGRITY_ERRATA_REGISTRY.json`.

## Accepted predecessor / rollback baseline: S1.42AB

- Artifact: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Readable snapshot: `ProfileSources/S1.42AB/`
- File index: `ProfileSources/S1.42AB/FILE_INDEX.json`
- Readable manifest/export: `ProfileSources/S1.42AB/export.r2x`
- Runtime index: `RuntimeEvidence/S1.42AB/20260904T174010Z/INDEX.json`
- Raw runtime log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`
- Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

S1.42AC was built directly from S1.42AB and inherits its accepted interior-normalization implementation outside the isolated BCMER EventType config change.

## Important project DLL provenance

### S139 Compatibility Fixes 1.3.14

Source: `Patches/S139CompatibilityFixes/`  
Accepted DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`  
Runtime acceptance reference: `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

### S1.42AB interior-normalization DLL inherited by S1.42AC

Accepted injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`  
Build record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

S1.42AC's isolated delta did not replace this DLL.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also be represented in at least one readable indexed form: `ProfileSources`, `FILE_INDEX`, runtime `INDEX/analysis`, project source, build record, or canonical Knowledge/current-state documentation.

Git blob SHAs are not substitutes for project SHA-256 artifact provenance.
