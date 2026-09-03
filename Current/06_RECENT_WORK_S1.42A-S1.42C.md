# 06 — Recent Work S1.42A-S1.42C

## S1.42A — Interior Config Seed

Built from accepted S1.41 using GitHub Actions.

Profile:
`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:
`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Manifest changed from 179 to 188 packages:
- eight requested interior packages;
- one hard dependency, LethalModDataLib 1.2.2.

Runtime seed generated the real config set and registered 52 dungeon flows total, 26 more than S1.41.

Mausoleum generated on Offense and was visually far too foggy.

CullFactory exact IDs discovered:
- `junkrooms`
- `shatteredrooms`

Generated weights were strongly unequal and need future normalization.

S1.42A also exposed a blocking LethalModDataLib initialization NRE.

## S1.42B — LMDL NRE Guard

Compatibility plugin was extended with a null-safe LethalModDataLib registration scan.

Profile:
`Profiles/LC V1 S1.42B LMDL NRE Guard.r2z`

SHA-256:
`8523754926e3f67c0ccef5aee976cbe72ab976f997876c59b51fedcfb293befe`

Runtime proved:
- offending null Chainloader plugin entry was `MW.MagicWesleyInteriors`;
- the guard skipped it;
- LMDL completed initialization;
- save/load/delete hooks connected;
- moddata load/save succeeded.

Result:
**LMDL NRE fixed and carry-forward guard accepted technically.**

The same S1.42B log exposed:
- a Thumper/Crawler spawn followed by a Pikmin enemy-grab state and huge leader-null error spam;
- Puffer smoke still receives a LethalMin effect trigger even with `Puffer Can Poison Pikmin = false`.

## S1.42C — Pikmin Enemy Guard

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Changes:
- `Thumper Bite Limit = 0`;
- `Crawler` added to Pikmin Attack Blacklist;
- compatibility plugin v1.2.0 adds targeted Puffer smoke effect-trigger removal;
- LMDL guard retained.

Runtime evidence:
`RuntimeEvidence/S1.42C/20260902T235238Z/`

Findings:
- no new S1.42C startup regression;
- LMDL remains healthy;
- Puffer did not spawn -> Puffer guard unvalidated;
- Crawler spawned but no deliberate controlled Thumper/Pikmin interaction -> total noninteraction not fully validated;
- Baboon Hawk bit a Bulbmin and reproduced the same leader-null spam.

Important conclusion:
the leader-null loop is a generic LethalMin grab/bite + Invincible-Pikmin state problem, not a Thumper-only problem.

## New binding design decisions captured during this stage

### Interiors
Every interior should have equal effective spawn probability on every moon, now and after future additions.

### Mausoleum
Reduce indoor fog specifically for Melanie Mausoleum.

### BCMER
Use an equal fixed global EventType distribution:
8 categories x 12.5%, using constant scale `12.5, 0, 12.5, 12.5` with `Use custom weights? = false`.

### Functional Microwave
Target volume 0.7 and enable its CodeRebirth editing gate.

### Jetpack
Match old juijui duration if historical evidence is recovered. Current is 40s; 50s is only a fallback candidate, not confirmed historical.

## Current build state

`BuildSpecs/current.json` is disabled/idle after S1.42C runtime.

`BuildSpecs/S1.42D_PLAN.md` is draft only and must not be auto-built.

Next engineering priority:
generic LethalMin grab/bite + invincible follower-state repair.
