# 04 — Open Issues and Next Tests

## Active next task — S1.42T Normal Enemy Restore

S1.42S focused Baboon-Hawk/Pikmin gate is **closed / PASS**.

Evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

Next plan:

`BuildSpecs/S1.42T_PLAN.md`

Restore contract:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

### Required S1.42T delta

Set:

`Isolated Enemy Regression = false`

Do not change the compatibility code.

Preserve:

- v1.3.14 compatibility plugin;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- all accepted S1.42S interaction fixes.

Keep exact BCMER 1.71.0 **disabled** for this first restore gate.

### S1.42T runtime acceptance

- EnemyIsolation warning absent.
- Normal non-allowlisted enemies can spawn again.
- Terminal EnemyScan can show normal active enemies.
- No startup crash/freeze.
- No Work/no-task loop.
- No Leader-null loop.
- No new exception flood.
- Commit full fresh `LogOutput.log` to `RuntimeInbox/Current/`.

## Following gate — BCMER restoration

After S1.42T passes:

Re-enable **exact**:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Use the accepted S1.41 BCMER config/ownership/rain-event decisions.

Do not upgrade to BCMER 2.0.0.

Keep BCMER restoration separate from the first normal-enemy restore gate.

## Monitor-only issue

LethalMin disconnect-only exception:

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

Observed once during lobby disconnect after ShipOnion save.

No user-facing regression.

Status:

**monitor only**

Do not patch unless reproducible/user-facing and supported by a Patch Safety Review.

## Remaining broader S1.42 roadmap

Still pending after enemy/BCMER restoration:

- final normal-stack runtime acceptance;
- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- final S1.42 acceptance.

See:

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`

## Repository maintenance

Structural repository optimization remains planned in:

`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Do not mix migration work into S1.42T gameplay restoration.
