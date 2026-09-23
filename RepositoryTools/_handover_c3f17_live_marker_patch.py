#!/usr/bin/env python3
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md'
t = p.read_text(encoding='utf-8')
old = '<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->'
new = '<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->'
if old not in t:
    raise SystemExit('required ROADMAP live-state marker not found')
p.write_text(t.replace(old, new, 1), encoding='utf-8')
print('synced ROADMAP live-state marker')
