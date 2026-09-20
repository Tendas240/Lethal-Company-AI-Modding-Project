#!/usr/bin/env python3
"""Fail-closed exact BlackMesa.dll IL scan for C3F3.

Reads only the exact Black Mesa 3.4.4 Thunderstore ZIP and exact BlackMesa.dll
established by C3F2. Uses dnfile/dncil for static IL metadata/body inspection.
No managed assembly, Unity, game, or mod code is executed.

Usage:
  python inspect_universal_interior_c3f3.py --zip PACKAGE.zip --out OUTPUT
  python inspect_universal_interior_c3f3.py --self-test
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import zipfile

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

PACKAGE = "Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior"
VERSION = "3.4.4"
EXPECTED_ZIP_BYTES = 228214268
EXPECTED_ZIP_SHA256 = "12921825bee51bfd46582989322a1f31183b65f59293c73654a102fb68d068b7"
DLL_MEMBER = "BepInEx/plugins/BlackMesa.dll"
EXPECTED_DLL_BYTES = 143360
EXPECTED_DLL_SHA256 = "a90f157becdc68ab7fe6898eefc2feaee98352a0f04b2cda414741729a048eef"
PARSER_VERSIONS = {"dnfile": "0.18.0", "dncil": "1.0.2"}

SIGNAL_RE = re.compile(
    r"entranceteleport|entranceid|isentrancetobuilding|entrancepoint|exitpoint|"
    r"fire.?exit|shortcut|teleport|harmony|patch|dawn|dusk",
    re.I,
)
STRONG_ENTRANCE_RE = re.compile(
    r"entranceteleport|entranceid|isentrancetobuilding|entrancepoint|exitpoint|"
    r"fire.?exit|shortcut",
    re.I,
)
PAIRING_FIELDS = ("::entranceId", "::isEntranceToBuilding", "::entrancePoint", "::exitPoint")
CREATION_RE = re.compile(
    r"UnityEngine\.(?:Object|GameObject)::Instantiate|::AddComponent|"
    r"::GetComponent|::GetComponents|::FindObjectOfType|::FindObjectsOfType",
    re.I,
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def self_test():
    assert SIGNAL_RE.search("EntranceTeleport")
    assert SIGNAL_RE.search("HarmonyPatch")
    assert STRONG_ENTRANCE_RE.search("isEntranceToBuilding")
    assert not STRONG_ENTRANCE_RE.search("ordinaryMethod")
    assert CREATION_RE.search("UnityEngine.Object::Instantiate")
    print("C3F3 self-test passed")


def capture(data):
    if len(data) != EXPECTED_DLL_BYTES or sha256(data) != EXPECTED_DLL_SHA256:
        raise ValueError("Exact BlackMesa.dll size/SHA-256 mismatch")

    pe = dnfile.dnPE(data=data)
    if pe.net is None or pe.net.mdtables is None:
        raise ValueError("BlackMesa.dll is not a readable managed .NET assembly")

    nested = {
        id(row.NestedClass.row): row.EnclosingClass.row
        for row in (pe.net.mdtables.NestedClass or [])
    }

    def defined_type_name(row):
        name = str(row.TypeName)
        ns = str(row.TypeNamespace)
        own = (ns + "." + name) if ns else name
        if id(row) in nested:
            return defined_type_name(nested[id(row)]) + "+" + name
        return own

    method_owners = {}
    field_owners = {}
    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        method_owners.update({id(m.row): owner for m in t.MethodList})
        field_owners.update({id(f.row): owner for f in t.FieldList})

    def compressed(buf, i):
        x = buf[i]
        if x < 128:
            return x, i + 1
        if x < 192:
            return ((x & 63) << 8) | buf[i + 1], i + 2
        return (
            ((x & 31) << 24)
            | (buf[i + 1] << 16)
            | (buf[i + 2] << 8)
            | buf[i + 3],
            i + 4,
        )

    def type_name(row):
        if hasattr(row, "TypeName"):
            if row in pe.net.mdtables.TypeDef:
                return defined_type_name(row)
            ns = str(row.TypeNamespace)
            name = str(row.TypeName)
            return (ns + "." + name) if ns else name
        if hasattr(row, "Signature"):
            buf = row.Signature.value
            if len(buf) >= 3 and buf[:2] in (b"\x15\x12", b"\x15\x11"):
                coded, _ = compressed(buf, 2)
                tag = coded & 3
                tables = [pe.net.mdtables.TypeDef, pe.net.mdtables.TypeRef, pe.net.mdtables.TypeSpec]
                if tag >= len(tables):
                    return "TypeSpec[signature=" + buf.hex() + "]"
                table = tables[tag]
                idx = (coded >> 2) - 1
                if idx < 0 or idx >= len(table.rows):
                    return "TypeSpec[signature=" + buf.hex() + "]"
                return type_name(table.rows[idx]) + " [signature=" + buf.hex() + "]"
            return "TypeSpec[signature=" + buf.hex() + "]"
        return type(row).__name__

    table_names = {
        1: "TypeRef",
        2: "TypeDef",
        4: "Field",
        6: "MethodDef",
        10: "MemberRef",
        27: "TypeSpec",
        43: "MethodSpec",
    }

    def resolve(value):
        table_id = value >> 24
        idx = value & 0xFFFFFF
        if table_id == 0x70:
            entry = pe.net.user_strings.get(idx)
            return repr(entry.value) if entry is not None else f"user_string(0x{idx:x})"
        table_name = table_names.get(table_id)
        if not table_name:
            return f"token(0x{value:08x})"
        table = getattr(pe.net.mdtables, table_name)
        if idx <= 0 or idx > len(table.rows):
            return f"invalid_token(0x{value:08x})"
        row = table.rows[idx - 1]
        if table_id == 43:
            method_token = (row.Method.table.number << 24) | row.Method.row_index
            return "MethodSpec(" + resolve(method_token) + "; instantiation=" + row.Instantiation.value.hex() + ")"
        if table_id in (1, 2, 27):
            return type_name(row)
        if table_id == 6:
            return method_owners[id(row)] + "::" + str(row.Name)
        if table_id == 4:
            return field_owners[id(row)] + "::" + str(row.Name)
        return type_name(row.Class.row) + "::" + str(row.Name)

    assembly_refs = sorted(str(r.Name) for r in (pe.net.mdtables.AssemblyRef or []))

    matching_type_defs = []
    all_type_defs = []
    for t in pe.net.mdtables.TypeDef:
        name = defined_type_name(t)
        all_type_defs.append(name)
        if SIGNAL_RE.search(name):
            matching_type_defs.append(name)

    matching_type_refs = []
    for r in (pe.net.mdtables.TypeRef or []):
        name = type_name(r)
        if SIGNAL_RE.search(name):
            matching_type_refs.append(name)

    matching_member_refs = []
    for i, _ in enumerate((pe.net.mdtables.MemberRef or []), 1):
        resolved = resolve(0x0A000000 | i)
        if SIGNAL_RE.search(resolved):
            matching_member_refs.append(resolved)

    signal_methods = []
    entrance_references = []
    pairing_field_references = []
    pairing_field_writes = []
    signal_string_literals = []
    methods_scanned = 0
    methods_without_body = 0
    instructions_scanned = 0

    for t in pe.net.mdtables.TypeDef:
        owner = defined_type_name(t)
        for mr in t.MethodList:
            m = mr.row
            method = str(m.Name)
            identity = {
                "type": owner,
                "method": method,
                "method_token": f"0x{0x06000000 | mr.row_index:08x}",
                "rva": m.Rva,
                "signature_hex": m.Signature.value.hex(),
            }
            if not m.Rva:
                methods_without_body += 1
                continue

            body = read_method_body_from_bytes(pe.get_data(m.Rva, 100000))
            methods_scanned += 1
            ins_records = []
            local_signal = bool(SIGNAL_RE.search(owner) or SIGNAL_RE.search(method))
            strong_signal = bool(STRONG_ENTRANCE_RE.search(owner) or STRONG_ENTRANCE_RE.search(method))
            creation_calls = []

            for ins in body.instructions:
                instructions_scanned += 1
                operand = ins.operand
                token = operand.value if hasattr(operand, "value") else None
                resolved = resolve(token) if token is not None else None
                record = {
                    "offset": ins.offset,
                    "opcode": ins.opcode.name,
                    "operand": None if operand is None else str(operand),
                    "resolved_token": resolved,
                }
                ins_records.append(record)

                if resolved and SIGNAL_RE.search(resolved):
                    local_signal = True
                if resolved and STRONG_ENTRANCE_RE.search(resolved):
                    strong_signal = True
                    entrance_references.append({**identity, **record})
                if resolved and any(field in resolved for field in PAIRING_FIELDS):
                    ref = {**identity, **record}
                    pairing_field_references.append(ref)
                    if ins.opcode.name in ("stfld", "stsfld", "stobj", "initobj"):
                        pairing_field_writes.append(ref)
                if resolved and CREATION_RE.search(resolved):
                    creation_calls.append(record)
                if ins.opcode.name == "ldstr" and resolved and SIGNAL_RE.search(resolved):
                    signal_string_literals.append({**identity, **record})
                    local_signal = True
                    if STRONG_ENTRANCE_RE.search(resolved):
                        strong_signal = True

            if local_signal:
                signal_methods.append(
                    {
                        **identity,
                        "strong_entrance_signal": strong_signal,
                        "creation_or_component_calls": creation_calls,
                        "instructions": ins_records,
                    }
                )

    if methods_scanned == 0:
        raise ValueError("No method bodies scanned")

    return {
        "schema_version": "phase-c3f3-il-1",
        "package": PACKAGE,
        "version": VERSION,
        "dll_member": DLL_MEMBER,
        "dll_bytes": len(data),
        "dll_sha256": sha256(data),
        "assembly_refs": assembly_refs,
        "coverage": {
            "type_defs": len(all_type_defs),
            "method_bodies_scanned": methods_scanned,
            "methods_without_body": methods_without_body,
            "instructions_scanned": instructions_scanned,
            "parse_errors": 0,
        },
        "metadata_signals": {
            "matching_type_defs": sorted(set(matching_type_defs)),
            "matching_type_refs": sorted(set(matching_type_refs)),
            "matching_member_refs": sorted(set(matching_member_refs)),
        },
        "signal_methods": signal_methods,
        "entrance_references": entrance_references,
        "pairing_field_references": pairing_field_references,
        "pairing_field_writes": pairing_field_writes,
        "signal_string_literals": signal_string_literals,
        "summary": {
            "signal_methods": len(signal_methods),
            "strong_entrance_signal_methods": sum(m["strong_entrance_signal"] for m in signal_methods),
            "entrance_references": len(entrance_references),
            "pairing_field_references": len(pairing_field_references),
            "pairing_field_writes": len(pairing_field_writes),
            "signal_string_literals": len(signal_string_literals),
            "opcode_counts_on_pairing_fields": dict(Counter(r["opcode"] for r in pairing_field_references)),
        },
        "proof_boundary": (
            "Exact BlackMesa.dll static IL/metadata only. Reflection, dynamically generated code, "
            "other assemblies, scene serialization, final Harmony patch order and actual runtime "
            "entrance behavior are not inferred beyond directly captured IL references."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    if args.zip is None or args.out is None:
        parser.error("--zip and --out are required unless --self-test is used")

    versions = {name: importlib.metadata.version(name) for name in PARSER_VERSIONS}
    if versions != PARSER_VERSIONS:
        raise ValueError(f"Parser version mismatch: expected {PARSER_VERSIONS}, got {versions}")

    args.out.mkdir(parents=True, exist_ok=True)

    try:
        raw = args.zip.read_bytes()
        if len(raw) != EXPECTED_ZIP_BYTES or sha256(raw) != EXPECTED_ZIP_SHA256:
            raise ValueError("Exact Black Mesa 3.4.4 ZIP size/SHA-256 mismatch")
        with zipfile.ZipFile(args.zip) as archive:
            info = archive.getinfo(DLL_MEMBER)
            if info.file_size != EXPECTED_DLL_BYTES:
                raise ValueError("BlackMesa.dll ZIP member size mismatch")
            data = archive.read(info)
        report = capture(data)
        report["tools"] = versions
        report["zip_bytes"] = len(raw)
        report["zip_sha256"] = sha256(raw)
        output = args.out / "BLACK_MESA_344_DLL_ENTRANCE_IL.json"
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["summary"], indent=2))
    except Exception as exc:
        failure = {
            "schema_version": "phase-c3f3-failure-1",
            "package": PACKAGE,
            "version": VERSION,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "fail_closed": True,
        }
        (args.out / "CAPTURE_FAILURE.json").write_text(
            json.dumps(failure, indent=2) + "\n", encoding="utf-8"
        )
        raise


if __name__ == "__main__":
    main()
