# Student Impact Assessment — EP-003.2

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-003.2 |
| **Title** | Readiness Intelligence Enhancement |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | Yes — Estimated readiness now carries evidence, confidence, drivers, change reasoning, and a clear next action on Runtime A dashboard/analytics surfaces |
| **Production activation?** | Gated — inherits existing Runtime A / Twin / cutover flags; no new production-only flag |
| **Related KSI categories** | K3 (primary), K8 (supporting), K1 (next-action Mission labelling), K6 (light) |

**Template:** [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

---

## 1. Student problem

**Student problem:**

> Estimated readiness often felt unpackable or anxiety-inducing: a percentage without clear evidence, confidence, or what to do next. Cold-start honesty existed in places, but filled composites did not show their working. Readiness usefulness is Partial (K3 = 52).

**Evidence:**

> P-001.1 `BASELINE_KSI_ASSESSMENT.md` §3.1 (K3 = 52); EP-004 blind-review themes on unpackable readiness; EP-001.3 / EP-002.6 delivered Twin drivers without P-001.2 student schema.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | One `suggested_next_action` (Mission / planner / weak-topic fallback) |
| How am I progressing? | Yes | Judgement + supporting evidence + change reasoning |
| What is stopping me? | Yes | Risk-elevating drivers named in change / evidence |
| What happens next? | Yes | Review point after next session / plan refresh |

**Student benefit summary:**

> Students can see why Estimated readiness is at its level, how confident the system is, what evidence supports it, and one clear study next step — without inventing certainty on cold start.

**Final Test:** Does this help students become better professionals? **Yes** — models evidence-based preparation judgement and honest uncertainty.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Improves consistency of study decisions? | Yes — next action defers to Today’s Mission when available |
| Improves feedback quality on readiness? | Yes — Mandatory Explanation Schema fields |
| Improves reflection / agency? | Yes — confidence + review point + change reasoning |
| Improves revision timing honesty? | Partial — weak areas cited in evidence; does not re-plan revision |
| Honesty risks? | Residual: richer copy could still feel dense if templates dump all fields (mitigated: L2 default; presentation summary) |

---

## 4. Success metrics

| Metric | Baseline | Target (programme) | Measurement | Owner |
|---|---|---|---|---|
| Explanation schema completeness on readiness surfaces | Incomplete | 100% of dashboard surfaces from `get_dashboard_readiness_surface` | Unit tests + `has_complete_readiness_explanation_schema` | ReadinessService |
| Student-safe confidence labels | Internal / empty | High / Moderate / Low / Cannot yet be estimated | Unit tests | ReadinessService |
| K3 estimated score | 52 | **58–64** (estimated; under-claim) | Product re-score after dogfood | Product |
| K8 contribution | 55 (+EP-003.1 lift) | +2 to +4 via readiness schema honesty | Explainability review Pass | Product |

---

## 5. Estimated KSI contribution

See [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md).

| Category | Δ (points) | Rationale |
|---|---:|---|
| K1 | +1 | Mission-aligned next action labelling |
| K2 | 0 | Recommendation ranking unchanged |
| K3 | +8 | Primary — evidence, confidence, drivers, next action |
| K4 | +1 | Personal weak-area evidence citation |
| K5 | 0 | Motivation not targeted |
| K6 | +1 | Progress judgement more decision-grade |
| K7 | 0 | Revision optimisation unchanged |
| K8 | +4 | Readiness Mandatory Explanation Schema |

---

## 6. Risks to students

| Risk | Mitigation |
|---|---|
| Anxiety from seeing risk drivers | Confidence honesty + actionable next step; not alarm theatre |
| Confusion vs syllabus coverage % | Coverage narrative remains separate Learning Progress fact |
| Feeling “blocked” by cannot-estimate | Refusal includes concrete first study step |

---

## 7. Assumptions

- Students encounter readiness primarily via Dashboard / Analytics Runtime A path.
- Twin cutover remains gated; legacy enriched path is the default student experience until cutover eligible.
- Live cohort re-score will validate or revise estimated K3 lift.

---

## 8. Non-claims

- Does not claim exam pass-rate improvement.
- Does not claim Twin Ready / production HTTP cutover activation.
- Does not merge coverage and Estimated readiness into one percentage.
