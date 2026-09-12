#!/usr/bin/env python3
"""Exact full-source capture for the ten direct SpawnEnemyGameObject candidates
from S1.42AI remaining-package discovery run 34705334804.

Read-only patch-safety evidence generation. Re-download exact Thunderstore package
versions, fail closed on ZIP/DLL/source hash drift, and preserve complete C#/IL for
method/caller/state review. No profile/build/runtime mutation.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "direct-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-direct-spawn-candidates-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024

EXPECTED = (
    {"package": "Zigzag-PremiumScraps", "version": "2.5.0", "zip_sha256": "5004b52dd80f31d436cebaedddfc72de31ae6406cb3eeccb40485cc61d29b602", "member": "plugins/PremiumScraps.dll", "dll_sha256": "380ffa37ff53576f561c27a9d06c30ecd35d9195606e142122647a0df583bf96", "source_sha256": "78baada0c26f265fc3185348ce4be90b981f0b2b3d6e19580539532fd642fac4", "stem": "PremiumScraps-2.5.0"},
    {"package": "Zigzag-ChillaxScraps", "version": "1.6.6", "zip_sha256": "dba051732612189f6317d6ae6dbcbb52011241aa771361ae4d13f34dbb052b79", "member": "ChillaxScraps/ChillaxScraps.dll", "dll_sha256": "1a448aaf93af58da00f16e7e7acf0c7e69b1bb564f084dc64020d06101bbb7d0", "source_sha256": "cd320fdf6fc9bc7d2f10282ab7cd46cd079fb8cd2bdd155a4f9bb187c0cd2f32", "stem": "ChillaxScraps-1.6.6"},
    {"package": "rectorado-KenjiLib", "version": "0.7.0", "zip_sha256": "af37ae5f1bec456943b8961cbf4304157cc3192c4077acfeaf26128e5d92bb71", "member": "KenjiLib.dll", "dll_sha256": "3425ef267033ade207e7fb75bd9274ef4433a907e507a981c85b4050f550cccd", "source_sha256": "1c30443a0eb72980f31abef9b73eff86440fbfb953926064cf34d433d0a3cd4a", "stem": "KenjiLib-0.7.0"},
    {"package": "pacoito-itolib", "version": "0.9.3", "zip_sha256": "d4f30087aeae04963a20e8f2decff7f3c2446d35a1df5989f77069e51cb00f11", "member": "BepInEx/plugins/itolib.dll", "dll_sha256": "f454dcb67041914124f0f3ee415282b078409bb413ef51e3e9639a9d8dcb07d6", "source_sha256": "b03d294bb202b502c3ae33094c869e765fc15bd5c8ba729c7a2d58b19121fb51", "stem": "itolib-0.9.3"},
    {"package": "notnotnotswipez-MoreCompany", "version": "1.14.0", "zip_sha256": "dba111a2744478ce927cf2493ace871214c11339f3a6768bdc552b1d5554a1dc", "member": "BepInEx/plugins/MoreCompany.dll", "dll_sha256": "d1947db8908fdf5b2d20a3e40c571099c656f6880434594e6997b20ec57b7fd7", "source_sha256": "4eb4c63fd12a85108b31fa90290955bfabda06640d384ac862fda1af56a47cbd", "stem": "MoreCompany-1.14.0"},
    {"package": "lethal_coder-31Arcadia_UPDATED", "version": "1.0.2", "zip_sha256": "287c00db1c9829251f7805c682f659521e7933cafb498c43bd9e26a9884e9ee6", "member": "ArcadiaMoonPlugin.dll", "dll_sha256": "c71866c7a2e4a0e1f2af1eb392aa41a428e584753f263ddc50efa8d7e75af4a0", "source_sha256": "7ef9eacc421c6d2c6dd89c85cddea4eb170b88aff5acb5543cdece4e4c920dfd", "stem": "ArcadiaMoonPlugin-1.0.2"},
    {"package": "Kittenji-Herobrine", "version": "1.3.9", "zip_sha256": "ad01126dc687b1ae72dc36aff026eee6d8159396b95904eadf28168ff7de332e", "member": "BepInEx/plugins/HerobrineMod.dll", "dll_sha256": "d4d7f4fa19ef1a9ceb0b1ef5b7108f39001e834deefc2247feb5af458211524e", "source_sha256": "80116b6e7ee8bae34dd638dcdb9e1fb7aafe8b8e302377b5529ac3ea00e05ecb", "stem": "Herobrine-1.3.9"},
    {"package": "Kittenji-Football", "version": "1.1.14", "zip_sha256": "d12933f4795923e483960a835bcb0fae525f351f71d7db1e45e3a3e82e4492f2", "member": "BepInEx/plugins/FootballEntity.dll", "dll_sha256": "7add08cb69f0d1d0ea83c229f23a44e1918d4753281b0117c768955beda02044", "source_sha256": "fb318ff8d319e3e9185c35c6d63c15116ef5ea41642d9db9e56582e7fea151f8", "stem": "Football-1.1.14"},
    {"package": "JacobG5-JLL", "version": "1.10.1", "zip_sha256": "3fdd0ab7503890b0a12ecac2331c460fed3a3777ede0d30b27510fcf12636f45", "member": "BepInEx/plugins/JLL/JLL.dll", "dll_sha256": "bbe20f86805f8cb90cf8c88893b27b664d39ea79107edc826e1089f0ac473f5a", "source_sha256": "e72ba7929dae63e07127a88e6029a12b89935d8a81edb03c671151ab792ad77a", "stem": "JLL-1.10.1"},
    {"package": "super_fucking_cool_and_badass_team-Biodiversity", "version": "0.2.9", "zip_sha256": "fcb2a5160a75b82c0410b69d30cc610145abe9f6d32bbf3053c5c44c1ad214a1", "member": "BepInEx/plugins/Biodiversity/com.github.biodiversitylc.Biodiversity.dll", "dll_sha256": "6853a6430674721ffbc6ab13de0e85b2f921f05339bf33f167e8f391debf9f28", "source_sha256": "d9fdd09370586c0b1eea1c5b3eaf6adc6b81a689e448c98844658ed447c4f306", "stem": "Biodiversity-0.2.9"},
)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run(args: list[str]) -> tuple[bytes, bytes]:
    result = subprocess.run(args, capture_output=True, timeout=360)
    if result.returncode:
        raise RuntimeError(
            f"{args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", errors="replace")[-4000:]
        )
    if len(result.stdout) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"Decompiler output exceeded bounded {MAX_OUTPUT_BYTES} bytes")
    return result.stdout, result.stderr

def download(url: str, path: Path) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent":"s142ai-direct-spawn-exact/1"})
    with urllib.request.urlopen(request, timeout=180) as response:
        data = response.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data

verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact review capture for ten direct RoundManager.SpawnEnemyGameObject discovery candidates",
    "repository_commit": os.environ.get("GITHUB_SHA"),
    "discovery_run": DISCOVERY_RUN,
    "discovery_head": DISCOVERY_HEAD,
    "decompiler": {"tool":"ilspycmd","version":ILSPY_VERSION},
    "assemblies": [],
    "qualification": (
        "Complete C#/IL decompile of exactly ten SHA-anchored DLLs that the prior "
        "discovery classified as direct RoundManager.SpawnEnemyGameObject candidates. "
        "This evidence is for method/caller/state/lifecycle review only and does not "
        "authorize S1.42AI-DIAG1 implementation, build, controller transition, or gameplay."
    ),
}

cache = {}
for item in EXPECTED:
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{item['package']}-{item['version']}.zip"
    if url not in cache:
        zip_path = WORK / (item["package"] + "-" + item["version"] + ".zip")
        package_bytes = download(url, zip_path)
        actual_zip = sha256(package_bytes)
        if actual_zip != item["zip_sha256"]:
            raise RuntimeError(f"ZIP SHA mismatch for {item['package']}: {actual_zip}")
        cache[url] = (zip_path, package_bytes)
    zip_path, package_bytes = cache[url]
    with zipfile.ZipFile(zip_path) as archive:
        if item["member"] not in archive.namelist():
            raise RuntimeError("Exact DLL member missing: " + item["member"])
        dll_bytes = archive.read(item["member"])
    actual_dll = sha256(dll_bytes)
    if actual_dll != item["dll_sha256"]:
        raise RuntimeError(f"DLL SHA mismatch for {item['member']}: {actual_dll}")
    dll_path = WORK / (item["stem"] + ".dll")
    dll_path.write_bytes(dll_bytes)
    source, source_stderr = run(["ilspycmd", str(dll_path)])
    actual_source = sha256(source)
    if actual_source != item["source_sha256"]:
        raise RuntimeError(
            f"Source SHA mismatch for {item['member']}: {actual_source}; "
            "refusing review against bytes/decompile different from discovery"
        )
    il, il_stderr = run(["ilspycmd", "-il", str(dll_path)])
    cs_name = item["stem"] + ".cs"
    il_name = item["stem"] + ".il"
    (OUT / cs_name).write_bytes(source)
    (OUT / il_name).write_bytes(il)
    verification["assemblies"].append({
        "package": item["package"],
        "version": item["version"],
        "package_zip_sha256": sha256(package_bytes),
        "member": item["member"],
        "dll_sha256": actual_dll,
        "source_sha256": actual_source,
        "source_bytes": len(source),
        "source_lines": len(source.decode("utf-8", errors="replace").splitlines()),
        "il_sha256": sha256(il),
        "il_bytes": len(il),
        "il_lines": len(il.decode("utf-8", errors="replace").splitlines()),
        "spawn_enemy_game_object_source_occurrences": source.count(b"SpawnEnemyGameObject"),
        "spawn_enemy_game_object_il_occurrences": il.count(b"SpawnEnemyGameObject"),
        "source_stderr": source_stderr.decode("utf-8", errors="replace")[-4000:],
        "il_stderr": il_stderr.decode("utf-8", errors="replace")[-4000:],
        "outputs": [cs_name, il_name],
    })
    dll_path.unlink(missing_ok=True)

(OUT / "VERIFICATION.json").write_text(
    json.dumps(verification, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(verification, indent=2))
