# 79 — Final Handover: S1.42U PASS / S1.42V Next

**Date:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Current accepted state

Newest fully accepted full-normal-stack gameplay baseline and newest runtime-accepted technical descendant:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Profile SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Runtime evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw runtime log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Raw runtime log size:

`1,959,356 bytes`

Line count:

`19,939`

GitHub Actions profile build run:

`33818241873` = **success**

S1.42U build commit:

`29e7b36c3d09ff37551894438744d67089d7aba4`

## S1.42U runtime verdict

**PASS — full normal stack restored and accepted.**

Confirmed from complete runtime evidence plus the user's clean gameplay report:

- exact `BrutalCompanyMinusExtraReborn 1.71.0` loads;
- BCMER reports `1.71.0 is done patching`;
- `S1.39 Compatibility Fixes 1.3.14` loads;
- EnemyIsolation is disabled;
- normal non-isolated enemies are active (`ADDING ENEMY` = 13);
- `Work state with no task assigned!` = 0;
- `Leader is null when following` = 0;
- `[Error  :S1.39 Compatibility Fixes]` = 0;
- Fatal = 0;
- old disconnect-only Pikmin NoticeZone / unspawned NetworkObjectReference marker = 0;
- no crash/freeze;
- no gameplay-visible technical problem was reported;
- known setup SoundAPI/SoftMask exception classes did not become a gameplay cascade.

Direct runtime power-count evidence from S1.42U:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1;
- Crawler = 3;
- Bunker Spider = 2.

## Accepted reference history

Previous accepted full-normal-stack baseline:

**S1.41 — BCMER Reactivation**  
Profile `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Accepted BCMER-off comparison point:

**S1.42T — Normal Enemy Restore**  
Profile `Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`  
SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`  
Evidence `RuntimeEvidence/S1.42T/20260903T222109Z/`  
Raw log SHA-256 `b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

S1.42T remains diagnostically valuable as the clean BCMER-off comparison point. Do not erase its acceptance evidence merely because S1.42U superseded its active role.

## Permanent do-not-regress compatibility state

Compatibility plugin:

**v1.3.14**

Embedded compatibility DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Preserve:

- exact BCMER 1.71.0 enabled unless a deliberate diagnostic gate says otherwise;
- EnemyIsolation off;
- `BaboonBirdPikminEnemy` enabled;
- only narrow Hawk -> Pikmin entry points blocked;
- native inherited `PikminEnemy` death/unlatch/task lifecycle preserved;
- Pikmin -> Baboon Hawk combat allowed;
- Puffer -> Pikmin poison/effect protection preserved;
- `Thumper Bite Limit = 3`;
- Crawler absent from LethalMin Attack Blacklist;
- normal enemy population restored.

Permanent patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Focused accepted lifecycle evidence:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Failed root-cause / never-repeat reference:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Never again disable the complete `LethalMin.BaboonBirdPikminEnemy` merely to prevent Hawk -> Pikmin interaction. The S1.42R failure proved that doing so suppresses inherited native lifecycle cleanup and can leave stale attack/task state.

## Canonical moon / spawn restore state

Current S1.42U:

`ProfileSources/S1.42U/BepInEx/config/LethalLevelLoader.cfg`

is byte-identical to:

`ProfileSources/S1.42C/BepInEx/config/LethalLevelLoader.cfg`

Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

Therefore all stored per-moon:

- maximum inside enemy power counts;
- maximum outside daytime enemy power counts;
- maximum outside nighttime enemy power counts;
- inside/daytime/nighttime enemy spawning lists

are already on the intended canonical restore baseline. Do not regenerate/normalize this file wholesale.

Spawn-cycle state is also preserved from S1.42C:

`Consistent Spawn Times = true`

This keeps the standardized first spawn wave at approximately 07:39 and avoids the vanilla vent-empty dependency delaying outside/daytime participation in the first wave.

Canonical restore reference:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Current tuning observations / requested changes

### Immortal Snail

Owner/config:

`BepInEx/config/dev.idjut.SnailFork.cfg`

Current:

- `Rarity = 80`
- `Max Snails = 2`

Requested next change:

`Rarity = 40`

Keep `Max Snails = 2`.

This halves the configured weighted spawn value; it is not a claim that every moon's final absolute probability becomes mathematically exactly 50% after the full weighted pool is evaluated.

### CodeRebirth Functional Microwave

Owner/config:

`BepInEx/config/CodeRebirth.cfg`

Current volume:

`Functional Microwave | Volume = 0.7`

The previous reduction survived into S1.42U, but the user still perceived the Microwave as too loud.

Proposed next value:

`Functional Microwave | Volume = 0.5`

Separate backlog item: CodeRebirth Microwave rarity should also be reduced later. Do not confuse spawn rarity with audio volume.

### Jetpack acceleration

User request:

Increase Jetpack acceleration modestly.

Current ButteRyBalance handling:

`Control Scheme = V49`

This is a broad inertia/handling mode, not a numeric acceleration knob. Do not change V49 merely to approximate a small acceleration buff.

More Ship Upgrades contains the actual purchasable `Jet Fuel` acceleration upgrade:

- `Initial Acceleration Increase = 20`;
- `Incremental Acceleration Increase = 20`.

Those settings only apply after the Jet Fuel upgrade is purchased. They are not an unconditional base-Jetpack acceleration setting.

The intended requirement at handover is an **always-on modest base Jetpack acceleration increase**. The exact owner/method/field must be identified before implementation. Do not invent a config key and do not silently substitute a Jet Fuel-only change.

If custom project-local code is required, perform a dedicated Patch Safety Review first and keep that risky code change isolated from unrelated balance changes if practical.

## Immediate next stage

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed / no S1.42V profile exists yet.**

### Exact next technical action

Before arming S1.42V:

1. identify the exact runtime owner and narrow implementation for an always-on modest Jetpack acceleration increase;
2. verify interaction with ButteRyBalance V49 handling and JetpackFixes;
3. determine whether this is config-only or requires project-local code;
4. if custom code is required, complete the Patch Safety Review and preferably isolate the Jetpack patch from unrelated tuning;
5. freeze the final S1.42V file/value delta;
6. only then arm `BuildSpecs/current.json` and use the GitHub-native build workflow.

### S1.42V currently intended tuning

- ImmortalSnail `Rarity 80 -> 40`;
- Functional Microwave `Volume 0.7 -> 0.5` proposed;
- modest always-on Jetpack acceleration increase once exact implementation is resolved.

### S1.42V runtime acceptance minimum

- startup/main menu succeeds;
- exact BCMER 1.71.0 remains active;
- Compatibility Fixes 1.3.14 still loads;
- normal enemies still spawn;
- Snail remains functional with deterministic config `Rarity = 40` verified;
- Microwave is audibly lower without functional regression;
- Jetpack accelerates modestly as intended;
- no unintended max-speed, V49 inertia/handling, explosion/death or JetpackFixes regression;
- Work/no-task = 0;
- Leader-null = 0;
- no new project compatibility error/exception flood;
- fresh complete runtime log ingested.

## Planned stages after S1.42V

These stages are intentionally not yet assigned build IDs. Do not silently mix them into S1.42V.

### Stage 2 — Environment / Interior tuning

Pending scope:

- equal probability for all installed interiors, including future newly added interiors by project rule;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

Expected tests:

- deterministic config/delta verification;
- multiple landings/reroutes to exercise different interiors;
- targeted `junkrooms` / `shatteredrooms` CullFactory behavior check;
- visual Mausoleum fog check;
- Microwave functionality plus lower occurrence over repeated normal play.

### Stage 3 — BCMER EventType balancing

Pending scope:

- fixed equal EventType distribution: **8 x 12.5%**.

Expected tests:

- exact config verification that all eight EventTypes are equally weighted;
- BCMER exact 1.71.0 preserved;
- multiple event/runtime runs for functional coverage;
- do not claim empirical 12.5% statistical proof from a small sample when deterministic config verification is available.

### Stage 4 — Final S1.42 full-stack acceptance

After the tuning stages pass individually:

- run a longer normal full-stack gameplay session;
- exercise varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth systems;
- ingest the complete log;
- verify all permanent critical counters/invariants again;
- if clean, promote the resulting profile as the final S1.42 accepted baseline.

Do not reopen isolated-enemy diagnostics or heavy Baboon-Hawk stress testing unless a later change touches that compatibility path or new evidence reopens the regression.

## Monitor-only issues

1. Historical S1.42S disconnect-only `PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`. It did not recur in S1.42U. Do not patch absent reproducibility/user impact plus Patch Safety Review.
2. Historical S1.42T one-off `Failed getting load state of FSB for audio clip "AloeChase"`. No gameplay impact established. Monitor only.
3. Known setup noise: loaforcsSoundAPI/HarmonyX TypeLoadException and SoftMaskKiller-handled SoftMask NullReferenceException classes. Non-blocking unless behavior changes, frequency explodes or gameplay impact appears.

## Known non-functional documentation drift

Do not confuse these with gameplay/code drift:

- `Current/02_TECHNICAL_BASELINE.md` has older chronology subsections containing stale local `current` wording;
- `Patches/S139CompatibilityFixes/Plugin.cs` has historical comments from older S1.42J-era assumptions that do not perfectly describe accepted v1.3.14 behavior.

Current code/config/runtime evidence and chronologically newer canonical documents are authoritative. Cleanup can be done later as a separate repository-maintenance task; do not mix comment/document cleanup into a risky runtime patch build.

## Controllers at handover

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base profile = `Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`;
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`;
- no package/config/local-plugin change armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

No successor profile is built or armed.

## Runtime evidence retention

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Keep diagnostically valuable S1.42 restoration evidence and acceptance documents. Do not delete unique historical evidence merely because the active role moved forward.

S1.42T remains useful as the BCMER-off comparison baseline. S1.42U is the full-stack accepted reference.

## Local-user action at handover

**None required.**

Do not ask for a local repository clone or local profile build. The accepted base profile and GitHub-native build infrastructure are already in the repository.
