#!/usr/bin/env python3
"""Capture selected IL from repository-pinned DawnLib; no Unity/game execution.

Requires dnfile and dncil. Usage:
  python inspect_universal_interior_c3a.py DAWNLIB_DLL OUTPUT_JSON
The input must match the existing native-owner evidence manifest exactly.
"""
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

EXPECTED_SHA256 = '9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b'
SELECTED = {
    'Dawn.NamespacedKey': {'Vanilla', 'IsVanilla'},
    'Dawn.LethalContent': {'.cctor'},
    'Dawn.TaggedRegistry`1': {'.ctor', 'Freeze'},
    'Dawn.CustomAutoTagger`1': {'get_Tag', 'ShouldApply'},
    'Dawn.VanillaAutoTagger`1': {'ShouldApply'},
    'Dawn.AllAutoTagger`1': {'get_Tag', 'ShouldApply'},
    'Dawn.Tags': {'.cctor'},
    'Dawn.HasTagWeightContextualProvider`2': {'Provide'},
    'Dawn.Internal.LethalLevelLoaderCompat': {'EnsureCorrectDawnDungeonDynamicRarity'},
}


def capture(path):
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        raise ValueError('Refusing unverified DawnLib assembly: ' + sha)
    pe = dnfile.dnPE(data=data)
    method_owners = {}
    field_owners = {}
    for t in pe.net.mdtables.TypeDef:
        name = str(t.TypeNamespace) + '.' + str(t.TypeName)
        method_owners.update({id(m.row): name for m in t.MethodList})
        field_owners.update({id(f.row): name for f in t.FieldList})

    def compressed(b, i):
        x = b[i]
        if x < 128:
            return x, i + 1
        if x < 192:
            return ((x & 63) << 8) | b[i+1], i + 2
        return ((x & 31) << 24) | (b[i+1] << 16) | (b[i+2] << 8) | b[i+3], i + 4

    def type_name(row):
        if hasattr(row, 'TypeName'):
            return str(row.TypeNamespace) + '.' + str(row.TypeName)
        if hasattr(row, 'Signature'):
            b = row.Signature.value
            if b[:2] in (b'\x15\x12', b'\x15\x11'):
                coded, _ = compressed(b, 2)
                table = [pe.net.mdtables.TypeDef, pe.net.mdtables.TypeRef,
                         pe.net.mdtables.TypeSpec][coded & 3]
                return type_name(table.rows[(coded >> 2)-1]) + ' [signature=' + b.hex() + ']'
            return 'TypeSpec[signature=' + b.hex() + ']'
        return type(row).__name__

    def resolve(v):
        table, idx = v >> 24, v & 0xffffff
        if table == 0x70:
            return repr(pe.net.user_strings.get(idx).value)
        names = {1: 'TypeRef', 2: 'TypeDef', 4: 'Field', 6: 'MethodDef',
                 10: 'MemberRef', 27: 'TypeSpec', 43: 'MethodSpec'}
        if table not in names:
            return f'token(0x{v:08x})'
        row = getattr(pe.net.mdtables, names[table]).rows[idx-1]
        if table == 43:
            return 'MethodSpec(' + resolve((row.Method.table.number << 24) | row.Method.row_index) + ')'
        if table in (1, 2, 27):
            return type_name(row)
        if table == 6:
            return method_owners[id(row)] + '::' + str(row.Name)
        if table == 4:
            return field_owners[id(row)] + '::' + str(row.Name)
        return type_name(row.Class.row) + '::' + str(row.Name)

    methods = []
    for t in pe.net.mdtables.TypeDef:
        name = str(t.TypeNamespace) + '.' + str(t.TypeName)
        for mr in t.MethodList:
            m = mr.row
            if str(m.Name) not in SELECTED.get(name, set()):
                continue
            body = read_method_body_from_bytes(pe.get_data(m.Rva, 100000))
            instructions = []
            for ins in body.instructions:
                operand = ins.operand
                token = operand.value if hasattr(operand, 'value') else None
                instructions.append({
                    'offset': ins.offset, 'opcode': ins.opcode.name,
                    'operand': None if operand is None else str(operand),
                    'resolved_token': None if token is None else resolve(token),
                })
            methods.append({'type': name, 'method': str(m.Name),
                            'method_token': f'0x{0x06000000 | mr.row_index:08x}',
                            'rva': m.Rva, 'signature_hex': m.Signature.value.hex(),
                            'instructions': instructions})
    expected = {(t, m) for t, ms in SELECTED.items() for m in ms}
    if {(m['type'], m['method']) for m in methods} != expected:
        raise ValueError('Selected method capture incomplete')
    return {'schema_version': 1, 'package': 'TeamXiaolan-DawnLib', 'version': '0.9.25',
            'assembly_sha256': sha,
            'tools': {n: importlib.metadata.version(n) for n in ('dnfile', 'dncil')},
            'qualification': 'Static selected-method IL only; generic signatures retained; not a runtime tag dump or topology proof.',
            'methods': methods}


if __name__ == '__main__':
    result = capture(Path(sys.argv[1]))
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Captured {len(result["methods"])} methods from verified DawnLib 0.9.25')
