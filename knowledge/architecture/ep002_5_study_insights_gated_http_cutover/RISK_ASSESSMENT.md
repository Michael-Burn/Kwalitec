# EP-002.5 — Risk Assessment

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
**Date:** 2026-07-26  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Production-wide student UX flip | Low | High | Cutover + Twin default OFF; production env hard-excludes eligibility |
| R2 | Bridge / Founder inherit Twin payloads | Medium | High | Cutover only in dashboard service methods; `generate_recommendations` remains legacy |
| R3 | Double Twin assemble (dual-run + cutover) | Medium | Medium | Skip dual-run when cutover eligible |
| R4 | Template / explainability overwrite Twin honesty | Medium | Medium | Project full card fields; skip enrich for `source_authority=study_insights` |
| R5 | Operators treat fingerprint mismatch as failure | Medium | Low | Alignment uses topic_id / title heuristics; docs forbid fingerprint-as-gate |
| R6 | Twin latency regresses dashboard TTFB | Medium | Medium | Measure P95; kill switch; request remains fail-open to legacy |
| R7 | Blocking rules too strict → cutover never serves | Medium | Low | Tunable code set; metrics for limitation-driven fallback rate |
| R8 | Blocking rules too loose → empty/unhelpful UX | Low | Medium | Require actionable focus or next-action; projection_empty → legacy |
| R9 | Scope creep into readiness / mission cutover | Medium | High | Explicit out-of-scope; EP-002.6–7 own those surfaces |
| R10 | Claiming Twin Ready (T7) | Low | High | Explicit non-claim in completion report |

---

## 2. Residual acceptance

**O:** First student-visible Twin guidance always carries narrative and latency risk.  
**E:** EP-002.3 soak + EP-002.4 dual-run provide operational substrate; fail-open is constitutional.  
**C:** Residual risk is acceptable for **gated non-production** activation only.  
**R:** Do not enable production Cutover / Twin until EP-002.5 metrics + rollback drill are green on staging.

---

## 3. Ownership / constitutional risks

| Invariant | Risk if violated | Guard |
|---|---|---|
| Insight communicates only | Inventing scores in projection | Projection maps existing Insight fields only |
| Runtime A writes unchanged | Accidental write from cutover | Read-only path |
| Curriculum V1/V2 | Traversal fork | No curriculum edits |
| Fail-open | Student error pages | Broad try/except + legacy return |

---

## 4. Go / no-go for implementation

| Gate | Status |
|---|---|
| Discovery complete | Yes |
| Cutover Design recorded | Yes |
| Eligibility Matrix recorded | Yes |
| Rollback Plan recorded | Yes |
| Risk Assessment recorded | Yes |
| Production activation authorised | **No** |

**Conclusion:** Implementation authorised for gated non-production cutover only.  
