# 74 — Large Runtime Log Pipeline and Evidence Retention

**Date:** 2026-09-04  
**Status:** canonical infrastructure and retention policy

## Goal

Runtime logs must be analyzable completely even when they are too large to load into one ChatGPT/GitHub-connector response.

“Completely analyzed” means the automation streams **every source line** through deterministic parsing/aggregation. It does not require placing hundreds of megabytes of raw text into one model context.

At the same time, large temporary logs must not permanently bloat `main` or remain in the repository after their diagnostic value is exhausted.

## Normal path

For ordinary logs use:

`RuntimeInbox/Current/`

Workflow:

`.github/workflows/runtime-ingest.yml`

Analyzer:

`BuildSystem/runtime_log_analyzer.py`

The ingest now automatically creates machine-readable analysis under the run's `analysis/` directory.

For logs up to 8 MiB it additionally creates lossless ~256 KiB `chat_chunks/`, so ChatGPT can read the entire raw log in bounded pieces through normal repository file access.

Every analyzed log produces at least:

- `STATS.json` — exact SHA-256, bytes, line/event counts, severity counts, timestamp range;
- `MARKERS.json` — exact counts plus first/last samples for project-critical markers;
- `SOURCE_COUNTS.json` — event counts by logger/source;
- `TIMELINE_BY_MINUTE.json` — severity distribution over time;
- `TOP_SIGNATURES.md` — highest-frequency normalized event signatures;
- `SIGNATURES_MANIFEST.json` and `signatures/*.jsonl` — exhaustive normalized signature coverage with exact counts, first/last line positions, timestamps, and samples;
- `CHAT_CHUNKS_MANIFEST.json` and optional lossless `chat_chunks/`.

Dynamic GUID/hex/numeric values are normalized only for signature aggregation. The analyzer still processes every original line, and first/last raw samples are retained per signature.

## Very-large path

For logs that would be undesirable on `main` — especially tens/hundreds of MiB or larger — use the disposable branch:

`runtime-large`

and directory:

`RuntimeInbox/Large/`

Prepare locally from the actual game log:

```powershell
python BuildSystem/prepare_large_runtime_log.py "C:\path\to\LogOutput.log"
```

The helper:

1. ZIP-compresses the original log with ZIP64 support;
2. computes original and archive SHA-256 values;
3. if necessary, splits the ZIP into 20 MiB parts suitable even for browser-oriented GitHub uploads;
4. writes `UPLOAD_MANIFEST.json`.

Commit those generated files to `RuntimeInbox/Large/` on the **`runtime-large` branch**, never to `main`.

## Large-ingest workflow

`.github/workflows/runtime-large-ingest.yml`

uses:

`BuildSystem/runtime_large_ingest.py`

It:

1. reconstructs split ZIP parts when present;
2. verifies and records hashes;
3. safely extracts the archive in the runner's temporary filesystem;
4. streams every text-log line through `runtime_log_analyzer.py`;
5. commits only compact analysis + provenance to `main` under `RuntimeEvidence/<build>/<timestamp>/`;
6. uploads the original compressed logical source as a temporary GitHub Actions artifact for **14 days**;
7. force-resets `runtime-large` back to current `main` after successful ingestion.

Result: the large raw upload commit is not retained in the reachable `main` history. The temporary source branch no longer points to it after ingest; GitHub may retain unreachable objects internally until garbage collection, but they are not part of normal project history.

## Querying an arbitrary place in a huge raw log

The compact signature/marker analysis is normally enough for runtime-gate classification. If an unexpected question requires exact raw context while the 14-day artifact still exists, use:

`RuntimeAnalysis/QUERY.json`

Workflow:

`.github/workflows/runtime-large-query.yml`

Extractor:

`BuildSystem/runtime_log_query.py`

Supported query modes:

- substring or regular-expression search with configurable context lines;
- exact global line ranges.

The workflow downloads the temporary raw artifact, streams the requested source/archive member, and commits only the requested excerpt plus query metadata to:

`RuntimeEvidence/<build>/<timestamp>/analysis/queries/`

Then it automatically disarms `RuntimeAnalysis/QUERY.json`.

This gives ChatGPT targeted, exact access to arbitrary portions of a 500 MB-class source without committing the full expanded log to `main`.

## GitHub size reality

A normal GitHub Git blob has a hard per-file limit around 100 MiB, and browser upload paths can be lower. Therefore an uncompressed 500 MB log must not be committed as one file.

The project solution is:

- compress first;
- split the compressed archive into 20 MiB upload parts when necessary;
- use the disposable `runtime-large` branch;
- retain only compact analysis on `main`.

The pipeline itself is streaming and is not tied to 500 MB; the practical limits are GitHub runner disk/time/artifact quotas rather than ChatGPT context size.

## Retention classes

### A — keep canonically

Keep long-term when relevant:

- runtime acceptance/rejection document;
- build/profile identity and SHA-256;
- raw log SHA-256 and size;
- exact gate verdict;
- key marker counts and error classifications needed to understand the decision;
- unique root-cause evidence or failed-approach evidence still useful for regression prevention.

### B — keep while diagnostically useful

May be deleted after the dependent issue/gate is closed and the canonical documents contain enough evidence:

- compact signature chunks;
- query excerpts;
- extracted copies;
- auxiliary analyzer outputs;
- ordinary raw logs used only as comparison evidence.

### C — disposable by design

Delete/expire as soon as they are no longer required:

- very-large raw logs;
- split upload parts;
- temporary expanded files;
- lossless chat chunks when their gate and any follow-up investigation are closed;
- Actions raw artifacts after the active investigation window.

Large raw artifacts expire automatically after 14 days unless intentionally preserved elsewhere for an unresolved issue.

## Deletion rule

A runtime raw log may be removed when **all** are true:

1. its runtime gate has a recorded verdict;
2. no open issue still depends on exact raw context from that run;
3. any unique error/root-cause evidence has been preserved in canonical documentation or a compact excerpt;
4. its SHA-256, build identity, and verdict are preserved where future handover can find them;
5. it is not the only useful comparison baseline for an immediately following gate.

For failed/unresolved runs, retain the raw evidence until root cause is closed or the unique evidence has been preserved elsewhere.

## Current S1.42T retention decision

`RuntimeEvidence/S1.42T/20260903T222109Z/raw/LogOutput.log`

is **not deleted yet**. It is currently the clean BCMER-off normal-enemy reference run for the next BCMER restoration gate.

After that comparison/final normal-stack gate is closed, it may be pruned while keeping `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`, the raw SHA-256, and any still-relevant compact evidence.
