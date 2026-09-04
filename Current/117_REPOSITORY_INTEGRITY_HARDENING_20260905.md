# 117 — Repository Integrity Hardening after Independent Re-Audit

**Date:** 2026-09-05  
**Status:** IMPLEMENTED / VALIDATION PENDING  
**Scope:** repository information integrity, provenance, auditability and CI only  
**Gameplay/config/profile/runtime behavior change:** NONE

## Trigger

The independent frozen-state re-audit in `Current/116_INDEPENDENT_PREOVERHAUL_CONTRACT_AUDIT_20260905.md` established two important qualifications:

1. the final Phase 0–11 deliverables are present and the end state is valid, but exact individual Phase 3–10 completion order is not independently reconstructible from immutable phase-completion checkpoints;
2. the old incorrect S1.42AC raw-runtime-log SHA survived in additional retained historical documents after the first narrow provenance remediation.

The hardening here addresses the reusable failure modes without rewriting history and without changing gameplay state.

## 1. Measures that already existed before this hardening

- `Current/CURRENT_STATE.json` is the single compact machine-readable global current state.
- `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/00_CURRENT_STATE.md` and `Current/01_HANDOVER_CORE.md` are renderer-controlled and CI already checked byte equality.
- `RepositoryTools/knowledge_architecture_validator.py` already checked current state/controller/lineage/reference consistency and orphan Knowledge topics.
- `RepositoryTools/runtime_sha_provenance_validator.py` already performed a repository-wide scan for the known superseded S1.42AC raw-log SHA.
- `RepositoryTools/overhaul_contract_validator.py` already independently checked frozen-contract obligations and backup-before-structural-migration provenance from Git history.
- `RepositoryTools/answerability_regression.py` already maintained semantic routing regression cases.
- `Current/DOCUMENT_AUTHORITY.json` already distinguished current authority from retained historical snapshots.
- The overhaul was non-destructive; historical evidence was retained instead of silently rewritten.

## 2. Measures added by this hardening

### A. Central errata / known-bad registry

Added `Current/INTEGRITY_ERRATA_REGISTRY.json` as current machine authority for known bad values and supersession qualifications. The first registered known-bad value is the superseded S1.42AC raw-log SHA; the registry points to the authoritative replacement and the exact historical documents allowed to retain the old value.

The registry also records the Phase 3–10 historical checkpoint limitation so the repository cannot drift back to an overstrong "strict order historically proven" claim.

### B. Actual-byte SHA validation

Added `RepositoryTools/artifact_byte_integrity_validator.py`.

It recomputes SHA-256 from the actual repository bytes for every profile listed in `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`, including current critical S1.42AB and S1.42AC artifacts, and for their linked raw `LogOutput.log` files. It also checks raw-log size, RuntimeEvidence INDEX SHA and embedded analysis `source_sha256` against the actual bytes.

This closes the distinction between "metadata agrees" and "the stored bytes are exactly the expected artifact".

### C. Repository-wide integrity / authority linter

Added `RepositoryTools/repository_integrity_guard.py`.

It checks:

- repository-wide occurrences of every value registered in `Current/INTEGRITY_ERRATA_REGISTRY.json`;
- every occurrence must be locally qualified or explicitly registered historical evidence;
- duplicate same-level current authority claims in `Current/DOCUMENT_AUTHORITY.json`;
- orphan `Knowledge/*.md` topics;
- required generated-file protection markers.

### D. Generated-file protection

`RepositoryTools/render_current_navigation.py` now emits an explicit:

`GENERATED — DO NOT MANUALLY EDIT`

marker into all four generated bootstrap/current-navigation files. The existing byte-exact renderer check remains mandatory.

### E. Validator coverage and blindspots

Added `Current/VALIDATOR_COVERAGE.json`.

Each permanent validator now has explicit machine-readable documentation for:

- what it checks;
- which paths/data it scans;
- what it does **not** prove.

A green CI run must not be cited as proof for an obligation outside this declared coverage.

### F. Negative validator tests

Added `RepositoryTools/validator_selftest.py` with representative synthetic fixtures:

- unqualified known-bad SHA -> MUST FAIL;
- registered historical bad SHA -> MAY PASS;
- two same-level current authorities for one claim -> MUST FAIL;
- orphan Knowledge topic -> MUST FAIL;
- phase 5 checkpoint without phase 4 -> MUST FAIL.

### G. Future immutable phase checkpoints

Added `Current/MULTIPHASE_CHECKPOINT_POLICY.json` and `RepositoryTools/phase_checkpoint_validator.py`.

For new multi-phase repository programs, completion records live under:

`ExecutionCheckpoints/<process>/phase_<NN>.json`

The validator enforces predecessor PASS order, immutable checkpoint history, existing completion commits and presence of declared produced artifacts in those commits.

This is prospective. It intentionally does **not** fabricate missing Phase 3–10 checkpoints for the completed 2026 overhaul.

### H. Broader CI trigger coverage

`.github/workflows/knowledge-architecture.yml` now also reacts to authority-relevant changes under:

- `Profiles/**`
- `ProfileSources/**`
- `RuntimeEvidence/**`
- `Patches/**`
- `BuildSystem/**`
- `RuntimeTools/**`
- `BuildSpecs/**`
- `ExecutionCheckpoints/**`

The permanent gate now runs nine layers: renderer, architecture/state, actual-byte integrity, central integrity/authority, S1.42AC provenance, future phase checkpoints, frozen contract, answerability regression and negative self-tests.

## 3. Recommendations deliberately not implemented

### Branch protection / required checks

**Classification: OPTIONAL HARDENING.**

Not enabled. The repository currently relies on a functioning direct repository-native automation/write workflow. Enabling mandatory PR protection without separately designing bypass/automation policy could block that workflow. This remains a governance choice, not an integrity blocker.

### GitHub-archive the standalone backup

**Classification: OPTIONAL HARDENING.**

The standalone backup is verified and described as historical/read-only, but GitHub repository metadata is not archived. Archiving would be useful governance hardening but is not required for content integrity.

### Retroactive Phase 3–10 checkpoint manufacture

**Not implemented by design.**

Doing so would create false historical evidence. The limitation is preserved as an explicit non-blocking historical/auditability qualification.

### Generic automatic validation of arbitrary future ChatGPT handover prompts

**Not implemented as a separate CI parser.**

The repository already generates the canonical takeover files from `Current/CURRENT_STATE.json`, validates them byte-for-byte, validates controllers/lineage/authority and routes through the Knowledge Map. CI cannot reliably validate arbitrary prose that has not been committed. Future handovers should use the generated canonical takeover artifacts rather than introducing another manually maintained handover truth.

### Universal semantic detection of every possible stale word such as "current"

**Not implemented as an unrestricted regex failure rule.**

Historical files legitimately contain those words. Unqualified semantic detection across all history would be false-positive prone. Instead authority metadata, explicit historical classification and the central known-bad registry are used; known concrete bad values fail closed.

## 4. Remaining risks after hardening

### NON-BLOCKING INTEGRITY ISSUE — HISTORICAL / IRREVERSIBLE

The exact individual Phase 3–10 completion checkpoint order of the already completed overhaul is not independently reconstructible. The final artifacts and dependency end state remain validated.

### OPTIONAL HARDENING

- `main` is not protected by required status checks.
- the standalone pre-overhaul backup repository is not GitHub-archived.

### Residual validator limitation

No finite validator can discover a future incorrect value that has never been registered and is not contradicted by another modeled authority. `Current/VALIDATOR_COVERAGE.json` makes these blindspots explicit; independent audit remains available for exceptional/frozen-contract revalidation.

## 5. Operational conclusion

After this hardening passes CI, the repository architecture is intended to be robust enough that a future normal project chat does **not** need to perform a manual full-repository audit before ordinary work.

Normal takeover remains:

`README / START_HERE -> Current/CURRENT_STATE.json + Current/00 -> Project Knowledge Map -> relevant canonical topic/evidence`

A full independent audit remains appropriate only for exceptional cases such as a newly discovered provenance contradiction, a major future repository migration, or an explicit request to re-audit historical compliance.

## Gameplay state preserved

- Accepted baseline: **S1.42AB — Interior Weight Normalization**
- Accepted profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Latest built artifact: **S1.42AC — BCMER EventType Equal Distribution**
- S1.42AC status: **FORMALLY REJECTED / NOT PROMOTED**
- Active candidate: **NONE**
- Runtime test outstanding: **NO**
- Successor armed: **NO**

No runtime upload command is applicable to this repository-only validation work.
