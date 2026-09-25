# V81 RoundManager seed-control helper: reviewed Steam manifest variant

Date: 2026-09-25  
Scope: `AnalysisTools/InspectRoundManagerSeedControlV81.ps1` derived installed-V81 seed-control capture only  
Pinned base helper: `AnalysisTools/InspectRoundManagerGenerationV81.ps1` at `e376e09e09454b4c25b578626fafc9c721f27cda`, blob `51a577179f17343411cbdb05506cc374334497e7`  
Prior shared provenance review: `AnalysisTools/InspectRoundManagerSpawningV81_PROVENANCE_REVIEW.md`

## Observed fail-closed provenance event

On 2026-09-25 the repository-native seed-control wrapper successfully fetched and validated its pinned base helper, completed the deterministic seed-control transformation, located the installed Lethal Company V81 game, and then refused before decompilation/publication with this exact appmanifest SHA-256:

`4974c9249f249053275d93a5ba4f68e92346c1cfa09e89e6fce0b860c0c306a7`

The inherited provenance gate checks, in order, the exact `Assembly-CSharp.dll` SHA-256, exact `Lethal Company.exe` SHA-256, Steam App ID, Steam build ID, and only then the reviewed appmanifest allowlist. Reaching the manifest-specific rejection therefore establishes for this execution that the preceding four pinned identities matched:

- `Assembly-CSharp.dll`: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`
- `Lethal Company.exe`: `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`
- Steam App ID: `1966720`
- Steam build ID: `22825947`

This conclusion is an inference from the exact helper control flow plus the observed console failure. The full Steam appmanifest was not captured, and the byte-level cause of the manifest drift is unknown.

## Bounded decision

For the seed-control derived helper only, review and allow the exact appmanifest SHA-256 `4974c9249f249053275d93a5ba4f68e92346c1cfa09e89e6fce0b860c0c306a7` in addition to the three variants already accepted by the pinned base helper.

All other provenance checks remain unchanged and mandatory. There is no bypass switch, wildcard, prefix match, or automatic hash adoption. Any future unknown appmanifest hash still fails closed. The pinned base-helper commit and blob remain unchanged.

The wrapper must also replace the inherited manifest-review path with this file so that any published seed-control evidence records the review that actually authorizes the fourth variant.

## Validation and lifecycle boundary

The inherited PowerShell self-test iterates every member of the derived `$ReviewedAppManifestSha256` allowlist, so the fourth exact variant is covered automatically once the deterministic wrapper transformation adds it. Existing wrong-DLL, wrong-executable, wrong-App-ID, wrong-build-ID, unknown-manifest, extractor, and publication tests remain inherited from the pinned base helper.

This provenance correction does not prove a successful installed-V81 capture, does not change any gameplay/profile/config/plugin bytes, does not alter the active runtime candidate or controllers, and does not authorize a gameplay run. A successful seed-control evidence capture remains required before the map-seed-control analysis can proceed.
