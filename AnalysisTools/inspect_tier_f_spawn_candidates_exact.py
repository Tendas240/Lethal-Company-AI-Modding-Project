#!/usr/bin/env python3
"""Exact full-source capture for Tier-F S1.42AI spawn-owner candidates."""
from __future__ import annotations
import hashlib, json, os, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tier-f-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-f-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = '2eac9f13eeadeb37989f397afa0e07d7c03a01fe'
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_f_spawn_candidates_exact.py",
    ".github/workflows/tier-f-spawn-candidates-exact-review.yml",
}
EXPECTED = ({'package': 'zealsprince-Locker', 'version': '1.6.3', 'zip_sha256': '3311242edb634841aacf9977185d42d4077d6c28c8bec9e6381fac729ed0b61c', 'member': 'Locker.dll', 'dll_sha256': 'b8ab49f52e3d3cb9f7d9c7cdbca191559de84bd11df5a458669393a78d1e424d', 'il_sha256': '25b006b8acd875797e5fe545dbaf8dcccf629adf595ea59fee0808cf14d4f8b1', 'source_sha256': 'bdc94c00806d2223e6b87c5cef0322fc413ae88cf6e3dfdaffb472c23106730f', 'stem': 'Locker-1.6.3'}, {'package': 'Cabinet_crew-TheCabinet', 'version': '1.12.1', 'zip_sha256': '7376507414dad60a25caa50977f34a43b5639cfe0fa5fa810f12b45be057361d', 'member': 'plugins/TheCabinet/VectorV.TheCabinet.dll', 'dll_sha256': 'c3effc72f5c845437998bf4e5765d2a7474f5ef99196eda9b41d0b50dc5ef134', 'il_sha256': '40ecf6f3b75216ed0d855abe2c9e1a74a42ba16be7f2460f95db9669762e7864', 'source_sha256': '0bedfe8ec64b0a39090f6abf45d8ecfbdc79d5d5c18f29acc38db0087dc34f4f', 'stem': 'TheCabinet-1.12.1'}, {'package': 'Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior', 'version': '3.4.4', 'zip_sha256': '12921825bee51bfd46582989322a1f31183b65f59293c73654a102fb68d068b7', 'member': 'BepInEx/plugins/BlackMesa.dll', 'dll_sha256': 'a90f157becdc68ab7fe6898eefc2feaee98352a0f04b2cda414741729a048eef', 'il_sha256': '5ecbfe20d57ff3927ca844726dee9fc4e0eafae2ddca781ea0e8d67d555ba362', 'source_sha256': 'c7f18a074701a8b5bd41f8576cd6fcd83e736262f2ff87b8368c1a2bcc6cb376', 'stem': 'BlackMesa-3.4.4'}, {'package': 'NotezyTeam-EnemyHealthBars', 'version': '1.4.0', 'zip_sha256': '5fa0bec01e4a94595a280eecd2628a2c0bfe3dacba6be0e879d50478b2ded9d6', 'member': 'NoteBoxz.EnemyHealthBars.dll', 'dll_sha256': '908095cee2d95e3c0cfcb11889d3fbd153cabb55e0578277eb69dac04c778bcc', 'il_sha256': 'acd63d39f26849c2bd29b8a985489c51a1bdcc2514052774e197630b0c670741', 'source_sha256': '468a31ea8390433167755965bbab8142822cac11b14505e891aa57d393625079', 'stem': 'EnemyHealthBars-1.4.0'}, {'package': 'DiggC-CruiserImproved', 'version': '1.6.3', 'zip_sha256': 'a0e40bbe0f7fbb156694960396ea03321511b3149007fc7d9fb09ba5b4d815dc', 'member': 'BepInEx/plugins/CruiserImproved/DiggC.CruiserImproved.dll', 'dll_sha256': 'b161c2f87431e9265d6b909728157e52bfdbbfaa1f707ac2306ebd21aa3eef1e', 'il_sha256': '9c34778c649fdcb03f589103274afa7125a215f82fa4a7421cccb4486507f02f', 'source_sha256': 'cd43cf6d8b914201e8c2559ba8e3c6e8b7255bc37fe6f0b01644405d7784c117', 'stem': 'CruiserImproved-1.6.3'}, {'package': 'Zaggy1024-OpenBodyCams', 'version': '3.0.12', 'zip_sha256': '4e4da7b1775e9b1fb0049f42c05c486f27f4413f0929b2ec8cd17986f0f4e2b5', 'member': 'OpenBodyCams.dll', 'dll_sha256': '24bfe62ca0e76e4bc08366c92264fea02a8bc7f44f0fff23d570e061e1c1b3be', 'il_sha256': '0e4ce66a93a6e2ba7211e6e99258ad423c049f2e2f3323df21f9036422813784', 'source_sha256': '8d2d0ff886698fb1ce83777647aa74037e2147ad1cc7118aca8f8da60f9b0068', 'stem': 'OpenBodyCams-3.0.12'})

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
    req = urllib.request.Request(url, headers={"User-Agent":"s142ai-tier-f-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data

verify_analysis_branch_delta()
verification = {
    "schema_version":1,
    "purpose":"S1.42AI-DIAG1 Tier-F exact review capture for six prioritized remaining discovery-positive packages (six managed DLLs)",
    "canonical_main":CANONICAL_MAIN,
    "repository_commit":os.environ.get("GITHUB_SHA"),
    "discovery_run":DISCOVERY_RUN,
    "discovery_head":DISCOVERY_HEAD,
    "decompiler":{"tool":"ilspycmd","version":ILSPY_VERSION},
    "assemblies":[],
    "qualification":"Complete C#/IL decompile of six ZIP/DLL/discovery-source/discovery-IL anchored assemblies from six packages. Evidence only; no DIAG1 implementation, build, controller transition, Gale import or gameplay authorization."
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
    if actual_source != item["source_sha256"]:
        raise RuntimeError(f"Discovery source SHA mismatch for {item['member']}: {actual_source}")
    cs_name=item["stem"]+".cs"; il_name=item["stem"]+".il"
    (OUT/cs_name).write_bytes(source); (OUT/il_name).write_bytes(il)
    verification["assemblies"].append({
        "package":item["package"],"version":item["version"],"package_zip_sha256":actual_zip,
        "member":item["member"],"dll_sha256":actual_dll,
        "source_sha256":actual_source,"source_bytes":len(source),
        "source_lines":len(source.decode("utf-8",errors="replace").splitlines()),
        "il_sha256":actual_il,"il_bytes":len(il),
        "il_lines":len(il.decode("utf-8",errors="replace").splitlines()),
        "source_occurrences":{
            "EnemyAI":source.count(b"EnemyAI"),"EnemyType":source.count(b"EnemyType"),
            "enemyPrefab":source.count(b"enemyPrefab"),"Instantiate":source.count(b"Instantiate"),
            "NetworkObject":source.count(b"NetworkObject"),"SpawnEnemyOnServer":source.count(b"SpawnEnemyOnServer"),
            "SpawnEnemyGameObject":source.count(b"SpawnEnemyGameObject"),"EnemyVent":source.count(b"EnemyVent"),
            "SpawnableEnemyWithRarity":source.count(b"SpawnableEnemyWithRarity"),
            "RegisterEnemy":source.count(b"RegisterEnemy"),"RegisterNetworkPrefab":source.count(b"RegisterNetworkPrefab"),
            "HarmonyPatch":source.count(b"HarmonyPatch"),"RoundManager":source.count(b"RoundManager"),
            "SpawnedEnemies":source.count(b"SpawnedEnemies")
        },
        "outputs":[cs_name,il_name]
    })
    dll_path.unlink(missing_ok=True)

(OUT/"VERIFICATION.json").write_text(json.dumps(verification,indent=2)+"\n",encoding="utf-8")
print(json.dumps(verification,indent=2))
