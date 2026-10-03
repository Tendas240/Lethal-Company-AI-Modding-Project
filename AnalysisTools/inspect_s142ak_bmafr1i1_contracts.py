#!/usr/bin/env python3
"""Read existing, hash-pinned DLL metadata/IL; never load, execute or compile them.

Requires dnfile==0.17.0 and dncil==1.0.2. Input: directory of already-extracted
package DLLs. Output: deterministic JSON on stdout. No network or writes.
"""
import hashlib
import json
import sys
from pathlib import Path

import dnfile
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBytes

EXPECTED = {
    "CodeRebirth.dll": "a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36",
    "com.github.teamxiaolan.dawnlib.dusk.dll": "3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03",
}
TARGETS = {
    "CodeRebirth.src.Content.Enemies.Janitor": {
        "SetBlendShapeWeightClientRpc", "KillEnemy", "KeepPlayerAttachedDuringZoom", "SwitchToChaseState",
    },
    "Dusk.Internal.EntityReplacementRegistrationPatch": {"ReplaceEnemyEntity"},
    "Dusk.SkinnedMeshReplacement": {"ReplaceSkinnedMeshRenderer", "BuildBoneLookup", "get_ReplacementRenderer"},
    "Dusk.MaterialsReplacement": {"CopyOrResizeMaterials"},
    "Dusk.DuskEntityReplacementDefinition": {"get_Replacements", "get_SkinName"},
    "Dusk.Hierarchy": {"get_HierarchyPath"},
    "Dusk.DuskEnemyReplacementDefinition": {"Apply"},
}


class Reader:
    def __init__(self, path):
        self.pe = dnfile.dnPE(str(path))
        self.tables = self.pe.net.mdtables.tables
        self.nested = {id(n.NestedClass.row): n.EnclosingClass.row for n in (self.pe.net.mdtables.NestedClass or [])}
        self.owners = {}
        for t in self.pe.net.mdtables.TypeDef:
            for x in list(t.MethodList) + list(t.FieldList):
                self.owners[id(x.row)] = self.typename(t)

    def typename(self, row):
        if row.__class__.__name__ == "TypeSpecRow":
            return self.type(iter(row.Signature.value))
        if id(row) in self.nested:
            return self.typename(self.nested[id(row)]) + "+" + str(row.TypeName)
        ns = str(row.TypeNamespace)
        scope = getattr(row, "ResolutionScope", None)
        if scope and scope.row.__class__.__name__ == "TypeRefRow":
            return self.typename(scope.row) + "+" + str(row.TypeName)
        return (ns + "." if ns else "") + str(row.TypeName)

    @staticmethod
    def uint(it):
        a = next(it)
        if a & 0x80 == 0:
            return a
        if a & 0xc0 == 0x80:
            return ((a & 0x3f) << 8) | next(it)
        return ((a & 0x1f) << 24) | (next(it) << 16) | (next(it) << 8) | next(it)

    def coded_type(self, value):
        table = (2, 1, 27)[value & 3]
        return self.typename(self.tables[table].rows[(value >> 2) - 1])

    def type(self, it):
        tag = next(it)
        simple = {1: "System.Void", 2: "System.Boolean", 3: "System.Char", 4: "System.SByte", 5: "System.Byte", 6: "System.Int16", 7: "System.UInt16", 8: "System.Int32", 9: "System.UInt32", 10: "System.Int64", 11: "System.UInt64", 12: "System.Single", 13: "System.Double", 14: "System.String", 24: "System.IntPtr", 25: "System.UIntPtr", 28: "System.Object"}
        if tag in simple:
            return simple[tag]
        if tag in (17, 18):
            return self.coded_type(self.uint(it))
        if tag in (19, 30):
            return ("!" if tag == 19 else "!!") + str(self.uint(it))
        if tag in (15, 16, 29, 69):
            return self.type(it) + {15: "*", 16: "&", 29: "[]", 69: " pinned"}[tag]
        if tag == 21:
            base = self.type(it)
            return base + "<" + ",".join(self.type(it) for _ in range(self.uint(it))) + ">"
        raise ValueError("Unsupported signature element: " + hex(tag))

    def signature(self, raw):
        it = iter(raw)
        flags = next(it)
        if flags == 6:
            return {"field_type": self.type(it)}
        if flags == 7:
            return {"locals": [self.type(it) for _ in range(self.uint(it))]}
        generic_count = self.uint(it) if flags & 0x10 else 0
        count = self.uint(it)
        result = {"has_this": bool(flags & 0x20), "generic_parameter_count": generic_count,
                  "return_type": self.type(it), "parameter_types": [self.type(it) for _ in range(count)]}
        if list(it):
            raise ValueError("Unconsumed signature bytes")
        return result

    def token(self, value):
        table, rid = value >> 24, value & 0xffffff
        if table == 0x70:
            return {"string": self.pe.net.user_strings.get(rid).value}
        row = self.tables[table].rows[rid - 1]
        if table in (1, 2, 27):
            return {"type": self.typename(row)}
        if table == 43:
            return {"method_spec": self.member(row.Method.row), "instantiation_hex": row.Instantiation.value.hex()}
        if table == 17:
            return self.signature(row.Signature.value)
        return self.member(row)

    def member(self, row):
        owner = self.owners.get(id(row))
        if owner is None:
            owner = self.typename(row.Class.row)
        return {"owner": owner, "name": str(row.Name), **self.signature(row.Signature.value)}

    def method(self, row):
        body = CilMethodBody(CilMethodBodyReaderBytes(self.pe.get_data(row.Rva)))
        def operand(x):
            op = x.operand
            if hasattr(op, "value"):
                return self.token(op.value)
            if hasattr(op, "index") and not isinstance(op, (str, list, tuple)):
                return {"slot": op.index}
            return op
        result = {**self.member(row), "signature_hex": row.Signature.value.hex(),
                  "access": "public" if row.Flags.mdPublic else "private" if row.Flags.mdPrivate else "assembly" if row.Flags.mdAssem else "other",
                  "static": bool(row.Flags.mdStatic), "virtual": bool(row.Flags.mdVirtual),
                  "parameters": [{"name": str(p.row.Name), "sequence": p.row.Sequence, "optional": bool(p.row.Flags.pdOptional)} for p in row.ParamList],
                  "method_body_sha256": hashlib.sha256(body.raw_bytes).hexdigest(),
                  "il_sha256": hashlib.sha256(body.raw_bytes[body.header_size:body.header_size + body.code_size]).hexdigest(),
                  "il_bytes_hex": body.raw_bytes[body.header_size:body.header_size + body.code_size].hex(),
                  "max_stack": body.max_stack,
                  "init_locals": bool(body.flags.InitLocals),
                  "il": [{"offset": x.offset - body.header_size, "opcode": x.opcode.name, "operand": operand(x)} for x in body.instructions]}
        # dncil reports branch targets including the method header, normalize to IL offsets.
        for ins in result["il"]:
            op = ins["opcode"]
            if op.startswith(("br", "beq", "bge", "bgt", "ble", "blt", "bne", "leave")) and isinstance(ins["operand"], int):
                ins["operand"] -= body.header_size
            if op == "switch":
                ins["operand"] = [x - body.header_size for x in ins["operand"]]
        result["locals"] = self.token(body.local_var_sig_tok.value)["locals"] if body.local_var_sig_tok else []
        result["exception_handler_count"] = len(body.exception_handlers)
        result["exception_handlers"] = [
            {"kind": int(e.exception_type), "try_start": e.try_start, "try_end": e.try_end,
             "handler_start": e.handler_start, "handler_end": e.handler_end,
             "filter_start": e.filter_start,
             "catch_type": self.token(e.catch_type.value) if e.catch_type else None}
            for e in body.exception_handlers
        ]
        return result


def main():
    root = Path(sys.argv[1])
    output = {"schema_version": 1, "source_id": "S1.42AK-BMAFR1I1", "status": "EXACT_DEPENDENCY_CONTRACT_PREPARATION_ONLY_IMPLEMENTATION_PENDING", "tools": {"dnfile": "0.17.0", "dncil": "1.0.2"}, "assemblies": []}
    seen = set()
    for filename, expected in EXPECTED.items():
        path = root / filename
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("Exact dependency SHA-256 mismatch: " + filename)
        reader = Reader(path)
        assembly = {"file": filename, "sha256": actual, "methods": [], "fields": []}
        for t in reader.pe.net.mdtables.TypeDef:
            name = reader.typename(t)
            if name not in TARGETS:
                continue
            for mi in t.MethodList:
                m = mi.row
                if str(m.Name) in TARGETS[name]:
                    key = (name, str(m.Name))
                    if key in seen:
                        raise ValueError("Ambiguous target: " + str(key))
                    seen.add(key)
                    assembly["methods"].append(reader.method(m))
            for fi in t.FieldList:
                if str(fi.row.Name) == "IsDefault":
                    assembly["fields"].append(reader.member(fi.row))
        output["assemblies"].append(assembly)
    if seen != {(t, m) for t, methods in TARGETS.items() for m in methods}:
        raise ValueError("Missing exact declared target")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
