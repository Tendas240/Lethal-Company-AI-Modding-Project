# S1.42AI-DIAG1 cross-assembly spawn-API consumer review

**Status:** EXACT INSTALLED-SET CROSS-ASSEMBLY CONSUMER REVIEW COMPLETE / BOTH NAMED CONSUMER GATES CLOSED / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Canonical main reviewed:** `8b4e6f832a6fee38dc92d17f491f4060f390e336`  
**Exact S1.42AI profile SHA-256:** `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
**Analysis branch:** `analysis/s142ai-cross-assembly-consumers`  
**Exact scan head:** `374595d45bbeee44b544ea4cf464111a51df150d`  
**Actions run:** `34715820639` — SUCCESS  
**Artifact:** `10304508813` / `s142ai-spawn-api-cross-consumer-review`  
**Artifact digest:** `sha256:733bb10b253372afe704c3c01e8c4852e9faf06c141c578d162db2e5cad55cd1`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope

Earlier exact reviews established two public/generic enemy-spawn providers whose own assemblies did not prove whether other enabled mods called them:

1. Snowlance-SnowyLib 1.13.1 exposes `NetworkHandler.SpawnEnemyRpc(...)` plus direct-position and vent `Utils.SpawnEnemy(...)` surfaces. Tier-A found no autonomous normal-stack caller inside SnowyLib; its debug `/spawnenemy` caller is testing-gated by a default-false config.
2. WhiteSpike-Interactive_Terminal_API 1.3.3 exposes `InteractiveTerminalAPI.Tools.SpawnMob(string, Vector3, int)`, which calls `RoundManager.SpawnEnemyOnServer`, but Tier-D found no internal caller in that assembly.

This review closes only the named **cross-assembly consumer** questions for the exact installed S1.42AI assembly set. It does not redefine the provider methods as harmless, does not authorize a broad patch on those shared libraries, and does not claim that arbitrary future package sets or dynamically generated reflection strings can never call them.

## Exact coverage and method

The repository-native scanner used the guarded S1.42AI `export.r2x` and `ProfileSources/S1.42AI/FILE_INDEX.json` as inventory authorities. Twelve parallel fail-closed shards re-downloaded every exact enabled Thunderstore package version and inspected every managed DLL. Shard 0 additionally inspected every embedded project DLL and required its bytes to match `FILE_INDEX.json`.

Coverage result:

- enabled package records scanned: **183**;
- embedded project DLLs scanned: **5**;
- managed DLLs scanned: **224**;
- raw provider/method-marker candidate assemblies: **3**;
- external raw candidate assemblies after excluding the two provider assemblies themselves: **1**.

The scan searched managed metadata/IL for the exact provider identities and spawn method names, then fully decompiled every candidate to C# and IL with pinned ILSpy. Direct-call contexts and reflection-like contexts were preserved. The aggregate job failed closed unless all 183 enabled package records and all five embedded DLLs were covered exactly as expected.

## SnowyLib result

Exact provider identity remains the Tier-A byte identity:

- package: `Snowlance-SnowyLib` 1.13.1;
- package ZIP SHA-256: `60c64b5df528d62491b7f584d8ec3d14c41c9c3cd46b8d9c3fb1f6e230dec95b`;
- DLL: `Snowlance.SnowyLib.dll`;
- DLL SHA-256: `cdbb80c8b0afa3e65acae83e25bd00fb704cefbeb2e14ccc561f1d959b0c3c95`;
- complete source SHA-256: `0b9b13fdc95cfb827eb5de2cdbd3ba94b6405d315af29e5ba1b13210f1e68d36`;
- IL SHA-256: `a41e3b0d9d050f070345e9dce2cef3ef4f5e8b69eb87848bbb58b504ef064e7e`.

Across the exact installed S1.42AI assembly set the aggregate found:

- external assemblies directly calling a SnowyLib spawn API: **0**;
- external SnowyLib reflection-like spawn-API candidates: **0**.

The provider self-capture still shows only SnowyLib's own expected internal/generated RPC handling and debug-command vent calls described by Tier-A; those are not cross-assembly consumers.

**Classification:** `EXACT_S142AI_INSTALLED_SET_NO_EXTERNAL_SNOWYLIB_SPAWN_API_CONSUMER_FOUND`.

**Gate result:** the SnowyLib cross-assembly consumer gate is **CLOSED for the exact S1.42AI installed static assembly set**. The public APIs remain real creation surfaces; this finding means no additional installed external owner path through them was found that requires separate DIAG1 interception coverage.

## InteractiveTerminalAPI SpawnMob result

Exact provider identity remains the Tier-D byte identity:

- package: `WhiteSpike-Interactive_Terminal_API` 1.3.3;
- package ZIP SHA-256: `dcb969e1ea831a4c3e56320f7f395eea875a9d41d47f4e355529d8bb516f277c`;
- DLL: `BepInEx/plugins/InteractiveTerminalAPI/InteractiveTerminalAPI.dll`;
- DLL SHA-256: `981c2874ab1af36b06b5ca18a171d521f1d25694fce7764cfa1058da03c4ff77`;
- complete source SHA-256: `7987671896805623c023d3a868e79d21fd6b7ab23147e66ce81460636580b793`;
- IL SHA-256: `47a0cd88370bd42b1c148eac545122bc8e11120ff0fed5c1b7636d8c67f81bbb`.

Four enabled packages declare an Interactive Terminal API dependency: ProjectSCP PSCPLibrary, ShipWindows, Lategame Upgrades and MisideItems. Dependency declaration is not treated as a spawn-call proof.

The only external raw candidate assembly was `malco-Lategame_Upgrades` 3.14.1 / `MoreShipUpgrades.dll`. Its exact bytes reproduce the already canonical Tier-A identity:

- package ZIP SHA-256: `8ffa3a987e2626526406673825d5523a044e6e6cf68581edba844b24f2f2c79a`;
- DLL SHA-256: `c3c6da8a2ad57930ec91db9df24223379a27bd0e0dcc60cf21fb1c9472f20465`;
- complete source SHA-256: `c027768e0b850573fb6ef4b90d86bd89baa557f739a91371fd49d30e6d86961a`;
- IL SHA-256: `b5b9bcedbf1f8231540944dba575038028c6a28c459caf2f2b6452574de71025`.

The full exact IL resolves all three `SpawnMob` call instructions to **its own** `MoreShipUpgrades.Misc.Util.Tools::SpawnMob` at IL lines 44703, 44727 and 51948. It contains **zero** calls to `InteractiveTerminalAPI.Util.Tools::SpawnMob` and **zero** SnowyLib spawn calls. Its InteractiveTerminalAPI references belong to UI/application infrastructure.

Across the full installed set the aggregate therefore found:

- external assemblies directly calling `InteractiveTerminalAPI.Tools.SpawnMob`: **0**;
- external InteractiveTerminalAPI SpawnMob reflection-like candidates: **0**.

**Classification:** `EXACT_S142AI_INSTALLED_SET_NO_EXTERNAL_INTERACTIVE_TERMINAL_SPAWNMOB_CONSUMER_FOUND`.

**Gate result:** the InteractiveTerminalAPI `SpawnMob` cross-assembly consumer gate is **CLOSED for the exact S1.42AI installed static assembly set**.

## Patch-safety consequence

These closures remove two uncertainty branches; they do **not** make either provider a preferred interception surface. SnowyLib and InteractiveTerminalAPI are shared public infrastructure, and broad callee suppression remains contrary to `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` when the unwanted behavior can be stopped at narrower reviewed owner decisions.

The exact installed-set scan also does not invalidate the already confirmed direct Lategame Upgrades owner path: its own `MoreShipUpgrades.Misc.Util.Tools.SpawnMob` still calls `RoundManager.SpawnEnemyOnServer` and retains the Tier-A caller/return-semantics obligations. This review only proves that those three call sites do not route through InteractiveTerminalAPI or SnowyLib.

Static analysis can prove the captured IL references and static reflection-like markers present in these exact binaries. It cannot mathematically rule out a method name assembled entirely at runtime and invoked reflectively. No such static indicator was found in the installed set. Any package/version/profile change after S1.42AI must reopen this installed-set consumer conclusion rather than inheriting it blindly.

## Remaining gates

The 53-package discovery-positive exact-review inventory is already complete, and these two named public-API consumer gates are now closed. Patch safety remains **PARTIAL / NOT_BUILD_READY** because the remaining bounded work is still:

1. close the exact BCMER forced / forced-side / additional / runtime-custom event execution gate;
2. preserve/verify exact Shy Guy runtime identity and the project source-to-DLL provenance needed by the final narrow prevention design;
3. select and statically validate the smallest host/client-safe interception points across the already reviewed owner paths.

No DIAG1 implementation, profile build, build-controller transition, runtime-controller transition, Gale import or gameplay test is authorized by this review. `S1.42AI-DIAG1` remains `PLANNED_NOT_BUILT / NOT_BUILD_READY`.
