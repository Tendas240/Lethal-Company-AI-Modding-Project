# 113 — Post-Overhaul Integrity Remediation

**Date:** 2026-09-04  
**Status:** PASS / CI VERIFIED  
**Scope:** post-overhaul information-integrity hardening only; no gameplay/config/mod/profile/runtime behavior change  
**Authority:** follow-up audit record after the post-overhaul handover review

## Why this follow-up exists

A fresh independent review of the completed repository overhaul identified two concrete repository-truth inconsistencies and two optional hardening opportunities. The two concrete inconsistencies were corrected together, and the permanent Knowledge Architecture validator was extended so the runtime-SHA class of error becomes CI-blocking in future.

## Finding 1 — stale current lifecycle wording

`Knowledge/CURRENT_LIFECYCLE.md` still said that the repository overhaul was the active maintenance scope even though the overhaul had already completed and passed the frozen-contract post-acceptance re-audit.

That statement contradicted the current roadmap and repository-overhaul topics and was especially risky because `Knowledge/CURRENT_LIFECYCLE.md` is canonical for "what is next?" questions.

### Remediation

The lifecycle topic now states explicitly:

- repository information-architecture overhaul is complete;
- it is no longer the active maintenance scope;
- there is no active gameplay candidate/runtime gate;
- no successor is implied automatically;
- if gameplay work resumes, either reconsider existing S1.42AC under `Current/109` or explicitly select another deferred scope.

## Finding 2 — S1.42AC raw-log SHA-256 provenance contradiction

The authoritative runtime index:

`RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json`

records the 2,000,261-byte raw `LogOutput.log` SHA-256 as:

`fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`

Its embedded analysis `source_sha256` agrees with the same value. `Current/ARTIFACT_EVIDENCE_INTEGRITY.md/.json` also already used this authoritative hash.

However, the older `Current/Projektstatus_S1.42AC_REJECTED.json` and `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` had still recorded:

`8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

### Provenance decision

The RuntimeEvidence `INDEX.json` is definitive byte provenance for the ingested raw runtime log. Therefore:

- authoritative raw-log SHA-256 = `fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`;
- `862603...` is retained only as the superseded historically recorded value;
- the S1.42AC project-status record carries an explicit machine-readable provenance/supersession object;
- the historical rejection record has a conspicuous provenance erratum and uses the authoritative hash in its Runtime Evidence section;
- this byte-provenance correction does **not** change S1.42AC's formal rejected/not-promoted status and does not change the later BCMER interpretation in `Current/109`.

## Validator hardening

`RepositoryTools/knowledge_architecture_validator.py` now validates runtime-log SHA provenance across:

1. `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`;
2. the referenced `RuntimeEvidence/.../INDEX.json` file entry;
3. embedded runtime-analysis `source_sha256` metadata;
4. S1.42AB/S1.42AC project-status raw-log SHA declarations;
5. the explicit S1.42AC provenance authority/supersession object;
6. the S1.42AC rejection-record provenance erratum.

A future mismatch in this chain is therefore intended to fail the permanent Knowledge Architecture CI.

## Optional hardening review

### Standalone pre-overhaul backup repository

The backup repository is semantically marked historical/read-only but GitHub metadata currently reports `archived: false`.

Archiving it is recommended as an additional safeguard against accidental mutation, but it is **not** required to establish the already-verified backup equivalence or the overhaul PASS. This chat's GitHub connector does not expose repository-archive mutation, so this remains an optional manual GitHub administration action unless the user chooses to perform it.

### `main` branch protection

GitHub currently reports `main` as unprotected. This is a genuine optional hardening opportunity, but it is deliberately **not enabled by this remediation** because the established repository-native workflow currently performs direct authenticated writes to `main`. Turning the Knowledge Architecture job into a required pre-merge check should be done together with a deliberate switch to PR-based authoring/bypass policy so it does not unexpectedly break the working automation path.

This is not an overhaul acceptance failure; it is repository-governance hardening for a future workflow change.

## Gameplay/controller state unchanged

- accepted baseline: S1.42AB — Interior Weight Normalization;
- accepted profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- latest built artifact: S1.42AC — formally rejected/not promoted;
- active candidate: none;
- runtime test outstanding: no;
- successor armed: no;
- `BuildSpecs/current.json`: disabled;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`.

## Validation result — PASS

Remediation commit:

`0d1a06e226ddbe0e37e94a79b72fb3d14bf6d8dd`

Permanent `Knowledge Architecture` workflow run:

`33922283909`

Result: **SUCCESS**.

The run passed all permanent gates:

1. generated current navigation — PASS;
2. knowledge/state/reference validation — PASS, including the new runtime-SHA provenance checks;
3. frozen original-overhaul-contract validation — PASS;
4. answerability routing regression — PASS.

A fresh final handover may therefore be generated from this corrected and validated state.
