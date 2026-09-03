# 18 — juijui Historical Reference Profile

**Date added:** 2026-09-03

## Role in the project

The original `juijui.r2z` profile is a historically important primary reference for this project.

The project was originally intended to bring modern Lethal Company modding as close as reasonably possible to the old juijui mod constellation/configuration, while adapting it to:
- the current game version;
- currently available and maintained mods;
- current dependencies/APIs;
- modern compatibility constraints;
- newer runtime-confirmed project decisions.

This means juijui is a **historical behavioral/configuration target**, not a current gameplay build and not a license to restore obsolete or incompatible packages blindly.

## Canonical repository location

Expected binary:

`References/LegacyProfiles/juijui/juijui.r2z`

Reference documentation:

`References/LegacyProfiles/juijui/README.md`

Existing manually retained historic values:

`References/juijui_Referenzwerte.txt`

The binary is still pending user upload as of this document.

## Handling after upload

Preserve `juijui.r2z` unchanged as primary evidence.

Repository-first follow-up should:
- calculate and document SHA-256;
- extract/index readable profile metadata/configs;
- identify exact historical mod versions and settings;
- compare relevant values with current V81 equivalents;
- never treat old package versions as automatically safe/current.

## Immediate Jetpack use

The current Jetpack question must be resolved from the uploaded juijui profile instead of guessing.

Current project state:
- ButteryBalance `Reduce Battery = true`
- current resulting capacity/duration: 40 seconds

Once juijui is uploaded, inspect its Jetpack-related mod/config values and use the actual historical value as the requested target where technically compatible.

The previously mentioned 50-second value remains only a fallback hypothesis and must not be substituted for the historical value once primary evidence is available.

## Current engineering priority remains unchanged

The generic LethalMin issue confirmed in S1.42C remains the first active compatibility problem to solve:

enemy grab/bite -> leader removal -> grabbed/death state -> invincibility blocks death -> Pikmin remains in an invalid leader-less follow state -> repeated `Leader is null when following`.

This affects enemy interactions beyond the specific Thumper/Puffer requirements and should be fixed generically without blacklisting all enemies.

Specific requirements remain:
- Thumper/Crawler <-> Pikmin: total noninteraction;
- Puffer attack/smoke -> Pikmin: no effect.
