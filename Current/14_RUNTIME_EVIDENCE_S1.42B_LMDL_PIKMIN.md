# 14 — Runtime Evidence: S1.42B LMDL Guard + Pikmin Interaction Findings

**Evidence:** `RuntimeEvidence/S1.42B/20260902T231959Z/`  
**Candidate:** `Profiles/LC V1 S1.42B LMDL NRE Guard.r2z`  
**Candidate SHA-256:** `8523754926e3f67c0ccef5aee976cbe72ab976f997876c59b51fedcfb293befe`

## LethalModDataLib result — FIX CONFIRMED

The S1.42B null-safe compatibility guard worked.

Runtime markers:
- `[LMDLGuard] Skipping Chainloader PluginInfo with null Instance: MW.MagicWesleyInteriors`
- `[LMDLGuard] Safe ModDataAttribute scan completed: plugins=155, types=10494, nullInstancesSkipped=1.`
- LethalModDataLib continued with `Hooking up save, load and delete events...`
- LethalModDataLib logged `ModDataHandler initialised!`
- LethalModDataLib successfully loaded/saved `LCGeneralSaveData.moddata`.

The S1.42A initialization NRE is therefore resolved by the project-local compatibility guard.

The concrete null Chainloader entry responsible for the upstream crash path is:
`MW.MagicWesleyInteriors`.

Keep the LMDL guard in all descendants while LethalModDataLib 1.2.2 remains present.

## Thumper ↔ Pikmin regression

Runtime sequence:
1. Crawler/Thumper spawned from an indoor vent.
2. Shortly afterwards a Purple Pikmin logged:
   `Grabbed by enemy, will die in 0.75s if not released.`
3. It lost its leader.
4. LethalMin then emitted a large repeated stream:
   `Leader is null when following`
5. The grab-death timer attempted to kill the Pikmin, but Invincible Pikmin blocked final death.

The current LethalMin nightly config has:
- `Use Enemy Configs = true`
- `Thumper Bite Cooldown = 2`
- `Thumper Bite Limit = 3`
- Crawler/Thumper is absent from `Attack Blacklist`.

User requirement:
**Thumper and Pikmin must not interact in either direction.**

Planned isolated control:
- `Thumper Bite Limit = 0`
- add `Crawler` to `[Pikmin Behavior] Attack Blacklist`

Validation must confirm:
- Thumper does not grab/bite Pikmin;
- Pikmin do not attack/latch onto Thumper;
- no new `Grabbed by enemy` sequence attributable to Thumper;
- no resulting `Leader is null when following` spam.

## Puffer → Pikmin regression

The config already has:

`Puffer Can Poison Pikmin = false`

Nevertheless, at Puffer spawn LethalMin logs:

`Injected effect trigger to Puffer's Smoke prefab`

and the user observed Pikmin still being affected by Puffer's attack/smoke.

User requirement:
**Puffer attack/smoke must not affect Pikmin.**

The project-local compatibility plugin v1.2.0 adds a targeted `PufferAI.Start` postfix that removes only LethalMin-owned effect/trigger/hazard MonoBehaviours from Puffer smoke objects. Vanilla Puffer behavior toward players remains untouched.

Expected runtime marker:
`[PufferPikminGuard] Removed ... LethalMin Pikmin effect-trigger component(s) from Puffer smoke.`

Puffer is **not** being added to the Pikmin Attack Blacklist because the user only requested immunity from Puffer attacks, not total bidirectional noninteraction.

## Next isolated candidate

S1.42C — Pikmin Enemy Interaction Guard.

Do not mix BCMER equal EventType weights, interior normalization, CullFactory tuning, or Mausoleum fog tuning into this candidate.
