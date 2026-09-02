# 06 - Recent Work: S1.32 to S1.39

This file preserves detailed recent handover facts so diagnosis context is not lost.

## S1.32 - Leaf Boy and Mirage

Pikmins entered a multi-minute attack loop against `LeafBoi(Clone)`. Because Pikmins are immortal, the engagement could persist indefinitely. Decision: append exactly `Leaf boy` to the existing current LethalMin Attack Blacklist; do not solve targeting by changing Leaf Boy spawn chance/health.

Mirage retention was changed to `neverDeleteRecordings=true` while preserving local volume/record/mimic settings. Mirage stores this in game-root `Mirage/settings.json`, which can survive/ignore profile-import expectations.

## S1.32-S1.35 - ship-door lockout diagnosis

A normal/external close plus AJB's unconditional door-power refill produced permanent outside lockout. The exact original close actor remained unproven. Masked vanilla AI has no hangar-button interaction; Poltergeist ghost interaction is separate.

First custom DLL in S1.33 was not imported by normal Gale profile import and therefore never ran. S1.34's hydraulic countdown was vanilla, not evidence that the algorithm failed.

S1.35 rebuilt the local compatibility plugin against V81 and added DoorAudit/DoorFailsafe plus complete EnemyScan output. Operational rule: use Gale `Advanced options -> Import all files` or import the standalone local-mod package.

## S1.34-S1.36 - EnemyScan, Coin, Puma, SCP999

EnemyScan 1.2.1 source showed `BuildEnemyCountString()` filtered out EnemyAI without ScanNodeProperties. The local plugin patches the listing only.

Puma/PumaAI was identified as vanilla Feiopar.

CodeRebirth Coin was identified as its currency, collected with Denomination Analyzer/MoneyCounter and used by merchant/vending systems.

Current logs contradicted older docs by showing SCP999 2.4.0 loading and throwing a startup NRE. S1.36 disabled ProjectSCP-SCP999 and became the clean deterministic baseline.

### S1.36 runtime acceptance

The user imported S1.36 with Gale `Advanced options -> Import all files`. Runtime confirmed the local compatibility plugin and `[EnemyScanFix]` marker loaded. The ship-door behavior worked as intended in the user's test. A terminal `enemies` screenshot taken around 7pm was cross-checked against the runtime spawn state and the listed counts matched. The user also explicitly confirmed Pikmins were no longer affected by CodeRebirth microwaves. These behaviors are accepted unless later regression evidence appears.

## S1.37 - scrap-level currency filter

User wanted CodeRebirth currency to come from its dedicated systems rather than normal scrap rolls.

S137CompatibilityFixes temporarily removes these during `RoundManager.SpawnScrapInLevel`:

- Coin
- Crisp Dollar Bill
- Wayfarer's Wallet
- Credit Pad 100cc
- Credit Pad 500cc
- Credit Pad 1000cc

Entries are restored after the roll so dedicated CodeRebirth systems stay registered.

## S1.38 - 1440p and Old Bird audio

Added FixCameraResolution 1.5.3 and configured a fixed 2560x1440 internal target. Added Lethal Resonance 4.7.8 plus the LC SoundAPI binding, with exactly three enabled groups: Old Bird, Old Bird footsteps, Old Bird speaker.

S1.38 was run and is the latest runtime-tested reference. The latest log proves:

- profile path/name was `LC V1 S1.38 1440p Old Bird Resonance`;
- `FixCameraResolutions 1.5.3` loaded;
- `S1.37 Compatibility Fixes` loaded;
- `[EnemyScanFix]` marker present;
- SoundAPI completed its load pipeline;
- after the user manually set Mirage retention in the Main Menu/LethalConfig, Mirage loaded `neverDeleteRecordings=true`; the profile import itself had not reliably applied this per-player setting.

Remaining issues discovered in/around this test:

- generated `NewCoinPrefab(Clone)` entries still appeared through a path outside the scrap-only filter;
- the user wanted Flash Turret removed from natural hazard generation;
- Ogopogo/Vermin should be disabled;
- CodeRebirth Autonomous Crane could still kill Pikmin despite `Crane Targets Pikmin=false` and `Crane Squishes Pikmin=false`;
- Old Bird audio replacement still lacked a clean encounter validation;
- the user's four-legged Jester-like indoor enemy was identified from the runtime log as `Cabinet` from `Cabinet_crew-TheCabinet 1.12.1`, with `Spawning Cabinet from vent` logged at runtime.

## S1.39 - broader natural map-object filter + crane shield

S1.39 cumulative plugin filters both V81 `IndoorMapHazard[]` and legacy `SpawnableMapObject[]` during `RoundManager.SpawnMapObjects`.

It suppresses:

- Flash Turret;
- currency/map-object identities detected as Coin, dollar bill, wallet/Wayfarer and matching currency item/scan-node names.

The S1.37 scrap filter remains separately active.

For the crane gap, S1.39 dynamically patches CodeRebirth's `CodeRebirthUtils.KillEnemyOnOwnerClientRpc`. While inside that CodeRebirth utility-kill context, the local plugin blocks `EnemyAI.KillEnemyOnOwnerClient` for Pikmin/Puffmin. This is intentionally narrower than making all Pikmins globally impossible to kill through every game system.

Config changes/verification:

- Biodiversity `OgopogoEnabled=false`;
- Biodiversity `EnableVermin=false`;
- all CodeRebirth/Pikmin toggles remain false;
- GeneralImprovements `AddHealthRechargeStation=true` retained;
- BCMER still disabled;
- S1.38 camera/audio settings carried forward.

S1.39 GitHub Actions run passed compilation, archive CRC, member delta, package manifests and config assertions.

Runtime acceptance is the next task.
