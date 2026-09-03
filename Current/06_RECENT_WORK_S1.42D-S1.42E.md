# 06 — Recent Work S1.42D-S1.42E

## Historical juijui reference became repository-readable

Original:
`References/LegacyProfiles/juijui/juijui.r2z`

SHA-256:
`ddd10bcec3329c155b3a0a2d74460928b02df147356701fb6cf79ebb5a9f7e00`

Indexed snapshot:
`References/LegacyProfiles/juijui/Extracted/`

Recovered Jetpack evidence:
`JetpackBatteryUsage = 140`

The historical Bigger Battery package is absent from the final export and its DLL is absent, so 140 is treated as the strongest historical intended/configured value rather than proof of final-export runtime activation.

## S1.42D — first isolated enemy regression build

Profile:
`Profiles/LC V1 S1.42D Isolated Enemy Regression.r2z`

SHA-256:
`b455bd413a6da4ac059117d8fec667053c96ffeef7e239d9188d6e514d15bd5c`

Goals:
- generic LethalMin enemy grab/bite + Invincible Pikmin state recovery;
- diagnostic enemy roster only: Thumper/Crawler, Puffer, Baboon Hawk;
- Jetpack 140-second target;
- no high-speed/mid-air Jetpack self-explosion;
- Functional Microwave volume 0.7.

Build passed compile and static verification.

### S1.42D runtime failure

The user reported a startup crash before a usable Main Menu.

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

Log SHA-256:
`55cdbf6904c7d1acb74647c90a79820df9e3a39978cd60ccf4d6e25bc95d4107`

The log reached:
`Custom Content Processed. Unlocking Main Menu.`

Then compatibility plugin v1.3.0 began a broad runtime reflection/Harmony scan of LethalMin methods.

It patched many generated/inherited methods and HarmonyX emitted warnings that inherited/non-declared methods should not be patched through derived types.

The log terminated during that scan before the scan completion marker.

Conclusion:
**S1.42D failed startup due to the new broad LethalMin patch architecture.**

Do not retest S1.42D.

## S1.42E — startup-safe hotfix candidate

Profile:
`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

Compatibility plugin:
v1.3.1

DLL SHA-256:
`caf20c785245396d9f31ff32b556cbe75d64b87a5a676807184093a6cef78eab`

Build:
- 0 compiler warnings;
- 0 compiler errors;
- 331 archive members;
- 188 packages / 183 enabled / 5 disabled;
- no package/version/state differences vs S1.42D;
- only DLL + export/profile metadata changed vs S1.42D.

### LethalMin hotfix

Now only:
- `*PikminEnemy` adapter types;
- `DeclaredOnly`;
- local `BitePikmin`, `GrabPikmin`, `GrabPikminWithTongue`;
- implemented bodies.

No:
- RPC wrappers;
- generic PikminAI methods;
- PikminItem methods;
- inherited methods patched through derived types.

### Jetpack cleanup

S1.42D showed `JetpackItem.Start` resolved to inherited `GrabbableObject.Start`.

S1.42E removes that Harmony target entirely.

The 140-second value is attempted only against the loaded Jetpack Item asset and retried narrowly until the asset exists.

`MidAirExplosions = Off` remains.

### Next runtime gate

S1.42E is not runtime tested yet.

First:
**reach Main Menu without startup crash.**

If successful, continue the same isolated Baboon Hawk / Thumper / Puffer regression test and Jetpack/Microwave checks.

Runtime routing:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42E`
