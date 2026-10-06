import json
from pathlib import Path

NEXT = (
    "Perform one separately bounded S1.42AK-SHDIAG1 publication PR integration/reconciliation. "
    "Verify PR #309 final changed-file set and exact final-head CI with the temporary publication "
    "workflow absent; merge only if justified. After merge, verify permanent exact-main-head "
    "Knowledge Architecture. Canonical indexing, Profiles/EXPECTED_HASHES.json changes, Gale import, "
    "controller changes, runtime activation and gameplay remain unauthorized."
)

p = Path("Current/CURRENT_STATE.json")
state = json.loads(p.read_text(encoding="utf-8"))
scope = state["selected_scope"]
scope["status"] = "PHASE_C_STOREHOUSE_SHDIAG1_EXACT_BYTES_MATERIALIZED_PUBLICATION_INTEGRATION_PENDING_BMDSFIX1_ACTIVE_NOT_ACCEPTED"
scope["analysis_contract"] = (
    "SHDIAG1 exact frozen review bytes are materialized on publication PR #309. "
    "Current/295 and BuildSpecs/S1.42AK-SHDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md "
    "are publication-branch authority. Main integration and canonical indexing remain pending; "
    "live controllers remain unchanged."
)
scope["next_action"] = NEXT
state["next_action"] = NEXT
pc = scope["phase_c"]
pc["storehouse_shdiag1_built"] = True
pc.update({
    "storehouse_shdiag1_publication_authorization": "Current/294_S1.42AK_SHDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md",
    "storehouse_shdiag1_publication_checkpoint": "Current/295_S1.42AK_SHDIAG1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md",
    "storehouse_shdiag1_publication_verification": "BuildSpecs/S1.42AK-SHDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md",
    "storehouse_shdiag1_publication_status": "EXACT_BYTES_MATERIALIZED_ON_PUBLICATION_BRANCH_MAIN_INTEGRATION_PENDING_NOT_CANONICALLY_INDEXED",
    "storehouse_shdiag1_publication_pr": 309,
    "storehouse_shdiag1_publication_branch": "publish/s142ak-shdiag1-exact",
    "storehouse_shdiag1_publication_transport_run": 37479350216,
    "storehouse_shdiag1_publication_transport_run_number": 1,
    "storehouse_shdiag1_publication_revalidation_run": 37480229257,
    "storehouse_shdiag1_publication_revalidation_run_number": 3,
    "storehouse_shdiag1_publication_transport_definition_commit": "61bd6342624f9a4b23669f6b5e51ee48a4cd3a74",
    "storehouse_shdiag1_publication_materialization_commit": "5f3fe6379bb05735b37c22b6243d156ce8f53c9f",
    "storehouse_shdiag1_publication_transport_removal_commit": "ba3abb28fe1dbe204f004222ee719c3ff3efab6f",
    "storehouse_shdiag1_publication_main_integrated": False,
    "storehouse_shdiag1_profile": "Profiles/LC V1 S1.42AK-SHD1.r2z",
    "storehouse_shdiag1_profile_sha256": "787a7baf441ec0ccc2af1295ccc3e94b70ca3bff17e026fb90985733efcb957e",
    "storehouse_shdiag1_dll_sha256": "e78e0eb6483d332e3b2a05be772173036c90e9fccd2c1fc9d52980a5d516d062",
    "storehouse_shdiag1_publication_snapshot_entries": 338,
    "storehouse_shdiag1_publication_snapshot_text_entries": 331,
})
p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

hp = Path("Current/00_CURRENT_STATE.md")
human = hp.read_text(encoding="utf-8")
marker = "## Exact next action"
start = human.index(marker)
end = human.index("\n## ", start + len(marker))
human = human[:start] + marker + "\n\n" + NEXT + "\n" + human[end:]
hp.write_text(human, encoding="utf-8")
