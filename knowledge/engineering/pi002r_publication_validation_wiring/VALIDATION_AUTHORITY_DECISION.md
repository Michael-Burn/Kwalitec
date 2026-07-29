# Validation Authority Decision

**Programme:** PI-002R  
**Phase:** 1 — Validation Authority

---

## Decision

**Single authoritative curriculum for Founder publication:**

> CIP / Foundation extraction → `StructurePreparationService` → Curriculum Management `ValidationPolicy`

Studio `validation_passed` is set **only** when Management validation passes after structure preparation.

---

## Why this authority

| Candidate | Role | Publication gate? |
|---|---|---|
| CIP / Foundation parsed structure | Founder-visible curriculum (topics, sections, objectives) | Input to preparation |
| Structure Preparation | Syncs extraction into workspace + assigns default blueprints | Required prelude |
| Curriculum Management ValidationPolicy | Package / syllabus / blueprint safety | **Yes — authority** |
| Curriculum Ingestion (reference-only stub) | Historical parallel path; fabricates `topic-e-1` | **No** |
| Curriculum Ingestion (with real `entries`) | Optional structural engine when populated | Advisory / AND-gate only when authoritative |

---

## Rejected alternatives

### B — Feed CIP into Ingestion
Harder operationally; risks coupling CIP shapes into Ingestion documents. Deferred. Deterministic Management gates already enforce publication safety.

### C — Management-only with Ingestion always advisory
Chosen as the Founder default. Ingestion remains available for jobs that carry real `entries` / objectives; stubs are never authoritative.

---

## Explicit non-goals

- Do **not** set `validation_passed=True` without Management validation
- Do **not** remove blueprint / package / syllabus rules
- Do **not** redesign Educational Intelligence, Runtime Integration, LP-001, VP-001, or Curriculum Authority

---

## Implementation anchors

| Behaviour | Location |
|---|---|
| Prepare structure before validate | `ValidationService.validate_curriculum` → `StructurePreparationService` |
| Skip reference-only Ingestion start | `WorkspaceService.upload_sources`, `DocumentUploadService._link_workspace_sources` |
| Ignore non-authoritative jobs | `_ingestion_job_is_authoritative` |
| Management gate | `CurriculumManagementPort.validate_version` |

---

## Statement

The Founder must never review CIP-extracted curriculum while the publication engine validates a disposable Ingestion stub. After PI-002R, that mismatch cannot occur on the Founder upload path.
