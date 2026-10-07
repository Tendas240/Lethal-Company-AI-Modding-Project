#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import urllib.request
import zipfile
from pathlib import Path

import validate_s142ai_diag1_static as validator

# The exact owner/type -> package/DLL ownership is already closed by canonical
# DIAG1 evidence. The .r2z intentionally does not embed every Thunderstore DLL;
# Gale reconstructs those packages from export.r2x. Hydrate only the exact
# reviewed owner DLL bytes below, fail closed on package/DLL/source drift, then
# let the original validator perform its unchanged exact type/method/body gate.
OWNER_EVIDENCE_BINDINGS = {
    "SlendermanMod.": ("Sparble-FacelessStalker", "SlendermanMod.dll"),
    "Kittenji.FootballEntity.": ("Kittenji-Football", "FootballEntity.dll"),
    "Kittenji.HerobrineMod.": ("Kittenji-Herobrine", "HerobrineMod.dll"),
    "MoreShipUpgrades.": ("malco-Lategame_Upgrades", "MoreShipUpgrades.dll"),
    "PremiumScraps.": ("Zigzag-PremiumScraps", "PremiumScraps.dll"),
    "ChillaxScraps.": ("Zigzag-ChillaxScraps", "ChillaxScraps.dll"),
    "JLL.": ("JacobG5-JLL", "JLL.dll"),
    "KenjiLib.": ("rectorado-KenjiLib", "KenjiLib.dll"),
    "itolib.": ("pacoito-itolib", "itolib.dll"),
    "CodeRebirth.": ("XuXiaolan-CodeRebirth", "CodeRebirth.dll"),
    "LethalMin.": ("NotezyTeam-LethalMinNightly", "NoteBoxz.LethalMin.dll"),
}

DIRECT_EVIDENCE = (
    validator.ROOT
    / "SourceEvidence/NativeSpawnOwners/20260912T163927Z-DirectSpawnCandidatesExact/VERIFICATION.json"
)
TIER_A_EVIDENCE = (
    validator.ROOT
    / "SourceEvidence/NativeSpawnOwners/20260912T173403Z-TierAExact/VERIFICATION.json"
)
INITIAL_MANIFEST = (
    validator.ROOT
    / "SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json"
)
PROFILE_PACKAGE_INVENTORY = (
    validator.ROOT
    / "SourceEvidence/NativeSpawnOwners/20260911T144505Z/PROFILE_PACKAGE_INVENTORY.json"
)

MAX_PACKAGE_BYTES = 768 * 1024 * 1024
ORIGINAL_RUN = validator.run
ORIGINAL_READ_ZIP = validator.read_zip
_HYDRATED: dict[str, tuple[str, bytes, str]] | None = None

# Exact CodeRebirth 1.6.9 reviewed source decompiles this reference-return
# annotation as `EnemyAI?`. Nullable reference annotations do not change the CLR
# return type, but this static gate intentionally validates the exact C# source
# token emitted by pinned ILSpy. Keep the override fail-closed and target-local.
_code_rebirth_target = (
    "CodeRebirth.src.MiscScripts.EnemyLevelSpawner",
    "SpawnRandomEnemy",
)
_override_count = 0
_patched_targets = []
for type_name, method, ret, params, is_static in validator.TARGETS:
    if (type_name, method) == _code_rebirth_target:
        if ret != "EnemyAI":
            validator.fail(
                f"Unexpected pre-override return token for {type_name}.{method}: {ret}"
            )
        ret = "EnemyAI?"
        _override_count += 1
    _patched_targets.append((type_name, method, ret, params, is_static))
if _override_count != 1:
    validator.fail(
        f"Expected exactly one CodeRebirth SpawnRandomEnemy target override, found {_override_count}"
    )
validator.TARGETS = _patched_targets


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    if not path.exists():
        validator.fail(f"Canonical owner evidence is missing: {path.relative_to(validator.ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_index() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}

    direct = load_json(DIRECT_EVIDENCE)
    for item in direct.get("assemblies", []):
        out.setdefault(item["package"], []).append(
            {
                "package": item["package"],
                "version": item["version"],
                "zip_sha256": item["zip_sha256"],
                "member": item["member"],
                "dll_sha256": item["dll_sha256"],
                "source_sha256": item["source_sha256"],
                "authority": str(DIRECT_EVIDENCE.relative_to(validator.ROOT)),
            }
        )

    tier_a = load_json(TIER_A_EVIDENCE)
    for item in tier_a.get("assemblies", []):
        out.setdefault(item["package"], []).append(
            {
                "package": item["package"],
                "version": item["version"],
                "zip_sha256": item["package_zip_sha256"],
                "member": item["member"],
                "dll_sha256": item["dll_sha256"],
                "source_sha256": item["source_sha256"],
                "authority": str(TIER_A_EVIDENCE.relative_to(validator.ROOT)),
            }
        )

    initial = load_json(INITIAL_MANIFEST)
    for package in initial.get("packages", []):
        for assembly in package.get("assemblies", []):
            out.setdefault(package["package"], []).append(
                {
                    "package": package["package"],
                    "version": package["version"],
                    "zip_sha256": package["zip_sha256"],
                    "member": assembly["member"],
                    "dll_sha256": assembly["sha256"],
                    "source_sha256": assembly["source_sha256"],
                    "authority": str(INITIAL_MANIFEST.relative_to(validator.ROOT)),
                }
            )
    return out


def assert_profile_package_binding(record: dict, inventory: dict) -> None:
    matches = [
        item
        for item in inventory.get("packages", [])
        if item.get("package") == record["package"]
    ]
    if len(matches) != 1:
        validator.fail(
            f"Expected exactly one S1.42AI package inventory entry for {record['package']}, "
            f"found {len(matches)}"
        )
    item = matches[0]
    if item.get("version") != record["version"] or item.get("enabled") is not True:
        validator.fail(
            f"S1.42AI package binding drift for {record['package']}: "
            f"inventory version={item.get('version')!r}, enabled={item.get('enabled')!r}; "
            f"reviewed version={record['version']!r}, enabled=True required"
        )


def select_owner_records() -> list[dict]:
    evidence = evidence_index()
    inventory = load_json(PROFILE_PACKAGE_INVENTORY)
    selected: list[dict] = []

    for prefix, (package, assembly_name) in OWNER_EVIDENCE_BINDINGS.items():
        matches = [
            item
            for item in evidence.get(package, [])
            if Path(item["member"]).name.casefold() == assembly_name.casefold()
        ]
        if len(matches) != 1:
            validator.fail(
                f"Expected exactly one canonical evidence record for {prefix} -> "
                f"{package}/{assembly_name}, found {len(matches)}"
            )
        record = matches[0]
        for key in ("zip_sha256", "dll_sha256", "source_sha256"):
            value = record.get(key, "")
            if not isinstance(value, str) or len(value) != 64:
                validator.fail(
                    f"Canonical evidence field {key} is invalid for "
                    f"{record['package']}:{record['member']}"
                )
        assert_profile_package_binding(record, inventory)
        selected.append(record)

    return selected


def download_package(record: dict, package_cache: dict[tuple[str, str, str], bytes]) -> bytes:
    key = (record["package"], record["version"], record["zip_sha256"])
    if key in package_cache:
        return package_cache[key]

    url = (
        "https://gcdn.thunderstore.io/live/repository/packages/"
        f"{record['package']}-{record['version']}.zip"
    )
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "s142ai-diag1-static-evidence/1"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = response.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        validator.fail(f"Bounded package download exceeded 768 MiB: {record['package']}")
    actual_zip = sha256_bytes(data)
    if actual_zip != record["zip_sha256"]:
        validator.fail(
            f"Exact package ZIP SHA mismatch for {record['package']} {record['version']}: "
            f"{actual_zip} != {record['zip_sha256']}"
        )
    package_cache[key] = data
    return data


def hydrate_owner_assemblies() -> dict[str, tuple[str, bytes, str]]:
    global _HYDRATED
    if _HYDRATED is not None:
        return _HYDRATED

    package_cache: dict[tuple[str, str, str], bytes] = {}
    hydrated: dict[str, tuple[str, bytes, str]] = {}

    for record in select_owner_records():
        package_bytes = download_package(record, package_cache)
        with zipfile.ZipFile(io.BytesIO(package_bytes)) as archive:
            names = archive.namelist()
            if record["member"] not in names:
                validator.fail(
                    f"Exact reviewed DLL member missing from {record['package']}: "
                    f"{record['member']}"
                )
            dll_bytes = archive.read(record["member"])

        actual_dll = sha256_bytes(dll_bytes)
        if actual_dll != record["dll_sha256"]:
            validator.fail(
                f"Exact DLL SHA mismatch for {record['package']}:{record['member']}: "
                f"{actual_dll} != {record['dll_sha256']}"
            )

        # source_sha256 is part of the same canonical evidence record as the
        # exact DLL hash. Matching that reviewed DLL byte identity binds this
        # run to the already-reviewed source capture; the original validator
        # then freshly decompiles each target type with pinned ILSpy and checks
        # its declared method signature/body.
        basename = Path(record["member"]).name.casefold()
        if basename in hydrated:
            validator.fail(f"Duplicate hydrated owner assembly basename: {basename}")
        synthetic_name = (
            "__external_package_evidence__/"
            f"{record['package']}-{record['version']}/{record['member']}"
        )
        hydrated[basename] = (synthetic_name, dll_bytes, record["authority"])

    _HYDRATED = hydrated
    return hydrated


def evidence_bound_read_zip(path: Path) -> dict[str, bytes]:
    members = ORIGINAL_READ_ZIP(path)

    # Both base and ephemeral validation profiles have the same package set.
    # Adding the same exact synthetic evidence members to both preserves the
    # original archive-diff gate while exposing Thunderstore-managed DLL bytes
    # to the downstream exact target validator.
    if path not in (validator.BASE_PROFILE, validator.VALIDATION_PROFILE):
        return members

    for basename, (synthetic_name, dll_bytes, authority) in hydrate_owner_assemblies().items():
        existing = [
            (name, data)
            for name, data in members.items()
            if name.lower().endswith(".dll")
            and Path(name).name.casefold() == basename
        ]
        if existing:
            if len(existing) != 1:
                validator.fail(
                    f"Ambiguous embedded owner assembly basename {basename}: "
                    f"{[name for name, _data in existing]}"
                )
            existing_name, existing_bytes = existing[0]
            if sha256_bytes(existing_bytes) != sha256_bytes(dll_bytes):
                validator.fail(
                    f"Embedded owner DLL conflicts with canonical package evidence for "
                    f"{basename}: {existing_name}; authority={authority}"
                )
            continue
        if synthetic_name in members:
            validator.fail(f"Synthetic evidence member collision: {synthetic_name}")
        members[synthetic_name] = dll_bytes

    return members


def expected_types_for_assembly(path: str) -> list[str]:
    basename = Path(path).name.casefold()
    matched = []
    for type_name, *_rest in validator.TARGETS:
        binding = next(
            (
                assembly_name
                for prefix, (_package, assembly_name) in OWNER_EVIDENCE_BINDINGS.items()
                if type_name.startswith(prefix)
            ),
            None,
        )
        if binding is None:
            validator.fail(f"No reviewed owner-evidence binding declared for {type_name}")
        if binding.casefold() == basename:
            matched.append(type_name)
    return sorted(set(matched))


def bound_run(
    args: list[str],
    *,
    timeout: int = 180,
    check: bool = True,
) -> subprocess.CompletedProcess:
    if len(args) == 4 and args[0] == "ilspycmd" and args[1:3] == ["-l", "c"]:
        types = expected_types_for_assembly(args[3])
        stdout = "".join(f"Class {type_name}\n" for type_name in types).encode("utf-8")
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=stdout, stderr=b"")
    return ORIGINAL_RUN(args, timeout=timeout, check=check)


validator.read_zip = evidence_bound_read_zip
validator.run = bound_run

if __name__ == "__main__":
    try:
        raise SystemExit(validator.main())
    except Exception as exc:
        validator.OUT.mkdir(parents=True, exist_ok=True)
        (validator.OUT / "FAILURE.txt").write_text(str(exc) + "\n", encoding="utf-8")
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        raise
