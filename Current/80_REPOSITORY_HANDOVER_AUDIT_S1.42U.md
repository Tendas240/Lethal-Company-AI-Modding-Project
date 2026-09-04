# 80 — Repository Handover Audit: S1.42U

**Date:** 2026-09-04  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Purpose:** final consistency audit for transfer to a new ChatGPT conversation.

## Audit verdict

**PASS — repository is handover-ready.**

The canonical repository state consistently identifies:

- S1.42U as the newest fully accepted full-normal-stack gameplay baseline;
- S1.42U as the newest runtime-accepted technical descendant;
- no newer built candidate;
- S1.42V as plan-only / not armed;
- the exact next technical action as resolving the narrow always-on Jetpack acceleration implementation before S1.42V is armed;
- the later environment/interior, BCMER EventType and final full-stack stages as separate future gates.

No local repository clone or local build is required for the handover.

## Accepted baseline identity — verified

Build:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Profile SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build Actions run:

`33818241873` = **success**

Build commit:

`29e7b36c3d09ff37551894438744d67089d7aba4`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Final handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

## Runtime evidence — verified

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Raw size:

`1,959,356 bytes`

Line count:

`19,939`

Accepted runtime facts:

- exact BCMER 1.71.0 loaded and completed patching;
- Compatibility Fixes 1.3.14 loaded;
- EnemyIsolation disabled;
- normal `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- Fatal = 0;
- old NoticeZone/unspawned NetworkObjectReference marker = 0;
- no crash/freeze;
- no gameplay-visible technical problem reported.

This evidence closes the S1.42U BCMER-on integration gate.

## Controller audit — verified

### Build controller

`BuildSpecs/current.json`

Current state:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base profile = `Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`;
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`;
- `mod_state_changes = []`;
- `mod_additions = []`;
- `mod_removals = []`;
- `config_patches = []`;
- `local_plugin_builds = []`;
- no successor build armed.

Blob SHA verified at handover:

`f1248c0b5740d83081ccf16c1de1295fafdbf1f5`

### Runtime router

`RuntimeInbox/ACTIVE_BUILD.txt`

Current value:

`S1.42U`

Blob SHA verified at handover:

`75a334389cd722cb1d5dcd08e4dd343f14ea727f`

This routing is correct because S1.42V does not exist yet and no successor runtime gate is active.

### Workflow state

The newest canonical-profile workflow run remains the safe idle-controller run:

`33855281208` / run #70 = **success**

Its head commit is the idle-controller commit `0afeb889723312ec5036726e3c654cdfbe4f3a27`.

No S1.42V build was triggered during handover documentation updates.

## Restore invariant audit — verified

S1.42U:

`ProfileSources/S1.42U/BepInEx/config/LethalLevelLoader.cfg`

remains byte-identical to the canonical S1.42C restore baseline:

`ProfileSources/S1.42C/BepInEx/config/LethalLevelLoader.cfg`

Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

Therefore the stored per-moon inside/daytime/nighttime power counts and enemy spawn lists are already correct and must not be treated as open repair work.

SpawnCycleFixes remains on:

`Consistent Spawn Times = true`

and is byte-identical to S1.42C, preserving the intended standardized first wave around 07:39 including outside/daytime participation.

## Permanent compatibility audit — preserve

Current accepted compatibility state:

- exact BCMER 1.71.0 enabled;
- EnemyIsolation off;
- compatibility plugin v1.3.14;
- compatibility DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle preserved;
- Pikmin -> Baboon Hawk combat preserved;
- Puffer -> Pikmin protection preserved;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- normal enemy population restored.

Never-repeat evidence remains:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Patch safety remains binding:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Focused accepted lifecycle evidence remains:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

## Gale import / project-local DLL guard — verified documented

The accepted S1.42U profile and expected successors carry the project-local Compatibility Fixes DLL.

README now explicitly requires Gale:

**Advanced options -> Import all files**

A successor compatibility runtime test is invalid unless its log contains:

`Loading [S1.39 Compatibility Fixes 1.3.14]`

If the marker is absent, correct the import/load path before interpreting compatibility behavior.

## Next-build audit — S1.42V

`BuildSpecs/S1.42V_PLAN.md`

Status verified:

**plan-only / not armed / no S1.42V profile exists.**

Current intended scope:

- ImmortalSnail `Rarity 80 -> 40`, keep `Max Snails = 2`;
- Functional Microwave volume `0.7 -> 0.5` proposed;
- modest always-on base Jetpack acceleration increase.

Blocking technical question:

The exact unconditional base Jetpack acceleration owner/method/field is not yet frozen.

The handover correctly records that:

- ButteRyBalance `Control Scheme = V49` is a broad handling/inertia mode and must not be switched merely to fake acceleration;
- More Ship Upgrades `Jet Fuel` uses `20` initial / `20` incremental acceleration but is purchase-gated;
- Jet Fuel must not silently replace the requested always-on base behavior;
- JetpackFixes interaction must be inspected;
- custom code, if required, needs a Patch Safety Review and should be isolated from unrelated tuning if practical.

## Post-S1.42V sequence audit

The repository consistently records the following staged plan without prematurely assigning later build IDs:

1. **Environment / Interior tuning**
   - equal probability for all installed interiors and the same rule for future additions;
   - CullFactory exceptions `junkrooms`, `shatteredrooms`;
   - Mausoleum fog reduction;
   - CodeRebirth Microwave rarity reduction.

2. **BCMER EventType balancing**
   - fixed equal distribution: `8 x 12.5%`.

3. **Final S1.42 full-stack acceptance**
   - longer normal run after individual tuning gates pass;
   - varied enemies/Pikmin/BCMER/interiors/Jetpack/CodeRebirth coverage;
   - complete runtime-log ingest;
   - final promotion only if permanent invariants remain clean.

Heavy Baboon-Hawk or isolated-enemy diagnostics are not routine next tests; reopen only if a future change touches the path or new evidence indicates regression.

## Repository cleanup classification

### KEEP — intentionally preserved

- S1.42U profile, snapshot, build verification and runtime evidence;
- S1.42T accepted BCMER-off comparison evidence and profile;
- S1.41 previous accepted full-normal-stack historical baseline;
- S1.42S lifecycle acceptance evidence;
- S1.42R failed-root-cause evidence;
- S1.42C enemy restore baseline;
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
- `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`;
- older detailed handover/diagnostic files that retain unique chronology or root-cause value;
- relevant historical profiles/config snapshots needed for regression reconstruction.

### UPDATE — synchronized for this handover

- `START_HERE_ChatGPT_Masterprompt.txt` current takeover bootstrap;
- `README.md`;
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`;
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` current checkpoint;
- `Current/Projektstatus_S1.42U.json`;
- `BuildSpecs/S1.42V_PLAN.md`.

### ADD

- `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`;
- `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`.

### ARCHIVE

No physical archive move was necessary. Older handover/build-plan documents remain in place as clearly historical evidence and are overridden by newer chronological files.

### DELETE

**None.**

No file or runtime evidence was sufficiently certain to be permanently valueless. The conservative preserve-history rule was followed.

## Final canonical entrypoint blob snapshot

The following repository text blobs were verified as the final handover entrypoint state immediately before finalizing this audit:

- `START_HERE_ChatGPT_Masterprompt.txt` = `f2619d3791629f3f1cef8c7728fc03156b030fef`;
- `README.md` = `f047ec84e265226373e30589ae9f2e8dd3df8ef4`;
- `Current/00_CURRENT_STATE.md` = `8290f669b274940972e86563e6448565b95503cb`;
- `Current/01_HANDOVER_CORE.md` = `5feaba5539eeba0cc459c9dd5b58fa5a845eb968`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md` = `186e7042f2e9acd1bfdbc128c8d1b29cd7f83d34`;
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` = `278310ec4d0822c4206f345bbb72bb65f9ae655d`;
- `Current/Projektstatus_S1.42U.json` = `2f0b4e58675e3c0adc68af650f6abd055eb3261a`;
- `BuildSpecs/S1.42V_PLAN.md` = `173791bb1c1423fe49dfc912734d95157731c449`;
- `BuildSpecs/current.json` = `f1248c0b5740d83081ccf16c1de1295fafdbf1f5`;
- `RuntimeInbox/ACTIVE_BUILD.txt` = `75a334389cd722cb1d5dcd08e4dd343f14ea727f`;
- `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md` = `5223efeebb2fec8315b7eebcd564056157110042`.

This audit file itself is intentionally excluded from its own blob snapshot because updating the list would recursively change its blob SHA.

## Known non-functional drift — intentionally not mixed into gameplay work

The audit confirms two known non-functional stale areas still exist:

- older chronology subsections in `Current/02_TECHNICAL_BASELINE.md` contain stale local `current` wording;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` do not perfectly describe accepted v1.3.14 behavior.

These do not override current code/config/runtime evidence. Cleanup is a later separate maintenance task and should not be mixed into a risky Jetpack/runtime patch.

## Monitor-only issues — carried forward

- historical S1.42S disconnect-only Pikmin NoticeZone / unspawned NetworkObjectReference exception, absent in S1.42U;
- historical S1.42T one-off `AloeChase` FSB load-state message with no established gameplay impact;
- known setup loaforcsSoundAPI/HarmonyX and SoftMaskKiller-handled exception classes, non-blocking unless they change behavior, flood or become user-facing.

## Manual user work

**No manual repository work is required.**

No PowerShell command is required for this handover.

Do not ask for a local clone or local profile build. The required S1.42U base profile, snapshots and GitHub-native build infrastructure are already online.

## Entry-point consistency — verified

README and `Current/01_HANDOVER_CORE.md` now directly reference this audit.

The canonical read order begins:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`
3. `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`
4. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/Projektstatus_S1.42U.json`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `BuildSpecs/S1.42V_PLAN.md`

The chronologically newest confirmed state wins over older historical wording.
