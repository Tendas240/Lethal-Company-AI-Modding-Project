# S1.42AJ Static Verification — LC Office V81 Integration

**Status:** PASS / STATIC VALIDATED / RUNTIME NOT ARMED  
**Date:** 2026-09-17  
**Parent:** S1.42AI  
**Build workflow:** `35222275686`  
**Build commit:** `7fbaae92523637ae3fec6c1e242ec2538918e7b7`

## Verified artifact

- Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`
- SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`
- Parent profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
- Parent SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
- Builder result changed exactly one existing ZIP member: `export.r2x`; no ZIP members were added.
- Independent FILE_INDEX comparison likewise proves `export.r2x` is the only member whose SHA changed.

## Exact package delta

- added/enabled `Piggy-LC_Office 2.3.4`;
- added/enabled `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`;
- added/enabled `JacobG5-DestroyItemInSlotFix 1.0.0`;
- transitioned `Alice-DungeonGenerationPlus 1.5.0 -> 1.5.1`;
- every other accepted S1.42AI package block is byte-identical in the Gale export.

This proves there was no unintended exported package-version/state/source cascade.

## Ownership and interior guards

- `IAmBatby-LethalLevelLoader 1.7.12` remains enabled and is the sole package whose name contains `LethalLevelLoader`;
- `pacoito-LethalLevelLoaderUpdated` is absent;
- `BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll` remains byte-identical at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- no config, DLL or other existing non-export profile member changed;
- no universal-moon availability, Wesley, CullFactory, DunGenReferenceFixer or unrelated deferred Interior scope was introduced.

## Decision

Static acceptance gate: **PASS**. S1.42AJ is a built/static-validated successor only. It is not accepted gameplay, is not an active runtime candidate yet, `RuntimeInbox/ACTIVE_BUILD.txt` remains S1.42AI, and no runtime test is armed by this decision.
