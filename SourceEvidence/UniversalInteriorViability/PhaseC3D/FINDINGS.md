# S1.42AK universal interior viability — Phase C3D native Black Mesa selection rule

**Status:** SELECTION-LAYER EVIDENCE / TWO BLACK-MESA PAIRINGS SUPPORTED / TOPOLOGY STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** `S1.42AK`  
**Main authority commit at checkpoint start:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `9b6bf950754aa269bcf71a0347c75dced676a4c0`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Result

C3D resolves the remaining native-selection question for the Black Mesa interior against the two External target moons.

The accepted S1.42AK Black Mesa owner config has:

- `Black Mesa | Allow Editing Config = true`;
- `Black Mesa | Preset Moon Weights = lethal_company:vanilla=+100,lethal_company:custom=+100`;
- empty weather weights;
- empty route weights.

C3A already proves from the exact accepted DawnLib 0.9.25 main assembly that the registered moon keys `black_mesa:black_mesa` and `code_rebirth:oxyde` satisfy Dawn's automatic non-vanilla custom-tag rule and therefore receive `lethal_company:custom`.

The DawnLib/Dusk 0.9.25 release source aligned with the accepted version shows the dungeon definition using the editable config value to build its `SpawnWeightsPreset`, the moon transformer falling back from exact-key matching to tag matching, and additive `+100` producing weight 100 from the preset's zero starting value. Empty weather and route tables leave that value unchanged.

The remaining `ShouldSkipRespectOverride()` guard is also resolved for the current owner chain. Dawn's guard skips vanilla, Dawn-`is_external`, or unimplemented content unless LunarConfig overrides that decision. Black Mesa is keyed `black_mesa:black_mesa` and is the Dawn-native dungeon that LLL exposes as its one External dungeon entry. LLL's Dawn conversion path only converts Dawn dungeons that are not already tagged `dawn_lib:is_external`. Combined with Phase A/C3C ownership evidence, the current Black Mesa dungeon therefore follows Dawn's native dynamic-rarity path rather than the skip/fallback path.

## Selection consequence

The following two B3 cells are now supported at the **selection layer** with effective rarity 100:

- Black Mesa interior × Black Mesa moon → `VIABLE_EQUAL_100`;
- Black Mesa interior × Oxyde → `VIABLE_EQUAL_100`.

C3B already supported 44 direct-LLL External-moon pairings. C3D therefore raises the supported External-row selection-layer total to **46 pairings**.

The authoritative B3 matrix is intentionally **not rewritten** in this intermediate draft checkpoint.

## Provenance qualification

The accepted runtime package remains byte-bound by the repository's SHA-256 native-owner snapshot:

- DawnLib main DLL SHA-256: `9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b`;
- DawnLib Dusk DLL SHA-256: `3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03`.

The public DawnLib release tag `v1.0.3-pre` points to source commit `810613e556ecc357eac25e97c25a3bb90516f071` and publishes DawnLib 0.9.25 artifacts. This is version-aligned source evidence for the Dusk weight-table implementation, not a claim that the public release archive is byte-identical to the accepted Thunderstore package. Exact accepted-package identity remains the repository SHA-256 evidence.

## Proof boundary

This checkpoint proves only that the current owner/matching stack can assign Black Mesa selection rarity 100 on the two External target moons.

It does **not** prove:

- successful generation for either pairing;
- main-entrance or fire-exit IDs/counts/pairing;
- topology compatibility;
- player traversal;
- geometry/socket compatibility;
- elevators;
- routing;
- NavMesh compatibility.

No duplicate LLL registration is introduced. S1.42AB normalization remains unchanged. Shatteredrooms exclusions remain unchanged. No gameplay candidate or runtime test is authorized.

## Next bounded analysis

Continue Phase C3 with **scene topology only**. Resolve Black Mesa 3.4.4 and Oxyde 1.6.9 moon-side main-entrance/fire-exit `EntranceTeleport` IDs and pairings from exact package/source evidence, then compare those expectations with Dawn/LLL/vanilla dungeon entrance-numbering behavior. Do not infer topology safety merely from the 46 selection-layer pairings.
