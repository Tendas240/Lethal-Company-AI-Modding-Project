# S1.42AK-SCRAPDIAG1 Scrap Placement Diagnostic

Diagnostic-only BepInEx/Harmony plugin for the LC Office scrap placement investigation.

Contract:

- hard-depends on the reviewed S1.42AJ-DIAG1 Office selector and accepted S139 Compatibility Fixes;
- validates and patches only declared `RoundManager.SpawnScrapInLevel()`;
- installs exactly one postfix ordered after `tendas.s139.compatibilityfixes`;
- schedules two bounded read-only snapshots at approximately 16s and 20s;
- logs stable scrap object IDs, values, world positions, EntranceTeleport Y anchors and downward support-collider paths;
- never mutates scrap quantity, rarity, values, spawn pools, transforms, gameplay state, RPC/network state or configs.

This plugin is diagnostic-only and is not directly promotable to a normal gameplay baseline.
