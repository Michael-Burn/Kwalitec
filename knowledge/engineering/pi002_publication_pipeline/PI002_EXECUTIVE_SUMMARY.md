# PI-002 — Publication Pipeline Root Cause Investigation

**Programme:** PI-002  
**Status:** Complete (investigation only — no remediation implemented)  
**Date:** 2026-07-29  
**Trigger:** FV-001B (Re-run) second consecutive **NO-GO**

---

## Verdict

The publication pipeline fails at the **Validation** stage.

The earliest incorrect state transition is:

```text
validation_passed: False  ↛  True
```

After Official CMP and Official Syllabus are Ready and CIP extraction has produced Founder-visible topics, **Validate Curriculum** still cannot set `WorkspacePublicationFacts.validation_passed = True`.

Everything downstream (Preview readiness, Approval, Publication, Subject Catalogue Ready) is blocked by that missing fact.

---

## Root cause (primary)

**Curriculum Ingestion is started from document upload with synthetic stub content, then AND-gated into Studio validation — while Founder-visible structure comes from a separate CIP/Foundation path.**

Evidence (reproduced against production adapters, 2026-07-29):

1. `DocumentUploadService` → `WorkspaceService.upload_sources(..., start_ingestion=True)` registers an Ingestion job whose documents contain only opaque references.
2. `CurriculumIngestionAdapter` synthesises a placeholder topic (`Untitled` / `topic-e-1`) when sources have no entries.
3. Ingestion validation fails with blocking `missing_objectives` (and related issues under key `issues`).
4. Studio `ValidationService.validate_curriculum` requires **both** Ingestion pass **and** Management pass.
5. Management can pass (assets + blueprints present) while Ingestion fails → Studio raises `ValidationError("Validation failed … 0 error(s)")`.
6. `validation_passed` remains `False`.

This matches FV-001B Re-run `complete.json` → `C2_validate` flash text exactly.

---

## Amplifying defects (not the first failure)

| Defect | Effect |
|---|---|
| Studio `_map_report` reads `errors` / `blocking_issues`, but Ingestion/Management reports use `issues` | UI shows **0 validation errors** and empty findings while validation failed |
| Preview success gated only on `node_count > 0`; readiness requires `validation_passed` | Success flash + `not_ready` |
| Approve `PublicationError("…validation")` mapped by `recover_flash` to **publish** copy | Approve looks like Publish failure |
| Ready requires Management publish + Foundation package | Never reached because publish checklist still needs `validation_passed` + `preview_approved` |

---

## What is not the root cause

- Educational Intelligence redesign
- Runtime Integration / LP-001 / VP-001 / Curriculum Authority model changes
- Weakening of publication safety gates
- “Preview has no package” as the first failure (topics exist; readiness is false because validation never passed)
- UX copy alone (copy is contradictory because state and report mapping are wrong)

---

## Dependency chain

```text
Upload starts stub Ingestion job (failed validation report)
        ↓
Validate AND-gates Ingestion + Management
        ↓
validation_passed stays False          ← FIRST FAILED TRANSITION
        ↓
Preview builds topics but stays not_ready
        ↓
Approve refuses (requires validation_passed)
        ↓
Publish refuses (checklist incomplete)
        ↓
Subject Catalogue Ready never materialises
```

---

## Deliverables

| Artefact | Purpose |
|---|---|
| [`PUBLICATION_STATE_MACHINE.md`](PUBLICATION_STATE_MACHINE.md) | All publication / workflow states |
| [`VALIDATION_INVESTIGATION.md`](VALIDATION_INVESTIGATION.md) | Validation inputs/outputs/contradictions |
| [`PREVIEW_PIPELINE_REPORT.md`](PREVIEW_PIPELINE_REPORT.md) | Preview / readiness |
| [`APPROVAL_PIPELINE_REPORT.md`](APPROVAL_PIPELINE_REPORT.md) | Approval prerequisites |
| [`PUBLICATION_TRACE_REPORT.md`](PUBLICATION_TRACE_REPORT.md) | Publish request → Ready |
| [`READY_STATE_ANALYSIS.md`](READY_STATE_ANALYSIS.md) | How Ready is defined |
| [`STATE_CONSISTENCY_AUDIT.md`](STATE_CONSISTENCY_AUDIT.md) | UI vs workflow contradictions |
| [`ROOT_CAUSE_ANALYSIS.md`](ROOT_CAUSE_ANALYSIS.md) | Earliest failure + propagation |
| [`RECOMMENDED_REMEDIATION_PLAN.md`](RECOMMENDED_REMEDIATION_PLAN.md) | Fix plan (not implemented) |

---

## Evidence sources

- FV-001B Re-run: `knowledge/product/fv001b_rerun_validation/` (`FINAL_VERDICT.md`, `LAUNCH_BLOCKERS.md`, `_evidence/complete.json`)
- Code: `app/application/curriculum_studio/validation_service.py`, `document_upload_service.py`, `workspace_service.py`, `preview_service.py`, `publication_service.py`
- Adapters: `app/infrastructure/adapters/curriculum_ingestion/adapter.py`, `curriculum_management/adapter.py`
- Domain gates: `app/application/curriculum_management/policies/validation_policy.py`
- Live reproduction script results captured in investigation notes (same process as above)

---

## Next step

Authorise a **remediation programme** only after accepting this root cause. Do not patch Approve/Publish messaging or Ready bridging first — they are downstream of the Validation fact never flipping true.
