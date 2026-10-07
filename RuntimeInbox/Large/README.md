# Very large runtime logs

Use this directory only on the disposable `runtime-large` branch.

Normal logs should continue to go to `RuntimeInbox/Current/` on `main`.

For a very large `LogOutput.log`, run from the repository root:

```powershell
python BuildSystem/prepare_large_runtime_log.py "C:\path\to\LogOutput.log"
```

The helper ZIP-compresses the log and automatically splits the archive into 20 MiB parts when necessary, keeping each upload part comfortably below GitHub's per-file limits. Commit the generated files under `RuntimeInbox/Large/` to the `runtime-large` branch. The workflow streams every extracted log line through the analyzer, writes only compact machine-readable analysis to `main`, uploads temporary raw evidence as a 14-day GitHub Actions artifact, and force-resets `runtime-large` back to `main` after a successful ingest.

Do not put very large raw logs directly on `main`: deleting them later would not remove their blobs from reachable Git history.
