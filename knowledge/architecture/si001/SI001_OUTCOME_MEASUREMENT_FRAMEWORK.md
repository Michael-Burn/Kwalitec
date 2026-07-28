# SI-001 — Outcome Measurement Framework

**Programme:** SI-001 — Student Intelligence  
**Version:** 1.0  
**Status:** Active — measurement architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `SI001_STUDENT_INTELLIGENCE_ARCHITECTURE.md`  
**Constraint:** No analytics collectors, warehouses, dashboards, or KSI re-baselines executed by this programme.

---

## 1. Purpose

Define how Kwalitec will measure whether Student Intelligence improves **learning** and, over time, **exam outcomes** — without conflating operational usefulness, educational release quality, engineering readiness, or marketing aspiration.

This framework operationalises Vision 2030 success metrics and Product Constitution claim honesty for the SI capability stack.

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| Vision 2030 | North star = materially higher pass probability for consistent users; learning ≠ activity |
| Product Constitution PC-02…PC-04 | Independent assessment boards; claims ≤ evidence |
| Product Success Framework (P-001.1) | KSI operational usefulness index; validated vs estimated |
| P-001.2 / P-001.3 | K8 / K2 measurement law for intelligence surfaces |
| Product Analytics Architecture | Metric catalogue; one educational truth; privacy |
| EVF / Educational Release Gates | Educational quality to release to students |
| P-002.1 / P-003.1 | Version 1 production-ready gates (G1–G12) — not satisfied by ΔKSI alone |
| ER-002 | Engineering claim-class bounds |

---

## 3. Measurement layers (normative separation)

Mixing these layers in one unchecked narrative violates PC-02 / PC-03.

| Layer | Question | Primary instruments | Owner board |
|-------|----------|---------------------|-------------|
| **L1 Operational usefulness** | Is guidance educationally useful day-to-day? | KSI (K1–K8), Decision Journal, completion | Product Success |
| **L2 Educational release quality** | May we release this intelligence to students? | EVF gates, Explainability / Recommendation checklists | Educational governance / EVF |
| **L3 Engineering operability** | Is the system safe for the claimed class? | P-002.1 G7–G12, ER programmes | Engineering |
| **L4 North-star outcomes** | Do consistent users pass at higher rates? | Longitudinal outcome studies (research) | Research + Product (ethics/privacy) |
| **L5 Experimentation signals** | Did a controlled change improve educational metrics? | Educational trial framework | Research under OA-001 lifecycle |

**KSI is not the north star.** Pass probability is. KSI is the operational index that supports progress toward that outcome.

---

## 4. Vision success metrics → SI instrumentation

| Vision metric | SI instrumentation (design) | Layer | Notes |
|---------------|----------------------------|-------|-------|
| Exam pass rate | Opt-in / privacy-preserving outcome study; long horizon | L4 | Not claimable from Alpha vanity |
| Predicted readiness accuracy | Calibration: readiness bands vs later performance / outcomes | L1→L4 | Honesty before precision theatre |
| Study consistency | Twin consistency facet + plan adherence aggregates | L1 | Behavioural substrate |
| Mission / Session completion | Execution evidence + completion rates | L1 | Domain Mission; UI Session |
| Revision adherence | Planned vs completed revision | L1 | Intelligent revision |
| Recommendation acceptance | Decision Journal accept/defer/reject | L1 | Trust substrate |
| Retention (product) | Continued use through exam cycle | L1 | Not streak gamification |
| Educational satisfaction | Structured check-ins / qualitative trust | L1 | Not NPS theatre alone |
| Confidence (evidenced) | Confidence trend + student-reported where lawful | L1 | Gradual; not vanity |

**Non-metrics (alone):** raw page views, undifferentiated engagement, tip-chrome clicks, video minutes without learning evidence.

---

## 5. KSI mapping for Student Intelligence

Future SI implementation programmes estimate ΔKSI with evidence. SI-001 itself: **ΔKSI = 0**.

| Category | SI relevance | Typical SI levers |
|----------|--------------|-------------------|
| K1 Clarity / next action | High | Primary recommendation consolidation |
| K2 Recommendation usefulness | Critical | P-001.3 quality; RE-H1…H3 |
| K3 Readiness honesty / usefulness | High | SI-C3 calibration & sparse evidence |
| K4 Consistency support | High | Mission Intelligence; pacing |
| K5 Progress clarity | Medium | Analytics projections; trajectory views |
| K6 Feedback / reflection | Medium–High | Reflection Intelligence (H3) |
| K7 Sustainable workload | Medium | Cognitive load / recovery recommendations |
| K8 Explainability | Critical | P-001.2 compliance on all intelligence speech |

**Rule:** K2 claims require Recommendation Review Pass (or waiver). K8 claims require Explainability Review Pass (or waiver). Estimated ΔKSI does not clear Gate G1.

---

## 6. Learning analytics architecture (alignment)

SI-001 adopts Product Analytics Architecture principles:

1. Learning over activity  
2. One Educational Truth — metrics project from Twin / Evidence / Educational State authorities  
3. Reproducible & auditable aggregates  
4. Privacy — student data belongs to the student  
5. No dual analytics surfaces inventing a second scoring brain  

```
Runtime A facts / Evidence / Decision Journal / Twin snapshots
        ↓
Metric definitions (versioned)
        ↓
Aggregation jobs / privacy filters (future programmes)
        ↓
Read models → Founder ops / research / product reviews
        ↓
Learner surfaces: only lawful educational projections
```

Canonical learner analytics remain History / Educational State projections — not a parallel `/analytics` educational story.

---

## 7. Outcome metric catalogue (SI-specific)

### 7.1 Recommendation effectiveness chain

```
Shown → Understood (explainability) → Accepted → Started → Completed → Learning movement
```

| Stage | Metric (design) | Failure signal |
|-------|-----------------|----------------|
| Shown | Eligible impressions under flag honesty | Over-showing sparse-evidence tips |
| Understood | Explanation schema compliance sample | Opaque Coach speech |
| Accepted | Accept rate / defer rate | Chronic dismiss without alternative |
| Started | Time-to-start after accept | Friction / wrong surface |
| Completed | Session/task completion of accepted item | Unrealistic recommendations |
| Learning movement | Mastery/readiness/revision adherence delta | Activity without learning |

### 7.2 Readiness calibration

| Metric | Definition (design) |
|--------|---------------------|
| Band stability | Readiness band changes only with evidence warrant |
| Overconfidence gap | High stated/shown readiness vs weak evidence rate |
| Underrating gap | Low readiness vs strong evidence rate |
| Outcome linkage (research) | Pre-exam readiness vs exam result (L4, consented) |

### 7.3 Twin health (operational, not vanity)

| Metric | Definition (design) |
|--------|---------------------|
| Completeness distribution | Structural facet availability over cohort |
| Provenance coverage | % consumer fields with expandable provenance |
| Shadow agreement | Dual-run divergence rate (when enabled) |
| Unknown discipline | Rate of lawful “unavailable” vs filled estimates (must stay honest) |

### 7.4 Experimentation outcomes

See Research Backlog. Trial metrics remain operational signals (acceptance, completion, activation) until L4 studies exist. **No autonomous policy promotion from thin lift.**

---

## 8. Evidence packs (claim discipline)

Any SI claim in product/marketing/release language must cite:

| Claim class | Required evidence |
|-------------|-------------------|
| “Recommendations are useful” | P-001.3 review Pass + Decision Journal metrics pack |
| “Explainable guidance” | P-001.2 review Pass + schema compliance sample |
| “Twin-powered” | Flag matrix + Twin Ready/Authority status artefacts |
| “Improves pass rates” | L4 study protocol + results; never Alpha anecdote |
| “Experimentally proven lift” | Trial design, cohort rules, pre-registered metrics, Independent Review |
| “Version 1 production-ready” | Full P-002.1 / P-003.1 — out of scope for SI alone |

---

## 9. Multi-release measurement roadmap

| Horizon | Measurement focus |
|---------|-------------------|
| **OM-H0** | This framework freeze; map Vision metrics → layers |
| **OM-H1** | Decision Journal completeness; explainability compliance sampling; KSI estimation discipline for SI programmes |
| **OM-H2** | Twin health + readiness honesty dashboards for ops (Founder); dual-run divergence packs |
| **OM-H3** | Closed-loop effectiveness packs; authorised trial lift reports; reflection participation (non-coercive) |
| **OM-H4** | Consented longitudinal pass-probability research design execution |

---

## 10. Privacy and ethics constraints

Aligned with Vision data principles:

- Student data belongs to the student  
- Minimise PII in research extracts  
- Opt-in for exam outcome linkage where required by law/ethics  
- No silent exfiltration to opaque vendors without security/privacy review  
- Reflection content especially sensitive — default non-persistence until ADR  

---

## 11. Traceability

| Vision 2030 | Framework element |
|-------------|-------------------|
| North star | L4 outcome studies |
| Learning ≠ activity | Non-metrics list; L1 catalogue |
| Success metrics table | §4 mapping |
| Auditable recommendations | Decision Journal chain §7.1 |
| Final Test | Evidence packs §8 |

| Product Constitution | Framework element |
|----------------------|-------------------|
| PC-02 | Layer separation §3 |
| PC-03–PC-04 | Evidence packs §8 |
| PC-12 | No silent claim expansion from weak trial lift |

---

## 12. Explicit non-goals

- Recomputing validated KSI in SI-001  
- Implementing analytics pipelines  
- Declaring north-star outcome proof  
- Using activity vanity to justify SI features  

---

**End of SI001_OUTCOME_MEASUREMENT_FRAMEWORK**
