# 05 — Failed, Obsolete, Parked, or Misclassified Approaches

Do not reintroduce these without new technical evidence or explicit user instruction.

| Component / approach | Status / reason |
|---|---|
| LethalCompanyVariables / EnemyRarityConfig | Historically removed; do not restore as spawn authority. |
| LethalQuantities 1.2.9 as global enemy owner | Examined enemy-control sections were not the active source of truth. |
| AutoCompanyBuilding 1.2.1 | Loaded but routing unreliable on V81. |
| AutoCompanyBuilding 1.1.3 | Routing could work; automatic landing did not. |
| RandomMoonFX 1.4.4 for Company automation | Active state interfered with manual moon selection; disabled state lacked needed behavior. |
| Old Hold_Scan_Button | Replaced by working LethalHUD Hold-to-Scan. |
| Peepers enemy/hazard | Removed. Do not confuse with Peeper tool. |
| CodeRebirthLib | Hard project rule: do not reinstall. Modern stack uses DawnLib. |
| ProjectSCP-SCP999 | Keep disabled; S1.31-S1.34 runtime logs proved startup NRE in `SCP999.Plugin.Awake()`. |
| Gnomes | Removed after V81 `PlayerIsTargetable` MissingMethod spam. |
| FacilityMeltdown | Fully removed. |
| ASTeam Racist Hoarding Bugs replacer | Removed. |
| FearOverhauled | Removed. |
| LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight | Do not reactivate on V81 due to AI/collision problems. |
| MirageClipLimiter.dll | Unrealized plan; DLL does not exist. |
| Forcing Rolling Giant / Shy Guy / Siren Head positive weights through LLL | Native ownership is the reliable architecture. |
| AJB-Keep_hangar_ship_door_closed | Unconditional refill can turn an ordinary close into permanent outside lockout. Replaced by narrower local failsafe. |
| Treating S1.34 hydraulic countdown as a failed custom algorithm | Invalid conclusion: local DLL had not loaded; observed behavior was vanilla. |
| EnemyScan 1.2.1 original scan-node-filtered list as complete census | Incomplete by design; project-local patch replaces list-building output. |
| S1.37 normal-scrap Currency filter as complete solution | Insufficient: CodeRebirth also has a separate DawnLib map-object path. |
| S1.39 late `RoundManager/SelectableLevel` map-object Currency filter as complete solution | Runtime disproved it; natural Coins/Wallets still appeared while plugin load was confirmed. |
| S1.40 sparse `CodeRebirth.cfg` without disabling config cleanup | Runtime disproved it; post-run config restored `Clean Unusued Configs=true`, Flash Turret inside-hazard=true and positive Currency moon curves. |
| S1.40A cleanup-retention-only fix as complete solution | Runtime disproved it. `Clean Unusued Configs=false` survived, but DawnLib per-content `Allow Editing Config=false` still restored author defaults. S1.40B opened only the relevant edit gates and passed. |
| Assuming LethalMin `Crane Targets/Squishes Pikmin=false` prevents every crane kill | Runtime disproved it; S1.39 direct CodeRebirth utility-kill guard exists for this gap. |
| Enabling all Lethal Resonance groups | Not desired. Design is Old-Bird-only. |
| Using S1.29D as gameplay base | Forbidden; diagnostic-only power audit derivative. |
| Upgrading BCMER to 2.0.0 as part of first reactivation | Do not do this. BCMER 2.0.0 is a major compatibility break from prior versions. First reactivation must use exact existing 1.71.0. |
| Pre-writing all future interior configs before content has generated real sections/IDs | Avoid. Binding workflow uses S1.42A seed first, then real generated configs are collected and tuned. |
| S1.42D broad LethalMin reflection/Harmony scan | **Failed startup.** It patched inherited/generated methods through derived types, produced HarmonyX warnings and the process terminated during the scan. Never restore this broad scan; S1.42E uses DeclaredOnly *PikminEnemy interaction methods. |
| Patching `JetpackItem.Start` when it resolves inherited `GrabbableObject.Start` | Avoid. S1.42D showed the target is inherited and HarmonyX warned. S1.42E uses narrow loaded Jetpack Item asset targeting instead. |
| S1.42E EnemyIsolation using `Activator.CreateInstance(entryType)` for `SpawnableEnemyWithRarity` | **Failed diagnostic implementation.** V81 has no usable parameterless constructor. On Gordion this retried six times per second and matched visible periodic freezes. S1.42F skips Gordion/Company and uses the EnemyType/int constructor with clone fallback. |
| Continuous `FindObjectsOfType<EnemyAI>()` from diagnostic EnemyIsolation | **Failed performance approach.** S1.42F proved Gordion smooth but routed moons still stalled when the once-per-second global EnemyAI scan became active. The clean S1.42G BCMER-off retest confirmed the freezes disappeared after removal. S1.42H uses late lifecycle pool hooks and must not restore continuous scanning. |
| Coroner `JetpackItem.Update` death detector on an unheld Jetpack | **Failed upstream interaction.** Coroner queries `playerHeldBy` every frame even when null, producing `PlayerController was null` + `Index not assigned!` at frame-rate cadence. S1.42G keeps Coroner but unpatches only this Jetpack Update detector; the clean BCMER-off retest confirmed the `PlayerController was null` flood is gone. || Treating the four declared LethalMin `*PikminEnemy` adapter hooks as a complete generic invincible-Pikmin grab repair | **Insufficient.** The clean S1.42G BCMER-off retest reproduced Thumper -> Pikmin leader removal through the common declared `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` path. S1.42H patches that exact base method once; do not return to adapter-only coverage as the complete solution. |


## S1.42P Baboon-Hawk correction

**S1.42P proximity-only Hawk-death selection + one-shot FinishTask as a complete solution is insufficient.**

Runtime evidence:
`RuntimeEvidence/S1.42P/20260903T181706Z/`

Do not repeat these assumptions:
- a fixed 4.0 m world-distance zone reliably identifies every Pikmin attacking the dying Hawk;
- calling `PikminAI.FinishTask()` once is sufficient while the dead Hawk remains discoverable as an enemy target.

S1.42P proved:
- `FinishTask()` itself is the correct high-level native task finalizer;
- real attacker `Yellow Pikmin_ruCpzY` was missed by the 4.0 m selector and hit the dead Hawk for ~84.565 s;
- FinishTask-selected Pikmin immediately rediscovered the already-dead Hawk and could start a fresh `AttackEnemy` task;
- the user's 20 -> 18 loss is log-confirmed.

Future work must use actual target identity and must invalidate dead Hawks for Pikmin enemy acquisition. Do not merely increase the radius and do not fall back to direct `RemoveCurrentTask()`.


## Important correction — LethalModDataLib

Older project wording was too categorical.

Correct status:
- LethalModDataLib used to be present.
- An old NRE occurred in the ShipWindows/save/mod-data context.
- After a ShipWindows update, LethalModDataLib was removed and the old NRE disappeared.
- No surviving mod required it, so there was no reason to reintroduce it.
- This chronology does **not** prove LethalModDataLib alone was the root cause.
- It may have been an interaction among old ShipWindows + LethalModDataLib + V81.
- No complete old stack trace has been rediscovered in current evidence.

Therefore LethalModDataLib is **not** a hard ban like CodeRebirthLib.

If `Dungeons_Ultimately_Lacking_Liveliness` requires `MaxWasUnavailable-LethalModDataLib 1.2.2`, it may be reintroduced only in the isolated S1.42A interior stage and must be regression-tested around save/mod-data/netcode behavior.

## Deliberately parked, not obsolete

### Malfunctions
Disabled from S1.34 onward by explicit user decision. Do not re-enable unless the user explicitly asks.

### BCMER
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` is no longer parked.

It was reactivated in isolated S1.41 and **runtime accepted**.

Current rule:
- keep exact 1.71.0 as the accepted baseline;
- do not silently upgrade to 2.0.0;
- any future 2.0 migration must be an explicit isolated compatibility stage.

See `Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.

## General anti-regression rule

Before proposing an old mod/config/patch as a fix, search:
- this file;
- `Current/06_RECENT_WORK_S1.32-S1.41.md`;
- `Current/03_PROJECT_CHRONOLOGY.md`;
- `Logs/`;
- `Archive/` only when historical reconstruction is actually needed.


## S1.42Q minimal native rollback supersession

The first post-S1.42P idea was to keep project-local Hawk-death finalization and add exact attacker-target identity plus dead-Hawk reacquisition filtering.

**Do not pursue that as the default next layer.**

The user explicitly chose the simpler architecture now implemented in S1.42Q:

- native LethalMin owns Pikmin -> enemy combat;
- native LethalMin owns enemy-death task completion;
- native LethalMin owns dead-body carry and Onion delivery;
- project-local code only blocks proven Enemy -> Pikmin gaps.

Therefore the custom target-identity/dead-Hawk-filter successor concept is superseded unless a clean S1.42Q native runtime proves that upstream LethalMin itself still fails with all project-local death-task code removed.

S1.42Q removes BaboonHawkDeathCleanup, project-local FinishTask death handling, the 4.0 m scan, and reflection-heavy post-grab repair rather than adding more lifecycle code.

Canonical plan:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`


## S1.42R exact upstream correction

S1.42Q proved that the remaining Pikmin-loss symptom was not caused by an external Hawk-death selector.

Exact LethalMinNightly 1.1.108 decompilation shows the real upstream defect:

`AttackEnemyTask.IntervaledUpdate()` returns while `IsPikminOnEnemy == true` **before** its existing dead-target check.

Therefore still-latched co-attackers cannot reach upstream `enemy.enemyScript.isEnemyDead -> FinishTaskServerRpc()`.

Do not regress to:
- proximity/radius death selection;
- Baboon-Hawk-specific death scans;
- global Pikmin/enemy scans;
- direct `RemoveCurrentTask()`;
- manual unlatch/leader restoration.

S1.42R uses the minimal exact bridge:
only a still-latched `AttackEnemyTask` whose **own target is already dead** requests native `PikminAI.FinishTaskServerRpc()`.

Evidence:
- `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
- `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
- `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
