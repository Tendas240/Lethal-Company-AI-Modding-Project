#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY_PATH = ROOT / "BuildSpecs/S1.42AI-DIAG1_OVERLAY.json"
OUTPUT_PATH = ROOT / "BuildSpecs/S1.42AI-DIAG1_DRAFT.json"
SOURCE_ROOT = ROOT / "ProfileSources/S1.42AI"


def fail(message):
    raise RuntimeError(f"S1.42AI-DIAG1 spec generation failed: {message}")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ini(path):
    if not path.exists():
        fail(f"missing config: {path.relative_to(ROOT)}")
    sections = {}
    section = None
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if not section or section in sections:
                fail(f"duplicate/invalid section [{section}] in {path.relative_to(ROOT)}:{number}")
            sections[section] = {}
            continue
        if "=" not in raw:
            fail(f"unparsed data in {path.relative_to(ROOT)}:{number}: {raw!r}")
        if section is None:
            fail(f"key before section in {path.relative_to(ROOT)}:{number}")
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key in sections[section]:
            fail(f"duplicate key [{section}] {key!r} in {path.relative_to(ROOT)}")
        sections[section][key] = value
    return sections


def value(doc, section, key):
    if section not in doc or key not in doc[section]:
        fail(f"missing exact key [{section}] {key}")
    return doc[section][key]


def assert_value(doc, section, key, expected, label):
    actual = value(doc, section, key)
    if actual != expected:
        fail(f"{label}: [{section}] {key} expected {expected!r}, got {actual!r}")


def assert_unique_key(doc, key, expected, label):
    matches = [(section, values[key]) for section, values in doc.items() if key in values]
    if len(matches) != 1:
        fail(f"{label}: key {key!r} expected exactly once, found {len(matches)}")
    if matches[0][1] != expected:
        fail(f"{label}: {key!r} expected {expected!r}, got {matches[0][1]!r}")


def config_path(archive_path):
    return SOURCE_ROOT / archive_path


def line_regex(section, key, expected):
    return (
        r"(?ms)^\[" + re.escape(section) + r"\]\s*$"
        r"(?:(?!^\[).)*?^" + re.escape(key) + r"\s*=\s*" + re.escape(expected) + r"\s*$"
    )


def main():
    overlay = json.loads(OVERLAY_PATH.read_text(encoding="utf-8"))
    base = ROOT / overlay["base_profile"]
    if not base.exists():
        fail(f"base profile missing: {overlay['base_profile']}")
    actual_base_sha = sha256(base)
    if actual_base_sha != overlay["base_sha256"]:
        fail(f"base profile SHA mismatch: expected {overlay['base_sha256']}, got {actual_base_sha}")

    bcmer = overlay["bcmer"]
    vanilla = parse_ini(config_path(bcmer["vanilla_events"]))
    modded = parse_ini(config_path(bcmer["modded_events"]))
    custom_path = config_path(bcmer["custom_events"])
    if custom_path.read_bytes() != b"":
        fail("BCMER CustomEvents.cfg is not the exact empty S1.42AI source")
    core = parse_ini(config_path(bcmer["core"]))
    difficulty = parse_ini(config_path(bcmer["difficulty"]))

    event_key = bcmer["event_enabled_key"]
    vanilla_event_sections = sorted(section for section, data in vanilla.items() if event_key in data)
    modded_event_sections = sorted(section for section, data in modded.items() if event_key in data)
    if not vanilla_event_sections or not modded_event_sections:
        fail("BCMER event inventories are unexpectedly empty")
    if "ShyGuy" in vanilla_event_sections:
        fail("unexpected ShyGuy event section in VanillaEvents.cfg")
    if modded_event_sections.count("ShyGuy") != 1:
        fail("expected exactly one [ShyGuy] event section in ModdedEvents.cfg")

    for key, expected in bcmer["shyguy_preserved"].items():
        assert_value(modded, "ShyGuy", key, expected, "ShyGuy preserved contract")

    assert_value(core, "Custom Events", "Enable Custom Events?", "true", "S1.42AI source contract")
    for item in bcmer["core_assertions"]:
        assert_value(core, item["section"], item["key"], item["value"], "BCMER core preserved assertion")
    for item in bcmer["difficulty_assertions"]:
        assert_value(difficulty, item["section"], item["key"], item["value"], "BCMER difficulty preserved assertion")
    for item in bcmer["difficulty_unique_key_assertions"]:
        assert_unique_key(difficulty, item["key"], item["value"], "BCMER difficulty preserved assertion")

    for item in overlay["fixed_config_assertions"]:
        doc = parse_ini(config_path(item["path"]))
        assert_value(doc, item["section"], item["key"], item["value"], f"preserved assertion {item['path']}")

    patches = []
    for section in vanilla_event_sections:
        patches.append({"path": bcmer["vanilla_events"], "section": section, "key": event_key, "value": "false"})
    for section in modded_event_sections:
        patches.append({
            "path": bcmer["modded_events"],
            "section": section,
            "key": event_key,
            "value": "true" if section == "ShyGuy" else "false",
        })
    for item in bcmer["core_patches"]:
        patches.append({"path": bcmer["core"], **item})
    for item in bcmer["difficulty_patches"]:
        patches.append({"path": bcmer["difficulty"], **item})
    patches.extend(overlay["fixed_config_patches"])

    assertions = [
        {"path": bcmer["vanilla_events"], "regex": r"(?s)\A(?!.*(?m:^Event Enabled\?\s*=\s*true\s*$)).*\Z"},
        {"path": bcmer["modded_events"], "regex": line_regex("ShyGuy", event_key, "true")},
        {"path": bcmer["custom_events"], "regex": r"\A\s*\Z"},
    ]
    for key, expected in bcmer["shyguy_preserved"].items():
        assertions.append({"path": bcmer["modded_events"], "regex": line_regex("ShyGuy", key, expected)})
    for item in bcmer["core_patches"] + bcmer["core_assertions"]:
        assertions.append({"path": bcmer["core"], "regex": line_regex(item["section"], item["key"], item["value"])})
    for item in bcmer["difficulty_patches"] + bcmer["difficulty_assertions"]:
        assertions.append({"path": bcmer["difficulty"], "regex": line_regex(item["section"], item["key"], item["value"])})
    for item in bcmer["difficulty_unique_key_assertions"]:
        assertions.append({"path": bcmer["difficulty"], "regex": r"(?m)^" + re.escape(item["key"]) + r"\s*=\s*" + re.escape(item["value"]) + r"\s*$"})
    for item in overlay["fixed_config_patches"] + overlay["fixed_config_assertions"]:
        assertions.append({"path": item["path"], "regex": line_regex(item["section"], item["key"], item["value"])})

    spec = {
        "enabled": False,
        "build_id": overlay["build_id"],
        "base_profile": overlay["base_profile"],
        "base_sha256": overlay["base_sha256"],
        "output_profile": overlay["output_profile"],
        "profile_name": overlay["profile_name"],
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": patches,
        "local_plugin_builds": [overlay["local_plugin_build"]],
        "file_injections": [],
        "text_assertions": assertions,
        "snapshot_dir": "ProfileSources/S1.42AI-DIAG1",
        "generated_from": "BuildSpecs/S1.42AI-DIAG1_OVERLAY.json",
        "event_inventory": {
            "vanilla_sections": len(vanilla_event_sections),
            "modded_sections": len(modded_event_sections),
            "enabled_sections": ["ModdedEvents.cfg:[ShyGuy]"],
        },
    }
    OUTPUT_PATH.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"BCMER event sections: vanilla={len(vanilla_event_sections)}, modded={len(modded_event_sections)}, enabled=1 ([ShyGuy])")
    print(f"Config patches: {len(patches)}; text assertions: {len(assertions)}")
    print("Draft remains enabled=false; BuildSpecs/current.json is not modified by this generator.")


if __name__ == "__main__":
    main()
