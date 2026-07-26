# Student Impact Assessment — EP-003.1

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-003.1 |
| **Title** | Recommendation Engine Enhancement |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | Yes — recommendation ranking, explanations, confidence, honest refusal on Runtime A legacy path (and schema fill on dashboard rows) |
| **Production activation?** | Gated — inherits existing feature-flag / cutover governance; no new production-only flag |
| **Related KSI categories** | K2 (primary), K8 (supporting), K4 (light), K1 (plan coherence labelling) |

**Template:** [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

---

## 1. Student problem

**Student problem:**

> Coach / Insight tips often felt generic or opaque (“highest-value / learning evidence”) and sometimes competed with Today’s Mission without saying so. Cold-start students could receive thin tips or silence without an honest “not yet” message. Recommendation usefulness is the weakest KSI pillar (K2 = 48).

**Evidence:**

> P-001.1 `BASELINE_KSI_ASSESSMENT.md` §3.1 (K2 = 48); P-001.3 completion notes that standards alone do not raise live usefulness; EP-004 blind-review themes on opaque guidance (cited in baseline).

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | Decision ladder picks a clearer primary; one `suggested_next_action` |
| How am I progressing? | N/A | Not a progress surface |
| What is stopping me? | Yes | Blocking deficits / risks ranked above routine tips; advisory labels when Mission competes |
| What happens next? | Yes | Review point + honest refusal with a build-evidence next step |

**Student benefit summary:**

> Students see why a tip was chosen, how confident it is, how it relates to Today’s Mission, and get an honest deferral instead of fabricated certainty.

**Final Test:** Does this help students become better professionals? **Yes** — models evidence-based prioritisation and honest uncertainty.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Improves consistency of study decisions? | Yes — protects authorised daily loop (ladder rank 2 / advisory labelling) |
| Improves feedback quality on next action? | Yes — Mandatory Explanation Schema fields |
| Improves reflection / agency? | Yes — confidence + review point; students can defer knowingly |
| Improves revision timing honesty? | Partial — exam-critical ranks elevated; G6 blocks premature mock tips on thin history |
| Honesty risks? | Residual: refusal copy must not feel like product emptiness (mitigated with actionable next step) |

---

## 4. Success metrics

| Metric | Baseline | Target (programme) | Measurement | Owner |
|---|---|---|---|---|
| Explanation schema completeness on legacy rows | Incomplete | 100% of returned rows | Unit tests + `has_complete_explanation_schema` | RecommendationService |
| Decision ladder compliance | Priority-only | Ladder ranks 1–9 applied | Unit tests | RecommendationService |
| K2 estimated score | 48 | **52–58** (estimated; under-claim) | Product re-score after dogfood | Product |
| K8 contribution | 55 | +2 to +4 estimated via schema honesty | Explainability review Pass | Product |

---

## 5. Estimated KSI contribution

See [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md).

| Category | Δ (points) | Rationale |
|---|---:|---|
| K1 | +1 | Plan coherence labelling reduces plan fight |
| K2 | +6 | Primary target — prioritisation + evidence + refusal |
| K3 | 0 | Readiness maths unchanged |
| K4 | +1 | Personal evidence density / Mission awareness |
| K5 | 0 | Motivation tips still lowest ladder class |
| K6 | 0 | Analytics unchanged |
| K7 | +1 | Exam-critical ranking + thin-history gate |
| K8 | +3 | Mandatory schema + confidence honesty |
| **Net ΔKSI (weighted)** | **~+1.7** | See KSI Impact for formula |

Prefer under-claiming; live cohort may revise.

---

## 6. Validation plan

1. Unit/integration tests for ladder, schema, confidence, coherence, refusal, ownership.
2. Dogfood Dashboard recommendations with Mission present vs absent.
3. Re-score K2/K8 after private-beta evidence (not claimed as Pass outcome here).

---

## 7. Risks

See [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md). Primary student risk: cold-start honest refusal perceived as emptiness.

---

## 8. Assumptions

- Runtime A legacy dict contract remains the template wire format.
- Planning mission surface remains a lawful read for coherence labelling.
- EP-001 / EP-003 marketing freezes on effectiveness claims remain in force.

---

## 9. Evidence collected

- `tests/services/test_recommendation_quality_ep003_1.py`
- `EXPLAINABILITY_REVIEW.md`, `RECOMMENDATION_REVIEW.md`
- Implementation: `app/services/recommendation_quality.py`

---

## 10. Lessons learned for student value

Standards without implementation do not move K2. Moving explanation ownership into RecommendationService removes presentation theatre that masked missing confidence and plan coherence. Honest refusal is educationally correct but must stay actionable.
