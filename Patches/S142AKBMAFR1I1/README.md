# S1.42AK-BMAFR1I1 observational source

Status: SOURCE IMPLEMENTATION FOR REVIEW / NOT BUILT / NOT RUNTIME AUTHORIZED.
Classification: DIAGNOSTIC ONLY / NEVER ACCEPT.

Authority: Current/230_S1.42AK_BMAFR1_INSTRUMENTATION_SOURCE_STATIC_AUTHORIZATION_DECISION.md.
Plan: BuildSpecs/S1.42AK-BMAFR1I1_PLAN.md.
Exact dependency evidence: SourceEvidence/BMAFR1Instrumentation/EXACT_DEPENDENCY_CONTRACTS.json.

The plugin observes seven exact foreign method targets: the Dusk selector,
skinned-mesh transfer and material helper, and four Janitor direct blendshape
writes. It does not select an enemy/interior, execute an RPC, replace an Apply
method, patch Unity's global blendshape setter, or change any foreign state.

Contracts.cs validates exact dependency GUID/version/assembly/file SHA-256,
declared method signatures/access/return types and IL byte hashes before arming.
ContractData.cs is generated from the hash-verified package metadata evidence.
Physical installed game provenance is separate from loaded game type identity;
no loaded Assembly-CSharp path, module-name, ScopeName or MVID equality is added.

IlGuard.cs compares every incoming Harmony opcode and operand against the exact
original method body, including branch destinations. Existing foreign transpilers
cause refusal. Probes.cs inserts only an observer call and local stack
spill/restore; existing instructions, operands, labels and exception blocks are
left intact. An injection point with a label or exception-block boundary refuses.
The original Dusk coroutine receiver and optional immediate=false argument survive.
The incoming comparison explicitly accounts for HarmonyX 2.10.2's documented
pre-transpiler short-to-long branch normalization; destinations remain exact.

Observers are void and exception-guarded. An observer error disables observation
globally and marks INCONCLUSIVE, while the original foreign method/call continues.
Arming failure calls UnpatchSelf and reports REFUSED TO ARM; normal behavior
preserved. A failed log sink disables observation as well. No diagnostic code
catches, skips, clamps or substitutes the original gameplay write.

Selection absence is always SELECTION_STATE_INCONCLUSIVE in this first version.
No default, missing-definition or already-replaced classification is inferred.
The selected asset ID/name, concrete type, validated SkinName, IsDefault and exact
Hierarchy action manifest are recorded. Stable namespace keys are explicitly
NOT_READ; skin/asset identity is the authorized name-based identity, not an invented
key or Princess-selection conclusion.

Only exact tracked Janitor and SpringMan roots receive full renderer snapshots,
after selector completion, on the next frame and on the next frame after the first
observed array onset. Other selected Dusk enemies receive lightweight identities
and action manifests. Mesh transfer observers collect pre/replacement/post state
only for peers; material observers filter to already correlated enemy roots.
Reads use sharedMesh/sharedMaterials; instantiating material getters are excluded.

Bounds: 16 peer and 32 other tracked roots, 16 renderers per peer snapshot, 256
bones per renderer, 128 blendshape names, 32 actions, 512 transforms in a tracked
bone-root traversal, 64 hierarchy levels, 1024 characters per captured name/path,
32768 characters per marker, and 2048 markers per process. Bounds produce
INCONCLUSIVE, never a silently truncated complete result. Dusk's bone-name rule
uses first depth-first exact-name matches with original-root fallback.

Every Janitor direct-write callback is reached and counted. It logs the first
eight calls per instance/callsite, then at most one full sample per second, with
cumulative invocation and emitted-sample counts. This is sampled evidence;
unlogged intermediate mesh/weight changes must not be inferred absent.
Array summaries are at most once per five seconds, plus onset and teardown.

ArrayAnchor.Capture is the threaded Unity callback. It filters only the exact
array signature and uses BCL timestamps and atomic fields. It invokes no Unity
object APIs and emits no log. Timestamp fields are independent atomic extrema,
not a transactionally paired event record; monotonic time is primary. The supplied
LogType bitmask and empty/nonempty stack counts are retained. None identifies the
native emitter or proves the error's root cause.

Static validation (with the pinned Python binary parser packages installed):

```
python AnalysisTools/generate_s142ak_bmafr1i1_contract_data.py --check
python AnalysisTools/validate_s142ak_bmafr1i1_source.py --self-test
```

These checks parse source, enforce a closed audited call/write surface, inspect
exact dependency contracts and symbolically prove the inserted stack recipes.
They are not a C# compiler/type checker, JIT test, Harmony execution test, proof
against arbitrary coordinated validator/source changes, or a runtime PASS.
Compiler and live-loader validity remain unproven until a later separately
authorized build; this checkpoint must compile nothing.
