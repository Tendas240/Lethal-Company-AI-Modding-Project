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
import struct
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
    r"::GetComponent|::GetComponents|::TryGetComponent|"
    r"::FindObjectOfType|::FindObjectsOfType|::FindFirstObjectByType|"
    r"::FindAnyObjectByType|UnityEngine\.Resources::Load|"
    r"UnityEngine\.AssetBundle::LoadAsset",
    re.I,
)
REFLECTION_RE = re.compile(
    r"System\.(?:Type|Activator|AppDomain)::|System\.Reflection\.|"
    r"::(?:GetType|GetMethod|GetMethods|GetField|GetFields|GetProperty|"
    r"GetProperties|Invoke|CreateInstance|MakeGenericType|GetCustomAttribute|"
    r"GetCustomAttributes)(?:\b|$)",
    re.I,
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def self_test():
    metadata_self_test()
    assert SIGNAL_RE.search("EntranceTeleport")
    assert SIGNAL_RE.search("HarmonyPatch")
    assert STRONG_ENTRANCE_RE.search("isEntranceToBuilding")
    assert not STRONG_ENTRANCE_RE.search("ordinaryMethod")
    assert CREATION_RE.search("UnityEngine.Object::Instantiate")
    assert CREATION_RE.search("UnityEngine.AssetBundle::LoadAsset")
    assert REFLECTION_RE.search("System.Type::GetMethod")
    assert REFLECTION_RE.search("System.Reflection.MethodBase::Invoke")
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
    creation_or_component_references = []
    reflection_references = []
    dynamic_or_reflection_methods = []
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
            reflection_calls = []
            method_string_literals = []

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
                    creation_or_component_references.append({**identity, **record})
                if resolved and REFLECTION_RE.search(resolved):
                    reflection_calls.append(record)
                    reflection_references.append({**identity, **record})
                if ins.opcode.name == "ldstr" and resolved:
                    method_string_literals.append(record)
                    if SIGNAL_RE.search(resolved):
                        signal_string_literals.append({**identity, **record})
                        local_signal = True
                        if STRONG_ENTRANCE_RE.search(resolved):
                            strong_signal = True

            if creation_calls or reflection_calls:
                dynamic_or_reflection_methods.append(
                    {
                        **identity,
                        "creation_or_component_calls": creation_calls,
                        "reflection_calls": reflection_calls,
                        "string_literals": method_string_literals,
                        "instructions": ins_records,
                    }
                )

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
        "schema_version": "phase-c3f3-il-2",
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
        "dynamic_or_reflection_methods": dynamic_or_reflection_methods,
        "creation_or_component_references": creation_or_component_references,
        "reflection_references": reflection_references,
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
            "dynamic_or_reflection_methods": len(dynamic_or_reflection_methods),
            "creation_or_component_references": len(creation_or_component_references),
            "reflection_references": len(reflection_references),
            "opcode_counts_on_pairing_fields": dict(Counter(r["opcode"] for r in pairing_field_references)),
        },
        "proof_boundary": (
            "Exact BlackMesa.dll static IL/metadata only. Direct dynamic/component callsites and "
            "reflection API callsites in this DLL are captured globally across all scanned method "
            "bodies. Reflective targets not directly identifiable from captured operands/strings, "
            "dynamically generated code, other assemblies, scene serialization, final Harmony patch "
            "order and actual runtime entrance behavior are not inferred beyond captured evidence."
        ),
    }


# Metadata encoding follows ECMA-335 II.23.1/II.23.3. This deliberately
# supports a bounded subset: unknown encodings are errors, never guesses.
class MetadataReader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, count):
        if count < 0 or self.pos + count > len(self.data):
            raise ValueError("Truncated metadata payload")
        result = self.data[self.pos:self.pos + count]
        self.pos += count
        return result

    def byte(self):
        return self.take(1)[0]

    def uint(self):
        first = self.byte()
        if first < 0x80:
            return first
        if first < 0xc0:
            value = ((first & 0x3f) << 8) | self.byte()
            if value < 0x80:
                raise ValueError("Noncanonical compressed integer")
            return value
        if first < 0xe0:
            value = ((first & 0x1f) << 24) | int.from_bytes(self.take(3), "big")
            if value < 0x4000:
                raise ValueError("Noncanonical compressed integer")
            return value
        raise ValueError("Invalid compressed integer prefix")

    def string(self):
        if self.pos < len(self.data) and self.data[self.pos] == 0xff:
            self.pos += 1
            return None
        return self.take(self.uint()).decode("utf-8", errors="strict")

    def end(self):
        if self.pos != len(self.data):
            raise ValueError("Unconsumed metadata payload bytes")


CA_PRIMITIVES = {
    0x02: ("Boolean", "B"), 0x03: ("Char", "H"),
    0x04: ("SByte", "b"), 0x05: ("Byte", "B"),
    0x06: ("Int16", "h"), 0x07: ("UInt16", "H"),
    0x08: ("Int32", "i"), 0x09: ("UInt32", "I"),
    0x0a: ("Int64", "q"), 0x0b: ("UInt64", "Q"),
    0x0c: ("Single", "f"), 0x0d: ("Double", "d"),
}


def ca_signature_type(reader, resolve_type):
    code = reader.byte()
    if code in CA_PRIMITIVES:
        return "System." + CA_PRIMITIVES[code][0]
    if code == 0x0e:
        return "System.String"
    if code == 0x1d:
        return {"array": ca_signature_type(reader, resolve_type)}
    if code in (0x11, 0x12):
        resolved = resolve_type(reader.uint())
        if code == 0x12 and resolved == "System.Type":
            return resolved
        # The underlying width of an external enum is not encoded here.
        raise ValueError("Unsupported CA signature type (no width guessing): " + resolved)
    raise ValueError(f"Unsupported CA signature element 0x{code:02x}")


def ca_named_type(reader):
    code = reader.byte()
    if code in CA_PRIMITIVES:
        return "System." + CA_PRIMITIVES[code][0]
    if code == 0x0e:
        return "System.String"
    if code == 0x50:
        return "System.Type"
    if code == 0x1d:
        return {"array": ca_named_type(reader)}
    raise ValueError(f"Unsupported named-argument type 0x{code:02x}")


def ca_value(reader, kind):
    if isinstance(kind, dict) and "array" in kind:
        count = struct.unpack("<i", reader.take(4))[0]
        if count == -1:
            return None
        if count < 0 or count > len(reader.data) - reader.pos:
            raise ValueError("Invalid custom-attribute array count")
        return [ca_value(reader, kind["array"]) for _ in range(count)]
    if kind in ("System.String", "System.Type"):
        return reader.string()
    for name, fmt in CA_PRIMITIVES.values():
        if kind == "System." + name:
            value = struct.unpack("<" + fmt, reader.take(struct.calcsize(fmt)))[0]
            if name == "Boolean" and value not in (0, 1):
                raise ValueError("Invalid Boolean")
            return value
    raise ValueError("Unsupported custom-attribute value type")


def decode_custom_attribute(signature, payload, resolve_type):
    sig = MetadataReader(signature)
    if sig.byte() != 0x20:  # instance, default calling convention, non-generic
        raise ValueError("Unsupported attribute constructor calling convention")
    count = sig.uint()
    if sig.byte() != 0x01:
        raise ValueError("Attribute constructor must return void")
    params = [ca_signature_type(sig, resolve_type) for _ in range(count)]
    sig.end()
    data = MetadataReader(payload)
    if data.take(2) != b"\x01\x00":
        raise ValueError("Invalid CustomAttribute prolog")
    fixed = [{"type": kind, "value": ca_value(data, kind)} for kind in params]
    count = int.from_bytes(data.take(2), "little")
    named = []
    for _ in range(count):
        tag = data.byte()
        if tag not in (0x53, 0x54):
            raise ValueError("Invalid named argument discriminator")
        kind = ca_named_type(data)
        name = data.string()
        if not name or any(x["name"] == name for x in named):
            raise ValueError("Null/empty/duplicate named argument")
        named.append({"kind": "field" if tag == 0x53 else "property",
                      "name": name, "type": kind, "value": ca_value(data, kind)})
    data.end()
    return {"fixed_arguments": fixed, "named_arguments": named}


def metadata_self_test():
    resolve = lambda coded: {5: "System.Type"}[coded]
    # Independent hand-encoded Type + method name + Type[] constructor fixture.
    signature = bytes.fromhex("20 03 01 12 05 0e 1d 12 05")
    payload = b"\x01\x00\x03Foo\x03Bar\x01\x00\x00\x00\x03Baz\x00\x00"
    result = decode_custom_attribute(signature, payload, resolve)
    assert [x["value"] for x in result["fixed_arguments"]] == ["Foo", "Bar", ["Baz"]]
    # Truncation at every boundary and trailing junk must all fail closed.
    for bad in [payload[:n] for n in range(len(payload))] + [payload + b"\x00", b"\x00\x00" + payload[2:]]:
        try:
            decode_custom_attribute(signature, bad, resolve)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError("Malformed attribute accepted")
    named = b"\x01\x00\x01\x00\x53\x0e\x0amethodName\x03Bar"
    assert decode_custom_attribute(b"\x20\x00\x01", named, resolve)["named_arguments"][0]["value"] == "Bar"
    for bad in (b"\x80\x01", b"\xc0\x00\x00\x01", b"\xe0", b"\xff"):
        try:
            MetadataReader(bad).uint()
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid compressed integer accepted")
    assert MetadataReader(b"\xff").string() is None
    assert MetadataReader(b"\x00").string() == ""
    assert ca_value(MetadataReader(b"\xff\xff\xff\xff"), {"array": "System.Type"}) is None
    try:
        decode_custom_attribute(bytes.fromhex("20 01 01 11 05"), b"\x01\x00\x00\x00\x00\x00\x00\x00", resolve)
    except ValueError:
        pass
    else:
        raise AssertionError("External enum width guessed")


def capture_metadata(data):
    if len(data) != EXPECTED_DLL_BYTES or sha256(data) != EXPECTED_DLL_SHA256:
        raise ValueError("Exact BlackMesa.dll size/SHA-256 mismatch")
    pe = dnfile.dnPE(data=data)
    if pe.net is None or pe.net.mdtables is None:
        raise ValueError("Missing managed metadata")
    tables = pe.net.mdtables
    nested = {id(x.NestedClass.row): x.EnclosingClass.row for x in (tables.NestedClass or [])}

    def type_name(row):
        if row is None or not hasattr(row, "TypeName"):
            raise ValueError("Unresolved metadata type")
        name = str(row.TypeName)
        if id(row) in nested:
            return type_name(nested[id(row)]) + "+" + name
        return (str(row.TypeNamespace) + "." if str(row.TypeNamespace) else "") + name

    def token(index):
        if not index.row_index or index.row is None:
            raise ValueError("Null/unresolved metadata index")
        return f"0x{(index.table.number << 24) | index.row_index:08x}"

    def resolve_type(coded):
        tag, index = coded & 3, coded >> 2
        if tag not in (0, 1) or not index:
            raise ValueError("Unsupported TypeDefOrRef signature index")
        table = tables.TypeDef if tag == 0 else tables.TypeRef
        if table is None or index > len(table.rows):
            raise ValueError("Invalid TypeDefOrRef signature index")
        return type_name(table.rows[index - 1])

    def scope(row):
        index = getattr(row, "ResolutionScope", None)
        if index is None:
            return {"table": "TypeDef", "assembly": "BlackMesa.dll (exact input)"}
        target = index.row
        if target is None:
            raise ValueError("Unresolved TypeRef ResolutionScope")
        info = {"token": token(index), "table": index.table.name}
        if hasattr(target, "Name"):
            info["name"] = str(target.Name)
        if hasattr(target, "MajorVersion"):
            info["version"] = ".".join(str(getattr(target, x)) for x in
                                         ("MajorVersion", "MinorVersion", "BuildNumber", "RevisionNumber"))
            info["public_key_or_token_hex"] = target.PublicKey.value.hex()
        if hasattr(target, "TypeName"):
            info["enclosing_type"] = type_name(target)
            info["scope"] = scope(target)
        return info

    def flags(value):
        return sorted(k for k in dir(value) if not k.startswith("_")
                      and isinstance(getattr(value, k), bool) and getattr(value, k))

    owners, owner_rows, targets = {}, {}, {}
    for i, t in enumerate(tables.TypeDef, 1):
        identity = {"type": type_name(t), "type_token": f"0x{0x02000000 | i:08x}"}
        targets[id(t)] = identity
        for index in t.MethodList:
            owners[id(index.row)] = type_name(t)
            owner_rows[id(index.row)] = t
            targets[id(index.row)] = {**identity, "method": str(index.row.Name),
                                     "method_token": token(index),
                                     "signature_hex": index.row.Signature.value.hex()}
    blockers = []
    implmaps = []
    for i, row in enumerate(tables.ImplMap or [], 1):
        implmaps.append({"token": f"0x{0x1c000000 | i:08x}",
                        "member_token": token(row.MemberForwarded),
                        "mapping_flags_raw": row.struct.MappingFlags,
                        "mapping_flags": flags(row.MappingFlags),
                        "import_name": str(row.ImportName),
                        "import_scope_token": token(row.ImportScope),
                        "import_scope": str(row.ImportScope.row.Name)})
    bodyless, exceptional = [], []
    for i, m in enumerate(tables.MethodDef, 1):
        owner = owner_rows[id(m)]
        base = type_name(owner.Extends.row) if owner.Extends.row_index else None
        raw, impl = m.struct.Flags, m.struct.ImplFlags
        method_token = f"0x{0x06000000 | i:08x}"
        maps = [x for x in implmaps if x["member_token"] == method_token]
        semantics = {"code_type": ("IL", "native", "OPTIL", "runtime")[impl & 3],
                     "unmanaged": bool(impl & 4), "pinvoke_impl": bool(raw & 0x2000),
                     "abstract": bool(raw & 0x0400), "internal_call": bool(impl & 0x1000),
                     "forward_ref": bool(impl & 0x10), "unmanaged_export": bool(raw & 8),
                     "extern_keyword": "not a separate CLI metadata flag"}
        record = {**targets[id(m)], "rva": m.Rva, "owner_base_type": base,
                  "owner_base_scope": scope(owner.Extends.row) if owner.Extends.row_index else None,
                  "attributes_raw": raw, "attributes_hex": f"0x{raw:04x}",
                  "impl_flags_raw": impl, "impl_flags_hex": f"0x{impl:04x}",
                  "attributes": flags(m.Flags), "impl_flags": flags(m.ImplFlags),
                  "semantics": semantics, "impl_map": maps}
        external = maps or semantics["pinvoke_impl"] or semantics["unmanaged"] or semantics["internal_call"] or semantics["forward_ref"] or semantics["unmanaged_export"] or (impl & 3) in (1, 2)
        if external:
            exceptional.append(record)
            blockers.append("External/native/forwarded method requires review: " + method_token)
        if not m.Rva:
            if (not external and (impl & 3) == 3 and base == "System.MulticastDelegate"
                    and str(m.Name) in (".ctor", "Invoke", "BeginInvoke", "EndInvoke")
                    and not semantics["abstract"]):
                record["classification"] = "RUNTIME_PROVIDED_DELEGATE_MEMBER"
            elif not external and semantics["abstract"] and (impl & 3) == 0:
                record["classification"] = "ABSTRACT_DECLARATION_REQUIRES_DISPATCH_REVIEW"
                blockers.append("Abstract dispatch requires review: " + method_token)
            else:
                record["classification"] = "UNRESOLVED_NO_RVA"
                blockers.append("Unresolved RVA-less method: " + method_token)
            bodyless.append(record)
    if implmaps:
        blockers.append("ImplMap entries require external-path review")

    attributes, patch_attributes, dynamic_targets = [], [], []
    all_harmony_patch_count = 0
    for i, ca in enumerate(tables.CustomAttribute or [], 1):
        parent = targets.get(id(ca.Parent.row))
        ctor = ca.Type.row
        if ctor is None:
            raise ValueError("Unresolved custom-attribute constructor")
        if ca.Type.table.name == "MemberRef":
            declaring = ctor.Class.row
            attribute_name = type_name(declaring)
        elif ca.Type.table.name == "MethodDef":
            declaring = owner_rows[id(ctor)]
            attribute_name = owners[id(ctor)]
        else:
            raise ValueError("Unsupported custom-attribute constructor table")
        is_patch = attribute_name == "HarmonyLib.HarmonyPatch"
        all_harmony_patch_count += int(is_patch)
        in_scope = parent is not None and parent["type"].startswith("BlackMesa.Patches.")
        if not in_scope:
            if is_patch:
                blockers.append("HarmonyPatch outside requested namespace: " + token(ca.Parent))
            continue
        record = {"attribute_token": f"0x{0x0c000000 | i:08x}", "parent_token": token(ca.Parent),
                  "parent": parent, "attribute_type": attribute_name,
                  "attribute_scope": scope(declaring), "constructor_token": token(ca.Type),
                  "constructor_name": str(ctor.Name), "constructor_signature_hex": ctor.Signature.value.hex(),
                  "payload_hex": ca.Value.value.hex()}
        if attribute_name.startswith("HarmonyLib."):
            try:
                if str(ctor.Name) != ".ctor":
                    raise ValueError("Attribute constructor is not .ctor")
                record["decoded"] = decode_custom_attribute(ctor.Signature.value, ca.Value.value, resolve_type)
                record["decode_status"] = "COMPLETE"
            except Exception as exc:
                record["decode_status"] = "UNRESOLVED"
                record["error"] = str(exc)
                blockers.append("Attribute decode failed: " + record["attribute_token"])
        else:
            record["decode_status"] = "RAW_NON_HARMONY_ATTRIBUTE"
        attributes.append(record)
        if is_patch:
            patch_attributes.append(record)
        if attribute_name in ("HarmonyLib.HarmonyTargetMethod", "HarmonyLib.HarmonyTargetMethods"):
            dynamic_targets.append(record)
    patch_types = []
    for i, t in enumerate(tables.TypeDef, 1):
        name = type_name(t)
        if not name.startswith("BlackMesa.Patches."):
            continue
        methods = []
        for index in t.MethodList:
            m = index.row
            attrs = [x for x in attributes if x["parent_token"] == token(index)]
            methods.append({**targets[id(m)], "rva": m.Rva,
                            "attribute_tokens": [x["attribute_token"] for x in attrs]})
            if str(m.Name) in ("TargetMethod", "TargetMethods"):
                dynamic_targets.append({**targets[id(m)], "reason": "Harmony convention name"})
        patch_types.append({"type": name, "type_token": f"0x{0x02000000 | i:08x}",
                            "methods": methods})
    if dynamic_targets:
        blockers.append("Dynamic Harmony target resolver requires focused review")
    # Preserve the declared fragments by exact parent token. Do not invent
    # overload identity or merge contradictory class/method declarations.
    declarations = []
    for entry in patch_types:
        class_patches = [x for x in patch_attributes if x["parent_token"] == entry["type_token"]]
        for m in entry["methods"]:
            method_attrs = [x for x in attributes if x["parent_token"] == m["method_token"]]
            method_patches = [x for x in method_attrs if x["attribute_type"] == "HarmonyLib.HarmonyPatch"]
            roles = [x["attribute_type"] for x in method_attrs if x["attribute_type"] in
                     ("HarmonyLib.HarmonyPrefix", "HarmonyLib.HarmonyPostfix", "HarmonyLib.HarmonyTranspiler", "HarmonyLib.HarmonyFinalizer", "HarmonyLib.HarmonyReversePatch")]
            if method_patches or roles or m["method"] in ("Prefix", "Postfix", "Transpiler", "Finalizer"):
                fragments = class_patches + method_patches
                declarations.append({"patch_method": m, "roles": roles,
                                     "class_attribute_tokens": [x["attribute_token"] for x in class_patches],
                                     "method_attribute_tokens": [x["attribute_token"] for x in method_patches],
                                     "declared_target_fragments": [x.get("decoded") for x in fragments]})
                if not fragments:
                    blockers.append("Patch method without target declaration: " + m["method_token"])
    coverage = {"type_defs": len(tables.TypeDef.rows), "method_defs": len(tables.MethodDef.rows),
                "methods_with_rva": sum(bool(x.Rva) for x in tables.MethodDef),
                "methods_without_rva": len(bodyless), "impl_map_rows": len(implmaps),
                "custom_attribute_rows_inspected": len(tables.CustomAttribute.rows),
                "patch_types": len(patch_types), "scoped_attributes": len(attributes),
                "assembly_harmony_patch_attributes": all_harmony_patch_count,
                "scoped_harmony_patch_attributes": len(patch_attributes),
                "decoded_harmony_patch_attributes": sum(x.get("decode_status") == "COMPLETE" for x in patch_attributes)}
    if (coverage["type_defs"], coverage["method_defs"], coverage["methods_with_rva"], len(bodyless)) != (91, 576, 568, 8):
        blockers.append("Exact v2 metadata coverage mismatch")
    if not patch_types or not patch_attributes or not declarations:
        blockers.append("No usable Harmony target metadata")
    blockers = sorted(set(blockers))
    return {"schema_version": "phase-c3f3-metadata-1", "package": PACKAGE, "version": VERSION,
            "dll_member": DLL_MEMBER, "dll_bytes": len(data), "dll_sha256": sha256(data),
            "gate_status": "UNRESOLVED" if blockers else "METADATA_CAPTURE_COMPLETE_REVIEW_REQUIRED",
            "coverage": coverage, "methods_without_rva": bodyless, "exceptional_methods": exceptional,
            "impl_maps": implmaps, "patch_types": patch_types, "scoped_custom_attributes": attributes,
            "harmony_target_declarations": declarations, "dynamic_target_resolvers": dynamic_targets,
            "blockers": blockers,
            "summary": {**coverage, "blockers": len(blockers)},
            "proof_boundary": "Static metadata capture, not automatic C3F3 clearance. Review exact class/method target fragments together with existing v2 IL evidence. Declared target types/names are not proof of external overload resolution, final patch order, actual runtime behavior or general interior compatibility. No mod assembly is loaded or executed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--metadata-only", action="store_true",
                        help="Capture metadata gate without repeating the v2 IL scan")
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
        report = capture_metadata(data) if args.metadata_only else capture(data)
        report["tools"] = versions
        report["zip_bytes"] = len(raw)
        report["zip_sha256"] = sha256(raw)
        output = args.out / ("BLACK_MESA_344_METADATA_GATE.json" if args.metadata_only
                             else "BLACK_MESA_344_DLL_ENTRANCE_IL.json")
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["summary"], indent=2))
        if args.metadata_only and report["gate_status"] != "METADATA_CAPTURE_COMPLETE_REVIEW_REQUIRED":
            raise ValueError("Metadata gate is unresolved; inspect raw evidence and blockers")
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
