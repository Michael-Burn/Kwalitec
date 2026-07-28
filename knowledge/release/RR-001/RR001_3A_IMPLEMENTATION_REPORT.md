# RR-001.3A — Implementation Report

**Programme:** RR-001.3 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3A — Educational Identity & Narrator Consistency  
**Date:** 2026-07-28  
**Commit message (mandated):** `feat(rr-001.3a): implement educational identity and narrator consistency`  
**Governance authority:** DG-001.1 · DG-001.2 · DG-001.4 · EGC-001  
**Remediation packages:** EGC-R01 · EGC-R02 (primary NCRs below)

---

## Summary

RR-001.3A implements the mandatory **Kwalitec → Study Sensei** educational handoff and applies the Canonical Educational Lexicon to in-scope educational identity surfaces. Students now meet Study Sensei explicitly during onboarding and welcome; Home, Mission, Session, explanation, and commitment continuity speech name Sensei (or use Mission/guidance nouns) instead of Kwalitec-as-mentor, tip, or “the system.”

**Not changed:** recommendation selection, Mission Intelligence composition fields, algorithms, architecture, schema, feature flags, curriculum, Journal/Timeline/Help/Reflection architecture (deferred to later EGC-R* packages).

---

## Primary NCRs closed (in-scope surfaces)

| NCR | Title | Resolution |
|-----|-------|------------|
| **NCR-001** | Missing Study Sensei introduction | Dedicated onboarding step + Board handoff sentence |
| **NCR-014** | System narrator wording | Runtime C summary → “Why this Mission?” |
| **NCR-015** | Mission / Session / tip inconsistency | Tip retired on explanation, commitment, Mission/Dashboard prep cards; Mission≠Session wording in onboarding/welcome |
| **NCR-018** | Missing onboarding handoff | T04 handoff in onboarding + welcome modal |
| **NCR-020** | Educational terminology drift | Lexicon applied on in-scope copy; `product_language.py` reconciled |

Related in-scope residuals also remidiated: explanation tip eyebrow (NCR-016 surface), Home Sensei naming / Coach chrome (NCR-002 narrator portion), commitment continuity tip (NCR-004).

---

## Implementation detail

### EGC-R01 — Narrator handoff & Sensei attribution

1. **Alpha onboarding** (`alpha_onboarding_service.py`): five steps; step 2 “Meet Study Sensei” with mandatory sentence: *Study Sensei is how Kwalitec guides your daily learning decisions.* Guidance/explanations/reflection attributed to Study Sensei; Kwalitec remains product OS only.
2. **Welcome modal**: product eyebrow stays Kwalitec; body carries handoff + Mission/Session distinction; CTA remains “Start Today's Session” (practice).
3. **Home**: `data-narrator="study-sensei"` label; Coach panel → Study Sensei / Guidance; empty copy mentions Sensei guidance.
4. **Session overview**: Sensei narrator + “Session is focused practice on today's Mission.”
5. **Mission prep card**: “Study Tip” → “Before you begin” (environment prep, not Mission noun).

### EGC-R02 — Lexicon application

1. Explanation card: “Why this tip?” → “Why this guidance?”
2. Runtime C panel: “Why the system chose this” → “Why this Mission?”
3. Commitment continuity / humble frame: tip → Mission
4. MI axis chrome (presentation only): “Optimising for” → “Focusing on”
5. `product_language.py`: approve Mission / Study Sensei / Guidance; reject tip/system phrases; keep Session CTAs for practice entry

---

## Files Created

- `tests/presentation/student/test_rr001_3a_educational_identity.py`
- `knowledge/release/RR-001/RR001_3A_IMPLEMENTATION_REPORT.md`
- `knowledge/release/RR-001/RR001_3A_TRACEABILITY.md`
- `knowledge/release/RR-001/RR001_3A_TEST_REPORT.md`
- `knowledge/release/RR-001/RR001_3A_STUDENT_IMPACT_ASSESSMENT.md`

---

## Files Modified

- `app/services/alpha_onboarding_service.py`
- `app/templates/alpha/onboarding.html`
- `app/templates/partials/welcome_modal.html`
- `app/templates/student/home.html`
- `app/templates/student/components/explanation_card.html`
- `app/templates/student/components/educational_experience.html`
- `app/templates/session/overview.html`
- `app/templates/mission/index.html`
- `app/templates/dashboard/index.html`
- `app/application/student_experience/recommendation_commitment.py`
- `app/presentation/product_language.py`
- `tests/presentation/student/test_home_template_mes.py`
- `tests/test_alpha_001_infrastructure.py`
- `tests/test_first_time_experience.py`
- `tests/test_internal_alpha_polish.py`
- `tests/application/student_experience/test_recommendation_commitment.py`
- `tests/presentation/student/test_recommendation_commitment_contract.py`
- `knowledge/release/RR-001/ALPHA_REMEDIATION_REGISTER.md` *(status notes)*

---

## Tests Executed

See `RR001_3A_TEST_REPORT.md`. Focused suite **134 passed**; ruff clean on touched Python.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved (copy/presentation only; no recommendation math in routes).  
- Curriculum V1/V2 loadability/traversal **untouched**.  
- Mission Intelligence composition / DTO field meanings unchanged (axis *chrome* wording only).  
- Feature flags unchanged.  
- StartupService / schema untouched.

---

## Technical Debt

- Journal empty “Mission tip” / Timeline tip narrative remain (EGC-R12; Journal/Timeline out of this WP scope).  
- Help glossary / memory first-introduction lag remains (EGC-R03).  
- Home Sensei naming density may need cohort tuning (OQ-02 residual).  
- Internal code identifiers (`tip` payloads, `coach_insight` fields) remain non-student-facing.

---

## Known Limitations

- Does not close Help, History bridge, Reflection map, or Product Check-in rename (EGC-R03–R06).  
- Does not enable or redesign Runtime C beyond rename-before-enable identity fix.  
- Does not claim full ED-01–ED-20 closure across the whole product — only in-scope educational identity surfaces.  
- Does not claim Version 1 production-ready or validated KSI cohort evidence.

---

## Student Impact Assessment

See `RR001_3A_STUDENT_IMPACT_ASSESSMENT.md`.

---

## Estimated KSI Contribution

| Category | Δ | Rationale |
|----------|---|-----------|
| K8 Explainability / trust governance | +1 *(estimated)* | Narrator ownership + guidance eyebrow clarity; not cohort-validated |
| K2 Recommendation quality | 0 | Selection unchanged |
| K1–K7 | 0 | No learning behaviour change |

**Net ΔKSI ≈ +1 (estimated, unvalidated).** Do not treat as Gate G1 validated KSI.

---

## Evidence collected

- Tests: `tests/presentation/student/test_rr001_3a_educational_identity.py` + regression suite in Test Report  
- Governance: `GOVERNANCE_NON_COMPLIANCE_REGISTER.md` NCR-001/014/015/018/020; `AUTHORITY_TRANSITION_MAP.md` T04  
- Traceability: `RR001_3A_TRACEABILITY.md`

---

## Lessons learned for student value

Students cannot trust “one mentor” until the product says so once, early, and then stays consistent. Tip/Session synonym storms broke transfer of “today’s decision” more than any missing field in Mission Intelligence.

---

## Explainability Review

| # | Requirement | Result | Evidence |
|---|-------------|--------|----------|
| R1 | Evidence-backed | Pass *(unchanged content)* | Explanation card fields unchanged; eyebrow only |
| R2 | Confidence appropriate | Pass *(unchanged)* | Confidence labels untouched |
| R3 | Student action clear | Pass | Session CTA + Mission focus nouns clarified |
| R4 | Avoid technical detail | Pass | “the system” retired on Runtime C disclosure |
| R5 | Cross-surface consistency | Pass *(in-scope)* | Guidance / Mission / Sensei aligned on Home/Session/onboarding |

Schema S1–S8: **Pass / N/A** — no schema field removal; narrator/lexicon labels only. Full checklist path: `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`.

---

## Recommendation Quality Review

**N/A — selection/ranking unchanged.** Copy changes do not alter which recommendation wins; only who narrates and which lexicon noun is used. K2 claims: none.

---

## Version 1 readiness residual

**N/A for production-ready declaration.** Identity remediation supports educational honesty but does not close P-002.1 G1–G12.

---

**End of RR001_3A_IMPLEMENTATION_REPORT**
