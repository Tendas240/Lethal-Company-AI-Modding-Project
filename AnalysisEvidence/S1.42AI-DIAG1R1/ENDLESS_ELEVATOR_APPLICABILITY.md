# S1.42AI-DIAG1R1 EndlessElevator applicability proof

**Status:** PROVEN OPTIONAL-COMPAT APPLICABILITY CONTRACT / REPAIR INPUT

Exact LethalMinNightly `1.1.108` evidence binds `LethalMin.Compats.EndlessElevatorPatch` to `[CompatClass("kite.ZelevatorCode")]`. LethalMin activates CompatClass owners only when `IsDependencyLoaded(modGUID)` is true, and that method is exactly `Chainloader.PluginInfos.ContainsKey(pluginGUID)`.

The same owner IL binds `WaitRespawnPikmin` to CLR TypeRef `[kite.ZelevatorCode]ElevatorMod.Patches.EndlessElevator`. R1 runtime evidence then proves that `kite.ZelevatorCode, Version=1.0.0.0` was absent: LethalMin logged that `WaitRespawnPikmin` was skipped for the missing dependency and continued loading normally.

Therefore, for the exact unchanged S1.42AI package set, this target is `NOT_APPLICABLE_DEPENDENCY_ABSENT`. If the exact BepInEx GUID `kite.ZelevatorCode` is present, the target becomes REQUIRED and provider assembly, CLR type, exact owner signature and patch installation must all validate fail-closed. There is no generic `missing target => ignore` rule.

The concrete Thunderstore package name that supplies `kite.ZelevatorCode` is not proven by current repository evidence and is deliberately not guessed.
