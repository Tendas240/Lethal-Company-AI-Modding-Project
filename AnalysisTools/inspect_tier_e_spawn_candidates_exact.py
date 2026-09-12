#!/usr/bin/env python3
"""Exact full-source capture for Tier-E S1.42AI spawn-owner candidates."""
from __future__ import annotations
import hashlib, json, os, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tier-e-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-e-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "fce6d19de0a8810fe457b0436a44f948c51701cf"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_e_spawn_candidates_exact.py",
    ".github/workflows/tier-e-spawn-candidates-exact-review.yml",
}
EXPECTED = ({'package': 'DiFFoZ-LethalPerformance', 'version': '1.2.6', 'zip_sha256': 'b43e4358e79917ae181b9912f2fe52ae8d0ef1680da27824aa12b890fe4a5c2b', 'member': 'BepInEx/patchers/LethalPerformance/LethalPerformance.Patcher.dll', 'dll_sha256': 'a7673b28042d2a95e169eb46d1149e3203b6a0975d038783124a4219c6e00b2a', 'il_sha256': '039f51549da2c742bb0cec07314947be8a3fc4f98fe5a79ac2c36c85b175b471', 'stem': 'LethalPerformance-Patcher-1.2.6'}, {'package': 'DiFFoZ-LethalPerformance', 'version': '1.2.6', 'zip_sha256': 'b43e4358e79917ae181b9912f2fe52ae8d0ef1680da27824aa12b890fe4a5c2b', 'member': 'BepInEx/plugins/LethalPerformance/LethalPerformance.dll', 'dll_sha256': 'ebc853ad5f1b6469f7db9a33bfc4480dbc7d532b83133aab524c2dd28761f55c', 'il_sha256': 'a6451014d26ec8677c93839ea081fb13b8508d128c3fe0a7b4ef5a90cda65e6d', 'stem': 'LethalPerformance-Plugin-1.2.6'}, {'package': 'DiFFoZ-LethalPerformance', 'version': '1.2.6', 'zip_sha256': 'b43e4358e79917ae181b9912f2fe52ae8d0ef1680da27824aa12b890fe4a5c2b', 'member': 'BepInEx/plugins/LethalPerformance/LethalPerformance.Unity.dll', 'dll_sha256': 'c74f42554f49c6fe24fafe6da40d7ec66fd5ac71d68d77314af2296b171cd75e', 'il_sha256': 'e277841eb91d034b65493ca5b1bca55c9cc7aab9207254f4d8e893d45558bd53', 'stem': 'LethalPerformance-Unity-1.2.6'}, {'package': 'Scoops-LethalSponge', 'version': '1.4.3', 'zip_sha256': 'dcd9e94b1c5747875edba95e9f9f49ba3a1c77b33d3d8ba2af099a153b61633e', 'member': 'LethalSponge/LethalSponge.dll', 'dll_sha256': 'd0fdf6b3f4ab1669f6dd523f506256d2322a3910e0045bf54030f322ab381ec0', 'il_sha256': '07b422e567464d59db15cbc2ca3f2a10607ee007efc15821bbd5c2881ed0baf3', 'stem': 'LethalSponge-1.4.3'}, {'package': 'ButteryStancakes-BarberFixes', 'version': '1.3.1', 'zip_sha256': '5dfc72cfe3b6e729da839cde8b24d2962abe7a5097c86cdaffa8dd12bb6ac41f', 'member': 'BarberFixes.dll', 'dll_sha256': 'ce625861badbe0946fcaa0456272ad3a7074704bf998a8d1cff223cce7ae4ae8', 'il_sha256': 'd1fd8b9386fc3ffd144b4104a3fd226d876eb97af715c70cae5ad44f9899cb39', 'stem': 'BarberFixes-1.3.1'}, {'package': 'Wexop-RandomEnemiesSize', 'version': '1.1.20', 'zip_sha256': '48d3e16fe2c26e36a6b476467d53f641aed93880f712df09bf2a1ed0d8ca44cd', 'member': 'RandomEnemiesSize.dll', 'dll_sha256': '8f9723eeac8f2c3281be2b1e3866475cad6110cc10b2e95b1632db051fb94b8e', 'il_sha256': '31b7ea2da68da24107006899a7cd4909cdcf864db3df525b43722a988eeb0006', 'stem': 'RandomEnemiesSize-1.1.20'}, {'package': 'TheFluff-FairAI', 'version': '1.6.1', 'zip_sha256': 'a8baf78603fffa98581659823babdcef8b3f65fbdcef8afbcc827a4e8f9738ec', 'member': 'FairAI.dll', 'dll_sha256': '807efe10eab10168dcfbb08185688930bba212580c48c61e9f4dec9260b4d6e1', 'il_sha256': '7649b15b6fbbb0a924fc75509ae0a701046384af31d4eb11676e4b64862dc5fd', 'stem': 'FairAI-1.6.1'}, {'package': 'ButteryStancakes-MaskFixes', 'version': '1.6.2', 'zip_sha256': 'c621c5deb337511983c257ada68631d75ae2660bf3ddc26ac3efd362a9250901', 'member': 'MaskFixes.dll', 'dll_sha256': '9c992664706513c11b6cc26b2f7281dead2f67afefaf6fe5012b2d780d095921', 'il_sha256': '5d76ee08739e3ba0695b1fb0f3577948558fda3dc9035e3dd99dfa249fa446d8', 'stem': 'MaskFixes-1.6.2'})

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr[-2000:]))
    return p.stdout.strip()

def verify_analysis_branch_delta() -> None:
    p = subprocess.run(["git","merge-base","--is-ancestor",CANONICAL_MAIN,"HEAD"], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError("Canonical main is not an ancestor of analysis HEAD")
    changed = [x for x in git("diff","--name-only",CANONICAL_MAIN+"..HEAD").splitlines() if x]
    unexpected = sorted(set(changed) - ALLOWED_DELTA)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))

def run(args: list[str]) -> bytes:
    p = subprocess.run(args, capture_output=True, timeout=420)
    if p.returncode:
        raise RuntimeError(f"{args[0]} failed ({p.returncode}): " + p.stderr.decode("utf-8",errors="replace")[-4000:])
    if len(p.stdout) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"Decompiler output exceeded {MAX_OUTPUT_BYTES} bytes")
    return p.stdout

def download(url: str, path: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent":"s142ai-tier-e-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data

verify_analysis_branch_delta()
verification = {
    "schema_version":1,
    "purpose":"S1.42AI-DIAG1 Tier-E exact review capture for six prioritized remaining discovery-positive packages (eight managed DLLs)",
    "canonical_main":CANONICAL_MAIN,
    "repository_commit":os.environ.get("GITHUB_SHA"),
    "discovery_run":DISCOVERY_RUN,
    "discovery_head":DISCOVERY_HEAD,
    "decompiler":{"tool":"ilspycmd","version":ILSPY_VERSION},
    "assemblies":[],
    "qualification":"Complete C#/IL decompile of eight ZIP/DLL/discovery-IL anchored assemblies from six packages. Evidence only; no DIAG1 implementation, build, controller transition, Gale import or gameplay authorization."
}
cache = {}
for item in EXPECTED:
    key=(item["package"],item["version"])
    if key not in cache:
        url=f"https://gcdn.thunderstore.io/live/repository/packages/{item['package']}-{item['version']}.zip"
        zp=WORK/(item["package"]+"-"+item["version"]+".zip")
        package_bytes=download(url,zp)
        actual_zip=sha256(package_bytes)
        if actual_zip != item["zip_sha256"]:
            raise RuntimeError(f"ZIP SHA mismatch for {item['package']}: {actual_zip}")
        cache[key]=(zp,actual_zip)
    zip_path, actual_zip=cache[key]
    with zipfile.ZipFile(zip_path) as archive:
        if item["member"] not in archive.namelist():
            raise RuntimeError("Exact DLL member missing: "+item["member"])
        dll_bytes=archive.read(item["member"])
    actual_dll=sha256(dll_bytes)
    if actual_dll != item["dll_sha256"]:
        raise RuntimeError(f"DLL SHA mismatch for {item['member']}: {actual_dll}")
    dll_path=WORK/(item["stem"]+".dll")
    dll_path.write_bytes(dll_bytes)
    il=run(["ilspycmd","-il",str(dll_path)])
    actual_il=sha256(il)
    if actual_il != item["il_sha256"]:
        raise RuntimeError(f"Discovery IL SHA mismatch for {item['member']}: {actual_il}")
    source=run(["ilspycmd",str(dll_path)])
    cs_name=item["stem"]+".cs"; il_name=item["stem"]+".il"
    (OUT/cs_name).write_bytes(source); (OUT/il_name).write_bytes(il)
    verification["assemblies"].append({
        "package":item["package"],"version":item["version"],"package_zip_sha256":actual_zip,
        "member":item["member"],"dll_sha256":actual_dll,
        "source_sha256":sha256(source),"source_bytes":len(source),
        "source_lines":len(source.decode("utf-8",errors="replace").splitlines()),
        "il_sha256":actual_il,"il_bytes":len(il),
        "il_lines":len(il.decode("utf-8",errors="replace").splitlines()),
        "source_occurrences":{
            "EnemyAI":source.count(b"EnemyAI"),"EnemyType":source.count(b"EnemyType"),
            "enemyPrefab":source.count(b"enemyPrefab"),"Instantiate":source.count(b"Instantiate"),
            "NetworkObject":source.count(b"NetworkObject"),"SpawnEnemyOnServer":source.count(b"SpawnEnemyOnServer"),
            "SpawnEnemyGameObject":source.count(b"SpawnEnemyGameObject"),"EnemyVent":source.count(b"EnemyVent"),
            "SpawnableEnemyWithRarity":source.count(b"SpawnableEnemyWithRarity"),
            "RegisterEnemy":source.count(b"RegisterEnemy"),"HarmonyPatch":source.count(b"HarmonyPatch")
        },
        "outputs":[cs_name,il_name]
    })
    dll_path.unlink(missing_ok=True)

(OUT/"VERIFICATION.json").write_text(json.dumps(verification,indent=2)+"\n",encoding="utf-8")
print(json.dumps(verification,indent=2))
