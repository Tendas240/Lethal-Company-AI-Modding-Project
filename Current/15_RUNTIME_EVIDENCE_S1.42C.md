# 15 — Runtime Evidence: S1.42C Pikmin Enemy Guard

**Evidence:** `RuntimeEvidence/S1.42C/20260902T235238Z/`  
**Candidate:** `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`  
**Candidate SHA-256:** `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

## Overall result

No new startup regression attributable to S1.42C was found.

LethalModDataLib remains healthy:
- null entry `MW.MagicWesleyInteriors` skipped;
- safe scan completed;
- save/load/delete hooks connected;
- `ModDataHandler initialised!`;
- moddata load/save continued.

The S1.42B LMDL fix therefore remains confirmed.

## Puffer guard

The compatibility plugin registered the patch:

`[PufferPikminGuard] Patched PufferAI.Start ...`

However, no Puffer spawned in this runtime evidence.

Therefore:
- Puffer smoke immunity is **not runtime-validated yet**;
- there is no `[PufferPikminGuard] Removed ...` runtime marker because `PufferAI.Start` never executed;
- keep the guard and validate opportunistically in a later run.

## Thumper / Crawler guard

A Crawler/Thumper did spawn in the Mineshaft at approximately 23:37:23 and was later killed by the player.

During the logged Crawler lifetime:
- no LethalMin Thumper-specific Pikmin bite/grab message was identified;
- no clear Pikmin attack/latch message against the Crawler was identified;
- the user did not deliberately observe/test the interaction.

Therefore the result is **compatible with the guard working but not sufficient for acceptance**.

Keep:
- `Thumper Bite Limit = 0`
- `Crawler` in Pikmin Attack Blacklist

and validate deliberately when a Thumper is encountered in a future run.

## Important new finding — leader-null spam is not Thumper-specific

Later in the run a Bulbmin was explicitly bitten by a Baboon Hawk:

`LethalMin: BaboonBirdPikminEnemy.BitePikmin: Bulbmin_w70BA8K is being bitten by BaboonHawkEnemy(Clone)`

Immediately afterwards:
- leader removed;
- `Grabbed by enemy, will die in 0.5s if not released.`
- Invincible Pikmin prevented final death;
- repeated `Leader is null when following` errors followed.

This proves the error-spam mechanism is a **general LethalMin enemy grab/bite + invincible-Pikmin state issue**, not uniquely a Thumper bug.

Do not blindly blacklist every enemy. A later compatibility fix should preferably repair/reset the Pikmin grab/follow state generically while preserving intended enemy interactions, unless the user explicitly requests immunity from a specific enemy.

## Other known log noise

Previously-known/non-S1.42C-specific warnings remain, including:
- SoundAPI reporting TypeLoadException during floor generation;
- SoftMaskKiller-protected SoftMask NREs;
- duplicate NetworkPrefab hash warnings from the expanded content set;
- assorted RuntimeNavMeshBuilder unreadable-mesh messages.

A scene-teardown `InvalidOperationException: Collection was modified` also appeared near ship-phase onion cleanup. Track if it reproduces with user-facing consequences; do not attribute it to the S1.42C guard without evidence.

## Next-build user requests

### Jetpack capacity

User wants Jetpack capacity/duration matched to the old juijui profile.

Current active setting:
- ButteryBalance `[Item.Jetpack] Reduce Battery = true`
- this explicitly reduces Jetpack battery from 50 seconds to 40 seconds.

The exact historical juijui Jetpack value is **not currently preserved in `References/juijui_Referenzwerte.txt` or other text snapshots discovered so far**.

Do not invent the juijui value.

If no stronger historical evidence can be recovered before the next tuning build, the technically obvious first candidate is:
- `Reduce Battery = false` => restore current vanilla 50-second capacity,

but this is only a fallback candidate, not yet proven to equal the old juijui profile.

### CodeRebirth Functional Microwave volume

Generated CodeRebirth config exposes:

- `Functional Microwave | Allow Editing Config = false`
- `Functional Microwave | Volume = 1`

User wants the Functional Microwaves slightly quieter.

Next-build target:
- set `Functional Microwave | Allow Editing Config = true`
- set `Functional Microwave | Volume = 0.7`

Rationale:
- 0.7 is a moderate 30% reduction;
- preserve audibility and gameplay feedback;
- CodeRebirth edit gate must be enabled so the override can survive runtime regeneration, consistent with the S1.40B lesson.

This is a config-only change; no audio Harmony patch should be needed unless runtime regenerates/ignores the value.

## Status

S1.42C is a useful regression candidate and can remain the technical base for descendants.

Unvalidated but retained:
- Thumper ↔ Pikmin total noninteraction;
- Puffer → Pikmin smoke immunity.

Confirmed:
- LMDL NRE fix remains healthy.

Open generic issue:
- enemy bite/grab + Invincible Pikmin can leave a follower in leader-null error spam (confirmed with Baboon Hawk).
