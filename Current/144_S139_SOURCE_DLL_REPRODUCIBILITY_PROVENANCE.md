# 144 — S139 Compatibility Fixes Source-to-DLL Reproducibility Provenance

**Status:** CURRENT / CANONICAL PROVENANCE CLOSURE  
**Scope:** `Patches/S139CompatibilityFixes` source-to-runtime-DLL reproducibility  
**Lifecycle effect:** NONE — this record does not accept/reject a gameplay build, activate a BuildSpec, change runtime attribution, build S1.42AI-DIAG1, or request gameplay validation  
**Date:** 2026-09-13

## Provenance question

The accepted S1.42AH compatibility binary, inherited unchanged by S1.42AI, is:

- archive member: `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
- runtime DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`

A repository-native rebuild using the current .NET host patch produced `912e097ae61d3af394f0132115327478b714ee83a4b5b73bbacba7c86dff8de7` even though the managed IL was identical. The provenance review therefore had to identify the remaining deterministic build-environment input before S139 source-to-DLL reproducibility could be considered closed.

## Exact reproducible build contract

The historical binary is byte-reproducible when the historical build context uses all of the following:

- historical pre-build commit: `af415c8d6fdb69b0b7c88102e714764f3dc24b57`
- historical branch/tracking context: `build/s142ah-mouthdog-dual-prevention`
- Actions workspace: `/home/runner/work/Lethal-Company-AI-Modding-Project/Lethal-Company-AI-Modding-Project`
- no repository `global.json`
- .NET SDK: `10.0.400`
- .NET Host / `Microsoft.NETCore.App`: `10.0.11`

The .NET host patch level is part of the exact deterministic binary provenance. SDK `10.0.400` under Host `10.0.12` preserves the compiled C#/managed IL but does **not** reproduce the accepted DLL/PDB deterministic identities; it reproducibly yields DLL SHA-256 `912e097ae61d3af394f0132115327478b714ee83a4b5b73bbacba7c86dff8de7` instead.

## Final decisive reproduction

Analysis source branch: `analysis/s142ai-s139-source-dll-rebuild-exact`  
Analysis head: `a48b03297210b57b005df16340319bc560b252a5`  
Workflow: `S1.42AI S139 Historical .NET Host 10.0.11 Review`  
Run: `34742936157` / run number `12` / event `push` / conclusion `SUCCESS`  
Artifact: `10313352329` — `s142ai-s139-historical-dotnet-host-10-0-11`  
Artifact digest: `sha256:4add3d1d945333f8bb9b3d37260cdd87e61654387cb2facb7cdc457255fe98e6`

The decisive result is exact:

- selected SDK: `10.0.400`
- selected Host / Runtime: `10.0.11`
- runtime SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- rebuilt SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- byte-identical: `true`
- differing byte count: `0`
- differing ranges: `[]`
- managed IL identical: `true`
- MVID: `1399bed4-4f26-4202-8a52-3c910a189735`
- CodeView GUID: `4b36fb9e-c283-4359-a3eb-c448c54db44d`
- PDB SHA-256 checksum: `9efb364b83c25913e3ebc448c54db44d8b71302ec7ba01deb6a8ab2afdb72ed2`
- reproducible PE timestamp/hash field: `d838dcb8`

The technical source-to-DLL reproducibility gate for this accepted S139 binary is therefore **CLOSED / PASS**.

## Supporting exclusion evidence

The preceding analysis runs are retained as historical investigation evidence; their workflow failures mean that the then-tested hypothesis did not eliminate the byte mismatch, not that the evidence was invalid.

- Run `34742150808` recreated the historical workspace, branch/upstream context, no-`global.json` selection, SourceLink/generated context and SDK `10.0.400`. Runtime and rebuild C#/IL were identical, but Host `10.0.12` still produced `912e097a...` rather than `bf86f338...`.
- Run `34742488509` captured the actual Roslyn input set: `275` compiler references plus the SDK/compiler inventory while the same byte mismatch remained.
- Run `34742717937` erased the global NuGet package cache and performed a forced no-cache restore. Warm and clean builds were byte-identical to each other at `912e097a...`; both had `275` compiler references, with `0` changed references and `0` changed package-provenance entries, and both retained IL identity with the accepted runtime DLL.

Accordingly, workspace path, Git branch/tracking context, SourceLink/generated inputs and NuGet/reference-byte provenance were eliminated as the remaining cause. The final controlled change from Host `10.0.12` to `10.0.11` restored the historical binary and deterministic identities exactly.

## Permanent rule

When exact reproduction of this historical/accepted S139 binary is required, use **SDK `10.0.400` + .NET Host/Runtime `10.0.11`** and preserve the historical deterministic context above. Do not treat SDK pinning alone as sufficient.

A rebuild under a newer host patch may be semantically/IL-equivalent while still being a different deterministic binary. Such a rebuild must not be substituted for the accepted DLL when byte identity is the gate.

The temporary analysis workflow and analysis tool are investigation infrastructure only. They are deliberately **not** promoted to permanent `main` infrastructure by this closure; their branch/history remains provenance evidence.

## Lifecycle non-transition

This provenance closure does not change the canonical gameplay lifecycle. Resolve accepted baseline, active candidate, pending runtime state and next project action only from `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md`.

In particular, this record does not modify `BuildSpecs/current.json` or `RuntimeInbox/ACTIVE_BUILD.txt` and does not authorize an S1.42AI-DIAG1 build or another gameplay run.
