# Student Impact Assessment

**Programme / Milestone ID:** P-003.4  
**Title:** Product Assumption Register  
**Date:** 2026-07-26  
**Author:** Product Board documentation programme  
**Student-visible change?** No  
**Production activation?** None  
**Related KSI categories:** None (docs/governance packaging only)

**Template:** `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

---

## 1. Student problem

**Student problem:**

> Students do not directly experience “missing assumption documentation.” Indirectly, releasing or marketing Version 1 on unvalidated beliefs (e.g. perception = effectiveness, personalisation works while OFF, recommendations improve behaviour without measurement) would harm trust and learning. This programme does not change student-facing behaviour; it makes the Board’s epistemic status explicit so overclaim is harder.

**Evidence:**

> EP-007.3 effectiveness NO-GO / external N=0; EP-005.1 falsified estimate stacking; DR-033 perception ≠ effectiveness; DR-041 NO GO; P-003.3 PR-001/PR-002.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A | No student-visible change |
| How am I progressing? | N/A | No student-visible change |
| What is stopping me? | N/A | No student-visible change |
| What happens next? | N/A | No student-visible change |

**Student benefit summary:**

> Indirect only: clearer Board visibility of Hypothesis vs Validated vs Rejected assumptions reduces risk of shipping “believed” features as “known” educational value.

**Final Test:** Does this help students become better professionals? **Yes (indirect)** — by protecting honesty of claims that would otherwise mislead study behaviour. Not a direct learning intervention.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | N/A — no learning-path change |
| Risks rewarding activity vanity? | No |
| Educational Constitution / honesty risks? | Low — register restates evidence honesty; does not amend constitution |

**Learning benefit summary:**

> None direct. Preserves educational honesty by indexing which educational-usefulness claims remain hypotheses.

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| Board can distinguish known / believed / disproved / needs evidence from register alone | Fragmented across validation logs + SIAs | Indexes usable in 15–20 minutes | Board walkthrough | Product |
| Unsupported assumptions invented | 0 allowed | 0 | Traceability audit | Product |
| Student-visible regressions from this programme | N/A | None | N/A (docs-only) | — |

Activity vanity metrics: N/A.

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 | Docs only |
| Recommendation usefulness | K2 | 15 | 0 | Docs only |
| Readiness usefulness | K3 | 12 | 0 | Docs only |
| Personalisation | K4 | 12 | 0 | Docs only |
| Motivation | K5 | 10 | 0 | Docs only |
| Learning analytics | K6 | 10 | 0 | Docs only |
| Revision support | K7 | 12 | 0 | Docs only |
| Explainability | K8 | 14 | 0 | Docs only |

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | **0** |
| **Confidence** | High |
| **Assumes production / flag state** | Unchanged; no activation |

---

## 6. Validation plan

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| Traceability audit | Programme exit | Every PA cites evidence path | Orphan / invented PA |
| Board reading test | Post-publish | Indexes answer known/believed/disproved/needs evidence | Board still needs tribal knowledge |
| N/A cohort KPI | — | — | Docs-only; no M1–M9 movement expected |

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Register mistaken for new law that amends gates/decisions/risks | Medium | High | Confused release claims | README + review process: indexes epistemic status only |
| Supported treated as Validated in marketing | Medium | High | Overclaim | Status definitions; Rejected PA-025/023 callouts |
| Stale status treated as permanent | Medium | Medium | Wrong urgency | Validation Triggers; evidence freeze date |
| Accidental governance/runtime edits | Low | High | Student-facing drift | Programme constraint: docs folder only |

---

## 8. Assumptions

1. P-003.1–P-003.3 artefacts remain accurate as of 2026-07-26.  
2. External N remains 0 and Privacy Review unsigned until evidence programmes say otherwise.  
3. Board will use Validation Triggers when evidence updates (not rely on frozen statuses forever).  

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Assumption cards | `PRODUCT_ASSUMPTION_REGISTER.md` | Full PA inventory |
| Validated index | `VALIDATED_ASSUMPTIONS.md` | Known set |
| Unvalidated index | `UNVALIDATED_ASSUMPTIONS.md` | Believed / needs evidence |
| Rejected index | `REJECTED_ASSUMPTIONS.md` | Disproved / superseded |
| Traceability | `ASSUMPTION_TRACEABILITY.md` | DR/PR/programme links |
| Review process | `ASSUMPTION_REVIEW_PROCESS.md` | Maintenance discipline |
| Upstream registers | `../p003_2_*`, `../p003_3_*`, `../p003_1_*` | Decisions, risks, dossier |
| Validation chain | EP-005.*–EP-007.* | Status evidence |

---

## 10. Lessons learned for student value (exit)

- Students benefit when the Board *sees* Hypothesis behavioural claims (recommendations, personalisation, perception→behaviour) as first-class — but seeing them does not move KSI.  
- Separating **Validated law** (KSI bar, external evidence requirement) from **Validated score** (KSI = 62) prevents false “bar met” narratives.  
- Rejected shortcuts (estimate stacking, perception-as-effectiveness, GA-as-ready) are as important to student honesty as Supported perception wins.

---

## Appendix A — Optional blast-radius table

| Cohort / flag state | Student-visible change |
|---|---|
| Production defaults | None |
| Non-prod gated | None |

---

**End of Student Impact Assessment**
