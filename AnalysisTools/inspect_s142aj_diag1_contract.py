#!/usr/bin/env python3
"""Read-only exact-package evidence for the AJ diagnostic selection patch."""
import hashlib, io, json, os, re, subprocess, urllib.request, zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "s142aj-diag1-contract-output"
out.mkdir(exist_ok=True)
profile = root / "Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z"
digest = lambda b: hashlib.sha256(b).hexdigest()
assert digest(profile.read_bytes()) == "7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba"
with zipfile.ZipFile(profile) as z:
    export = z.read("export.r2x").decode("utf-8-sig")
assert re.search(r"- name: IAmBatby-LethalLevelLoader\s+version:\s+major: 1\s+minor: 7\s+patch: 12\s+enabled: true", export)
assert "LethalLevelLoaderUpdated" not in export
url = "https://gcdn.thunderstore.io/live/repository/packages/IAmBatby-LethalLevelLoader-1.7.12.zip"
with urllib.request.urlopen(url, timeout=90) as r:
    data = r.read(64 * 1024 * 1024 + 1)
assert len(data) <= 64 * 1024 * 1024
with zipfile.ZipFile(io.BytesIO(data)) as z:
    manifest = json.loads(z.read("manifest.json"))
    assert manifest["version_number"] == "1.7.12"
    names = [n for n in z.namelist() if n.rsplit("/", 1)[-1] == "LethalLevelLoader.dll"]
    assert len(names) == 1, names
    dll = z.read(names[0])
work = Path(os.environ["RUNNER_TEMP"]) / "s142aj-diag1-contract"
work.mkdir(exist_ok=True)
binary = work / "LethalLevelLoader.dll"
binary.write_bytes(dll)
p = subprocess.run(["ilspycmd", str(binary)], check=True, capture_output=True, timeout=300)
source = p.stdout.decode("utf-8")
(out / "LethalLevelLoader-1.7.12.cs").write_text(source)
record = {"repository_commit": os.environ["GITHUB_SHA"], "base_profile_sha256": digest(profile.read_bytes()),
          "package_url": url, "package_sha256": digest(data), "dll_member": names[0],
          "dll_sha256": digest(dll), "source_sha256": digest(p.stdout), "decompiler": "11.0.0.9375",
          "qualification": "Pinned package materialized from exact AJ export; first capture hashes, not independently verified installed-user DLL."}
(out / "PROVENANCE.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
lines = source.splitlines()
indices = set()
for i, line in enumerate(lines):
    if any(term in line for term in ("GetValidExtendedDungeonFlows(", "GetRandomDungeonFlow", "NumberlessPlanetName", "class ExtendedDungeonFlowWithRarity", "DungeonFlow DungeonFlow", "string DungeonName")):
        indices.update(range(max(0, i - 8), min(len(lines), i + 95)))
print("=== BOUNDED CONTRACT EXCERPTS ===")
for i in sorted(indices):
    print(f"{i+1}: {lines[i]}")
