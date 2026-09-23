# S1.42AK universal interior viability — Phase C3A source checkpoint

**Status:** PARTIAL C3 EVIDENCE / NO MATRIX RECLASSIFICATION / NO BUILD OR RUNTIME AUTHORIZATION  
**Date:** 2026-09-19  
**Repository source commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Current authority:** `Current/CURRENT_STATE.json` and `Knowledge/INTERIORS_AND_LLL.md`  
**Plan:** `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`

## Result

LLL's **External** inventory category does not establish that an asset lacks DawnLib's **lethal_company:custom** tag.

The exact accepted-profile DawnLib binary contains an automatic tag rule that classifies registered keys outside the `lethal_company` namespace as custom. Both runtime-registered moon keys, `black_mesa:black_mesa` and `code_rebirth:oxyde`, satisfy that predicate.

This is a static source-derived tag expectation, not a final runtime tag dump, not proof that LLL receives the same tag list, and not entrance/generation/traversal clearance. The existing 106 External-moon matrix cells remain `NOT_YET_PROVEN` at this checkpoint.

## Exact package and configuration reconciliation

The current package versions come from `ProfileSources/S1.42AK/export.r2x`:

| Role | Package | Enabled version |
|---|---|---|
| Moon/interior owner | Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior | 3.4.4 |
| Oxyde owner | XuXiaolan-CodeRebirth | 1.6.9 |
| Native registration/tagging | TeamXiaolan-DawnLib | 0.9.25 |
| Viability/selection integration | IAmBatby-LethalLevelLoader | 1.7.12 |

The Black Mesa config header says 3.4.1 and the current startup log also reports plugin version 3.4.1. These strings must not be substituted for the **package version 3.4.4** recorded by the accepted profile. This checkpoint does not claim the exact Black Mesa package assembly has been inspected.

Current `Black Mesa Team.Black Mesa Half Life Moon Interior.cfg` establishes:

- `[BlackMesaDungeon Options]`: enabled; config editing enabled; `Preset Moon Weights = lethal_company:vanilla=+100,lethal_company:custom=+100`.
- Its commented default is `black_mesa:black_mesa=+300`; the active line contains the two broad tags instead. A default comment does not add the original exact-moon rule back.
- `[BlackMesaMoon Options]`: enabled; config editing enabled; cost 500; `BlackMesaScene | Allow Editing Config = false`.
- None of those settings enumerates entrance IDs, fire exits, teleport pairing or scene transforms.

Current `LethalLevelLoader.cfg` establishes:

- Black Mesa's **Custom Dungeon** section has `Enable Content Configuration = false`. Its displayed `Vanilla:100,Custom:100` line is not an enabled direct LLL override.
- Black Mesa's **Custom Level** section contains the author-disabled-automatic-config warning, not a usable level-tag/topology template.
- There is no Oxyde **Custom Level** section.
- Missing/disabled LLL templates do not establish a missing native-owner registration or an empty runtime tag set.

Current `CodeRebirth.cfg` is a small targeted config containing General, Merchant, FlashTurret and FunctionalMicrowave sections. It contains no Oxyde section. Owner defaults/assets remain required evidence; the absence of an Oxyde stanza is not a disabled moon or an unsupported-interior verdict.

## Runtime observations and their limits

Primary runtime: `RuntimeEvidence/S1.42AK/20260918T172838Z/raw/LogOutput.log`.

| Exact lines (splitlines numbering) | Observation |
|---|---|
| 8039–8040 | LLL lists Black Mesa and 745 Oxyde as External levels. |
| 10228–10229 | Dawn moon registry resolves `black_mesa:black_mesa -> Black Mesa` and `code_rebirth:oxyde -> 745 Oxyde`. |
| 12145, 21465 | Both played/attempted level loads name 21 Offense. |
| 12360, 21637 | Both LLL matching reports describe Offense, with Vanilla, Vanilla, Free, Canyon tags. |

There is no Black Mesa/Oxyde level-matching report in this accepted log. Its Offense entrance connections cannot be assigned to either External moon. The startup `EntranceTeleportB` missing-script warning is not causally attributed to either External moon here.

The broader trusted runtime triage in `Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md` likewise reports Offense-only observed generation. This checkpoint did not repeat the full historical-runtime scan.

## Binary-bound DawnLib evidence

The package URL and hashes were taken from the existing repository manifest:

`SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json`.

DawnLib 0.9.25 also matches the accepted S1.42AK export. The downloaded archive and all four assembly members were hash-checked against that manifest. No unpinned latest package was substituted.

- ZIP SHA-256: `c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3`.
- Inspected main DLL SHA-256: `9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b`.
- Selected-method capture: `DAWNLIB_TAG_AND_MATCHING_IL.json` beside this report.
- Reproducer: `AnalysisTools/inspect_universal_interior_c3a.py`.
- Dependencies: dnfile 0.18.0, dncil 1.0.2. The script reads IL and does not execute the inspected DLL or start Unity.

Thirteen captured methods establish:

1. `LethalContent::.cctor` constructs `Moons` as a `TaggedRegistry`.
2. `TaggedRegistry::.ctor` installs VanillaAutoTagger, CustomAutoTagger and AllAutoTagger.
3. `NamespacedKey::IsVanilla` compares the key namespace with `lethal_company`.
4. `CustomAutoTagger::ShouldApply` returns the negation of that test.
5. `Tags::.cctor` constructs `Custom` from `NamespacedKey.Vanilla("custom")`; `Vanilla` uses the namespace `lethal_company`. Thus the tag is `lethal_company:custom`, not a namespace named after the owner.
6. `TaggedRegistry::Freeze` evaluates taggers and calls `Internal_AddTag` for matching entries, then invokes AfterTagging.
7. `HasTagWeightContextualProvider::Provide` checks `HasTag` and returns a weight when matched, otherwise no value.
8. `LethalLevelLoaderCompat::EnsureCorrectDawnDungeonDynamicRarity` locates the matching dungeon, checks its Dawn information and respect-override guard, builds a moon/weather/route-price context and returns its Dawn weight clamped to zero. If the guarded native-owner path is not applicable, it delegates to the original LLL calculation.

This establishes a supported native tag/weight path relevant to Black Mesa's existing config. It does **not** prove every runtime guard, final tag mutation or weight-transformer outcome for the two target moons. It also does not prove that 22 directly configured LLL flows see a `Custom` tag on their LLL ExtendedLevels.

The packaged `custom.tag.json` and `vanilla.tag.json` have empty explicit values lists and comments identifying automatic generation. Empty JSON values lists therefore cannot be used to deny the binary's automatic tagging rule.

## Required next bounded analysis

Continue C3 with exact S1.42AK owner and bridge evidence:

1. Inspect the LLL 1.7.12 / Dawn 0.9.25 conversion path to determine how native moons become External ExtendedLevels and which tags LLL actually receives.
2. Inspect Black Mesa **package 3.4.4** and CodeRebirth **1.6.9** registration/assets for additional tags, level/scene identities, entrance counts/IDs and special transit mechanisms. Preserve source/package hashes.
3. Trace the relevant native-owner guard and weight-table transformation as needed before claiming a Black Mesa pairing is viable on either External moon.
4. Reclassify only pairings supported by the resulting owner/bridge evidence. Continue to distinguish availability from generation/traversal and routing proof.

If scene assets do not expose sufficient static topology or existing logs lack the necessary observation, record the exact remaining evidence gap. That does not authorize a runtime test by itself.

## Checkpoint decision

Phase C3 is **not complete**. Its first bounded source checkpoint is complete. No current-state lifecycle transition or matrix update is proposed by this evidence-only change.

S1.42AK remains accepted; the S1.42AB normalizer, build/runtime controllers, Shatteredrooms restrictions and all gameplay/config bytes remain unchanged. No gameplay build, universal override or runtime test was started.

