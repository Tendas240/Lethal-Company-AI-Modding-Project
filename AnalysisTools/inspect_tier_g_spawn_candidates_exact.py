#!/usr/bin/env python3
"""Exact full-source capture for Tier-G S1.42AI spawn-owner candidates."""
from __future__ import annotations
import hashlib, json, os, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tier-g-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-g-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "a3844ed8f708b0c5834ba1792ac331b3bc3c8d84"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_g_spawn_candidates_exact.py",
    ".github/workflows/tier-g-spawn-candidates-exact-review.yml",
}
EXPECTED = ({'package': 'XuXiaolan-ImmersiveScrap', 'version': '1.4.2', 'zip_sha256': '35140d4b44fb86722e78f3f0ac59b8147441af95ddf12fcb227dcd29d205616e', 'member': 'plugins/ImmersiveScrap/ImmersiveScrap.dll', 'dll_sha256': '34ab563c0b31be2ff11355607d2f051e473fd03b97ca669761b0bca322fc7443', 'il_sha256': '0409a1197ba8602af7e04dd8a53f9bb7d3a4a97dd80cb0f994f5c1f335ee94ba', 'source_sha256': '32ecbea94db92e370c0d9297857308b7d63745a038b060c87f34f2523289cc13', 'stem': 'ImmersiveScrap-1.4.2'}, {'package': 'FlipMods-TooManyEmotes', 'version': '2.3.17', 'zip_sha256': 'a195a71e9c02c02ab58aa5eecf20ef735424753e6d92da47cf84a88eb8cbf91a', 'member': 'plugins/TooManyEmotes.dll', 'dll_sha256': 'd122e10e6eb942d001607b08f31f315f194ba9367f6437b749841473f5ac9131', 'il_sha256': '5cca9fffb5b08634cecca8d09a2c5a610cc5ea6691a5d02dec4b06a868a0afee', 'source_sha256': '3ae4d6b3180591332da396b9d3a6312c5efbc294686778be0e1ac0436a747c0d', 'stem': 'TooManyEmotes-2.3.17'}, {'package': 'darmuh-darmuhsTerminalStuff', 'version': '3.10.2', 'zip_sha256': 'b22c27a6693201ec37c49f9fe8db85a80c7f3abe67b3abb60b296045dc063ce6', 'member': 'darmuhsTerminalStuff.dll', 'dll_sha256': 'ddb2b92dc1817d77975e079a0ea2c3ac239dbe4d2983e7e8e0cb7b01a88f6020', 'il_sha256': '280947a7f63c6702f46ae6b850b0c98bb7044ed205c120d0cd2b22102fc56a96', 'source_sha256': '3ff945aca2ab99f80b2834b2f4ebcaa6dff5e769650218f93fa6fa398436cba6', 'stem': 'darmuhsTerminalStuff-3.10.2'}, {'package': 'BunyaPineTree-ModelReplacementAPI', 'version': '2.4.20', 'zip_sha256': '27128446ab809293c3a1ce4f88e48b9f9cceaa66b10509562087ba7722f5fb20', 'member': 'ModelReplacementAPI.dll', 'dll_sha256': '0334ebac744b1cf84c53501516e3d1034cf7c39f328fd71861d6261b608fe844', 'il_sha256': '5e27bd4c232be8cfc36d7dde9c8ffd92e7f57311ecb85c985810ddee1bae487d', 'source_sha256': '5bca86a59f25ef003343d6784b753c682990865cb2e54969f21ebce182701bee', 'stem': 'ModelReplacementAPI-2.4.20'}, {'package': 'Beaniebe-Beanie_Lib', 'version': '1.0.9', 'zip_sha256': 'ec96359194b3c3b6384715419373a8d8d24a85043cbf122e27f837314dcd1662', 'member': 'LethalGravityControl.dll', 'dll_sha256': '6d95757edf8e772474979ac191fd188beab9e361434e644d781e7729d2864324', 'il_sha256': '13333d1e4659cc4487ffd7f68491db0aef1bdeb5426a01e4e54e9182897aa35b', 'source_sha256': '4b68f7c306938fef8865ce8e55ee66cf1d240993715d0887d30c938538b82380', 'stem': 'Beanie_Lib-1.0.9'}, {'package': 'mattymatty-LobbyControl', 'version': '2.5.12', 'zip_sha256': '0966822d12c62df0caa10fc69857363413f822a67eff922f80d725467ed9d1f4', 'member': 'BepInEx/plugins/LobbyControl.dll', 'dll_sha256': '78270a61e22fa7a3d8a7120ab7a4e62d7748772fa3f621f8ce66e8631be8d346', 'il_sha256': 'af4e3df01ff1c055276fee1804e6175d1a39e782f979709588ef80f95c7c5b15', 'source_sha256': '70b8f56260d5b83385f5bfb7643e49625a6883e69d29b6e67913961456c98de3', 'stem': 'LobbyControl-2.5.12'}, {'package': 'fumiko-CullFactory', 'version': '2.0.7', 'zip_sha256': '2918e9b97347f62bc28bd1cbc6923b04c2a522d3af50bd4c656da26a00534073', 'member': 'CullFactory.dll', 'dll_sha256': '4bcc863c3b067a8f856d14a43cb828a708bc7090c68ac884fe4f24c59c8ec6bc', 'il_sha256': '399042ddbf520fd44e0f48fe46ec776634811d58c7f8f354eaaf84abd7930f83', 'source_sha256': '7f3a7e499ceb997834cbce5fc467113db1836a26e1ebd99a0458e8fa6d714044', 'stem': 'CullFactory-2.0.7'}, {'package': 'fumiko-CullFactory', 'version': '2.0.7', 'zip_sha256': '2918e9b97347f62bc28bd1cbc6923b04c2a522d3af50bd4c656da26a00534073', 'member': 'CullFactoryBurstPlugin.dll', 'dll_sha256': '578a556b3c088f32ddad8ebcf411ce74a9cf3937d6c889d2e2df09bf6456ea1e', 'il_sha256': 'f95ff93b348904f853bde9c57664fb70a38f03d2bc342e42c075364e88c2c9c8', 'source_sha256': None, 'stem': 'CullFactory-2.0.7-Burst'})

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
    req = urllib.request.Request(url, headers={"User-Agent":"s142ai-tier-g-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data

verify_analysis_branch_delta()
verification = {
    "schema_version":1,
    "purpose":"S1.42AI-DIAG1 Tier-G exact review capture for all seven remaining discovery-positive packages (eight managed DLLs)",
    "canonical_main":CANONICAL_MAIN,
    "repository_commit":os.environ.get("GITHUB_SHA"),
    "discovery_run":DISCOVERY_RUN,
    "discovery_head":DISCOVERY_HEAD,
    "decompiler":{"tool":"ilspycmd","version":ILSPY_VERSION},
    "assemblies":[],
    "qualification":"Complete C#/IL capture of all managed assemblies in the seven remaining discovery-positive packages, with exact ZIP/DLL/IL gates and prior complete-source gates where discovery produced one. Evidence only; no DIAG1 implementation, build, controller transition, Gale import or gameplay authorization."
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
    actual_source=sha256(source)
    if item["source_sha256"] is not None and actual_source != item["source_sha256"]:
        raise RuntimeError(f"Discovery source SHA mismatch for {item['member']}: {actual_source}")
    cs_name=item["stem"]+".cs"; il_name=item["stem"]+".il"
    (OUT/cs_name).write_bytes(source); (OUT/il_name).write_bytes(il)
    verification["assemblies"].append({
        "package":item["package"],"version":item["version"],"package_zip_sha256":actual_zip,
        "member":item["member"],"dll_sha256":actual_dll,
        "source_sha256":actual_source,"source_sha256_prior_gate":item["source_sha256"],
        "source_bytes":len(source),"source_lines":len(source.decode("utf-8",errors="replace").splitlines()),
        "il_sha256":actual_il,"il_bytes":len(il),"il_lines":len(il.decode("utf-8",errors="replace").splitlines()),
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
