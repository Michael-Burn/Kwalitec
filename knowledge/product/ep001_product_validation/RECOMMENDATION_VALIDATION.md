# Recommendation Validation

**Programme:** EP-001 — Workstream 4  
**Version:** 1.0  
**Status:** Framework  
**Updated:** 2026-07-23  

---

## 1. Purpose

Every recommendation must answer:

| Question | Required field / source |
|---|---|
| **Why?** | `rationale` |
| **Evidence?** | `evidence_ids` (and Decision Journal when authoritative) |
| **Expected outcome?** | `expected_benefit` |
| **Confidence?** | `confidence` / ConfidenceBand |

Domain shape already exists on Twin `Recommendation` (`app/domain/student_twin/recommendation_state.py`). Production recommendation paths must expose the same four answers in learner-facing copy (Product Language Guide).

---

## 2. Lifecycle tracking

| State | Meaning | Event (target) |
|---|---|---|
| Shown | Presented as next action | `recommendation.shown` |
| Accepted | Student starts / commits | `recommendation.accepted` |
| Ignored / dismissed | Explicit dismiss or timeout without accept | `recommendation.dismissed` / expired |
| Completed | Recommended action finished with educational outcome | `recommendation.completed` |
| Benefit assessed | Later evidence supports / refutes expected benefit | Derived (Phase 2) |

**Educational benefit (default rule):** Within 14 days of acceptance, observe positive evidence on the recommended topic (or stated expected_benefit target). Compare to a matched set of ignored recommendations of the same kind/topic band where possible.

---

## 3. Effectiveness report (deliverable)

Periodic artefact: `RECOMMENDATION_EFFECTIVENESS_REPORT.md` (generate per cohort window; do not invent numbers without data).

Required sections:

1. **Volume** — shown / accepted / dismissed / completed  
2. **Acceptance rate** — with sample size  
3. **Completion among accepted**  
4. **Benefit rate** — among completed with sufficient follow-up evidence  
5. **Calibration** — high-confidence recommendations vs realised benefit  
6. **Failure modes** — top reasons dismissed (interview + UI codes)  
7. **Actions** — product changes tied to Validation Framework outcomes  

Minimum sample: Educational Validation Framework §5.

---

## 4. Instrumentation gate

- Prefer Decision Journal as sole acceptance authority if Analytics Architecture open question #4 resolves that way.
- Do not optimise UI to inflate accept rate without benefit tracking.
- Analytics must not recompute recommendation ranking.

Phase 1 may emit Session/reflection events first; recommendation events follow once persistence source is confirmed (see PRD-001 open questions). A dedicated PRD-002 should cover recommendation instrumentation before production claims.

---

## 5. Exit criteria (WS4)

| Criterion | Status |
|---|---|
| Four-question contract documented | COMPLETE |
| Lifecycle states defined | COMPLETE |
| Effectiveness report template defined | COMPLETE |
| Events implemented + report with real cohort data | NOT STARTED |

---

## References

- Validation Framework O8  
- `PRODUCT_ANALYTICS_ARCHITECTURE.md` event sketch  
- Twin recommendation_state  
- Vision: no opaque AI recommendations  
