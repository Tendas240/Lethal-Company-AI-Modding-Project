# 06 — Recent Work: S1.32 to S1.36

This file preserves the detailed handover facts from the work phase after S1.31 so diagnostic context is not lost.

## S1.31 Leaf Boy / LethalMin incident

User observation:

- Pikmins attacked Leaf Boys continuously.
- Leaf Boy appeared unable to end the interaction.
- Because Pikmins are immortal, the engagement could continue indefinitely.

Runtime evidence showed:

- LethalMin registered Leaf boy as a Pikmin enemy.
- LethalConfig registered the LethalMin/Pikmin Behavior/Attack Blacklist setting.
- repeated Pikmin hits against LeafBoi(Clone),
- repeated real damage aggregation through LethalMin over several minutes.

Historical handover data explicitly warned not to replace the newer longer blacklist with an old shorter list.

Decision:

- append exactly Leaf boy to the existing Attack Blacklist;
- do not change Leaf Boy spawn chance, health, or other behavior merely to solve Pikmin targeting.

S1.36 still carries this append-only blacklist change.

## Mirage recording retention

Observed runtime settings before the change:

- localPlayerVolume: 0.5
- neverDeleteRecordings: false
- allowRecordVoice: true
- muteVoiceMimic: false

Mirage source/documentation established game-root storage:

- settings: <Lethal Company folder>/Mirage/settings.json
- recordings: <Lethal Company folder>/Mirage/Recording

Decision in S1.32+:

- neverDeleteRecordings=true;
- preserve the other observed settings.

## S1.32 unexpected ship-door lockout

User test:

- left the ship for the dungeon;
- returned to a closed hangar door;
- could not enter;
- AJB Keep hangar ship door closed prevented hydraulic power from counting down, so the door never auto-reopened.

Investigation:

- Malfunctions was active at that time, but the analyzed run did not show a successful relevant door malfunction.
- BCMER was disabled.
- a MaskedPlayerEnemy was near the ship around a suspicious time window.
- source inspection of vanilla MaskedPlayerEnemy found no interaction with StartButton, StopButton, or HangarShipDoor controls.
- Poltergeist can let dead players/ghosts interact with ship-door buttons; that is distinct from Masked AI.
- vanilla logging does not reliably identify the actor/source for an ordinary hangar-button close.

Conclusion:

- exact original close trigger remained unproven;
- permanent lockout was clearly caused by a close action combined with AJB's unconditional door-power refill.

## S1.33 first door-failsafe design

Goal:

- retain unlimited closed-door power while a living player is inside;
- prevent permanent outside lockout by allowing vanilla hydraulic drain when every living player is outside;
- log door state/method stacks for future attribution.

Implementation:

- AJB disabled;
- custom S133ShipDoorFailsafe.dll added.

Important later discovery:

- the DLL was embedded in the .r2z but normal Gale import did not install/load it;
- therefore S1.33's algorithm was never actually runtime-tested.

## Malfunctions policy from S1.34

The user explicitly requested that zealsprince-Malfunctions be disabled and remain disabled until the user might explicitly request reactivation in the future.

This is a persistent project decision.

S1.36 keeps it disabled.

## S1.34 runtime test — door behavior

User test while alone inside the landed ship:

- closed hangar door from inside;
- door energy percentage decreased;
- at 0% the door reopened.

Log audit:

- no S1.33 Ship Door Failsafe plugin load line;
- no DoorAudit;
- no DoorFailsafe.

Conclusion:

- custom DLL was not installed/loaded by Gale;
- AJB was also disabled;
- observed behavior was pure vanilla hydraulic behavior, not failure of the custom algorithm.

Operational rule for future local-DLL profiles:

- Gale Advanced options → Import all files, or
- import the supplied local-mod ZIP separately.

## S1.34 runtime test — EnemyScan

User suspected the enemies terminal command did not show every spawned enemy.

EnemyScan 1.2.1 source confirmed the reason in BuildEnemyCountString():

FindObjectsOfType<EnemyAI>().Where(ai => ai.GetComponentInChildren<ScanNodeProperties>() is not null)

The mod intentionally hid enemies that were not scannable / lacked a scan node.

Conclusion:

- enemies was not a complete active-enemy census.

S1.35/S1.36 patches only that list-building result so all active EnemyAI with valid EnemyType are grouped and shown.

## S1.34 runtime test — Coin

Log/runtime registration showed Coin under CodeRebirth.

CodeRebirth source confirms:

- Coin is code_rebirth:coin;
- collecting it requires a MoneyCounter supplied by the Denomination Analyzer;
- without the analyzer the player gets a hint to buy it from the ship terminal;
- when collected, the coin adds its value to CodeRebirth stored currency and despawns;
- stored money is used by CodeRebirth merchant/vending systems.

## S1.34 runtime test — Puma

Puma / PumaAI is not a mod name.

It is the internal vanilla class/name for the V80+ Feiopar enemy.

Other mods may patch PumaAI, but the enemy itself is vanilla.

## S1.35 rebuilt compatibility plugin

S135CompatibilityFixes.dll was compiled against V81 GameLibs.

Door logic:

- counts living controlled players only;
- inside status uses isInHangarShipRoom plus shipInnerRoomBounds fallback;
- refills door power only when landed, closed, and at least one living player is inside;
- when all living players are outside, vanilla drain/open logic is allowed;
- orbit/leaving/no-living-player states are left alone;
- door method/button audit logging retained.

EnemyScan patch:

- no ScanNode requirement for terminal listing;
- no spawn/AI/Power changes.

A standalone local-mod ZIP was created as installation fallback.

S1.35 passed compile/archive/diff checks but was not runtime-tested.

## SCP999 contradiction found during handover

Older current documentation claimed SCP999 was disabled after the historical NRE incident.

Current S1.31, S1.32 and S1.34 runtime logs explicitly showed:

- Loading [SCP999 2.4.0]
- immediate NullReferenceException in SCP999.Plugin.Awake()
- later SCP999 Max health debug lines.

The S1.35 manifest still had ProjectSCP-SCP999 enabled:true.

Handover decision:

- do not freeze this known regression into the new baseline;
- create S1.36 as S1.35 plus exactly ProjectSCP-SCP999 enabled:false.

## S1.36 canonical handover candidate

Profile:

Profiles/LC V1 S1.36 Handover Clean Baseline.r2z

Manifest:

- 176 total
- 170 active
- 6 disabled

Disabled:

- AJB-Keep_hangar_ship_door_closed
- zealsprince-Malfunctions
- Reiko88-Observer
- ProjectSCP-SCP999
- Kittenji-Dont_Touch_Me
- SoftDiamond-BrutalCompanyMinusExtraReborn

Archive verification confirmed:

- only export.r2x changed relative to S1.35;
- custom S135CompatibilityFixes DLL remains embedded;
- Leaf boy blacklist remains;
- Mirage neverDeleteRecordings=true remains;
- no other S1.35 archive member changed.

Runtime status:

**not yet tested**.

The next chat should begin with the controlled S1.36 import/load/door/enemy-list/SCP999 tests in 04_OPEN_ISSUES_AND_NEXT_TESTS.md.
