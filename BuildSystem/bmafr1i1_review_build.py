#!/usr/bin/env python3
"""One isolated inactive build. Never index, publish or update live controllers."""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import dnfile

ROOT = Path(__file__).resolve().parents[1]
BASE = 'cc26952be87ab2ff3e441a208a3357da66e3a89b'
PATCH = 'Patches/S142AKBMAFR1I1'
PARENT = 'Profiles/LC V1 S1.42AK-BMAFR1.r2z'
PARENT_SHA = '8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5'
PROFILE = 'Profiles/LC V1 S1.42AK-BMAFR1I1.r2z'
MEMBER = 'BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll'
OUT = ROOT / 'review-output'
EVIDENCE = OUT / 'Evidence'
WORK = ROOT / 'review-work'
LOCKED = [PATCH, 'AnalysisTools/validate_s142ak_bmafr1i1_source.py',
          'AnalysisTools/generate_s142ak_bmafr1i1_contract_data.py',
          'SourceEvidence/BMAFR1Instrumentation/EXACT_DEPENDENCY_CONTRACTS.json',
          '.github/workflows/s142ak-bmafr1i1-source-static.yml',
          'RepositoryTools/gale_profile_path_length_guard.py',
          'Current/232_S1.42AK_BMAFR1I1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md',
          'Current/CURRENT_STATE.json', 'BuildSpecs/current.json',
          'RuntimeInbox/ACTIVE_BUILD.txt', 'Current/AUTO_BUILD_RESULT.json',
          'Profiles/EXPECTED_HASHES.json',
          'ProfileSources/S1.42AK-BMAFR1/PROFILE_INDEX_RESULT.json', PARENT]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def command(args, log=None):
    result = subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    if log:
        (EVIDENCE / log).write_text(result.stdout, encoding='utf-8')
    print(result.stdout, end='', flush=True)
    require(result.returncode == 0, 'Command failed: ' + repr(args))
    return result.stdout


def lock_inputs():
    raw = subprocess.check_output(['git', 'ls-tree', '-r', '-z', BASE, '--', *LOCKED], cwd=ROOT)
    records = {}
    for item in raw.split(b'\0'):
        if not item:
            continue
        meta, path_bytes = item.split(b'\t', 1)
        mode, kind, blob = meta.decode().split()
        path = path_bytes.decode()
        require(kind == 'blob' and mode == '100644', 'Unexpected input mode: ' + path)
        data = (ROOT / path).read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(actual == blob, 'Integrated input bytes changed: ' + path)
        records[path] = {'git_blob': blob, 'sha256': sha(data)}
    require(len(records) >= 24, 'Incomplete frozen input tree')
    expected_patch = {p for p in records if p.startswith(PATCH + '/')}
    actual_patch = {p.relative_to(ROOT).as_posix() for p in (ROOT / PATCH).rglob('*') if p.is_file()}
    require(actual_patch == expected_patch and len(expected_patch) == 11, 'Patch directory drift')
    return records


def main():
    os.chdir(ROOT)
    require(not OUT.exists() and not WORK.exists(), 'Review output/work already exists; refuse overwrite')
    require(not (ROOT / PROFILE).exists(), 'Review profile already published; refuse rebuild')
    require(not (ROOT / 'ProfileSources/S1.42AK-BMAFR1I1').exists(), 'Unauthorized successor index exists')
    EVIDENCE.mkdir(parents=True)
    WORK.mkdir()
    command(['git', 'fetch', '--no-tags', '--depth=1', 'origin', BASE], 'input-fetch.log')
    inputs = lock_inputs()
    spec = json.loads((ROOT / 'BuildSpecs/S1.42AK-BMAFR1I1.json').read_text())
    expected_spec = dict(enabled=False, review_only=True, build_id='S1.42AK-BMAFR1I1',
                         source_main_commit=BASE, base_profile=PARENT, base_sha256=PARENT_SHA,
                         profile_name='LC V1 S1.42AK-BMAFR1I1', output_profile=PROFILE,
                         overwrite=False, mod_state_changes=[], mod_additions=[], mod_removals=[],
                         config_patches=[], file_injections=[], local_plugin_builds=[], text_assertions=[])
    require(spec == expected_spec, 'Review recipe exceeds exact authorized scope')
    parent_data = (ROOT / PARENT).read_bytes()
    require(sha(parent_data) == PARENT_SHA, 'Parent binary hash mismatch')
    index = json.loads((ROOT / 'ProfileSources/S1.42AK-BMAFR1/PROFILE_INDEX_RESULT.json').read_text())
    hashes = json.loads((ROOT / 'Profiles/EXPECTED_HASHES.json').read_text())
    require(index['sha256'] == PARENT_SHA and index['zip_members'] == 337, 'Parent index mismatch')
    require(hashes[PARENT]['sha256'] == PARENT_SHA and hashes[PARENT]['build_id'] == 'S1.42AK-BMAFR1', 'Parent mapping mismatch')
    command([sys.executable, 'AnalysisTools/generate_s142ak_bmafr1i1_contract_data.py', '--check'], 'generated-contract.log')
    command([sys.executable, 'AnalysisTools/validate_s142ak_bmafr1i1_source.py', '--self-test'], 'source-static-before.log')
    command([sys.executable, 'RepositoryTools/gale_profile_path_length_guard.py', '--spec',
             'BuildSpecs/S1.42AK-BMAFR1I1.json'], 'path-guard.log')
    sdk = command(['dotnet', '--info'], 'dotnet-info.log')
    project = PATCH + '/S142AKBMAFR1I1.csproj'
    props = ['-p:BaseIntermediateOutputPath=' + str(WORK / 'obj') + '/',
             '-p:MSBuildProjectExtensionsPath=' + str(WORK / 'obj') + '/',
             '-p:OutputPath=' + str(WORK / 'bin') + '/']
    command(['dotnet', 'restore', project, '--packages', str(WORK / 'packages'), *props], 'restore.log')
    assets = json.loads((WORK / 'obj/project.assets.json').read_text())
    direct = {'BepInEx.Core': '5.4.21', 'HarmonyX': '2.10.2', 'LethalCompany.GameLibs.Steam': '81.0.5-ngd.0'}
    for name, version in direct.items():
        require(name + '/' + version in assets['libraries'], 'Resolved dependency mismatch: ' + name)
    build_log = command(['dotnet', 'build', project, '-c', 'Release', '--no-restore', *props], 'compile.log')
    require(re.search(r'\b0 Warning\(s\)', build_log) and re.search(r'\b0 Error\(s\)', build_log),
            'Clean compilation requires zero warnings and errors; no automatic source repair')
    dll = WORK / 'bin/S142AKBMAFR1I1.dll'
    dll_data = dll.read_bytes()
    pe = dnfile.dnPE(data=dll_data)
    require(pe.net is not None and len(pe.net.mdtables.Assembly.rows) == 1, 'Missing/ambiguous assembly')
    identity = str(pe.net.mdtables.Assembly.rows[0].Name)
    require(identity == 'S142AKBMAFR1I1', 'Wrong compiled assembly identity')
    references = {str(a.Name): f'{a.MajorVersion}.{a.MinorVersion}.{a.BuildNumber}.{a.RevisionNumber}'
                  for a in pe.net.mdtables.AssemblyRef.rows}
    pe.close()
    command([sys.executable, 'AnalysisTools/validate_s142ak_bmafr1i1_source.py', '--self-test'], 'source-static-after.log')
    require(lock_inputs() == inputs, 'Inputs changed during build')
    output = OUT / PROFILE
    output.parent.mkdir(parents=True)
    with zipfile.ZipFile(ROOT / PARENT) as src:
        names = src.namelist()
        require(len(names) == len(set(names)) == 337 and MEMBER not in names, 'Parent member set mismatch')
        export = src.read('export.r2x')
        old = b'profileName: LC V1 S1.42AK-BMAFR1'
        new = b'profileName: LC V1 S1.42AK-BMAFR1I1'
        lines = export.splitlines(keepends=True)
        hits = [i for i, line in enumerate(lines) if line.rstrip(b'\r\n') == old]
        require(len(hits) == 1, 'Parent profileName not uniquely exact')
        i = hits[0]
        lines[i] = new + lines[i][len(old):]
        changed_export = b''.join(lines)
        with zipfile.ZipFile(output, 'x') as dst:
            for info in src.infolist():
                data = changed_export if info.filename == 'export.r2x' else src.read(info.filename)
                dst.writestr(info, data)
            info = zipfile.ZipInfo(MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
            dst.writestr(info, dll_data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    (OUT / 'DLL').mkdir()
    (OUT / 'DLL/S142AKBMAFR1I1.dll').write_bytes(dll_data)
    packages = {k: {'sha512': v.get('sha512'), 'type': v['type']} for k, v in assets['libraries'].items()}
    (EVIDENCE / 'project.assets.json').write_text(json.dumps(assets, indent=2) + '\n')
    report = dict(status='COMPILE_PASS_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION',
                  build_id='S1.42AK-BMAFR1I1', source_main_commit=BASE,
                  build_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  run_id=os.environ.get('GITHUB_RUN_ID'), run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),
                  assembly_name=identity, assembly_references=references, dll_sha256=sha(dll_data),
                  parent_sha256=PARENT_SHA, profile_sha256=sha(output.read_bytes()),
                  inputs=inputs, resolved_packages=packages, profile_indexing=False,
                  published=False, runtime_armed=False, runtime_proof=False,
                  qualification='Source/static output retains historical NOT_RUN_NOT_AUTHORIZED labels; '
                  'the separate compile log establishes compilation under Current/232 only. '
                  'No Harmony/JIT installation, loader/runtime, emitter or root-cause proof.')
    (EVIDENCE / 'BUILD_RESULT.json').write_text(json.dumps(report, indent=2) + '\n')
    command(['git', 'diff', '--exit-code'], 'tracked-worktree.log')
    require(not (ROOT / 'ProfileSources/S1.42AK-BMAFR1I1').exists(), 'Indexing occurred')
    print(json.dumps({k: v for k, v in report.items() if k not in {'inputs', 'resolved_packages'}}, indent=2))


if __name__ == '__main__':
    main()
