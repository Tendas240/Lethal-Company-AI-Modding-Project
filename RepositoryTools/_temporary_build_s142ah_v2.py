from pathlib import Path

source_path = Path("RepositoryTools/_temporary_build_s142ah.py")
source = source_path.read_text(encoding="utf-8")
old = '"Do not patch the position-only `DetectNoise()` path"'
new = '"The successor must **not** patch `DetectNoise()`"'
if source.count(old) != 1:
    raise SystemExit(f"Expected exactly one stale DetectNoise evidence assertion, got {source.count(old)}")
source = source.replace(old, new, 1)
namespace = {"__name__": "__main__", "__file__": str(source_path)}
exec(compile(source, str(source_path), "exec"), namespace, namespace)
