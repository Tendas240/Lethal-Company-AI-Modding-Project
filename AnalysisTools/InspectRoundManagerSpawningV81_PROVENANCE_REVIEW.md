# V81 RoundManager helper: reviewed Steam manifest variant

Date: 2026-09-11
Scope: `AnalysisTools/InspectRoundManagerSpawningV81.ps1` only
Prior authority: `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`
Repository main inspected: `18602af6ea97c7f19a5fbd969891e75c5ffe7a7e`

## Observed failure and follow-up

The user supplied console screenshots of the canonical helper failing at its exact
Steam appmanifest SHA gate, followed by the requested read-only Steam-library
identity check. The follow-up reports:

- App ID: `1966720`
- Steam build ID: `22825947`
- Actual appmanifest SHA-256:
  `b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3`

The prior evidence records this different appmanifest SHA-256:
`fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432`.

Screenshot provenance: user attachments
`74e6ed5e-526a-41d0-b6b2-b7893e6c446d.png` (original helper failure) and
`428b23bb-cc66-4d75-8ec3-c672f4a04256.png` (follow-up identity output).
These names identify the conversation attachments; they are not repository file paths.
This record transcribes the relevant values; the full appmanifest was not captured.

At the inspected helper revision, the Assembly-CSharp and executable SHA checks
precede the failing manifest check. Reaching that failure therefore supports that
both binary checks passed in that execution. This is an inference from the exact
control flow plus the user console evidence, not a new repository-hosted binary
capture. The follow-up separately reports the expected app/build identity.

Unchanged pinned binaries:

- Assembly-CSharp.dll:
  `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`
- Lethal Company.exe:
  `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`

## Bounded decision

Allow the two explicitly listed appmanifest hashes for this helper, only together
with the exact binary hashes, App ID and build ID above. Retain the prior manifest
unchanged. Every future execution rechecks all five values before authentication,
decompilation or upload. Missing or duplicate app/build fields are rejected.

The precise changed appmanifest fields and the reason they changed are unknown.
This review does not label the whole manifest byte-identical or claim a specific
Steam metadata update caused the difference. No unknown manifest is allowed, and
there is no bypass switch or automatic hash adoption.

The uploaded capture manifest records the actual appmanifest hash, original
reference hash, whether they match, and this review path. The prior repository
manifest is also checked against its original app ID/build/binary/manifest pins.

## Validation and lifecycle boundary

The existing Windows PowerShell 5.1 Actions self-test now exercises acceptance of
both exact manifest variants and rejection of unknown manifest hashes, wrong DLL,
wrong executable, wrong app ID and wrong build ID. It also rejects absent or
duplicate app/build fields. Existing extraction/publication tests remain in place.

CI is separate from installed-game evidence. This correction does not prove a
successful source capture, change a profile, build S1.42AI-DIAG1, update controllers,
or make any gameplay acceptance decision.
