# S1.42AK-BMAFR1 Config-Binding Repair Implementation

**Date:** 2026-10-02  
**Status:** IMPLEMENTED ON DEDICATED REPAIR BRANCH / INACTIVE REVIEW CI PENDING / NOT PUBLISHED / NOT RUNTIME-ARMED  
**Scope:** Black Mesa x Abandoned Foundry config-binding repair only  
**Build ID:** `S1.42AK-BMAFR1`

## Implemented decisions

The repair successor uses short profile identity `LC V1 S1.42AK-BMAFR1` and derives directly from exact accepted S1.42AK SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

The dedicated `BuildSystem/bmafr1_profile_builder.py` repair path fail-closes on visible-equivalent/raw-different LLL sections while leaving the generic `BuildSystem/profile_builder.py` unchanged. For Foundry, the BuildSpec encodes exactly nine `\u200b` JSON escapes before `Custom Dungeon:  Abandoned Foundry`; JSON decoding therefore supplies the exact nine U+200B raw section identifier to the repair builder.

Visible-equivalent comparison is used only to reject duplicate or raw-mismatched sections. It is never used to claim section identity.

## Diagnostic DLL preservation

The accepted S1.42AK parent does not contain the BMAFDIAG1 plugin. The BMAFR1 BuildSpec therefore declares one hash-guarded `archive_member_injections` donor. The bounded repair builder validates the donor profile/member hashes, extracts only that DLL to a temporary file, and delegates final archive construction to the unchanged generic builder.

BMAFR1 reuses only:

`BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`

from exact published BMAFDIAG1 profile SHA-256 `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`, with required DLL SHA-256 `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`.

No C# source is changed and no diagnostic rebuild is authorized.

## Validator correction

The historical BMAFDIAG1 build validator no longer strips Unicode `Cf` characters to establish Foundry section identity. It now requires the exact nine-U+200B raw header and treats visible equivalence only as duplicate/mismatch detection.

The new BMAFR1 validator additionally proves:

- owner evidence itself has exactly nine U+200B characters;
- accepted S1.42AK has no visible-equivalent Foundry section;
- review output has exactly one visible-equivalent Foundry section and it is the exact raw header;
- plain Foundry and raw+plain duplicate states fail closed;
- owner values are preserved except `Enable Content Configuration=true` and exact one-time `Black Mesa:100`;
- exact BMAFDIAG1 DLL bytes are reused;
- accepted normalizer and LLL 1.7.12 identities remain exact;
- only `export.r2x` and LLL config change among existing baseline members;
- the diagnostic DLL is the only added member;
- live controllers remain unchanged.

## Review construction

The dedicated workflow `.github/workflows/s142ak-bmafr1-build-static.yml` performs only an ephemeral Actions review build. It runs the permanent Gale path guard, fresh LLL provenance, bounded BMAFR1 repair builder and BMAFR1 validator, then uploads the review artifact.

The short profile projects to 217/219-character canonical reference paths, below the permanent 255-character project budget.

## Preserved boundaries

No publication, profile index, Gale import, runtime activation, gameplay, Foundry qualification, BMDSFIX1 acceptance/waiver, normalizer change, universal availability change or unrelated interior/moon repair is included.

`BuildSpecs/current.json` remains disabled and `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
