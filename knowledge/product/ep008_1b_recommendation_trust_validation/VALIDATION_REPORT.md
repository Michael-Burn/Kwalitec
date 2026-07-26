# EP-008.1B — Validation Report (Recommendation Trust Perception)

**Programme:** EP-008.1B — Recommendation Trust Validation (Tier B)  
**Date:** 2026-07-26  
**Claim window:** W-PROD (sole-runtime Student Home after EP-008.1A)  
**Tier B archive:** [`tier_b_reviews/`](tier_b_reviews/) (N=9)  
**Baseline perception:** EP-004 corpus + EP-006.3 Tier B (K2 **55**; inspectability residual REM-06 / IMP-01)  
**Method:** [`PERCEPTION_METHODOLOGY.md`](PERCEPTION_METHODOLOGY.md) · EP-008.1 [`VALIDATION_PLAN.md`](../ep008_1_recommendation_trust/VALIDATION_PLAN.md)

---

## 1. Executive verdict

| Question | Verdict |
|---|---|
| Did Recommendation Trust improve student perception of recommendations? | **Yes** on schema-complete nights |
| Did it improve validated **K2**? | **Yes** — **55 → 68** (prefer-lower; Medium confidence) |
| Should trust presentation become permanent? | **Yes** |
| Is EP-008.3 justified? | **Yes** — acceptance KPIs / Strong-band K2 still open |
| Unexpected regressions? | **None material** on schema-complete path; cold-start residual unchanged |

**Board one-liner:** Trust presentation clears the inspectability gap that kept K2 at 55; it does **not** prove tip acceptance rates or educational effectiveness.

---

## 2. Dimension findings vs baseline

| Dimension | Baseline (pre–EP-008.1A) | Post–EP-008.1A Tier B | Meaningful change? |
|---|---|---|---|
| Recommendation clarity | Partial (why/next via MES; why-now / benefit / coherence unbound) | **Majority Pass** | **Yes** |
| Understanding (five success questions) | Incomplete | **Majority Pass** on schema-complete | **Yes** |
| Actionability | Next often clear; tip hesitation residual | **Majority Pass** | **Yes** (stated) |
| Trust | Conditional; Coach opacity mitigated but trust residual | **Pass / Conditional Pass** majority | **Yes** |
| Confidence | Suggested available; refusal speech incomplete | **Pass**; refusal Cannot-yet **Pass** | **Yes** |
| Acceptance (stated willingness) | Low / unmeasured anecdotes | **Majority Pass** (H2 supported) | **Yes** (stated only) |
| Completion intention | Review sometimes present; loop unclear | **Majority Pass** | **Yes** |
| Coherence (Q9) | Authored but unbound on Home | **Majority Pass** | **Yes** |
| Alternatives / refusal (Q10) | Unbound | **Pass** (H3/H4) | **Yes** |

Cold-start / incomplete schema remains **Fail** for trust speech — prefer-lower applied.

---

## 3. Hypothesis outcomes (VALIDATION_PLAN §4.2)

| ID | Result | Evidence |
|---|---|---|
| **H1** | **Supported** | 9/9 can state why/evidence on schema-complete; opacity not majority |
| **H2** | **Supported** | 9/9 stated willingness Pass (stated acceptance; not behavioural KPI) |
| **H3** | **Supported** | SV-008 / SV-013 / majority prefer honest refusal over fake tip |
| **H4** | **Supported (non-blocking)** | Alternatives add agency; no overwhelm / primary-CTA ignore majority |

Tier B exit (VALIDATION_PLAN §4.3): **Themes support H1–H3; H4 non-blocking** → eligible for prefer-lower K2 lift.

---

## 4. Cohort & codes

| Item | Value |
|---|---|
| Personas | SV-003, 005, 008, 010, 011, 012, 013, 014, 015 |
| N | 9 |
| Schema-complete five-question Pass | 9/9 |
| Stated acceptance Pass | 9/9 |
| Refusal honesty Pass | 9/9 (H3) |
| Confidence Conditional (benefit watch) | SV-013 |
| Trust Conditional (adaptation / mature-system) | SV-003, SV-012 |

Detailed theme roll-up: [`STUDENT_FEEDBACK_SUMMARY.md`](STUDENT_FEEDBACK_SUMMARY.md).

---

## 5. Secondary effects & regressions

| Area | Finding |
|---|---|
| **K8** | Structured Coach + L1 benefit / coherence / refusal deepen explainability → prefer-lower **70 → 72** |
| **K1** | Coherence reduces silent mission fight; **no** category lift claimed (prefer 0) |
| Ranking / precision | Unchanged — **no** claim |
| Acceptance rates | **Not measured** — EP-008.3 |
| Coach opacity | Remains minority on schema-complete; structured bullets further reduce residual |
| Overclaim | Mild benefit-language watch (SV-013) — not a P1 honesty incident |
| Clutter | L1 denser; not Fail (SV-015) |
| Cold-start | Unchanged residual |

---

## 6. Evidence quality & confidence

| Factor | Assessment |
|---|---|
| Tier A | EP-008.1A TR-A01–TR-A08 Pass |
| Tier B | N=9 persona re-reviews filed |
| External Stage 1 | N=0 |
| Behavioural acceptance KPI | Absent |
| Composite confidence | **Medium** (methodology ceiling without external N) |

Statistically this is a **qualitative cohort shift**, not an external RCT. Sufficient Tier B under EP-005.1 to support category re-score with **Medium** confidence — not High, not Stage 1 product-decision KPIs.

---

## 7. Claims explicitly not made

- Validated acceptance / completion **rates**  
- K2 ≥ 75 Strong mid-band  
- Educational-effectiveness GO / exam outcomes  
- Ranking quality improvement  
- Overall Gate G1 PASS  

---

## 8. Board recommendations

1. **Adopt permanently** Recommendation Trust presentation (T1–T11) on sole-runtime Home/Coach.  
2. **Publish** validated K2 **68** / KSI **64** (see [`KSI_IMPACT_REPORT.md`](KSI_IMPACT_REPORT.md)).  
3. **Commission EP-008.3** for accept/dismiss instrumentation under approved PRD — required for Strong-band K2 and effectiveness claims.  
4. **Keep** honesty discipline on benefit copy; monitor overclaim in dogfood.  
5. **Do not** treat this pack as Stage 1 effectiveness evidence.

---

**End of VALIDATION_REPORT**
