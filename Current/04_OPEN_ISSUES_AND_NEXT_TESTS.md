# 04 — Open Issues and Next Tests

## Accepted baseline — S1.42AB

**PASS / ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine status: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Fresh Offense runtime closed the gate successfully:

- exact S1.42AB plugin loaded;
- LethalLevelLoader `1.7.12` validated;
- exact post-viability target contract validated and armed;
- pre-normalization viable pool: 40 entries, rarity range `20..300`;
- final effective viable pool: same 40 entries, every positive rarity exactly `100`;
- `12 / 40` entries normalized;
- no flow membership insertion/removal;
- Black Mesa single-registered at final `100`;
- normal dungeon generation succeeded and `Expanded facility` was selected;
- user entered the interior, played normally until death and reported no problematic behavior;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- unspawned NetworkObjectReference `0`;
- PikminNoticeZone regression `0`;
- Fatal `0`.

The complete log contains 32 Error-severity events, matching accepted S1.42Z. Known loaforcsSoundAPI/HarmonyX and SoftMask/SoftMasking exception classes remain monitor-only.

## Accepted interior rule

LethalLevelLoader owns viability/exclusion membership first. S1.42AB then normalizes only positive rarity values in the already-returned viable list to `100`.

Permanent accepted behavior:

- flow absent from LLL result -> remains unavailable;
- returned positive-rarity flow -> effective rarity `100`;
- no flow appended, removed, re-registered or deduplicated;
- no LLL matching/config list rewritten;
- Enemy, Scrap and MapObject rarity systems untouched;
- newly installed interiors inherit effective rarity `100` automatically whenever LLL itself considers them viable.

Preserve the Shatteredrooms Experimentation/Embrion restriction until dedicated evidence proves removal safe.

The built-in LLL `Viable ExtendedDungeonFlows` line is pre-Postfix only. The authoritative accepted marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## Previous / rejected states

### Previous accepted baseline — S1.42Z

S1.42Z remains the previous accepted rollback/provenance artifact. Its accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning is inherited by S1.42AB.

### Rejected gate — S1.42AA

S1.42AA remains **RUNTIME FAIL / NOT ACCEPTED**. The `Inject Dynamic Matching Weights = false` config-only experiment did not equalize effective LLL weights because LLL retains the highest matching rarity.

Black Mesa table/NavMesh/Pikmin ToShip routing remains a separate deferred compatibility finding. The two-warning Work/no-task lifecycle finding from AA did not reproduce in AB.

## Next test/build state

**No runtime test is currently outstanding and no successor build is armed.**

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AB_ACCEPTANCE`, guarded by the accepted S1.42AB SHA-256.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

The next isolated scope must be explicitly selected before a successor is designed or built.

## Eligible next isolated scopes

### BCMER EventTypes equal distribution

Planned target: exactly `8 × 12.5%` across the eight BCMER EventTypes.

This scope is now eligible to be selected next because the S1.42AB gate has closed. It is not yet armed and must remain isolated from unrelated changes unless explicitly grouped by the user.

### Functional Microwave spawn-rarity reduction

The current accepted volume remains `0.15`. Spawn rarity reduction is still deferred and should be handled independently.

### CullFactory exceptions

Potential exceptions for `junkrooms` / `shatteredrooms` remain deferred pending an isolated safety review.

### Mausoleum fog reduction

Deferred balance/visibility scope; keep separate from unrelated gameplay changes.

### Black Mesa table/NavMesh/Pikmin route recovery

AA produced meaningful unreachable-entrance / `Unpathable` ToShip evidence correlated with a Pikmin stuck while carrying scrap from a table. Do not introduce a broad global recovery/teleport patch without stronger reproducibility and a narrow compatibility design.

### LethalEscapeUpdated 2.5.0 evaluation

Potential isolated V81 evaluation of `woah25-LethalEscapeUpdated 2.5.0`. Inspect the actual package/config first and protect Baboon Hawk/LethalMin/Pikmin lifecycle plus SmartEnemyPathfinding/FairAI/NavMesh behavior. Do not silently mix it into another scope.

### Final long full-stack acceptance

Still deferred until the intended remaining isolated changes are complete.

## Monitor-only / stronger evidence required

- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown repair only with stronger evidence;
- historical S1.42S disconnect PikminNoticeZone/unspawned NetworkObjectReference exception;
- historical S1.42T AloeChase FSB load-state message;
- historical S1.42W `DespawnLumiknulls()` collection-modified teardown exception;
- loaforcsSoundAPI/HarmonyX `TypeLoadException`;
- SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes;
- cosmetic documentation/comment cleanup.

## Verified invariants — preserve

- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- BaboonBirdPikminEnemy enabled;
- narrow Hawk -> Pikmin block with native inherited lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- Jetpack `18`, Jet Fuel `18/18`, Thrusters `25/20`;
- Indoor Pikmin `0.09`, CarryStrength `3 / 30`;
- ACU + G.R.E.G. exact 18-curve providers ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `40 / 2`;
- accepted S1.42AB post-viability interior normalization.

Never repeat the S1.42R whole-component disable approach.
