# RR-001.3C — Traceability Matrix

**Programme:** RR-001  
**Work Package:** RR-001.3C — Educational Memory & History Coherence  
**Date:** 2026-07-28  
**Authority:** DG-001.2 · DG-001.3 · DG-001.4 · EGC-001

---

## NCR → evidence

| NCR | Requirement | Implementation | Status |
|-----|-------------|----------------|--------|
| NCR-006 | Journal empty tip / QC honesty | `decision_journal/dto.py` empty_description; journal template | **Closed** |
| NCR-007 | Timeline tip + stats tension | Timeline DTO; `narrative.py` tip retirement; History bridge | **Closed** |
| NCR-010 | History epistemology bridge | `history.html` bridge; shell descriptions; Help FAQ | **Closed** |
| NCR-019 | Memory authority ownership | Journal/Timeline Sensei memory; History SY+KW context + SS bridge | **Closed** |
| NCR-021 | First-introduction consistency | Onboarding memory step; Help memory model; empty intros | **Closed** |

---

## Package → clauses → surfaces

| Package | Clauses | Surfaces | Result |
|---------|---------|----------|--------|
| **EGC-R06** | D06; ED-05; CP-07; CP-08; AC-03 | History, Timeline, Help, narrative | Implemented |
| **EGC-R07** *(memory)* | D07; ED-14 | Journal empty (no QC ad) | Implemented (memory scope) |
| **EGC-R12** *(memory)* | ED-14; DEP-01; CP-07 | Journal/Timeline/History empties | Implemented (memory scope) |

---

## Acceptance criteria → evidence

| Student question | Where answered | Test |
|------------------|----------------|------|
| What is the Decision Journal? | Help FAQ + Journal intro + glossary | `test_help_teaches_educational_memory_model` |
| What is Timeline? | Help FAQ + Timeline intro + glossary | same |
| Why different? | Help FAQ + memory model sentence | same + onboarding |
| Why does History exist? | Help FAQ + History bridge | `test_history_route_epistemology_bridge` |
| How does Sensei remember? | Help + onboarding memory step | `test_onboarding_introduces_educational_memory` |
| After Reflection? | Help FAQ + memory model sentence | Help test |
| No Reflection Architecture contradiction | Session notes ≠ Journal; Sensei reflection optional | Help / model sentence |
| No duplicate memory concepts | Timeline “not a second memory store” | DTO + Help + Timeline empty |

---

## Authority ownership (DG-001.2)

| Surface | Owner | Evidence |
|---------|-------|----------|
| Decision Journal | Study Sensei (durable memory) | eyebrow + intro |
| Educational Timeline | Study Sensei (interpretation) | eyebrow + intro |
| History stats / archives | System + Kwalitec context | bridge copy |
| History → memory links | Sensei bridge only | Journal/Timeline CTAs |

---

## Out of scope (explicit)

Mission Intelligence algorithms · recommendation scoring · curriculum · schema · architecture · feature flags · reflection capture logic · Help orientation beyond memory · Calibration · Notifications · Home Mission generation · NCR-013 non-memory empties · NCR-002 Home density.
