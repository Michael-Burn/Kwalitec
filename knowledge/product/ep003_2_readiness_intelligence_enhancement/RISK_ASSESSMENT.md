# EP-003.2 — Risk Assessment

**Programme:** EP-003.2 — Readiness Intelligence Enhancement  
**Date:** 2026-07-26  

---

## 1. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Presentation narrative text changes for schema-complete surfaces | High | Medium | Pass-through uses authorised schema fields; templates still consume `ReadinessNarrative` |
| R2 | Twin confidence string changes from `medium` → `Moderate confidence` | High | Low | Student-safe mapping required by P-001.2; dual-run diagnostics remain operational |
| R3 | Mission lookup failure breaks next action | Low | Medium | Fail-open catch; fallback session copy |
| R4 | Students confuse coverage % with Estimated readiness | Medium | Medium | Schema labels estimate; coverage narrative untouched |
| R5 | Quality wrap accidentally applied to `get_overall_readiness` | Low | Critical | Contract forbids; regression test asserts bare keys |
| R6 | Over-claiming K3 without cohort proof | Medium | Medium | Under-claim ΔKSI; live re-score pending |
| R7 | Change reasoning without stored previous score feels generic | Medium | Low | Driver-based narrative always present; previous_score optional |

---

## 2. Residual risks after mitigation

- No persisted readiness history — deltas only when caller supplies `previous_score`.
- Domain structural readiness still parallel and unwired to HTTP.
- Cutover OFF students get enriched legacy schema; cutover ON students get enriched Twin projection — wording may differ slightly while components align.

---

## 3. Rollback

- Feature flags unchanged; disable Twin / cutover as before.
- Quality module is additive: removing `apply_readiness_quality_contract` calls restores pre-EP-003.2 surfaces (not required for production safety — fail-open preserved).
