#!/usr/bin/env python3
"""Read-only CodeRebirth 1.6.9 package/bundle inventory; no gameplay execution.

Usage: python inspect_universal_interior_c3e3a.py --zip PACKAGE.zip --out OUTPUT
Requires UnityPy==1.25.3. Does not extract entrance IDs or start Unity.
Expected package hashes come from the canonical native-owner manifest.
"""
import argparse
import collections
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path
import struct
import zipfile

EXPECTED_ZIP_SHA256 = 'a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6'
EXPECTED_ZIP_BYTES = 263010364
EXPECTED_DLLS = {
    'plugins/CodeRebirth/CodeRebirth.dll': 'a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36',
    'plugins/CodeRebirth/com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll': '308ddf095d807b719c204c48bee3ce26795281c6b399baf3ac105e6b9d258163',
}
PREFIX = 'plugins/CodeRebirth/Assets/'
TARGETS = ['oxydeassets', 'oxydecrashshipassets', 'oxydeloreassets', 'oxydescene']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def header(data):
    stream = io.BytesIO(data)
    def cstring():
        value = bytearray()
        while True:
            b = stream.read(1)
            if not b:
                raise ValueError('Unterminated UnityFS header')
            if b == b'\0':
                return value.decode('ascii')
            value.extend(b)
    signature = cstring()
    if signature != 'UnityFS':
        raise ValueError('Unexpected bundle signature')
    fmt = struct.unpack('>I', stream.read(4))[0]
    player, revision = cstring(), cstring()
    size, compressed, uncompressed, flags = struct.unpack('>QIII', stream.read(20))
    if size != len(data):
        raise ValueError('Bundle header size mismatch')
    return dict(signature=signature, format_version=fmt, player_version=player,
                unity_revision=revision, declared_bytes=size,
                compressed_block_info_bytes=compressed,
                uncompressed_block_info_bytes=uncompressed, flags=flags)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    with args.zip.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    if args.zip.stat().st_size != EXPECTED_ZIP_BYTES or digest != EXPECTED_ZIP_SHA256:
        raise ValueError('Exact package SHA/size mismatch; refusing inspection')
    import UnityPy
    version = importlib.metadata.version('UnityPy')
    if version != '1.25.3':
        raise ValueError('Expected UnityPy 1.25.3')
    args.out.mkdir(parents=True, exist_ok=True)
    result = {'package': 'XuXiaolan-CodeRebirth', 'version': '1.6.9',
              'zip_sha256': digest, 'zip_bytes': EXPECTED_ZIP_BYTES,
              'unitypy_version': version, 'assemblies': [], 'bundles': [],
              'executed_game_or_mod_code': False, 'entrance_id_extraction_performed': False}
    with zipfile.ZipFile(args.zip) as archive:
        for name, expected in EXPECTED_DLLS.items():
            digest = sha(archive.read(name))
            if digest != expected:
                raise ValueError('Assembly SHA mismatch: ' + name)
            result['assemblies'].append({'member': name, 'sha256': digest})
        for name in TARGETS:
            member = archive.getinfo(PREFIX + name)
            data = archive.read(member)
            row = {'member': member.filename, 'bytes': len(data),
                   'zip_compressed_bytes': member.compress_size,
                   'sha256': sha(data), 'header': header(data)}
            if name in ('oxydeassets', 'oxydescene'):
                # Pass bytes: no directory crawling and no managed assembly execution.
                env = UnityPy.load(data)
                objects = list(env.objects)
                row['static_reader'] = {'object_count': len(objects),
                    'type_counts': dict(sorted(collections.Counter(o.type.name for o in objects).items())),
                    'serialized_files': []}
                assets = {id(o.assets_file): o.assets_file for o in objects}
                for asset in assets.values():
                    row['static_reader']['serialized_files'].append({
                        'name': asset.name, 'unity_version': asset.unity_version,
                        'externals': [str(x.path) for x in asset.externals],
                        'type_tree_enabled': asset._enable_type_tree,
                        'object_count': len(asset.objects)})
                # Probe one MonoBehaviour for parser readiness only. Do not report values.
                mono = next((o for o in objects if o.type.name == 'MonoBehaviour'), None)
                if mono is not None:
                    try:
                        tree = mono.read_typetree()
                        row['static_reader']['monobehaviour_probe'] = {
                            'path_id': mono.path_id, 'serialized_file': mono.assets_file.name, 'success': True,
                            'top_level_field_names': list(tree.keys())}
                    except Exception as exc:
                        row['static_reader']['monobehaviour_probe'] = {
                            'path_id': mono.path_id, 'serialized_file': mono.assets_file.name, 'success': False,
                            'error_type': type(exc).__name__, 'error': str(exc)}
                del objects, env
            result['bundles'].append(row)
    output = args.out / 'OXYDE_PACKAGE_BUNDLE_INVENTORY.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
