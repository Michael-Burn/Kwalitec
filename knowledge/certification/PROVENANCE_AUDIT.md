# Educational Intelligence — Provenance Audit

**Milestone:** AP-002D7  
**Date:** 2026-07-28  
**Verdict:** PASS — no broken provenance chains  

---

## Required identity chain

Every learner-facing artefact must reconstruct:

| Link | Certified field |
|---|---|
| Assessment Session | `assessment_session_id` / `session_id` |
| Evidence Bundle | `evidence_bundle_id` |
| Observations | `observation_ids` / `observation_set_id` |
| Decisions | `decision_ids` / `decision_set_id` |
| Reasoning Request | `reasoning_request_id` |
| Twin Version | `twin_version` (+ `twin_id`) |
| Graph Projection | `projection_id` |
| Mission Plan | `mission_plan_id` / `mission_id` |
| Tutor Explanation | `explanation_id` |
| Correlation | `correlation_id` |

Auditor: `tests/certification/educational_intelligence/provenance.py`.

---

## Audit results

| Check | Result |
|---|---|
| Observation set links to evidence + reasoning request | PASS |
| Every decision references known observation ids | PASS |
| Decision evidence / session / correlation links intact | PASS |
| Twin reasoning history present after apply | PASS |
| Projection references valid decision ids + matching twin version | PASS |
| Mission plan links evidence / reasoning / correlation / twin version | PASS |
| Explanation links evidence / reasoning / correlation / twin version | PASS |
| Explanation decision ids ⊆ decision set | PASS |
| Available explanations have sections + supporting decisions | PASS |

---

## Explainability audit

- No certified available explanation exists without supporting decision ids.
- Explanation sections retain bodies and, where references exist, preserve evidence / reasoning identity.
- Soft / thin / conflicting evidence paths remain explainable without fabricating mastery certainty.

---

## Failure policy

If any link is missing, `ProvenanceChain.is_complete` is false and the pipeline result is not certified. The harness never invents missing provenance.
