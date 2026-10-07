# Externalized Cold History — Logs

The frozen legacy payload formerly stored under `Logs/` was removed from the current working tree on 2026-09-08 after a positive deletion audit.

Exact pre-externalization Git tree SHA:

`9e67fc1a098b869dab9ba86063f5c2396d69c03f`

Verified recovery repository:

`Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`

Frozen recovery commit:

`5dbd0e637a480d8591773e422bbca4b0654cad20`

Recovery rule: `Logs/<relative-path>` maps to the identical `Logs/<relative-path>` at that frozen recovery commit.

Machine authority and registered historical-reference mapping:

`Current/COLD_HISTORY_STORAGE.json`

No Git history rewrite was performed. The exact historical bytes also remain reachable through this primary repository's earlier Git history.

This directory is legacy recovery infrastructure only. Current runtime evidence is stored under `RuntimeEvidence/` and current project truth routes through `Current/CURRENT_STATE.json` plus `Current/PROJECT_KNOWLEDGE_MAP.md`.
