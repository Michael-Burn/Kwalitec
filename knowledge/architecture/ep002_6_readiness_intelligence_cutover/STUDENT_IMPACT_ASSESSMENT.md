# EP-002.6 — Student Impact Assessment

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Date:** 2026-07-26  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Who can be affected

| Cohort | Impact |
|---|---|
| Production students | **None** — production always ineligible |
| Non-prod students with Twin OFF | **None** — legacy surface |
| Non-prod students with Twin ON + Cutover OFF | **None visible** — dual-run diagnostic only |
| Non-prod students with Twin ON + Cutover ON + eligible success | **Yes** — readiness score / weak-strong lists may reflect Twin intelligence |
| Non-prod eligible but Twin failure / blocking | **None visible vs legacy** — fail-open |

---

## 2. What students see when Twin is served

| Surface element | Change |
|---|---|
| Composite readiness score | May differ within projection rules; carries `confidence_level` |
| Weakest / strongest topic lists | May include Twin area reasons; still template-compatible rows |
| Review backlog / streaks / coverage widgets | Unchanged (legacy) |
| Syllabus `calculate_readiness` progress | Unchanged |
| Recommendation cards | Independent Study Insights cutover (EP-002.5) |

**O:** Templates do not require structural changes.  
**C:** Student-visible delta is limited to readiness hero metrics and topic highlight lists on `/dashboard` and `/analytics`.

---

## 3. Honesty / limitation speech

When Twin cannot truthfully assess readiness, students continue to receive legacy
scores rather than invented Twin copy. Blocking limitations never force empty
or fabricated readiness onto the page.

---

## 4. Blast radius controls

- Dedicated cutover flag (default OFF)
- Non-production env gate
- Legacy fail-open on every Twin failure class
- Collectors excluded from cutover path
- Experience `/student` home not on this cutover path

---

## 5. Assessment verdict

| Question | Answer |
|---|---|
| Production student impact | None by design |
| Eligible cohort impact | Bounded readiness surfaces only |
| Behaviour outside eligible cohorts | Unchanged |
| Rollback to zero student Twin influence | Cutover OFF and/or Twin OFF |

**R:** Accept bounded non-prod student impact as the price of constitutional surface activation; keep production OFF until staging soak evidence.
