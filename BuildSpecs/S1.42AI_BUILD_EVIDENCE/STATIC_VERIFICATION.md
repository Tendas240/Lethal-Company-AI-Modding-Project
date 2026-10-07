# S1.42AI Static Build Verification

**Status:** BUILD PASS / STATIC DELTA VERIFIED / NOT YET RUNTIME CANDIDATE

- Output profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
- Output SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
- Parent: `S1.42AH`
- Changed existing archive members: exactly `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`
- Added archive members: none
- Package state/add/remove changes: none
- `ModdedEvents.cfg` semantic line delta: exactly three `[ShyGuy]` exterior values
- Every other archive member SHA-256 is byte-identical to S1.42AH, including `BepInEx/config/Scopophobia.cfg`.

No runtime test is authorized by this static verification alone.
