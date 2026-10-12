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


if __name__ == "__main__":
    unittest.main()
