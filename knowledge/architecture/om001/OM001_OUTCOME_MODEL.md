# OM-001 — Educational Outcome Model

**Programme:** OM-001 — Outcomes Measurement  
**Version:** 1.0  
**Status:** Active — permanent educational outcome model (design only)  
**Effective:** 2026-07-28  
**Change class:** Architecture & Educational Research  
**Constraint:** No application behaviour, schema, algorithms, UI, or release artefacts modified by this programme.

---

## 1. Purpose

Define the permanent conceptual model of **educational outcomes** for Kwalitec: what “success” means, how outcome types nest, and how Student Intelligence claims map to measurable educational evidence.

This model defines **educational evidence**, not educational interventions. It does not implement collectors, dashboards, trials, or product changes.

OM-001 generalises and hardens the SI-001 Outcome Measurement Framework (`SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md`) into product-wide outcome law for all Student Intelligence capabilities and future educational claims.

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| Vision 2030 | North star = materially higher exam pass probability for consistent users; learning ≠ activity; success metrics table |
| DG-001 / Educational Governance Constitution | Lawful educational meaning; independent educational assessment |
| OA-001 Product Constitution | PC-02 layer separation; PC-03–PC-04 claims ≤ evidence; PC-12 STOP on thin evidence |
| SI-001 | Student Intelligence capability map (SI-C1…C10); measurement layers L1–L5; OM-H0…H4 horizons |
| P-001.1 Product Success Framework | KSI as operational usefulness index — not the north star |
| P-001.2 / P-001.3 | Explainability and recommendation quality as measurement law for intelligence surfaces |
| Student Digital Twin Constitution | Understanding ≠ certainty; Twin interpretations are not facts |
| Educational Trial Architecture (P4-MS001) | Controlled operational trial signals; flag OFF by default |
| Evidence Model / Outcome Analytics (MS-006) | Claim boundaries (`organisation` … `transfer`) |
| Product Analytics Architecture | Learning over activity; one Educational Truth |

**Conflict rule:** Vision 2030 wins on north-star meaning. Educational Constitution / DG-001 win on educational meaning. Product Constitution wins on claim discipline. OM-001 does not amend those authorities; it specialises how outcomes are modelled and evidenced.

---

## 3. North star and operational expression

| Concept | Definition | Role in OM-001 |
|---------|------------|----------------|
| **North star** | Students who consistently use Kwalitec should have a materially higher probability of passing their examinations than students who do not | Ultimate L4 outcome; never claimable from activity vanity or Alpha anecdote |
| **Design question** | What is the highest-value thing this student should do next? | Daily operational expression of the north star — not a second north star |
| **KSI** | Weighted operational educational-usefulness index (K1–K8) | L1 instrument supporting progress toward the north star; estimated ΔKSI ≠ Gate G1 |

**Invariant:** Improving KSI without improving learning movement or (eventually) pass probability is incomplete success. Declaring north-star success from KSI alone is a constitutional claim violation (PC-03).

---

## 4. Measurement layers (normative separation)

Inherited from SI-001 and Product Constitution PC-02. Mixing layers in one unchecked narrative is forbidden.

| Layer | Question | Primary instruments | Owner board |
|-------|----------|---------------------|-------------|
| **L1 Operational usefulness** | Is guidance educationally useful day-to-day? | KSI (K1–K8), Decision Journal, completion, consistency | Product Success |
| **L2 Educational release quality** | May we release this intelligence to students? | EVF gates, Explainability / Recommendation checklists | Educational governance / EVF |
| **L3 Engineering operability** | Is the system safe for the claimed class? | P-002.1 G7–G12, ER programmes | Engineering |
| **L4 North-star outcomes** | Do consistent users pass at higher rates? | Longitudinal outcome studies (research) | Research + Product (ethics/privacy) |
| **L5 Experimentation signals** | Did a controlled change improve educational metrics? | Educational trial / pre-registered experiments | Research under OA-001 lifecycle |

```
L4 North-star (exam pass probability)
        ↑ informed by, never replaced by
L5 Experimentation (causal lift on pre-registered metrics)
        ↑ informed by
L1 Operational usefulness (KSI, behaviour, learning signals)
        ↔ gated by
L2 Educational release quality    L3 Engineering operability
```

---

## 5. Outcome taxonomy

Every measurable educational outcome belongs to exactly one primary class. Secondary tags (claim boundary, SI capability) are allowed; dual primary classes are not.

### 5.1 Learning outcomes

Outcomes that describe **change in knowledge, skill, or readiness** backed by educational evidence — not mere presence in the product.

| Outcome family | Meaning | Typical claim boundary |
|----------------|---------|------------------------|
| Mastery movement | Evidence-backed change in topic/skill mastery estimates | `learning_signal` → `learning_depth` (pre-registered) |
| Readiness movement | Change in readiness band/drivers with evidence warrant | `learning_signal` |
| Coverage / curriculum progress | Syllabus topic progress under curriculum truth | `organisation` + `learning_signal` |
| Revision effectiveness | Planned revision completed and linked to weak-area repair | `learning_signal` |
| Mistake-aware repair | Return to weak topics after failure / reflection | `learning_depth` (when pre-registered) |

**Non-outcomes alone:** finishing a Session without practice evidence; watching UI chrome; streak length.

### 5.2 Behavioural outcomes

Outcomes that describe **study behaviour** that is necessary but not sufficient for learning success.

| Outcome family | Meaning | Typical claim boundary |
|----------------|---------|------------------------|
| Study consistency | Productive study across planned days/windows | `organisation` |
| Mission / Session completion | Authoritative study commitment completed vs assigned | `organisation` |
| Plan adherence | Planned vs executed study slots | `organisation` |
| Time-on-task (contextual) | Session duration with educational context | `organisation` (supporting only) |
| Recovery behaviour | Resume after abandon / recovery tip follow-through | `organisation` |

### 5.3 Guidance outcomes

Outcomes that describe whether Student Intelligence **guidance** is understood, accepted, and acted on.

| Outcome family | Meaning | Typical claim boundary |
|----------------|---------|------------------------|
| Recommendation acceptance | Accept / start / defer / reject of next-action guidance | `organisation` / trust |
| Recommendation follow-through | Accepted → started → completed chain | `organisation` + `learning_signal` |
| Explainability effectiveness | Student can state why / what evidence / what next | `trust_inspectability` |
| Reflection usefulness | Optional reflection improves subsequent study choices | `learning_signal` (careful) |
| Lawful refusal quality | System refuses fabricated certainty when evidence sparse | `trust_inspectability` |

### 5.4 Predictive outcomes

Outcomes that evaluate whether **predictions and models** are honest and calibrated.

| Outcome family | Meaning | Typical claim boundary |
|----------------|---------|------------------------|
| Readiness prediction accuracy | Calibration of readiness vs later performance / outcomes | `learning_signal` → L4 research |
| Twin predictive usefulness | Facets forecast useful interventions without inventing certainty | Research / ops |
| Workload sustainability prediction | Soft-cap / recovery advice vs burnout / consistency | `organisation` |

### 5.5 Longitudinal outcomes

Outcomes that require **time and consent** beyond a single Session or Alpha window.

| Outcome family | Meaning | Typical claim boundary |
|----------------|---------|------------------------|
| Trajectory stability | Multi-week mastery / readiness / consistency trajectories | Research |
| Exam pass probability (north star) | Consented comparative pass rates for consistent users | `transfer` / L4 |
| Retention through exam cycle | Continued lawful use across the study cycle | `organisation` |
| Educational satisfaction / trust | Structured check-ins; not NPS theatre alone | Qualitative + L1 |

---

## 6. Student Intelligence capability → outcome map

Every SI capability must have measurable success criteria. Detail IDs live in `OM001_METRIC_CATALOGUE.md` and claim packs in `OM001_EVIDENCE_REQUIREMENTS.md`.

| SI capability | Primary outcome families | Success (design) |
|---------------|--------------------------|------------------|
| **SI-C1** Digital Twin | Twin health; predictive usefulness; honest incompleteness | Completeness + provenance + unknown discipline; no certainty theatre |
| **SI-C2** Recommendation Engine | Guidance chain; learning movement after accept | Shown→Understood→Accepted→Started→Completed→Learning movement |
| **SI-C3** Study Readiness | Predictive calibration; honesty gaps | Calibrated bands; over/underrating gaps shrink without fabricating evidence |
| **SI-C4** Mission Intelligence | Completion quality; consistency; workload sustainability | Higher completion with sustainable load; not longer Sessions alone |
| **SI-C5** Reflection Intelligence | Reflection usefulness; mistake-aware repair | Optional participation linked to revision return; non-coercive |
| **SI-C6** Curriculum adaptation | Coverage progress; syllabus-faithful pacing | Progress under curriculum truth; V1/V2 traversable |
| **SI-C7** Explainability | Explainability effectiveness | Schema compliance + student-understood why/evidence/next |
| **SI-C8** Learning analytics | Metric integrity; one Educational Truth | Reproducible aggregates; no parallel scoring brain |
| **SI-C9** Outcome measurement | This model’s adherence | Claims cite layers, claim boundaries, evidence packs |
| **SI-C10** Educational experimentation | L5 lift with ethics | Pre-registered; research≠production; Independent Review |

---

## 7. Vision success metrics → outcome families

| Vision 2030 success metric | Outcome family | Layer |
|----------------------------|----------------|-------|
| Student consistency | Study consistency | L1 |
| Mission / Session completion | Mission completion quality | L1 |
| Revision adherence | Revision effectiveness | L1 |
| Recommendation acceptance | Guidance outcomes | L1 |
| Retention | Longitudinal retention | L1 → L4 context |
| Educational satisfaction | Trust / satisfaction | L1 |
| Predicted readiness accuracy | Predictive outcomes | L1 → L4 |
| Exam pass rate | North-star longitudinal | L4 |

---

## 8. Causal chain (normative narrative)

Educational success is evaluated along this chain. Skipping stages while claiming later-stage success is forbidden.

```
Eligible guidance shown
        ↓
Understood (explainability)
        ↓
Accepted / deferred / refused (agency)
        ↓
Started (friction check)
        ↓
Completed (Mission / Session / task quality)
        ↓
Behavioural consistency (sustained study)
        ↓
Learning movement (mastery / readiness / revision repair)
        ↓
Calibrated prediction (readiness honesty)
        ↓
Longitudinal progress
        ↓
North-star exam outcome (consented research)
```

Operational trial metrics (P4-MS001) may measure early chain stages. They must not be narrated as mastery or exam success.

---

## 9. Relationship to existing artefacts

| Artefact | Relationship to OM-001 Outcome Model |
|----------|--------------------------------------|
| SI001 Outcome Measurement Framework | Seed; OM-001 is permanent product-wide outcome law |
| Product Analytics Architecture | Metric source principles; OM owns educational success semantics |
| Advisory Outcome Measurement (P3-MS002) | Operational rollout behaviour only — not learning depth |
| Educational Trial Architecture (P4-MS001) | L5 operational signal instrument — locked advisory field |
| Evidence Model claim boundaries | Binding tags on every metric and evidence pack |
| KSI / P-001.1 | L1 usefulness index; subordinate to north star |
| EVF Educational Release Gate | L2 — release-to-students quality, not outcome proof |

---

## 10. Explicit non-goals

- Implementing analytics pipelines, warehouses, or student dashboards  
- Enabling educational trials or expanding advisory fields  
- Recomputing validated KSI or clearing Gate G1  
- Declaring north-star exam outcome proof  
- Changing recommendation ranking, Twin authority, or UI  
- Treating engagement vanity as educational success  

---

## 11. Traceability

| Authority | Model element |
|-----------|---------------|
| Vision north star | §3, §5.5, causal chain end |
| Vision success metrics | §7 |
| PC-02 / PC-03 / PC-04 | Layers §4; claim honesty throughout |
| Twin Constitution | Predictive outcomes; understanding ≠ certainty |
| SI-C1…C10 | Capability map §6 |
| MS-006 claim boundaries | Taxonomy tags §5 |

---

**End of OM001_OUTCOME_MODEL**
