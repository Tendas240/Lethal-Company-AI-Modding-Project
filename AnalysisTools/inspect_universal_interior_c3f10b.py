#!/usr/bin/env python3
"""C3F10B exact LethalLevelLoader 1.7.12 package/binary restoration capture.

Repository-native, fail-closed static evidence only. Provenance mode records the
exact accepted Thunderstore package as an unreviewed byte-binding candidate.
Locked capture mode statically inspects only the LLL methods relevant to the
C3F9 SpawnSyncedObject/network-prefab restoration gate. No managed assembly is
loaded or executed.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import urllib.request
import zipfile

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F10"
EXPORT = ROOT / "ProfileSources/S1.42AK/export.r2x"
C3B = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3B/LLL_DAWN_BRIDGE_SOURCE.json"
C3E3E = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3E3E/GENERATION_INTEGRATION_SOURCE.json"
C3F9 = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F9/FINDINGS.md"

PACKAGE = "IAmBatby-LethalLevelLoader"
VERSION = "1.7.12"
URL = f"https://gcdn.thunderstore.io/live/repository/packages/{PACKAGE}-{VERSION}.zip"
RELEASE_COMMIT = "f9998b91adf242cd8d735f4e697d55b32b94bfac"
PARSERS = {"dnfile": "0.18.0", "dncil": "1.0.2"}
BLOCK = 1024 * 1024

TARGET_METHODS = {
    ("LethalLevelLoader.Tools.ContentRestorer", "TryRestoreNetworkPrefab"): [
        "System.String::Equals",
        "LethalLevelLoader.Tools.ContentRestorer::RestoreAsset",
    ],
    ("LethalLevelLoader.Tools.ContentRestorer", "TryRestoreSpawnSyncedObject"): [
        "LethalLevelLoader.Tools.ContentRestorer::TryRestoreNetworkPrefab",
        "spawnPrefab",
    ],
    ("LethalLevelLoader.Tools.ContentRestorer", "RestoreAsset"): [
        "objectsToDestroy",
    ],
    ("LethalLevelLoader.AssetBundleLoader", "NetworkRegisterDungeonContent"): [
        "LethalLevelLoader.Tools.ContentRestorer::TryRestoreSpawnSyncedObject",
        "GetSpawnSyncedObjects",
        "RegisterNetworkPrefab",
    ],
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(BLOCK), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_member(name: str) -> str:
    raw = name.rstrip("/")
    if not raw or "\\" in raw or raw.startswith("/"):
        raise ValueError("Unsafe ZIP member path: " + repr(name))
    p = PurePosixPath(raw)
    if any(part in ("", ".", "..") for part in p.parts):
        raise ValueError("Unsafe ZIP member path: " + repr(name))
    return str(p)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_authority():
    import yaml

    profile = yaml.safe_load(EXPORT.read_text(encoding="utf-8"))
    matches = [m for m in profile["mods"] if m.get("name") == PACKAGE]
    if len(matches) != 1 or matches[0].get("enabled") is not True:
        raise ValueError("Accepted profile LLL package missing/ambiguous/disabled")
    m = matches[0]
    observed_version = ".".join(str(m["version"][k]) for k in ("major", "minor", "patch"))
    if observed_version != VERSION:
        raise ValueError(f"Accepted profile LLL version drift: {observed_version}")

    c3b = json.loads(C3B.read_text(encoding="utf-8"))
    if c3b["profile_package"]["dependency_string"] != f"{PACKAGE}-{VERSION}":
        raise ValueError("C3B LLL dependency drift")
    if c3b["source_binding"]["release_source_commit"] != RELEASE_COMMIT:
        raise ValueError("C3B LLL release-source commit drift")

    c3e3e = json.loads(C3E3E.read_text(encoding="utf-8"))
    lll = c3e3e["lll_binding"]
    if lll["dependency"] != f"{PACKAGE}-{VERSION}":
        raise ValueError("C3E3E LLL dependency drift")
    if lll["release_commit"] != RELEASE_COMMIT:
        raise ValueError("C3E3E LLL release-source commit drift")

    c3f9 = C3F9.read_text(encoding="utf-8")
    for required in ("BackroomsFlow", "CastleFlow", "CircusFacilityFlow"):
        if required not in c3f9:
            raise ValueError("C3F9 restoration-gate authority drift: " + required)

    return {
        "accepted_export_sha256": sha256_file(EXPORT),
        "c3b_lll_bridge_sha256": sha256_file(C3B),
        "c3e3e_generation_integration_sha256": sha256_file(C3E3E),
        "c3f9_findings_sha256": sha256_file(C3F9),
        "lll_release_source_commit": RELEASE_COMMIT,
    }


def download(cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / f"{PACKAGE}-{VERSION}.zip"
    if not target.exists():
        tmp = target.with_suffix(".partial")
        req = urllib.request.Request(URL, headers={"User-Agent": "LC-AI-Modding-Project-C3F10B/1"})
        with urllib.request.urlopen(req, timeout=180) as response, tmp.open("wb") as out:
            shutil.copyfileobj(response, out)
        tmp.replace(target)
    return target


def inventory(path: Path):
    members = []
    seen = set()
    manifest = None
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            name = safe_member(info.filename)
            folded = name.casefold()
            if folded in seen:
                raise ValueError("Duplicate/case-colliding ZIP member: " + name)
            seen.add(folded)
            if info.flag_bits & 1:
                raise ValueError("Encrypted ZIP member: " + name)
            if info.is_dir():
                continue
            data = z.read(info)
            rec = {
                "member": name,
                "bytes": len(data),
                "sha256": sha256_bytes(data),
                "dll": name.lower().endswith(".dll"),
                "unityfs": data.startswith(b"UnityFS\x00"),
            }
            members.append(rec)
            if name == "manifest.json":
                if manifest is not None:
                    raise ValueError("Multiple root manifest.json files")
                manifest = json.loads(data.decode("utf-8-sig"))

    if not isinstance(manifest, dict):
        raise ValueError("Root manifest.json missing")
    if manifest.get("name") != "LethalLevelLoader":
        raise ValueError("Package manifest name mismatch: " + repr(manifest.get("name")))
    if manifest.get("version_number") != VERSION:
        raise ValueError("Package manifest version mismatch: " + repr(manifest.get("version_number")))

    dlls = [x for x in members if x["dll"]]
    target = [x for x in dlls if PurePosixPath(x["member"]).name.casefold() == "lethallevelloader.dll"]
    if len(target) != 1:
        raise ValueError(f"Expected exactly one LethalLevelLoader.dll, found {len(target)}")

    return {
        "package": PACKAGE,
        "version": VERSION,
        "source_url": URL,
        "zip_bytes": path.stat().st_size,
        "zip_sha256": sha256_file(path),
        "manifest": manifest,
        "members": sorted(members, key=lambda x: x["member"]),
        "dll_members": dlls,
        "target_dll": target[0],
    }


def inspect_target_dll(member: str, data: bytes):
    pe = dnfile.dnPE(data=data)
    if pe.net is None or pe.net.mdtables is None:
        raise ValueError("LethalLevelLoader.dll is not a readable managed assembly")

    nested = {
        id(row.NestedClass.row): row.EnclosingClass.row
        for row in (pe.net.mdtables.NestedClass or [])
    }

    def defined_type_name(row):
        name, ns = str(row.TypeName), str(row.TypeNamespace)
        own = f"{ns}.{name}" if ns else name
        return defined_type_name(nested[id(row)]) + "+" + name if id(row) in nested else own

    method_owners = {}
    field_owners = {}
    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        method_owners.update({id(m.row): owner for m in t.MethodList})
        field_owners.update({id(f.row): owner for f in t.FieldList})

    def type_name(row):
        if hasattr(row, "TypeName"):
            ns, name = str(row.TypeNamespace), str(row.TypeName)
            return f"{ns}.{name}" if ns else name
        if hasattr(row, "Signature"):
            return "TypeSpec[" + row.Signature.value.hex() + "]"
        return type(row).__name__

    tables = {1: "TypeRef", 2: "TypeDef", 4: "Field", 6: "MethodDef",
              10: "MemberRef", 27: "TypeSpec", 43: "MethodSpec"}

    def resolve(token):
        table_id = token >> 24
        idx = token & 0xFFFFFF
        if table_id == 0x70:
            entry = pe.net.user_strings.get(idx)
            return repr(entry.value) if entry is not None else f"user_string(0x{idx:x})"
        table_name = tables.get(table_id)
        if not table_name:
            return f"token(0x{token:08x})"
        table = getattr(pe.net.mdtables, table_name)
        if idx <= 0 or idx > len(table.rows):
            return f"invalid_token(0x{token:08x})"
        row = table.rows[idx - 1]
        if table_id == 43:
            inner = (row.Method.table.number << 24) | row.Method.row_index
            return "MethodSpec(" + resolve(inner) + "; " + row.Instantiation.value.hex() + ")"
        if table_id in (1, 2, 27):
            return type_name(row)
        if table_id == 6:
            return method_owners[id(row)] + "::" + str(row.Name)
        if table_id == 4:
            return field_owners[id(row)] + "::" + str(row.Name)
        return type_name(row.Class.row) + "::" + str(row.Name)

    assembly_rows = pe.net.mdtables.Assembly or []
    if not assembly_rows:
        raise ValueError("Managed assembly metadata has no Assembly row")
    a = assembly_rows.rows[0]
    assembly = {
        "name": str(a.Name),
        "version": f"{a.MajorVersion}.{a.MinorVersion}.{a.BuildNumber}.{a.RevisionNumber}",
    }
    if assembly["name"] != "LethalLevelLoader":
        raise ValueError("Target DLL assembly identity mismatch: " + repr(assembly["name"]))

    found = {}
    parse_errors = []
    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        for mr in t.MethodList:
            m = mr.row
            key = (owner, str(m.Name))
            if key not in TARGET_METHODS:
                continue
            if key in found:
                raise ValueError("Duplicate target method: " + "::".join(key))
            if not m.Rva:
                raise ValueError("Target method has no RVA body: " + "::".join(key))
            try:
                body = read_method_body_from_bytes(pe.get_data(m.Rva, 250000))
            except Exception as exc:
                parse_errors.append({
                    "type": owner,
                    "method": str(m.Name),
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

            instructions = []
            resolved_values = []
            for ins in body.instructions:
                operand = ins.operand
                value = operand.value if hasattr(operand, "value") else None
                resolved = resolve(value) if isinstance(value, int) else None
                if resolved is not None:
                    resolved_values.append(resolved)
                instructions.append({
                    "offset": ins.offset,
                    "opcode": ins.opcode.name,
                    "operand": None if operand is None else str(operand),
                    "resolved": resolved,
                })

            missing_signals = [
                signal for signal in TARGET_METHODS[key]
                if not any(signal in resolved for resolved in resolved_values)
            ]
            if missing_signals:
                raise ValueError(
                    "Target method expected IL signal(s) missing for "
                    + "::".join(key) + ": " + ", ".join(missing_signals)
                )

            found[key] = {
                "type": owner,
                "method": str(m.Name),
                "token": f"0x{0x06000000 | mr.row_index:08x}",
                "rva": int(m.Rva),
                "signature_hex": m.Signature.value.hex(),
                "required_signals": TARGET_METHODS[key],
                "instructions": instructions,
            }

    if parse_errors:
        raise ValueError("Target managed IL parse errors: " + json.dumps(parse_errors))
    missing = [f"{t}::{m}" for (t, m) in TARGET_METHODS if (t, m) not in found]
    if missing:
        raise ValueError("Required target methods missing: " + ", ".join(missing))

    return {
        "member": member,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "assembly": assembly,
        "target_methods": [
            found[key] for key in TARGET_METHODS
        ],
        "summary": {
            "target_methods": len(found),
            "target_instructions": sum(len(v["instructions"]) for v in found.values()),
            "parse_errors": 0,
        },
    }


def verify_lock(lock, authority, observed):
    if lock.get("schema_version") != "c3f10b-lll-package-lock-1":
        raise ValueError("LLL package lock schema drift")
    if lock.get("authority") != authority:
        raise ValueError("LLL package lock authority drift")
    if lock.get("package") != observed:
        raise ValueError("Exact LLL package/member provenance drift")


def capture(path: Path, observed, authority, lock_path: Path, out: Path):
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    verify_lock(lock, authority, observed)

    versions = {name: importlib.metadata.version(name) for name in PARSERS}
    if versions != PARSERS:
        raise ValueError(f"Parser version mismatch: expected {PARSERS}, got {versions}")

    target = observed["target_dll"]
    with zipfile.ZipFile(path) as z:
        data = z.read(target["member"])
    if len(data) != target["bytes"] or sha256_bytes(data) != target["sha256"]:
        raise ValueError("Target LLL DLL drift during capture")

    report = inspect_target_dll(target["member"], data)
    result = {
        "schema_version": "c3f10b-lll-restoration-capture-1",
        "authority": authority,
        "package": observed,
        "package_lock_sha256": sha256_file(lock_path),
        "helper_sha256": sha256_file(Path(__file__)),
        "toolchain": {"python": sys.version.split()[0], **versions},
        "target_dll_report": report,
        "proof_boundary": (
            "Exact accepted IAmBatby-LethalLevelLoader 1.7.12 Thunderstore package and static "
            "managed IL for TryRestoreNetworkPrefab, TryRestoreSpawnSyncedObject, RestoreAsset, "
            "and NetworkRegisterDungeonContent only. No assembly is loaded or executed. This "
            "capture alone does not prove that V81 NetworkConfig contains a registered prefab "
            "named EntranceTeleportB or that any of the three C3F9 placeholders restored at runtime."
        ),
    }
    write_json(out / "LLL_RESTORATION_CAPTURE.json", result)
    print(json.dumps(report["summary"], indent=2))


def self_test():
    assert safe_member("BepInEx/plugins/LethalLevelLoader/LethalLevelLoader.dll").endswith("LethalLevelLoader.dll")
    for bad in ("../x", "/x", "a\\b"):
        try:
            safe_member(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("unsafe path accepted: " + bad)
    assert len(TARGET_METHODS) == 4
    assert ("LethalLevelLoader.AssetBundleLoader", "NetworkRegisterDungeonContent") in TARGET_METHODS
    print("C3F10B LLL self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cache", type=Path, default=Path("c3f10b-lll-package"))
    p.add_argument("--lock", type=Path, default=EVIDENCE / "LLL_PACKAGE_LOCK.json")
    p.add_argument("--record-provenance", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()

    if args.self_test:
        self_test()
        return

    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("LLL_PROVENANCE_CANDIDATE.json", "LLL_RESTORATION_CAPTURE.json", "LLL_CAPTURE_FAILURE.json"):
        (args.out / name).unlink(missing_ok=True)

    try:
        authority = verify_authority()
        package_path = download(args.cache)
        observed = inventory(package_path)
        if args.record_provenance:
            write_json(args.out / "LLL_PROVENANCE_CANDIDATE.json", {
                "schema_version": "c3f10b-lll-provenance-candidate-1",
                "status": "UNREVIEWED_BYTE_BINDING_NO_RESTORATION_CLAIM",
                "authority": authority,
                "package": observed,
                "helper_sha256": sha256_file(Path(__file__)),
            })
            print(json.dumps({
                "zip_bytes": observed["zip_bytes"],
                "zip_sha256": observed["zip_sha256"],
                "target_dll": observed["target_dll"],
            }, indent=2))
            return
        capture(package_path, observed, authority, args.lock, args.out)
    except Exception as exc:
        write_json(args.out / "LLL_CAPTURE_FAILURE.json", {
            "fail_closed": True,
            "package": PACKAGE,
            "version": VERSION,
            "source_url": URL,
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
        raise


if __name__ == "__main__":
    main()
