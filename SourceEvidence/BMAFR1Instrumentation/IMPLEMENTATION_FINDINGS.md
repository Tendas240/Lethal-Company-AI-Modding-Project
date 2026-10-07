# S1.42AK-BMAFR1I1 source/static implementation checkpoint

Date: 2026-10-03.
Status: IMPLEMENTED ON REVIEW BRANCH / SOURCE-STATIC INTEGRATION OUTSTANDING.
Classification: DIAGNOSTIC ONLY / NEVER ACCEPT.
Main authority: Current/230_S1.42AK_BMAFR1_INSTRUMENTATION_SOURCE_STATIC_AUTHORIZATION_DECISION.md.
Preparation parent: 39aca988578fdda900c1360fe197811611448a98.
Main analysis base: 7c1df95d3698b2b7e98b820c90370e89ace9970e.

## Implemented unit

Patches/S142AKBMAFR1I1 contains the separate diagnostic source/project, exact
dependency and declared method resolution, generated IL/local/EH contracts,
complete incoming IL comparison, stack-preserving observational transpilers,
bounded Janitor/SpringMan snapshots, correlated Dusk helper observers and atomic
Unity log-callback correlation. BuildSpecs/S1.42AK-BMAFR1I1_PLAN.md records the
patch-safety review and preserved adjacent native responsibilities.

The seven targets are the selector, Dusk mesh/material helpers and four Janitor
methods authorized by Current/230. The selector reads the already chosen current
and self before the exact generic Apply call, preserving its immediate=false
argument and the original coroutine receiver/calls. No Apply method is patched.
No unobserved default/no-definition/existing-replacement outcome is invented.

MethodContract also validates locals, MaxStack, InitLocals and the exact finally
regions. The preparation inspector was extended to preserve raw IL byte hashes,
InitLocals and exact nested TypeDef names; nested closure types now retain their
declaring owner. The input package/DLL hashes are unchanged.

## Concrete HarmonyX source finding

Pinned HarmonyX v2.10.2 source was inspected at:
https://github.com/BepInEx/HarmonyX/blob/v2.10.2/Harmony/Internal/Patching/ILManipulator.cs

ApplyTranspilers invokes NormalizeInstructions before each transpiler. Its exact
14-entry short-to-long branch map must be reflected in the incoming IL comparison;
otherwise a raw opcode comparison would refuse the known method bodies merely
because Harmony normalizes branch encoding. IlGuard.NormalizeBranch implements
that exact map, while all original branch destinations remain checked. This does
not allow semantic branch changes or fuzzy opcode fallback.

The same source resolves transpiler arguments by parameter type (ILGenerator,
MethodBase, IEnumerable<CodeInstruction>) and provides typed LocalBuilder operands.
These source facts do not substitute for a later compiler/loader test.

## Static verification performed

- C# syntax parsed without compiling.
- Generated ContractData compared with exact evidence.
- Thirteen exact dependency method contracts checked, including the seven targets.
- Each Janitor target has exactly one direct Unity index-zero write with the exact
  renderer and value producer. KillEnemy(bool destroy=false) is declared/virtual;
  no fallback overload is used.
- The selector's non-default Apply call is unique and preserves its generic owner,
  selected local, self, optional bool and adjacent StartCoroutine call.
- Injection sites are not original branch/exception boundaries.
- Actual C# insertion recipes are parsed and symbolically executed to verify
  typed local storage, exact observer arguments and exact restoration of all
  existing stack values, including any values below the instrumentation surface.
- Syntax-tree checks restrict foreign member writes, ref arguments, method calls,
  collection mutations, Unity scans, callback operations and patch topology.
- Negative cases exercise mesh/material/bone/blendshape/network mutation, global
  scans, RNG replay, candidate mutation, callback logging/Unity access, fabricated
  default state, broad patching, return suppression, original-operand rewriting,
  missing restores, wrong local types, foreign calls, duplicate writes, guessed
  KillEnemy signatures, changed optional arguments and branch entry at injection.
- Static workflow commands are restricted to pinned binary parser installation,
  generated-constant verification and the source/static validator with self-tests.

Exact evidence file SHA-256:
f873eecd4a2d03b2e45afbc73686ae8d189014159895e96fa27800969df0eae2.

## Qualifications and next gate

The validator is a bounded source-contract/regression gate, not a C# type checker,
compiler, JIT/Harmony execution proof, general security verifier, runtime pass or
acceptance decision. All project source remains uncompiled, as required.

Write hooks count every invocation but emit bounded samples (first eight per
instance/callsite, then at most one full record per second). Selection identity
uses the observed asset/skin name, type and Unity ID; the stable namespace key is
explicitly NOT_READ. This satisfies name-based selection observation and does not
claim a reconstructed key. Timestamp extrema are independently atomic fields.
Observers preserve originals even if capture fails; capture failure is globally
INCONCLUSIVE. No root cause or native emitter ownership is established.

The next bounded task is exact PR-head source review and relevant CI verification,
followed by integration/lifecycle reconciliation only when those gates justify it.
Do not treat this branch checkpoint or green source CI as main integration or
inactive-review-build authorization. A later CURRENT_STATE transition must include
renderer-generated navigation and a permanent exact-main-head Knowledge
Architecture push gate. No canonical live-state transition has been made here.

This is execution segment 2 of the originating chat. That chat must not start a
third execution segment; continuation belongs to a freshly bootstrapped chat.

## Preserved boundaries

No diagnostic DLL/profile was built or published; no profile/package/config bytes
were changed; no Gale import, controller activation or runtime run occurred.
BuildSpecs/current.json stays disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS;
RuntimeInbox/ACTIVE_BUILD.txt stays S1.42AK-BMDSFIX1. S1.42AK remains accepted,
BMDSFIX1 remains not accepted with its passive unwaived outstanding DeepSewersFlow
gate and no dedicated reroll, and BMAFR1 remains inactive/DIAGNOSTIC ONLY/NEVER
ACCEPT with its bounded pair PASS preserved. BMAFDIAG1/PATH1 stay DO NOT RERUN.

Princess selection in the prior run, a live zero-blendshape Janitor mesh, exact
array emitter, native Unity ownership and root cause remain unproven. SpringMan
remains a contemporaneous alternative with equal snapshot scope.
