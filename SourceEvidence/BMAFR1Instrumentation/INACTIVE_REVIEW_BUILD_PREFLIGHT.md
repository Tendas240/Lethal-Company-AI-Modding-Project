# BMAFR1I1 inactive review-build preflight

Date: 2026-10-03.
Status: PREFLIGHT COMPLETE / BUILD INFRASTRUCTURE AND BUILD OUTSTANDING.
Authority: Current/232_S1.42AK_BMAFR1I1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md.
Classification: DIAGNOSTIC ONLY / NEVER ACCEPT.
This is a working-branch preparation record, not a completed review-build checkpoint or canonical lifecycle transition.

## Fresh repository verification

The mandatory policy, CURRENT_STATE and topic router were read from main in that order.
Verified main: cc26952be87ab2ff3e441a208a3357da66e3a89b.
Permanent Knowledge Architecture run 37139094183 / #986 / push:
head_sha exactly cc26952be87ab2ff3e441a208a3357da66e3a89b, completed/success.
No open pull requests were returned before this working branch was created.

BuildSpecs/current.json remains disabled at IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS.
RuntimeInbox/ACTIVE_BUILD.txt and Current/AUTO_BUILD_RESULT.json remain S1.42AK-BMDSFIX1.
S1.42AK accepted; BMDSFIX1 active/not accepted; its DeepSewersFlow gate passive,
outstanding and unwaived. BMAFR1 inactive/diagnostic only with its bounded pair PASS.
No new runtime run or qualification rerun is authorized.

## Exact source input lock

The following Git blob IDs were read at the verified main commit. The build must
compare the entire patch directory and preserve these source/project bytes.
No compile failure may be silently repaired by broadening or rewriting the reviewed
observational source in this checkpoint.

| File | Git blob SHA-1 |
|---|---|
| `ArrayAnchor.cs` | `14a3d32bf3200e11f53b269f0e70693e7af3b4e3` |
| `ContractData.cs` | `e983610c4158be0f813db8c61fd42d259e619ff9` |
| `Contracts.cs` | `a4f26c838d9f118e8505dc1ab5110f3a15bc73d6` |
| `GameAssemblyProvenance.cs` | `eb0ea20f1556171bdb0d9fc27401c59d675b2432` |
| `IlGuard.cs` | `556dd5d8140cd43ad7e1359f13590aa5bffc2e59` |
| `NuGet.Config` | `a7d4e5a8ecc5cbfb2fa226791995a580a21500b8` |
| `Observers.cs` | `a1bb652f6adb8891523b1bfc534a5c009e5cc1bb` |
| `Plugin.cs` | `44631784a21aa036a8a8b6758c04e4a98c47836a` |
| `Probes.cs` | `4e77884c712c158830c288a1ec077a73b022f958` |
| `README.md` | `77a553aaad8a4f2eeb8032fb482d290a88bc2366` |
| `S142AKBMAFR1I1.csproj` | `4af83fc0e84a13087637ca231ccc1c370200639e` |

Project contracts: netstandard2.1; assembly S142AKBMAFR1I1; BepInEx.Core 5.4.21;
HarmonyX 2.10.2; LethalCompany.GameLibs.Steam 81.0.5-ngd.0.
Exact dependency evidence SHA-256:
f873eecd4a2d03b2e45afbc73686ae8d189014159895e96fa27800969df0eae2.

## Parent and intended output

Parent: Profiles/LC V1 S1.42AK-BMAFR1.r2z.
SHA-256: 8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5.
Canonical PROFILE_INDEX_RESULT and EXPECTED_HASHES agree; parent has 337 members.
The parent binary must still be independently hashed by the build before use.

Proposed short profile identity: LC V1 S1.42AK-BMAFR1I1.
Proposed output: Profiles/LC V1 S1.42AK-BMAFR1I1.r2z, ephemeral Actions artifact only.
New member: BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll.
Expected member count: 338; removed members: zero.
Only existing changed member: export.r2x, exact profileName replacement only.
Every other member must remain byte-identical, including all configs, existing
BMAF diagnostic DLL and accepted normalizer. Package/export content outside the
profile identity must remain byte-identical.

The unchanged repository Gale path guard was executed locally from the verified
main bytes against this proposed identity, with its self-test: PASS, maximum
projected path 221/255. This is an identity preflight, not proof of a built profile.

## Implementation constraints discovered

There is no BMAFR1I1 review-build workflow or JSON recipe on main.
The source-static workflow must remain source-static: its validator explicitly
rejects compilation, artifact upload or extra commands in that workflow.

The source validator requires the exact eleven-file patch directory and rejects
additional bin/obj directories. Run it before compilation; direct compiler outputs
and intermediates outside the source directory if it is rerun afterward.

BuildSystem/profile_builder.py unconditionally generates a ProfileSources snapshot
and FILE_INDEX, and defaults result output to Current/AUTO_BUILD_RESULT.
The explicit user boundary forbids profile indexing and controller/result changes.
Use a narrow build-specific review path, reusing safe ZIP primitives if useful,
without calling generic main/snapshot, canonical indexing, publishing or modifying
the generic builder. Do not rerun historical BMAF review workflows.

## Next bounded execution unit

Implement one isolated, read-only-permission Actions review workflow and minimal
build/validation helpers on this branch. Check out the exact PR head, prove the
source lock and controllers, run the existing source/static gate and generated-data
check, compile the unchanged project, inspect the resulting PE assembly identity
and record dependency/compiler evidence, construct the exact minimal archive and
verify it independently, run the permanent path guard, and upload the inactive
profile plus compact evidence with a fixed artifact identity.

After the run, download the frozen Actions ZIP independently and hash its actual
bytes, compare its digest with Actions, rehash the contained profile/DLL and
recheck the archive delta. Record exact run/head/artifact IDs and hashes before
a later lifecycle relies on them. A failed compile or contract check remains a
failed/incomplete review, not authority to mutate the source or widen scope.

Integration and canonical lifecycle reconciliation must remain a later bounded
unit if needed; do not combine publication/indexing/activation/runtime with review.
This originating GPT-6 chat has consumed execution segment 1 of its maximum 2.
After segment 2 it must stop and return control through handover/reassessment.

## Evidence limits

No DLL/profile was compiled or constructed in this preflight. No artifact hashes
or completed build PASS are claimed. Princess selection, live zero-blendshape
Janitor state, exact array emitter, native Unity ownership and root cause remain
unproven. SpringMan remains an equal-scope contemporaneous alternative.
