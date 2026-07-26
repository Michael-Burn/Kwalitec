# Student Impact Assessment — EP-008.3

**Template:** `../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-008.3 |
| **Title** | Recommendation Commitment & Follow-through |
| **Date** | 2026-07-26 |
| **Author** | Product engineering (design programme) |
| **Student-visible change?** | **Yes** (successor delivery: commit / defer / reflection / history) |
| **Production activation?** | Successor defaults on sole-runtime path; observational metrics research-bound |
| **Related KSI categories** | **K2** (primary); **K7** (secondary); **K8** (hold / no regression) |

---

## 1. Student problem

**Student problem:**

> I finally understand why tonight’s tip is the priority — but I still don’t *choose* it as my commitment. When I can’t do it, I just ignore the app. When I finish, I’m not sure what changed or how it connects to one continuous plan. So follow-through stays accidental, and I can’t tell whether I’m studying with the product or around it.

**Evidence:**

> EP-008.1B validated K2 **68** (stated willingness Pass; acceptance KPI absent — `TRUST-PERC-06`); KSI **64**; PSF K2 requires acceptance/follow-through for Strong-band; P-004.1 IMP-02 / GAP-06; EP-008.1 deferred accept UI explicitly; Decision Journal `record_decision` exists but student HTTP commitment UX missing; Learning Experience Programme requires conscious daily commitment → completion → reflection → next guidance; Product Constitution: advice advisory — students must retain honest agency.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | Commit makes the tip a chosen next step; Start Session remains primary |
| How am I progressing? | Yes | Reflection + history narrative of completed / deferred choices |
| What is stopping me? | Yes | Honest defer reasons without shame |
| What happens next? | Yes | Reflection “what next” + plan continuity + Runtime A tip regeneration |

**Student benefit summary:**

> Serious candidates get an educational execution loop: understand the tip (already shipped), consciously commit or honestly defer, complete a session, see what changed, and recognise the work as part of one continuous study plan — without a smarter opaque coach.

**Final Test:** Does this help students become better professionals? **Yes** — professionals commit to priorities, renegotiate honestly when blocked, and review what changed after work; the loop models that habit without gamified compliance.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | Reinforces **commitment**, **honest renegotiation**, **reflection**, and **plan continuity**; history supports revision narrative (K7) |
| Risks rewarding activity vanity? | **Mitigated** — no streaks/points; metrics observational only; commit ≠ mastery |
| Educational Constitution / honesty risks? | Mitigated — preference/intent claim; authored reflection; no LLM; ranking untouched |

**Learning benefit summary:**

> Learning improves when scarce study time is *chosen* and closed honestly. Commitment converts inspectable advice into intentional practice; deferral prevents fake compliance; reflection closes the feedback loop so tomorrow’s tip feels earned rather than random.

---

## 4. Success metrics

| Metric | Baseline | Target | How measured | Owner |
|---|---|---|---|---|
| Conscious commitment UX | Absent | Live on schema-complete Home | CF-A01 / dogfood | Eng |
| Honest defer UX | Absent | Catalogue + calm ack | CF-A03 / Tier B H2 | Eng / Product |
| Reflection after completion | Partial review echo | Full brief reflection block | CF-A06 / Tier B H3 | Eng |
| Recommendation narrative history | Absent / weak | ≤10 educational entries | CF-A07 / Tier B H4 | Eng |
| Commitment rate (research) | Uninstrumented | Baseline established | Observational KPI | Product |
| Completion among committed | Uninstrumented | Directional | Observational KPI | Product |
| Cognitive load | Trust baseline OK (EP-008.1B H4) | No increase | Tier B H5 | Product |
| Validated K2 | 68 | **≥75** after Tier B + KPIs (prefer-lower) | KSI re-score | Product |
| K7 | 58 | Directional +2–6 if themes support | KSI re-score | Product |
| K8 | 72 | Hold ≥72 | Regression watch | Product |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Estimated delta (category points) | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | 0 to +2 | Continuity may help; prefer **0** in net |
| Recommendation usefulness | K2 | 15 | **+7 to +12** | IMP-02 behavioural unlock; Strong-band target |
| Readiness usefulness | K3 | 12 | 0 | Unchanged |
| Personalisation | K4 | 12 | 0 | Flags OFF |
| Motivation | K5 | 10 | 0 to +2 | Honest defer; do not claim |
| Learning analytics | K6 | 10 | 0 | Research metrics ≠ student analytics redesign |
| Revision support | K7 | 12 | **+2 to +6** | History + continuity narrative |
| Explainability | K8 | 14 | **0** (hold) | Must not regress |

**Net estimated KSI contribution** (weighted, prefer under-claim):

| Estimate | Value |
|---|---|
| **Net ΔKSI (points)** | **+1.0 to +2.5** (planning; after delivery + Tier B + KPIs) |
| **Midpoint used for portfolio** | ≈ **+1.5** |
| **Confidence** | Medium (depends on shame/load control and KPI floors) |
| **Assumes production / flag state** | Sole-runtime W-PROD; personalisation OFF; Trust Contract permanent |

**This design programme alone:** **ΔKSI = 0** (docs only).

Illustrative math (implementation success, mid band):  
K2 +9 × 0.15 = +1.35; K7 +4 × 0.12 = +0.48; K8 0 → de-duped prefer-lower → **~+1.0 to +2.5**.

---

## 6. Validation plan

| Method | When | Success signal | Failure signal |
|---|---|---|---|
| Contract tests CF-A0* | Delivery | All green | Missing bindings / claim leak |
| Dogfood UI checklist | Delivery | §13 Pass | Dual CTA / shame / clutter |
| Observational KPIs | Post-delivery | Baselines live | Metrics feed ranking |
| Tier B perception | Post-delivery | H1–H3; H5–H6 hold | Shame / load / Twin theatre |
| Prefer-lower K2 re-score | After Tier B + KPIs | K2 ≥ 75 eligible | Stuck at 68 or regression |

Detail: [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md).

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Commitment as dark pattern | Medium | High | Coerced compliance | Calm copy; defer first-class; no streaks |
| Cognitive load / dual CTA | Medium | High | Ignore tip | DR-050; Pattern A combined start; Tier B H5 |
| Reflection invents AI learning | Medium | High | False trust | Humble frames; authored MES only |
| History audit clutter | Medium | Medium | Avoid History | Cap entries; narrative tone |
| Metrics → ranking temptation | Medium | High | Wrong educational authority | Hard STOP; research-only |
| Privacy of defer reasons | Low–Medium | Medium | Preference oversharing | Preference claim; PRD / pilot gates |
| K8 regression | Low–Medium | High | Opacity returns | Regression tests + Tier B H6 |

---

## 8. Assumptions

1. Trust Contract T1–T11 remains permanent and bound on schema-complete nights.  
2. Runtime A continues to author tips, review points, and benefits without ranking changes.  
3. Existing session completion / reflection shell can host completion reflection.  
4. Decision Journal / learning-feedback preference path remains lawful for intent-only claims.  
5. Tier B + observational KPI capacity exists after delivery; without them K2 ≥ 75 stays unclaimable.  
6. Students will sometimes defer honestly if the UI does not punish them.

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Design package | `knowledge/product/ep008_3_recommendation_commitment_followthrough/` | Commitment contract defined |
| Upstream trust validation | EP-008.1B | Understanding ready; behaviour gap real |
| Implementation evidence | `IMPLEMENTATION_COMPLETION_REPORT.md`, `TEST_REPORT.md` | Student-visible loop shipped (structural) |
| Tier B / KPI / K2 re-score | *Pending* | Validated ΔKSI — **not claimed** |

---

## 10. Lessons learned for student value (exit)

> Design-time: After Recommendation Trust, the remaining student-value gap is **execution with agency** — conscious commitment, honest deferral, and a closed reflection loop inside one continuous plan. Instrumenting acceptance without educational UX would measure ghosts; UX without observational metrics would repeat the Strong-band block. Neither may change Runtime A reasoning.

> Implementation: EP-008.3A shipped the commitment loop on Home / Mission / History with Pattern A (combined Start Session), observational events, and CF-A0* structural Pass. Validated student benefit / K2 ≥ 75 remain **pending Tier B + KPI floors** — not claimed from delivery alone.

---

## Appendix A — Blast radius

| Cohort / flag state | Student-visible change |
|---|---|
| Design programme artefacts | Authority / plans only |
| Successor sole-runtime delivery | Home commit/defer; reflection; history narrative |
| Personalisation flags | Unchanged (OFF) |
| Runtime A ranking / Planning / Readiness cores | Unchanged |
| Operator research metrics | Aggregates only; no student gamification |

---

**End of STUDENT_IMPACT_ASSESSMENT**
