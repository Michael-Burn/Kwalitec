# Student Impact Assessment — EP-008.1

**Template:** `../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-008.1 |
| **Title** | Recommendation Trust |
| **Date** | 2026-07-26 |
| **Author** | Product engineering (design programme) |
| **Student-visible change?** | **Yes** (EP-008.1A presentation on sole-runtime Home/Coach; Mission/Revision parity) |
| **Production activation?** | Presentation defaults; no new feature flags |
| **Related KSI categories** | **K2** (primary); **K8** (secondary) |

---

## 1. Student problem

**Student problem:**

> I can see tonight’s tip, but I am not sure I should trust it over my own notes. I often cannot tell why it matters *now*, what improvement to expect, whether it fights today’s mission, what else was considered, or how finishing practice will change tomorrow’s tip — so I hesitate, second-guess, or ignore the recommendation.

**Evidence:**

> Validated K2 **55** (W-PROD / EP-007.2 lineage; DR-051); P-004.1 PP-001 / RC-05 / IMP-01; EP-005.2 REM-06; historical Coach opacity themes (partially mitigated by EP-006.2/006.3 MES pass-through); DR-036 effectiveness freeze; PA-014 Hypothesis; no acceptance KPI; plan coherence / alternatives / honest refusal still unbound on Home despite Runtime A authorship (EP-003.1).

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes (successor) | Clear next + single Start Session CTA retained |
| How am I progressing? | Partial | Benefit + readiness bridge; not a full analytics redesign |
| What is stopping me? | Yes | Evidence, confidence, refusal honesty, coherence label |
| What happens next? | Yes | Review point / completion-loop echo |

**Student benefit summary:**

> When implemented, serious candidates get an inspectable recommendation: why it exists, why it matters tonight, what to do, what improvement to expect, how practice feeds future tips, plus coherence and alternatives or an honest empty state — without a “smarter” opaque coach.

**Final Test:** Does this help students become better professionals? **Yes** — professionals justify priorities with evidence, label uncertainty, and revise plans after work; the trust surface models that habit.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | Reinforces **decision quality** and **trustworthy follow-through**; review point supports reflection timing |
| Risks rewarding activity vanity? | **No** if copy stays educational; mitigate by forbidding Exam Ready / guaranteed lifts |
| Educational Constitution / honesty risks? | Mitigated — pass-through MES; honest refusal; no LLM truth; ranking untouched |

**Learning benefit summary:**

> Learning improves when students *choose* to follow guidance they understand. Trust presentation converts opaque tips into inspectable study priorities, increasing the chance that scarce study time is spent on the authorised next step.

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| Home trust field binding (T1–T11) | Partial (why/next/L2; missing coherence/alts/refusal/L1 benefit) | Complete on schema-complete path | Contract tests TR-A0* | Eng |
| Student can restate why + next | Weak (perception residual) | Pass on Tier B trust pack | Blind review / interviews | Product |
| Willingness to follow tip (stated) | Unmeasured / low trust anecdotes | Directional improvement in Tier B | Interview codes | Product |
| Honest refusal perception | Cold-start residual | Prefer refusal over fake confidence | Tier B H3 | Product |
| Validated K2 | 55 | Planning **67–73** after Tier B (prefer-lower); Strong-band deferred | KSI re-score | Product |
| Acceptance rate | Not instrumented | N/A this programme | EP-008.3 | Product |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta (category points) | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 to +2 | Coherence may reduce mission fight perception; prefer under-claim → **0** in net |
| Recommendation usefulness | K2 | 15 | **+12 to +18** | IMP-01 primary lever; inspectability closes RC-05 presentation gap |
| Readiness usefulness | K3 | 12 | 0 | Readiness panel unchanged (link only) |
| Personalisation | K4 | 12 | 0 | Flags remain OFF |
| Motivation | K5 | 10 | 0 to +2 | Secondary; do not claim |
| Learning analytics | K6 | 10 | 0 | No analytics redesign |
| Revision support | K7 | 12 | 0 to +2 | Alternatives explanations on Revision; minor |
| Explainability | K8 | 14 | **+3 to +6** | Residual deepen via coherence/refusal/benefit L1 |

**Net estimated KSI contribution** (weighted, prefer under-claim):

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | **+1.5 to +2.5** (planning; matches IMP-01) |
| **Midpoint used for portfolio** | ≈ **+2.0** |
| **Confidence** | Medium (presentation evidence strong; perception not yet re-run) |
| **Assumes production / flag state** | Sole-runtime W-PROD Home; personalisation OFF; **after successor delivery + Tier B** |

**This design programme alone:** **ΔKSI = 0** (docs only — no student-visible change until implementation).

Illustrative math (implementation success, mid band):  
K2 +15 × 0.15 = +2.25; K8 +4 × 0.14 = +0.56; de-duped prefer-lower → **~+1.5 to +2.5**.

---

## 6. Validation plan

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| Contract tests TR-A0* | Delivery | All green | Missing bindings |
| Dogfood UI checklist | Delivery | §12 Pass | Clutter / jargon |
| Tier B blind / interviews | Post-delivery | H1–H3 supported | Opacity / overclaim |
| Prefer-lower K2 re-score | After Tier B | K2 moves into Partial-upper / Strong-floor band | Score stuck ≤55 |
| Acceptance KPI | EP-008.3 | Separate | — |

Detail: [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md).

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Over-claiming benefit / readiness | Medium | High | False confidence | Authored MES only; copy bans |
| L1 clutter / decision fatigue | Medium | Medium | Ignore tip | Alternatives in L2; ≤2 alts |
| Dual Coach/Home messaging | Low | Medium | Confusion | Same DTO fields |
| Ranking temptation | Medium | High | Wrong fix for trust | Hard non-goal; IMP-11 gated |
| Privacy / accept events early | Low | Medium | Scope creep | EP-008.3 boundary |

---

## 8. Assumptions

1. Runtime A continues to emit schema-complete MES including coherence, refusal, alternatives, benefit, review.  
2. Sole-runtime Student Home remains the primary daily path (EP-007.x).  
3. Students will use L2 disclosure at least sometimes for evidence; L1 carries the five success answers.  
4. Tier B capacity exists after delivery; without it, K2 lifts stay unclaimable.  
5. EP-008.3 will follow for acceptance measurement; Strong-band K2 is not expected from UI alone.

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Design package | `knowledge/product/ep008_1_recommendation_trust/` | Trust contract defined |
| Upstream diagnosis | P-004.1 / EP-005.2 REM-06 / EP-006.x | Problem real; MES already authored |
| Implementation evidence | `IMPLEMENTATION_COMPLETION_REPORT.md`, `TEST_REPORT.md`, TR-A0* tests | Student-visible trust presentation shipped; contract satisfied |
| Tier B / K2 re-score | *Pending* | Validated ΔKSI — **not claimed** |

---

## 10. Lessons learned for student value (exit)

> Design-time: K2’s remaining gap is **inspectability and agency speech**, not missing ranking maths. MES delivery (EP-006.2) was necessary but not sufficient — coherence, alternatives, refusal, L1 benefit, and completion-loop honesty were still the missing trust layer.

> Implementation (EP-008.1A): Trust Contract T1–T11 is now bound on the sole-runtime Home/Coach path (with Mission coherence + Revision alternative explanations) without changing Runtime A educational reasoning. **Tier A structural Pass only** — no KSI, educational-effectiveness, or student-benefit claim until Tier B perception validation.

---

## Appendix A — Blast radius

| Cohort / flag state | Student-visible change |
|---|---|
| Production sole-runtime (this delivery) | Home/Coach/Mission/Revision trust UI (presentation only) |
| Design programme artefacts | Unchanged authority |
| Personalisation flags | Unchanged (OFF) |
| Accept/dismiss | Not introduced (EP-008.3) |

---

**End of STUDENT_IMPACT_ASSESSMENT**
