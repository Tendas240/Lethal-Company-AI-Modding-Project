import json
from pathlib import Path

p = Path("Current/CURRENT_STATE.json")
s = json.loads(p.read_text(encoding="utf-8"))
s["selected_scope"]["analysis_contract"] = (
    "SHDIAG1 exact frozen review bytes are materialized on publication PR #309. "
    "Current/295 and BuildSpecs/S1.42AK-SHDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md "
    "are publication-branch authority. Main integration and canonical indexing remain pending. "
    "S1.42AK-BMDSFIX1 remains the active candidate / NOT ACCEPTED with its passive outstanding "
    "and unwaived Black Mesa x DeepSewersFlow gate. BuildSpecs/current.json remains disabled and "
    "RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK-BMDSFIX1. Profiles/EXPECTED_HASHES.json is "
    "unchanged; Gale import, runtime activation and gameplay remain unauthorized."
)
p.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
