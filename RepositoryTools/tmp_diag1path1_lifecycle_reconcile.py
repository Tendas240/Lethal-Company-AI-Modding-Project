#!/usr/bin/env python3
from pathlib import Path
import json

STATE = Path('Current/CURRENT_STATE.json')
LIFECYCLE = Path('Knowledge/CURRENT_LIFECYCLE.md')
MAP = Path('Current/PROJECT_KNOWLEDGE_MAP.md')
CHECKPOINT = Path('Current/185_S1.42AK_BMDSFIX1_DIAG1PATH1_PROFILE_INDEX_LIFECYCLE_RECONCILIATION.md')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one occurrence, found {count}')
    return text.replace(old, new, 1)


state = json.loads(STATE.read_text(encoding='utf-8'))
assert state['updated'] == '2026-09-24'
assert state['runtime_test_outstanding'] is True
assert state['controllers']['build_enabled'] is False
assert state['controllers']['build_id'] == 'IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS'
assert state['controllers']['runtime_active_build'] == 'S1.42AK-BMDSFIX1-DIAG1'

scope = state['selected_scope']
assert scope['status'] == 'PHASE_C3F18_DIAG1_PRELOADER_BLOCKED_DIAG1PATH1_REVIEWED_PUBLICATION_OUTSTANDING'
state['updated'] = '2026-09-25'
scope['status'] = 'PHASE_C3F18_DIAG1_PRELOADER_BLOCKED_DIAG1PATH1_PUBLISHED_INDEXED_ACTIVATION_OUTSTANDING'
scope['finding'] = (
    'The exact published/indexed S1.42AK-BMDSFIX1-DIAG1 remains the repository runtime/evidence pointer, '
    'but two consecutive local launches are bounded preloader-block evidence and the long-name DIAG1 must not be rerun. '
    'Its identity-only successor S1.42AK-BMDSFIX1-DIAG1PATH1 is now exact-byte published and canonically indexed as '
    'Profiles/LC V1 S1.42AK-D1P1.r2z with SHA-256 0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6; '
    'ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json resolves it through EXPECTED_HASHES with 338 archive members. '
    'DIAG1PATH1 remains not runtime-armed, diagnostic support only and never acceptable as gameplay. '
    'S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted and its regular exact-byte Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived.'
)
scope['analysis_contract'] = (
    'Keep S1.42AK-BMDSFIX1 as the active gameplay candidate / not accepted. Treat S1.42AK-BMDSFIX1-DIAG1 as the still-routed historical diagnostic target that is locally preloader-blocked and must not be rerun. '
    'Treat S1.42AK-BMDSFIX1-DIAG1PATH1 as the exact published/indexed identity-only successor that remains inactive until a separate explicit runtime-activation checkpoint changes runtime/evidence routing. '
    'Do not import or run DIAG1PATH1 before that activation checkpoint, do not infer BMDSFIX1 acceptance from either diagnostic, do not waive the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow gate, and do not mix Black Mesa x Greenhouse/BMGHDIAG into this successor.'
)
next_action = (
    'Perform a separate explicit S1.42AK-BMDSFIX1-DIAG1PATH1 runtime-activation checkpoint. Activation may update only RuntimeInbox/ACTIVE_BUILD.txt and matching canonical lifecycle/controller routing required for Gale resolution and evidence attribution; '
    'it must not rebuild or alter profile, DLL, package, config or gameplay bytes and must not accept BMDSFIX1 or DIAG1PATH1. '
    'Do not import or run DIAG1PATH1 until that activation checkpoint is integrated and validated. The regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived.'
)
scope['next_action'] = next_action
state['next_action'] = next_action


def dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from dicts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from dicts(v)


long_diag = [d for d in dicts(scope) if d.get('build_id') == 'S1.42AK-BMDSFIX1-DIAG1' and 'runtime_validation_status' in d]
if len(long_diag) != 1:
    raise RuntimeError(f'expected one long DIAG1 runtime state, found {len(long_diag)}')
long_diag[0]['runtime_validation_status'] = 'PRELOADER_BLOCKED_BEFORE_DIAGNOSTIC_EXECUTION_DO_NOT_RERUN_DIAG1PATH1_PUBLISHED_INDEXED_ACTIVATION_OUTSTANDING'

successors = [d for d in dicts(scope) if d.get('build_id') == 'S1.42AK-BMDSFIX1-DIAG1PATH1']
if len(successors) != 1:
    raise RuntimeError(f'expected one DIAG1PATH1 successor state, found {len(successors)}')
succ = successors[0]
assert succ['status'] == 'INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_INDEXED_NOT_ARMED'
assert succ['profile_sha256'] == '0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6'
assert succ['published'] is False
assert succ['runtime_armed'] is False
succ['status'] = 'PUBLISHED_INDEXED_NOT_ARMED'
succ['profile'] = 'Profiles/LC V1 S1.42AK-D1P1.r2z'
succ['profile_sources'] = 'ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/'
succ['file_index'] = 'ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/FILE_INDEX.json'
succ['profile_index_result'] = 'ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json'
succ['publication_checkpoint'] = 'Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md'
succ['publication_evidence'] = 'BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md'
succ['publication_branch'] = 'c3f18-bmdsfix1-diag1path1-exact-publication'
succ['publication_workflow_run'] = 36067974897
succ['published_profile_commit'] = '1d13c152b3d44b118d8969bc6009e5adf7a7c48e'
succ['publication_integration_pr'] = 161
succ['publication_main_integration_commit'] = 'c1273fee0cdf666c56c7cb1a72d390e5a058349b'
succ['index_registry'] = 'Profiles/EXPECTED_HASHES.json'
succ['index_mapping_commit'] = '859efcd4bf736636b9431a0c52ba297f7c2f98d6'
succ['index_mapping_pr'] = 162
succ['index_mapping_merge_commit'] = '2fd739b118fd4d237f3e2658ba87210462c8fd2c'
succ['index_workflow_run'] = 36107014143
succ['index_commit'] = '26c0ab05a512dc98f1532b6c0742a6ef0033c9b4'
succ['index_exact_head_validation_run'] = 36107034365
succ['published'] = True
succ['indexed'] = True
succ['runtime_armed'] = False

STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

lifecycle = LIFECYCLE.read_text(encoding='utf-8')
lifecycle = replace_once(lifecycle, '**Last-Validated:** 2026-09-24', '**Last-Validated:** 2026-09-25', 'lifecycle date')
lifecycle = replace_once(
    lifecycle,
    '`BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md`  ',
    '`BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md`, `Current/181_S1.42AK_BMDSFIX1_DIAG1_PATH_LENGTH_BLOCK_AND_DIAG1PATH1_SOURCE_STATIC.md`, `Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`, `Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`, `BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`, `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`  ',
    'lifecycle evidence'
)
lifecycle = replace_once(lifecycle, '## DIAG1 launch block and DIAG1PATH1 reviewed successor', '## DIAG1 launch block and DIAG1PATH1 published/indexed successor', 'lifecycle section heading')
lifecycle = replace_once(
    lifecycle,
    'The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor has passed its inactive review build under `Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`. Frozen publication source is Actions artifact `10835876163` from review run `36063701766`; reviewed profile SHA-256 is `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`. It shortens the profile identity to `LC V1 S1.42AK-D1P1`, reducing the observed paths to 215/217 characters, while changing only `export.r2x` profile identity metadata and preserving all DLL/package/config bytes. DIAG1PATH1 is not yet published, indexed or runtime-armed.',
    'The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor is now exact-byte published and canonically indexed. Publication authority is `Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`; exact profile `Profiles/LC V1 S1.42AK-D1P1.r2z` remains SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, with only the reviewed `export.r2x` profile-identity delta relative to long-name DIAG1 and all protected DLL/package/config bytes unchanged. Canonical indexing is recorded by `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`: build ID `S1.42AK-BMDSFIX1-DIAG1PATH1`, profile identity `LC V1 S1.42AK-D1P1`, 338 archive members, resolution through `EXPECTED_HASHES`. DIAG1PATH1 remains **not runtime-armed / diagnostic support only / never accept**.',
    'lifecycle successor paragraph'
)
lifecycle = replace_once(lifecycle, '- Reviewed diagnostic successor: **S1.42AK-BMDSFIX1-DIAG1PATH1 — inactive review PASS / not published / not indexed / not armed / never accept**.', '- Diagnostic successor: **S1.42AK-BMDSFIX1-DIAG1PATH1 — published / indexed / not armed / diagnostic support only / never accept**.', 'lifecycle successor bullet')
lifecycle = replace_once(lifecycle, '- Runtime test outstanding: **yes — regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived; no new DIAG1PATH1 runtime is authorized before publication/index/activation**.', '- Runtime test outstanding: **yes — regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived; DIAG1PATH1 is published/indexed but no DIAG1PATH1 runtime is authorized before a separate explicit activation checkpoint**.', 'lifecycle runtime bullet')
lifecycle = replace_once(lifecycle, '- Selected scope: **Universal Interior Viability / Equal Availability — DIAG1PATH1 exact-byte publication next; gameplay candidate unchanged**.', '- Selected scope: **Universal Interior Viability / Equal Availability — DIAG1PATH1 publication/indexing complete; explicit runtime activation is the next bounded gate; gameplay candidate unchanged**.', 'lifecycle scope bullet')
lifecycle = replace_once(
    lifecycle,
    'Perform the separate `S1.42AK-BMDSFIX1-DIAG1PATH1` exact-byte publication checkpoint from frozen Actions artifact `10835876163` / review run `36063701766`. Materialize only the reviewed profile bytes SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6` and readable snapshot, then revalidate the identity-only delta without changing runtime controllers. Do **not** import or rerun the long-name DIAG1 profile. Profile-index reconciliation and explicit DIAG1PATH1 runtime activation remain later gates. BMDSFIX1 remains not accepted and its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived.',
    'Perform a separate explicit `S1.42AK-BMDSFIX1-DIAG1PATH1` runtime-activation checkpoint. The activation may change runtime/evidence routing only after re-verifying the exact published/indexed profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; it must not rebuild or alter profile, DLL, package, config or gameplay bytes and cannot accept DIAG1PATH1 or BMDSFIX1. Do **not** import or run DIAG1PATH1 before that activation checkpoint is integrated and validated. The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived.',
    'lifecycle next action'
)
lifecycle = replace_once(
    lifecycle,
    'The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. `RuntimeInbox/ACTIVE_BUILD.txt` still points to `S1.42AK-BMDSFIX1-DIAG1`, so invoking the helper now would still resolve the preloader-blocked long-name diagnostic and is therefore **not authorized**. Do not change that controller merely to bypass publication/indexing. After DIAG1PATH1 is exact-byte-published, profile-index-reconciled and explicitly runtime-activated in later gates, the repository-driven helper must resolve the newly authorized successor exact bytes. None of these diagnostic lifecycle operations may promote or accept BMDSFIX1.',
    'The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. `RuntimeInbox/ACTIVE_BUILD.txt` still points to `S1.42AK-BMDSFIX1-DIAG1`, so invoking the helper now would still resolve the preloader-blocked long-name diagnostic and remains **not authorized**. DIAG1PATH1 is now published and indexed, but the runtime pointer must change only in the separate explicit activation checkpoint. After that checkpoint is integrated and exact-head validated, the repository-driven helper must resolve the exact DIAG1PATH1 bytes. None of these diagnostic lifecycle operations may promote or accept BMDSFIX1 or DIAG1PATH1.',
    'lifecycle Gale paragraph'
)
LIFECYCLE.write_text(lifecycle, encoding='utf-8')

kmap = MAP.read_text(encoding='utf-8')
kmap = replace_once(kmap, '**Last-Validated:** 2026-09-24', '**Last-Validated:** 2026-09-25', 'map date')
kmap = replace_once(kmap, 'Accepted gameplay baseline and latest built artifact: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**.', 'Accepted gameplay baseline: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**. Active gameplay candidate / latest built gameplay artifact: **S1.42AK-BMDSFIX1 — not accepted**.', 'map lifecycle anchor')
kmap = replace_once(
    kmap,
    'The published/indexed `S1.42AK-BMDSFIX1-DIAG1` still occupies the runtime/evidence pointer, but two consecutive launches are now documented as preloader-blocked before diagnostic execution because the long Gale profile identity produced 260/262-character nested runtime paths. It must not be rerun. `S1.42AK-BMDSFIX1-DIAG1PATH1` is the reviewed identity-only successor: inactive review build PASS, short profile identity `LC V1 S1.42AK-D1P1`, reviewed profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, frozen publication source artifact `10835876163`; it is not yet published, indexed or armed. The immediate repository task is its separate exact-byte publication checkpoint, not a gameplay launch. BMDSFIX1 remains not accepted, its regular qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse/BMGHDIAG remains separate.',
    'The published/indexed `S1.42AK-BMDSFIX1-DIAG1` still occupies the runtime/evidence pointer, but two consecutive launches are documented as preloader-blocked before diagnostic execution and the long-name profile must not be rerun. Its identity-only successor `S1.42AK-BMDSFIX1-DIAG1PATH1` is now exact-byte published and canonically indexed: profile `Profiles/LC V1 S1.42AK-D1P1.r2z`, SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, canonical index result `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`, 338 archive members, `EXPECTED_HASHES` resolution. It remains not runtime-armed, diagnostic support only and never acceptable as gameplay. The immediate repository task is a separate explicit DIAG1PATH1 runtime-activation checkpoint; do not import or run it before that gate is integrated and validated. BMDSFIX1 remains not accepted, its regular qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse/BMGHDIAG remains separate.',
    'map DIAG1PATH1 paragraph'
)
MAP.write_text(kmap, encoding='utf-8')

checkpoint = """# S1.42AK-BMDSFIX1-DIAG1PATH1 — Profile-Index Lifecycle Reconciliation

**Date:** 2026-09-25  
**Status:** PUBLISHED + INDEXED / NOT ARMED / CURRENT-STATE DRIFT RECONCILED / DIAGNOSTIC SUPPORT ONLY / NEVER ACCEPT  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted

## Purpose

This checkpoint reconciles canonical lifecycle/navigation authority with repository reality after exact-byte DIAG1PATH1 publication and successful fail-closed profile-index reconciliation.

The successor is now repository-readable and deterministically mapped, but it is **not** runtime-armed by this checkpoint. No Gale import or runtime execution is authorized yet.

## Exact publication and index proof

- profile: `Profiles/LC V1 S1.42AK-D1P1.r2z`;
- profile SHA-256: `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`;
- profile identity: `LC V1 S1.42AK-D1P1`;
- archive members: `338`;
- readable snapshot: `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/`;
- canonical index result: `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`;
- build-ID resolution: `EXPECTED_HASHES`;
- publication authority: `Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`;
- publication integration PR: `#161` / main merge `c1273fee0cdf666c56c7cb1a72d390e5a058349b`;
- index mapping PR: `#162` / main merge `2fd739b118fd4d237f3e2658ba87210462c8fd2c`;
- successful profile-index workflow: `36107014143` / run `#22`;
- profile-index commit: `26c0ab05a512dc98f1532b6c0742a6ef0033c9b4`;
- exact-head Knowledge Architecture validation: `36107034365` / run `#760` / success.

## Preserved boundaries

- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1-DIAG1`; the long-name DIAG1 remains preloader-blocked and must not be rerun.
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS` and guards exact BMDSFIX1 bytes.
- S1.42AK remains the accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted.
- The regular exact-byte Black Mesa x `DeepSewersFlow` BMDSFIX1 qualification remains outstanding and unwaived.
- Black Mesa x Greenhouse/BMGHDIAG remains separate.
- No profile, DLL, package, config, mod-state or gameplay bytes are changed by this lifecycle reconciliation.
- DIAG1PATH1 remains **diagnostic support only / never accept**.

## Exact next bounded gate

Perform a separate explicit **S1.42AK-BMDSFIX1-DIAG1PATH1 runtime-activation checkpoint**. That gate may update runtime/evidence routing only after re-verifying the exact published/indexed successor bytes. It must not rebuild gameplay/profile bytes or imply acceptance. Do not import or run DIAG1PATH1 before that activation checkpoint is integrated and exact-head validated.
"""
CHECKPOINT.write_text(checkpoint, encoding='utf-8')
