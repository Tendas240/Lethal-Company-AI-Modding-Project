#!/usr/bin/env python3
"""Exact full-source capture for the six strongest remaining S1.42AI spawn-owner candidates.

Read-only patch-safety evidence generation. Re-downloads the exact Thunderstore
versions, verifies package/DLL/source hashes from discovery run 34705334804,
and preserves complete C#/IL for method/caller/state/lifecycle review.
No profile, build controller, runtime controller, or gameplay state is changed.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tier-d-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-d-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "ae1a4693d23e41fce6674380f6ff83631b0a1eb3"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_d_spawn_candidates_exact.py",
    ".github/workflows/tier-d-spawn-candidates-exact-review.yml",
}

EXPECTED = ({'package': 'ButteryStancakes-ButteryFixes', 'version': '1.17.16', 'zip_sha256': '17869badc6286b64f032fe3e393c9269ea6f9c716d50a581d8cc15f747ffcdad', 'member': 'ButteryFixes.dll', 'dll_sha256': '8526a6721e42c03093ff3b1dbf924cc849ef3bed73920edc73a68a7d749d5fed', 'source_sha256': '3b3df2fcb8198a2158708735026beb53eab7f4912375295f56c20a002a18a166', 'stem': 'ButteryFixes-1.17.16'}, {'package': 'Evaisa-LethalLib', 'version': '1.2.0', 'zip_sha256': 'ba013e1282c503c2b1170eefaee0a770fc031485f28dea40da32a4bdbbffb180', 'member': 'plugins/LethalLib/LethalLib.dll', 'dll_sha256': '28fde57d12bf14222c916d81fbc9995608639857f3c5e9dd712dd6424efa45bc', 'source_sha256': '241e498107d55c979590889a024fe2756e12338a63e5124c9365d56034ebd7cd', 'stem': 'LethalLib-1.2.0'}, {'package': 'TestAccount666-ShipWindows', 'version': '2.11.1', 'zip_sha256': 'c93ca093b3ce3fa3898aa7f5560dd5f2865e20709a08a3dc8cdb13737904bbeb', 'member': 'ShipWindows.dll', 'dll_sha256': 'ddf7ec1e426a512a0fa0d1da17f18c03b8b28faddf08e7e90633909f6b2d0ea7', 'source_sha256': '64208922699edc0662bfbaa2e9d0d7449a4e5ca85ea1016c8a9aad61f8c88439', 'stem': 'ShipWindows-2.11.1'}, {'package': 'WhiteSpike-Interactive_Terminal_API', 'version': '1.3.3', 'zip_sha256': 'dcb969e1ea831a4c3e56320f7f395eea875a9d41d47f4e355529d8bb516f277c', 'member': 'BepInEx/plugins/InteractiveTerminalAPI/InteractiveTerminalAPI.dll', 'dll_sha256': '981c2874ab1af36b06b5ca18a171d521f1d25694fce7764cfa1058da03c4ff77', 'source_sha256': '7987671896805623c023d3a868e79d21fd6b7ab23147e66ce81460636580b793', 'stem': 'InteractiveTerminalAPI-1.3.3'}, {'package': 'Zehs-SellMyScrap', 'version': '1.15.3', 'zip_sha256': '417afce368c7f2ee6ac69ffca64869f5c080a473b1e68dbf05a09c7040385ec6', 'member': 'com.github.zehsteam.SellMyScrap.dll', 'dll_sha256': '1a27500f4e1c683f569325ceeea7a780506be96a935275407c5a881dfc95800d', 'source_sha256': '2706c01c44762e0976b42b2189637d8ef8fcbab201637b7c957bd61b1cae914e', 'stem': 'SellMyScrap-1.15.3'}, {'package': 'Zehs-SellMyScrap', 'version': '1.15.3', 'zip_sha256': '417afce368c7f2ee6ac69ffca64869f5c080a473b1e68dbf05a09c7040385ec6', 'member': 'com.github.zehsteam.SellMyScrap.v40-v72.dll', 'dll_sha256': '0ab886b906c58768af2d8601745b75591e49aec606bf1b8f528122dcc2de89a8', 'source_sha256': '900305b96b4dc270ba274e1ddd9cac89b7abda33da95fa15d085283f20bb15e9', 'stem': 'SellMyScrap-v40-v72-1.15.3'}, {'package': 'mr_hat-MisideItems', 'version': '0.3.9', 'zip_sha256': '7664afa307e7a8e61455f50b4c96ede301bee54f3f2eb70660067b0e6ffaaa84', 'member': 'BepInEx/plugins/MisideItems.dll', 'dll_sha256': '5c15c3c8f53705a4f75c2299f0ebf6b44a6934f54a2d3fbf06873a1d5f2102fa', 'source_sha256': '5da3e90b4d6be41b09ccaf9423816d245f6e9440fe6cf6bbcc17118e874a8e06', 'stem': 'MisideItems-0.3.9'})

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

def run(args: list[str]) -> tuple[bytes,bytes]:
    p = subprocess.run(args, capture_output=True, timeout=420)
    if p.returncode:
        raise RuntimeError(f"{args[0]} failed ({p.returncode}): " + p.stderr.decode("utf-8",errors="replace")[-4000:])
    if len(p.stdout) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"Decompiler output exceeded bounded {MAX_OUTPUT_BYTES} bytes")
    return p.stdout, p.stderr

def download(url: str, path: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent":"s142ai-tier-d-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data

verify_analysis_branch_delta()
verification = {
    "schema_version":1,
    "purpose":"S1.42AI-DIAG1 exact review capture for the six strongest remaining discovery-positive packages (seven DLLs)",
    "canonical_main":CANONICAL_MAIN,
    "repository_commit":os.environ.get("GITHUB_SHA"),
    "discovery_run":DISCOVERY_RUN,
    "discovery_head":DISCOVERY_HEAD,
    "decompiler":{"tool":"ilspycmd","version":ILSPY_VERSION},
    "assemblies":[],
    "qualification":"Complete C#/IL decompile of seven ZIP/DLL/source-SHA-anchored assemblies from six packages. Evidence only; no DIAG1 implementation, build, controller transition, Gale import or gameplay authorization."
}
cache = {}
for item in EXPECTED:
    key = (item["package"], item["version"])
    if key not in cache:
        url=f"https://gcdn.thunderstore.io/live/repository/packages/{item['package']}-{item['version']}.zip"
        zp=WORK/(item["package"]+"-"+item["version"]+".zip")
        package_bytes=download(url,zp)
        actual_zip=sha256(package_bytes)
        if actual_zip != item["zip_sha256"]:
            raise RuntimeError(f"ZIP SHA mismatch for {item['package']}: {actual_zip}")
        cache[key]=(zp,actual_zip)
    zip_path, actual_zip = cache[key]
    with zipfile.ZipFile(zip_path) as archive:
        if item["member"] not in archive.namelist():
            raise RuntimeError("Exact DLL member missing: " + item["member"])
        dll_bytes=archive.read(item["member"])
    actual_dll=sha256(dll_bytes)
    if actual_dll != item["dll_sha256"]:
        raise RuntimeError(f"DLL SHA mismatch for {item['member']}: {actual_dll}")
    dll_path=WORK/(item["stem"]+".dll")
    dll_path.write_bytes(dll_bytes)
    source, source_stderr=run(["ilspycmd",str(dll_path)])
    actual_source=sha256(source)
    if actual_source != item["source_sha256"]:
        raise RuntimeError(f"Source SHA mismatch for {item['member']}: {actual_source}")
    il, il_stderr=run(["ilspycmd","-il",str(dll_path)])
    cs_name=item["stem"]+".cs"; il_name=item["stem"]+".il"
    (OUT/cs_name).write_bytes(source); (OUT/il_name).write_bytes(il)
    verification["assemblies"].append({
        "package":item["package"],"version":item["version"],
        "package_zip_sha256":actual_zip,"member":item["member"],
        "dll_sha256":actual_dll,"source_sha256":actual_source,
        "source_bytes":len(source),"source_lines":len(source.decode("utf-8",errors="replace").splitlines()),
        "il_sha256":sha256(il),"il_bytes":len(il),"il_lines":len(il.decode("utf-8",errors="replace").splitlines()),
        "source_occurrences":{
            "EnemyAI":source.count(b"EnemyAI"),"EnemyType":source.count(b"EnemyType"),
            "enemyPrefab":source.count(b"enemyPrefab"),"Instantiate":source.count(b"Instantiate"),
            "NetworkObject":source.count(b"NetworkObject"),"SpawnEnemyOnServer":source.count(b"SpawnEnemyOnServer"),
            "SpawnEnemyGameObject":source.count(b"SpawnEnemyGameObject"),"EnemyVent":source.count(b"EnemyVent"),
            "RegisterEnemy":source.count(b"RegisterEnemy"),"HarmonyPatch":source.count(b"HarmonyPatch")
        },
        "source_stderr":source_stderr.decode("utf-8",errors="replace")[-4000:],
        "il_stderr":il_stderr.decode("utf-8",errors="replace")[-4000:],
        "outputs":[cs_name,il_name]
    })
    dll_path.unlink(missing_ok=True)

(OUT/"VERIFICATION.json").write_text(json.dumps(verification,indent=2)+"\n",encoding="utf-8")
print(json.dumps(verification,indent=2))
