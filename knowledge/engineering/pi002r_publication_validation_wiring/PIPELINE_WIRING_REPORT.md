# Pipeline Wiring Report

**Programme:** PI-002R  
**Phases:** 2–6

---

## Verification matrix

| Stage | Same curriculum? | Mechanism |
|---|---|---|
| Validation | ✓ | StructurePreparation syncs CIP/Foundation → workspace; Management validates version package + blueprints |
| Preview | ✓ | Hierarchy from prepared structure; Management `preview_version` advances gate only |
| Approval | ✓ | Requires `validation_passed`; sets `preview_approved` on same workspace/version |
| Publication | ✓ | Checklist on same facts; Management `publish` on same `version_id`; Foundation bridge uses prepared structure |
| Ready | ✓ | Catalogue reflects Foundation package published from bridged version |
| Subject Catalogue | ✓ | Discovery reads active Foundation package — no independent curriculum rewrite |

---

## Stage wiring detail

### Validation
1. `prepare_for_validation` loads CIP entities / Foundation parse / workspace fallback  
2. Syncs `section_ids` / `topic_ids` / `objective_ids`  
3. Assigns default blueprints on Management version  
4. Runs Management `validate_version`  
5. Ingestion AND-gate only if job is authoritative (real entries/objectives)  
6. Sets `validation_passed` only on combined pass  

### Preview
1. `build_for_review` re-prepares structure when needed  
2. Hierarchy prefers prepared structure over Management generic refs  
3. Readiness `ready_for_review` requires `validation_passed` + nodes  
4. UI success flash requires readiness + validation  

### Approval
1. Hard-requires `validation_passed`  
2. Calls Management `preview_version` then `approve`  
3. Sets `preview_approved=True` on the same workspace facts  

### Publication
1. Ensures rollback snapshot  
2. Asserts checklist ready  
3. Management `publish` on `workspace.version_id`  
4. Foundation `PublicationBridgeService` materialises Ready from prepared structure  

### Ready / Catalogue
1. No duplicate Ready computation in Studio  
2. Subject Catalogue / discovery reads published Foundation package state  

---

## Parallel representations removed from the gate

| Representation | Before | After |
|---|---|---|
| Ingestion stub (`topic-e-1`) | AND-gated into `validation_passed` | Not started for reference uploads; ignored if non-authoritative |
| CIP structure panel | Display only | Feeds Structure Preparation → validation + preview |
| Management package assets | Parallel pass possible while stub failed | Sole publication-gate validator |

---

## Safety preserved

- Empty structure → ValidationError  
- Missing version → ValidationError  
- Approval without validation → PublicationError  
- Publish without checklist → PublicationError  
- Management ValidationPolicy unchanged (syllabus, package, blueprints)
