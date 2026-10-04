# Runtime Ingest Exact-Head and Uploader Hardening

**Date:** 2026-10-04  
**Status:** HANDOVER-CRITICAL INFRASTRUCTURE HARDENING  
**Scope:** runtime-log uploader first-create behavior and bot-generated runtime-ingest exact-head CI only  
**Gameplay/profile impact:** none

## Trigger

The first S1.42AK-BMAFR1I1 runtime-log upload used the build-specific command in `Current/238_S1.42AK_BMAFR1I1_RUNTIME_ACTIVATION.md`. The local log and both required diagnostic markers were valid, but the command queried `RuntimeInbox/Current/LogOutput.log` before upload. Because that destination did not yet exist, GitHub correctly returned HTTP 404; on the user's PowerShell/native-command error behavior, that expected create-case 404 aborted the one-liner before the PUT.

A create-only retry then uploaded the exact log successfully. Runtime ingest committed the evidence as bot commit `d0e7aaae059ffd87099d3b79b707d91bfa121fb5`.

That bot commit exposed a second handover-critical gap: `.github/workflows/runtime-ingest.yml` pushed the generated evidence with `GITHUB_TOKEN` but did not explicitly dispatch Knowledge Architecture for the resulting exact head. GitHub therefore registered no permanent exact-head Knowledge Architecture run for `d0e7aaa...`.

## Hardening contract

The repository now applies the same fail-closed bot-follow-up pattern already proven by `.github/workflows/profile-index.yml`:

1. runtime ingest records whether it created an evidence commit and captures its exact SHA;
2. after push, it verifies remote `main` still equals that exact SHA;
3. it explicitly dispatches `knowledge-architecture.yml` for `main`;
4. it verifies that a `workflow_dispatch` Knowledge Architecture run is registered with `head_sha` equal to the generated evidence commit;
5. handover validation requires this runtime-ingest exact-head wiring so it cannot silently regress.

The build-specific BMAFR1I1 uploader is also corrected so a missing destination is treated as the normal create case rather than an upload failure. Future uploader guidance must preserve the create-or-replace contract from `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.

## Boundaries

This hardening changes no gameplay/config/profile/package/DLL bytes and no acceptance decision. It does not reinterpret runtime evidence. It only makes runtime evidence submission and exact-head repository validation reliable.

The historical failed first upload attempt remains a transport/tooling failure only; the successfully ingested BMAFR1I1 log and its SHA-256 remain the runtime evidence authority.
