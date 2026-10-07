#!/usr/bin/env python3
"""Independent byte-level review validator; no dependency on the builder."""
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = 'Profiles/LC V1 S1.42AK-BMAFR1.r2z'
PROFILE = 'Profiles/LC V1 S1.42AK-BMAFR1I1.r2z'
PARENT_SHA = '8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5'
PLUGIN = 'BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll'
PRESERVED = {
    'BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll': 'c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1',
    'BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll': '901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06',
    'BepInEx/config/LethalLevelLoader.cfg': 'd2a01df4829623ef3dcbacf8c09e98a9c6a72b0885f9302502da2bcb91b31b68',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_members(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(archive.testzip() is None, 'ZIP CRC failed')
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP members')
        require(all(not n.startswith(('/', '\\')) and '..' not in n.replace('\\', '/').split('/') for n in names), 'Unsafe ZIP path')
        return {n: archive.read(n) for n in names}


def validate_members(parent, built, dll):
    require(len(parent) == 337 and len(built) == 338, 'Member count drift')
    require(set(built) - set(parent) == {PLUGIN}, 'Unexpected added member')
    require(not set(parent) - set(built), 'Removed parent member')
    changed = [n for n in parent if parent[n] != built[n]]
    require(changed == ['export.r2x'], 'Unexpected existing-member change: ' + repr(changed))
    # An independent reversal proves that every byte except the identity is retained.
    pattern = rb'(?m)^profileName: LC V1 S1\.42AK-BMAFR1I1(?=\r?$)'
    reverted, count = re.subn(pattern, b'profileName: LC V1 S1.42AK-BMAFR1', built['export.r2x'])
    require(count == 1 and reverted == parent['export.r2x'], 'Export drift beyond exact profile identity')
    require(dll and built[PLUGIN] == dll, 'Injected DLL does not match compiled bytes')
    for name, digest in PRESERVED.items():
        require(sha(parent[name]) == sha(built[name]) == digest, 'Critical parent bytes drift: ' + name)
    foundry_header = ('[' + '\u200b' * 9 + 'Custom Dungeon:  Abandoned Foundry]').encode()
    require(built['BepInEx/config/LethalLevelLoader.cfg'].count(foundry_header) == 1, 'Raw Foundry binding lost')
    require(b'[Custom Dungeon:  Abandoned Foundry]' not in built['BepInEx/config/LethalLevelLoader.cfg'], 'Plain Foundry duplicate')
    return dict(parent_members=337, review_members=338, changed_existing_members=changed,
                added_members=[PLUGIN], removed_members=[], package_changes=0, config_changes=0,
                critical_preserved_sha256=PRESERVED)


def self_test(parent, built, dll):
    cases = []
    mutations = {
        'config-drift': lambda b: b.__setitem__('BepInEx/config/LethalLevelLoader.cfg', b['BepInEx/config/LethalLevelLoader.cfg'] + b'\n'),
        'existing-diagnostic-replaced': lambda b: b.__setitem__(next(iter(PRESERVED)), b'wrong'),
        'member-removed': lambda b: b.pop(next(iter(PRESERVED))),
        'extra-plugin': lambda b: b.__setitem__('BepInEx/plugins/unauthorized.dll', b'wrong'),
        'package-export-drift': lambda b: b.__setitem__('export.r2x', b['export.r2x'] + b'\n# unauthorized\n'),
        'wrong-profile-identity': lambda b: b.__setitem__('export.r2x', b['export.r2x'].replace(b'BMAFR1I1', b'BMAFR1I2')),
        'wrong-instrumentation-dll': lambda b: b.__setitem__(PLUGIN, b'wrong'),
    }
    for name, mutate in mutations.items():
        altered = dict(built)
        mutate(altered)
        try:
            validate_members(parent, altered, dll)
        except ValueError:
            cases.append(name)
        else:
            raise ValueError('Negative case unexpectedly accepted: ' + name)
    return cases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--artifact-root', type=Path, default=ROOT / 'review-output')
    ap.add_argument('--parent', type=Path, default=ROOT / PARENT)
    args = ap.parse_args()
    parent_bytes = args.parent.read_bytes()
    require(sha(parent_bytes) == PARENT_SHA, 'Wrong exact parent')
    profile_bytes = (args.artifact_root / PROFILE).read_bytes()
    dll = (args.artifact_root / 'DLL/S142AKBMAFR1I1.dll').read_bytes()
    parent, built = read_members(parent_bytes), read_members(profile_bytes)
    report = validate_members(parent, built, dll)
    result = json.loads((args.artifact_root / 'Evidence/BUILD_RESULT.json').read_text())
    require(result['assembly_name'] == 'S142AKBMAFR1I1', 'Assembly identity report drift')
    require(result['parent_sha256'] == PARENT_SHA, 'Parent hash report drift')
    require(result['dll_sha256'] == sha(dll), 'DLL hash report drift')
    require(result['profile_sha256'] == sha(profile_bytes), 'Profile hash report drift')
    require(not result['profile_indexing'] and not result['published'] and not result['runtime_armed'], 'Inactive scope drift')
    report.update(status='PASS_INACTIVE_COMPILE_ARCHIVE_REVIEW_ONLY',
                  parent_sha256=PARENT_SHA, profile_sha256=sha(profile_bytes), dll_sha256=sha(dll),
                  negative_cases=self_test(parent, built, dll) if args.self_test else [],
                  runtime_proof=False, publication_authorized=False,
                  actions_zip_rehash='OUTSTANDING_AFTER_ARTIFACT_FREEZE')
    (args.artifact_root / 'Evidence/ARCHIVE_VERIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
