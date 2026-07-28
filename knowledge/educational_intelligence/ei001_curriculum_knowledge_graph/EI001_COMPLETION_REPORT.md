# EI-001 Completion Report — Curriculum Knowledge Graph Foundation

**Programme:** EI-001 — Curriculum Knowledge Graph Foundation (Educational Intelligence)  
**Date:** 2026-07-28  
**Status:** Complete  
**Commits:** `2bcc3d2` (`feat(ei-001)`) · *(docs hash recorded in this commit)*  

> Disambiguation: this is **not** the historical Engineering Improvements programme at `knowledge/release/EI-001/`.

---

### Summary

EI-001 designs and implements the Curriculum Knowledge Graph (CKG): an additive educational domain model and normalised persistence layer capable of representing any IFoA subject at subsection-level precision (`Subject → Topic → Section → Subsection → Learning Objective`), plus educational objects, typed relationships, and edition-stable curriculum ids. No extraction, Twin, mission, or UI work was performed. V1/V2 Curriculum Engine and CIP tables remain untouched; CKG is the target Single Source of Educational Truth for future EI programmes.

---

### Files Created

- `app/domain/curriculum_knowledge_graph/` (package: entities, value objects, graph aggregate)
- `app/models/curriculum_knowledge_graph.py`
- `migrations/versions/202607280010_ei001_curriculum_knowledge_graph.py`
- `tests/domain/curriculum_knowledge_graph/` (stable ids, entities/graph, purity, ORM)
- `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/ARCHITECTURE.md`
- `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/DOMAIN_MODEL.md`
- `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/RELATIONSHIPS.md`
- `knowledge/educational_intelligence/ei001_curriculum_knowledge_graph/EI001_COMPLETION_REPORT.md` (this report)

---

### Files Modified

- `app/models/__init__.py` — export CKG ORM models
- `app/__init__.py` — register CKG models with SQLAlchemy metadata
- `.cursor/rules/99-CURRENT_MILESTONE.md` — EI-001 delivery window
- `knowledge/operations/oa001/PROGRAMME_DASHBOARD.md` — Educational EI-001 row

---

### Tests Executed

```bash
python3 -m pytest tests/domain/curriculum_knowledge_graph/ -v
python3 -m ruff check app/domain/curriculum_knowledge_graph \
  app/models/curriculum_knowledge_graph.py \
  tests/domain/curriculum_knowledge_graph \
  migrations/versions/202607280010_ei001_curriculum_knowledge_graph.py
```

Outcome: **36 passed**; ruff clean on new CKG paths.

---

### Migration Impact

Alembic revision `202607280010` adds `ckg_*` tables and merges heads `202607190002` + `202607280002`.  
No changes to V1/V2 curriculum engine tables, CIP, Twin, missions, or student runtime schema. Reversible via `downgrade()` dropping `ckg_*` tables.

---

### Architecture Compliance

- Layering preserved: pure domain under `app/domain/`; ORM under `app/models/`; no HTTP/UI.  
- Curriculum V1/V2 loaders, import paths, and `CurriculumService` traversal **untouched**.  
- CKG is additive parallel SoT; no cutover of student runtime.  
- Traversal/import compatibility for existing curricula: **preserved** (N/A change).  
- Architecture verdict: **Pass** for in-scope foundation.

---

### Technical Debt

- Alembic multi-head history remains complex; this migration merges two heads but does not audit the full historical graph.  
- CIP → CKG publish adapter not built (intentional).  
- No seed/import of CS1 JSON into CKG yet (intentional — no extraction/migration in this programme).

---

### Known Limitations

- Does not populate a full IFoA subject from CMP/PDFs.  
- Does not wire recommendations, missions, Twin, or student UI to CKG.  
- Does not replace V2 Section→Topic naming in the Curriculum Engine.  
- Does not clear Version 1 educational gates or raise validated KSI/CRI.

---

### Student Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| Student problem | Runtime still uses V1/V2; students do not yet consume CKG |
| Student benefit | Indirect foundation for future subsection-precise guidance |
| Learning benefit | Enables future explainable structure-aware study guidance |
| Success metrics | Domain+ORM tests green; subsection-level model expressible |
| Risks | Dual-model confusion until cutover programme |
| Assumptions | Future EI programmes will publish into / consume CKG |

Template reference: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` (sections covered above).

---

### Estimated KSI contribution

**ΔKSI = 0** — infrastructure/domain foundation only; no student-facing educational behaviour change. K1–K8 unchanged.

---

### Evidence collected

- `tests/domain/curriculum_knowledge_graph/` (36 tests)  
- Architecture / domain / relationships docs in this folder  
- Migration `202607280010_ei001_curriculum_knowledge_graph.py`

---

### Lessons learned for student value

Educational intelligence needs a permanent subsection-level model *before* extraction or Twin reasoning. Shipping the SoT without cutting over runtime avoids breaking daily study while unlocking future programmes.

---

### Explainability Review

**N/A** — no student-facing intelligence surfaces changed.

---

### Recommendation Quality Review

**N/A** — no recommendation ranking/selection changed.

---

### Version 1 readiness residual

**N/A** — does not claim Version 1 production-ready progress. Residual gates unchanged (see P-002.1 / CQ board).

---

### CRI domains improved

**None** — foundation only; no Commercial Quality domain movement.

### Estimated CRI delta

**ΔCRI = 0** — docs/domain/infra foundation without student-facing CRI evidence.

### Evidence supporting the increase

N/A (delta zero).

### Remaining blockers

Unchanged vs Commercial Readiness Board / FV-001 constraints.

### Provisional or validated

N/A (no CRI claim).

---

**End of EI-001 Completion Report**
