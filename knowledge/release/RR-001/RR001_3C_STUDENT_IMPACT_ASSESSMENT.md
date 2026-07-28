# RR-001.3C — Student Impact Assessment

**Programme:** RR-001 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3C — Educational Memory & History Coherence  
**Date:** 2026-07-28  
**Template:** `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

---

## Student problem

Students encountered three memory-like surfaces — Decision Journal, Educational Timeline, and History — without a single mental model. Journal empty states said “Mission tip” and advertised Quick Check while gated OFF. Timeline narrative still used tip language. History presented accuracy/progress culture without stating that educational meaning lives in Journal/Timeline, so stats competed with Sensei memory (ED-05 / AC-03). First introduction of educational memory was incomplete on onboarding/empty surfaces (NCR-021 residual after RR-001.3B Help).

## Student benefit

- One sentence that defines Journal (durable memory), Timeline (chronological story from Journal), and History (practice context).  
- Empty states that teach the same model without tip language or gated-feature ads.  
- History always bridges to Journal/Timeline for “what it meant / what was learned / future guidance.”  
- Onboarding and Help introduce the memory system before students drown in stats.

## Learning benefit

Students can trust that Study Sensei remembers significant guidance in one place (Journal), can re-read their learning story over time (Timeline), and can use History for practice archives without mistaking numbers for mentor truth. Reflections remain coherent with DG-001.3: Session notes stay with the Session; Sensei reflection deepens Journal memory.

## Success metrics

| Metric | Target | Evidence |
|--------|--------|----------|
| Acceptance questions answerable | All six WP memory questions | Help + 3C tests |
| Journal empty free of tip / QC | 0 “Mission tip”; 0 Quick Check ad | DTO + route tests |
| History bridge present | Always-visible epistemology copy | History route test |
| Distinct Journal ≠ Timeline ≠ History | Explicit “not a second memory store” | Timeline DTO + Help |
| Regression green | Pass | 117 tests |

## Risks

| Risk | Mitigation |
|------|------------|
| History bridge ignored if students skip past intro | Repeated on empty History and in Help FAQ |
| Onboarding skip misses memory step | Help memory panel + Journal/Timeline empties |
| Longer Help increases load | Progressive disclosure for FAQs; scannable memory panel |

## Assumptions

- Students who open History will read the lead bridge section.  
- Quick Check remains OFF for Alpha; empty honesty must not advertise it.  
- Feedback Loop jargon name (OQ-03) stays unpublished; Sensei reflection is the student label.

## Estimated KSI contribution

| Category | Δ | Rationale |
|----------|---|-----------|
| K1 Continuity | +2 | Memory surfaces form one continuous story |
| K2 Recommendations | 0 | Ranking unchanged |
| K3 Planning | 0 | Sequencing unchanged |
| K4 Practice | 0 | Session workflow unchanged |
| K5 Mastery honesty | +2 | Stats vs meaning epistemology fixed |
| K6 Calm / trust | +1 | Empty honesty; no gated ads |
| K7 Agency | +1 | Clear where to look after reflection |
| K8 Explainability | +2 | Memory model teachable |
| **Net ΔKSI** | **+8 (estimated)** | Copy-heavy; not validated cohort KSI |

## Evidence collected

- `tests/presentation/student/test_rr001_3c_educational_memory.py`  
- Journal / Timeline / History / Help / onboarding / 3A / 3B regressions  
- `RR001_3C_TRACEABILITY_MATRIX.md`

## Lessons learned for student value

Teaching “History is not Timeline” only in Help is insufficient — the History page itself must say so every visit. Empty states are first-introduction surfaces and must not reintroduce deprecated nouns.

## Explainability Review

N/A for ranking engines. Epistemology explainability improved (History context vs Sensei meaning). No new opaque scores.

## Recommendation Quality Review

N/A — recommendation selection/scoring untouched.
