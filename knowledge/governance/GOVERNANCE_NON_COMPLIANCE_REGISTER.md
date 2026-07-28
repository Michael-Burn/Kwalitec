# Governance Non-Compliance Register

**Programme:** EGC-001 — Educational Governance Compliance  
**Version:** 1.0  
**Status:** Active — Board non-compliance baseline  
**Effective:** 2026-07-28  
**Authority:** `EDUCATIONAL_GOVERNANCE_COMPLIANCE_AUDIT.md`  
**Constraint:** Baseline register from EGC-001; closures require implementation evidence (RR-001.3A+).

Severity: **Critical / High / Medium / Low**  
Priority: **P0 / P1 / P2 / P3**  
Status values: **Open** · **Contained** · **Watch** · **Closed**

---

## Purpose

Catalogue every **Non-Compliant** finding and material **Partially Compliant** residual that blocks product certification under DG-001.

Fully Compliant pockets are listed in the Scorecard, not here.

**RR-001.3A (2026-07-28):** Closed NCR-001, NCR-004, NCR-014 (Runtime C system narrator), NCR-015 (in-scope identity surfaces), NCR-016, NCR-018 (handoff + Home/Session), NCR-020 (in-scope). Evidence: `RR001_3A_COMPLETION_REPORT.md`, `test_rr001_3a_educational_identity.py`.

**RR-001.3B (2026-07-28):** Closed NCR-011, NCR-017, NCR-022. Evidence: `RR001_3B_COMPLETION_REPORT.md`.

**RR-001.3C (2026-07-28):** Closed NCR-006, NCR-007, NCR-010, NCR-019, NCR-021. Evidence: `RR001_3C_COMPLETION_REPORT.md`, `test_rr001_3c_educational_memory.py`.

**RR-001.3D (2026-07-28):** Closed NCR-002, NCR-003, NCR-005, NCR-008, NCR-009, NCR-012, NCR-013, NCR-014 (in-scope residual). Evidence: `RR001_3D_COMPLETION_REPORT.md`, `test_rr001_3d_educational_consistency.py`.

---

## Summary

| ID | Title | Status class | Severity | Priority | Package | RP / AC link |
|----|-------|--------------|----------|----------|---------|--------------|
| NCR-001 | Onboarding lacks Sensei handoff; KW-as-mentor | **Closed** | High | P0 | EGC-R01 | ED-01; ED-20; AC-01 |
| NCR-002 | Home authority unnamed; tip/Session collision; optimisation tone | **Closed** | High | P0 | EGC-R08 | ED-01; ED-02; ED-15 |
| NCR-003 | Mission Intelligence engineering chrome | **Closed** | Medium | P1 | EGC-R08; R02 | ED-10; ED-15 |
| NCR-004 | Commitment continuity “tip” | **Closed** | Medium | P1 | EGC-R02 | ED-06 |
| NCR-005 | Session readiness overclaim; Session/Mission CTA mix | **Closed** | Medium | P1 | EGC-R02; R10 | ED-02; ED-16 |
| NCR-006 | Journal empty “Mission tip” / QC mention | **Closed** | Medium | P1 | EGC-R02; R12 | ED-14; DEP-01 |
| NCR-007 | Timeline tip wording + stats tension | **Closed** | Medium | P1 | EGC-R02; R06 | ED-05; DEP-01 |
| NCR-008 | Feedback Loop not taught in Help | **Closed** | Medium | P1 | EGC-R03; R04 | ED-04; OQ-03 |
| NCR-009 | Revision vs Mission competing focus | **Closed** | Medium | P2 | EGC-R09 | ED-13 |
| NCR-010 | History lacks Sensei/meaning bridge | **Closed** | Medium | P1 | EGC-R06 | ED-05; AC-03 |
| NCR-011 | Help omits Sensei memory map; anxiety phrasing | **Closed** | High | P0 | EGC-R03 | ED-04; ED-08; AC-04 |
| NCR-012 | Success states mix praise / readiness claims | **Closed** | Low–Med | P2 | EGC-R10 | AC-15; ED-16 |
| NCR-013 | Empty states reintroduce deprecated / gated nouns | **Closed** | Medium | P1 | EGC-R12 | ED-12; ED-14 |
| NCR-014 | Flag speech residuals (Runtime C; QC OFF ads) | **Closed** | High if ON | P0*/P1 | EGC-R07; R12 | ED-11; ED-14; AC-02 |
| NCR-015 | Educational copy tip / Session noun storm | **Closed*** | High | P0 | EGC-R02 | ED-02; DEP-01/02 |
| NCR-016 | Explanation eyebrow “Why this tip?” + KW reasons | **Closed** | High | P0 | EGC-R02; R01 | ED-07; ED-20 |
| NCR-017 | Reflection not one student system | **Closed** | High | P0 | EGC-R04; R05 | ED-03; AC-07 |
| NCR-018 | Hidden narrator transitions | **Closed*** | High | P0 | EGC-R01; R08 | ED-01; AC-01/04/05 |
| NCR-019 | Authority ownership incorrect in live speech | **Closed*** | High | P0 | EGC-R01; R03; R06 | AC-* |
| NCR-020 | Terminology not lexicon-applied | **Closed*** | High | P0 | EGC-R02 | ED-02; CP-03 |
| NCR-021 | Educational memory not introduced at orientation | **Closed** | High | P0 | EGC-R03; R01 | ED-04; D04 |
| NCR-022 | Product Check-in titled as Reflection | **Closed** | Medium | P1 | EGC-R05 | ED-18; D05 |

\*Closed for RR-001.3A–3D in-scope educational surfaces. RR-001.3D closes NCR-002 / 003 / 005 / 008 / 009 / 012 / 013 / 014 residual. Ops Contained: keep QC / UJ / Runtime C OFF until separately certified. EGC-R11 notifications remain preventive.

\*P0 before any Runtime C enablement.

---

## Records

### NCR-001 — Onboarding lacks Sensei handoff

| Field | Detail |
|-------|--------|
| **Capability** | Onboarding |
| **Observed** | Steps attribute missions, reasons, and reflection usefulness to **Kwalitec**; no Board handoff sentence. |
| **Clause** | DG-001.1-D01; DG-001.2-D04; CI-05; CP-04; CP-10 |
| **Compliance** | **Closed** — RR-001.3A |
| **Risk** | High — wrong first mentor relationship |
| **Student impact** | Learns product-as-tutor; later Sensei memory feels like a different product |
| **Required remediation** | Insert handoff; reattribute guidance to Study Sensei; fix Mission/Session wording |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01 (+ EGC-R02 for lexicon) |
| **Evidence** | `app/services/alpha_onboarding_service.py` ONBOARDING_STEPS |
| **Closure** | Meet Study Sensei step + Board handoff; KW-as-mentor strings removed; `test_rr001_3a_educational_identity.py`; `RR001_3A_COMPLETION_REPORT.md` |

---

### NCR-002 — Home narrator / lexicon residuals

| Field | Detail |
|-------|--------|
| **Capability** | Home |
| **Observed** | Today's Mission hero OK when active; Sensei often unnamed; Guided Reflection honesty present; “Optimising for…”; welcome modal KW + Today's Session |
| **Clause** | D01; D02; D05; DEP-01/02; CP-03/04/10 |
| **Compliance** | **Closed** — RR-001.3D (OQ-02 naming density policy applied) |
| **Risk** | High |
| **Student impact** | Daily focus half-clear; authority invisible |
| **Required remediation** | Naming density; tip retirement elsewhere; soften axis chrome |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01; EGC-R02; EGC-R08 |
| **Evidence** | `app/templates/student/home.html`; `partials/welcome_modal.html` |
| **Progress** | Sensei named; Guidance panel; Focusing-on chrome; welcome handoff |
| **Closure** | Hero-only Sensei naming; Guidance without duplicate eyebrow; MI educational priority; `test_rr001_3d_educational_consistency.py`; `RR001_3D_COMPLETION_REPORT.md` |

---

### NCR-010 — History epistemology without bridge

| Field | Detail |
|-------|--------|
| **Capability** | History |
| **Observed** | Accuracy/progress culture in Help/History vs Timeline not-from-scores |
| **Clause** | DG-001.2-D06; CP-07; CP-08 |
| **Compliance** | **Closed** — RR-001.3C |
| **Risk** | Medium |
| **Student impact** | Numbers feel like educational truth |
| **Required remediation** | History intro: context only; meaning in Journal/Timeline |
| **Priority** | P1 |
| **Implementation dependency** | EGC-R06 |
| **Evidence** | Help FAQ “accuracy over time”; Timeline narrative culture; ED-05 |
| **Closure** | History page bridge + shell description + Help FAQ; `test_rr001_3c_educational_memory.py`; `RR001_3C_COMPLETION_REPORT.md` |

---

### NCR-006 — Journal empty tip / QC honesty

| Field | Detail |
|-------|--------|
| **Capability** | Decision Journal |
| **Observed** | Empty description used “Mission tip” and advertised Quick Check |
| **Clause** | DEP-01; ED-14; DG-001.2-D07 |
| **Compliance** | **Closed** — RR-001.3C |
| **Risk** | Medium |
| **Student impact** | Deprecated tip noun + gated capability ad on first visit |
| **Required remediation** | Lexicon empty state; no QC ad while OFF |
| **Priority** | P1 |
| **Implementation dependency** | EGC-R12 |
| **Evidence** | `app/application/decision_journal/dto.py` |
| **Closure** | Mission guidance / revision wording; no tip/QC; 3C tests |

---

### NCR-007 — Timeline tip wording + stats tension

| Field | Detail |
|-------|--------|
| **Capability** | Educational Timeline |
| **Observed** | Narrative “Mission tip”; epistemology tension with History stats |
| **Clause** | DEP-01; ED-05; DG-001.2-D06 |
| **Compliance** | **Closed** — RR-001.3C |
| **Risk** | Medium |
| **Student impact** | Tip noun + numbers competing with learning story |
| **Required remediation** | Tip retirement; History bridge |
| **Priority** | P1 |
| **Implementation dependency** | EGC-R06; EGC-R02 |
| **Evidence** | `narrative.py`; Timeline DTO |
| **Closure** | Guidance noun in narrative; Timeline empty distinguishes History; 3C tests |

---

### NCR-011 — Help orientation lag

| Field | Detail |
|-------|--------|
| **Capability** | Help |
| **Observed** | Session/Readiness/session-reflection FAQ only; omits Journal, Timeline, MI, Sensei reflection; “closest to being tested on” |
| **Clause** | DG-001.1-D04; DG-001.2-D04/D10; CP-03; CP-06 |
| **Compliance** | **Closed** — RR-001.3B |
| **Risk** | High |
| **Student impact** | Never learns where long-term mastery story lives |
| **Required remediation** | Educational glossary + map; soften anxiety phrasing |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R03 (+ R01 handoff sentence in Help) |
| **Evidence** | `app/templates/alpha/help.html` |
| **Closure** | Journey map + glossary + Sensei handoff; anxiety phrasing removed; `test_rr001_3b_educational_orientation.py`; `RR001_3B_COMPLETION_REPORT.md` |

---

### NCR-014 — Feature-flag speech

| Field | Detail |
|-------|--------|
| **Capability** | Feature flag messaging |
| **Observed** | Runtime C “the system” contained OFF; Journal empty may advertise QC while OFF |
| **Clause** | DG-001.2-D07; DEP-04; Constitution §11 |
| **Compliance** | **Closed** (Runtime C system narrator — RR-001.3A); Journal empty QC ad **Closed** RR-001.3C; remaining QC empty/CTA residual **Closed** RR-001.3D |
| **Risk** | High if Runtime C enabled as-is |
| **Student impact** | Robotic mentor / false gated affordances |
| **Required remediation** | Rename before enable; empty-state flag honesty |
| **Priority** | P0 before enable; P1 empty honesty |
| **Implementation dependency** | EGC-R07; EGC-R12 |
| **Evidence** | ED-11; ED-14; AC-02 |
| **Closure** | Runtime C summary → “Why this Mission?”; flag still OFF; Journal empty QC honesty closed RR-001.3C |

---

### NCR-015 — Tip / Session noun storm in copy

| Field | Detail |
|-------|--------|
| **Capability** | Educational copy |
| **Observed** | “Why this tip?”; Study Tip cards; Mission tip; Today's Session as focus synonym |
| **Clause** | DG-001.1-D02; DEP-01; DEP-02; CP-03; CI-01 |
| **Compliance** | **Closed** (in-scope identity surfaces — RR-001.3A); Journal/Timeline tip residuals **Closed** RR-001.3C |
| **Risk** | High |
| **Student impact** | Cannot transfer “today's decision” across surfaces |
| **Required remediation** | Apply lexicon; PX reconciliation (OQ-01) |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R02 |
| **Evidence** | `student/components/explanation_card.html`; `presentation/product_language.py`; dashboard/mission study-tip cards |
| **Closure** | Tip retired on explanation/commitment/Mission/Dashboard prep; Mission≠Session in onboarding/welcome |

---

### NCR-016 — Explanation authority / tip eyebrow

| Field | Detail |
|-------|--------|
| **Capability** | Educational explanations |
| **Observed** | Explanation card “Why this tip?”; onboarding “reasons Kwalitec used”; Journal “Why this guidance” compliant |
| **Clause** | DEP-01; DG-001.2-D01; CP-07 |
| **Compliance** | **Closed** — RR-001.3A |
| **Risk** | High |
| **Student impact** | Explainability fragmented by noun and speaker |
| **Required remediation** | Standardise guidance/Mission eyebrows; Sensei ownership |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R02; EGC-R01 |
| **Evidence** | explanation_card.html; alpha_onboarding_service.py |
| **Closure** | “Why this guidance?”; onboarding “reasons Study Sensei used” |

---

### NCR-017 — Reflection system not coherent for students

| Field | Detail |
|-------|--------|
| **Capability** | Reflection flows |
| **Observed** | Multiple reflection types; preview honesty OK; no student map; Check-in titled Reflection |
| **Clause** | DG-001.3-D01; D05; CP-05; CI-03; §11.5 |
| **Compliance** | **Closed** — RR-001.3B |
| **Risk** | High |
| **Student impact** | Reflection = forms, not judgement practice |
| **Required remediation** | Publish map; rename Check-in; keep optionality |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R04; EGC-R05; OQ-R02 |
| **Evidence** | home Guided Reflection; session reflection; Journal optional; checkin.html title |
| **Closure** | Help + onboarding publish DG-001.3 map; Session reflection / Guided Reflection preview qualified; Check-in renamed; `test_rr001_3b_educational_orientation.py` |

---

### NCR-018 — Hidden narrator transitions

| Field | Detail |
|-------|--------|
| **Capability** | Narrator transitions |
| **Observed** | KW orientation → unnamed Home → SS memory without signal |
| **Clause** | DG-001.2-D04; CI-05; CP-04; CP-10 |
| **Compliance** | **Closed** (T04 handoff + Home/Session narrator — RR-001.3A); Help lag residual NCR-011; density Watch NCR-002/EGC-R08 |
| **Risk** | High |
| **Student impact** | No singular mentor relationship |
| **Required remediation** | Explicit handoff + Home naming policy |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01; EGC-R08 |
| **Evidence** | AC-01; AC-04; AC-05; ED-01 |
| **Closure** | Onboarding + welcome handoff; `data-narrator="study-sensei"` on Home/Session |

---

### NCR-019 — Authority ownership failures in live speech

| Field | Detail |
|-------|--------|
| **Capability** | Authority ownership |
| **Observed** | Educational judgement speech on KW surfaces; felt multi-authority via tip/Session; History soft alternate |
| **Clause** | DG-001.2-D01–D10; Constitution §11.1–11.3 |
| **Compliance** | **Closed** (memory / History AC-03 + tip empties — RR-001.3C); Home density Watch remains NCR-002 |
| **Risk** | High |
| **Student impact** | Unclear who teaches / remembers / reports facts |
| **Required remediation** | Implement authority matrix in copy |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01; EGC-R03; EGC-R06 |
| **Evidence** | Authority Conflict Register AC-01–AC-07 |
| **Closure** | History bridge (D06); Journal durable memory / Timeline chronological record ownership speech; tip empties retired; `RR001_3C_COMPLETION_REPORT.md` |

---

### NCR-020 — Terminology not applied

| Field | Detail |
|-------|--------|
| **Capability** | Educational terminology |
| **Observed** | Lexicon law active; product strings diverge |
| **Clause** | CP-03; CI-01; DG-001.1; DEP-* |
| **Compliance** | **Closed** (in-scope identity surfaces — RR-001.3A); OQ-01 PX docs + out-of-scope surfaces remain open via other NCRs |
| **Risk** | High |
| **Student impact** | Same as ED-02 noun storm |
| **Required remediation** | Lexicon application programme |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R02; OQ-01 |
| **Evidence** | TERMINOLOGY / DEP / templates |
| **Closure** | `product_language.py` + in-scope templates; see RR001_3A_TRACEABILITY_MATRIX.md |

---

### NCR-021 — Memory introduction gap

| Field | Detail |
|-------|--------|
| **Capability** | Educational memory |
| **Observed** | Journal host compliant; Help/onboarding omit introduction |
| **Clause** | DG-001.1-D04; DG-001.3-D02; ED-04 |
| **Compliance** | **Closed** — RR-001.3C |
| **Risk** | High (discoverability) |
| **Student impact** | Durable memory unused / unknown |
| **Required remediation** | First-introduction in Help + onboarding + memory empties |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R03; EGC-R01; EGC-R06 |
| **Evidence** | help.html topics; onboarding steps; Journal/Timeline empties |
| **Closure** | Onboarding memory step + Help memory model + glossary History + empty intros; `test_rr001_3c_educational_memory.py` |

---

### NCR-022 — Product Check-in titled Reflection

| Field | Detail |
|-------|--------|
| **Capability** | Product Check-in |
| **Observed** | H1 “Daily Reflection & Product Check-in” |
| **Clause** | DG-001.3-D05; CI-03; §11.5; ED-18 |
| **Compliance** | **Closed** — RR-001.3B |
| **Risk** | Medium |
| **Student impact** | Survey mistaken for educational reflection |
| **Required remediation** | Rename; remove Reflection from title |
| **Priority** | P1 |
| **Implementation dependency** | EGC-R05; OQ-R03 |
| **Evidence** | `app/templates/research/checkin.html` |
| **Closure** | H1 Product Check-in + non-reflection disclosure; RIP-001 tests assert no “Daily Reflection” |

---

### Condensed residuals (post RR-001.3D)

NCR-003–005, 008–009, 012–013 closed RR-001.3D (see `RR001_3D_COMPLETION_REPORT.md`). Preventive residual: **EGC-R11** notifications-when-built. Ops Contained: QC / UJ / Runtime C remain OFF. Escalate any reopened copy only if a future programme claims ED closure without keeping the cited strings.

---

## Closure rules

A Non-Compliance Register item may move to **Closed** only when:

1. Implementation evidence exists (diff / dogfood / review), and  
2. The remediation WP publishes a Pass (or Conditional Pass with named residual) on `GOVERNANCE_COMPLIANCE_CHECKLIST.md`, and  
3. The claimed ED-* / AC-* residual is updated in its source register.

Governance claims alone **do not** close NCR items (Constitution §11.6).

---

**End of GOVERNANCE_NON_COMPLIANCE_REGISTER**
