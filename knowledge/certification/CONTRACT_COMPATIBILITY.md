# Educational Intelligence — Contract Compatibility

**Milestone:** AP-002D7  
**Date:** 2026-07-28  
**Verdict:** PASS  

---

## Certified contract matrix

| Contract | Version | Role |
|---|---|---|
| Packaging | `AP-002C.1` | Evidence Bundle export |
| Evidence Ingress | `AP-001.evidence_ingress.v1` | AP-001 boundary |
| Interpretation | `AP-002D2.interpretation.v1` | Evidence → observations |
| Decision | `AP-002D3.decision.v1` | Observations → decisions / Twin |
| Projection | `AP-002D4.projection.v1` | Decisions → graph relationships |
| Planning | `AP-002D5.planning.v1` | Decisions → StudyMissionPlan |
| Explanation | `AP-002D6.explanation.v1` | Decisions (+ plan) → TutorExplanation |

Negotiation rule: each stage accepts only its approved upstream versions. Unsupported versions raise explicit errors (never silently coerced).

---

## Version rejection behaviour

| Probe | Expected error | Observed |
|---|---|---|
| Packaging `AP-999.unsupported.v0` at interpretation | `UnsupportedEvidenceSchema` | PASS |
| Decision version probe at DecisionValidator | `UnsupportedDecisionVersion` | PASS |
| Decision version probe at projection | `InvalidDecisionVersion` | PASS |
| Decision version probe at planning | `InvalidDecisionVersion` | PASS |
| Decision version probe at explanation | `InvalidDecisionVersion` | PASS |

---

## Compatibility notes

- Ingress and Interpretation both accept packaging `AP-002C.1` only.
- Projection / Planning / Explanation consume decisions at `AP-002D3.decision.v1`.
- Explanation accepts mission plans at `AP-002D5.planning.v1`.
- Twin version mismatches continue to fail closed (existing D5/D6 validators).

Registry: `tests/certification/educational_intelligence/contracts.py`.
