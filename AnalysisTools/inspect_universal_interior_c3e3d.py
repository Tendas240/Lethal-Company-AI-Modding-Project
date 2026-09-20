#!/usr/bin/env python3
"""Hash-bound owner registration IL and narrow field-use inventory for C3E3D.

Requires dnfile==0.18.0 and dncil==1.0.2. Reads six pinned owner DLLs from
verified CodeRebirth 1.6.9 / DawnLib 0.9.25 ZIPs. Executes no managed code.
Does not inspect other mods, resolve reflection or establish runtime hook order.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import zipfile
import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

MANIFEST = 'SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json'
MANIFEST_GIT_BLOB = '77e77022d3cbdd742d57013f66812c0e8a336c64'
FIELDS = {'.SelectableLevel::spawnEnemiesAndScrap', '.SelectableLevel::dungeonFlowTypes'}
SELECTED = {
 'CodeRebirth.src.Content.Moons.MoonHandler': {'.ctor'},
 'CodeRebirth.src.Content.Moons.MoonHandler+OxydeAssets': {'.ctor'},
 'Dusk.ContentHandler': {'RegisterContent', 'TryLoadContentBundle', 'LoadAllContent'},
 'Dusk.AssetBundleLoader`1': {'.ctor'},
 'Dusk.DuskContentDefinition': {'Register', 'RegisterPost', 'RegisterConfigs'},
 'Dusk.DuskMoonDefinition': {'Register', 'CreateMoonConfig', 'TryNetworkRegisterAssets'},
 'Dusk.DuskMoonDefinition+<>c__DisplayClass57_0': {'<Register>b__0'},
 'Dawn.DawnLib': {'DefineMoon'},
 'Dawn.MoonInfoBuilder': {'.ctor', 'AddScene', 'Build'},
 'Dawn.DawnMoonInfo': {'.ctor'},
 'Dawn.MoonRegistrationHandler': {'Init', 'RegisterDawnLevels'},
 'Dawn.MoonRegistrationHandler+<>c': {'<Init>b__2_0'},
 'Dawn.DungeonRegistrationHandler': {'Init', 'AddDawnDungeonsToMoons', 'UpdateDungeonWeightOnLevel'},
 'Dawn.DungeonRegistrationHandler+<>c': {'<Init>b__0_0', '<Init>b__0_1', '<Init>b__0_2'},
}


def capture(data):
    pe = dnfile.dnPE(data=data)
    nested = {id(n.NestedClass.row): n.EnclosingClass.row for n in (pe.net.mdtables.NestedClass or [])}
    def defined_type_name(row):
        if id(row) in nested:
            return defined_type_name(nested[id(row)]) + '+' + str(row.TypeName)
        return str(row.TypeNamespace) + '.' + str(row.TypeName)
    method_owners = {}
    field_owners = {}
    for t in pe.net.mdtables.TypeDef:
        name = defined_type_name(t)
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
            return defined_type_name(row)
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
            return 'MethodSpec(' + resolve((row.Method.table.number << 24) | row.Method.row_index) + '; instantiation=' + row.Instantiation.value.hex() + ')'
        if table in (1, 2, 27):
            return type_name(row)
        if table == 6:
            return method_owners[id(row)] + '::' + str(row.Name)
        if table == 4:
            return field_owners[id(row)] + '::' + str(row.Name)
        return type_name(row.Class.row) + '::' + str(row.Name)

    methods, hits, literal_hits = [], [], []
    inspected, no_body = 0, 0
    for t in pe.net.mdtables.TypeDef:
        name = defined_type_name(t)
        for mr in t.MethodList:
            m = mr.row
            if not m.Rva:
                no_body += 1
                continue
            body = read_method_body_from_bytes(pe.get_data(m.Rva, 100000))
            inspected += 1
            identity = {'type': name, 'method': str(m.Name), 'method_token': f'0x{0x06000000 | mr.row_index:08x}',
                        'rva': m.Rva, 'signature_hex': m.Signature.value.hex()}
            instructions = []
            for ins in body.instructions:
                operand = ins.operand
                token = operand.value if hasattr(operand, 'value') else None
                decoded = None if token is None else resolve(token)
                record = {'offset': ins.offset, 'opcode': ins.opcode.name,
                          'operand': None if operand is None else str(operand),
                          'resolved_token': decoded}
                instructions.append(record)
                if decoded in FIELDS:
                    hits.append({**identity, **record})
                if ins.opcode.name == 'ldstr' and decoded in (repr('spawnEnemiesAndScrap'), repr('dungeonFlowTypes')):
                    literal_hits.append({**identity, **record})
            if str(m.Name) in SELECTED.get(name, set()):
                methods.append({**identity, 'instructions': instructions})
    return {'assembly_sha256': hashlib.sha256(data).hexdigest(),
            'coverage': {'method_bodies_scanned': inspected, 'methods_without_body': no_body, 'parse_errors': 0},
            'field_opcode_counts': dict(Counter(h['opcode'] for h in hits)),
            'field_references': hits, 'exact_field_name_string_literals': literal_hits,
            'selected_methods': methods}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--coderebirth-package', type=Path, required=True)
    parser.add_argument('--dawnlib-package', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    tools = {n: importlib.metadata.version(n) for n in ('dnfile', 'dncil')}
    if tools != {'dnfile': '0.18.0', 'dncil': '1.0.2'}:
        raise ValueError('Parser version mismatch')
    raw = (args.repo / MANIFEST).read_bytes()
    if hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != MANIFEST_GIT_BLOB:
        raise ValueError('Native-owner manifest changed')
    manifest = json.loads(raw)
    packages = {'XuXiaolan-CodeRebirth': args.coderebirth_package, 'TeamXiaolan-DawnLib': args.dawnlib_package}
    report = {'schema_version': 'phase-c3e3d-1', 'tools': tools, 'manifest': MANIFEST,
              'manifest_git_blob': MANIFEST_GIT_BLOB, 'packages': [], 'assemblies': [],
              'proof_boundary': 'Static direct IL field references and selected owner methods only. No other mods, arbitrary reflection, runtime patch order, client generation body or topology proof.'}
    for package in manifest['packages']:
        if package['package'] not in packages:
            continue
        path = packages[package['package']]
        raw = path.read_bytes()
        if len(raw) != package['zip_bytes'] or hashlib.sha256(raw).hexdigest() != package['zip_sha256']:
            raise ValueError('Package size/SHA-256 mismatch')
        report['packages'].append({k: package[k] for k in ('package', 'version', 'url', 'zip_bytes', 'zip_sha256')})
        with zipfile.ZipFile(path) as archive:
            for assembly in package['assemblies']:
                data = archive.read(assembly['member'])
                if hashlib.sha256(data).hexdigest() != assembly['sha256']:
                    raise ValueError('Assembly SHA-256 mismatch')
                report['assemblies'].append({'package': package['package'], 'member': assembly['member'], **capture(data)})
    if len(report['assemblies']) != 6:
        raise ValueError('Expected exactly six assemblies')
    methods = [m for a in report['assemblies'] for m in a['selected_methods']]
    expected = {(t, m) for t, ms in SELECTED.items() for m in ms}
    if {(m['type'], m['method']) for m in methods} != expected:
        raise ValueError('Selected method capture incomplete')
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'OXYDE_OWNER_REGISTRATION_IL.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'assemblies': len(report['assemblies']), 'selected_methods': len(methods),
                      'method_bodies_scanned': sum(a['coverage']['method_bodies_scanned'] for a in report['assemblies']),
                      'field_references': sum(len(a['field_references']) for a in report['assemblies'])}))


if __name__ == '__main__':
    main()
