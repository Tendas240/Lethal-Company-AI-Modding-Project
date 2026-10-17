# LEADFACTORY_MINIMAL_PROVENANCE_PERSISTENCE_V1 — bounded evidence and rights contract

**Date:** 2026-10-17  
**Status:** PR-STAGED CONTRACT PROPOSAL ONLY / NOT CANONICAL UNTIL SEPARATELY APPROVED PINNED MERGE AND PERMANENT EXACT-MAIN CI  
**Scope:** Universal Interior Viability / Equal Availability; Offense C1 #24 Lead Factory / `LeadFactory`; static serialized owner provenance ONLY  
**Contract decision:** SPECIFICATION_ONLY / NO LIVE CAPTURE / NO PERSISTENCE IMPLEMENTATION / PUBLICATION_RIGHTS_NOT_CLEARED  
**Reviewed starting main:** `7a4401b81184feab54a52dbc155dce21ba9dd457` (Knowledge Architecture push #1686 / run 39030128345, completed/success, exact head, 24/24 steps)  
**Historical integration:** PR #464 -> `afd9ffa97baed1a6d92c018e1e9d89befe51651b`; PR #465 -> `7a4401b81184feab54a52dbc155dce21ba9dd457`.

## 1. Authority, purpose and hard boundary

This single-file proposal is **a specification, not approval or implementation of any storage, acquisition, publication, source change, workflow dispatch, build or runtime action**. It does not modify the live source-only LeadFactory capture flow, create a retention endpoint, preserve a real JSON report, or convert earlier conversation-local observations into newly authenticated original bytes.

Binding higher authorities, in precedence order: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`; `Current/CURRENT_STATE.json`; `Current/PROJECT_KNOWLEDGE_MAP.md`; `Knowledge/CURRENT_LIFECYCLE.md`; `Knowledge/INTERIORS_AND_LLL.md`; Interior-first `Current/412_S1.42AK_PHASE_C_INTERIOR_FIRST_COMPLETION_PRIORITY_DECISION.md`; GoldenHotel method stop `Current/416_S1.42AK_PHASE_C_GOLDENHOTEL_GENERATION_PROOF_METHOD_SAFETY_DECISION.md`; CKDIAG1 safety `Current/406`, `Current/409`, `Current/410` and patch-safety `Current/68` (resolve exact canonical filenames via repository). `Current/CURRENT_STATE.json.next_action` remains the live machine route; this PR neither replaces nor edits it.

Live implementation and immutable historical evidence references:

- `.github/workflows/universal-interior-c3-owner-matching-evidence.yml`
- `AnalysisTools/capture_leadfactory_minimal_provenance.py`
- `AnalysisTools/inspect_universal_interior_owner_matching.py`
- `SourceEvidence/UniversalInteriorViability/PhaseC3OwnerMatching/PACKAGE_LOCK.json`
- `SourceEvidence/UniversalInteriorViability/PhaseC3OwnerMatching/CAPTURE_PROVENANCE.json`
- `SourceEvidence/UniversalInteriorViability/PhaseC3OwnerMatching/LEAD_INTERIORS_CAPTURE.json`
- `Current/164_S1.42AK_UNIVERSAL_INTERIOR_PHASE_A_REGISTERED_OWNER_INVENTORY.md`

The merged capture workflow runs only dependency-free validation in `pull_request`. Its `capture` job is restricted to a distinct manually approved `workflow_dispatch`, exact reviewed workflow/code commit pin and LeadFactory-only target. It currently writes `c3-owner-output/LEADFACTORY_MINIMAL.json` **only to the temporary runner**. No artifact upload, repository commit, public JSON, cache publication, release, or log dump is permitted. PR #465's exact-head owner-matching run #9 / 39029949631 had 7/7 validation steps PASS, capture SKIPPED, and zero artifacts. Source tests, including synthetic positive/negative examples, are not original-byte recapture.

Historical `PACKAGE_LOCK.json` pins source package `BLB_Thunderstore_Mods_LOL-Lead_Interiors` version `0.0.7`, its exact ZIP byte count/SHA-256 and its one `BepInEx/plugins/boomsinterior.lethalbundle` UnityFS member's byte count/SHA-256. Its archived historical flow list contains **BellevilleApp and CrimsonKeep only**; `LEAD_INTERIORS_CAPTURE.json` also has only these two targets. The four LeadFactory object path-ID/raw-hash constants in the owner inspector are **historical candidate pins** and MUST be independently checked against actually acquired authentic originals in a separately approved future operation.

## 2. Evidence tier and success semantics

This contract covers exactly the static four-node linkage:

`LeadInteriors (ExtendedMod) -> LFExtended (ExtendedDungeonFlow) -> LeadFactory (DungeonFlow)`, and `LFExtended -> LFMatchingProperties (LevelMatchingProperties)`.

The **highest** success tier the proposed persisted report may establish is:

`PINNED_SERIALIZED_REFERENCES_ONLY_NOT_OFFENSE_OR_RUNTIME_PASS`.

It **cannot** establish actual Offense owner applicability/rarity, a live managed `ReferenceEquals` wrapper, selector/Harmony patch ordering, loaded assembly identities, actual natural or diagnostic floor generation, CullFactory materialization, entrances, traversal, NavMesh/route health, all-moons compatibility, gameplay acceptance or safe deterministic selection. Only a later independently qualified coherent generation episode could change the current basic-generation residual. Even a rights-cleared, successfully persisted static report is **not** a generation PASS, selector-safety PASS or authorization for runtime.

## 3. Strict minimal payload whitelist

For any future separately authorized preservation, first require the existing `verify_minimal` semantics, then a separately reviewed storage-side **independent** validator. It MUST enforce the exact seven root keys: `schema_version`, `target`, `result`, `source`, `objects`, `edges`, `proof_boundary`; reject unknown or missing fields, other targets, other proof tiers, nonfinite values, unexpected types and inconsistent byte/hash lengths.

- `source`: only `package`, `version`, `zip_bytes`, `zip_sha256`, `unityfs_member`, `unityfs_bytes`, `unityfs_sha256`, `authority_verified`, `exact_package_lock_verified`, `unitypy_version`. Exact source version, sizes and hashes must agree with the reviewed immutable package lock **and** a freshly verified authenticated original file. A lock string alone is not evidence of bytes.
- `objects`: **exactly** `extended_mod`, `extended_flow`, `dungeon_flow`, `matching`. Each has exactly `name`, `class`, `bundle_member`, `serialized_file`, `path_id`, `raw_object_sha256`. Four objects must each match the correct class, exact CAB/member, unique identity, authenticated original-object bytes and individually pinned SHA-256. An observed failure or duplicate owner is a refusal, not a partial PASS.
- `edges`: exactly `extended_mod_to_extended_flow`, `extended_flow_to_dungeon_flow`, `extended_flow_to_matching`. Every array must be nonempty, unique, sorted, bounded and refer to an actually resolved pointer to its exact object. Field-name lexical validation alone is not sufficient for future public persistence: freeze/review a **semantic allowlist of expected technical field names** independently before permitting publication. Unexpected but regex-valid names are refused pending a new contract review.
- `proof_boundary`: fixed `PINNED_SERIALIZED_REFERENCES_ONLY_NOT_OFFENSE_OR_RUNTIME_PASS`. `result=PASS` means only that exact static capture contract passed on independently reverified bytes.

Never store serialized field values or raw trees; `serialized_fields`, `legacy_matching_fields`, `direct_references`, `levelTags`, `planetNames`, `modNames`, `authorNames`, `currentRoutePrice`, `currentWeather`, `m_GameObject`, arbitrary dynamic matching content, original ZIP/UnityFS bytes, descriptive package text, unrestricted parser output, error payloads or unknown fields remain disallowed. Do not replace this whitelist by a heuristic redaction pass.

The existing `MAX_OUTPUT_BYTES=8192` applies to a compact canonical JSON serialization. A future storage validator MUST additionally enforce **at most 8192 bytes of the actual persisted UTF-8 file**, prohibit alternate encodings and excessive whitespace, require unambiguous canonical serialization, reparse/revalidate the exact bytes to be stored, and verify the resulting payload-byte SHA-256 after read-back. The present capture script is **not** modified by this proposal; these are additional **future** implementation requirements.

## 4. Separate proposed attestation contract

A later `LEADFACTORY_CAPTURE_ATTESTATION.json` is a proposed name/schema, **not an existing evidence file**. Its independent narrowly enumerated metadata should bind:

1. Exact run ID and attempt, `workflow_dispatch` event, workflow path and source/head SHA, code/blob/lock SHAs and exact pinned checkout; distinguish PR validation runs from genuinely executed captures.
2. Exact original ZIP and UnityFS SHA-256/byte lengths as actually rehashed, verified object-pin and pointer-edge checks, exact parser/UnityPy version and static proof-tier identifier. References may point to the immutable package lock; no source bytes or matching-property content.
3. SHA-256 of the **actual stored minimal JSON byte stream**, its size, deterministic schema/validator version, independent validator result and a storage-read-back hash check. If a Git commit is separately approved, bind the exact stored Git blob/commit and path; never treat Git SHA-1 as a substitute for original SHA-256.
4. The separately approved storage mode, rights review decision identifier, authorized scope, approved retention/access/deletion policy, verifying party and capture-vs-storage timing. Do not store authorization secrets, bearer tokens or private runner credentials.

The attestation **must not self-attest its own authority** merely by copying `PASS` from the producer. Independent validation of the available source commit, workflow execution provenance, actual stored file and hash linkage is required; `PASS` without an independently verifiable surviving record is not durable proof. If a job finishes but its ephemeral output was discarded, mark `CAPTURE_RESULT_NOT_PRESERVED`; do not reconstruct a supposed report from historical pins.

A formal schema, canonicalization choice, signing/independent-review mechanism, retention location and publication policies remain **future design approval gates**, not assertions of present capabilities.

## 5. Rights and publication decision boundary

**Current verdict: `PUBLICATION_RIGHTS_NOT_CLEARED` / fail closed.** A publicly downloadable Thunderstore ZIP, matching SHA-256, historical capture metadata, or access permission does not supply publication/re-licensing rights to the owner's original UnityFS, serialized trees or derived content. Neither this document nor a CI PASS constitutes a legal clearance. Do not infer all technical field names/metadata are automatically free of third-party rights; review the exact contemplated content, applicable license/permission, hosting terms and distribution mode.

Three separate modes must be approved independently:

| Mode | Evidence retention | Prerequisites / outcome |
| --- | --- | --- |
| 0 — Ephemeral only (current) | Runner-local minimal JSON only; no artifact/public retention | No durable LeadFactory provenance claim. Existing source-only/manual-dispatch security model remains unchanged. |
| 1 — Restricted, independently controlled retention | **Proposed, not deployed** | Require documented legal/storage basis, explicitly authorized protected destination, least-privilege ACLs, confidentiality, retention duration, deletion/revocation, integrity/retrieval checks and independent approval of new implementation. Do not claim GitHub Actions artifact retention alone is a permanent or protected archive. |
| 2 — Public minimized technical evidence | **BLOCKED** | Require documented rights review for exact payload and field names, documented distribution authorization if needed, separate owner/user publication approval, exact independent validator and durable hash/attestation binding. Absence/ambiguity of rights -> refuse. |

The following must remain prohibited without their own prior express permission: public original ZIP/UnityFS/complete serialized object trees; rehosting an unreviewed asset or dependency; publication of a raw or derived capture by repository file, Actions upload, job summary/log, cache, release, external endpoint or PR attachment; changing production capture workflow to add such an upload. A document-only Draft PR publishing this **specification** does not mean permission to publish the future **evidence payload**.

## 6. Failure taxonomy and atomic storage expectations

An eventual validator/persister MUST fail closed with explicit safe error codes, without logging sensitive serialized input:

| Failure | Required outcome |
| --- | --- |
| Source/ZIP/member/object hash, owner or exact reviewed commit mismatch | `BLOCKED_IDENTITY_MISMATCH` |
| Missing, ambiguous, unresolved or nonunique four-object reference/owner chain | `BLOCKED_PROVENANCE` |
| Extra/missing fields, unexpected semantic field names, invalid JSON, excessive actual file size or forbidden content | `BLOCKED_CONTENT_POLICY` |
| No authentic run/attempt/execution trace, unbound stored SHA or unverifiable attestation | `BLOCKED_ATTESTATION` |
| Missing authorization or unclear license/rights for that storage mode | `BLOCKED_RIGHTS` |
| Missing/unsafe destination, privacy/ACL/retention/integrity/rollback guarantees | `BLOCKED_STORAGE` |

Fail **before** writing to a destination unless all prerequisites are satisfied; any later supported implementation must use an isolated temporary/private staging area, exact precommit inspection, atomic publish/rename or equivalent transaction, read-back rehash, no partial public artifacts and idempotent rollback/deletion on failure. A `workflow_dispatch` input approval phrase is an execution guard, **not** an auditable or cryptographic substitute for separately recorded explicit user authorization. Logs must not print source bytes, output JSON or environment secrets. Independent negative tests should include unknown fields, edge surprises, mismatched SHA/commit/run, synthetic oversized stored UTF-8, rights denial, inaccessible storage and injected failures before/after staging. Synthetic tests do **not** require original assets or network.

## 7. Separate authorization sequence; no hidden side effects

All future steps need distinct scopes and fresh authority/CI/controller verification:

1. **This PR only:** document the contract, optionally future synthetic test cases; run only CI automatically triggered by this document-only PR; stop at Draft. It does not modify scripts, workflows, lock, JSON evidence or navigation.
2. **Later:** independently decide exact rights/content and available restricted/public retention destination, then authorize an isolated implementation Draft PR; test synthetically and obtain separate reviewed-head CI/pinned-merge approval. Until proven safe, keep existing capture workflow unchanged.
3. **Later:** independently authorize one exact original-byte acquisition/capture operation including package, hashes, exact workflow/code commit and explicit execution consent. An earlier conversation attachment is `NOT TRANSFERRED` until the actual bytes are available and verified. Do not request re-upload when repository-native documentation suffices.
4. **Later:** independently authorize and verify the concrete storage/publication operation after rights and integrity checks. A capture approval never implicitly authorizes publication or even private retention.
5. **Still later, independently:** decide an exact viable Offense selection/generation/materialization proof contract and any method-specific safety evidence. No selector, runtime, new hook, gameplay test or acceptance follows from static Owner provenance.

The anti-loop rule parks identical CKDIAG1/Museum, GoldenHotel and Magmatic selector/ref-result safety methods unless genuinely new authenticated evidence changes their decision fingerprint. Do not reattempt unsafe `Clear(); Add()`, hypothesized `ref __result`, owner-bypass, weight/seed manipulation or unapproved forcing. A static LeadFactory capture is a materially different provenance prerequisite, **not** a blanket substitute for selector or generation safety.

## 8. Unchanged lifecycle and PR exit criteria

No live lifecycle transition in this Draft. `S1.42AK` stays sole `ACCEPTED_FULL_NORMAL_STACK`; `S1.42AK-BMDSFIX1` stays `ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED` with its distinct passive **selector-free Black Mesa x DeepSewersFlow** proof outstanding/unwaived. Offense proof/owner residual **21 = 9 viable/equal-100 lacking trusted own generation + 12 owner-hard-blocks**. Museum/CKDIAG1 five guarantees remain UNPROVEN/BLOCKED/REFUSED; TSDIAG1 inactive/NEVER ACCEPT/no rerun. GoldenHotel and Magmatic static assets are not generation PASS. Herobrine and BCMER/Pikmin are deferred.

`BuildSpecs/current.json` remains disabled / `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`; `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`. No normalizer, LLL, source, package, profile, controllers, Gale import, build, runtime test, owner availability, acceptance or canonical `next_action` mutation is authorized.

**Document-only Draft review gate:** exactly this one new Markdown contract; no source/code/workflow, original, evidence JSON, profile or controller diff. Verify actually triggered `pull_request` CI on the **exact final PR head**. Stop with Draft still open. Draft removal, pinned-head merge and a later permanent exact-resulting-main `push` Knowledge Architecture run all require their own independent express authorization. Historical `PR-STAGED` text must not be interpreted as live authority after any later integration.
