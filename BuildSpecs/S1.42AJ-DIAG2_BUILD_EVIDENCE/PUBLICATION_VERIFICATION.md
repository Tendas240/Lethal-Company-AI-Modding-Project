# S1.42AJ-DIAG2 reviewed-artifact publication verification

- Source PR: #117, reviewed head `753491b4da672bc8d731c3e2c8e7f3caff6def5b`.
- Merge commit: `638b9ee5c715656b41954cc59339c2c9d9d96ea6`.
- Static/build gate: run `35337732825`, artifact `S1.42AJ-DIAG2-review`, artifact ID `10543786202`.
- PR-head Knowledge Architecture run: `35337732721` / #485 — SUCCESS.
- Merge-head Knowledge Architecture run: `35337908516` / #486 — SUCCESS.
- Artifact ZIP SHA-256: `3ebabd1af28a0dbe08faa32809ef21bea76dc553100acb3caa2484dfced73aae`.
- Published DIAG2 profile SHA-256: `1a17b532ebe5cfa598348ae15dea21af906ac7b33ec00c9c428d2684cc9f69cb`.
- Exact parent DIAG1 profile SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`.
- DIAG1 force-selection DLL remains byte-identical at `9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad`.
- Accepted Interior Weight Normalization remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.
- Member-by-member verification proves zero changed existing members, zero removed members and exactly one added member: `BepInEx/config/Piggy.LCOffice.cfg`.
- The exact added config bytes are `[General]` with `Camera Frame Speed = 0`; `export.r2x` remains byte-identical to DIAG1.
- Publication uses the exact already-reviewed CI artifact. No rebuild is substituted.
- `Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged. Balanced S1.42AJ remains lifecycle authority; DIAG2 is not armed by this publication.

Status: `STATIC_PASS_NOT_RUNTIME_READY`. Publication proves the isolated artifact delta only and does not establish performance causality.
