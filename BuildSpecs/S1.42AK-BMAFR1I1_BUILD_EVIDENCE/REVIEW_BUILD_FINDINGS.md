# BMAFR1I1 inactive compile/archive review checkpoint

Date: 2026-10-03.
Status: PASS ON REVIEW BRANCH / INDEPENDENT FROZEN-ARTIFACT REHASH PASS.
Main integration and canonical lifecycle reconciliation: OUTSTANDING.
Authority: Current/232_S1.42AK_BMAFR1I1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md.
Classification: DIAGNOSTIC ONLY / NEVER ACCEPT.

## Result and provenance

The exact eleven-file Patches/S142AKBMAFR1I1 directory from main
cc26952be87ab2ff3e441a208a3357da66e3a89b compiled with zero warnings and zero errors.
No source, project, existing validator, dependency-contract evidence or live controller
was modified. Twenty-four frozen input files were compared by Git blob identity and
SHA-256 before and after the build. The source/static gate passed before and after
compilation: 13 exact method contracts, seven patch targets, selector/Janitor symbolic
stack preservation and 24 negative cases.

Exact build head: 6efb8fd3ff4e5b5a31b3b85bd600abe5ac5c5da9 (PR #235).
All three pull_request runs at that exact head completed successfully:

- Inactive compile/archive review: 37140903801 / #2.
- Knowledge Architecture: 37140903816 / #989.
- Source/static contract gate: 37140903805 / #7.

The earlier workflow-parser failure 37140829036 / #1 at 851fe3b1b10408b433f35c3aa411867813d211f5
was a YAML quoting error in the parser-install command. It ran no jobs and compiled
or built nothing. Only workflow quoting was repaired before the successful run.

The project targets netstandard2.1. Actual SDK selected by dotnet was 10.0.401,
MSBuild 18.9.11+e34a38d2a, as recorded in dotnet-info.log. setup-dotnet ensured 8.0.x
was installed but did not pin SDK selection; do not describe this artifact as built
by SDK 8. The three source-pinned NuGet versions resolved exactly: BepInEx.Core
5.4.21, HarmonyX 2.10.2 and LethalCompany.GameLibs.Steam 81.0.5-ngd.0. Full resolved
package identities/SHA-512 values and PE AssemblyRef metadata are in BUILD_RESULT.json;
the original project.assets.json remains in the frozen artifact. BepInEx.Core 5.4.21
resolves BepInEx.BaseLib 5.4.20, explaining its PE reference version 5.4.20.0.

## Exact frozen bytes

Assembly name: S142AKBMAFR1I1.
DLL SHA-256: d9e09b20a889260d5cc8b4970d023a76d5b7af77ad677077b9718dfa8a150b6a.
Profile SHA-256: 734dbe491b4f4fb77704472a303e386058e976325e0595dc4795af1940d1cb07.
Actions ZIP SHA-256: c16938786c6ffa8e0dc43e71a3fad206457433397cb9fd34c8676da1d2d4b60c.
Artifact ID: 11280870468; size: 598993 bytes.
Artifact name: S1.42AK-BMAFR1I1-review-6efb8fd3ff4e5b5a31b3b85bd600abe5ac5c5da9.

The frozen Actions ZIP was downloaded to a separate assistant workspace. Its actual
bytes were independently hashed with Python hashlib and matched both the Actions
digest and upload log; ZIP CRC checks passed. The exact public BMAFR1 parent was
downloaded independently at the frozen main commit and rehashed. The independent
archive validator and its seven negative cases then passed against the downloaded
profile/DLL and parent. This is completed independent verification, not reliance
on a digest merely returned by the build job.

REVIEW_BUILD_CHECKPOINT.json records the complete provenance and individual hashes
of the frozen artifact's 14 files. BUILD_RESULT.json, ARCHIVE_VERIFICATION.json and
the retained logs are exact original artifact bytes. Their earlier status fields
are chronological: BUILD_RESULT precedes the independent archive step, and the
archive report precedes Actions upload/download. This checkpoint closes those
pending checks without rewriting the original reports.

## Archive contract

Parent: Profiles/LC V1 S1.42AK-BMAFR1.r2z.
Parent SHA-256: 8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5.
Review identity: LC V1 S1.42AK-BMAFR1I1.
337 parent members become 338 review members.

- Added exactly BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll.
- Changed existing member exactly export.r2x: byte-exact profileName replacement only.
- No removed members, package changes or config changes.
- All other parent member bytes remain identical, including raw nine-U+200B Foundry
  binding, BMAF diagnostic DLL and accepted normalizer.
- Permanent Gale path guard and self-test pass: 219/221 characters, maximum 221/255.

The review-only JSON recipe is disabled for the generic builder; the isolated helper
requires its exact shape explicitly. No ProfileSources indexing or canonical build
result writing occurs. No binary DLL/profile is committed by this PR.

## Freeze and remaining gate

Recording the checkpoint also adds a workflow guard: later PR synchronization with
this record verifies the source/recipe against the exact build head and skips all
recompilation, reconstruction and upload. This avoids creating an accidental second
review artifact when only evidence is committed. A green frozen-guard run is not a
new build or a new independent artifact download. Trust the exact build run and
frozen artifact identified above; do not rebuild to obtain different bytes.

Next bounded work: review PR #235, its final changed files and exact final-head CI,
then integrate infrastructure/evidence and reconcile canonical lifecycle only when
justified. If CURRENT_STATE is updated, use render_current_navigation.py and verify
permanent exact-main-head Knowledge Architecture. Publication authorization remains
a separate later lifecycle decision; no publication, indexing, Gale import or
runtime activation is authorized by this review.

This originating chat has completed execution segment 2 of its maximum 2 and must
not start a third project segment. The open draft PR is the durable continuation
point. Read the three mandatory main authorities afresh before continuing and then
read this branch checkpoint; main correctly still represents the pre-integration
authorization state.

## Preserved lifecycle and uncertainty

S1.42AK remains accepted. BMDSFIX1 remains active/not accepted with its passive,
outstanding, unwaived DeepSewersFlow gate; no dedicated reroll. BuildSpecs/current.json
remains disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS and ACTIVE_BUILD plus
AUTO_BUILD_RESULT remain BMDSFIX1. BMAFR1 keeps its bounded Black Mesa x Foundry PASS
and stays inactive/DIAGNOSTIC ONLY/NEVER ACCEPT. BMAFDIAG1/PATH1 remain DO NOT RERUN.

Compilation, source/static and archive validation do not prove live Harmony/JIT
installation, loader behavior, Princess selection, live Janitor blendShapeCount=0,
the exact array emitter, native Unity ownership or root cause. SpringMan remains
an equal-scope contemporaneous alternative. No runtime test is released.
