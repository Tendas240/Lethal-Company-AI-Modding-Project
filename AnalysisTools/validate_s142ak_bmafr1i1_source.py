#!/usr/bin/env python3
"""Static syntax, safety-surface, exact evidence and symbolic injection checks.

No C# compilation, assembly loading, profile construction or runtime execution.
This gate is deliberately not a compiler, runtime proof or acceptance authority.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import yaml
from pathlib import Path
import xml.etree.ElementTree as ET

from tree_sitter import Language, Parser
import tree_sitter_c_sharp

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / 'Patches/S142AKBMAFR1I1'
EVIDENCE = ROOT / 'SourceEvidence/BMAFR1Instrumentation/EXACT_DEPENDENCY_CONTRACTS.json'
EVIDENCE_SHA256 = 'f873eecd4a2d03b2e45afbc73686ae8d189014159895e96fa27800969df0eae2'
PARSER = Parser(Language(tree_sitter_c_sharp.language()))
FILES = {'Plugin.cs', 'Contracts.cs', 'ContractData.cs', 'GameAssemblyProvenance.cs', 'IlGuard.cs', 'Probes.cs', 'Observers.cs', 'ArrayAnchor.cs'}

CALLS = {
    'Observers.cs': set('Summary Begin Bone BoneMap GetValue IsInstanceOfType Require Emit Find Read IsPeer MeshFacts Path Fault Marker ReferenceEquals Snapshot GetTimestamp Text Track Remove ToArray TryGetValue Count Where EscapeDataString GetInstanceID GetType Select ToString Add ContainsKey GetBlendShapeName GetChild IsChildOf Reverse Pop Push IsNullOrWhiteSpace Join GetComponentsInChildren'.split()),
    'ArrayAnchor.cs': set('CompareExchange Increment Read Max Min GetTimestamp IsNullOrEmpty'.split()),
    'Probes.cs': set('Callback Require Contains EmptyBoundary Equals Check Slot InsertRange Select Where ToArray DeclareLocal nameof GetField GetMethod'.split()),
    'Plugin.cs': set('Summary PatchTargets Require Resolve Contains GetPatchInfo Hook Exchange Read Marker Tick SafeLog GetTimestamp Write GetType Patch UnpatchSelf nameof Concat Count LogInfo GetMethod ToLocalTime ToString'.split()),
    'Contracts.cs': set('All SequenceEqual GetAssemblies Where ToArray ToString Replace ToLowerInvariant TryGetValue Single GetField Dependency Equals Exists ReadAllBytes Find Validate GetPatchInfo Hash PatchTargets Property Require Create TypeName Add Concat GetParameters GetName GetMethod GetType MakeGenericType GetMethodBody GetILAsByteArray GetProperty GetGetMethod GetIndexParameters ComputeHash StartsWith Select IsNullOrEmpty Join GetElementType GetGenericArguments GetGenericTypeDefinition IsSubclassOf'.split()),
    'IlGuard.cs': set('NormalizeBranch ToDouble ToInt32 ToInt64 ToSingle ToUInt16 Require Equals Read Slot Select ToDictionary GetValue ToList Add TryGetValue GetGenericArguments GetMethodBody GetILAsByteArray ResolveMember ResolveString GetFields Where'.split()),
    'GameAssemblyProvenance.cs': set('ToString Replace ToLowerInvariant Exists IsLowerHexSha256 Combine GetFullPath Create openRead ComputeHash IsNullOrWhiteSpace'.split()),
    'ContractData.cs': set(),
}

# Non-local writes are restricted to explicitly owned diagnostic fields/collections.
# No foreign object property/field setter is on this allowlist.
OWNED_WRITES = {
    'Observers.cs': set('Tracked[id] t.Selection t.NextFrame t.OnsetFrame t.Writes[callsite] sample.LastTick sample.Count sample.Emitted'.split()),
    'Plugin.cs': {'Application.logMessageReceivedThreaded', 'Observers.MainThread', 'Observers.Ready'},
    'Contracts.cs': {'spec.Method'},
    'IlGuard.cs': {'targets[i]'},
    'Probes.cs': set(), 'ArrayAnchor.cs': set(), 'GameAssemblyProvenance.cs': set(), 'ContractData.cs': set(),
}
MUTABLE_CALLS = {
    'Observers.cs': set('Tracked.Remove Tracked.TryGetValue lookup.Add lookup.ContainsKey lookup.TryGetValue manifest.Add mapped.Add names.Add parts.Add parts.Reverse pending.Pop pending.Push t.Writes.TryGetValue unmapped.Add'.split()),
    'Probes.cs': {'code.InsertRange'}, 'Contracts.cs': {'Writes.Add', 'Chainloader.PluginInfos.TryGetValue'},
    'IlGuard.cs': {'labels.Add', 'labels.TryGetValue', 'offsets.TryGetValue', 'result.Add'},
}
REF_ALLOWED = {'Active', 'Count', 'FirstUtc', 'LastUtc', 'FirstMono', 'LastMono', 'EmptyStacks', 'NonemptyStacks', 'TypeMask', 'field', 'ArrayAnchor.Active', 'ArrayAnchor.Count', 'faulted'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def walk(node, kind=None):
    if kind is None or node.type == kind:
        yield node
    for child in node.children:
        yield from walk(child, kind)


def text(node):
    return node.text.decode() if node else ''


def norm(value):
    return re.sub(r'\s+', '', value)


def method(tree, name):
    matches = [n for n in walk(tree, 'method_declaration') if text(n.child_by_field_name('name')) == name]
    require(len(matches) == 1, 'Missing/ambiguous source method ' + name)
    return matches[0]


def terminal(function):
    name = function.child_by_field_name('name')
    raw = text(name if name else function).split('.')[-1]
    return raw.split('<')[0].removeprefix('?')


def audit_sources(sources):
    require(set(sources) == FILES, 'Unexpected/missing C# source surface')
    trees = {}
    for filename, source in sources.items():
        tree = PARSER.parse(source.encode()).root_node
        require(not tree.has_error, 'C# syntax error: ' + filename)
        trees[filename] = tree
        for n in walk(tree):
            require(n.type not in {'unsafe_statement', 'pointer_type', 'goto_statement', 'yield_statement', 'function_pointer_type'}, 'Forbidden unsafe/control surface')
            if n.type == 'using_directive':
                require('=' not in text(n), 'Type aliases require separate safety review')
            if n.type == 'invocation_expression':
                fn = n.child_by_field_name('function')
                short = terminal(fn)
                require(short in CALLS[filename], 'Unreviewed invocation: ' + filename + ':' + text(fn))
                if short in {'Add', 'Remove', 'InsertRange', 'Reverse', 'Push', 'Pop', 'TryGetValue'}:
                    require(norm(text(fn)) in MUTABLE_CALLS.get(filename, set()), 'Foreign/ambiguous collection mutation')
                if short == 'GetComponentsInChildren':
                    require(norm(text(n)) == 't.Enemy.GetComponentsInChildren<SkinnedMeshRenderer>(true)', 'Unbounded/wrong subtree enumeration')
                if short == 'LogInfo':
                    require(filename == 'Plugin.cs' and norm(text(fn)) == 'self.Logger.LogInfo', 'Logging outside guarded sink')
            if n.type == 'assignment_expression':
                left = n.child_by_field_name('left')
                lhs = norm(text(left))
                if left.type != 'identifier':
                    require(lhs in OWNED_WRITES[filename], 'Foreign/ambiguous member assignment: ' + lhs)
            if n.type in {'prefix_unary_expression', 'postfix_unary_expression'} and ('++' in text(n) or '--' in text(n)):
                target = norm(text(n)).replace('++', '').replace('--', '')
                if '.' in target or '[' in target:
                    require(target in OWNED_WRITES[filename], 'Foreign increment/decrement')
            if n.type == 'argument' and text(n).lstrip().startswith('ref '):
                require(norm(text(n)[text(n).index('ref ') + 4:]) in REF_ALLOWED, 'Foreign ref argument')
            if n.type == 'object_creation_expression':
                created = text(n.child_by_field_name('type'))
                require(not re.search(r'(^|\.)(Random|Material|Mesh|GameObject|EnemyAI|SkinnedMeshRenderer)$', created), 'Foreign/RNG construction')
        # Auto-property setters on foreign objects cannot be hidden in object initializers
        # because foreign component/material/mesh construction is prohibited above.

    observers = trees['Observers.cs']
    for name in ('SelectorPrefix', 'Selected', 'SelectorPostfix', 'MeshPrefix', 'MeshPostfix', 'MaterialPrefix', 'MaterialPostfix', 'BeforeWrite', 'Tick'):
        m = method(observers, name)
        require(text(m.child_by_field_name('returns')) == 'void', 'Observer can suppress/replace return')
        body = m.child_by_field_name('body')
        catches = list(walk(body, 'catch_clause'))
        require(len(catches) == 1 and 'Plugin.Fault(' in text(catches[0]), 'Observer exception guard missing: ' + name)
        require('if (!Begin()' in text(body), 'Observer readiness/thread guard missing: ' + name)
    require('SELECTION_STATE_INCONCLUSIVE' in sources['Observers.cs'], 'Conservative selection state missing')
    for wrong in ('NO_NONDEFAULT_REPLACEMENT', 'NO_DUSK_DEFINITION', 'ALREADY_REPLACED', '"DEFAULT"'):
        require(wrong not in sources['Observers.cs'], 'Unproven outcome classification: ' + wrong)
    require('renderer.materials' not in sources['Observers.cs'] and 'r.materials' not in sources['Observers.cs'], 'Instantiating material getter forbidden')
    for name in ('Capture', 'Min', 'Max'):
        body = method(trees['ArrayAnchor.cs'], name)
        for call in walk(body, 'invocation_expression'):
            require(norm(text(call.child_by_field_name('function'))) in {'Volatile.Read', 'Stopwatch.GetTimestamp', 'Min', 'Max', 'string.IsNullOrEmpty', 'Interlocked.Increment', 'Interlocked.CompareExchange', 'Interlocked.Read'}, 'Non-atomic callback call')
        require(not list(walk(body, 'object_creation_expression')), 'Allocation in log callback')
    capture = norm(text(method(trees['ArrayAnchor.cs'], 'Capture')))
    require('condition!=Signature' in capture and 'UnityEngine.Object' not in capture and not re.search(r'(?<![A-Za-z])Time\.', capture), 'Log filter/Unity callback violation')
    plugin = sources['Plugin.cs']
    require(plugin.count('harmony.Patch(') == 4 and 'harmony?.UnpatchSelf()' in plugin, 'Explicit patch topology/rollback drift')
    for anchor in ('harmony.Patch(target, transpiler:', 'harmony.Patch(Contracts.MeshTransfer,', 'harmony.Patch(Contracts.Materials,', 'harmony.Patch(Contracts.Selector,'):
        require(anchor in plugin, 'Patch target drift')
    require('Application.logMessageReceivedThreaded += ArrayAnchor.Capture' in plugin and 'Application.logMessageReceivedThreaded -= ArrayAnchor.Capture' in plugin, 'Log subscription lifetime drift')
    require('REFUSED TO ARM; normal behavior preserved' in plugin and 'INCONCLUSIVE' in plugin, 'Failure markers missing')
    require('BindingFlags.DeclaredOnly' in sources['Contracts.cs'], 'Declared-only resolution missing')
    require('Hash(m.GetMethodBody().GetILAsByteArray()) == spec.IlHash' in sources['Contracts.cs'], 'Exact body gate missing')
    require('prior.Transpilers.Count == 0' in sources['Contracts.cs'], 'Ambiguous foreign transpiler guard missing')
    for anchor in ('expected.Count == actual.Count', 'a.opcode == NormalizeBranch(e.Code)', 'offsets.TryGetValue', 'Contracts.Require(equal,'):
        require(anchor in sources['IlGuard.cs'], 'Full incoming-IL comparison missing')
    branch_adapter = text(method(trees['IlGuard.cs'], 'NormalizeBranch'))
    pairs = re.findall(r'if \(code == OpCodes\.(\w+)\) return OpCodes\.(\w+);', branch_adapter)
    expected_pairs = [(name + '_S', name) for name in ('Beq', 'Bge', 'Bge_Un', 'Bgt', 'Bgt_Un', 'Ble', 'Ble_Un', 'Blt', 'Blt_Un', 'Bne_Un', 'Brfalse', 'Brtrue', 'Br', 'Leave')]
    require(pairs == expected_pairs, 'HarmonyX branch encoding adapter drift')
    return trees


def injection_recipe(tree, name):
    m = method(tree, name)
    body = m.child_by_field_name('body')
    # Insertion is the only permitted instruction-list write; no original operands,
    # labels, blocks or original calls can be changed by this source surface.
    calls = [norm(text(n)) for n in walk(body, 'invocation_expression') if terminal(n.child_by_field_name('function')) == 'InsertRange']
    require(calls == ['code.InsertRange(at,insert)'], 'Transpiler must insert exactly once')
    returns = [norm(text(n)) for n in walk(body, 'return_statement')]
    require(returns == ['returncode;'], 'Transpiler must return original list plus insertion')
    require(not list(walk(body, 'assignment_expression')), 'Transpiler contains instruction/state assignment')
    require('IlGuard.Check(instructions, original)' in text(body), 'Incoming contract validation missing')
    require('int at = sites[0].i;' in text(body) and 'sites.Length == 1' in text(body), 'Unique exact insertion site required')
    require('EmptyBoundary(code[at])' in text(body), 'Label/EH guard missing')
    recipe = []
    for n in walk(body, 'object_creation_expression'):
        if text(n.child_by_field_name('type')) != 'CodeInstruction':
            continue
        args = n.child_by_field_name('arguments').named_children
        values = [norm(text(a)) for a in args]
        require(values and values[0].startswith('OpCodes.'), 'Nonconstant inserted opcode')
        recipe.append((values[0].split('.')[1], values[1] if len(values) > 1 else None))
    types = {'typeof(bool)': 'bool', 'typeof(float)': 'float', 'typeof(int)': 'int', 'typeof(EnemyAI)': 'enemy', 'typeof(SkinnedMeshRenderer)': 'renderer', 'Contracts.ApplyOperand.DeclaringType': 'definition'}
    locals_ = {}
    for local, type_expression in re.findall(r'LocalBuilder\s+(\w+)\s*=\s*generator\.DeclareLocal\(([^;]+)\);', text(body)):
        require(norm(type_expression) in types and local not in locals_, 'Unproven or duplicate scratch local type')
        locals_[local] = types[norm(type_expression)]
    require(len(locals_) == 3, 'Exactly three typed scratch locals expected')
    return recipe, locals_


def prove_stack(injection, kind):
    recipe, local_types = injection
    initial = [('opaque-below', 'opaque')]
    if kind == 'Selector':
        initial += [('coroutine-receiver', 'object'), ('selected-original', 'definition'), ('self-original', 'enemy'), ('false-original', 'bool')]
        callback = 'Callback(nameof(Observers.Selected))'
        expected_args = [('selected-original', 'definition'), ('self-original', 'enemy')]
    else:
        initial += [('renderer-original', 'renderer'), ('index-original', 'int'), ('weight-original', 'float')]
        callback = 'Callback(nameof(Observers.BeforeWrite))'
        expected_args = [('this-original', 'enemy'), *initial[-3:], ('original-callsite', 'string')]
    stack = initial.copy(); locals_ = {}; observations = 0
    for op, arg in recipe:
        if op == 'Stloc':
            require(stack and stack[-1][1] != 'opaque', 'Injection underflows original stack')
            require(arg in local_types and local_types[arg] == stack[-1][1], 'Invalid scratch local type')
            locals_[arg] = stack.pop()
        elif op == 'Ldloc':
            require(arg in locals_, 'Injection reads uninitialized local')
            stack.append(locals_[arg])
        elif op == 'Ldarg_0':
            require(kind != 'Selector', 'Selector must observe self argument, not orig delegate')
            stack.append(('this-original', 'enemy'))
        elif op == 'Ldstr':
            require(arg == 'original.Name', 'Wrong write callsite label')
            stack.append(('original-callsite', 'string'))
        elif op == 'Call':
            require(arg == callback, 'Injection calls non-observer code')
            require(stack[-len(expected_args):] == expected_args, 'Observer received altered/wrong operands')
            del stack[-len(expected_args):]
            observations += 1
        else:
            raise ValueError('Non-observational injected opcode: ' + op)
    require(observations == 1 and stack == initial, 'Original stack/operands not restored exactly')


def evidence_contract(data):
    methods = {(m['owner'], m['name']): m for a in data['assemblies'] for m in a['methods']}
    owner = 'CodeRebirth.src.Content.Enemies.Janitor'
    expected = {'SetBlendShapeWeightClientRpc': ('public', ['System.Int32'], None), 'KillEnemy': ('public', ['System.Boolean'], 0.0), 'KeepPlayerAttachedDuringZoom': ('private', [], 0.0), 'SwitchToChaseState': ('private', ['GameNetcodeStuff.PlayerControllerB'], 100.0)}
    for name, (access, args, weight) in expected.items():
        m = methods[owner, name]
        require(m['access'] == access and not m['static'] and m['parameter_types'] == args and m['return_type'] == 'System.Void', 'Exact Janitor signature drift')
        il = m['il']
        writes = [i for i, x in enumerate(il) if x['opcode'] in ('call', 'callvirt') and isinstance(x['operand'], dict) and x['operand'].get('name') == 'SetBlendShapeWeight']
        require(len(writes) == 1, 'Expected exactly one direct write per Janitor target')
        i = writes[0]
        require(il[i]['operand']['owner'] == 'UnityEngine.SkinnedMeshRenderer' and il[i]['operand']['parameter_types'] == ['System.Int32', 'System.Single'], 'Wrong Unity write operand')
        z = i - (3 if weight is None else 2)
        require([x['opcode'] for x in il[z-4:z+1]] == ['ldarg.0', 'ldfld', 'ldc.i4.0', 'ldelem.ref', 'ldc.i4.0'], 'Index-zero renderer producer drift')
        require(il[z-3]['operand']['owner'] == 'EnemyAI' and il[z-3]['operand']['name'] == 'skinnedMeshRenderers', 'Wrong renderer field')
        if weight is None:
            require([x['opcode'] for x in il[i-2:i]] == ['ldarg.1', 'conv.r4'], 'RPC conversion drift')
        else:
            require(il[i-1]['opcode'] == 'ldc.r4' and il[i-1]['operand'] == weight, 'Reset/chase value drift')
        empty_boundary(m, il[i]['offset'])
    kill = methods[owner, 'KillEnemy']
    require(kill['virtual'] and kill['parameters'][0]['optional'], 'KillEnemy override/optional contract missing')
    selector = methods['Dusk.Internal.EntityReplacementRegistrationPatch', 'ReplaceEnemyEntity']
    require(selector['static'] and selector['access'] == 'private' and selector['parameter_types'] == ['On.EnemyAI+orig_Start', 'EnemyAI'], 'Selector signature drift')
    il = selector['il']
    applies = [i for i, x in enumerate(il) if isinstance(x['operand'], dict) and x['operand'].get('name') == 'Apply']
    require(len(applies) == 1, 'Selector Apply callsite not unique')
    i = applies[0]; operand = il[i]['operand']
    require(operand['owner'] == 'Dusk.DuskEntityReplacementDefinition`1<EnemyAI>' and operand['parameter_types'] == ['!0', 'System.Boolean'], 'Optional generic Apply contract drift')
    require([x['opcode'] for x in il[i-3:i+2]] == ['ldloc.s', 'ldarg.1', 'ldc.i4.0', 'callvirt', 'callvirt'], 'Selector stack producer drift')
    require(il[i-3]['operand'] == {'slot': 11} and selector['locals'][11] == 'Dusk.DuskEnemyReplacementDefinition', 'Selected local drift')
    require(il[i+1]['operand']['owner'] == 'UnityEngine.MonoBehaviour' and il[i+1]['operand']['name'] == 'StartCoroutine', 'Coroutine adjacency drift')
    empty_boundary(selector, il[i]['offset'])
    for owner, name, access, static, args in [
        ('Dusk.SkinnedMeshReplacement', 'ReplaceSkinnedMeshRenderer', 'private', False, ['UnityEngine.SkinnedMeshRenderer']),
        ('Dusk.MaterialsReplacement', 'CopyOrResizeMaterials', 'assembly', True, ['UnityEngine.Renderer', 'UnityEngine.Material[]', 'System.Int32']),
    ]:
        m = methods[owner, name]
        require(m['access'] == access and m['static'] == static and m['parameter_types'] == args and m['return_type'] == 'System.Void', 'Dusk helper contract drift')
    for m in methods.values():
        require(hashlib.sha256(bytes.fromhex(m['il_bytes_hex'])).hexdigest() == m['il_sha256'], 'IL byte hash mismatch')
    return methods


def empty_boundary(method_, offset):
    targets = []
    for x in method_['il']:
        if x['opcode'].startswith(('br', 'beq', 'bge', 'bgt', 'ble', 'blt', 'bne', 'leave')):
            targets.append(x['operand'])
        if x['opcode'] == 'switch':
            targets.extend(x['operand'])
    for eh in method_['exception_handlers']:
        targets.extend(eh[k] for k in ('try_start', 'try_end', 'handler_start', 'handler_end', 'filter_start'))
    require(offset not in targets, 'Injection call is a branch/exception boundary')


def rejects(action, name):
    try:
        action()
    except (ValueError, KeyError):
        return name
    raise ValueError('Negative case unexpectedly passed: ' + name)


def negative_cases(sources, data, recipes):
    cases = []
    mutations = [
        ('mesh-mutation', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; enemy.sharedMesh = null;'),
        ('material-mutation', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; renderer.sharedMaterials = null;'),
        ('bone-mutation', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; renderer.bones = null;'),
        ('blendshape-write', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; renderer.SetBlendShapeWeight(0, 0f);'),
        ('network-mutation', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; enemy.NetworkObject.Despawn();'),
        ('global-scan', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; UnityEngine.Object.FindObjectsOfType<EnemyAI>();'),
        ('rng-replay', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; new System.Random().Next();'),
        ('candidate-list-mutation', 'Observers.cs', 'if (!Begin()) return;', 'if (!Begin()) return; replacements.RemoveAt(0);'),
        ('callback-log', 'ArrayAnchor.cs', 'long utc = DateTime.UtcNow.Ticks;', 'Plugin.Marker("bad", "bad"); long utc = DateTime.UtcNow.Ticks;'),
        ('callback-Unity-API', 'ArrayAnchor.cs', 'long utc = DateTime.UtcNow.Ticks;', 'UnityEngine.Object.FindObjectsOfType<EnemyAI>(); long utc = DateTime.UtcNow.Ticks;'),
        ('fabricated-default', 'Observers.cs', 'SELECTION_STATE_INCONCLUSIVE', 'NO_NONDEFAULT_REPLACEMENT'),
        ('broad-patch', 'Plugin.cs', 'Contracts.Resolve();', 'Contracts.Resolve(); harmony.PatchAll();'),
        ('observer-return-suppression', 'Observers.cs', 'void SelectorPrefix', 'bool SelectorPrefix'),
        ('original-operand-rewrite', 'Probes.cs', 'code.InsertRange(at, insert);', 'code[at].operand = null; code.InsertRange(at, insert);'),
    ]
    for name, file, old, new in mutations:
        changed = sources.copy(); require(old in changed[file], 'Bad negative fixture')
        changed[file] = changed[file].replace(old, new, 1)
        cases.append(rejects(lambda: audit_sources(changed), name))
    for kind, (recipe, local_types) in recipes.items():
        cases.append(rejects(lambda: prove_stack((recipe[:-1], local_types), kind), kind + '-missing-restore'))
        modified = list(recipe); call = next(i for i, x in enumerate(modified) if x[0] == 'Call'); modified[call] = ('Call', 'foreign-mutation')
        cases.append(rejects(lambda: prove_stack((modified, local_types), kind), kind + '-foreign-call'))
        bad_types = {name: 'wrong-type' for name in local_types}
        cases.append(rejects(lambda: prove_stack((recipe, bad_types), kind), kind + '-wrong-local-type'))
    duplicate = copy.deepcopy(data)
    janitor = duplicate['assemblies'][0]['methods'][0]
    janitor['il'].append(next(copy.deepcopy(x) for x in janitor['il'] if isinstance(x['operand'], dict) and x['operand'].get('name') == 'SetBlendShapeWeight'))
    cases.append(rejects(lambda: evidence_contract(duplicate), 'duplicate-direct-write'))
    wrong = copy.deepcopy(data)
    next(m for m in wrong['assemblies'][0]['methods'] if m['name'] == 'KillEnemy')['parameter_types'] = []
    cases.append(rejects(lambda: evidence_contract(wrong), 'guessed-KillEnemy-signature'))
    changed = copy.deepcopy(data)
    sel = next(m for a in changed['assemblies'] for m in a['methods'] if m['name'] == 'ReplaceEnemyEntity')
    i = next(i for i, x in enumerate(sel['il']) if isinstance(x['operand'], dict) and x['operand'].get('name') == 'Apply')
    sel['il'][i-1]['opcode'] = 'ldc.i4.1'
    cases.append(rejects(lambda: evidence_contract(changed), 'changed-immediate-argument'))
    boundary = copy.deepcopy(data)
    write = boundary['assemblies'][0]['methods'][0]
    target = next(x['offset'] for x in write['il'] if isinstance(x['operand'], dict) and x['operand'].get('name') == 'SetBlendShapeWeight')
    write['il'].append({'offset': 999999, 'opcode': 'br', 'operand': target})
    cases.append(rejects(lambda: evidence_contract(boundary), 'branch-into-injection-call'))
    return cases


def main(self_test):
    actual = {p.name for p in PATCH.iterdir()}
    require(actual == FILES | {'README.md', 'NuGet.Config', 'S142AKBMAFR1I1.csproj'}, 'Unexpected project file/output')
    sources = {name: (PATCH / name).read_text() for name in FILES}
    trees = audit_sources(sources)
    require(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() == EVIDENCE_SHA256, 'Pinned evidence bytes changed; provenance re-review required')
    data = json.loads(EVIDENCE.read_text())
    methods = evidence_contract(data)
    recipes = {name: injection_recipe(trees['Probes.cs'], name) for name in ('Selector', 'JanitorWrite')}
    for name, recipe in recipes.items():
        prove_stack(recipe, name)
    module_spec = importlib.util.spec_from_file_location('contract_generator', ROOT / 'AnalysisTools/generate_s142ak_bmafr1i1_contract_data.py')
    generator = importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(generator)
    require(sources['ContractData.cs'] == generator.render(data), 'Generated reflection/IL contracts drift')
    project = ET.parse(PATCH / 'S142AKBMAFR1I1.csproj').getroot()
    require(project.findtext('PropertyGroup/AssemblyName') == 'S142AKBMAFR1I1', 'Assembly identity mismatch')
    require({p.attrib['Include']: p.attrib['Version'] for p in project.findall('ItemGroup/PackageReference')} == {'BepInEx.Core': '5.4.21', 'HarmonyX': '2.10.2', 'LethalCompany.GameLibs.Steam': '81.0.5-ngd.0'}, 'Unexpected project dependencies')
    state = json.loads((ROOT / 'Current/CURRENT_STATE.json').read_text())
    build = json.loads((ROOT / 'BuildSpecs/current.json').read_text())
    require(build['enabled'] is False and build['build_id'] == 'IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS', 'Build controller changed')
    require((ROOT / 'RuntimeInbox/ACTIVE_BUILD.txt').read_text().strip() == 'S1.42AK-BMDSFIX1', 'Runtime controller changed')
    require(state['accepted_baseline']['build_id'] == 'S1.42AK' and state['active_candidate']['build_id'] == 'S1.42AK-BMDSFIX1' and state['runtime_test_outstanding'], 'Lifecycle boundary changed')
    workflow = (ROOT / '.github/workflows/s142ak-bmafr1i1-source-static.yml').read_text()
    require('python AnalysisTools/validate_s142ak_bmafr1i1_source.py --self-test' in workflow and '--only-binary=:all:' in workflow, 'Static CI missing')
    for forbidden in ('dotnet', 'msbuild', 'build_profile', 'workflow_dispatch', 'contents: write', 'upload-artifact'):
        require(forbidden not in workflow, 'CI exceeds static scope: ' + forbidden)
    workflow_data = yaml.safe_load(workflow)
    runs = [step['run'] for step in workflow_data['jobs']['validate']['steps'] if 'run' in step]
    require(runs == [
        'python -m pip install --only-binary=:all: tree-sitter==0.25.2 tree-sitter-c-sharp==0.23.1 PyYAML==6.0.2',
        'python AnalysisTools/generate_s142ak_bmafr1i1_contract_data.py --check',
        'python AnalysisTools/validate_s142ak_bmafr1i1_source.py --self-test'], 'Unreviewed static workflow command')
    cases = negative_cases(sources, data, recipes) if self_test else []
    print(json.dumps({'status': 'PASS_SOURCE_STATIC_CHECKS_ONLY', 'methods': len(methods), 'patch_targets': 7, 'stack_proofs': list(recipes), 'negative_cases': cases, 'compile': 'NOT_RUN_NOT_AUTHORIZED', 'runtime': 'NOT_RUN_NOT_AUTHORIZED'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    main(parser.parse_args().self_test)
