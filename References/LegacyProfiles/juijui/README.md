# juijui Legacy Profile Reference

**Status:** upload target prepared; binary `juijui.r2z` still needs to be uploaded by the user.

## Canonical upload path

Upload the original historical Gale/r2modman profile exactly as:

`References/LegacyProfiles/juijui/juijui.r2z`

Do not place this historical profile under `Profiles/`. `Profiles/` is reserved for current project gameplay/technical builds.

## Why this profile matters

The juijui profile is the historical Lethal Company mod profile from several years ago that originally defined the target feel/configuration for this project.

The project's long-term goal is to reproduce that historical mod constellation and gameplay/configuration **as closely as technically reasonable**, while still respecting:
- the current Lethal Company version;
- currently maintained/available mods;
- current mod APIs and dependencies;
- multiplayer/runtime compatibility;
- fixes and project decisions confirmed by newer runtime evidence.

Therefore juijui is a **reference target**, not an instruction to blindly restore obsolete versions or incompatible mods.

## How to use it

After `juijui.r2z` is uploaded:
1. preserve the original binary unchanged as historical primary evidence;
2. extract/index its readable `export.r2x`, configs and other useful text metadata through a repository-first workflow;
3. record its SHA-256;
4. compare relevant historic values against the current profile;
5. use those values where the old behavior is still desired and technically compatible.

Immediate known use:
- recover the exact historical Jetpack capacity/duration/config instead of guessing.

Other historic values may also be used to resolve future "match the old juijui profile" requests.

## Priority interaction with current engineering work

The current highest-priority technical defect remains the generic LethalMin enemy grab/bite + invincible-Pikmin invalid leader/follow state confirmed in S1.42C.

The existence or upload of juijui must **not** delay that compatibility fix. The profile is a reference source; the LethalMin state repair is an active V81 runtime issue.
