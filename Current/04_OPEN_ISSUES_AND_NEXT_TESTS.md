# 04 — Open Issues and Next Tests

**Status:** CURRENT ROUTING ALIAS / NO LIVE-STATE DUPLICATION  
**Canonical machine queue:** `Current/CURRENT_STATE.json`  
**Canonical human lifecycle:** `Knowledge/CURRENT_LIFECYCLE.md`

This file intentionally does not duplicate volatile accepted/latest/candidate IDs, profile hashes, controller values, completed runtime coverage or the current gameplay gate.

For the live work queue, read these fields from `Current/CURRENT_STATE.json`:

- `runtime_test_outstanding`
- `selected_scope`
- `next_action`
- `controllers`

Then use `Current/PROJECT_KNOWLEDGE_MAP.md` to route the exact task to its canonical topic/evidence. For current build/runtime lifecycle details, use `Knowledge/CURRENT_LIFECYCLE.md`.

Historical test plans, candidate records, runtime acceptances/rejections and old "next action" snapshots remain evidence only; they do not override the canonical machine state.
