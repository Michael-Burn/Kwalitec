# Recommended Remediation Plan

**Programme:** PI-002 follow-on (not authorised for implementation in PI-002)  
**Principle:** Fix the root cause; do not weaken safety gates; do not bypass Approve/Publish.

---

## Goal

Make the existing publication model work on the Founder path:

```text
Upload → Extraction → Validate → Preview → Approve → Publish → Ready
```

with honest state, honest findings, and honest flashes.

---

## Phase 0 — Acceptance criteria for any fix

A remediation is done only when a Founder can, without assistance:

1. Upload Official CMP + Syllabus to Ready  
2. See extracted structure  
3. **Validate successfully** with findings consistent with pass/fail  
4. Build preview that is both successful **and** `ready_for_review` when validation passed  
5. Approve with an Approve success message  
6. Publish successfully  
7. Subjects hub shows Ready + Current Version + Published Date  
8. Student Subject Catalogue discovers Ready  

Re-run **FV-001B** after remediation. Do not advance to FV-001C until GO / GO WITH CONDITIONS.

---

## Phase 1 — Fix primary root cause (Validation inputs)

**Target:** `validation_passed` becomes true when Management structural gates pass **and** Founder-facing extracted curriculum is coherent — without validating disposable stub jobs as if they were the curriculum.

### Recommended options (choose one; prefer A)

**A. Stop AND-gating the reference-only Ingestion stub (preferred)**  
- Do not start Curriculum Ingestion from `upload_sources` with empty `entries`, **or**  
- Do not require Ingestion pass in `validate_curriculum` unless the job was populated from real normalised structure / CIP output.  
- Keep Management `ValidationPolicy` intact (package, syllabus, blueprints).  
- Prefer validating against CIP/Foundation-prepared structure already used by `StructurePreparationService`.

**B. Feed real structure into Ingestion**  
- When starting ingestion, pass CIP-derived entries/objectives so the engine validates the same curriculum the Founder sees.  
- Ensure `subject_code` metadata satisfies ingestion rules.  
- Harder operationally; must stay deterministic (no LLM in core path).

**C. Explicit Founder-facing validation authority**  
- Define Studio validation SSOT as Management (+ structure preparation), with Ingestion as advisory until wired.  
- Document the authority boundary in ARCHITECTURE notes.

**Do not:** set `validation_passed=True` without running Management validation.  
**Do not:** remove blueprint / package / approval requirements.

### Tests

- Integration: upload CMP+syllabus fixtures → prepare → validate → `validation_passed=True`  
- Regression: empty package still fails Management validation  
- Regression: missing blueprints still fail until preparation assigns them  

---

## Phase 2 — Fix findings projection (honesty)

- Update `_map_report` to consume `issues` (and keep `errors` / `blocking_issues` for compatibility).  
- Map severities to Studio findings; surface blocking issues in the Validation findings panel.  
- Ensure failed validate produces readiness `failed` (not `in_progress`) when `passed=False`.  
- Fix or remove the “0 validation errors” overlay when Studio/Management/Ingestion blocking issues exist.  
- Consider projecting Management `latest_validation` correctly from the adapter (VersionSnapshot currently omits it).

### Tests

- Given an opaque report with `issues=[{severity:blocking}]`, summarise shows ≥1 error and `blocks_publication`.  
- Flash + findings panel agree.

---

## Phase 3 — Fix Preview / Approve / Publish messaging (consistency)

- Preview success flash only when readiness is `ready_for_review` (or explicitly say “topics loaded; validation still required”).  
- `recover_flash`: Approve failures must use Approve copy; include branches for `validation` / `approval` PublicationErrors.  
- NEXT STEP / stage guidance should follow facts (documents Ready + structure) not only workflow stage chrome.

### Tests

- Presentation tests for flash mapping (Approve ≠ Publish copy).  
- `friendly_preview_summary` never implies ready when `not_ready`.

---

## Phase 4 — Ready path verification

After Phases 1–3:

- Approve → Management `approved` + `preview_approved`  
- Publish → rollback + Management `published` + Foundation package  
- Catalogue Ready + Subjects hub columns  

Add an end-to-end Studio test (or founder walk script) covering the full chain with real adapters (not only `seed_publishable` shortcuts).

---

## Phase 5 — Hardening (follow-ups, not blockers for first GO)

- Persist StudioRegistry / Management catalogue **or** document single-process limitation explicitly for production topology.  
- Align checklist lifecycle labels so mid-pipeline Management states are not labelled student “READY”.  
- Avoid setting `blueprint_assigned=True` when assign threw (treat “already assigned” distinctly from hard failure).  
- Revisit publish ordering: do not create rollback fact before readiness assert (or clearly label it as prepare-only).

---

## Out of scope (reaffirm)

- Educational Intelligence redesign  
- Runtime Integration / LP-001 / VP-001 / Curriculum Authority redesign  
- Student Digital Twin changes  
- Temporary bypasses of validation, approval, or publish safety  

---

## Suggested programme naming

Implement under a dedicated remediation programme (e.g. **PI-002R — Publication Validation Wiring**) with FV-001B re-run as the exit gate.

---

## Priority order

1. Phase 1 (root cause)  
2. Phase 2 (findings honesty)  
3. Phase 3 (messaging consistency)  
4. Phase 4 (e2e Ready proof)  
5. Phase 5 (hardening)
