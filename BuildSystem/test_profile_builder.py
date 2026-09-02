#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from profile_builder import block_version, item_blocks, lines, patch_export

EXPORT = Path("ProfileSources/S1.41/export.r2x")


def block_text(data: list[str], block: tuple[int, int, str, str]) -> str:
    start, end, _indent, _name = block
    return "\n".join(data[start:end])


def main() -> int:
    original = EXPORT.read_text(encoding="utf-8-sig")
    original_lines = lines(original)
    original_blocks = item_blocks(original_lines)

    assert len(original_blocks) == 179, f"Expected 179 S1.41 packages, got {len(original_blocks)}"
    original_names = [b[3] for b in original_blocks]

    spec = {
        "profile_name": "SELFTEST S1.42A",
        "mod_state_changes": [],
        "mod_removals": [],
        "mod_additions": [
            {
                "name": "SelfTest-Interior_A",
                "version": "1.2.3",
                "enabled": True,
                "source": "Thunderstore",
            },
            {
                "name": "SelfTest-Interior_B",
                "version": "4.5.6",
                "enabled": False,
                "source": "Thunderstore",
            },
        ],
    }

    patched = patch_export(original, spec)
    data = lines(patched)
    blocks = item_blocks(data)

    assert len(blocks) == 181, f"Expected 181 packages after additions, got {len(blocks)}"
    names = [b[3] for b in blocks]
    assert names[:2] == ["SelfTest-Interior_A", "SelfTest-Interior_B"], names[:2]
    assert names[2:] == original_names, "Existing package order/content was not preserved"

    first_original_indent = original_blocks[0][2]
    assert blocks[0][2] == first_original_indent
    assert blocks[1][2] == first_original_indent

    a = next(b for b in blocks if b[3] == "SelfTest-Interior_A")
    b = next(b for b in blocks if b[3] == "SelfTest-Interior_B")
    assert block_version(block_text(data, a)) == "1.2.3"
    assert block_version(block_text(data, b)) == "4.5.6"

    a_text = block_text(data, a)
    b_text = block_text(data, b)
    assert "  enabled: true" in a_text
    assert "  source: Thunderstore" in a_text
    assert "  enabled: false" in b_text
    assert "  source: Thunderstore" in b_text

    assert "profileName: SELFTEST S1.42A" in patched

    duplicate = dict(spec)
    duplicate["mod_additions"] = [
        {
            "name": original_names[0],
            "version": "1.0.0",
            "enabled": True,
            "source": "Thunderstore",
        }
    ]
    try:
        patch_export(original, duplicate)
    except RuntimeError as exc:
        assert "already present" in str(exc)
    else:
        raise AssertionError("Duplicate package addition was not rejected")

    print("profile_builder mod_additions self-test: PASS")
    print(f"Base packages: {len(original_blocks)}")
    print(f"Patched packages: {len(blocks)}")
    print(f"Mirrored item indentation: {first_original_indent!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
