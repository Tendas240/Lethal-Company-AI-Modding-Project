# S1.42AI-DIAG1R1 Materialized Validation

- Status: **PASS_CANONICAL_DIAG1R1_MATERIALIZED_EQUIVALENCE**
- Canonical profile SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`
- Canonical diagnostic DLL SHA-256: `2d1b6e8a002eb55e0e6d935e36c0a619d1c875651b94afb9e748663af93c1de0`
- Green-gate rebuild DLL SHA-256: `557f4e44385570b898f302e2e984f34263cdff3d00f8db68d30dcb25556faf2a`
- Canonical build run: `34822019162` / commit `8329579d3481ab27db6407d2659ceb467eebd203`
- Post-build validation run: `34822644436` / artifact `10338433359`
- ZIP members: **337**
- 335 non-plugin/non-export members: byte-identical to the green .NET 8 gate materialization
- `export.r2x`: profileName-only difference
- Diagnostic DLL: byte hash differs between compilations, but class inventory, decompiled C# per class, and normalized IL per class are identical
- Metadata-derived Pikmin type: `LethalMin.Pikmin.PikminType`, same LethalMin assembly
- Known-bad hardcoded `LethalMin.PikminType` resolver: absent from both the source gate and canonical materialized DLL

This evidence qualifies the exact canonical R1 bytes for runtime testing. It does not constitute gameplay acceptance and does not waive the deferred full-normal S1.42AI gate.
