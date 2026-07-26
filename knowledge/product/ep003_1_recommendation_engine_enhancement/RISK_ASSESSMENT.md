# EP-003.1 — Risk Assessment

**Programme:** EP-003.1 — Recommendation Engine Enhancement  
**Date:** 2026-07-26  

---

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Honest refusal increases “empty coach” perception for cold-start users | Medium | Medium | Refusal includes clear next action to build evidence / follow Mission | Monitor dogfood; copy may iterate |
| R2 | Ladder reordering surprises students used to Critical weak-topic primacy over rest | Low | Medium | Critical Rest maps to ladder rank 1 (safety); tests lock order | Documented in Gap Analysis |
| R3 | Mission surface lookup adds latency / failure modes | Low | Low | Fail-open; coherence skipped on exception | Acceptable |
| R4 | Presentation pass-through skips EIP-003 enrich and regresses templates | Medium | Medium | Schema includes `observed_facts` / `next_action` / `educational_advice`; adapter tests | Template smoke via existing dashboard paths |
| R5 | Timestamp-sensitive equality tests flake | Medium | Low | Compare educational identity without `generated_at` | Done for advisory injection test |
| R6 | Accidental ownership violation (planning/readiness maths in quality module) | Low | High | Constitutional tests assert no `generate_today_mission` / no weak-topic recalculation | Ownership certification artefact |
| R7 | Twin Study Insights order disturbed by schema normalisation | Low | Medium | Preserve Twin title order when `source_authority=study_insights` | Covered in service helper |
| R8 | Over-claiming K2 without live cohort evidence | Medium | Medium | Estimated KSI only; under-claim; freeze on marketing effectiveness remains | KSI Impact Assessment |

**Overall risk posture:** Acceptable for gated / non-marketing rollout. No production Twin cutover changes required.
