# S1.42AI-DIAG1: installed V81 RoundManager source review

**Status:** CAPTURE_VERIFIED / NATIVE_ROUTE_REVIEW_PARTIAL / NOT_IMPLEMENTED / NOT_BUILD_READY
**Reviewed:** 2026-09-11
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`
**Patch safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Evidence boundary and verification

Original user capture commit: `fa7c090b075d84b6a2e9e8674aa19fea339c788e`.
Its single parent is repository main at capture:
`49337f84356c68a7a52ad3d3937d8b039ca1070a`.
That commit adds exactly the focused report and manifest retained in this directory;
it changes no existing files. Subsequent review files are separate from the original capture.

The report has 27 method blocks, including all 19 required names and eight additional
direct callers. Its header/signature list agrees exactly with the manifest; the
captured bodies are not reference-only throw-null stubs and remain within the
3000-line extraction cap.

Exact UTF-8 bytes, including CRLF, were rehashed after retrieval:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt | 43505 | 5317509a39e072db2c3df95de1cb9091dd9f7ff7e1a3bfe231045dea9cfc974f |
| MANIFEST.json | 7203 | 6aee2ac7700df0cfdddc419c88e6c547f0a8963b5b777ad5d36cf572cad1aa25 |

Git blob SHA-1 was independently recomputed for both files and matched GitHub.
The report SHA-256 matches its manifest. DLL/executable/app/build pins agree with
the prior MouthDogAI manifest, while the explicitly reviewed alternative Steam
manifest is recorded with `matches_prior_appmanifest = false`.
Decompiler identity is pinned ILSpy 11.0.0.9375.

The full type source and game binaries were intentionally not uploaded. Their
manifest hashes describe the helper's local capture; they cannot be independently
rehashed from this two-file upload. This is source evidence, not gameplay acceptance.

## Native route findings

The report's local type line numbers identify the original decompile positions,
not repository file line numbers. All types below refer to RoundManager.

| Exact declared surface | Observed responsibility | Isolation consequence |
| --- | --- | --- |
| `NetworkObjectReference SpawnEnemyGameObject(Vector3,float,int,EnemyType)` (2586) | Server directly instantiates, spawns NetworkObject and registers EnemyAI; explicit EnemyType precedes index selection | Exact species validation must cover explicit assets and all selector forms before instantiation. |
| `void SpawnEnemyOnServer(Vector3,float,int)` (2542), `void SpawnEnemyServerRpc(Vector3,float,int)` (2555) | Server call reaches SpawnEnemyGameObject; client route sends an owner-checked RPC whose server execution reaches the same method | Do not suppress the whole RPC lifecycle or infer that a client-side hook is sufficient. |
| `void SpawnEnemyFromVent(EnemyVent)` (2532) | Uses saved `vent.enemyTypeIndex`, then opens the vent and clears occupancy | Later list removal/reordering can invalidate queued identity. Blocking the whole vent method also loses native vent completion. |
| `bool SpawnRandomOutsideEnemy(float)` (2128) | Weighted selection, power/diversity bookkeeping, direct Instantiate + NetworkObject.Spawn and registration | This route bypasses SpawnEnemyGameObject. Prevention must precede power reservation/creation without blocking an allowed Shy Guy by location. |
| `bool SpawnRandomDaytimeEnemy(float)` (2053) | Independent daytime selection, departure-time eligibility, power accounting and direct spawn | Another bypass; returning failure ends the caller's current batch. |
| `bool SpawnRandomWeedEnemy(float,int)` (1979) | Uses independent `WeedEnemies`, weed power limit and direct spawn | A fourth pool exists beyond level indoor/outdoor/daytime lists. Three-list filtering is incomplete. |
| `void PredictAllOutsideEnemies()` (1591) | Server prediction modifies EnemyType spawn counters, selects nest owners and synchronizes nest order | It is not a spawn-only wrapper; preserve its bookkeeping/synchronization responsibilities. |
| `void SpawnNestObjectForOutsideEnemy(EnemyType,System.Random)` (1730) | Creates nest prefab, network-spawns it, registers EnemyAINestSpawnObject and increments nestsSpawned | Separate non-enemy-prefab infrastructure; its downstream spawn owner is not captured here. Do not equate it with a generic EnemyAI spawn or globally disable NetworkObjects. |
| `void PlotOutEnemiesForNextHour()` (2289) | Builds vent schedule, applies specialEnemyRarity override condition and calls AssignRandomEnemyToVent | The assignment method body is absent. Normal-list filtering alone does not establish special-override coverage. |
| `void SpawnEnemiesOutside()` (1931), `void SpawnDaytimeEnemiesOutside()` (2034), `void SpawnWeedEnemies()` (1955) | Batch wrappers call their corresponding bool selection/spawn method and break on false | Exact selection methods are narrower review surfaces than replacing the whole hourly lifecycle. |
| `void FinishGeneratingNewLevelClientRpc()` (1546), `void ResetEnemySpawningVariables()` (1851), `void BeginEnemySpawning()` (1914) | Loading/UI/doors, resets, prediction and initial schedule responsibilities | Do not skip these entire methods to obtain an empty round. |
| `void DespawnEnemyOnServer(NetworkObject)` (2626), `void DespawnEnemyServerRpc(NetworkObjectReference)` (2639), `void DespawnEnemyGameObject(NetworkObjectReference)` (2659) | Native RPC dispatch, registration removal, category power release, inside-spawn eligibility and network despawn | Preserve these paths. Post-spawn deletion is neither prevention nor a substitute for reviewing native accounting. |

The captured Update, SpawnInsideEnemiesFromVentsIfReady and
AdvanceHourAndSpawnNewBatchOfEnemies corroborate repeated scheduling and
server ownership. The generated spawn RPC handler checks sender ownership,
deserializes parameters and switches execution stage before invoking the RPC.

## Selector and state hazards

SpawnEnemyGameObject gives a non-null explicit EnemyType precedence over enemyNumber.
Without one, `-1` randomly selects an indoor entry, `-2` selects daytime, `-3`
selects outside, and other values are used as indoor indices. Those branches do
not themselves consult rarity or spawningDisabled. Zero weights therefore do not
prevent direct/random selector calls. The non-server early return also accesses
`currentLevel.Enemies[0]`; an empty indoor list is not safe for all callers.

A guard must not roll randomness twice, turn a denied enemy into a Shy Guy silently,
or assume that every consumer tolerates an invalid NetworkObjectReference. The
previous Scopophobia painting review already shows a consumer using the returned
ShyGuyAI. Empty pools, invalid indices, queued vents and return-value callers need
an explicit contract before implementation.

The outside/daytime/weed methods increment power before instantiation and then
update spawn counts. Cancelling at a later shared network-spawn point can leave
reserved power and created objects behind. Conversely, mutating shared EnemyType
spawningDisabled flags needs an owner/restoration and late-registration review;
this capture does not approve that approach.

Prediction reads level outside entries and may produce enemy-owned nests before
hourly enemy creation. The evidence does not contain EnemyAINestSpawnObject's
downstream lifecycle or AssignRandomEnemyToVent's assignment body. Their absence
must not be papered over with a global AI/component/network disable.

## Result and remaining work

The specific blocker "only reference-stub RoundManager bodies available" is resolved
for these 27 captured methods. This is not proof of all native or mod spawn paths,
complete inherited lifecycle coverage, or safe Harmony ordering.

Carry forward exact-package findings from
`SourceEvidence/ShyGuyIsolation/20260910T205433Z/REVIEW.md`:
BCMER direct queued spawns bypass the vanilla entry point; forced/side events bypass
simple enabled-config filtering; painting encounters do not prove BCMER execution.

Before coding, complete the bounded owner/coverage matrix for:
- remaining active mod spawn owners, including EnemyAI-derived Pikmin-family entities;
- native vent assignment/special override and nest downstream ownership;
- exact BCMER forced/side-event entry points and responsibilities;
- other patches on selected targets, default-off restoration and live Shy Guy identity;
- source-to-DLL equivalence and later archive/static/runtime gates.

An unexpected exterior Shy Guy must remain observable and fail the correction gate.
This review authorizes no blanket exterior shutdown and no cleanup that conceals it.
No new game run or source recapture is requested by this checkpoint.

Next: merge this reviewed capture after CI, then inventory the remaining active
mod spawn owners from exact S1.42AI package evidence and close the narrowly identified
coverage gaps. Build/runtime controllers and acceptance remain unchanged.
