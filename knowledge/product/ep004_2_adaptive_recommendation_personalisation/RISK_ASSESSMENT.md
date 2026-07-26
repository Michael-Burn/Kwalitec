# EP-004.2 — Risk Assessment

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Date:** 2026-07-26  

---

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Profile becomes second recommender | Low | Critical | No ranking API on profile; service owns rules; ownership tests | Watch future PRs |
| R2 | Accept/dismiss treated as mastery | Medium | Critical | Cadence-only use; explicit non-promotion test | Medium — educate consumers |
| R3 | Thin-sample overfit | Medium | High | Confidence ≥ 0.3 and sample ≥ 3 gates | Low |
| R4 | Safety/Mission demoted by habits | Low | Critical | Protected ladder ranks 1–3 | Low |
| R5 | Opaque personalisation | Medium | High | Mandatory factors + evidence lines; explainability review | Low |
| R6 | Flag-OFF regression | Low | Medium | Fail-open path; None profile ≡ baseline sort | Low |
| R7 | Presentation invents personalisation | Low | High | Adapter pass-through only; docstring + test | Low |
| R8 | Unsupported windows/duration invented | Low | High | Explicit no-op / declared-only duration | Low |
| R9 | Process-local profile instability | Medium | Medium | Documented EP-004.1 limitation; under-claim KSI | Medium |
| R10 | K2 over-claim without Scorecard | Medium | Medium | Estimated deltas only; review Pass ≠ live lift | Medium |

**Overall residual risk:** Acceptable for gated rollout.
