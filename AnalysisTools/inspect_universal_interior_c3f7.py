#!/usr/bin/env python3
"""Static C3F7 package capture. Never loads game/mod managed code.

Acquisition and ZIP hashing reuse the C3F2 exact Thunderstore/UnityPy pathway.
--record-provenance only produces a candidate byte lock, never asset clearance.
Normal capture requires that reviewed lock and rejects any byte/layout drift.
"""
import argparse
from collections import Counter
import gc
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import shutil
import sys
import urllib.request
import zipfile

from inspect_universal_interior_c3f2 import (
    UNITYPY_VERSION, sha256_file, hash_member, safe_member_name,
    EXPECTED_ZIP_BYTES, EXPECTED_ZIP_SHA256,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'SourceEvidence/UniversalInteriorViability/PhaseC3F7'
AUTHORITY = 'Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md'
EXPORT = 'ProfileSources/S1.42AK/export.r2x'
COHORT = {
    'Generic_GMD-Generic_Interiors': ('5.2.0', ['BunkerFlow', 'DrainsFlow', 'SubstationFlow', 'BackroomsFlow', 'SHFlow', 'TowerFlow']),
    'LethalMatt-Bozoros': ('2.9.3', ['CircusFacilityFlow']),
    'Magic_Wesley-WesleysInteriors': ('4.1.15', ['AquaticDungeonFlow', 'DeepSewersFlow', 'FracturedComplexFlow', 'GreenhouseFlow', 'MuseumInteriorFlow', 'StoreFlow', 'ExpandedFacility', 'Level3ButCoolFlow', 'GrandArmoryFlow', 'SpookyManorFlow', 'RubberRoomsFlow', 'ToystoreFlow']),
    'Tolian-Scoopy_Castle': ('1.0.1', ['CastleFlow']),
    'Nikki-Slaughterhouse': ('1.2.1', ['SlaughterhouseFlow']),
    'Beaniebe-Storage_Complex': ('1.2.5', ['StorageComplex']),
    'Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior': ('3.4.4', ['Black Mesa']),
}


def json_safe(value):
    # Unity animation curves serialize +/-Infinity slopes. Preserve them as
    # explicit typed values rather than dropping fields or emitting invalid JSON.
    if isinstance(value, float) and not math.isfinite(value):
        return {'serialized_nonfinite_float': repr(value)}
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_safe(data), indent=2, allow_nan=False) + '\n', encoding='utf-8')


def source_url(key):
    return f'https://gcdn.thunderstore.io/live/repository/packages/{key}-{COHORT[key][0]}.zip'


def verify_authority():
    import yaml
    text = (ROOT / AUTHORITY).read_text(encoding='utf-8')
    mods = yaml.safe_load((ROOT / EXPORT).read_text(encoding='utf-8'))['mods']
    for key, (version, flows) in COHORT.items():
        matches = [m for m in mods if m['name'] == key]
        if len(matches) != 1 or matches[0]['enabled'] is not True:
            raise ValueError('Missing/ambiguous/disabled accepted package: ' + key)
        m = matches[0]
        if '.'.join(str(m['version'][k]) for k in ('major', 'minor', 'patch')) != version:
            raise ValueError('Accepted version drift: ' + key)
        for flow in flows:
            rows = [r for r in text.splitlines() if f'| `{flow}` |' in r and f'| {key} {version} |' in r]
            if len(rows) != 1:
                raise ValueError('Authoritative flow identity drift: ' + flow)
    return {p: sha256_file(ROOT / p) for p in (AUTHORITY, EXPORT)}


def download(key, cache):
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f'{key}-{COHORT[key][0]}.zip'
    if not path.exists():
        temp = path.with_suffix('.partial')
        request = urllib.request.Request(source_url(key), headers={'User-Agent': 'LC-AI-Modding-Project-C3F7/1'})
        with urllib.request.urlopen(request, timeout=180) as response, temp.open('wb') as out:
            shutil.copyfileobj(response, out)
        temp.replace(path)
    return path


def inventory(key, path):
    version, flows = COHORT[key]
    size, digest = path.stat().st_size, sha256_file(path)
    if key.startswith('Plastered_Crab-') and (size, digest) != (EXPECTED_ZIP_BYTES, EXPECTED_ZIP_SHA256):
        raise ValueError('C3F2 Black Mesa archive provenance drift')
    members, seen, manifest = [], set(), None
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            raw = info.filename.rstrip('/')
            name = safe_member_name(raw)
            if name != raw or any(x in ('', '.', '..') for x in raw.split('/')):
                raise ValueError('Noncanonical ZIP path: ' + raw)
            if name.casefold() in seen or info.flag_bits & 1:
                raise ValueError('Duplicate/colliding/encrypted ZIP member: ' + name)
            seen.add(name.casefold())
            if info.is_dir():
                continue
            sha, prefix = hash_member(archive, info)
            members.append({'member': name, 'bytes': info.file_size, 'sha256': sha, 'unityfs': prefix.startswith(b'UnityFS\x00')})
            if name == 'manifest.json':
                manifest = json.loads(archive.read(info).decode('utf-8-sig'))
        if not manifest or manifest.get('name') != key.split('-', 1)[1] or manifest.get('version_number') != version:
            raise ValueError('Package manifest identity/version mismatch: ' + key)
    bundles = [m for m in members if m['unityfs']]
    if not bundles:
        raise ValueError('No UnityFS bundle: ' + key)
    return {'package': key, 'version': version, 'source_url': source_url(key), 'flows': flows,
            'zip_bytes': size, 'zip_sha256': digest, 'unityfs_members': bundles,
            'archive_members': sorted(members, key=lambda m: m['member'])}


class CaptureError(ValueError):
    pass


def pointers(value, prefix=''):
    if isinstance(value, dict):
        if 'm_PathID' in value or 'm_FileID' in value:
            if set(value) != {'m_PathID', 'm_FileID'}:
                raise CaptureError('Malformed pointer at ' + prefix)
            yield prefix, value
        else:
            for key, item in value.items():
                yield from pointers(item, f'{prefix}.{key}' if prefix else key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from pointers(item, f'{prefix}[{i}]')


class AssetIndex:
    """C3F2-style type-tree reader with package-wide external-file resolution.

    Text records are retained; textures, meshes, audio and managed assemblies are
    never decoded/executed. All MonoBehaviours/scripts are read to make unique
    flow identity and the GlobalProp inventory exhaustive within the package.
    """
    TYPES = {'MonoBehaviour', 'MonoScript', 'GameObject', 'Transform', 'RectTransform'}

    def __init__(self):
        self.objects = {}
        self.files = {}
        self.scripts = {}
        self.coverage = []

    def load(self, path, observed):
        import UnityPy
        with zipfile.ZipFile(path) as archive:
            for member in observed['unityfs_members']:
                data = archive.read(member['member'])
                if len(data) != member['bytes'] or hashlib.sha256(data).hexdigest() != member['sha256']:
                    raise CaptureError('UnityFS member changed during capture')
                env = UnityPy.load(data)
                files, counts = {}, Counter()
                for obj in env.objects:
                    filename = obj.assets_file.name
                    if filename in files and files[filename] is not obj.assets_file:
                        raise CaptureError('Ambiguous serialized-file identity in ' + member['member'])
                    files[filename] = obj.assets_file
                    key = (member['member'], filename, obj.path_id)
                    if key in self.objects:
                        raise CaptureError('Duplicate serialized-object identity')
                    rec = {'key': key, 'type': obj.type.name}
                    if obj.type.name in self.TYPES:
                        # Parser failure may hide a target, never silently skip it.
                        rec['tree'] = obj.read_typetree()
                        rec['raw_sha256'] = hashlib.sha256(obj.get_raw_data()).hexdigest()
                    self.objects[key] = rec
                    counts[obj.type.name] += 1
                for filename, asset in files.items():
                    self.files[(member['member'], filename)] = {
                        'externals': [str(x.path) for x in asset.externals],
                        'unity_version': str(asset.unity_version),
                        'type_tree_enabled': bool(asset._enable_type_tree),
                    }
                self.coverage.append({'member': member['member'], 'type_counts': dict(sorted(counts.items()))})
                del env, data, files
                gc.collect()
        for key, rec in self.objects.items():
            if rec['type'] != 'MonoBehaviour':
                continue
            script = self.resolve(key, rec['tree'].get('m_Script'))
            if script is None:
                self.scripts[key] = None
                continue
            s = self.objects[script]
            if s['type'] != 'MonoScript':
                raise CaptureError('m_Script target is not MonoScript: ' + str(key))
            t = s['tree']
            self.scripts[key] = {k: t.get(k) for k in ('m_ClassName', 'm_Namespace', 'm_AssemblyName')}

    def resolve(self, owner, ptr, required=False, expected=None):
        if not isinstance(ptr, dict) or set(ptr) != {'m_FileID', 'm_PathID'}:
            raise CaptureError('Malformed pointer from ' + str(owner))
        fid, pid = ptr['m_FileID'], ptr['m_PathID']
        if type(fid) is not int or type(pid) is not int or fid < 0:
            raise CaptureError('Invalid pointer numbers from ' + str(owner))
        if pid == 0:
            if required:
                raise CaptureError('Required pointer is null from ' + str(owner))
            return None
        member, filename, _ = owner
        if fid:
            externals = self.files[(member, filename)]['externals']
            if fid > len(externals):
                raise CaptureError('Invalid external index from ' + str(owner))
            name = externals[fid - 1].replace('\\', '/').rsplit('/', 1)[-1]
            # Prefer the explicit same-bundle serialized file, then package-wide
            # exact basename. No case-insensitive/name-similarity guessing.
            matches = [(m, f) for m, f in self.files if f == name]
            if (member, name) in matches:
                matches = [(member, name)]
            if len(matches) != 1:
                raise CaptureError('Unresolved/ambiguous non-null external: ' + externals[fid - 1])
            member, filename = matches[0]
        key = (member, filename, pid)
        if key not in self.objects:
            raise CaptureError('Unresolved non-null path ID: ' + str(key))
        if expected and self.objects[key]['type'] not in expected:
            raise CaptureError('Unexpected pointer target type: ' + str(key))
        return key

    def descriptor(self, key):
        rec = self.objects[key]
        return {'bundle_member': key[0], 'serialized_file': key[1], 'path_id': key[2],
                'type': rec['type'], 'raw_object_sha256': rec.get('raw_sha256'),
                'script': self.scripts.get(key)}

    def class_is(self, key, cls, namespace, assembly):
        # Exact class + namespace, with serialized exporter assembly layouts.
        # Bozoros/Wesley serialize DunGen stubs into Assembly-CSharp; the actual
        # descriptor and raw object hash remain in evidence. No namespace/name
        # substring matching and no runtime assembly equivalence is asserted.
        assemblies = {'DunGen.dll': {'DunGen.dll', 'Assembly-CSharp'},
                      'Assembly-CSharp.dll': {'Assembly-CSharp.dll', 'Assembly-CSharp'}}
        s = self.scripts.get(key)
        return bool(s and s['m_ClassName'] == cls and s['m_Namespace'] == namespace
                    and s['m_AssemblyName'] in assemblies.get(assembly, {assembly}))

    def record(self, key):
        return {**self.descriptor(key), 'serialized_fields': self.objects[key]['tree']}

    def hierarchy(self, root):
        """Only Transform descendants belong to a template, never its siblings.

        Component/child ownership and cycles are checked explicitly. Serialized
        prefab links are evidence edges, not assumed runtime instantiation.
        """
        result, visiting = {}, set()

        def walk(go, parent_transform=None):
            if go in visiting or go in result:
                raise CaptureError('Cyclic/duplicate GameObject hierarchy: ' + str(go))
            visiting.add(go)
            t = self.objects[go]['tree']
            components = t.get('m_Component')
            if not isinstance(components, list):
                raise CaptureError('GameObject component table missing')
            comp_ids, transforms = [], []
            for entry in components:
                comp = self.resolve(go, entry.get('component'), required=True)
                if comp in comp_ids:
                    raise CaptureError('Duplicate component pointer')
                comp_ids.append(comp)
                cr = self.objects[comp]
                if cr['type'] in self.TYPES:
                    owner = self.resolve(comp, cr['tree'].get('m_GameObject'), required=True, expected={'GameObject'})
                    if owner != go:
                        raise CaptureError('Component/GameObject ownership mismatch')
                if cr['type'] in ('Transform', 'RectTransform'):
                    transforms.append(comp)
            if len(transforms) != 1:
                raise CaptureError('GameObject must resolve exactly one Transform')
            tr = transforms[0]
            tt = self.objects[tr]['tree']
            father = self.resolve(tr, tt.get('m_Father'), expected={'Transform', 'RectTransform'})
            if parent_transform is not None and father != parent_transform:
                raise CaptureError('Transform parent/child mismatch')
            result[go] = comp_ids
            if not isinstance(tt.get('m_Children'), list):
                raise CaptureError('Transform children table missing')
            for ptr in tt['m_Children']:
                child = self.resolve(tr, ptr, required=True, expected={'Transform', 'RectTransform'})
                child_go = self.resolve(child, self.objects[child]['tree'].get('m_GameObject'), required=True, expected={'GameObject'})
                walk(child_go, tr)
            visiting.remove(go)
        walk(root)
        return result


def global_table(tree):
    table = tree.get('GlobalProps')
    if not isinstance(table, list):
        raise CaptureError('GlobalProps table missing/unreadable; absence not established')
    for legacy in ('globalPropGroupID_obsolete', 'globalPropRanges_obsolete'):
        if tree.get(legacy):
            raise CaptureError('Nonempty legacy GlobalProp data needs explicit migration interpretation')
    ids = []
    for row in table:
        if not isinstance(row, dict) or type(row.get('ID')) is not int:
            raise CaptureError('GlobalProp row lacks unambiguous integer ID')
        ids.append(row['ID'])
        count = row.get('Count')
        if not isinstance(count, dict) or any(type(count.get(k)) is not int for k in ('Min', 'Max')) or count['Min'] > count['Max']:
            raise CaptureError('GlobalProp Count range unresolved')
    if ids.count(1231) > 1:
        raise CaptureError('Duplicate target GlobalProp ID 1231')
    return table


def template_capture(idx, prop, template_root=None, ancestry=()):
    tree = idx.objects[prop]['tree']
    root = template_root or idx.resolve(prop, tree.get('m_GameObject'), required=True, expected={'GameObject'})
    if root in ancestry:
        raise CaptureError('Cyclic spawnPrefab template reference')
    hierarchy = idx.hierarchy(root)
    context, entrances, prefab_links, spawned = [], [], [], []
    for go, components in hierarchy.items():
        go_rec = idx.record(go)
        go_rec['components'] = []
        for key in components:
            rec = idx.objects[key]
            if rec['type'] not in idx.TYPES:
                go_rec['components'].append(idx.descriptor(key))
                continue
            go_rec['components'].append(idx.record(key))
            if rec['type'] != 'MonoBehaviour':
                continue
            if idx.scripts.get(key) is None:
                raise CaptureError('Null script on target template component')
            t = rec['tree']
            # Resolve potential prefab/component links for contextual evidence,
            # but they do not count as descendants or prove spawn semantics.
            for field, ptr in pointers(t):
                if field in ('m_Script', 'm_GameObject'):
                    continue
                # All non-null pointers on the actual template MonoBehaviours
                # must resolve, including indirect prefabs; never discard a
                # missing reference that could alter the entrance surface.
                target = idx.resolve(key, ptr)
                if target is not None:
                    prefab_links.append({'owner': idx.descriptor(key), 'field': field,
                                         'pointer': ptr, 'target': idx.descriptor(target)})
            if idx.class_is(key, 'EntranceTeleport', '', 'Assembly-CSharp.dll'):
                if type(t.get('entranceId')) is not int or type(t.get('isEntranceToBuilding')) not in (bool, int) or t['isEntranceToBuilding'] not in (0, 1):
                    raise CaptureError('EntranceTeleport ID/side fields unresolved')
                entrances.append(idx.record(key))
            if idx.class_is(key, 'SpawnSyncedObject', '', 'Assembly-CSharp.dll'):
                target = idx.resolve(key, t.get('spawnPrefab'), required=True, expected={'GameObject'})
                child = template_capture(idx, prop, target, ancestry + (root,))
                spawned.append({'source_component': idx.descriptor(key), 'field': 'spawnPrefab', 'template': child})
        context.append(go_rec)
    # A serialized spawnPrefab link proves a template reference, not that its
    # runtime spawner executes. Preserve multiplicity: two spawners referencing
    # one prefab are not one entrance instance.
    total = len(entrances) + sum(s['template']['referenced_entrance_count'] for s in spawned)
    standard = (total == 1 and all(e['serialized_fields']['entranceId'] == 1
                and e['serialized_fields']['isEntranceToBuilding'] == 0 for e in entrances)
                and all(s['template']['standard_inside_id_1_template_proven'] for s in spawned))
    return {'global_prop': idx.record(prop), 'template_root': idx.descriptor(root),
            'gameobject_component_context': context, 'referenced_context_edges': prefab_links,
            'entrance_teleports': entrances,
            'spawn_prefab_templates': spawned, 'referenced_entrance_count': total,
            'standard_inside_id_1_template_proven': standard,
            'qualification': 'Static descendants/explicit SpawnSyncedObject.spawnPrefab references and serialized fields only; actual spawning, activity, runtime mutations, capacity and count-3 generation unproven.'}


def capture_flow(idx, name):
    result = {'flow_name': name, 'result_class': 'CAPTURE_UNRESOLVED', 'prop_1231_presence': 'unresolved',
              'fatal_ambiguities': [], 'templates': []}
    try:
        candidates = [k for k, v in idx.objects.items()
                      if v.get('tree', {}).get('m_Name') == name
                      and idx.class_is(k, 'DungeonFlow', 'DunGen.Graph', 'DunGen.dll')]
        if len(candidates) != 1:
            raise CaptureError(f'Expected exactly one exact DungeonFlow identity, found {len(candidates)}')
        flow = candidates[0]
        tree = idx.objects[flow]['tree']
        result['dungeon_flow'] = idx.record(flow)
        result['global_prop_table'] = tree.get('GlobalProps')
        table = global_table(tree)
        result['global_prop_table'] = table  # retain every field, not just Count
        row = [r for r in table if r['ID'] == 1231]
        result['prop_1231_presence'] = 'present' if row else 'absent'
        result['prop_1231_serialized_settings'] = row
        result['non_target_duplicate_prop_ids'] = [k for k, n in Counter(r['ID'] for r in table).items() if n > 1 and k != 1231]
        if not row:
            result['result_class'] = 'PROP_1231_ABSENT'
            return result
        result['result_class'] = 'PROP_PRESENT_TEMPLATE_UNRESOLVED'
        # Follow exact serialized flow -> archetype/TileSet -> tile GameObject
        # references. Preserve the complete graph records and pointer edges so
        # a package-wide unrelated fire exit cannot masquerade as this flow's.
        pending, visited, roots, edges, graph = [flow], set(), set(), [], []
        while pending:
            key = pending.pop()
            if key in visited:
                continue
            visited.add(key)
            graph.append(idx.record(key))
            for field, ptr in pointers(idx.objects[key]['tree']):
                if field in ('m_Script', 'm_GameObject'):
                    continue
                target = idx.resolve(key, ptr)
                if target is None:
                    continue
                edges.append({'owner': idx.descriptor(key), 'field': field, 'pointer': ptr, 'target': idx.descriptor(target)})
                if idx.objects[target]['type'] == 'GameObject':
                    roots.add(target)
                elif any(idx.class_is(target, c, ns, 'DunGen.dll') for c, ns in
                         [('DungeonFlow', 'DunGen.Graph'), ('DungeonArchetype', 'DunGen'), ('TileSet', 'DunGen')]):
                    if idx.class_is(target, 'DungeonFlow', 'DunGen.Graph', 'DunGen.dll') and target != flow:
                        raise CaptureError('Flow graph refers to a different DungeonFlow')
                    pending.append(target)
                else:
                    raise CaptureError('Unsupported non-null flow-graph reference: ' + field + ' -> ' + str(idx.descriptor(target)))
        result['flow_graph_records'] = graph
        result['flow_graph_edges'] = edges
        result['tile_roots'] = [idx.descriptor(k) for k in sorted(roots)]
        if not roots:
            raise CaptureError('No serialized tile roots resolved for target flow')
        props, membership = set(), []
        for root in sorted(roots):
            for go, components in idx.hierarchy(root).items():
                for key in components:
                    if idx.objects[key]['type'] == 'MonoBehaviour' and idx.scripts.get(key) is None:
                        raise CaptureError('Null script could hide GlobalProp on reachable tile')
                    if idx.class_is(key, 'GlobalProp', 'DunGen', 'DunGen.dll'):
                        t = idx.objects[key]['tree']
                        if type(t.get('PropGroupID')) is not int:
                            raise CaptureError('GlobalProp component ID unresolved')
                        if t['PropGroupID'] == 1231:
                            props.add(key)
                            membership.append({'tile_root': idx.descriptor(root), 'gameobject': idx.descriptor(go), 'global_prop': idx.descriptor(key)})
        result['prop_tile_membership'] = membership
        for key in sorted(props):
            result['templates'].append(template_capture(idx, key))
        if props and all(t['standard_inside_id_1_template_proven'] for t in result['templates']):
            result['result_class'] = 'PROP_AND_TEMPLATE_PROVEN'
        else:
            result['unresolved_reason'] = 'No reachable standard template, or at least one template lacks exactly one serialized inside EntranceTeleport ID 1. Runtime substitution is not inferred.'
    except Exception as exc:
        result['fatal_ambiguities'].append(f'{type(exc).__name__}: {exc}')
        result['result_class'] = ('PROP_PRESENT_TEMPLATE_UNRESOLVED'
                                  if result['prop_1231_presence'] == 'present' else 'CAPTURE_UNRESOLVED')
    return result


def verify_lock(lock, key, authority, observed):
    if lock.get('schema_version') != 1 or lock.get('authority') != authority:
        raise CaptureError('Authority/lock schema drift')
    if set(lock.get('packages', {})) != set(COHORT):
        raise CaptureError('Lock must contain exactly the seven cohort packages')
    if lock['packages'][key] != observed:
        raise CaptureError('Archive/member provenance drift: ' + key)


def capture_package(key, path, observed, authority, lock_path, out):
    lock = json.loads(lock_path.read_text(encoding='utf-8'))
    verify_lock(lock, key, authority, observed)
    if importlib.metadata.version('UnityPy') != UNITYPY_VERSION:
        raise CaptureError('UnityPy version drift')
    idx = AssetIndex()
    idx.load(path, observed)
    flows = [capture_flow(idx, f) for f in COHORT[key][1]]
    result = {'schema_version': 'c3f7-static-asset-capture-1', 'package': observed,
              'authority_sha256': authority, 'lock_sha256': sha256_file(lock_path),
              'helper_sha256': sha256_file(Path(__file__)),
              'c3f2_helper_sha256': sha256_file(Path(__file__).with_name('inspect_universal_interior_c3f2.py')),
              'toolchain': {'python': sys.version.split()[0], 'unitypy': UNITYPY_VERSION},
              'coverage': idx.coverage,
              'package_global_prop_1231_inventory': [idx.record(k) for k in idx.scripts
                                                     if idx.class_is(k, 'GlobalProp', 'DunGen', 'DunGen.dll')
                                                     and idx.objects[k]['tree'].get('PropGroupID') == 1231],
              'target_script_inventory': [idx.descriptor(k) for k, s in idx.scripts.items()
                                          if s and s['m_ClassName'] in ('DungeonFlow', 'DungeonArchetype', 'TileSet', 'GlobalProp', 'EntranceTeleport')],
              'serialized_files': [{'bundle_member': k[0], 'name': k[1], **v} for k, v in sorted(idx.files.items())],
              'flows': flows,
              'result_counts': dict(Counter(f['result_class'] for f in flows)),
              'fatal_ambiguities': [f['flow_name'] + ': ' + e for f in flows for e in f['fatal_ambiguities']],
              'proof_boundary': 'Static asset evidence only. PROP_AND_TEMPLATE_PROVEN is not Black Mesa count-3 compatibility, generation, traversal, route/NavMesh or matrix clearance. No gameplay build/runtime authorization.'}
    write_json(out / 'CAPTURE.json', result)
    print(json.dumps({'package': key, 'result_counts': result['result_counts'], 'fatal_ambiguities': result['fatal_ambiguities']}))
    if result['fatal_ambiguities']:
        raise CaptureError('Fail-closed target-surface ambiguity; see CAPTURE.json')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package', choices=COHORT, required=True)
    p.add_argument('--cache', type=Path, default=Path('c3f7-packages'))
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--lock', type=Path, default=EVIDENCE / 'PACKAGE_LOCK.json')
    p.add_argument('--record-provenance', action='store_true')
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    # Never leave a previous successful result beside a failed fresh invocation.
    for name in ('CAPTURE.json', 'CAPTURE_FAILURE.json', 'PROVENANCE_CANDIDATE.json'):
        (args.out / name).unlink(missing_ok=True)
    try:
        authority = verify_authority()
        path = download(args.package, args.cache)
        observed = inventory(args.package, path)
        if args.record_provenance:
            write_json(args.out / 'PROVENANCE_CANDIDATE.json', {'status': 'UNREVIEWED_BYTE_BINDING_NO_ASSET_CLAIM', 'authority': authority, 'package': observed})
            print(json.dumps({'package': args.package, 'zip_bytes': observed['zip_bytes'], 'zip_sha256': observed['zip_sha256'], 'bundles': len(observed['unityfs_members'])}))
            return
        capture_package(args.package, path, observed, authority, args.lock, args.out)
    except Exception as exc:
        # If parsing stops before per-flow extraction, all target rows still get
        # explicit unresolved results. No missing package silently shrinks cohort.
        failure = {'fail_closed': True, 'package': args.package, 'source_url': source_url(args.package),
                   'error_type': type(exc).__name__, 'error': str(exc)}
        if not (args.out / 'CAPTURE.json').exists():
            failure['flows'] = [{'flow_name': f, 'result_class': 'CAPTURE_UNRESOLVED',
                                 'prop_1231_presence': 'unresolved'} for f in COHORT[args.package][1]]
        write_json(args.out / 'CAPTURE_FAILURE.json', failure)
        raise


if __name__ == '__main__':
    main()
