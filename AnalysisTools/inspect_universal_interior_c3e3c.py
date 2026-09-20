#!/usr/bin/env python3
"""Inspect exact Oxyde level/moon serialization; execute no managed or game code.

Requires UnityPy==1.25.3. Accepts the exact package ZIP or extracted oxydeassets.
Non-finite floats are represented by {"$float": "Infinity"/"-Infinity"/"NaN"}.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import zipfile

PACKAGE_SHA256 = 'a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6'
PACKAGE_BYTES = 263010364
BUNDLE_SHA256 = '86d2ef29d428bcb3b96cb5ec99283a362324f8261c4a8e26737e3bd04fe24fe4'
BUNDLE_BYTES = 398696
MEMBER = 'plugins/CodeRebirth/Assets/oxydeassets'


def checked(data, size, digest):
    if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('Input size/SHA-256 mismatch')
    return data


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return {'$float': 'NaN' if math.isnan(value) else ('Infinity' if value > 0 else '-Infinity')}
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


def pointers(value, path=''):
    if isinstance(value, dict):
        if set(value) == {'m_FileID', 'm_PathID'}:
            yield path, value
        else:
            for key, item in value.items():
                yield from pointers(item, f'{path}.{key}' if path else key)
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            yield from pointers(item, f'{path}[{i}]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--package', type=Path)
    source.add_argument('--bundle', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.package:
        checked(args.package.read_bytes(), PACKAGE_BYTES, PACKAGE_SHA256)
        with zipfile.ZipFile(args.package) as archive:
            data = archive.read(MEMBER)
    else:
        data = args.bundle.read_bytes()
    checked(data, BUNDLE_BYTES, BUNDLE_SHA256)
    import UnityPy
    version = importlib.metadata.version('UnityPy')
    if version != '1.25.3':
        raise ValueError('Expected UnityPy 1.25.3')
    env = UnityPy.load(data)
    objects = sorted(env.objects, key=lambda o: o.path_id)
    files = {id(o.assets_file): o.assets_file for o in objects}
    if len(files) != 1:
        raise ValueError('Expected one serialized file')
    asset_file = next(iter(files.values()))
    if asset_file.externals:
        raise ValueError('Unexpected external serialized-file references')
    by_id = {o.path_id: o for o in objects}
    cache = {}

    def read(obj):
        if obj.path_id not in cache:
            cache[obj.path_id] = obj.read_typetree()
        return cache[obj.path_id]

    def identity(obj):
        return {'serialized_file': obj.assets_file.name, 'path_id': obj.path_id, 'type': obj.type.name}

    scripts = {o.path_id: {**identity(o), 'serialized_fields': read(o)}
               for o in objects if o.type.name == 'MonoScript'}

    def script(obj):
        ptr = read(obj)['m_Script']
        if ptr['m_FileID'] != 0 or ptr['m_PathID'] not in scripts:
            raise ValueError('Unresolved MonoBehaviour script')
        return scripts[ptr['m_PathID']]

    behaviours = [o for o in objects if o.type.name == 'MonoBehaviour']
    inventory = [{**identity(o), 'name': read(o).get('m_Name'),
                  'script': script(o)} for o in behaviours]
    levels = [o for o in behaviours if script(o)['serialized_fields']['m_ClassName'] == 'SelectableLevel']
    moons = [o for o in behaviours if script(o)['serialized_fields']['m_ClassName'] == 'DuskMoonDefinition']
    bundles = [o for o in objects if o.type.name == 'AssetBundle']
    if len(levels) != 1 or len(moons) != 1 or len(bundles) != 1:
        raise ValueError('Ambiguous level/moon/container identity')
    level, moon, bundle = levels[0], moons[0], bundles[0]
    if read(moon)['<Level>k__BackingField'] != {'m_FileID': 0, 'm_PathID': level.path_id}:
        raise ValueError('Moon does not reference identified SelectableLevel')

    def resolve(ptr):
        result = {'pointer': ptr}
        if ptr['m_PathID'] == 0:
            return {**result, 'status': 'NULL'}
        target = by_id.get(ptr['m_PathID']) if ptr['m_FileID'] == 0 else None
        if target is None:
            raise ValueError('Unresolved non-null pointer')
        result.update(status='RESOLVED', target={**identity(target), 'name': read(target).get('m_Name')})
        if target.type.name == 'MonoBehaviour':
            result['target']['script'] = script(target)
        return result

    references = [{"owner_path_id": owner.path_id, "field_path": path, **resolve(ptr)}
                  for owner in (level, moon) for path, ptr in pointers(read(owner))]
    # Follow only the moon's route predicate and its fail node; not recursive asset closure.
    predicate = by_id[read(moon)['<TerminalPredicate>k__BackingField']['m_PathID']]
    fail_node = by_id[read(predicate)['_failNode']['m_PathID']]

    def record(obj):
        return {**identity(obj), 'script': script(obj), 'raw_object_bytes': obj.byte_size,
                'raw_object_sha256': hashlib.sha256(obj.get_raw_data()).hexdigest(),
                'serialized_fields': read(obj)}

    l = read(level)
    report = {
        'schema_version': 'phase-c3e3c-1', 'bundle_member': MEMBER,
        'bundle_sha256': BUNDLE_SHA256, 'bundle_bytes': len(data), 'unitypy_version': version,
        'serialization': {'name': asset_file.name, 'unity_version': asset_file.unity_version,
                          'type_tree_enabled': bool(asset_file._enable_type_tree), 'externals': []},
        'coverage': {'objects_indexed': len(objects), 'type_counts': dict(sorted(Counter(o.type.name for o in objects).items())),
                     'monoscripts_parsed': len(scripts), 'monobehaviours_parsed_for_identity': len(behaviours),
                     'selected_definition_records': 2, 'parse_errors': 0,
                     'level_and_moon_pointer_status_counts': dict(Counter(r['status'] for r in references))},
        'monobehaviour_inventory': inventory,
        'asset_bundle_registration': {**identity(bundle), 'serialized_fields': read(bundle)},
        'selectable_level': record(level), 'dusk_moon_definition': record(moon),
        'level_and_moon_references': references,
        'route_predicate': record(predicate), 'route_fail_node': record(fail_node),
        'generation_observations': {key: l[key] for key in ('sceneName', 'levelID', 'PlanetName', 'spawnEnemiesAndScrap',
            'dungeonFlowTypes', 'factorySizeMultiplier', 'planetHasTime', 'riskLevel', 'spawnableScrap',
            'minScrap', 'maxScrap', 'minTotalScrapValue', 'maxTotalScrapValue', 'Enemies', 'DaytimeEnemies')},
        'nonfinite_float_encoding': 'Tagged object {"$float": "Infinity"/"-Infinity"/"NaN"}; preserves non-finite values as valid JSON.',
        'proof_boundary': 'Packaged serialized defaults and local references only. No owner implementation, runtime mutation, effective generation gate, entrance count/pairing or topology clearance.'
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'OXYDE_LEVEL_MOON_DEFINITION.json').write_text(json.dumps(json_safe(report), indent=2, allow_nan=False) + '\n')
    print(json.dumps({'coverage': report['coverage'], 'generation_observations': report['generation_observations']}, indent=2))


if __name__ == '__main__':
    main()
