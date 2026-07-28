# EI-002 Completion Report — Curriculum Extraction Pipeline

**Programme:** EI-002 — Curriculum Extraction Pipeline (Educational Intelligence)  
**Date:** 2026-07-28  
**Status:** Complete  
**Commits:** `b13b2ba` (`feat(ei-002)`) · `e03fd54` (`docs(ei-002)`)  

---

### Summary

EI-002 implements the Curriculum Extraction Pipeline that transforms Canonical Structured Documents (IFoA CMP + Syllabus) into a Draft Curriculum Knowledge Graph compatible with EI-001. The pipeline is modular (import → parse → segment → extract → relationships → construct → validate → draft persist), preserves full source traceability and extraction confidence, and writes only `publication_state=draft` on `ckg_graph_editions`. PDF support is infrastructure-only via `PdfCanonicalAdapter`. No Twin, mission, recommendation, Founder UI, publish, or student runtime integration.

---

### Files Created

- `app/domain/curriculum_extraction/` (CSD, confidence, provenance, validation, publication state)
- `app/application/curriculum_extraction/` (pipeline stages + `CurriculumExtractionEngine`)
- `app/infrastructure/adapters/curriculum_extraction/` (`PdfCanonicalAdapter`)
- `migrations/versions/202607280020_ei002_curriculum_extraction.py`
- `tests/domain/curriculum_extraction/`
- `tests/application/curriculum_extraction/`
- `knowledge/educational_intelligence/ei002_curriculum_extraction_pipeline/ARCHITECTURE.md`
- `knowledge/educational_intelligence/ei002_curriculum_extraction_pipeline/EI002_COMPLETION_REPORT.md` (this report)

---

### Files Modified

- `app/models/curriculum_knowledge_graph.py` — draft fields; `CkgNodeProvenance`; `CkgValidationReport`
- `app/models/__init__.py` — export new ORM models
- `app/__init__.py` — register new ORM models
- `.cursor/rules/99-CURRENT_MILESTONE.md` — EI-002 delivery window
- `knowledge/operations/oa001/PROGRAMME_DASHBOARD.md` — Educational EI-002 row

---

### Tests Executed

```bash
python3 -m pytest tests/domain/curriculum_extraction/ \
  tests/application/curriculum_extraction/ \
  tests/domain/curriculum_knowledge_graph/ -v
python3 -m ruff check app/domain/curriculum_extraction \
  app/application/curriculum_extraction \
  app/infrastructure/adapters/curriculum_extraction \
  app/models/curriculum_knowledge_graph.py \
  tests/domain/curriculum_extraction \
  tests/application/curriculum_extraction \
  migrations/versions/202607280020_ei002_curriculum_extraction.py
```

Outcome: **49 passed** (13 EI-002 + 36 EI-001 regression); ruff clean on EI-002 paths.

---

### Migration Impact

Alembic revision `202607280020` (revises `202607280010`):

- Adds `publication_state`, `validation_status`, `source_cmp_ref`, `source_syllabus_ref` on `ckg_graph_editions`
- Adds `ckg_node_provenance`
- Adds `ckg_validation_reports`

No changes to V1/V2 curriculum engine tables, CIP, Twin, or student runtime schema. Reversible via `downgrade()`.

---

### Architecture Compliance

- Layering preserved: domain → application → infrastructure adapter; ORM under `app/models/`.
- Educational Intelligence consumes CSD only; PDF adapter is infrastructure-only.
- Curriculum V1/V2 loaders, import paths, and `CurriculumService` traversal **untouched**.
- CIP stage contracts **untouched**.
- CKG remains additive SoT; drafts unpublished; no student visibility.
- Architecture verdict: **Pass** for in-scope extraction.

---

### Technical Debt

- Heuristic parsers are deterministic but CMP-format sensitive; real IFoA CMP PDFs will need adapter + cue tuning.
- Replace-on-reextract deletes by subject-code prefix; multi-subject shared namespaces are out of scope.
- Explicit prerequisite cues resolve via numbered hosts → first LO under host (not full LO-code alignment).

---

### Known Limitations

- Does not implement Founder approval / publish workflows.
- Does not wire CKG into student plans, Twin, missions, or recommendations.
- Does not seed a full production IFoA subject from official PDFs in-repo (fixtures are CSD).
- Confidence is Founder-facing only; no UI yet.

---

### Student Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| Student problem | Runtime still uses V1/V2; students do not consume draft CKG |
| Student benefit | Indirect — enables future Founder-reviewed educational SoT |
| Learning benefit | Structured curriculum model with traceable origins |
| Success metrics | Pipeline tests green; draft edition persists with provenance |
| Risks | Dual-model confusion until publish/cutover programmes |
| Assumptions | Future EI programmes will review/publish drafts into student paths |

Template reference: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`.

---

### Estimated KSI contribution

**ΔKSI = 0** — educational intelligence infrastructure only; no student-facing behaviour change. K1–K8 unchanged.

---

### Evidence collected

- `tests/domain/curriculum_extraction/`
- `tests/application/curriculum_extraction/`
- Architecture doc in this folder
- Migration `202607280020_ei002_curriculum_extraction.py`

---

### Lessons learned for student value

Curriculum understanding must be acquired as structured educational knowledge with permanent provenance **before** Founder publish and student exposure. Keeping drafts unpublished protects students from unverified extraction artefacts.

---

### Explainability Review

**N/A** — no student-facing intelligence surfaces changed.

---

### Recommendation Quality Review

**N/A** — no recommendation ranking/selection changed.

---

### Version 1 readiness residual

**N/A** — does not claim Version 1 production-ready progress. Residual gates unchanged.

---

### CRI domains improved

**None** — extraction foundation only; no Commercial Quality domain movement.

### Estimated CRI delta

**ΔCRI = 0** — docs/domain/infra without student-facing CRI evidence.

### Evidence supporting the increase

N/A (delta zero).

### Remaining blockers

Unchanged vs Commercial Readiness Board / FV-001 constraints.

### Provisional or validated

N/A (no CRI claim).

---

**End of EI-002 Completion Report**
