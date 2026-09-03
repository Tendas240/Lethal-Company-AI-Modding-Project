README HANDOVER — S1.41

Canonical state:
S1.41 — runtime accepted

Canonical profile:
Profiles/LC V1 S1.41 BCMER Reactivation.r2z

SHA-256:
d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b

Read first:
1. README.md
2. START_HERE_ChatGPT_Masterprompt.txt
3. Current/00_CURRENT_STATE.md
4. Current/01_HANDOVER_CORE.md
5. Current/12_HANDOVER_S1.41_TO_S1.42A.md
6. Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md
7. Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md
8. Current/Projektstatus_S1.41.json
9. Current/Aktive_Modliste_S1.41.txt
10. BuildSpecs/S1.42A_PLAN.md

S1.41 acceptance:
- BCMER exact 1.71.0 loaded and ran events.
- Ownership guard survived runtime.
- Raining / HeavyRain / AllWeather / Hurricane stayed disabled.
- S1.40B CodeRebirth Currency/Flash-Turret suppression survived.
- Runtime evidence is persisted online under RuntimeEvidence/S1.41/20260902T215804Z/.

Next binding stage:
S1.42A candidate is already built and automation-verified.
Profile: Profiles/LC V1 S1.42A Interior Config Seed.r2z
SHA-256: 70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe
Immediate next step: runtime config-generation seed test + RuntimeInbox evidence upload.
S1.41 remains the accepted gameplay baseline until that evidence is evaluated.

Repository-first rule:
Build on GitHub using BuildSpecs/current.json + BuildSystem/profile_builder.py + GitHub Actions. No local repo clone or local PowerShell profile build is required.

Open non-blocking issue:
Mineshaft elevator + large Pikmin group caused one floor-clipping/fall-death incident with nearby NavMesh agent warnings. Causality is not proven and BCMER is not implicated.

Gale import rule:
Advanced options -> Import all files
