# 16 — Handover S1.42C -> next chat

**Handover date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## 1. Canonical vs latest tested

### Last fully accepted gameplay baseline

**S1.41 — accepted**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Do not silently replace this historical acceptance statement with S1.42A/B/C. Those are staged descendants, not yet final gameplay acceptance.

### Latest runtime-tested technical candidate

**S1.42C — runtime-tested regression candidate**

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Manifest:
- 188 Thunderstore entries
- 183 enabled
- 5 disabled
- cumulative local compatibility plugin embedded

S1.42C may remain the technical base for descendants because no new startup regression attributable to it was found and the S1.42B LethalModDataLib fix remained healthy.

## 2. Required read order for the next chat

After `START_HERE_ChatGPT_Masterprompt.txt` and root `README.md`, read:

1. `Current/00_CURRENT_STATE.md`
2. `Current/01_HANDOVER_CORE.md`
3. `Current/16_HANDOVER_S1.42C_TO_NEXT.md`
4. `Current/17_REPO_HANDOVER_CLEANUP_S1.42C.md`
5. `Current/06_RECENT_WORK_S1.42A-S1.42C.md`
6. `Current/15_RUNTIME_EVIDENCE_S1.42C.md`
7. `Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md`
8. `Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `Current/02_TECHNICAL_BASELINE.md`
11. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
12. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
13. `BuildSpecs/S1.42C_PLAN.md`
14. `BuildSpecs/S1.42D_PLAN.md`
15. `BuildSpecs/current.json`
16. `Current/Projektstatus_S1.42C.json`
17. `Current/Aktive_Modliste_S1.42C.txt`
18. `ProfileSources/S1.42C/`

## 3. Repository-first workflow is binding

Do not ask the user for:
- a local Git clone;
- local PowerShell profile builds;
- manual r2z unpack/repack;
- manual DLL copying into the repo.

When a build is needed:
1. use a repository profile under `Profiles/`;
2. update `BuildSpecs/current.json`;
3. let `.github/workflows/profile-build.yml` build and compile local plugins;
4. verify `Current/AUTO_BUILD_RESULT.json/.md`;
5. compare `ProfileSources/<build_id>/FILE_INDEX.json`;
6. return `BuildSpecs/current.json` to an idle state.

The user only needs local action for actual Lethal Company runtime testing and upload of runtime-generated evidence.

Any profile carrying the local DLL must be imported with Gale:
**Advanced options -> Import all files**

Expected general marker:
`S1.39 Compatibility Fixes loaded.`

## 4. S1.42A — interior seed result

Profile:
`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:
`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Added:
- Beaniebe-Liminal_House 1.1.6
- MelanieMelicious-Melanie_Interiors_MelanieMelicious 1.2.1
- Beaniebe-Deepcore_Mines 1.0.9
- MrKixcat-Junkrooms 4.0.2
- Beaniebe-Super_Market 1.0.3
- MrKixcat-Shatteredrooms 2.1.6
- BLB_Thunderstore_Mods_LOL-Lead_Interiors 0.0.7
- DemonMae-Dungeons_Ultimately_Lacking_Liveliness 1.8.8
- MaxWasUnavailable-LethalModDataLib 1.2.2

Boom_Scraps was intentionally not added.

Runtime evidence:
`RuntimeEvidence/S1.42A/20260902T224318Z/`

Seed outcome:
- 52 ExtendedDungeonFlows registered vs 26 in S1.41;
- exactly 26 new flows discovered;
- Mausoleum generated successfully on Offense;
- real generated LLL/JLL configs/weights now exist;
- exact CullFactory flow IDs confirmed:
  - `junkrooms`
  - `shatteredrooms`

Generated interior weights are not normalized yet.

## 5. Binding interior architecture

Permanent user rule:

**Every registered interior should have the same effective selection probability as every other registered interior on every moon, including all future interiors.**

Project implementation target:
- common Weight 100 per interior/moon pairing where technically supported;
- new interior packages must be normalized into this architecture before final acceptance;
- a pack containing multiple interiors contributes multiple equal-probability interiors;
- no theme/default rarity preference should override this design.

Hard author restrictions are technical compatibility questions, not desired balancing exceptions.

Example:
- Shatteredrooms currently hard-excludes Experimentation and Embrion.
- Do not blindly override until the technical reason/safety is understood.
- Desired final state remains equal availability everywhere if safely achievable.

## 6. Mausoleum visual requirement

Observed S1.42A:
- `MelanieMausoleum` was far too foggy;
- visibility was poor enough to impair gameplay.

Requirement:
- reduce fog specifically inside Mausoleum;
- do not globally reduce fog in all interiors;
- preserve some atmosphere if practical, but visibility has priority.

Generated Melanie config exposes no obvious fog-density key. Likely needs an interior-specific runtime/HDRP-volume compatibility approach.

## 7. BCMER binding configuration direction

BCMER remains exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not silently upgrade to 2.0.0.

Existing ownership guards remain binding:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

BCMER event rain routes remain disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy weather remains allowed.

### New fixed EventType rule

User wants every BCMER EventType globally equally likely, independent of moon, days passed, or difficulty.

Keep:
`Use custom weights? = false`

Set all eight EventType scales to:
`12.5, 0, 12.5, 12.5`

for:
- Insane
- VeryBad
- Bad
- Neutral
- Good
- VeryGood
- Rare
- Remove

This creates an equal 12.5% base EventType distribution. Event-specific eligibility/exclusions may still alter the effective pool in an individual run.

This is pending application in a later tuning build.

## 8. S1.42A LethalModDataLib NRE -> S1.42B fix

S1.42A exposed:

`NullReferenceException`

in:
`LethalModDataLib.Features.ModDataAttributeCollector.RegisterModDataAttributes()`

Root cause:
LethalModDataLib 1.2.2 dereferenced `PluginInfo.Instance` without a null check.

Project compatibility plugin v1.1.0 added a null-safe bulk scanner.

S1.42B runtime evidence:
`RuntimeEvidence/S1.42B/20260902T231959Z/`

Confirmed offending entry:
`MW.MagicWesleyInteriors` had `PluginInfo.Instance == null`.

Runtime success:
- guard skipped exactly that null entry;
- scanned valid plugin types;
- LMDL continued to `Hooking up save, load and delete events...`;
- `ModDataHandler initialised!`;
- moddata load/save succeeded.

**The LethalModDataLib initialization NRE is resolved.**

Keep this guard while LethalModDataLib 1.2.2 remains installed.

## 9. S1.42C Pikmin enemy guards

Build:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

Build delta vs S1.42B was exactly:
- `BepInEx/config/NoteBoxz.LethalMin.cfg`
- local compatibility DLL
- `export.r2x`

No other archive changes.

### Thumper / Crawler

User requirement:
**Thumper and Pikmin must not interact in either direction.**

S1.42C:
- `Thumper Bite Limit = 0`
- `Crawler` added to LethalMin Attack Blacklist

Runtime:
- a Crawler spawned and later died;
- no explicit Thumper-Pikmin grab/bite was logged;
- there was no deliberate controlled encounter.

Status:
**retained but not fully runtime-validated.**

### Puffer

User requirement:
**Puffer attack/smoke must not affect Pikmin.**

Existing config already had:
`Puffer Can Poison Pikmin = false`

Yet S1.42B showed:
`Injected effect trigger to Puffer's Smoke prefab`

Compatibility plugin v1.2.0 therefore adds a targeted `PufferAI.Start` postfix intended to remove LethalMin-owned Pikmin effect-trigger components from Puffer smoke only.

S1.42C runtime:
- patch registration marker appeared;
- no Puffer spawned;
- actual smoke immunity remains unvalidated.

Do not claim this guard accepted until a Puffer actually spawns and the user observes Pikmin in/near smoke.

## 10. New broader Pikmin state bug discovered in S1.42C

This is important and should guide the next engineering work.

A Baboon Hawk explicitly bit a Bulbmin:

`BaboonBirdPikminEnemy.BitePikmin: ... is being bitten ...`

Then:
- leader removed;
- LethalMin entered `Grabbed by enemy` state;
- grab-death timer started;
- `Invinceable Pikmin = true` prevented final death;
- follower remained in a broken leader-less follow state;
- repeated `Leader is null when following` errors followed.

Conclusion:
the leader-null spam is **not Thumper-specific**. It is a generic interaction between LethalMin enemy grab/bite logic and invincible Pikmin.

Preferred next compatibility direction:
- fix/reset the generic grabbed/follow state when invincibility prevents death;
- preserve intended enemy interactions;
- do not blindly blacklist every enemy.

Specific user-requested immunity remains separate:
- Thumper <-> Pikmin: total noninteraction;
- Puffer attack/smoke -> Pikmin: no effect.

## 11. Other pending gameplay tuning

### Functional Microwave volume

Current generated CodeRebirth values:
- `Functional Microwave | Allow Editing Config = false`
- `Functional Microwave | Volume = 1`

User wants it somewhat quieter.

Planned target:
- `Allow Editing Config = true`
- `Volume = 0.7`

This should be a config-only change first. Respect the S1.40B lesson: editing gate must be enabled or runtime regeneration may restore defaults.

### Jetpack capacity

User wants the old juijui-profile Jetpack duration/capacity.

Current:
- ButteryBalance `Reduce Battery = true`
- reduces 50s to 40s.

Exact historical juijui value is not present in retained text references.

Do not guess.

Fallback only if historical evidence cannot be recovered and the user accepts it:
- `Reduce Battery = false`
- current vanilla 50 seconds.

### Draft S1.42D

`BuildSpecs/S1.42D_PLAN.md` exists but is **DRAFT ONLY — DO NOT BUILD YET**.

Before enabling it decide whether the next candidate is:
- a small generic Pikmin-state + Jetpack/Microwave regression build;
- or the broader S1.42 tuning candidate including BCMER/interiors/CullFactory/Mausoleum.

Do not build S1.42D merely because the file exists.

## 12. Remaining planned S1.42 interior tuning

Still pending:
- normalize all safely available interiors to equal effective selection probability;
- use exact generated IDs;
- add CullFactory exceptions:
  - `junkrooms`
  - `shatteredrooms`
- investigate whether Shatteredrooms Experimentation/Embrion restrictions can safely be lifted;
- reduce Mausoleum fog;
- apply BCMER 12.5% x8 fixed EventType distribution;
- runtime-test the final tuned build.

## 13. Known carry-forward decisions

- Malfunctions disabled until explicit request.
- SCP999 disabled.
- Observer disabled.
- Don't Touch Me disabled.
- AJB ship-door mod disabled while local failsafe is active.
- CodeRebirthLib must not return.
- LethalModDataLib is allowed because DULL requires it; keep the confirmed null-instance guard.
- Leaf Boy stays in LethalMin Attack Blacklist.
- Unknown Enemy PowerLevels must never be guessed.
- S1.29D is diagnostic only, never gameplay base.
- Ogopogo disabled.
- Vermin disabled.
- local CodeRebirth Autonomous Crane Pikmin kill shield remains required.
- CodeRebirth natural Currency/Flash-Turret suppression from S1.40B remains required.

## 14. Monitor-only / unresolved validation

- Mineshaft elevator + many Pikmin: one floor-clipping/fall-death incident; NavMesh warnings nearby; causality unproven.
- Outdoor Pikmin Sprout density: subjective concern only; do not rebalance without evidence.
- GeneralImprovements recharge station full-heal behavior still needs direct runtime validation.
- Lethal Resonance Old Bird replacement still needs actual encounter validation.
- Mirage desired retained config should continue to be monitored.
- SoundAPI floor-reporting TypeLoadException predates S1.42 and is not a new regression.
- duplicate NetworkPrefab warnings from expanded content should only escalate with actual gameplay/network symptoms.
- scene-teardown Collection-modified exception in S1.42C should be tracked if it becomes reproducible/user-facing.

## 15. Binding next step for the new chat

Start from the repository and **do not rebuild S1.42C**.

First engineering priority:
1. inspect `Current/15_RUNTIME_EVIDENCE_S1.42C.md` and the full S1.42C log;
2. design a generic LethalMin enemy-grab/bite + Invincible-Pikmin state repair that prevents the leader-null loop without disabling all enemy interactions;
3. preserve the specific Thumper/Puffer guards;
4. decide the scope of the next candidate before enabling S1.42D.

Then continue the broader pending S1.42 tuning in controlled stages.

Repository-first only.


## 16. Handover cleanup / manifest correction

During final handover verification, an earlier generated `Current/Aktive_Modliste_S1.42C.txt` was found to have shifted package/version associations.

It was regenerated directly from:
`ProfileSources/S1.42C/export.r2x`

Verified manifest:
- 188 total
- 183 enabled
- 5 disabled

Correct disabled set:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

This was documentation-only; no profile content changed.

Superseded S1.41 handover-support metadata were moved from `Current/` to:
`Archive/S1.41/HandoverCheckpoint/`

Nothing was permanently deleted.

See:
`Current/17_REPO_HANDOVER_CLEANUP_S1.42C.md`

## 17. Historical juijui profile reference

The original `juijui.r2z` profile has been designated as a canonical historical project reference.

Expected location:
`References/LegacyProfiles/juijui/juijui.r2z`

Detailed reference:
`Current/18_JUIJUI_LEGACY_REFERENCE.md`

Project intent:
bring the modern mod constellation/configuration as close as reasonably possible to the old juijui experience while respecting current game version, maintained mods and compatibility.

Once the profile is uploaded, extract the exact historical Jetpack settings from it and stop treating 50 seconds as anything more than an unevidenced fallback.

The generic LethalMin grab/bite + Invincible Pikmin leader-state problem remains the immediate engineering priority and should be solved generically because S1.42C proved it can affect enemies beyond Thumper/Puffer.
