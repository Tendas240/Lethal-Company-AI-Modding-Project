"""C3F7 proof-boundary regression tests, using tiny serialized-object fixtures."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import inspect_universal_interior_c3f7 as c


def fixture():
    idx = c.AssetIndex()
    idx.files[('bundle', 'file')] = {'externals': []}

    def ptr(n):
        return {'m_FileID': 0, 'm_PathID': n}

    def add(n, typ, tree, cls=None, ns='DunGen', assembly='DunGen.dll'):
        k = ('bundle', 'file', n)
        idx.objects[k] = {'key': k, 'type': typ, 'tree': tree, 'raw_sha256': 'a' * 64}
        if cls:
            idx.scripts[k] = {'m_ClassName': cls, 'm_Namespace': ns, 'm_AssemblyName': assembly}
        return k

    add(1, 'MonoBehaviour', {'m_Name': 'Target', 'GlobalProps': [{'ID': 1231, 'Count': {'Min': 1, 'Max': 1}}],
                             'Nodes': [{'TileSets': [ptr(2)]}]}, 'DungeonFlow', 'DunGen.Graph')
    add(2, 'MonoBehaviour', {'TileWeights': {'Weights': [{'Value': ptr(10), 'MainPathWeight': 1}]}}, 'TileSet')
    add(10, 'GameObject', {'m_Name': 'Tile', 'm_IsActive': True, 'm_Component': [{'component': ptr(11)}]})
    add(11, 'Transform', {'m_GameObject': ptr(10), 'm_Father': ptr(0), 'm_Children': [ptr(21)]})
    add(20, 'GameObject', {'m_Name': 'FireExit', 'm_IsActive': True,
                         'm_Component': [{'component': ptr(21)}, {'component': ptr(22)}, {'component': ptr(23)}]})
    add(21, 'Transform', {'m_GameObject': ptr(20), 'm_Father': ptr(11), 'm_Children': []})
    add(22, 'MonoBehaviour', {'m_GameObject': ptr(20), 'PropGroupID': 1231, 'm_Enabled': 1}, 'GlobalProp')
    add(23, 'MonoBehaviour', {'m_GameObject': ptr(20), 'entranceId': 1, 'isEntranceToBuilding': False,
                             'entrancePoint': ptr(21), 'exitPoint': ptr(0)}, 'EntranceTeleport', '', 'Assembly-CSharp.dll')
    return idx, ptr


class ProofTests(unittest.TestCase):
    def setUp(self):
        self.idx, self.ptr = fixture()

    def tree(self, n):
        return self.idx.objects[('bundle', 'file', n)]['tree']

    def capture(self):
        return c.capture_flow(self.idx, 'Target')

    def test_positive_is_only_static_template_proof(self):
        result = self.capture()
        self.assertEqual(result['result_class'], 'PROP_AND_TEMPLATE_PROVEN')
        self.assertEqual(result['global_prop_table'][0]['Count'], {'Min': 1, 'Max': 1})
        self.assertIn('count-3 generation unproven', result['templates'][0]['qualification'])

    def test_absent_is_distinct_from_unreadable(self):
        self.tree(1)['GlobalProps'] = []
        self.assertEqual(self.capture()['result_class'], 'PROP_1231_ABSENT')
        del self.tree(1)['GlobalProps']
        self.assertEqual(self.capture()['result_class'], 'CAPTURE_UNRESOLVED')

    def test_complete_table_and_extra_count_fields_preserved(self):
        row = {'ID': 99, 'Count': {'Min': 0, 'Max': 4, 'Extra': 'preserve'}}
        self.tree(1)['GlobalProps'].insert(0, row)
        self.assertEqual(self.capture()['global_prop_table'][0], row)

    def test_duplicate_prop_id_fails_closed(self):
        self.tree(1)['GlobalProps'] *= 2
        self.assertEqual(self.capture()['result_class'], 'CAPTURE_UNRESOLVED')

    def test_non_target_duplicate_ids_preserved_without_generation_claim(self):
        self.tree(1)['GlobalProps'] += [{'ID': 5, 'Count': {'Min': 1, 'Max': 2}}, {'ID': 5, 'Count': {'Min': 3, 'Max': 4}}]
        result = self.capture()
        self.assertEqual(result['non_target_duplicate_prop_ids'], [5])
        self.assertEqual(len(result['global_prop_table']), 3)

    def test_legacy_table_and_invalid_range_are_unresolved(self):
        for mutate in ('legacy', 'range', 'id'):
            with self.subTest(mutate=mutate):
                self.idx, self.ptr = fixture()
                if mutate == 'legacy': self.tree(1)['globalPropGroupID_obsolete'] = [1231]
                if mutate == 'range': self.tree(1)['GlobalProps'][0]['Count'] = {'Min': 4, 'Max': 1}
                if mutate == 'id': self.tree(1)['GlobalProps'][0]['ID'] = '1231'
                self.assertEqual(self.capture()['result_class'], 'CAPTURE_UNRESOLVED')

    def test_duplicate_exact_flow_never_picks_first(self):
        self.idx.objects[('bundle', 'file', 3)] = copy.deepcopy(self.idx.objects[('bundle', 'file', 1)])
        self.idx.scripts[('bundle', 'file', 3)] = self.idx.scripts[('bundle', 'file', 1)]
        self.assertEqual(self.capture()['result_class'], 'CAPTURE_UNRESOLVED')

    def test_namespace_or_unreviewed_assembly_cannot_spoof_flow(self):
        for field in ('m_Namespace', 'm_AssemblyName'):
            self.idx, self.ptr = fixture()
            self.idx.scripts[('bundle', 'file', 1)][field] = 'Unrelated'
            self.assertEqual(self.capture()['result_class'], 'CAPTURE_UNRESOLVED')

    def test_observed_assembly_csharp_export_layout(self):
        self.idx.scripts[('bundle', 'file', 1)]['m_AssemblyName'] = 'Assembly-CSharp'
        self.assertEqual(self.capture()['result_class'], 'PROP_AND_TEMPLATE_PROVEN')

    def test_presence_alone_is_not_template_proof(self):
        self.tree(20)['m_Component'].pop()
        self.assertEqual(self.capture()['result_class'], 'PROP_PRESENT_TEMPLATE_UNRESOLVED')

    def test_unrelated_package_template_not_used(self):
        self.tree(11)['m_Children'] = []
        self.assertEqual(self.capture()['result_class'], 'PROP_PRESENT_TEMPLATE_UNRESOLVED')

    def test_wrong_pre_numbering_id_or_side_never_proven(self):
        for field, value in [('entranceId', 0), ('entranceId', 2), ('isEntranceToBuilding', True)]:
            self.idx, self.ptr = fixture()
            self.tree(23)[field] = value
            self.assertEqual(self.capture()['result_class'], 'PROP_PRESENT_TEMPLATE_UNRESOLVED')

    def test_duplicate_entrance_never_proven(self):
        k = ('bundle', 'file', 24)
        self.idx.objects[k] = copy.deepcopy(self.idx.objects[('bundle', 'file', 23)])
        self.idx.scripts[k] = self.idx.scripts[('bundle', 'file', 23)]
        self.tree(20)['m_Component'].append({'component': self.ptr(24)})
        self.assertEqual(self.capture()['result_class'], 'PROP_PRESENT_TEMPLATE_UNRESOLVED')

    def test_missing_nonnull_template_pointer_is_fatal(self):
        self.tree(23)['entrancePoint'] = self.ptr(999)
        result = self.capture()
        self.assertEqual(result['result_class'], 'PROP_PRESENT_TEMPLATE_UNRESOLVED')
        self.assertTrue(result['fatal_ambiguities'])

    def test_explicit_spawn_prefab_context_is_captured(self):
        # Move the entrance into a detached prefab and put a spawner on the prop.
        key = ('bundle', 'file', 23)
        entrance = copy.deepcopy(self.idx.objects[key])
        self.idx.objects[('bundle', 'file', 33)] = entrance
        entrance['tree']['m_GameObject'] = self.ptr(30)
        entrance['tree']['entrancePoint'] = self.ptr(31)
        self.idx.scripts[('bundle', 'file', 33)] = self.idx.scripts[key]
        self.idx.objects[('bundle', 'file', 30)] = {'type': 'GameObject', 'tree': {'m_Name': 'EntrancePrefab', 'm_Component': [{'component': self.ptr(31)}, {'component': self.ptr(33)}]}}
        self.idx.objects[('bundle', 'file', 31)] = {'type': 'Transform', 'tree': {'m_GameObject': self.ptr(30), 'm_Father': self.ptr(0), 'm_Children': []}}
        self.idx.objects[key]['tree'] = {'m_GameObject': self.ptr(20), 'spawnPrefab': self.ptr(30)}
        self.idx.scripts[key] = {'m_ClassName': 'SpawnSyncedObject', 'm_Namespace': '', 'm_AssemblyName': 'Assembly-CSharp.dll'}
        result = self.capture()
        self.assertEqual(result['result_class'], 'PROP_AND_TEMPLATE_PROVEN')
        child = result['templates'][0]['spawn_prefab_templates'][0]['template']
        self.assertEqual(child['entrance_teleports'][0]['serialized_fields']['entranceId'], 1)
        self.assertIn('actual spawning', child['qualification'])
        self.tree(23)['spawnPrefab'] = self.ptr(20)
        self.assertTrue(self.capture()['fatal_ambiguities'])

    def test_missing_graph_pointer_and_null_script_are_fatal(self):
        self.tree(2)['TileWeights']['Weights'][0]['Value'] = self.ptr(999)
        self.assertTrue(self.capture()['fatal_ambiguities'])
        self.idx, self.ptr = fixture()
        self.idx.scripts[('bundle', 'file', 22)] = None
        self.assertTrue(self.capture()['fatal_ambiguities'])

    def test_parent_child_conflict_and_cycle_are_fatal(self):
        self.tree(21)['m_Father'] = self.ptr(21)
        self.assertTrue(self.capture()['fatal_ambiguities'])
        self.idx, self.ptr = fixture()
        self.tree(21)['m_Children'] = [self.ptr(11)]
        self.assertTrue(self.capture()['fatal_ambiguities'])

    def test_cross_file_resolution_is_exact_and_ambiguity_fatal(self):
        owner = ('bundle', 'file', 1)
        self.idx.files[('bundle', 'file')]['externals'] = ['archive:/CAB-other/CAB-other']
        self.idx.files[('other', 'CAB-other')] = {'externals': []}
        key = ('other', 'CAB-other', 99)
        self.idx.objects[key] = {'type': 'MonoScript'}
        ptr = {'m_FileID': 1, 'm_PathID': 99}
        self.assertEqual(self.idx.resolve(owner, ptr), key)
        self.idx.files[('duplicate', 'CAB-other')] = {'externals': []}
        with self.assertRaises(c.CaptureError): self.idx.resolve(owner, ptr)
        with self.assertRaises(c.CaptureError): self.idx.resolve(owner, {'m_FileID': 2, 'm_PathID': 99})

    def test_nonfinite_unity_curve_values_preserved_in_strict_json(self):
        data = c.json_safe({'slope': float('inf'), 'range': [float('-inf'), float('nan')]})
        json.dumps(data, allow_nan=False)
        self.assertEqual(data['slope'], {'serialized_nonfinite_float': 'inf'})

    def test_exact_cohort_and_provenance_drift(self):
        self.assertEqual(sum(len(v[1]) for v in c.COHORT.values()), 23)
        lock = json.loads((c.EVIDENCE / 'PACKAGE_LOCK.json').read_text())
        authority = c.verify_authority()
        key = 'Tolian-Scoopy_Castle'
        observed = copy.deepcopy(lock['packages'][key])
        c.verify_lock(lock, key, authority, observed)
        for field, value in [('zip_bytes', 0), ('zip_sha256', '0' * 64), ('flows', [])]:
            changed = {**observed, field: value}
            with self.assertRaises(c.CaptureError): c.verify_lock(lock, key, authority, changed)
        observed['unityfs_members'][0]['sha256'] = '0' * 64
        with self.assertRaises(c.CaptureError): c.verify_lock(lock, key, authority, observed)
        with self.assertRaises(c.CaptureError): c.verify_lock(lock, key, {}, lock['packages'][key])

    def test_bundle_parser_failure_propagates(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fixture.zip'
            data = b'UnityFS\0invalid'
            with zipfile.ZipFile(path, 'w') as archive: archive.writestr('bundle', data)
            observed = {'unityfs_members': [{'member': 'bundle', 'bytes': len(data), 'sha256': c.hashlib.sha256(data).hexdigest()}]}
            with patch('UnityPy.load', side_effect=ValueError('parser fault')):
                with self.assertRaisesRegex(ValueError, 'parser fault'): self.idx.load(path, observed)


if __name__ == '__main__':
    unittest.main()
