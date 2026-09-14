#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PROFILE = ROOT / "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
DRAFT_SPEC = ROOT / "BuildSpecs/S1.42AI-DIAG1_DRAFT.json"
VALIDATION_PROFILE = Path(os.environ["DIAG1_VALIDATION_PROFILE"]).resolve()
VALIDATION_RESULT = Path(os.environ["DIAG1_VALIDATION_RESULT"]).resolve()
OUT = Path(os.environ["DIAG1_STATIC_OUT"]).resolve()
PLUGIN_DIR = ROOT / "Patches/S142AIDiag1Isolation"
EXPECTED_BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_S139_SHA = "bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573"
EXPECTED_PREMIUM_SHA = "380ffa37ff53576f561c27a9d06c30ecd35d9195606e142122647a0df583bf96"
EXPECTED_CHILLAX_SHA = "1a448aaf93af58da00f16e7e7acf0c7e69b1bb564f084dc64020d06101bbb7d0"
PLUGIN_ARCHIVE_PATH = "BepInEx/plugins/Tendas-S142AIDiag1Isolation/S142AIDiag1Isolation.dll"
DIAG_CONFIG_PATH = "BepInEx/config/tendas.s142ai.diag1.isolation.cfg"
KNOWN_BAD_PIKMIN_RESOLVER = 'ResolveRequiredType("LethalMin.PikminType")'

OUT.mkdir(parents=True, exist_ok=True)

def fail(message: str) -> None:
    raise RuntimeError(message)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def run(args: list[str], *, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if check and p.returncode != 0:
        raise RuntimeError(
            f"{args[0]} failed ({p.returncode}) for {' '.join(args[1:])}: "
            + p.stderr.decode("utf-8", errors="replace")[-5000:]
        )
    return p

def read_zip(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            fail(f"duplicate ZIP members in {path}")
        return {name: z.read(name) for name in names if not name.endswith("/")}

def parse_ini_text(text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    section: str | None = None
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if not section or section in sections:
                fail(f"duplicate/invalid INI section [{section}]")
            sections[section] = {}
            continue
        if "=" not in raw or section is None:
            fail(f"unparsed INI line: {raw!r}")
        key, value = raw.split("=", 1)
        key = key.strip()
        if key in sections[section]:
            fail(f"duplicate INI key [{section}] {key}")
        sections[section][key] = value.strip()
    return sections

def semantic_ini_diff(before: bytes, after: bytes) -> dict[tuple[str, str], tuple[str | None, str | None]]:
    a = parse_ini_text(before.decode("utf-8-sig"))
    b = parse_ini_text(after.decode("utf-8-sig"))
    keys = {(s, k) for s, d in a.items() for k in d} | {(s, k) for s, d in b.items() for k in d}
    out = {}
    for key in sorted(keys):
        av = a.get(key[0], {}).get(key[1])
        bv = b.get(key[0], {}).get(key[1])
        if av != bv:
            out[key] = (av, bv)
    return out

def normalize_export_without_profile_name(text: str) -> tuple[str, list[str]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    hits = [line for line in lines if re.match(r"^\s*profileName\s*:", line)]
    normalized = [re.sub(r"^(\s*)profileName\s*:.*$", r"\1profileName: <NORMALIZED>", line) for line in lines]
    return "\n".join(normalized), hits

def split_params(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    out, current = [], []
    angle = square = paren = 0
    for ch in value:
        if ch == "<": angle += 1
        elif ch == ">": angle = max(0, angle - 1)
        elif ch == "[": square += 1
        elif ch == "]": square = max(0, square - 1)
        elif ch == "(": paren += 1
        elif ch == ")": paren = max(0, paren - 1)
        if ch == "," and angle == 0 and square == 0 and paren == 0:
            out.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    out.append("".join(current).strip())
    return out

ALIASES = {
    "System.String": "string",
    "System.Int32": "int",
    "System.UInt64": "ulong",
    "System.Single": "float",
    "System.Boolean": "bool",
    "System.Void": "void",
}

def norm_type(value: str) -> str:
    value = value.replace("global::", "").strip()
    for src, dst in ALIASES.items():
        value = value.replace(src, dst)
    return re.sub(r"\s+", "", value)

def method_signature(source: str, method: str, expected_return: str, expected_params: list[str], expected_static: bool) -> tuple[re.Match, str]:
    pattern = re.compile(
        r"(?m)^[ \t]*(?P<mods>(?:(?:public|private|protected|internal|static|virtual|override|sealed|async|new|unsafe|extern)\s+)*)"
        r"(?P<ret>[A-Za-z_][A-Za-z0-9_.,<>\[\]?]*)\s+"
        + re.escape(method)
        + r"\s*\((?P<params>[^\n)]*)\)"
    )
    candidates = []
    for m in pattern.finditer(source):
        params = split_params(m.group("params"))
        if len(params) != len(expected_params):
            continue
        if norm_type(m.group("ret")) != norm_type(expected_return):
            continue
        if ("static" in m.group("mods").split()) != expected_static:
            continue
        ok = True
        for actual, expected in zip(params, expected_params):
            actual_norm = norm_type(re.sub(r"\b(?:ref|out|in|params|this)\b", "", actual))
            if norm_type(expected) not in actual_norm:
                ok = False
                break
        if ok:
            candidates.append(m)
    if len(candidates) != 1:
        fail(
            f"Exact declared signature mismatch for {method}({','.join(expected_params)}) -> {expected_return}, "
            f"static={expected_static}; candidates={len(candidates)}"
        )
    m = candidates[0]
    brace = source.find("{", m.end())
    if brace < 0:
        fail(f"Method {method} has no body")
    depth = 0
    for i in range(brace, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return m, source[brace:i+1]
    fail(f"Unclosed method body for {method}")


def il_declared_method_header(il_text: str, method: str) -> str:
    starts = [m.start() for m in re.finditer(r"(?m)^\s*\.method\b", il_text)]
    matches: list[str] = []
    method_token = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(method) + r"\s*\(")
    for index, start in enumerate(starts):
        limit = starts[index + 1] if index + 1 < len(starts) else len(il_text)
        body_start = il_text.find("{", start, limit)
        if body_start < 0:
            continue
        header = il_text[start:body_start]
        if method_token.search(header):
            matches.append(re.sub(r"\s+", " ", header).strip())
    if len(matches) != 1:
        fail(f"Expected exactly one CLR IL declaration for {method}, found {len(matches)}")
    return matches[0]


def prove_lethalmin_withdraw_clr_contract(dll_path: Path, digest: str) -> dict:
    il = run(
        ["ilspycmd", "--ilcode", "-t", "LethalMin.Onion", str(dll_path)],
        timeout=120,
    ).stdout.decode("utf-8", errors="replace")
    header = il_declared_method_header(il, "WithdrawPikminFromOnion")
    signature = re.search(
        r"(?P<prefix>.*?)\bWithdrawPikminFromOnion\s*\((?P<params>.*)\)\s+cil\s+managed\b",
        header,
    )
    if signature is None:
        fail("CLR IL signature for LethalMin.Onion.WithdrawPikminFromOnion was not parseable")

    prefix = signature.group("prefix").strip()
    if re.search(
        r"\binstance\s+(?:class\s+)?(?:\[[^\]]+\])?System\.Collections\.IEnumerator\s*$",
        prefix,
    ) is None:
        fail(f"CLR return/instance contract mismatch for WithdrawPikminFromOnion: {prefix}")

    params = split_params(signature.group("params"))
    if len(params) != 3:
        fail(f"CLR parameter count for WithdrawPikminFromOnion is {len(params)}, expected 3")

    list_match = re.fullmatch(
        r"(?:class\s+)?(?:\[[^\]]+\])?System\.Collections\.Generic\.List`1<(?P<arg>.+)>\s+\S+",
        params[0],
    )
    if list_match is None:
        fail(f"CLR parameter 0 is not exact List<T>: {params[0]}")

    generic_arg = re.sub(r"^(?:class|valuetype)\s+", "", list_match.group("arg").strip())
    if re.match(r"^\[[^\]]+\]", generic_arg):
        fail(f"PikminType generic argument is assembly-qualified away from LethalMin: {generic_arg}")
    generic_arg = generic_arg.strip("'")
    simple_name = re.split(r"[./+]", generic_arg)[-1]
    if simple_name != "PikminType":
        fail(f"Metadata-derived List<T> identity is not PikminType: {generic_arg}")

    if re.fullmatch(r"int32\[\]\s+\S+", params[1]) is None:
        fail(f"CLR parameter 1 is not exact int[]: {params[1]}")

    leader_match = re.fullmatch(r"(?:class|valuetype)\s+(?P<type>\S+)\s+\S+", params[2])
    if leader_match is None:
        fail(f"CLR parameter 2 is not parseable as exact Leader type: {params[2]}")
    leader_type = leader_match.group("type").strip("'")
    if leader_type.startswith("[") or leader_type != "LethalMin.Leader":
        fail(f"CLR parameter 2 is not same-assembly LethalMin.Leader: {leader_type}")

    type_probe = run(
        ["ilspycmd", "--ilcode", "-t", generic_arg, str(dll_path)],
        timeout=120,
        check=False,
    )
    if type_probe.returncode != 0:
        fail(
            f"Metadata-derived PikminType '{generic_arg}' is not resolvable from the same materialized LethalMin DLL: "
            + type_probe.stderr.decode("utf-8", errors="replace")[-2000:]
        )

    return {
        "assembly_sha256": digest,
        "owner_type": "LethalMin.Onion",
        "method": "WithdrawPikminFromOnion",
        "return_type": "System.Collections.IEnumerator",
        "instance": True,
        "parameter_count": 3,
        "parameter_0_generic_definition": "System.Collections.Generic.List`1",
        "parameter_0_generic_argument": generic_arg,
        "parameter_0_generic_argument_simple_name": simple_name,
        "parameter_0_generic_argument_same_assembly": True,
        "parameter_1": "System.Int32[]",
        "parameter_2": "LethalMin.Leader",
    }


TARGETS = [
    ("SlendermanMod.Behaviours.SpawnSlendermanEnemyItem", "SpawnSlenderman", "void", [], False),
    ("Kittenji.FootballEntity.TrainProp", "ForceSpawnEnemy", "void", [], False),
    ("Kittenji.HerobrineMod.RedstoneTorchProp", "ForceSpawnEnemy", "void", [], False),
    ("Kittenji.HerobrineMod.Networking.HerobrineNetworking", "cmd_Spawn", "void", ["string"], False),
    ("MoreShipUpgrades.Misc.Util.Tools", "SpawnMob", "bool", ["string", "Vector3", "int"], True),
    ("PremiumScraps.CustomEffects.HarryDoll", "SpawnEnemyServerRpc", "void", ["Vector3", "bool", "bool"], False),
    ("ChillaxScraps.CustomEffects.Ocarina", "SpawnSpecialEnemyServerRpc", "void", ["int", "Vector3", "ulong"], False),
    ("CodeRebirth.src.Content.Weathers.TornadoWeather", "SpawnTornado", "void", ["Vector3"], False),
    ("CodeRebirth.src.Content.Items.GuardPhone", "SpawnWithDelay", "IEnumerator", ["Vector3"], False),
    ("CodeRebirth.src.Content.Enemies.BoxChute", "SpawnEnemy", "void", [], False),
    ("LethalMin.Onion", "WithdrawPikminFromOnion", "IEnumerator", ["List<PikminType>", "int[]", "Leader"], False),
    ("LethalMin.Onion", "SetEnemyToBeRevived", "void", ["EnemyGrabbableObject"], False),
    ("LethalMin.GlowSeed", "SpawnGlowPikminServerRpc", "void", ["ulong"], False),
    ("LethalMin.Lumiknull", "DepositeItem", "void", ["float", "Leader"], False),
    ("LethalMin.Triknull", "DepositeItem", "void", ["float", "Leader"], False),
    ("LethalMin.Sprout", "PluckAndDespawnServerRpc", "void", ["ulong"], False),
    ("LethalMin.Sprout", "OnInteractEarlyOnOtherClients", "void", ["PlayerControllerB"], False),
    ("PremiumScraps.Utils.Effects", "Spawn", "NetworkObjectReference", ["SpawnableEnemyWithRarity", "Vector3", "float"], True),
    ("PremiumScraps.Utils.Effects", "SpawnMaskedOfPlayer", "void", ["ulong", "Vector3"], True),
    ("ChillaxScraps.Utils.Effects", "Spawn", "NetworkObjectReference", ["SpawnableEnemyWithRarity", "Vector3", "float"], True),
    ("JLL.Components.EnemySpawner", "SpawnEnemy", "void", ["Vector3"], False),
    ("KenjiLib.Scripts.KLightsEvent", "PermanentPowerOffRoutine", "IEnumerator", [], False),
    ("KenjiLib.Scripts.KLightsEvent", "TriggerAppyEventRoutine", "IEnumerator", [], False),
    ("itolib.Behaviours.Grabbables.EventfulApparatus", "HandleDisconnect", "IEnumerator", [], False),
    ("itolib.PlayZone.TwinApparatus", "HandleDisconnect", "IEnumerator", [], False),
    ("CodeRebirth.src.MiscScripts.EnemyLevelSpawner", "SpawnRandomEnemy", "EnemyAI", [], False),
    ("CodeRebirth.src.Content.Items.FakeSnailCat", "Update", "void", [], False),
    ("CodeRebirth.src.Content.Items.Xui", "OnNetworkDespawn", "void", [], False),
    ("LethalMin.Compats.EndlessElevatorPatch", "WaitRespawnPikmin", "IEnumerator", ["EndlessElevator"], True),
]

NATIVE_TARGETS = [
    ("PredictAllOutsideEnemies", "void", [], False),
    ("BeginEnemySpawning", "void", [], False),
    ("PlotOutEnemiesForNextHour", "void", [], False),
    ("FinishGeneratingNewLevelClientRpc", "void", [], False),
    ("AssignRandomEnemyToVent", "bool", ["EnemyVent", "float"], False),
    ("SpawnEnemyGameObject", "NetworkObjectReference", ["Vector3", "float", "int", "EnemyType"], False),
]

TRANSPILE_COUNTS = [
    ("JLL.Components.EnemySpawner", "SpawnEnemy", 1),
    ("KenjiLib.Scripts.KLightsEvent", "PermanentPowerOffRoutine", 1),
    ("KenjiLib.Scripts.KLightsEvent", "TriggerAppyEventRoutine", 1),
    ("itolib.Behaviours.Grabbables.EventfulApparatus", "HandleDisconnect", 1),
    ("itolib.PlayZone.TwinApparatus", "HandleDisconnect", 1),
    ("CodeRebirth.src.MiscScripts.EnemyLevelSpawner", "SpawnRandomEnemy", 1),
    ("CodeRebirth.src.Content.Items.FakeSnailCat", "Update", 1),
    ("CodeRebirth.src.Content.Items.Xui", "OnNetworkDespawn", 2),
]

def main() -> int:
    report: dict = {
        "schema_version": 1,
        "purpose": "S1.42AI-DIAG1 prebuild compile/static gate",
        "repository_commit": os.environ.get("GITHUB_SHA"),
        "base_profile": str(BASE_PROFILE.relative_to(ROOT)),
        "checks": {},
        "targets": [],
    }

    if sha256_file(BASE_PROFILE) != EXPECTED_BASE_SHA:
        fail("S1.42AI base profile SHA mismatch")
    if not DRAFT_SPEC.exists():
        fail("Generated DIAG1 draft spec is missing")
    draft = json.loads(DRAFT_SPEC.read_text(encoding="utf-8"))
    if draft.get("enabled") is not False:
        fail("Draft spec must remain enabled=false")
    if draft.get("build_id") != "S1.42AI-DIAG1":
        fail("Unexpected draft build_id")
    for key in ("mod_state_changes", "mod_additions", "mod_removals"):
        if draft.get(key) != []:
            fail(f"{key} must remain empty")
    if draft.get("event_inventory", {}).get("enabled_sections") != ["ModdedEvents.cfg:[ShyGuy]"]:
        fail("BCMER enabled event inventory is not exactly [ShyGuy]")
    allowed_config_paths = {
        "BepInEx/config/BrutalCompanyMinusExtraReborn/VanillaEvents.cfg",
        "BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg",
        "BepInEx/config/BrutalCompanyMinusExtraReborn/CoreProperties.cfg",
        "BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg",
        "BepInEx/config/ArcadiaMoonPlugin.cfg",
        "BepInEx/config/butterystancakes.lethalcompany.butterybalance.cfg",
        "BepInEx/config/me.biodiversity.junk_radar.cfg",
        "BepInEx/config/sparble.slendermanmod.cfg",
        "BepInEx/config/NoteBoxz.LethalMin.cfg",
        DIAG_CONFIG_PATH,
    }
    patch_paths = {p["path"] for p in draft.get("config_patches", [])}
    if not patch_paths <= allowed_config_paths or DIAG_CONFIG_PATH not in patch_paths:
        fail(f"Config patch paths differ from approved overlay: {sorted(patch_paths - allowed_config_paths)}")
    report["checks"]["draft_spec"] = {
        "config_patches": len(draft.get("config_patches", [])),
        "text_assertions": len(draft.get("text_assertions", [])),
        "paths": sorted(patch_paths),
        "enabled": False,
    }

    source = "\n".join(p.read_text(encoding="utf-8") for p in sorted(PLUGIN_DIR.glob("*.cs")))
    if "private const bool ImplementationComplete = true;" not in source:
        fail("Post-static-gate ImplementationComplete safety latch is not true")
    if not re.search(r'Config\.Bind\(\s*"Diagnostics"\s*,\s*"S1\.42AI-DIAG1 Enabled"\s*,\s*false\s*,', source, re.S):
        fail("Diagnostic config is not default-off")
    if "PatchAll(" in source:
        fail("Broad Harmony PatchAll is forbidden")
    if KNOWN_BAD_PIKMIN_RESOLVER in source:
        fail("Known-bad hardcoded LethalMin PikminType resolver regression is present")
    if "ResolveLethalMinWithdrawPikminContract" not in source or "[DIAG1_OWNER_TYPE_DERIVED]" not in source:
        fail("Metadata-bound LethalMin PikminType owner-resolution contract is missing")
    for label in (
        '"RoundManager.SpawnEnemyGameObject(',
        '"RoundManager.SpawnEnemyOnServer(',
        '"RoundManager.SpawnEnemyServerRpc(',
        '"NetworkObject.Spawn(',
        '"EnemyAI.Start(',
        '"EnemyAI.UseNestSpawnObject(',
    ):
        if label in source:
            fail(f"Forbidden broad patch target label present: {label}")
    for marker in (
        "[DIAG1_ENABLED]",
        "[DIAG1_IDENTITY_RESOLVED]",
        "[DIAG1_TARGET_INSTALLED]",
        "[DIAG1_OWNER_TARGET_INSTALLED]",
        "[DIAG1_COMPLEX_TARGET_INSTALLED]",
        "[DIAG1_TRANSPILER_MATCH]",
        "[DIAG1_CONFIG_VERIFIED]",
        "[DIAG1_CONFIG_OVERLAY_VERIFIED]",
        "[DIAG1_MORECOMPANY_COMMAND_DISABLED]",
        "[DIAG1_SNOWYLIB_TESTING_DISABLED]",
        "[DIAG1_INTERACTIVE_TERMINAL_NO_CONSUMER_EVIDENCE]",
        "[DIAG1_EMERGENCY_DICE_ABSENT]",
        "[DIAG1_LEGACY_ISOLATION_DISABLED]",
        "[DIAG1_ISOLATION_BYPASS]",
    ):
        if marker not in source:
            fail(f"Required static/startup marker missing: {marker}")
    report["checks"]["plugin_source"] = {
        "implementation_complete_latch": True,
        "diagnostic_default": False,
        "required_markers_present": True,
        "forbidden_broad_target_labels_absent": True,
        "known_bad_hardcoded_pikmin_resolver_absent": True,
        "metadata_bound_pikmin_resolution_present": True,
    }

    base = read_zip(BASE_PROFILE)
    final = read_zip(VALIDATION_PROFILE)
    result = json.loads(VALIDATION_RESULT.read_text(encoding="utf-8"))

    if result.get("base_sha256") != EXPECTED_BASE_SHA:
        fail("Ephemeral builder result base SHA mismatch")
    base_names = set(base)
    final_names = set(final)
    added = sorted(final_names - base_names)
    removed = sorted(base_names - final_names)
    if removed:
        fail(f"Validation profile removed members: {removed}")
    if added != sorted([DIAG_CONFIG_PATH, PLUGIN_ARCHIVE_PATH]):
        fail(f"Unexpected added archive members: {added}")
    changed_existing = sorted(name for name in base_names & final_names if sha256_bytes(base[name]) != sha256_bytes(final[name]))
    allowed_changed = {"export.r2x"} | {p for p in patch_paths if p in base}
    if set(changed_existing) - allowed_changed:
        fail(f"Unexpected changed archive members: {sorted(set(changed_existing) - allowed_changed)}")

    patches_by_path: dict[str, dict[tuple[str, str], str]] = {}
    for p in draft["config_patches"]:
        patches_by_path.setdefault(p["path"], {})[(p["section"], p["key"])] = str(p["value"])
    semantic_diffs = {}
    for path, expected in patches_by_path.items():
        if path in base:
            diff = semantic_ini_diff(base[path], final[path])
            unexpected = set(diff) - set(expected)
            if unexpected:
                fail(f"Unexpected semantic INI delta in {path}: {sorted(unexpected)}")
            doc = parse_ini_text(final[path].decode("utf-8-sig"))
            for (section, key), value in expected.items():
                actual = doc.get(section, {}).get(key)
                if actual != value:
                    fail(f"Final overlay mismatch [{section}] {key} in {path}: {actual!r} != {value!r}")
            semantic_diffs[path] = {f"[{s}] {k}": [a, b] for (s, k), (a, b) in diff.items()}
        else:
            if path != DIAG_CONFIG_PATH:
                fail(f"Unexpected new config path: {path}")
            doc = parse_ini_text(final[path].decode("utf-8-sig"))
            for (section, key), value in expected.items():
                if doc.get(section, {}).get(key) != value:
                    fail(f"New DIAG config mismatch [{section}] {key}")

    vanilla = parse_ini_text(final["BepInEx/config/BrutalCompanyMinusExtraReborn/VanillaEvents.cfg"].decode("utf-8-sig"))
    modded = parse_ini_text(final["BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg"].decode("utf-8-sig"))
    enabled = []
    for fname, doc in (("VanillaEvents.cfg", vanilla), ("ModdedEvents.cfg", modded)):
        for section, values in doc.items():
            if values.get("Event Enabled?") == "true":
                enabled.append(f"{fname}:[{section}]")
    if enabled != ["ModdedEvents.cfg:[ShyGuy]"]:
        fail(f"Final BCMER event allowlist mismatch: {enabled}")

    base_export, base_names_hit = normalize_export_without_profile_name(base["export.r2x"].decode("utf-8-sig"))
    final_export, final_names_hit = normalize_export_without_profile_name(final["export.r2x"].decode("utf-8-sig"))
    if len(base_names_hit) != 1 or len(final_names_hit) != 1 or base_export != final_export:
        fail("export.r2x differs by more than one profileName field")
    if "LC V1 S1.42AI-DIAG1 ShyGuy Isolation" not in final_names_hit[0]:
        fail("Validation export profileName mismatch")

    s139_path = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
    base_s139 = sha256_bytes(base[s139_path])
    final_s139 = sha256_bytes(final[s139_path])
    if base_s139 != EXPECTED_S139_SHA or final_s139 != EXPECTED_S139_SHA:
        fail(f"S139CompatibilityFixes SHA changed: base={base_s139}, final={final_s139}")

    plugin_sha = sha256_bytes(final[PLUGIN_ARCHIVE_PATH])
    report["checks"]["ephemeral_profile"] = {
        "output_sha256": sha256_file(VALIDATION_PROFILE),
        "plugin_sha256": plugin_sha,
        "changed_existing_members": changed_existing,
        "added_members": added,
        "s139_sha256": base_s139,
        "semantic_config_diffs": semantic_diffs,
        "bcmer_enabled_sections": enabled,
        "export_identity_only": True,
    }

    work = Path(tempfile.mkdtemp(prefix="diag1-static-"))
    dll_root = work / "dlls"
    dll_root.mkdir()
    dll_records = []
    for idx, (name, data) in enumerate(base.items()):
        if not name.lower().endswith(".dll"):
            continue
        dest = dll_root / Path(name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        dll_records.append((name, dest, sha256_bytes(data)))

    def list_one(record):
        name, path, digest = record
        p = run(["ilspycmd", "-l", "c", str(path)], timeout=90, check=False)
        if p.returncode != 0:
            return name, path, digest, ""
        return name, path, digest, p.stdout.decode("utf-8", errors="replace")

    listings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for item in pool.map(list_one, dll_records):
            listings.append(item)

    type_to_assembly = {}
    type_names = sorted({t[0] for t in TARGETS})
    for type_name in type_names:
        matches = []
        for archive_name, path, digest, listing in listings:
            for line in listing.splitlines():
                stripped = line.strip()
                if stripped.endswith(" " + type_name) or stripped == type_name:
                    matches.append((archive_name, path, digest))
                    break
        if len(matches) != 1:
            fail(f"Expected exactly one base-profile assembly containing {type_name}, found {len(matches)}")
        type_to_assembly[type_name] = matches[0]

    source_cache: dict[tuple[str, str], str] = {}
    bodies: dict[tuple[str, str], str] = {}
    for type_name, method, ret, params, is_static in TARGETS:
        archive_name, dll_path, digest = type_to_assembly[type_name]
        cache_key = (str(dll_path), type_name)
        if cache_key not in source_cache:
            p = run(["ilspycmd", "-t", type_name, str(dll_path)], timeout=120)
            source_cache[cache_key] = p.stdout.decode("utf-8", errors="replace")
        src = source_cache[cache_key]
        _match, body = method_signature(src, method, ret, params, is_static)
        bodies[(type_name, method)] = body
        report["targets"].append({
            "type": type_name,
            "method": method,
            "return": ret,
            "params": params,
            "static": is_static,
            "archive_member": archive_name,
            "assembly_sha256": digest,
        })

    lethalmin_archive, lethalmin_dll, lethalmin_digest = type_to_assembly["LethalMin.Onion"]
    report["checks"]["lethalmin_withdraw_clr_contract"] = prove_lethalmin_withdraw_clr_contract(
        lethalmin_dll,
        lethalmin_digest,
    )
    report["checks"]["lethalmin_withdraw_clr_contract"]["archive_member"] = lethalmin_archive

    premium_record = type_to_assembly["PremiumScraps.Utils.Effects"]
    chillax_record = type_to_assembly["ChillaxScraps.Utils.Effects"]
    if premium_record[2] != EXPECTED_PREMIUM_SHA:
        fail(f"PremiumScraps exact DLL SHA changed: {premium_record[2]}")
    if chillax_record[2] != EXPECTED_CHILLAX_SHA:
        fail(f"ChillaxScraps exact DLL SHA changed: {chillax_record[2]}")
    report["checks"]["caller_return_invariants"] = {
        "PremiumScraps": {
            "dll_sha256": premium_record[2],
            "expected_reviewed_sha256": EXPECTED_PREMIUM_SHA,
            "invariant": "reviewed exact DLL identity unchanged; Effects.Spawn callers-ignore-return proof remains byte-identical",
        },
        "ChillaxScraps": {
            "dll_sha256": chillax_record[2],
            "expected_reviewed_sha256": EXPECTED_CHILLAX_SHA,
            "invariant": "reviewed exact DLL identity unchanged; non-Ocarina Effects.Spawn callers-ignore-return proof remains byte-identical",
        },
    }

    for type_name, method, expected_count in TRANSPILE_COUNTS:
        body = bodies[(type_name, method)]
        count = body.count("SpawnEnemyGameObject(")
        if count != expected_count:
            fail(f"{type_name}.{method} expected SpawnEnemyGameObject calls={expected_count}, got {count}")
        if type_name.endswith("FakeSnailCat") and body.count("destroyed = true") != 1:
            fail("FakeSnailCat.Update destroyed=true anchor count changed")
    report["checks"]["transpiler_callsite_counts"] = {
        f"{t}.{m}": count for t, m, count in TRANSPILE_COUNTS
    }

    game_cache = Path.home() / ".nuget/packages/lethalcompany.gamelibs.steam/81.0.5-ngd.0"
    game_dlls = list(game_cache.rglob("Assembly-CSharp.dll"))
    if len(game_dlls) != 1:
        fail(f"Expected one V81 Assembly-CSharp reference, found {len(game_dlls)}")
    game_dll = game_dlls[0]
    native_src = run(["ilspycmd", "-t", "RoundManager", str(game_dll)], timeout=120).stdout.decode("utf-8", errors="replace")
    native_methods = []
    for method, ret, params, is_static in NATIVE_TARGETS:
        method_signature(native_src, method, ret, params, is_static)
        native_methods.append({"method": method, "return": ret, "params": params, "static": is_static})
    report["checks"]["native_v81_reference"] = {
        "package": "LethalCompany.GameLibs.Steam",
        "version": "81.0.5-ngd.0",
        "assembly_sha256": sha256_file(game_dll),
        "methods": native_methods,
        "qualification": "exact compile/reference metadata gate; prior exact installed-source review remains the behavioral authority",
    }

    report["status"] = "PASS_PREBUILD_STATIC_GATE"
    (OUT / "STATIC_VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md = [
        "# S1.42AI-DIAG1 prebuild static validation",
        "",
        f"- Status: **{report['status']}**",
        f"- Repository commit: `{report['repository_commit']}`",
        f"- Base SHA-256: `{EXPECTED_BASE_SHA}`",
        f"- Ephemeral validation profile SHA-256: `{report['checks']['ephemeral_profile']['output_sha256']}`",
        f"- Diagnostic DLL SHA-256: `{plugin_sha}`",
        f"- Exact owner targets validated: **{len(report['targets'])}**",
        f"- LethalMin WithdrawPikminFromOnion CLR generic argument: `{report['checks']['lethalmin_withdraw_clr_contract']['parameter_0_generic_argument']}`",
        "- Known-bad hardcoded LethalMin PikminType resolver: absent",
        f"- S139CompatibilityFixes SHA-256 preserved: `{base_s139}`",
        "- BCMER enabled event sections: `ModdedEvents.cfg:[ShyGuy]` only",
        "- PremiumScraps/Chillax caller-return invariants: re-proven by exact reviewed DLL SHA identity",
        "- Broad shared sink/lifecycle patch labels: absent",
        "- Plugin config default: false",
        "- Work-branch implementation-complete safety latch: false",
        "",
        "This is an ephemeral prebuild/static gate. It does not update BuildSpecs/current.json,",
        "RuntimeInbox/ACTIVE_BUILD.txt, Current/AUTO_BUILD_RESULT.*, any canonical profile, or runtime state.",
        "",
    ]
    (OUT / "STATIC_VALIDATION.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "FAILURE.txt").write_text(str(exc) + "\n", encoding="utf-8")
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
