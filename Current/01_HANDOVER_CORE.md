# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Latest explicit handover:** `Current/114_FINAL_HANDOVER_POST_INTEGRITY_REMEDIATION.md`  
**Last-Validated:** 2026-09-04

## Fresh-session procedure

1. Read `Current/00_CURRENT_STATE.md`.
2. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
3. Route the user's question to the registered semantic topic.
4. Read `Current/114_FINAL_HANDOVER_POST_INTEGRITY_REMEDIATION.md` once for the latest explicit transfer checkpoint.
5. Open linked config/code/runtime/history only when needed.
6. Use `Current/BUILD_LINEAGE.md` for build-history questions and `Current/DOCUMENT_AUTHORITY.md` when an older file says "current".

Do not require a local repository clone or local profile build while repository-native artifacts and automation are sufficient.

## Current anchors

Accepted: **S1.42AB — Interior Weight Normalization**, SHA-256 `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`.  
Latest built: **S1.42AC — BCMER EventType Equal Distribution**, SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`, formally rejected/not promoted.  
Active candidate: **none**. Runtime test: **none pending**. Successor: **not armed**.

Exact next action: If BCMER EventType work continues, reevaluate the existing S1.42AC artifact/evidence with the corrected static EventType acceptance model from Current/109. Do not build a compensation successor and do not require equal per-event log weights.

## Post-overhaul integrity correction

`Current/113_POST_OVERHAUL_INTEGRITY_REMEDIATION.md` records the latest follow-up audit and its green CI validation.

Two concrete residual inconsistencies were corrected:

- `Knowledge/CURRENT_LIFECYCLE.md` no longer incorrectly calls the completed repository overhaul the active maintenance scope;
- S1.42AC raw-runtime-log byte provenance is now consistently authoritative at SHA-256 `fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`, sourced from `RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json`; the previously recorded `862603...` value is explicitly superseded historical metadata.

The permanent Knowledge Architecture validator now fails CI on this class of runtime-SHA provenance mismatch.

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the exact build-specific one-line PowerShell log uploader in the same response.

Whenever the user must perform another manual repository action, provide the exact PowerShell one-liner(s) in execution order.

## Historical authority warning

Old final handovers, audits, candidate notes, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the new current-state/topic graph. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`

The backup is semantically historical/read-only and verified. GitHub repository archival is optional additional hardening, not an overhaul acceptance requirement.
