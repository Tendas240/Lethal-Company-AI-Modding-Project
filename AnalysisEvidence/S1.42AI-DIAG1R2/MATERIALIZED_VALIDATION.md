# S1.42AI-DIAG1R2 materialized validation

- Status: **PASS_CANONICAL_DIAG1R2_MATERIALIZED_APPLICABILITY_EQUIVALENCE**
- Canonical profile SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`
- Canonical diagnostic DLL SHA-256: `099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3`
- Green-gate diagnostic DLL SHA-256: `17ea9bf752d999b8bbb5e48e8a6bdd9ac0dae5c9e516dfd2cd70ac6e4a9a6f64`
- Static gate: **PASS_PREBUILD_STATIC_GATE**
- Materialized EndlessElevator applicability: **PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY**
- Plugin decompiled C# identical for all 31 classes: **true**
- Plugin normalized IL identical for all 31 classes: **true**
- ZIP members: **337**
- All non-plugin members except `export.r2x`: byte-identical to the repaired SDK8 green-gate materialization
- `export.r2x`: profileName-only difference
- Metadata-derived PikminType: `LethalMin.Pikmin.PikminType`
- EndlessElevator dependency GUID: `kite.ZelevatorCode`
