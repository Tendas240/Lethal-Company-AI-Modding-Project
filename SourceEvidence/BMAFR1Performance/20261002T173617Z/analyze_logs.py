"""Read-only BMAFR1 log differential; run with the repository root as argv[1]."""
import collections
import hashlib
import json
import pathlib
import re
import statistics
import sys

ROOT = pathlib.Path(sys.argv[1])
SIGNATURE = 'Array index (0) is out of bounds (size=0)'
EXPECTED = {
    '20261002T154834Z': '3113a1c9df2e1db231cf6aa0e7dc20699894a8646da3eaf7fd1ce0c3d89ac42b',
    '20261002T164741Z': 'ca2d83a56115f66623c3dfb38d2cdd47085b3c0a368efc3ace29321a323b4d90',
}
HEADER = re.compile(r'^\[(\d+):(\d+):([\d.]+)\] \[([^:]+):([^]]+)\] (.*)')
results = {}
plugins = []
for run, expected in EXPECTED.items():
    path = ROOT / 'RuntimeEvidence' / 'S1.42AK-BMAFR1' / run / 'raw/LogOutput.log'
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == expected, (run, digest)
    lines = raw.decode('utf-8-sig').splitlines()
    events = []
    for number, line in enumerate(lines, 1):
        m = HEADER.match(line)
        if m:
            events.append(dict(line=number, seconds=int(m[1])*3600+int(m[2])*60+float(m[3]),
                timestamp=f'{m[1]}:{m[2]}:{m[3]}', severity=m[4].strip(), logger=m[5].strip(), message=m[6]))
    errors = [e for e in events if e['message'] == SIGNATURE]
    loaded = sorted(line.split('Loading [', 1)[1] for line in lines if 'Loading [' in line)
    plugins.append(loaded)
    record = dict(sha256=digest, bytes=len(raw), lines=len(lines), loaded_plugin_count=len(loaded),
        array_count=len(errors), events=[e for e in events if any(token in e['message'] for token in
            ['Event chosen:', 'Succeeded spawning', 'Attempting to spawn Janitor', 'Failed to spawn Janitor',
             'RANDOM MAP SEED:', 'Final length multiplier:', 'Players finished generating the new floor',
             'TransferRenderer:', 'TRAVERSED id=', 'Leaving current lobby',
             'Shutting down and disconnecting', 'Janitor(Clone) from the', 'SpringMan(Clone) from the'])])
    record['stack_contexts'] = [dict(line=i+1, text='\n'.join(lines[max(0,i-3):i+3]))
        for i,line in enumerate(lines) if 'Dusk.SkinnedMeshReplacement' in line]
    if errors:
        times = [e['seconds'] for e in errors]
        gaps = [b-a for a,b in zip(times,times[1:])]
        ordered = sorted(gaps)
        record['timing'] = dict(first=errors[0], last=errors[-1], duration_seconds=times[-1]-times[0],
            interval_rate_per_second=(len(times)-1)/(times[-1]-times[0]), median_gap_ms=1000*statistics.median(gaps),
            p95_gap_ms=1000*ordered[int(.95*len(ordered))], max_gap_ms=1000*max(gaps),
            duplicate_timestamps=len(times)-len(set(times)), gaps_over_100ms=sum(g>.1 for g in gaps),
            bins_10s=dict(sorted(collections.Counter(int((t-times[0])//10) for t in times).items())),
            attached_nonempty_continuation_lines=sum(bool(lines[e['line']]) and not lines[e['line']].startswith('[')
                for e in errors if e['line']<len(lines)))
        record['traversal_windows'] = [dict(line=e['line'], timestamp=e['timestamp'],
            before_1s=sum(e['seconds']-1<=t<e['seconds'] for t in times),
            after_1s=sum(e['seconds']<=t<e['seconds']+1 for t in times))
            for e in events if 'TRAVERSED id=' in e['message']]
    results[run] = record
results['plugin_identity_lists_equal'] = plugins[0] == plugins[1]
print(json.dumps(results, indent=2))
