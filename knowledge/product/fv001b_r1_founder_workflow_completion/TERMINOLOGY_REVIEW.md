# FV-001B-R1 — Terminology Review

**Programme:** FV-001B-R1  
**Date:** 2026-07-28  
**Basis:** FV-001B `TERMINOLOGY_AUDIT.md` forbidden terms on primary Founder path

---

## Objective

Remove unnecessary Educational Intelligence terminology from the normal Founder curriculum-authoring experience. Advanced engineering tooling may retain technical terms; primary chrome must not.

---

## Replacements applied

| Before (primary chrome) | After |
|---|---|
| Curriculum Intelligence Pipeline | Document processing |
| Knowledge Graph Built | Curriculum structure built |
| Curriculum Intelligence | Curriculum review |
| Pipeline (tab) | Extraction status |
| Knowledge Graph (tab) | Curriculum structure |
| Evidence Explorer | Source evidence |
| Entity Details | Topic details |
| Metrics | Quality |
| Entities (overview metric) | Topics |
| Preview “N nodes” | Preview “N topics” |
| Pipeline updated / failed (toast) | Extraction updated / failed |
| Document N (job header) | Official CMP / Official Syllabus label |
| Audit lines containing Inference / embeddings | Filtered from Founder audit list |

Domain `FOUNDER_STAGE_LABELS` updated so processing stage chips stay Founder-aligned.

---

## Retained (appropriate Founder vocabulary)

- Official CMP / Official Syllabus
- Validate / Build Preview / Approve / Publish Verified Curriculum
- Review Queue
- Ready / Draft / Current Version
- Curriculum Authority / Subjects / Curriculum Studio

---

## Intentionally not redesigned

- CIP internal APIs, model names, and engineering routes remain (URLs may still say `intelligence` / `knowledge-graph`).
- Advanced retrieval diagnostics remain available behind review tabs; primary labels no longer advertise EI jargon.

---

## Acceptance against FV-001B criterion

> Never encounter unnecessary Educational Intelligence terminology.

**R1 status:** Primary workspace authoring chrome updated. Recommend FV-001B re-run terminology scan to confirm no remaining Knowledge Graph / Pipeline / Entity Details / Inference on the default path.
