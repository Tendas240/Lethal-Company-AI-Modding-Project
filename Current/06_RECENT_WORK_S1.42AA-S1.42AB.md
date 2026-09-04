# 06 — Recent Work S1.42AA -> S1.42AB

**Date:** 2026-09-04

## S1.42AA runtime result

S1.42AA `Interior Weight Equalization` was tested on Offense and rejected.

Profile SHA-256:
`0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Runtime evidence:
`RuntimeEvidence/S1.42AA/20260904T153744Z/`

The intended config-only change was:

`Inject Dynamic Matching Weights = true -> false`

Fresh runtime proved the effective dungeon pool remained unequal. Examples included:

- LiminalHouse `300`;
- Sub Systems `275`;
- Abandoned Foundry `250`;
- Shatteredrooms `75`;
- Lead Factory `70`;
- Spelunkers Caverns (Random) `50`;
- Crimson Keep `35`;
- Gray Apartments `25`;
- DeepcoreMines `25`;
- several `20`-weight interiors.

Root cause analysis established that LethalLevelLoader retains the highest matching rarity across matching sources, so generic `Vanilla:100,Custom:100` tags cannot lower stronger author/planet/mod matches.

Black Mesa generated successfully in the AA run.

A separate Black Mesa/Pikmin routing issue was observed: a Pikmin carrying scrap from a table ran in place and failed to reach the ship. The log repeatedly showed unreachable interior entrance nodes and `Unpathable` ToShip routing. This is tracked separately as likely map/NavMesh/entrance-routing compatibility evidence, not as the interior-weight failure.

The AA log also contained two `Work state with no task assigned!` warnings during a separate White-Pikmin lifecycle sequence. Leader-null remained `0`; Fatal remained `0`.

## S1.42AB design

Because the config-only approach could not reduce stronger LLL matches, S1.42AB moved normalization to the post-viability result.

Exact patch target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

S1.42AB behavior:

1. LLL performs its complete normal viability/matching/exclusion logic.
2. A project-local Harmony Postfix receives the already-returned viable list.
3. Every positive rarity in that list is changed to exactly `100`.
4. No flow membership is changed.
5. Enemy/Scrap/MapObject rarity systems are untouched.
6. Exact LLL `1.7.12` / API-contract checks fail closed.

This implements the permanent rule that future interiors automatically receive effective equal weight whenever LLL considers them viable, while preserving hard technical exclusions.

S1.42AB was built directly from accepted S1.42Z, not from rejected AA.

## S1.42AB build result

Profile:
`Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`

SHA-256:
`3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Successful workflow run:
`33892396551`

Automated build commit:
`9bf3085d82990ca565ad81f992d896855c21f1c6`

Injected DLL SHA-256:
`901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

Archive delta vs accepted S1.42Z:

- ZIP members `334`;
- changed existing = exactly `export.r2x`;
- added = exactly S1.42AB DLL;
- removed `0`;
- config changes `0`;
- package/mod state changes `0`.

The generated snapshot retains `Inject Dynamic Matching Weights = true`, proving AA's failed config switch was not inherited.

## Runtime-marker design

LLL's built-in `Viable ExtendedDungeonFlows` line is emitted before the Postfix and can still contain pre-normalization values.

Authoritative AB marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry there must be `(100)`.

## Gale replacement automation work

During the AA -> AB transition the project upgraded `RuntimeTools/ReplaceActiveGaleProfile.ps1` from a partly manual helper into a fully automated, evidence-verified replacement flow.

### Missing Profiles automation

Initial UI Automation attempts fell back safely as `ambiguous`. The selector was refined to target actual actionable UIA controls rather than duplicate text nodes.

The real `Missing Profiles` dialog was then successfully automated through semantic UI Automation:

`Delete -> Submit`

No screen coordinates or blind keyboard navigation are used.

### Import UI automation V1

The helper successfully automated:

`Advanced options -> Import all files -> Import`

but reopened the `.r2z` a second time after Missing Profiles, creating a second empty import-code dialog through Gale's single-instance/deep-link path.

This proved the import UIA targeting worked but exposed a sequencing defect.

### V2

V2 changed the architecture to:

- open the `.r2z` exactly once;
- use the already-buffered import dialog after Missing Profiles closes;
- remove transient toast detection;
- verify import completion by hashing `export.r2x` inside the verified archive and requiring the exact same SHA in the imported local target profile.

The first V2 controlled test failed safely before deletion because a cache-busting query string on the binary Raw-GitHub `.r2z` URL returned HTTP 404.

### V2.1 — FULL PASS

Validated revision:
`2026-09-04-import-uia-v2.1-download-hotfix`

Validated helper blob SHA:
`9458f427b538615249714e7f064f3107d6dcd36c`

Validated commit:
`f711f53f4971f97200ed3605479ef887a14b243d`

V2.1 removed the binary-download query string while preserving the single-open and post-import hash-evidence design.

Controlled user validation from real starting condition S1.42AA present / S1.42AB absent achieved full PASS:

- profile download SHA matched repository expectation;
- `export.r2x` evidence SHA was computed;
- old AA deleted only after numeric choice + `y`;
- Missing Profiles resolved automatically;
- `.r2z` opened exactly once;
- `Import all files` enabled automatically;
- Import triggered automatically;
- no second empty import dialog;
- exact target local `export.r2x` matched archive-entry SHA;
- temporary `.r2z` removed automatically;
- no further Gale click or PowerShell Enter was required after profile number + `y`.

S1.42AB is now locally imported and current in Gale.

## Exact current next step

Do not reinstall AB and do not build a successor.

Run one normal Offense gameplay round with S1.42AB, enter the generated interior, upload the complete fresh `LogOutput.log` using the exact uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`, then analyze the full log.
