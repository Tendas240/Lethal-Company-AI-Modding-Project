#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

UTF8 = "utf-8"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def decode(data: bytes) -> str:
    return data.decode("utf-8-sig")


def encode(text: str) -> bytes:
    return text.encode(UTF8)


def lines(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def joined(items: list[str]) -> str:
    return "\r\n".join(items)


def set_ini(text: str, section: str, key: str, value: str) -> str:
    data = lines(text)
    header = f"[{section}]"
    start = next((i for i, x in enumerate(data) if x.strip().casefold() == header.casefold()), -1)

    if start < 0:
        if data and data[-1] != "":
            data.append("")
        data.extend([header, f"{key} = {value}"])
        return joined(data)

    end = len(data)
    for i in range(start + 1, len(data)):
        x = data[i].strip()
        if x.startswith("[") and x.endswith("]"):
            end = i
            break

    rx = re.compile(r"^\s*" + re.escape(key) + r"\s*=", re.I)
    for i in range(start + 1, end):
        if rx.match(data[i]):
            data[i] = f"{key} = {value}"
            return joined(data)

    data[end:end] = [f"{key} = {value}", ""]
    return joined(data)


def item_blocks(data: list[str]) -> list[tuple[int, int, str, str]]:
    starts: list[tuple[int, str, str]] = []
    for i, x in enumerate(data):
        m = re.match(r"^(\s*)-\s+name\s*:\s*(.+?)\s*$", x)
        if m:
            starts.append((i, m.group(1), m.group(2).strip().strip('"').strip("'")))

    out = []
    for start, indent, name in starts:
        end = len(data)
        for j in range(start + 1, len(data)):
            if not data[j].strip() or data[j].lstrip().startswith("#"):
                continue
            leading = len(data[j]) - len(data[j].lstrip())
            if leading < len(indent):
                end = j
                break
            if re.match(r"^" + re.escape(indent) + r"-\s+name\s*:", data[j]):
                end = j
                break
        out.append((start, end, indent, name))
    return out


def block_version(block: str) -> str | None:
    m = re.search(
        r"(?ms)^\s*(?:version|versionNumber)\s*:\s*$"
        r".*?^\s*major\s*:\s*(\d+)\s*$"
        r".*?^\s*minor\s*:\s*(\d+)\s*$"
        r".*?^\s*patch\s*:\s*(\d+)\s*$",
        block,
    )
    if m:
        return ".".join(m.groups())
    m = re.search(
        r'(?m)^\s*(?:version|versionNumber)\s*:\s*["\']?(\d+\.\d+\.\d+)["\']?\s*$',
        block,
    )
    return m.group(1) if m else None


def patch_export(text: str, spec: dict) -> str:
    data = lines(text)

    hits = 0
    for i, x in enumerate(data):
        m = re.match(r"^(\s*)profileName\s*:", x)
        if m:
            hits += 1
            data[i] = f"{m.group(1)}profileName: {spec['profile_name']}"
    if hits != 1:
        raise RuntimeError(f"Expected one profileName, found {hits}")

    for change in spec.get("mod_state_changes", []):
        blocks = [b for b in item_blocks(data) if b[3] == change["name"]]
        if len(blocks) != 1:
            raise RuntimeError(f"Package {change['name']} count is {len(blocks)}, expected 1")
        start, end, _indent, _name = blocks[0]
        actual = block_version("\n".join(data[start:end]))
        if actual != str(change["version"]):
            raise RuntimeError(f"Package {change['name']} version is {actual}, expected {change['version']}")
        enabled_hits = 0
        for i in range(start + 1, end):
            m = re.match(r"^(\s*)enabled\s*:\s*(true|false)\s*$", data[i], re.I)
            if m:
                enabled_hits += 1
                data[i] = f"{m.group(1)}enabled: {'true' if change['enabled'] else 'false'}"
        if enabled_hits != 1:
            raise RuntimeError(f"Package {change['name']} enabled field count is {enabled_hits}")

    for removal in spec.get("mod_removals", []):
        blocks = [b for b in item_blocks(data) if b[3] == removal["name"]]
        if len(blocks) != 1:
            raise RuntimeError(f"Removal package {removal['name']} count is {len(blocks)}, expected 1")
        start, end, _indent, _name = blocks[0]
        if removal.get("version"):
            actual = block_version("\n".join(data[start:end]))
            if actual != str(removal["version"]):
                raise RuntimeError(f"Refusing removal of {removal['name']}: version {actual}")
        del data[start:end]

    additions = spec.get("mod_additions", [])
    if additions:
        existing = {b[3] for b in item_blocks(data)}
        mods_line = next((i for i, x in enumerate(data) if re.match(r"^mods\s*:\s*$", x)), -1)
        if mods_line < 0:
            raise RuntimeError("export.r2x has no top-level mods:")

        insert_at = len(data)
        for i in range(mods_line + 1, len(data)):
            if data[i] and not data[i][0].isspace() and not data[i].lstrip().startswith("#"):
                insert_at = i
                break

        new_lines: list[str] = []
        for add in additions:
            name = add["name"]
            if name in existing:
                raise RuntimeError(f"Package already present: {name}")
            parts = str(add["version"]).split(".")
            if len(parts) != 3 or not all(x.isdigit() for x in parts):
                raise RuntimeError(f"Invalid semantic version for {name}: {add['version']}")
            major, minor, patch = parts
            new_lines.extend([
                f"  - name: {name}",
                "    version:",
                f"      major: {major}",
                f"      minor: {minor}",
                f"      patch: {patch}",
                f"    enabled: {'true' if add.get('enabled', True) else 'false'}",
            ])
            if add.get("source"):
                new_lines.append(f"    source: {add['source']}")
            existing.add(name)
        data[insert_at:insert_at] = new_lines

    return joined(data)


@dataclass
class Entry:
    index: int
    name: str
    data: bytes
    date_time: tuple
    external_attr: int

    @property
    def hash(self) -> str:
        return sha_bytes(self.data)


def read_zip(path: Path) -> list[Entry]:
    out = []
    with zipfile.ZipFile(path, "r") as z:
        for i, info in enumerate(z.infolist()):
            out.append(Entry(
                i,
                info.filename,
                b"" if info.is_dir() else z.read(info),
                info.date_time,
                info.external_attr,
            ))
    return out


def write_zip(path: Path, entries: list[Entry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with zipfile.ZipFile(tmp, "w") as z:
        for e in entries:
            info = zipfile.ZipInfo(e.name, date_time=e.date_time)
            info.external_attr = e.external_attr
            method = zipfile.ZIP_STORED if e.name.endswith("/") else zipfile.ZIP_DEFLATED
            z.writestr(info, b"" if e.name.endswith("/") else e.data, compress_type=method, compresslevel=9)
    tmp.replace(path)


def build_plugins(spec: dict) -> list[dict]:
    inject = []
    for item in spec.get("local_plugin_builds", []):
        project = Path(item["project"])
        if not project.exists():
            raise RuntimeError(f"Plugin project missing: {project}")
        config = item.get("configuration", "Release")
        subprocess.run(["dotnet", "build", str(project), "-c", config], check=True)
        built = Path(item["built_file"])
        if not built.exists():
            raise RuntimeError(f"Built plugin missing: {built}")
        inject.append({"source": str(built), "archive_path": item["archive_path"]})
    return inject


def snapshot(entries: list[Entry], root: Path) -> dict:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    index = []

    for e in entries:
        rec = {"index": e.index, "path": e.name, "size": len(e.data), "sha256": e.hash, "text_snapshot": False}
        if not e.name.endswith("/"):
            candidate = (
                e.name == "export.r2x"
                or e.name.startswith("BepInEx/config/")
                or e.name.lower().endswith((".txt", ".md", ".json", ".yml", ".yaml", ".cfg", ".ini", ".xml"))
            )
            if candidate:
                try:
                    text = decode(e.data)
                except UnicodeDecodeError:
                    pass
                else:
                    dest = root / PurePosixPath(e.name)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(text, encoding=UTF8)
                    rec["text_snapshot"] = True
        index.append(rec)

    (root / "FILE_INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding=UTF8)
    return {"entries": len(index), "text_entries": sum(1 for x in index if x["text_snapshot"])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path)
    args = ap.parse_args()
    spec = json.loads(args.spec.read_text(encoding=UTF8))

    if not spec.get("enabled", False):
        print("Build spec disabled; nothing to build.")
        return 0

    for key in ("build_id", "base_profile", "base_sha256", "output_profile", "profile_name"):
        if key not in spec:
            raise RuntimeError(f"Missing build spec field: {key}")

    base = Path(spec["base_profile"])
    output = Path(spec["output_profile"])
    if not base.exists():
        raise RuntimeError(f"Base profile is not in repository: {base}")

    base_hash = sha_file(base)
    if base_hash != str(spec["base_sha256"]).lower():
        raise RuntimeError(f"Base SHA mismatch: expected {spec['base_sha256']}, got {base_hash}")

    if output.exists() and not spec.get("overwrite", False):
        raise RuntimeError(f"Output already exists: {output}")

    entries = read_zip(base)
    original_hashes = [e.hash for e in entries]
    original_count = len(entries)
    original_names = {e.name for e in entries}

    by_name: dict[str, list[Entry]] = {}
    for e in entries:
        by_name.setdefault(e.name, []).append(e)

    exports = by_name.get("export.r2x", [])
    if len(exports) != 1:
        raise RuntimeError(f"export.r2x count is {len(exports)}, expected 1")
    exports[0].data = encode(patch_export(decode(exports[0].data), spec))

    for patch in spec.get("config_patches", []):
        name = patch["path"]
        found = by_name.get(name, [])
        if len(found) > 1:
            raise RuntimeError(f"Duplicate target config: {name}")
        if found:
            e = found[0]
            text = decode(e.data)
        else:
            e = Entry(len(entries), name, b"", (1980, 1, 1, 0, 0, 0), 0)
            entries.append(e)
            by_name.setdefault(name, []).append(e)
            text = ""
        e.data = encode(set_ini(text, patch["section"], patch["key"], str(patch["value"])))

    injections = list(spec.get("file_injections", [])) + build_plugins(spec)
    for item in injections:
        source = Path(item["source"])
        name = item["archive_path"]
        if not source.exists():
            raise RuntimeError(f"Injection source missing: {source}")
        found = by_name.get(name, [])
        if len(found) > 1:
            raise RuntimeError(f"Duplicate injection target: {name}")
        if found:
            found[0].data = source.read_bytes()
        else:
            e = Entry(len(entries), name, source.read_bytes(), (1980, 1, 1, 0, 0, 0), 0)
            entries.append(e)
            by_name.setdefault(name, []).append(e)

    write_zip(output, entries)
    final = read_zip(output)

    if len(final) != len(entries):
        raise RuntimeError("ZIP member count changed unexpectedly")
    for i in range(original_count):
        if final[i].name != entries[i].name:
            raise RuntimeError(f"ZIP order/name changed at index {i}")

    changed = [final[i].name for i in range(original_count) if final[i].hash != original_hashes[i]]
    added = [e.name for e in final[original_count:]]

    allowed = {"export.r2x"}
    allowed.update(p["path"] for p in spec.get("config_patches", []) if p["path"] in original_names)
    allowed.update(x["archive_path"] for x in injections if x["archive_path"] in original_names)
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise RuntimeError(f"Unexpected changed existing members: {unexpected}")

    expected_added = {
        p["path"] for p in spec.get("config_patches", []) if p["path"] not in original_names
    }
    expected_added.update(x["archive_path"] for x in injections if x["archive_path"] not in original_names)
    if sorted(added) != sorted(expected_added):
        raise RuntimeError(f"Unexpected added members: expected {sorted(expected_added)}, got {sorted(added)}")

    final_by_name: dict[str, list[Entry]] = {}
    for e in final:
        final_by_name.setdefault(e.name, []).append(e)

    for assertion in spec.get("text_assertions", []):
        found = final_by_name.get(assertion["path"], [])
        if len(found) != 1:
            raise RuntimeError(f"Assertion path count is not 1: {assertion['path']}")
        text = decode(found[0].data)
        if assertion.get("contains") is not None and assertion["contains"] not in text:
            raise RuntimeError(f"Missing assertion text in {assertion['path']}: {assertion['contains']}")
        if assertion.get("not_contains") is not None and assertion["not_contains"] in text:
            raise RuntimeError(f"Forbidden assertion text in {assertion['path']}: {assertion['not_contains']}")
        if assertion.get("regex") is not None and not re.search(assertion["regex"], text, re.M | re.S):
            raise RuntimeError(f"Regex assertion failed in {assertion['path']}: {assertion['regex']}")

    build_id = str(spec["build_id"])
    snap_dir = Path(spec.get("snapshot_dir", f"ProfileSources/{build_id}"))
    snap_info = snapshot(final, snap_dir)
    output_hash = sha_file(output)

    result = {
        "build_id": build_id,
        "profile_name": spec["profile_name"],
        "base_profile": str(base),
        "base_sha256": base_hash,
        "output_profile": str(output),
        "output_sha256": output_hash,
        "zip_members": len(final),
        "changed_existing_members": changed,
        "added_members": added,
        "mod_state_changes": spec.get("mod_state_changes", []),
        "mod_additions": spec.get("mod_additions", []),
        "mod_removals": spec.get("mod_removals", []),
        "snapshot_dir": str(snap_dir),
        "snapshot": snap_info,
    }

    result_json = Path(spec.get("result_json", "Current/AUTO_BUILD_RESULT.json"))
    result_md = Path(spec.get("result_md", "Current/AUTO_BUILD_RESULT.md"))
    result_json.parent.mkdir(parents=True, exist_ok=True)
    result_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding=UTF8)

    md = [
        f"# Automated profile build result - {build_id}",
        "",
        f"- Profile: {spec['profile_name']}",
        f"- Base: {base}",
        f"- Base SHA-256: {base_hash}",
        f"- Output: {output}",
        f"- Output SHA-256: {output_hash}",
        f"- ZIP members: {len(final)}",
        f"- Text snapshot: {snap_dir} ({snap_info['text_entries']} readable files)",
        "",
        "## Changed existing members",
        "",
        *([f"- {x}" for x in changed] or ["- none"]),
        "",
        "## Added members",
        "",
        *([f"- {x}" for x in added] or ["- none"]),
        "",
    ]
    result_md.write_text("\n".join(md), encoding=UTF8)

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
