#!/usr/bin/env python3
import json
import re
from pathlib import Path

B='S1.42AI-DIAG1'
TITLE='ShyGuy Isolation Diagnostic'
PROFILE='Profiles/LC V1 S1.42AI-DIAG1 ShyGuy Isolation.r2z'
SHA='22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd'
PLUGIN_SHA='bc8d51121451ecd1b1550e2aa6007991983c7a88ad93c86c38541ec0d358a2b3'
PARENT='S1.42AI'
PARENT_SHA='d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2'
CAND='Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md'
PSTAT='Current/Projektstatus_S1.42AI-DIAG1_CANDIDATE.json'
SOURCES='ProfileSources/S1.42AI-DIAG1/'
INDEX=SOURCES+'FILE_INDEX.json'
CONTRACT='AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md'
RUN=34777833867
BUILD_COMMIT='1018ac909435a51f1b98ceb9dfdad0599dc4dcc4'
MARK='<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=S1.42AI-DIAG1 runtime_test_outstanding=true -->'


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def dump(p,o):
    Path(p).write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')


auto=load('Current/AUTO_BUILD_RESULT.json')
if (auto.get('build_id'),auto.get('output_sha256'),auto.get('base_sha256')) != (B,SHA,PARENT_SHA):
    raise RuntimeError('AUTO_BUILD_RESULT identity/lineage mismatch')
ctl_file=load('BuildSpecs/current.json')
expect=(False,'IDLE_AFTER_S1.42AI-DIAG1_BUILD_AWAITING_RUNTIME_VALIDATION',PROFILE,SHA)
actual=(ctl_file.get('enabled'),ctl_file.get('build_id'),ctl_file.get('base_profile'),ctl_file.get('base_sha256'))
if actual != expect:
    raise RuntimeError(f'Build controller mismatch: {actual!r}')
if not Path(PROFILE).is_file() or not Path(INDEX).is_file():
    raise RuntimeError('DIAG1 materialized profile/snapshot missing')

candidate=f'''# S1.42AI-DIAG1 Build Candidate — ShyGuy Isolation Diagnostic

**Date:** 2026-09-13  
**Status:** BUILD PASS / PRE-BUILD STATIC GATE PASS / MATERIALIZED DELTA VERIFIED / ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED  
**Accepted gameplay baseline:** `S1.42AH`  
**Parent full-normal candidate:** `S1.42AI`

## Candidate identity

- Build: `{B}`
- Profile: `{PROFILE}`
- SHA-256: `{SHA}`
- Parent: `{PARENT}`
- Canonical build workflow run: `{RUN}`
- Automated build commit: `{BUILD_COMMIT}`
- Readable snapshot: `{SOURCES}`
- File index: `{INDEX}`
- DIAG1 plugin DLL SHA-256: `{PLUGIN_SHA}`
- Guard contract: `{CONTRACT}`
- Final pre-build static gate: run `34764692012`, run number `9`, SUCCESS, artifact `10319769370`

## Proven build boundary

The canonical build completed with no package additions, removals, or state changes. The materialized profile contains 337 unique members, the reviewed DIAG1 overlay, and the exact diagnostic plugin. All 235 approved config target values and all 47 text assertions were rechecked against the real output profile with zero failures.

## Runtime diagnostic gate

Runtime evidence must establish:

1. DIAG1 startup/identity/config/guard/transpiler markers all succeed;
2. no `DIAG1_ISOLATION_BYPASS` reports a live non-ShyGuy `EnemyAI`;
3. no unexpected non-ShyGuy enemy is observed;
4. exact Shy Guy remains observable and is never suppressed merely for being exterior;
5. exercised owner-prevention markers remain bounded and produce no exception/retry flood;
6. no broad shared spawn/network lifecycle regression appears.

## Retained full-normal S1.42AI gate

Diagnostic success does not accept S1.42AI. The full-normal gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory afterward and is deferred, not waived.

## Acceptance boundary

S1.42AH remains the sole accepted gameplay baseline. DIAG1 is diagnostic evidence only.
'''
Path(CAND).write_text(candidate,encoding='utf-8')

dump(PSTAT,{
    'schema_version':1,'updated':'2026-09-13','build_id':B,
    'status':'ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED','accepted_baseline':'S1.42AH',
    'parent':PARENT,'profile':PROFILE,'sha256':SHA,'candidate_record':CAND,
    'profile_sources':SOURCES,'file_index':INDEX,'workflow_run':RUN,'build_commit':BUILD_COMMIT,
    'plugin_dll_sha256':PLUGIN_SHA,'guard_contract':CONTRACT,'runtime_test_outstanding':True,
    'full_normal_s142ai_gate':'DEFERRED_NOT_WAIVED',
    'full_normal_candidate_record':'Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md'
})

state=load('Current/CURRENT_STATE.json')
latest={
    'build_id':B,'title':TITLE,
    'status':'BUILD_PASS_STATIC_AND_MATERIALIZED_DELTA_VERIFIED_RUNTIME_VALIDATION_OUTSTANDING',
    'profile':PROFILE,'sha256':SHA,'candidate_record':CAND,'project_status':PSTAT,
    'build_plan':'BuildSpecs/S1.42AI_PLAN.md','profile_sources':SOURCES,'file_index':INDEX,
    'workflow_run':RUN,'build_commit':BUILD_COMMIT,'parent':PARENT,
    'analysis_contract':CONTRACT,'plugin_dll_sha256':PLUGIN_SHA
}
active=dict(latest)
active['status']='ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED'
state['updated']='2026-09-13'
state['latest_built_artifact']=latest
state['active_candidate']=active
state['runtime_test_outstanding']=True
sel=state.setdefault('selected_scope',{})
sel.update({
    'status':'DIAGNOSTIC_RUNTIME_VALIDATION_OUTSTANDING_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED',
    'candidate_build_id':B,'profile':PROFILE,'sha256':SHA,'candidate_record':CAND,'project_status':PSTAT,
    'analysis_contract':CONTRACT,'analysis_status':'DIAG1_BUILT_AND_STATIC_VALIDATED_RUNTIME_DIAGNOSTIC_OUTSTANDING',
    'finding':'S1.42AI-DIAG1 is built from S1.42AI with the reviewed ShyGuy-only diagnostic overlay and exact narrow guard plugin. Canonical build and materialized profile verification passed; runtime diagnostic evidence is now required. The normal-stack S1.42AI acceptance gate remains deferred and is not waived.',
    'currently_irrelevant_actions':[]
})
diag=sel.setdefault('diagnostic_revision',{})
diag.update({
    'build_id':B,'status':'BUILT_ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED','base_build_id':PARENT,
    'base_profile':'Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z','base_sha256':PARENT_SHA,
    'profile':PROFILE,'sha256':SHA,'candidate_record':CAND,'project_status':PSTAT,
    'workflow_run':RUN,'build_commit':BUILD_COMMIT,'plugin_dll_sha256':PLUGIN_SHA,
    'full_normal_validation':'DEFERRED_UNTIL_AFTER_DIAGNOSTIC_NOT_WAIVED'
})
state['next_action']='Runtime-test S1.42AI-DIAG1 as the active temporary diagnostic candidate. Verify DIAG1 startup/identity/config/guard markers, exercise the ShyGuy-only round, fail on any DIAG1_ISOLATION_BYPASS or unexpected non-ShyGuy enemy, preserve ShyGuy observability, then upload the exact DIAG1 LogOutput.log. Diagnostic success does not accept S1.42AI; its full-normal BCMER ShyGuy gate remains required afterward.'
state['controllers'].update({
    'build_enabled':False,
    'build_id':'IDLE_AFTER_S1.42AI-DIAG1_BUILD_AWAITING_RUNTIME_VALIDATION',
    'build_base_profile':PROFILE,'build_base_sha256':SHA,'runtime_active_build':B
})
dump('Current/CURRENT_STATE.json',state)
Path('RuntimeInbox/ACTIVE_BUILD.txt').write_text(B+'\n',encoding='utf-8')

lin=load('Current/BUILD_LINEAGE.json')
lin['date']='2026-09-13'
lin['active_candidate_build_id']=B
lin['latest_built_artifact_id']=B
if any(x.get('id')==B for x in lin['builds']):
    raise RuntimeError('DIAG1 lineage entry already exists')
lin['builds'].append({
    'id':B,'title':TITLE,'status':'active-diagnostic-runtime-candidate','parent':PARENT,
    'profile':PROFILE,'sha256':SHA,'build_plan':'BuildSpecs/S1.42AI_PLAN.md',
    'candidate_record':CAND,'decision_record':CAND,'project_status':PSTAT,
    'workflow_run':RUN,'build_commit':BUILD_COMMIT,'safe_as_gameplay_base':False,
    'principal_feature':'temporary ShyGuy-only diagnostic isolation using exact reviewed config gates and narrow package/native owner guards'
})
lin.setdefault('feature_index',{})['BCMER_ShyGuy_DIAG1_isolation']=B
dump('Current/BUILD_LINEAGE.json',lin)

integ=load('Current/ARTIFACT_EVIDENCE_INTEGRITY.json')
integ['updated']='2026-09-13'
for x in integ['pending_profiles']:
    if x.get('build_id')==PARENT:
        x['role']='DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED'
        x['note']='Full-normal S1.42AI gate remains mandatory after DIAG1; diagnostic success cannot replace it.'
if any(x.get('build_id')==B for x in integ['pending_profiles']):
    raise RuntimeError('DIAG1 pending entry already exists')
integ['pending_profiles'].append({
    'build_id':B,'role':'ACTIVE_RUNTIME_CANDIDATE_PENDING','profile':PROFILE,'profile_sha256':SHA,
    'profile_sources':SOURCES,'file_index':INDEX,'export':SOURCES+'export.r2x',
    'candidate_record':CAND,'project_status':PSTAT,'build_plan':'BuildSpecs/S1.42AI_PLAN.md',
    'guard_contract':CONTRACT,'plugin_dll_sha256':PLUGIN_SHA,
    'runtime_evidence_required':False,'partial_runtime_evidence_present':False
})
dump('Current/ARTIFACT_EVIDENCE_INTEGRITY.json',integ)

Path('Knowledge/CURRENT_LIFECYCLE.md').write_text(f'''{MARK}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `{CAND}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `{CONTRACT}`  
**Last-Validated:** 2026-09-13

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact / active candidate

**{B} — {TITLE} — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `{PROFILE}`  
SHA-256: `{SHA}`  
Parent: `{PARENT}`  
Candidate: `{CAND}`  
Canonical build run: `{RUN}`  
Build commit: `{BUILD_COMMIT}`

The canonical build, pre-build static gate, and materialized profile checks passed. Package state is unchanged; the reviewed diagnostic config overlay and exact narrow plugin are present.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **{B}**.
- Active candidate: **{B}**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1_BUILD_AWAITING_RUNTIME_VALIDATION` and guards the exact DIAG1 profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = {B}` attributes the next evidence to DIAG1.

## Diagnostic runtime gate

Use `{CONTRACT}` and `{CAND}`. Require successful startup/identity/config/guard markers, no `DIAG1_ISOLATION_BYPASS`, no unexpected non-ShyGuy live enemy, and preserved exact Shy Guy observability.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` is deferred until after DIAG1 and is **not waived**.

## Exact next project action

{state['next_action']}
''',encoding='utf-8')

Path('Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md').write_text(f'''{MARK}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{CAND}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `{CONTRACT}`  
**Last-Validated:** 2026-09-13

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active temporary diagnostic candidate: **{B}**, SHA-256 `{SHA}`. Runtime validation is outstanding.

## Active scope

Runtime-test the exact DIAG1 profile under `{CONTRACT}`. The diagnostic must isolate exact Shy Guy while preserving narrow owner/native lifecycle and fail visibly on any non-ShyGuy bypass.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after DIAG1; diagnostic success cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
''',encoding='utf-8')

Path('Current/ARTIFACT_EVIDENCE_INTEGRITY.md').write_text(f'''{MARK}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-13

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / active runtime candidate: {B}

Artifact: `{PROFILE}`  
SHA-256: `{SHA}`  
Candidate record: `{CAND}`  
Project status: `{PSTAT}`  
Readable snapshot: `{SOURCES}`  
Plugin DLL SHA-256: `{PLUGIN_SHA}`

{B} has no final runtime decision and is indexed as `ACTIVE_RUNTIME_CANDIDATE_PENDING`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after DIAG1.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
''',encoding='utf-8')

km=Path('Current/PROJECT_KNOWLEDGE_MAP.md')
text=km.read_text(encoding='utf-8')
text=re.sub(r'<!-- LIVE_STATE:.*?-->',MARK,text,count=1)
block=f'''## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact and active temporary diagnostic runtime candidate: **{B} — {TITLE} — NOT ACCEPTED**. Runtime diagnostic validation is outstanding. Candidate authority: `{CAND}`; implementation/runtime contract: `{CONTRACT}`.

`BuildSpecs/current.json` is disabled and guards the exact DIAG1 profile/SHA; `RuntimeInbox/ACTIVE_BUILD.txt = {B}` attributes the next runtime evidence to the diagnostic candidate.

The DIAG1 implementation/static/build stage is complete. The next action is the bounded DIAG1 runtime diagnostic. The ordinary S1.42AI full-normal BCMER ShyGuy acceptance gate remains explicitly deferred and not waived; diagnostic success cannot replace it. Use `Knowledge/CURRENT_LIFECYCLE.md` for execution order.

'''
text,n=re.subn(r'## Current lifecycle anchor\n.*?(?=## Authority rule)',block,text,count=1,flags=re.S)
if n!=1:
    raise RuntimeError('Knowledge map lifecycle block not found')
km.write_text(text,encoding='utf-8')

lm=Path('Current/BUILD_LINEAGE.md')
text=lm.read_text(encoding='utf-8').replace('**Last-Validated:** 2026-09-10','**Last-Validated:** 2026-09-13',1)
text,n=re.subn(r'## Current lineage head\n.*?(?=For live lifecycle state)',f'''## Current lineage head

- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** {B} — {TITLE}.
- **Active candidate:** {B} — **DIAGNOSTIC RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**.
- **Deferred full-normal gate:** S1.42AI — still mandatory after DIAG1.
- **Current gate:** run the DIAG1 runtime validation from `{CAND}`.

''',text,count=1,flags=re.S)
if n!=1:
    raise RuntimeError('Build lineage head not found')
old='| S1.42AI | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** | Single-variable BCMER ShyGuy interior-only correction from accepted S1.42AH; exact static delta verified, runtime gate outstanding. |'
if old not in text:
    raise RuntimeError('S1.42AI lineage row not found')
text=text.replace(old,old.replace('**ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**','**DEFERRED FULL-NORMAL RUNTIME GATE / NOT ACCEPTED**')+'\n| S1.42AI-DIAG1 | **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED** | Temporary exact ShyGuy isolation diagnostic built from S1.42AI; static/build/materialized delta verified, runtime diagnostic outstanding. |',1)
lm.write_text(text,encoding='utf-8')
