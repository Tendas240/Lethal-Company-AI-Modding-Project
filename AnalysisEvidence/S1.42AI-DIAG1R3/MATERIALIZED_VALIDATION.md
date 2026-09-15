# S1.42AI-DIAG1R3 materialized validation

- Status: **PASS_CANONICAL_DIAG1R3_MATERIALIZED_IDENTITY_APPLICABILITY_EQUIVALENCE**
- Canonical profile SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`
- Canonical diagnostic DLL SHA-256: `98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a`
- Green-gate diagnostic DLL SHA-256: `8494f636b075b6f8d30b69469ece0cfe44e5a1bd6e59d0ca7abe12f4045a0272`
- Exact ShyGuy identity: `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` / `StringComparison.Ordinal`
- Static gate: **PASS_PREBUILD_STATIC_GATE**
- Materialized EndlessElevator applicability: **PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY**
- Plugin decompiled C# identical for all 31 classes: **true**
- Plugin normalized IL identical for all 31 classes: **true**
- ZIP members: **337**
- All non-plugin members except `export.r2x`: byte-identical to the repaired SDK8 green-gate materialization
- `export.r2x`: profileName-only difference
- Metadata-derived PikminType: `LethalMin.Pikmin.PikminType`
- EndlessElevator dependency GUID: `kite.ZelevatorCode`
