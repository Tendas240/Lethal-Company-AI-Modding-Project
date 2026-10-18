# DULL 1.8.8 — Provenance, rights and retention specification (V1)

**Status:** DRAFT PROPOSAL / SPECIFICATION_ONLY / NOT CANONICAL UNTIL SEPARATE REVIEWED-HEAD MERGE AND EXACT-MAIN CI  
**Scope:** Universal Interior Viability / Equal Availability; procedural treatment of potential static DULL 1.8.8 evidence only  
**Decision boundary:** NO EVIDENCE CAPTURE / NO ORIGINAL OR DERIVED ASSET DATA PUBLISHED / PUBLICATION_RIGHTS_NOT_CLEARED  
**Effect on gameplay:** NONE; no source, patch, profile, controller, build, runtime or acceptance transition.

## 1. Authority and limited purpose

This document proposes a future-safe **procedure**, not a DULL capture, repository evidence payload, ownership assertion, license clearance or asset attestation. It follows the project-wide execution policy in `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`, live machine authority in `Current/CURRENT_STATE.json`, routing in `Current/PROJECT_KNOWLEDGE_MAP.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/INTERIORS_AND_LLL.md`, Interior-first scope in `Current/412_S1.42AK_PHASE_C_INTERIOR_FIRST_COMPLETION_PRIORITY_DECISION.md` and the rights/storage separation in `Current/LEADFACTORY_MINIMAL_PROVENANCE_PERSISTENCE_V1.md`.

Any stage descriptions in historical records remain historical; the actual main branch and controllers must be freshly verified before a later transition. This document does not change current next-action pointers, source authorities, existing archived evidence, flow eligibility, diagnostic restrictions or runtime state.

## 2. Non-transferable source and evidence classes

An earlier conversation's upload, inspection report, name or local filesystem path cannot transfer its original bytes into another chat or the repository. At any future point of byte-specific use, independently distinguish:

- **CURRENTLY_READABLE_ORIGINAL:** exact artifact accessible in the presently authorized environment, with independently re-checked size and digest;
- **REPOSITORY_AUTHENTICATED_ORIGINAL:** exact original artifact accessible at a currently verified, legally permitted, pinned repository source;
- **HISTORICAL_CONVERSATION_FINDING:** a reported earlier inspection whose original bytes have not been independently re-opened in the current environment;
- **DERIVED_ONLY_REFERENCE:** schema, notes or digests without the underlying original bytes; and
- **PUBLISHER_IDENTITY_UNVERIFIED:** no independent byte-for-byte binding to an authenticated publisher source.

The latter three classes cannot be relabeled as verified originals merely by copying historical text or by passing documentation CI. Do not claim upstream signing, publisher identity, current loaded plugin identity or a fresh capture if the source is inaccessible. Request the precise original artifact from the user **only** when a separately authorized, material next task genuinely needs it and no authorized readable copy exists; repeated CDN attempts and substitution are not a workaround.

This **specification contains no package archive digests, member identities, extracted object identities, numerical pointers or capture output**. Naming a version defines the planned scope, not source authentication.

## 3. Future abstract evidence-schema contract — not a payload

A separately authorized later design may define a minimized, explicitly versioned, closed schema with categories for:

- source provenance and identity method (package version, acquisition authority, verified source digest and byte length);
- original-container provenance (verified internal member identity and digest);
- typed serialized-object identity (object class, serialized-file association and independently pinned identity);
- typed reference relationships (declaring field type, pointer namespace and target resolution);
- capture/validator provenance (reviewed code revision, parser version, verification stage and independent reviewer);
- rights and retention decision (license/permission review identifier, authorized audience and storage mode); and
- explicit proof tier, refusal codes and evidence limitations.

These are **field-category definitions only**, not present verified values or authorization to populate them. A future whitelist must enumerate permitted fields, types, lengths and relationships and reject unknown or dynamic fields, mismatched identities, lexical lookalikes and unresolved or ambiguous pointers. A matching string or object name is not evidence of a typed serialized reference. A parser's success message is not proof of independent publisher identity.

Any actual schema instance, test fixture derived from the source, path identifier, pointer edge, digest, offset, serialized matching content or raw object metadata is a **separate data-publication decision**. Such values must not be added to this specification later by a routine edit.

## 4. Rights, attribution and disclosure boundary

**Current publication verdict: `BLOCKED_RIGHTS` for concrete source-derived DULL data.** Access to a publicly distributed archive, an old user upload, a source checksum or an apparent asset name does not establish copyright, license, downstream redistribution or publication rights. Rights conclusions require a separately documented review of the exact prospective payload and its relevant owner/license, distribution terms, attribution conditions and destination.

Treat the following as different independently gated operations:

| Mode | Permitted now by this specification | Required later |
| --- | --- | --- |
| Procedure-only public Markdown | Define abstract validation and rights rules; no asset-derived observations | Separate PR-head review and separately approved integration |
| Ephemeral future capture | Not implemented or authorized | Exact-source access, independent byte/owner validation and separate capture authorization |
| Restricted retention | No storage created or approved | Documented lawful basis, named controlled destination, access controls, retention/revocation and separate implementation approval |
| Public minimized evidence | **BLOCKED** | Rights and attribution clearance for the exact content, independently validated provenance, express publication approval and storage-integrity safeguards |
| Original ZIP, UnityFS or raw serialized objects | **BLOCKED** | Separate explicit rights and publication determination; this contract grants none |

Do not publish originals or extracted values via commits, pull-request bodies, Actions artifacts, workflow logs, job summaries, caches, release attachments or external endpoints. A PR reviewing this **procedure alone** never grants permission to publish its future evidence payload. Preserve the external author's rights without implying that every abstract field name itself is prohibited.

## 5. Verification, storage and attestation gates

A future, separately approved evidence-preservation implementation must fail closed before writing unless all of the following are satisfied:

1. Specific authorization for source access, capture, payload content, storage mode and destination;
2. re-opened authentic original bytes with independently checked digest/length and exactly scoped target;
3. verified typed serialized references, exact object identity and deterministic schema whitelist;
4. separately reviewable owner/license rights basis for the intended actual content and distribution audience;
5. an independent validator that re-parses the **exact bytes intended for retention**, checks bounded canonical encoding, prohibited content, cross-field integrity and content size;
6. separate attestation of producer run, pinned code/head, acquisition mode, independent validator, retained-file digest and read-back integrity; and
7. atomic staging/commit, safe failure behavior, rollback/deletion mechanism, least-privilege storage and an approved retention period.

An attestation may not self-certify by copying its own success flag. Git object identifiers and source/package hashes serve different purposes; one does not substitute for the other. No automatic workflow dispatch, repository artifact publishing or runner upload is authorized here.

## 6. Fail-closed decision taxonomy

| Condition | Result |
| --- | --- |
| Source absent, not independently accessible or mismatched | `BLOCKED_SOURCE_IDENTITY` |
| Owner/target/type reference missing, ambiguous or only name-based | `BLOCKED_SERIALIZED_PROVENANCE` |
| Illegal or unexpected fields, excessive size or source-derived content outside explicit allowance | `BLOCKED_CONTENT_POLICY` |
| No independently checkable capture and storage attestation | `BLOCKED_ATTESTATION` |
| License, attribution or intended publication rights unproven | `BLOCKED_RIGHTS` |
| No safe designated storage or verifiable rollback | `BLOCKED_STORAGE` |

Any blocker leaves existing project evidence and controllers unchanged. CI-green documentation establishes only documentation/check validity, not a source identity pass or a license determination.

## 7. Static proof ceiling and gameplay safety

A future successfully authenticated **static serialized-reference** report, if separately rights-cleared and ingested, could establish only the exact serialized association actually verified. It cannot establish effective runtime registration or owner identity, the original live managed wrapper, Harmony ordering, server caller legitimacy, selector atomicity, floor generation, CullFactory materialization, entrance relationships, traversal, NavMesh safety, natural selection frequency, all-moon viability, acceptance or safe forcing.

No generation residual decreases because of this specification. Preserve all existing Interior-first owner-block, selector, diagnostic, configuration and safety guards, including separate Museum/CKDIAG1 refusals, parked selector methods and the unwaived passive selector-free BMDSFIX1 proof obligation. A new rights decision cannot waive a technical proof gate.

## 8. Independent future permissions and Draft exit

This document-only Draft may modify **only this Markdown file**. It is not permission for an original-byte acquisition, data capture, parser implementation, evidence JSON creation, workflow edit, CI dispatch, profile modification, build, release/publication, controller mutation, Gale import, runtime, acceptance, Draft removal or merge. Automatically triggered pull-request CI may be read and verified on the exact final PR head; the Draft must remain open.

Any later rights assessment, schema implementation, retention mechanism, acquisition, publication, evidence reconciliation, merge or gameplay proof requires its **own express scope** and fresh repository-authority verification. A previous-chat file remains **NOT TRANSFERRED**; this document does not manufacture a durable substitute for its original bytes or historical evidence.

**STOP / RE-ENTRY:** until a distinct rights basis and separately approved publication scope exist, concrete source-derived DULL evidence remains `BLOCKED_RIGHTS`. Until separate source-authentication and safety gates are satisfied, no static-to-runtime inference is permitted.
