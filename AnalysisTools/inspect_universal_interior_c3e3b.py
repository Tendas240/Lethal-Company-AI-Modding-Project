#!/usr/bin/env python3
"""Scan exact Oxyde scene serialization for EntranceTeleport, without Unity execution.

Requires UnityPy==1.25.3. Input bundle is hash-bound to C3E3A package evidence.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re

EXPECTED_SHA256 = '6b6dc42c2bef7d858e7e2efa2573df3e1c2bc8507cc7c3840483f0f6c1b0e883'
EXPECTED_BYTES = 55038216
ENTRANCE_FIELDS = {'entranceId', 'isEntranceToBuilding', 'entrancePoint', 'exitPoint'}
DYNAMIC_CLASSES = {'SpawnSyncedDawnLibObject', 'UnlockProgressiveObject', 'ChanceScript'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    data = args.bundle.read_bytes()
    if len(data) != EXPECTED_BYTES or hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Exact Oxyde bundle size/hash mismatch')
    import UnityPy
    version = importlib.metadata.version('UnityPy')
    if version != '1.25.3':
        raise ValueError('Expected UnityPy 1.25.3')
    env = UnityPy.load(data)
    objects = list(env.objects)
    files = {o.assets_file.name: o.assets_file for o in objects}
    if len(files) != len({id(o.assets_file) for o in objects}):
        raise ValueError('Ambiguous serialized-file names')
    by_id = {(o.assets_file.name, o.path_id): o for o in objects}
    cache = {}
    def identity(o):
        return {'serialized_file': o.assets_file.name, 'path_id': o.path_id, 'type': o.type.name}
    def read(o):
        key = (o.assets_file.name, o.path_id)
        if key not in cache:
            cache[key] = o.read_typetree()
        return cache[key]
    def resolve(owner, ptr):
        if not isinstance(ptr, dict) or 'm_PathID' not in ptr or 'm_FileID' not in ptr:
            return None, 'MALFORMED_POINTER'
        if ptr['m_PathID'] == 0:
            return None, 'NULL'
        fid = ptr['m_FileID']
        if fid == 0:
            name = owner.assets_file.name
        else:
            if fid < 1 or fid > len(owner.assets_file.externals):
                return None, 'INVALID_EXTERNAL_INDEX'
            path = str(owner.assets_file.externals[fid-1].path)
            name = path.replace('\\', '/').rsplit('/', 1)[-1]
            if name not in files:
                return None, 'EXTERNAL_NOT_IN_BUNDLE:' + path
        obj = by_id.get((name, ptr['m_PathID']))
        return (obj, 'RESOLVED') if obj else (None, 'PATH_ID_NOT_FOUND:' + name)
    def describe_pointer(owner, ptr):
        target, status = resolve(owner, ptr)
        result = {'pointer': ptr, 'status': status}
        if target:
            result['target'] = identity(target)
            if target.type.name in ('GameObject', 'Transform'):
                result['target_data'] = read(target)
        return result
    def field_hits(value, prefix=''):
        hits = []
        if isinstance(value, dict):
            for key, item in value.items():
                path = prefix + '.' + key if prefix else key
                if key in ENTRANCE_FIELDS:
                    hits.append({'field_path': path, 'value': item})
                hits.extend(field_hits(item, path))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                hits.extend(field_hits(item, prefix + '[' + str(i) + ']'))
        return hits
    scripts = []
    script_map = {}
    for obj in objects:
        if obj.type.name != 'MonoScript':
            continue
        tree = read(obj)
        record = {**identity(obj), 'class': tree.get('m_ClassName'),
                  'namespace': tree.get('m_Namespace'), 'assembly': tree.get('m_AssemblyName')}
        scripts.append(record)
        script_map[(obj.assets_file.name, obj.path_id)] = record
    counts, script_status = Counter(), Counter()
    errors, problems, matches, dynamic = [], [], [], []
    parsed = 0
    for obj in objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        try:
            tree = read(obj)
        except Exception as exc:
            errors.append({**identity(obj), 'error_type': type(exc).__name__, 'error': str(exc)})
            continue
        parsed += 1
        script, status = resolve(obj, tree.get('m_Script'))
        descriptor = script_map.get((script.assets_file.name, script.path_id)) if script else None
        if status == 'RESOLVED' and descriptor is None:
            status = 'RESOLVED_NOT_MONOSCRIPT'
        script_status[status] += 1
        if descriptor:
            key = descriptor['assembly'] + ':' + descriptor['namespace'] + '.' + descriptor['class']
            counts[key] += 1
        else:
            problems.append({**identity(obj), 'm_Script': tree.get('m_Script'), 'status': status,
                             'serialized_fields': tree,
                             'raw_object_bytes': obj.byte_size,
                             'raw_object_sha256': hashlib.sha256(obj.get_raw_data()).hexdigest(),
                             'raw_object_hex': obj.get_raw_data().hex() if obj.byte_size <= 128 else None,
                             'game_object': describe_pointer(obj, tree.get('m_GameObject'))})
        hits = field_hits(tree)
        exact_entrance = bool(descriptor and descriptor['class'] == 'EntranceTeleport')
        if exact_entrance or hits:
            record = {**identity(obj), 'script': descriptor, 'exact_entrance_class': exact_entrance,
                      'field_hits': hits, 'serialized_fields': tree,
                      'game_object': describe_pointer(obj, tree.get('m_GameObject'))}
            for field in ('entrancePoint', 'exitPoint'):
                if field in tree:
                    record[field + '_resolution'] = describe_pointer(obj, tree[field])
            matches.append(record)
        if descriptor and descriptor['class'] in DYNAMIC_CLASSES:
            dynamic.append({**identity(obj), 'script': descriptor, 'serialized_fields': tree,
                            'game_object': describe_pointer(obj, tree.get('m_GameObject'))})
    names = []
    name_errors = []
    for obj in objects:
        if obj.type.name != 'GameObject':
            continue
        try:
            tree = read(obj)
            if re.search(r'entrance|fire.?exit|teleport|dungeon', tree.get('m_Name', ''), re.I):
                component_records = []
                for entry in tree.get('m_Component', []):
                    ptr = entry.get('component')
                    component, status = resolve(obj, ptr)
                    record = {'pointer': ptr, 'status': status}
                    if component:
                        record['target'] = identity(component)
                        record['serialized_fields'] = read(component)
                    component_records.append(record)
                names.append({**identity(obj), 'name': tree.get('m_Name'),
                              'active_self': tree.get('m_IsActive'), 'components': component_records})
        except Exception as exc:
            name_errors.append({**identity(obj), 'error': str(exc)})
    report = {'schema_version': 'phase-c3e3b-1', 'bundle_member': 'plugins/CodeRebirth/Assets/oxydescene',
              'bundle_sha256': EXPECTED_SHA256, 'bundle_bytes': len(data), 'unitypy_version': version,
              'serialized_files': [{'name': f.name, 'externals': [str(x.path) for x in f.externals]}
                                   for f in files.values()],
              'coverage': {'objects': len(objects), 'monoscripts': len(scripts),
                           'monobehaviours_total': sum(o.type.name == 'MonoBehaviour' for o in objects),
                           'monobehaviours_parsed': parsed, 'monobehaviour_parse_errors': len(errors),
                           'script_pointer_status_counts': dict(script_status),
                           'gameobjects_total': sum(o.type.name == 'GameObject' for o in objects),
                           'gameobject_parse_errors': len(name_errors)},
              'monoscript_inventory': scripts, 'monobehaviour_class_counts': dict(sorted(counts.items())),
              'parse_errors': errors, 'script_resolution_problems': problems,
              'entrance_class_or_field_matches': matches,
              'gameobject_name_matches': names, 'gameobject_name_parse_errors': name_errors,
              'dynamic_component_records': dynamic,
              'proof_boundary': 'Serialized scene-bundle inspection only. Does not cover runtime additions, other bundles, owner code, final entrance counts/pairings, generation or topology safety.'}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'OXYDE_ENTRANCE_COMPONENT_SCAN.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'coverage': report['coverage'], 'entrance_matches': matches,
                      'script_resolution_problems': problems, 'gameobject_names': names,
                      'dynamic_class_counts': dict(Counter(r['script']['class'] for r in dynamic))}, indent=2))

if __name__ == '__main__':
    main()
