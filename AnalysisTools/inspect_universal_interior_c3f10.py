#!/usr/bin/env python3
"""C3F10 exact DunGenReferenceFixer 0.0.1 package/binary capture.

Repository-native, fail-closed static evidence only. The accepted package is
first recorded as an unreviewed byte-binding candidate. Normal capture requires
a reviewed PACKAGE_LOCK.json and statically inspects managed IL/metadata without
loading or executing any game/mod assembly.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import urllib.request
import zipfile

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F10"
EXPORT = ROOT / "ProfileSources/S1.42AK/export.r2x"
C3F9 = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F9/FINDINGS.md"
PACKAGE = "Zaggy1024-DunGenReferenceFixer"
VERSION = "0.0.1"
URL = f"https://gcdn.thunderstore.io/live/repository/packages/{PACKAGE}-{VERSION}.zip"
PARSERS = {"dnfile": "0.18.0", "dncil": "1.0.2"}
SIGNAL_RE = re.compile(
    r"dungen|reference|assetbundle|loadasset|harmony|entrance|teleport|prefab|"
    r"gameobject|networkobject|lethallevelloader|extendeddungeon|fix",
    re.I,
)
BLOCK = 1024 * 1024


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
        raise ValueError("Accepted profile package missing/ambiguous/disabled")
    m = matches[0]
    observed_version = ".".join(str(m["version"][k]) for k in ("major", "minor", "patch"))
    if observed_version != VERSION:
        raise ValueError(f"Accepted profile version drift: {observed_version}")
    c3f9 = C3F9.read_text(encoding="utf-8")
    for required in (PACKAGE + " 0.0.1", "BackroomsFlow", "CastleFlow", "CircusFacilityFlow"):
        if required not in c3f9:
            raise ValueError("C3F9 reference-restoration authority drift: " + required)
    return {
        "accepted_export_sha256": sha256_file(EXPORT),
        "c3f9_findings_sha256": sha256_file(C3F9),
    }


def download(cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / f"{PACKAGE}-{VERSION}.zip"
    if not target.exists():
        tmp = target.with_suffix(".partial")
        req = urllib.request.Request(URL, headers={"User-Agent": "LC-AI-Modding-Project-C3F10/1"})
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
    if manifest.get("name") != PACKAGE.split("-", 1)[1]:
        raise ValueError("Package manifest name mismatch: " + repr(manifest.get("name")))
    if manifest.get("version_number") != VERSION:
        raise ValueError("Package manifest version mismatch: " + repr(manifest.get("version_number")))
    dlls = [x for x in members if x["dll"]]
    if not dlls:
        raise ValueError("Exact package contains no DLL")
    return {
        "package": PACKAGE,
        "version": VERSION,
        "source_url": URL,
        "zip_bytes": path.stat().st_size,
        "zip_sha256": sha256_file(path),
        "manifest": manifest,
        "members": sorted(members, key=lambda x: x["member"]),
        "dll_members": dlls,
    }


def compressed(buf: bytes, i: int):
    first = buf[i]
    if first < 0x80:
        return first, i + 1
    if first < 0xC0:
        return ((first & 0x3F) << 8) | buf[i + 1], i + 2
    if first < 0xE0:
        return (((first & 0x1F) << 24) | (buf[i + 1] << 16) |
                (buf[i + 2] << 8) | buf[i + 3]), i + 4
    raise ValueError("Invalid compressed metadata integer")


def inspect_managed(member: str, data: bytes):
    pe = dnfile.dnPE(data=data)
    if pe.net is None or pe.net.mdtables is None:
        return {
            "member": member,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "managed": False,
        }

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

    assembly = None
    if pe.net.mdtables.Assembly and pe.net.mdtables.Assembly.rows:
        a = pe.net.mdtables.Assembly.rows[0]
        assembly = {
            "name": str(a.Name),
            "version": f"{a.MajorVersion}.{a.MinorVersion}.{a.BuildNumber}.{a.RevisionNumber}",
        }

    type_defs = [defined_type_name(t) for t in pe.net.mdtables.TypeDef]
    type_refs = sorted(type_name(t) for t in (pe.net.mdtables.TypeRef or []))
    member_refs = []
    for i, _ in enumerate((pe.net.mdtables.MemberRef or []), 1):
        member_refs.append(resolve(0x0A000000 | i))

    methods = []
    parse_errors = []
    opcode_counts = Counter()
    instructions_scanned = 0
    methods_without_body = []
    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        for mr in t.MethodList:
            m = mr.row
            ident = {
                "type": owner,
                "method": str(m.Name),
                "token": f"0x{0x06000000 | mr.row_index:08x}",
                "rva": int(m.Rva),
                "signature_hex": m.Signature.value.hex(),
            }
            if not m.Rva:
                methods_without_body.append(ident)
                continue
            try:
                body = read_method_body_from_bytes(pe.get_data(m.Rva, 100000))
            except Exception as exc:
                parse_errors.append({**ident, "error": f"{type(exc).__name__}: {exc}"})
                continue
            ins = []
            signals = []
            for x in body.instructions:
                instructions_scanned += 1
                opcode_counts[x.opcode.name] += 1
                operand = x.operand
                value = operand.value if hasattr(operand, "value") else None
                resolved = resolve(value) if isinstance(value, int) else None
                rec = {
                    "offset": x.offset,
                    "opcode": x.opcode.name,
                    "operand": None if operand is None else str(operand),
                    "resolved": resolved,
                }
                ins.append(rec)
                if resolved and SIGNAL_RE.search(resolved):
                    signals.append(rec)
            methods.append({**ident, "signal": bool(SIGNAL_RE.search(owner) or SIGNAL_RE.search(str(m.Name)) or signals),
                            "signal_instructions": signals, "instructions": ins})

    if parse_errors:
        raise ValueError("Managed IL parse errors: " + json.dumps(parse_errors))
    if not methods:
        raise ValueError("Managed DLL contains no readable RVA-bearing method body")

    custom_attrs = []
    for i, ca in enumerate((pe.net.mdtables.CustomAttribute or []), 1):
        try:
            ctor = ca.Type
            ctor_token = (ctor.table.number << 24) | ctor.row_index
            parent = ca.Parent
            custom_attrs.append({
                "token": f"0x{0x0C000000 | i:08x}",
                "constructor": resolve(ctor_token),
                "parent_table": getattr(parent.table, "name", str(parent.table)),
                "parent_row_index": parent.row_index,
                "value_hex": ca.Value.value.hex(),
            })
        except Exception as exc:
            custom_attrs.append({"token": f"0x{0x0C000000 | i:08x}",
                                 "decode_error": f"{type(exc).__name__}: {exc}"})

    return {
        "member": member,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "managed": True,
        "assembly": assembly,
        "assembly_refs": sorted(str(r.Name) + " " +
                                f"{r.MajorVersion}.{r.MinorVersion}.{r.BuildNumber}.{r.RevisionNumber}"
                                for r in (pe.net.mdtables.AssemblyRef or [])),
        "type_defs": type_defs,
        "type_refs": type_refs,
        "member_refs": member_refs,
        "custom_attributes": custom_attrs,
        "methods_without_body": methods_without_body,
        "methods": methods,
        "summary": {
            "type_defs": len(type_defs),
            "type_refs": len(type_refs),
            "member_refs": len(member_refs),
            "custom_attributes": len(custom_attrs),
            "method_bodies_scanned": len(methods),
            "methods_without_body": len(methods_without_body),
            "instructions_scanned": instructions_scanned,
            "signal_methods": sum(m["signal"] for m in methods),
            "opcode_counts": dict(sorted(opcode_counts.items())),
            "parse_errors": 0,
        },
    }


def verify_lock(lock, authority, observed):
    if lock.get("schema_version") != "c3f10-package-lock-1":
        raise ValueError("Package lock schema drift")
    if lock.get("authority") != authority:
        raise ValueError("Package lock authority drift")
    if lock.get("package") != observed:
        raise ValueError("Exact package/member provenance drift")


def capture(path: Path, observed, authority, lock_path: Path, out: Path):
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    verify_lock(lock, authority, observed)
    versions = {name: importlib.metadata.version(name) for name in PARSERS}
    if versions != PARSERS:
        raise ValueError(f"Parser version mismatch: expected {PARSERS}, got {versions}")

    reports = []
    with zipfile.ZipFile(path) as z:
        for rec in observed["dll_members"]:
            data = z.read(rec["member"])
            if len(data) != rec["bytes"] or sha256_bytes(data) != rec["sha256"]:
                raise ValueError("DLL member drift during capture: " + rec["member"])
            reports.append(inspect_managed(rec["member"], data))
    if not any(r.get("managed") for r in reports):
        raise ValueError("No managed implementation DLL in exact package")

    result = {
        "schema_version": "c3f10-reference-restoration-capture-1",
        "authority": authority,
        "package": observed,
        "package_lock_sha256": sha256_file(lock_path),
        "helper_sha256": sha256_file(Path(__file__)),
        "toolchain": {"python": sys.version.split()[0], **versions},
        "dll_reports": reports,
        "summary": {
            "dlls": len(reports),
            "managed_dlls": sum(bool(r.get("managed")) for r in reports),
            "managed_method_bodies": sum(r.get("summary", {}).get("method_bodies_scanned", 0) for r in reports),
            "managed_instructions": sum(r.get("summary", {}).get("instructions_scanned", 0) for r in reports),
            "signal_methods": sum(r.get("summary", {}).get("signal_methods", 0) for r in reports),
        },
        "proof_boundary": (
            "Exact accepted DunGenReferenceFixer 0.0.1 package and static managed metadata/IL only. "
            "No managed assembly is loaded or executed. Loader behavior in other assemblies and "
            "actual Unity runtime object restoration are not inferred unless directly bound by captured references."
        ),
    }
    write_json(out / "REFERENCE_RESTORATION_CAPTURE.json", result)
    print(json.dumps(result["summary"], indent=2))


def self_test():
    assert safe_member("BepInEx/plugins/X.dll") == "BepInEx/plugins/X.dll"
    for bad in ("../x", "/x", "a\\b"):
        try:
            safe_member(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("unsafe path accepted: " + bad)
    assert SIGNAL_RE.search("DunGenReferenceFixer")
    assert SIGNAL_RE.search("AssetBundle.LoadAsset")
    print("C3F10 self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cache", type=Path, default=Path("c3f10-package"))
    p.add_argument("--lock", type=Path, default=EVIDENCE / "PACKAGE_LOCK.json")
    p.add_argument("--record-provenance", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("PROVENANCE_CANDIDATE.json", "REFERENCE_RESTORATION_CAPTURE.json", "CAPTURE_FAILURE.json"):
        (args.out / name).unlink(missing_ok=True)
    try:
        authority = verify_authority()
        package_path = download(args.cache)
        observed = inventory(package_path)
        if args.record_provenance:
            write_json(args.out / "PROVENANCE_CANDIDATE.json", {
                "status": "UNREVIEWED_BYTE_BINDING_NO_RESTORATION_CLAIM",
                "authority": authority,
                "package": observed,
                "helper_sha256": sha256_file(Path(__file__)),
            })
            print(json.dumps({
                "zip_bytes": observed["zip_bytes"],
                "zip_sha256": observed["zip_sha256"],
                "dlls": observed["dll_members"],
            }, indent=2))
            return
        capture(package_path, observed, authority, args.lock, args.out)
    except Exception as exc:
        write_json(args.out / "CAPTURE_FAILURE.json", {
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
