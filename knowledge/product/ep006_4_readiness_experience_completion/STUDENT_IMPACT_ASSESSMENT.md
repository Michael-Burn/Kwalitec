# Student Impact Assessment — EP-006.4

**Template:** `../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-006.4 |
| **Title** | Readiness Experience Completion |
| **Date** | 2026-07-26 |
| **Author** | Product explainability delivery |
| **Student-visible change?** | Yes — canonical Home readiness card |
| **Production activation?** | Yes (presentation pass-through; no new educational flag) |
| **Related KSI categories** | K3 (primary); K8 (secondary) |

---

## 1. Student problem

**Student problem:**

> After EP-006.2/006.3, students could unpack *recommendation* why/evidence on Home, but the readiness percentage still felt opaque — drivers, confidence basis, review point, and readiness-specific next action were missing on the daily path (Analytics had them; Home did not).

**Evidence:**

> EP-006.3 PERC-01 / unsupported claim “Home readiness drivers student-visible”; EP-005.2 REM-05; EP-006.1 §3.3 Home Level-2 contract; Tier B note that bare % without named drivers risks over-precision.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | Readiness-specific `suggested_next_action` on Home L1 |
| How am I progressing? | Yes | Why + ordered drivers + confidence unpackable on Home |
| What is stopping me? | Yes | Supporting evidence + drivers name coverage / knowledge / discipline gaps |
| What happens next? | Yes | `review_point` on readiness disclosure |

**Student benefit summary:**

> Students can now inspect the **same authored readiness explanation** Analytics already showed — drivers, confidence, review point, and next action — on the canonical Home readiness card, without a new scoring brain.

**Final Test:** Does this help students become better professionals? **Yes** — professionals challenge estimates with named drivers and reassessment points; Home now surfaces that working.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | Reinforces **honest progress judgement** and reflection timing via review point |
| Risks rewarding activity vanity? | No — no new vanity metric; prefers inspectable drivers over soothing composite |
| Educational Constitution / honesty risks? | Mitigated — pass-through only; honest cannot-estimate path preserved; no Exam Ready marketing inflation |

**Learning benefit summary:**

> Learning improves when students can see *what drives* a readiness estimate and *when* to reassess — reducing false precision and enabling informed study choices.

---

## 4. Success metrics

| Metric | Baseline (post EP-006.3) | Target | How measured | Status |
|---|---|---|---|---|
| Home `readiness_drivers` non-empty when schema-complete | Empty (`()`) | ≥3 student labels | Contract + template tests | **Met (automated)** |
| Home L1 why + readiness next | Partial / borrowed | Authored readiness why + next | Template smoke | **Met (automated)** |
| Home L2 review_point + confidence | Missing / borrowed | Bound from readiness MES | Template smoke | **Met (automated)** |
| Fail-open when surface unavailable | N/A | Home still renders | Fallback tests | **Met (automated)** |
| Tier B readiness perception | PERC-01 open | Drivers visible majority | Successor pack | **Ready — not run** |
| Validated K3 lift | 57 (EP-005.1 lineage) | Modest lift if perceived | Tier B + re-score | **Not claimed** |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 | Untouched |
| Recommendation usefulness | K2 | 15 | 0 | Untouched (rec MES preserved) |
| Readiness usefulness | K3 | 12 | +2 | Home unpackability closes PERC-01 delivery gap |
| Personalisation | K4 | 12 | 0 | Untouched |
| Learning feedback | K5 | 10 | 0 | Untouched |
| Engagement quality | K6 | 10 | 0 | Untouched |
| Retention / habit | K7 | 12 | 0 | Untouched |
| Explainability | K8 | 14 | +1 | Mild — G1.5 already PASS; residual unpackability |
| **Weighted net ΔKSI** | | | **≈ +0.4** | Under-claimed pending Tier B |

**Confidence:** Medium — automated delivery complete; **validated** K3/K8 movement requires Tier B readiness perception.  
**Upstream validated assessment unchanged until re-score:** W-PROD KSI **60**; K8 **70**; G1.5 **PASS**.

---

## 6. Risks and assumptions

| Risk | Mitigation |
|---|---|
| Dual speech (recommendation next ≠ readiness next) | Cards separate; readiness card prefers readiness MES |
| Extra HomeService call cost | Same surface Analytics already uses; fail-open |
| Claiming validated K3 from delivery alone | Forbidden — Tier B successor required |
| Over-long disclosure | Cap drivers ≤4; evidence ≤5; reuse `learn_more` |

**Assumptions:** Production ReadinessService surface remains schema-complete for active learners with practice history; cold-start incomplete-schema nights remain weakly explained (PERC-02).

---

## 7. Non-goals

- Recalibrating readiness weights against exam outcomes  
- Dual-home consolidation (REM-02)  
- Cold-start copy rewrite (PERC-02)  
- Declaring validated KSI / K3 lifts without Tier B  

---

**End of STUDENT_IMPACT_ASSESSMENT**
