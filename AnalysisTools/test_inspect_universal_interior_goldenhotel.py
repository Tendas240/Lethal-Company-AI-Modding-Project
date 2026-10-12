#!/usr/bin/env python3
"""Pure structural regressions for GoldenHotel. Never acquires original bytes."""
import copy
import unittest
import inspect_universal_interior_goldenhotel as probe
import inspect_universal_interior_c3f7 as c7


class PinnedCaptureTests(unittest.TestCase):
    def setUp(self):
        self.observed = {
            "package": probe.PACKAGE, "version": probe.VERSION,
            "flows": list(probe.HISTORICAL_FLOWS), "zip_bytes": probe.ZIP_BYTES,
            "zip_sha256": probe.ZIP_SHA256,
            "unityfs_members": [{"member": probe.MEMBER, "bytes": probe.MEMBER_BYTES,
                                 "sha256": probe.MEMBER_SHA256, "unityfs": True}],
            "archive_members": [{"member": str(i)} for i in range(5)],
        }
        self.lock = {
            "schema_version": 1, "authority": dict(probe.AUTHORITY_HASHES),
            "packages": {"Piggy-LC_Office": {}, probe.PACKAGE: copy.deepcopy(self.observed)},
        }

    def check(self):
        probe.check_locked_package(self.lock, dict(probe.AUTHORITY_HASHES), self.observed)

    def test_original_provenance_accepted(self):
        self.check()

    def test_reject_changed_zip(self):
        self.observed["zip_sha256"] = "0" * 64
        with self.assertRaises(c7.CaptureError):
            self.check()

    def test_reject_changed_unityfs(self):
        self.observed["unityfs_members"][0]["sha256"] = "0" * 64
        with self.assertRaises(c7.CaptureError):
            self.check()

    def test_reject_changed_version(self):
        self.observed["version"] = "0.0.8"
        with self.assertRaises(c7.CaptureError):
            self.check()

    def test_reject_expanded_legacy_cohort(self):
        self.observed["flows"].append(probe.FLOW)
        with self.assertRaises(c7.CaptureError):
            self.check()

    def test_reject_changed_archive_inventory(self):
        self.observed["archive_members"].pop()
        with self.assertRaises(c7.CaptureError):
            self.check()

    def test_reject_changed_authority(self):
        self.lock["authority"] = {}
        with self.assertRaises(c7.CaptureError):
            self.check()


def ptr(number, file_id=0):
    return {"m_FileID": file_id, "m_PathID": number}


class FakeIndex:
    """Tiny serialized graph exercising the real owner matching helpers."""
    def __init__(self):
        self.keys = [ (probe.MEMBER, "CAB-test", pid) for pid in (101, 202, 303) ]
        self.objects = {}
        self.scripts = {}
        scripts = [
            ("DungeonFlow", "DunGen.Graph", "DunGen.dll"),
            ("ExtendedDungeonFlow", "LethalLevelLoader", "LethalLevelLoader.dll"),
            ("LevelMatchingProperties", "LethalLevelLoader", "LethalLevelLoader.dll"),
        ]
        import hashlib
        for key, (cls, namespace, assembly) in zip(self.keys, scripts):
            self.objects[key] = {"type": "MonoBehaviour",
                                 "raw_sha256": hashlib.sha256(str(key).encode()).hexdigest()}
            self.scripts[key] = {"m_ClassName": cls, "m_Namespace": namespace,
                                 "m_AssemblyName": assembly}
        self.objects[self.keys[0]]["tree"] = {"m_Name": probe.FLOW}
        self.objects[self.keys[1]]["tree"] = {
            "m_Name": "GoldenExtended",
            "<DungeonName>k__BackingField": probe.DUNGEON_NAME,
            "<DungeonFlow>k__BackingField": ptr(101),
            "<LevelMatchingProperties>k__BackingField": ptr(303),
        }
        self.objects[self.keys[2]]["tree"] = {
            "m_Name": "GoldenMatching",
            "levelTags": [{"_name": "Canyon", "_rarity": 20}],
            "currentRoutePrice": [{"_minMax": {"x": 0, "y": 100}, "_rarity": 20}],
            "currentWeather": [],
            "planetNames": [{"_name": "Vow", "_rarity": 15}],
            "m_GameObject": ptr(0),
        }

    def class_is(self, key, cls, namespace, assembly):
        d = self.scripts.get(key)
        return bool(d and d["m_ClassName"] == cls
                    and d["m_Namespace"] == namespace
                    and d["m_AssemblyName"] == assembly)

    def resolve(self, parent, pointer, required=False, expected=None):
        if not isinstance(pointer, dict) or set(pointer) != {"m_FileID", "m_PathID"}:
            raise c7.CaptureError("Malformed synthetic pointer")
        if pointer["m_FileID"] != 0:
            raise c7.CaptureError("Unresolved synthetic external pointer")
        if pointer["m_PathID"] == 0:
            if required:
                raise c7.CaptureError("Null mandatory synthetic pointer")
            return None
        key = (parent[0], parent[1], pointer["m_PathID"])
        if key not in self.objects:
            raise c7.CaptureError("Unknown synthetic path ID")
        if expected and self.objects[key]["type"] not in expected:
            raise c7.CaptureError("Unexpected synthetic type")
        return key

    def descriptor(self, key):
        return {"bundle_member": key[0], "serialized_file": key[1],
                "path_id": key[2], "type": self.objects[key]["type"],
                "raw_object_sha256": self.objects[key]["raw_sha256"],
                "script": self.scripts.get(key)}


class GoldenHotelObjectGraphTests(unittest.TestCase):
    def setUp(self):
        self.idx = FakeIndex()

    def mutate_and_refuse(self, change):
        change()
        with self.assertRaises(c7.CaptureError):
            probe.validated_target(self.idx)

    def test_exact_static_graph(self):
        result = probe.validated_target(self.idx)
        self.assertEqual(result["flow_name"], "GoldenHotel")
        self.assertEqual(result["extended_dungeon_flow"]["dungeon_name"], "Goldstay Hotel")
        self.assertEqual(result["level_matching_properties"]["serialized_fields"]
                         ["levelTags"][0]["_rarity"], 20)

    def test_wrong_case(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[0]]
                               ["tree"].update(m_Name="goldenhotel"))

    def test_missing_owner(self):
        self.mutate_and_refuse(lambda: self.idx.scripts.pop(self.idx.keys[1]))

    def test_wrong_dungeon_display(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update({"<DungeonName>k__BackingField": "Wrong Name"}))

    def test_unresolved_flow_link(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update({"<DungeonFlow>k__BackingField": ptr(999)}))

    def test_missing_matching(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update({"<LevelMatchingProperties>k__BackingField": ptr(0)}))

    def test_wrong_matching_class(self):
        self.mutate_and_refuse(lambda: self.idx.scripts[self.idx.keys[2]]
                               .update(m_ClassName="Unrelated"))

    def test_unresolved_matching_reference(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[2]]
                               ["tree"].update(external=ptr(999)))

    def test_missing_matching_list(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[2]]
                               ["tree"].pop("planetNames"))

    def test_duplicate_owner_pointer(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update(second_matching=ptr(303)))

    def test_external_flow_pointer(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update({"<DungeonFlow>k__BackingField": ptr(101, 1)}))

    def test_invalid_raw_object_hash(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[2]]
                               .update(raw_sha256="not-sha256"))


    def test_missing_flow(self):
        self.mutate_and_refuse(lambda: self.idx.scripts.pop(self.idx.keys[0]))

    def test_ambiguous_exact_flow(self):
        newkey = (probe.MEMBER, "CAB-test", 404)
        self.idx.objects[newkey] = copy.deepcopy(self.idx.objects[self.idx.keys[0]])
        self.idx.scripts[newkey] = copy.deepcopy(self.idx.scripts[self.idx.keys[0]])
        with self.assertRaises(c7.CaptureError):
            probe.validated_target(self.idx)

    def test_ambiguous_original_owner(self):
        newkey = (probe.MEMBER, "CAB-test", 505)
        self.idx.objects[newkey] = copy.deepcopy(self.idx.objects[self.idx.keys[1]])
        self.idx.scripts[newkey] = copy.deepcopy(self.idx.scripts[self.idx.keys[1]])
        with self.assertRaises(c7.CaptureError):
            probe.validated_target(self.idx)

    def test_two_matching_assets(self):
        newkey = (probe.MEMBER, "CAB-test", 606)
        self.idx.objects[newkey] = copy.deepcopy(self.idx.objects[self.idx.keys[2]])
        self.idx.scripts[newkey] = copy.deepcopy(self.idx.scripts[self.idx.keys[2]])
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[1]]
                               ["tree"].update(otherMatching=ptr(606)))

    def test_wrong_owner_reference_type(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[0]]
                               .update(type="GameObject"))

    def test_wrong_matching_tag_type(self):
        self.mutate_and_refuse(lambda: self.idx.objects[self.idx.keys[2]]
                               ["tree"]["levelTags"][0].update(_rarity="20"))

    def test_wrong_owner_namespace(self):
        self.mutate_and_refuse(lambda: self.idx.scripts[self.idx.keys[1]]
                               .update(m_Namespace="UnrelatedMod"))



if __name__ == "__main__":
    unittest.main()
