# RR-001.3B — Student Impact Assessment

**Programme:** RR-001 — Governance-driven Educational Remediation  
**Work Package:** RR-001.3B — Educational Orientation & Reflection Coherence  
**Date:** 2026-07-28  
**Template:** `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

---

## Student problem

Students met multiple reflection-like moments (Session close, Home commitment ack, Journal optional questions, Timeline prompts, Guided preview, Product Check-in) without one mental model of what reflection is for, what is saved, or how Help orients them in the educational ecosystem. Help previously taught Session/Readiness only and omitted Journal, Timeline, Sensei, and Check-in distinctions. Product Check-in’s H1 called the survey a “Daily Reflection,” inviting false cousin confusion (ED-03 / ED-04 / ED-18).

## Student benefit

- One Help map explaining Mission, Study Session, Reflection, Decision Journal, Educational Timeline, and Study Sensei.  
- One reflection family with clear kinds and explicit non-reflections.  
- Product Check-in clearly labelled as product experience feedback, not learning reflection.  
- Softer Help language about how Sessions are chosen (less exam-anxiety framing).

## Learning benefit

Students can practise professional judgement with Reflections without mistaking surveys for educational memory, and can find where durable learning memory lives (Decision Journal / Educational Timeline) without treating History stats as the whole story.

## Success metrics

| Metric | Target | Evidence |
|--------|--------|----------|
| Acceptance questions answerable from Help | All six WP questions | `test_help_answers_acceptance_questions` |
| Check-in never titled Reflection | 0 “Daily Reflection” on student Check-in | HTTP + 3B tests |
| Reflection map published | Board sentence present in Help + onboarding | 3B tests |
| Regression green on adjacent flows | Pass | 164 tests |

## Risks

| Risk | Mitigation |
|------|------------|
| Help length increases cognitive load | Topics remain progressive disclosure (`learn_more`); orientation sections are scannable lists |
| Students still confuse History stats with Timeline meaning | Deferred to EGC-R06 (NCR-010); Help now points meaning to Journal/Timeline |
| Skip-onboarding students miss map until Help | Help always available; onboarding revisit quick action retained |

## Assumptions

- Students will open Help when confused about Reflection / Check-in.  
- Unified Journey Guided preview remains optional/flagged; when shown, honesty holds.  
- “Feedback Loop” student-visible name (OQ-03) is not required if Sensei reflection is taught under Journal.

## Estimated KSI contribution

| Category | Δ | Rationale |
|----------|---|-----------|
| K1 Continuity | +1 | Orientation connects journey surfaces |
| K2 Recommendations | 0 | Ranking unchanged |
| K3 Planning | 0 | Sequencing unchanged |
| K4 Practice | +1 | Session reflection purpose clarified |
| K5 Mastery honesty | +1 | Memory vs stats distinction introduced in Help |
| K6 Calm / trust | +2 | Anxiety phrasing softened; Check-in false cousin removed |
| K7 Agency | +1 | Clear optional reflection vs required practice |
| K8 Explainability | +2 | Ecosystem + reflection map teachable |
| **Net ΔKSI** | **+8 (estimated)** | Orientation/docs-heavy; not validated cohort KSI |

## Evidence collected

- `tests/presentation/student/test_rr001_3b_educational_orientation.py`  
- RIP-001 / post-session Check-in regressions  
- Journal / Timeline / Session language / onboarding regressions (see Test Report)  
- `RR001_3B_TRACEABILITY_MATRIX.md`

## Lessons learned for student value

Publishing the Board map in Help alone is insufficient without renaming the loudest false cousin (Check-in H1) and aligning Session/preview labels. Orientation copy must answer “what is this *not*?” as clearly as “what is this?”

## Explainability Review

N/A for recommendation ranking — orientation/copy only. Help and Session framing increase explainability of the educational system (K8 orientation); no new opaque scores.

## Recommendation Quality Review

N/A — recommendation selection/scoring untouched.
