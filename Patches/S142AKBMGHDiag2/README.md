# S142AKBMGHDiag2

Diagnostic-only Black Mesa x Greenhouse qualification plugin derived from exact accepted S1.42AK.

BMGHDIAG2 repairs only the predecessor startup-provenance defect: installed V81 `Assembly-CSharp.dll` provenance is hashed from BepInEx `Paths.ManagedPath`, while the loaded `EntranceTeleport` target is validated separately by exact structural reflection identity.

Gameplay scope remains exactly two postfixes: one post-normalizer LLL selection singleton for the already-viable Greenhouse wrapper on Black Mesa, and one read-only `EntranceTeleport.TeleportPlayer()` observer.

This project is not an accepted gameplay baseline and must not be runtime-armed merely because source/static CI passes.
