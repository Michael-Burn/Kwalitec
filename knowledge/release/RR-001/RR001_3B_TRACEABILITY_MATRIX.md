# RR-001.3B — Traceability Matrix

**Programme:** RR-001 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3B — Educational Orientation & Reflection Coherence  
**Date:** 2026-07-28  
**Authority:** DG-001.3 · DG-001.4 · EGC-001

---

## 1. Remediation package → implementation

| Package | Clause focus | Implementation evidence | Status |
|---------|--------------|-------------------------|--------|
| **EGC-R03** | Help orientation map (D04; D10; ED-04; ED-08) | `help.html` journey + glossary + topics; Sensei handoff; anxiety phrasing softened | **Implemented** |
| **EGC-R04** | Reflection family map (D01–D08; CP-05; ED-03) | Help map sentence + kinds; onboarding map; Session reflection + Guided preview naming | **Implemented** |
| **EGC-R05** | Product Check-in rename (D05; §11.5; ED-18) | `checkin.html` H1 + disclosure; rejected “daily reflection”; tests | **Implemented** |

---

## 2. NCR → evidence

| NCR | Required remediation | Evidence | Closure |
|-----|----------------------|----------|---------|
| **NCR-011** | Educational glossary + map; soften anxiety | Help orientation / glossary / topics; no “closest to being tested on”; `test_rr001_3b_*` | **Closed** |
| **NCR-017** | Publish map; rename Check-in; keep optionality | Help + onboarding map; Check-in rename; preview honesty retained | **Closed** |
| **NCR-022** | Rename; remove Reflection from title | Check-in H1 “Product Check-in”; tests assert no “Daily Reflection” | **Closed** |
| NCR-021 *(advance)* | First-introduction in Help + onboarding | Journal/Timeline/Sensei memory taught in Help journey + onboarding map | **Advanced** (orientation path) |
| NCR-008 *(advance)* | Teach Sensei reflection without FL jargon | Help Sensei reflection kind; no “Feedback Loop” student label | **Advanced** |

---

## 3. DG-001.3 decisions → product

| Decision | Product evidence |
|----------|------------------|
| **D01** One reflection system | Help “One reflection family”; single map sentence |
| **D02** Journal sole durable memory | Help glossary + journey; Session framing ≠ Journal |
| **D03** Sensei owns reflection meaning | Study Sensei named in Help / Session / onboarding map |
| **D05** Non-reflections named | Product Check-in, Calibration, Revision listed as not reflection |
| **D07** Guided preview honesty | Home preview disclaimer retained + strengthened |
| **RG-11 / RG-20** Check-in naming | “Daily Reflection” removed from student H1 |

---

## 4. Constitution / checklist

| Clause | Result |
|--------|--------|
| CP-05 Reflection coherence | **Addressed** on Help + orientation surfaces |
| CP-03 / CI-01 Lexicon | Glossary uses canonical terms; Check-in ≠ reflection |
| CI-03 Non-reflection | Product Check-in disclosure |
| CP-06 Anxiety-safe (ED-08) | Help Session FAQ softened |
| CP-09 Orientation completeness | Journey map published |
| V5 Reflection family qualifiers | Session reflection / Guided Reflection preview / Sensei reflection qualified |

---

## 5. Outstanding questions

| ID | Disposition after RR-001.3B |
|----|----------------------------|
| **OQ-R02** When to publish Help reflection map | **Closed** — published in Help + onboarding |
| **OQ-R03** RIP-001 Daily Reflection rename | **Closed** — student H1 is Product Check-in |
| **OQ-03** Feedback Loop student-visible name | **Open** — Sensei reflection taught; FL jargon still unpublished by design |

---

## 6. Out of scope (explicit)

Mission Intelligence algorithms · recommendation scoring · curriculum · schema · architecture · feature flags · Journal/Timeline capture logic · History bridge (EGC-R06) · Journal empty tip (EGC-R12).

---

## 7. Test traceability

| Requirement | Test |
|-------------|------|
| Map sentence Board authority | `test_reflection_map_sentence_matches_board_authority` |
| Help ecosystem + glossary | `test_help_teaches_educational_ecosystem` |
| Acceptance Q&A | `test_help_answers_acceptance_questions` |
| Check-in rename | `test_product_checkin_never_titled_reflection` + RIP-001 HTTP tests |
| Session reflection framing | `test_session_reflection_framing_aligns_with_architecture` |
| Guided preview naming | `test_guided_reflection_preview_named_on_home` |
| Onboarding map | `test_onboarding_publishes_reflection_family_map` |
