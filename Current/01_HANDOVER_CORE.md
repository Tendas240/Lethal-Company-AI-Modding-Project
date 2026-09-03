# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Current built candidate:
**S1.42M - Baboon Hawk Death Cleanup**

Profile:
`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Compatibility plugin:
- version 1.3.8
- DLL SHA-256 `47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Latest valid runtime evidence is still S1.42L:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

## Runtime status

Closed/PASS:
- Thumper/Crawler -> Pikmin protection;
- Pikmin -> Thumper/Crawler attack/latch;
- Puffer -> Pikmin;
- Jetpack;
- Baboon Hawk -> Pikmin protection;
- Pikmin -> Baboon Hawk live attack/latch.

S1.42L proved that Pikmin can latch to, damage and kill a Baboon Hawk with zero leader-null errors.

The remaining isolated issue is **death cleanup / corpse ownership**:
- latched Pikmin remained on the dead original Hawk target;
- SellBodies moved that old target away after spawning `BaboonHawkBody(Clone)`;
- attacking Pikmin visually disappeared with it;
- living Hawks picked up the new corpse item.

## Binding desired Baboon Hawk behavior

Living Hawk -> Pikmin:
blocked target/chase/bite/grab/hold.

Pikmin -> living Hawk:
normal LethalMin attack/latch allowed.

On Hawk death:
- attacking Pikmin must detach and remain usable;
- SellBodies corpse must remain enabled;
- Dead Baboon Hawk body must remain available for player/Pikmin carrying;
- Pikmin must be able to carry the corpse toward the Onion;
- living Hawks must not pick up the corpse.

## S1.42M scope

Only:
- exact `BaboonBirdAI.KillEnemy(bool)` death hook;
- exact `PikminAI.RemoveCurrentTask()` runtime resolution;
- specific dying-Hawk child Pikmin cleanup;
- exact `BaboonBirdAI.CanGrabScrap(GrabbableObject)` corpse rejection.

No global scene scan.
No broad/inherited LethalMin scan.
SellBodies remains enabled.

## Exact next action

Import:
**Gale -> Advanced options -> Import all files**

Test S1.42M only:
1. throw Pikmin onto a Baboon Hawk;
2. let them kill it;
3. confirm Pikmin detach/remain visible and usable;
4. wait >4 seconds;
5. confirm the Dead Baboon Hawk body remains;
6. throw Pikmin onto the corpse and verify Onion carrying;
7. confirm living Hawks do not pick up the corpse;
8. confirm Hawk -> Pikmin ignore still works;
9. confirm no `Leader is null when following`;
10. upload full log to `RuntimeInbox/Current/`.

## Temporary test state

EnemyIsolation:
enabled.

BCMER:
exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` disabled.

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal spawning/BCMER before S1.42M is evaluated.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`

## Critical anti-regression

- no S1.42D broad/inherited LethalMin Harmony scan;
- no continuous Update-driven global EnemyAI scan;
- no BCMER 2.0.0 upgrade without explicit decision;
- do not remove the S1.42C enemy restore baseline;
- CodeRebirthLib must not return;
- unknown Enemy PowerLevels must not be guessed.

## Deferred maintenance

Do not clean unrelated documentation/source drift during the active S1.42M gate.

Known later cleanup:
- `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in `Patches/S139CompatibilityFixes/Plugin.cs`;
- structural optimization per `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`.
