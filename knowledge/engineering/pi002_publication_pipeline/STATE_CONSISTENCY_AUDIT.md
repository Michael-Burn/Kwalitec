# State Consistency Audit

**Programme:** PI-002  
**Scope:** Places where UI / messaging disagree with underlying workflow state

---

## Register

| ID | UI / message | Underlying truth | Severity | Root link |
|---|---|---|---|---|
| SC-1 | Validate flash: “blocking findings remain… Review findings below” | Findings list empty; `error_count=0` | Critical | `_map_report` ignores `issues[]`; ValidationError uses summarised error_count |
| SC-2 | Intelligence / overview: “0 validation errors” | Ingestion report has blocking `missing_objectives` | Critical | Same mapper + separate CIP validation counters |
| SC-3 | Validation card: `in_progress` while flash says failed/blocking | Fact `validation_passed=False`; ingestion failed | High | Mis-mapped report → `IN_PROGRESS` not `FAILED` |
| SC-4 | Document slots Ready + structure topics present | Studio validation still fails | High | CIP Ready ≠ Ingestion/Management validation pass |
| SC-5 | Preview success flash with N topics | Preview readiness `not_ready` | Critical | Success keyed on `node_count`; readiness keyed on `validation_passed` |
| SC-6 | Preview / Structure topic counts disagree | Different projections (CIP vs Management refs vs stub ingestion) | Medium | Multiple structure authorities |
| SC-7 | Approve action → Publish refusal flash | Exception is approval prerequisite failure | Critical | `recover_flash(PublicationError)` defaults to publish copy |
| SC-8 | Version history may show `preview_ready` | Checklist still missing validation/approval facts | High | Management state advanced; Studio facts not |
| SC-9 | Checklist lifecycle maps `preview_ready`/`validated`/… to `READY` | Student Ready requires published Foundation package | High | `PublicationChecklistService._map_management_state` |
| SC-10 | NEXT STEP stuck on validate/upload guidance | Documents already Ready; topics extracted | Medium | Workflow stage / guidance not driven by document+CIP facts |
| SC-11 | Publish refused (correct) but after rollback fact may flip | Publish did not succeed | Low | Rollback ensured before assert_ready |
| SC-12 | Subjects show Validation / non-Ready after “successful” mid-journey UX | Never published | Critical | Expected consequence of SC-1 chain |

---

## Patterns

1. **Success of a side effect ≠ gate satisfaction** (Preview build vs preview readiness; document Ready vs validation_passed).
2. **Exception type → wrong product verb** (Approve → “couldn’t publish”).
3. **Authority split without a single projection** (CIP / Ingestion / Management / Foundation / Studio facts).
4. **Opaque DTO key mismatch** (`issues` vs `errors`) hides real failures.

---

## Evidence anchors

- FV-001B Re-run LB-R1…LB-R5  
- `_evidence/complete.json` phases C2–C5  
- `operator_guidance.py`, `view_models.py`, `validation_service._map_report`, `preview_summary.py`, `publication_checklist_service.py`
