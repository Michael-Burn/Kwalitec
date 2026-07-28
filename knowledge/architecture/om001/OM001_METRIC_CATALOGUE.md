# OM-001 — Metric Catalogue

**Programme:** OM-001 — Outcomes Measurement  
**Version:** 1.0  
**Status:** Active — permanent educational metric catalogue (design only)  
**Effective:** 2026-07-28  
**Companion to:** `OM001_OUTCOME_MODEL.md`, `OM001_MEASUREMENT_STANDARD.md`  
**Constraint:** Definitions only — no collectors or dashboards shipped by this programme.

---

## 1. Purpose

Catalogue the permanent **educational success metrics** Kwalitec uses to evaluate Student Intelligence and related educational claims.

IDs are stable. Implementations in future programmes must adopt these IDs (or version them) rather than inventing parallel vanity metrics.

---

## 2. How to read an entry

Each metric follows the Measurement Standard contract. Shorthand columns:

- **L** = layer (L1–L5)  
- **CB** = claim boundary  
- **SI** = primary SI capabilities  
- **Conf** = minimum confidence class before strong claim language  

**Non-metrics (alone):** raw page views, undifferentiated engagement, tip-chrome clicks, video minutes without learning evidence, gamification streaks as success.

---

## 3. Educational success metrics (index)

| Family | Prefix | Scope coverage |
|--------|--------|----------------|
| Recommendation acceptance & effectiveness | `OM-REC` | Recommendation acceptance; guidance chain |
| Study consistency | `OM-CON` | Study consistency metrics |
| Mission / Session completion quality | `OM-MSN` | Mission completion quality |
| Learning outcomes | `OM-LRN` | Learning outcome indicators |
| Behavioural indicators | `OM-BHV` | Behavioural indicators (supporting) |
| Readiness prediction evaluation | `OM-RDY` | Readiness prediction evaluation |
| Explainability effectiveness | `OM-EXP` | Explainability effectiveness |
| Reflection usefulness | `OM-REF` | Reflection usefulness |
| Longitudinal progress | `OM-LNG` | Longitudinal student progress |
| Twin / analytics integrity | `OM-TWN` | Twin health (operational) |
| Experimentation / trial | `OM-TRIAL` | L5 operational trial signals |
| North-star transfer | `OM-NS` | Exam pass probability research |

---

## 4. Recommendation acceptance & effectiveness (`OM-REC`)

Effectiveness chain: **Shown → Understood → Accepted → Started → Completed → Learning movement**.

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-REC-01** | Eligible impressions | Count of recommendation surfaces where guidance was eligible under flag honesty | L1 | organisation | C2,C7 | C1 |
| **OM-REC-02** | Understood rate | Share of sampled impressions where explanation schema is complete and student can identify why/evidence/next (perception or compliance sample) | L1 | trust_inspectability | C7,C2 | C1–C2 |
| **OM-REC-03** | Acceptance rate | Accepts / (accepts + rejects + dismisses) among eligible shown; defer reported separately | L1 | organisation | C2 | C1 |
| **OM-REC-04** | Defer rate | Defers / eligible shown | L1 | organisation | C2 | C1 |
| **OM-REC-05** | Reject / dismiss rate | Explicit reject or dismiss / eligible shown | L1 | organisation | C2 | C1 |
| **OM-REC-06** | Time-to-start | Median time from accept to start of recommended activity | L1 | organisation | C2,C4 | C1 |
| **OM-REC-07** | Accept→complete rate | Completions of accepted recommended activity / accepts | L1 | organisation | C2,C4 | C1 |
| **OM-REC-08** | Accept→learning movement | Share of accepts followed by mastery/readiness/revision delta in window (definition versioned) | L1 | learning_signal | C2,C9 | C2 |
| **OM-REC-09** | Chronic dismiss-without-alternative | Students with high dismiss and no lawful alternative shown — failure signal | L1 | trust_inspectability | C2,C7 | C1 |
| **OM-REC-10** | Decision Journal completeness | Share of eligible decisions with recorded accept/defer/reject outcome | L1 | organisation | C2,C8 | C1 |

**Vision link:** Recommendation acceptance.  
**Product law:** K2 claims require Recommendation Review Pass (P-001.3).

---

## 5. Study consistency (`OM-CON`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-CON-01** | Study-day rate | Student-days with productive study evidence / planned study-days in window | L1 | organisation | C4,C1 | C1 |
| **OM-CON-02** | Consistency streak (contextual) | Consecutive planned study-days met — **supporting only**, never sole success | L1 | organisation | C4 | C0–C1 |
| **OM-CON-03** | Plan adherence | Executed plan slots / planned slots | L1 | organisation | C4 | C1 |
| **OM-CON-04** | Twin consistency facet distribution | Cohort distribution of Twin consistency facet (ops) | L1 | organisation | C1 | C1 |
| **OM-CON-05** | Post-recovery consistency | Study-day rate in 7 days after recovery recommendation accept | L1 | organisation | C4,C2 | C2 |

**Vision link:** Student consistency.  
**KSI:** Primarily K4.

---

## 6. Mission / Session completion quality (`OM-MSN`)

Domain: Mission; learner UI: Session (Product Language Guide).

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-MSN-01** | Mission completion rate | Completed Missions / assigned Missions in window | L1 | organisation | C4 | C1 |
| **OM-MSN-02** | Same-night completion | Missions completed within intended study night / started | L1 | organisation | C4 | C1 |
| **OM-MSN-03** | Abandon rate | Abandoned / started Missions | L1 | organisation | C4 | C1 |
| **OM-MSN-04** | Completion with practice evidence | Completions that include required practice/attempt evidence / completions | L1 | learning_signal | C4,C8 | C1 |
| **OM-MSN-05** | Workload sustainability flag rate | Sessions flagged as overloaded / total (advisory pacing signal) | L1 | organisation | C4 | C1 |
| **OM-MSN-06** | Mission quality score (design) | Composite: completion + practice evidence + sustainable load — versioned; not vanity length | L1 | learning_signal | C4,C9 | C2 |

**Vision link:** Mission / Session completion.  
**Rule:** Duration alone is not quality.

---

## 7. Learning outcome indicators (`OM-LRN`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-LRN-01** | Topic mastery delta | Evidence-backed mastery estimate change per topic in window | L1 | learning_signal | C1,C6 | C2 |
| **OM-LRN-02** | Weak-topic repair rate | Weak topics revisited with improved evidence / weak topics identified | L1 | learning_signal | C2,C5 | C2 |
| **OM-LRN-03** | Revision adherence | Completed revision / planned revision windows | L1 | organisation | C2,C6 | C1 |
| **OM-LRN-04** | Curriculum coverage progress | Syllabus topics with sufficient evidence / topics in scope (V1/V2 aware) | L1 | learning_signal | C6 | C1 |
| **OM-LRN-05** | Practice outcome logged rate | Sessions with honesty ritual / practice outcome logged / eligible Sessions | L1 | learning_signal | C8 | C1 |
| **OM-LRN-06** | Pre-registered learning-depth construct | Protocol-defined construct only | L5/L1 | learning_depth | C9,C10 | C3 |

---

## 8. Behavioural indicators (`OM-BHV`)

Supporting behavioural substrate — never sole educational success.

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-BHV-01** | Session start rate | Starts / eligible daily opportunities | L1 | organisation | C4 | C1 |
| **OM-BHV-02** | Resume-after-abandon rate | Resumes within recovery window / abandons | L1 | organisation | C4 | C1 |
| **OM-BHV-03** | Session duration (contextual) | Elapsed learning time — interpret only with educational context | L1 | organisation | C4 | C0 |
| **OM-BHV-04** | Attempt density | Attempts per Session (observational) | L1 | learning_signal | C8 | C1 |
| **OM-BHV-05** | Retention (product cycle) | Continued use through exam-cycle windows among eligible cohort | L1 | organisation | C9 | C2 |

---

## 9. Readiness prediction evaluation (`OM-RDY`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-RDY-01** | Band stability | Share of band changes that coincide with evidence warrant (vs unexplained churn) | L1 | learning_signal | C3 | C2 |
| **OM-RDY-02** | Overconfidence gap | Rate of high readiness display given weak evidence | L1 | trust_inspectability | C3,C7 | C1 |
| **OM-RDY-03** | Underrating gap | Rate of low readiness given strong evidence | L1 | learning_signal | C3 | C1 |
| **OM-RDY-04** | Short-horizon calibration | Readiness band vs subsequent attempt/success in window (reliability table) | L1 | learning_signal | C3 | C2–C3 |
| **OM-RDY-05** | Driver traceability rate | Share of readiness surfaces with expandable drivers from Twin/curriculum facts | L1 | trust_inspectability | C3,C7 | C1 |
| **OM-RDY-06** | Pre-exam readiness vs outcome | Consented linkage of pre-exam readiness to exam result | L4 | transfer | C3,C9 | C4 |

**Vision link:** Predicted readiness accuracy.  
**KSI:** K3; honesty before precision theatre.

---

## 10. Explainability effectiveness (`OM-EXP`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-EXP-01** | Schema compliance rate | Sampled intelligence speech meeting Mandatory Explanation Schema | L1/L2 | trust_inspectability | C7 | C1 |
| **OM-EXP-02** | Fact≠estimate≠advice separation rate | Sampled speech with lawful separation | L1/L2 | trust_inspectability | C7 | C1 |
| **OM-EXP-03** | Student-understood why rate | Perception: student can state why this recommendation | L1 | trust_inspectability | C7 | C2 |
| **OM-EXP-04** | Empty-evidence strong-language incidents | Ops count of strong language with empty/sparse evidence | L1 | trust_inspectability | C7,C3 | C1 |
| **OM-EXP-05** | Lawful refusal rate | Eligible sparse-evidence cases where system refuses fabricated certainty | L1 | trust_inspectability | C7,C2 | C1 |

**Product law:** K8 claims require Explainability Review Pass (P-001.2).

---

## 11. Reflection usefulness (`OM-REF`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-REF-01** | Reflection participation rate | Optional reflections completed / eligible Sessions (non-coercive) | L1 | organisation | C5 | C1 |
| **OM-REF-02** | Reflection→revision return | Weak-topic revision within window after reflection / reflections | L1 | learning_signal | C5 | C2 |
| **OM-REF-03** | Reflection content sensitivity incidents | Ops: unlawful persistence / coercion flags | L2/L3 | trust_inspectability | C5 | C1 |
| **OM-REF-04** | Perceived usefulness (structured) | Check-in item: reflection helped next study choice | L1 | organisation | C5 | C2 |

**Invariant:** Participation inflation via coercion is a quality failure, not a success.

---

## 12. Longitudinal student progress (`OM-LNG`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-LNG-01** | Multi-week mastery trajectory | Topic mastery vector change across ≥ N weeks | L1→L4 | learning_signal | C1,C9 | C2 |
| **OM-LNG-02** | Multi-week consistency trajectory | OM-CON-01 trend across weeks | L1 | organisation | C4,C9 | C2 |
| **OM-LNG-03** | Readiness trajectory honesty | Band path vs evidence density over time | L1 | learning_signal | C3,C9 | C2 |
| **OM-LNG-04** | Journey milestone progress | Structured journey milestones completed under Educational State | L1 | organisation | C6 | C1 |
| **OM-LNG-05** | Educational satisfaction trend | Structured educational satisfaction / trust check-ins over cycle | L1 | organisation | C9 | C2 |

---

## 13. Twin / analytics integrity (`OM-TWN`)

Operational Twin health — not north-star proof.

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-TWN-01** | Facet completeness distribution | Structural facet availability over cohort | L1/L3 | organisation | C1 | C1 |
| **OM-TWN-02** | Provenance coverage | % consumer fields with expandable provenance | L1 | trust_inspectability | C1,C7 | C1 |
| **OM-TWN-03** | Shadow agreement rate | Dual-run divergence rate when enabled — **L3 engineering** | L3 | organisation | C1 | C1 |
| **OM-TWN-04** | Unknown discipline rate | Lawful “unavailable” vs filled estimates (honesty) | L1 | trust_inspectability | C1,C3 | C1 |
| **OM-TWN-05** | One Educational Truth incidents | Ops: parallel scoring / dual analytics narrative detections | L3 | trust_inspectability | C8 | C1 |

---

## 14. Experimentation / trial signals (`OM-TRIAL`)

Aligned with P4-MS001 operational metrics — early chain only.

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-TRIAL-01** | Trial acceptance rate | `recommendation_acceptance` by cohort | L5 | organisation | C10,C2 | C3 |
| **OM-TRIAL-02** | Trial mission completion | `mission_completion` by cohort | L5 | organisation | C10,C4 | C3 |
| **OM-TRIAL-03** | Trial study session completion | `study_session_completion` by cohort | L5 | organisation | C10 | C3 |
| **OM-TRIAL-04** | Trial reflection completion | `reflection_completion` by cohort | L5 | organisation | C10,C5 | C3 |
| **OM-TRIAL-05** | Policy activation rate | `policy_activation` by cohort | L5 | organisation | C10 | C3 |
| **OM-TRIAL-06** | Trial lift (primary) | Pre-registered Δ between treatment and baseline on primary metric | L5 | per primary | C10 | C3 |

**Non-claim:** These do not alone prove mastery or exam success.

---

## 15. North-star transfer (`OM-NS`)

| ID | Name | Definition (design) | L | CB | SI | Conf |
|----|------|---------------------|---|----|----|------|
| **OM-NS-01** | Consistent-user pass rate | Pass rate among pre-defined consistent users (consented) | L4 | transfer | C9 | C4 |
| **OM-NS-02** | Comparative pass probability | Pass probability difference vs matched non-consistent / control protocol | L4 | transfer | C9 | C4 |
| **OM-NS-03** | Readiness–outcome concordance | OM-RDY-06 aggregate under protocol | L4 | transfer | C3,C9 | C4 |

**Rule:** Never claimable from Alpha vanity, page views, or unconsented inference.

---

## 16. SI capability success criteria (summary)

| SI capability | Must-move metrics (minimum set) |
|---------------|----------------------------------|
| SI-C1 Twin | OM-TWN-01…04; OM-TWN-03 labelled L3 |
| SI-C2 Recommendations | OM-REC-03,07,08,10; K2 review |
| SI-C3 Readiness | OM-RDY-01…05; honesty before OM-RDY-06 |
| SI-C4 Mission Intelligence | OM-MSN-01,04,06; OM-CON-01 |
| SI-C5 Reflection | OM-REF-01,02,04 (non-coercive) |
| SI-C6 Curriculum adaptation | OM-LRN-04; V1/V2 traversal preserved |
| SI-C7 Explainability | OM-EXP-01…05; K8 review |
| SI-C8 Learning analytics | OM-REC-10; OM-LRN-05; OM-TWN-05 |
| SI-C9 Outcome measurement | Catalogue adoption; evidence packs |
| SI-C10 Experimentation | OM-TRIAL-* under Experimentation Guide |

---

## 17. Versioning

- Catalogue version **1.0** with OM-001.  
- Additive metrics get new IDs.  
- Breaking definition changes → new ID or `metric_id@vN`.  
- Deprecations require successor ID and claim-language sunset note.

---

**End of OM001_METRIC_CATALOGUE**
