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

---

## Summary

| ID | Title | Status class | Severity | Priority | Package | RP / AC link |
|----|-------|--------------|----------|----------|---------|--------------|
| NCR-001 | Onboarding lacks Sensei handoff; KW-as-mentor | **Closed** | High | P0 | EGC-R01 | ED-01; ED-20; AC-01 |
| NCR-002 | Home authority unnamed; tip/Session collision; optimisation tone | PC / Watch | High | P0 | EGC-R08 residual | ED-01; ED-02; ED-15 |
| NCR-003 | Mission Intelligence engineering chrome | PC | Medium | P1 | EGC-R08; R02 | ED-10; ED-15 |
| NCR-004 | Commitment continuity “tip” | **Closed** | Medium | P1 | EGC-R02 | ED-06 |
| NCR-005 | Session readiness overclaim; Session/Mission CTA mix | PC | Medium | P1 | EGC-R02; R10 | ED-02; ED-16 |
| NCR-006 | Journal empty “Mission tip” / QC mention | PC | Medium | P1 | EGC-R02; R12 | ED-14; DEP-01 |
| NCR-007 | Timeline tip wording + stats tension | PC | Medium | P1 | EGC-R02; R06 | ED-05; DEP-01 |
| NCR-008 | Feedback Loop not taught in Help | **Advanced*** | Medium | P1 | EGC-R03; R04 | ED-04; OQ-03 |
| NCR-009 | Revision vs Mission competing focus | PC | Medium | P2 | EGC-R09 | ED-13 |
| NCR-010 | History lacks Sensei/meaning bridge | NC | Medium | P1 | EGC-R06 | ED-05; AC-03 |
| NCR-011 | Help omits Sensei memory map; anxiety phrasing | **Closed** | High | P0 | EGC-R03 | ED-04; ED-08; AC-04 |
| NCR-012 | Success states mix praise / readiness claims | PC | Low–Med | P2 | EGC-R10 | AC-15; ED-16 |
| NCR-013 | Empty states reintroduce deprecated / gated nouns | PC | Medium | P1 | EGC-R12 | ED-12; ED-14 |
| NCR-014 | Flag speech residuals (Runtime C; QC OFF ads) | **Closed*** / Contained | High if ON | P0*/P1 | EGC-R07; R12 | ED-11; ED-14; AC-02 |
| NCR-015 | Educational copy tip / Session noun storm | **Closed*** | High | P0 | EGC-R02 | ED-02; DEP-01/02 |
| NCR-016 | Explanation eyebrow “Why this tip?” + KW reasons | **Closed** | High | P0 | EGC-R02; R01 | ED-07; ED-20 |
| NCR-017 | Reflection not one student system | **Closed** | High | P0 | EGC-R04; R05 | ED-03; AC-07 |
| NCR-018 | Hidden narrator transitions | **Closed*** | High | P0 | EGC-R01; R08 | ED-01; AC-01/04/05 |
| NCR-019 | Authority ownership incorrect in live speech | PC / residual | High | P0 | EGC-R01; R03; R06 | AC-* |
| NCR-020 | Terminology not lexicon-applied | **Closed*** | High | P0 | EGC-R02 | ED-02; CP-03 |
| NCR-021 | Educational memory not introduced at orientation | **Advanced*** | High | P0 | EGC-R03; R01 | ED-04; D04 |
| NCR-022 | Product Check-in titled as Reflection | **Closed** | Medium | P1 | EGC-R05 | ED-18; D05 |

\*Closed for RR-001.3A **in-scope** educational identity surfaces where noted. RR-001.3B closes NCR-011 / NCR-017 / NCR-022. NCR-008 / NCR-021 advanced via Help Sensei reflection + memory map (OQ-03 FL jargon name still open). Named residuals: Journal/Timeline tip empties (NCR-006/007); QC empty ads (NCR-013); Home naming density Watch (NCR-002 / EGC-R08); History bridge (NCR-010).

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
| **Compliance** | Partially Compliant / **Watch** — narrator + tip/axis chrome remidiated (RR-001.3A); OQ-02 naming density remains EGC-R08 |
| **Risk** | High |
| **Student impact** | Daily focus half-clear; authority invisible |
| **Required remediation** | Naming density; tip retirement elsewhere; soften axis chrome |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01; EGC-R02; EGC-R08 |
| **Evidence** | `app/templates/student/home.html`; `partials/welcome_modal.html` |
| **Progress** | Sensei named; Guidance panel; Focusing-on chrome; welcome handoff |

---

### NCR-010 — History epistemology without bridge

| Field | Detail |
|-------|--------|
| **Capability** | History |
| **Observed** | Accuracy/progress culture in Help/History vs Timeline not-from-scores |
| **Clause** | DG-001.2-D06; CP-07; CP-08 |
| **Compliance** | Non-Compliant |
| **Risk** | Medium |
| **Student impact** | Numbers feel like educational truth |
| **Required remediation** | History intro: context only; meaning in Journal/Timeline |
| **Priority** | P1 |
| **Implementation dependency** | EGC-R06 |
| **Evidence** | Help FAQ “accuracy over time”; Timeline narrative culture; ED-05 |

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
| **Compliance** | **Closed** (Runtime C system narrator — RR-001.3A); **Contained** residual QC empty ads → NCR-013 / EGC-R12 |
| **Risk** | High if Runtime C enabled as-is |
| **Student impact** | Robotic mentor / false gated affordances |
| **Required remediation** | Rename before enable; empty-state flag honesty |
| **Priority** | P0 before enable; P1 empty honesty |
| **Implementation dependency** | EGC-R07; EGC-R12 |
| **Evidence** | ED-11; ED-14; AC-02 |
| **Closure** | Runtime C summary → “Why this Mission?”; flag still OFF; QC empty honesty deferred |

---

### NCR-015 — Tip / Session noun storm in copy

| Field | Detail |
|-------|--------|
| **Capability** | Educational copy |
| **Observed** | “Why this tip?”; Study Tip cards; Mission tip; Today's Session as focus synonym |
| **Clause** | DG-001.1-D02; DEP-01; DEP-02; CP-03; CI-01 |
| **Compliance** | **Closed** (in-scope identity surfaces — RR-001.3A); Journal/Timeline tip residuals remain NCR-006/007 |
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
| **Compliance** | Non-Compliant |
| **Risk** | High |
| **Student impact** | Unclear who teaches / remembers / reports facts |
| **Required remediation** | Implement authority matrix in copy |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R01; EGC-R03; EGC-R06 |
| **Evidence** | Authority Conflict Register AC-01–AC-07 |

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
| **Compliance** | **Advanced** — Help + onboarding introduce Journal / Timeline (RR-001.3B); residual Watch if other surfaces omit |
| **Risk** | High (discoverability) |
| **Student impact** | Durable memory unused / unknown |
| **Required remediation** | First-introduction in Help + onboarding |
| **Priority** | P0 |
| **Implementation dependency** | EGC-R03; EGC-R01 |
| **Evidence** | help.html topics; onboarding steps |
| **Progress** | Journey map + glossary + reflection map name Decision Journal and Educational Timeline |

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

### Condensed residuals (NCR-003–009, 012–013)

Full narrative for these PC items lives in the Audit §5. Shared pattern: **governance resolved; product copy open**. Each cites DEP/ED and maps to EGC-R* in the summary table. Escalate any to Critical only if a future programme claims ED closure without fixing the cited strings.

---

## Closure rules

A Non-Compliance Register item may move to **Closed** only when:

1. Implementation evidence exists (diff / dogfood / review), and  
2. The remediation WP publishes a Pass (or Conditional Pass with named residual) on `GOVERNANCE_COMPLIANCE_CHECKLIST.md`, and  
3. The claimed ED-* / AC-* residual is updated in its source register.

Governance claims alone **do not** close NCR items (Constitution §11.6).

---

**End of GOVERNANCE_NON_COMPLIANCE_REGISTER**
