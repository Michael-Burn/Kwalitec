# SI-001 — Student Intelligence Architecture

**Programme:** SI-001 — Student Intelligence  
**Version:** 1.0  
**Status:** Active — long-term architectural direction (design only)  
**Effective:** 2026-07-28  
**Change class:** Architecture & Product Design  
**Constraint:** No application behaviour, schema, algorithms, UI, or release artefacts modified by this programme.

---

## 1. Purpose

Define the next-generation **Student Intelligence** architecture that builds on certified governance (DG-001), runtime convergence (RR-002), engineering Conditional GO (ER-002), and operational law (OA-001).

Student Intelligence is the durable capability stack that answers Vision 2030’s four daily questions:

1. What to study  
2. Why it matters  
3. Whether the student understands it  
4. What they should do next  

This document is the **system architecture roadmap**. Companions cover twin evolution, recommendation evolution, outcome measurement, and research backlog.

---

## 2. Authority and non-contradiction

| Authority | Role for SI-001 |
|-----------|-----------------|
| **Vision 2030** | Philosophy apex — north star, Final Test, never-build, AI philosophy |
| **Product Constitution (OA-001)** | Operating principles PC-01…PC-12 — evidence, ADR-before-implementation, deterministic cores, student agency |
| **Product Blueprint** | Strategy — educational model pillars, Digital Twin role, Version 1 / later epic framing |
| **Educational Constitution / DG-001** | Educational meaning and governance procedure |
| **Digital Twin Constitution** | Twin educational charter — understanding ≠ certainty |
| **EP-002.9 Authoritative Architecture Baseline** | Binding Runtime A student-intelligence surface ownership |
| **P-001.2 / P-001.3** | Explainability and recommendation quality product law |
| **RR-002** | Sole-runtime Education OS presentation path; legacy Contained |
| **ER-002** | Engineering claim-class bounds (invite-only Conditional GO; flag honesty) |
| **OA-001** | Feature lifecycle, ADR standard, claim honesty |

**Conflict rule:** Vision 2030 and Educational Constitution win on philosophy and educational meaning. Architecture Constitution and Twin Constitution win on structural/educational Twin law. OA-001 Product Constitution wins on *how* programmes operate. SI-001 proposes direction; it does not amend those authorities.

---

## 3. Current baseline (as of SI-001)

### 3.1 Constitutional consumer chain (EP-001 → EP-002)

```
Curriculum Engine (syllabus truth)
        ↓
Runtime A writes / facts          ← sole educational write authority
        ↓
MS-004 collectors → TwinRuntimeEvidence
        ↓
EP-001.1 Foundation (CanonicalLearnerState)  ← learner-state read model
        ↓
   ┌────┴────┬────────────┐
   ↓         ↓            ↓
Planner   Readiness    (inputs)
   ↓         ↓
   └────┬────┘
        ↓
     Insight / Recommendation     ← communication only
        ↓
Consumer Chain (observe / dual-run / cutover)
        ↓
Runtime A presentation (sole-runtime Education OS)
```

**Production defaults (ER-002 / G12 honesty):** Twin / Authority / Cutover remain **OFF** unless lawfully enabled. SI-001 must not invent marketing that they are live.

### 3.2 What is already designed or implemented (reference, not cutover claim)

| Capability | Status posture | Primary authority |
|------------|----------------|-------------------|
| Twin contracts / facets / snapshot / explainability / adaptive attach / shadow | Implemented under flags; Twin Ready (T7) not declared by EP-002 | MS-004 · EP-001.1 |
| Adaptive planner / readiness / insight consumers | Implemented under Twin-gated chain | EP-001.2–4 |
| Student intelligence surface activation path | Certified controlled-pilot architecture; defaults OFF | EP-002.9 |
| Recommendation / explainability product law | Active standards | P-001.2 · P-001.3 |
| Educational trial framework (narrow advisory field) | Implemented; flag OFF | P4-MS001 |
| Product analytics architecture | Design only | Product Analytics Architecture |
| Guided reflection experience | Experience-layer implemented; evidence-platform integration deferred | Unified Journey / P2-MS005 |

SI-001 **evolves** this stack; it does not redefine ownership or reopen Contained dual-authority without ADR.

---

## 4. Student Intelligence capability map

Ten capability domains form the long-term architecture. Each traces to Vision 2030 and Product Constitution.

| ID | Capability | Vision 2030 link | Product Constitution link | Companion |
|----|------------|------------------|---------------------------|-----------|
| **SI-C1** | Student Digital Twin evolution | One Educational State; evidence before opinion | PC-09 deterministic cores; PC-10 curriculum truth | `SI001_DIGITAL_TWIN_EVOLUTION.md` |
| **SI-C2** | Recommendation Engine evolution | Highest-value next action; AI philosophy | PC-01 trust; PC-09; PC-11 agency | `SI001_RECOMMENDATION_ENGINE_ROADMAP.md` |
| **SI-C3** | Study Readiness modelling | “Whether they understand it”; readiness accuracy metric | PC-03 claim honesty; PC-09 | This architecture §6.3 |
| **SI-C4** | Mission Intelligence | Consistency; Mission/Session completion | PC-10 sole-runtime path | This architecture §6.4 |
| **SI-C5** | Reflection Intelligence | Reflect regularly; understand mistakes | PC-11 agency (optional, non-coercive) | This architecture §6.5 |
| **SI-C6** | Curriculum adaptation | Curriculum-first syllabus truth | PC-10 curriculum precedes UI | This architecture §6.6 |
| **SI-C7** | Explainability | Transparent, evidence-based recommendations | PC-01; P-001.2 law | This architecture §6.7 |
| **SI-C8** | Learning analytics | Learning over activity; auditable metrics | PC-03–PC-04 evidence-bound claims | `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md` |
| **SI-C9** | Outcome measurement | North star (pass probability); KSI operational index | PC-02 independent boards; PC-04 | `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md` |
| **SI-C10** | Educational experimentation | Evidence before opinion; measurable benefit | PC-07 Blueprint→Impl→Review; PC-12 STOP | `SI001_RESEARCH_BACKLOG.md` |

---

## 5. Multi-release roadmap (architecture horizons)

Horizons are **architectural releases**, not product marketing versions. Each may map to multiple OA-001 Feature Lifecycle programmes. Implementation requires ADR (PC-06) and Independent Review (PC-07).

| Horizon | Intent | Dominant capabilities | Claim-class gate |
|---------|--------|----------------------|------------------|
| **SI-H0** | Freeze direction (this programme) | All — design only | Docs-only; ΔKSI = 0 |
| **SI-H1** | Trustworthy intelligence under invite-only Alpha | SI-C2, SI-C7, SI-C3 (honesty), SI-C8 (instrumentation design→lawful ops) | Obey ER-002 C1–C7; G12 flag honesty |
| **SI-H2** | Twin-first authority readiness | SI-C1 persistence/authority, SI-C4 Mission Intelligence, SI-C6 pacing adaptation | Twin Ready / Authority cutover only after ADR + EVF + engineering gates |
| **SI-H3** | Closed learning loops | SI-C5 Reflection→Evidence, SI-C9 outcome calibration, SI-C10 controlled experiments | Educational release quality (EVF); no north-star overclaim |
| **SI-H4** | Longitudinal professional OS | SI-C1 longitudinal twin, multi-exam trajectories, SI-C9 pass-probability research | Vision 2030 long-term; institutional Epic 4 only when lawful |

```
SI-H0 (now)     SI-H1              SI-H2                 SI-H3                SI-H4
Design freeze → Trust & quality → Twin-first readiness → Closed loops → Longitudinal OS
                recommendations     Mission intel          Reflection→         Multi-exam /
                explainability      Curriculum adapt       Evidence            outcome research
                readiness honesty   Authority path         Experiments
```

**Ordering invariant:** Recommendation quality and explainability (H1) precede Twin-first authority marketing (H2). Outcome measurement design (H0/H1) precedes experimental expansion (H3). Longitudinal modelling (H4) never bypasses curriculum truth or deterministic cores.

---

## 6. Capability architectures (target state)

### 6.1 Student Digital Twin evolution (SI-C1)

**Target:** The Twin remains the sole learner-state *understanding* model for educational consumers — provisional, evidence-bound, explainable — evolving toward lawful persistence, longitudinal trajectory, and authority cutover without inventing certainty.

**Non-goals:** Twin does not teach, store curriculum PDFs, execute sessions, or become an opaque AI oracle.

Detail: `SI001_DIGITAL_TWIN_EVOLUTION.md`.

### 6.2 Recommendation Engine evolution (SI-C2)

**Target:** One Decision / Recommendation path that maximises expected educational value under scarce time, ranked by P-001.3 Decision Framework, explained by P-001.2 schema, reproducible (PC-09), advisory (PC-11).

**Non-goals:** No LLM authority in the core path; no tip theatre; no conflict with authorised Learning Mode / Today’s Session.

Detail: `SI001_RECOMMENDATION_ENGINE_ROADMAP.md`.

### 6.3 Study Readiness modelling (SI-C3)

**Ownership (preserved):** ReadinessService owns evaluation; Twin owns learner state; Planner owns planning; Insight owns communication (EP-001.3–4).

**Evolution axes (design):**

| Axis | Direction | Vision / PC |
|------|-----------|-------------|
| Honesty | Sparse evidence → humble bands / refusal; never fabricated pass certainty | Vision AI philosophy; PC-03 |
| Calibration | Predicted readiness vs later outcomes (design metrics in Outcome Framework) | Vision success metrics |
| Drivers | Traceable drivers from Twin facets + curriculum coverage + pace | Explainability Standard |
| Separation | Readiness ≠ recommendation ≠ marketing “Exam Ready guarantee” | Blueprint V1 limits |

**Horizon placement:** H1 honesty + instrumentation; H2 Twin-enriched readiness under authority gates; H3 calibration loops.

### 6.4 Mission Intelligence (SI-C4)

**Meaning:** Intelligence that improves the *authoritative study commitment* (domain Mission; UI Session) — composition, workload balance, recovery, and completion likelihood — without relocating educational writes outside Runtime A.

**Evolution axes (design):**

| Axis | Direction |
|------|-----------|
| Composition | Planner consumes Twin Foundation for slot/topic/workload (already EP-001.2); deepen under quality law |
| Continuity | Mission outcomes feed Evidence → Twin → next plan (closed loop) |
| Burnout / sustainability | Workload signals remain advisory pacing aids (Vision sustainable progress) |
| Quarantine respect | `MissionOptimizer.generate_balanced_mission` remains quarantined until ADR lifts EP-002.2 decision |

**Horizon placement:** H1 quality of guidance about today’s Session; H2 Mission Intelligence as Twin-first planning consumer; H3 outcome-linked mission effectiveness.

### 6.5 Reflection Intelligence (SI-C5)

**Current:** Guided Reflection is Experience-layer, lightweight, optional; responses not a second educational brain.

**Target evolution:**

```
SessionOutcome → ReflectionExperience (presentation)
        ↓ (lawful, consented, optional)
Evidence events (typed reflection evidence)
        ↓
Twin / Educational State update (provisional understanding only)
        ↓
Explainable effect on next recommendation (never coercive scoring)
```

**Invariants:** Reflection must not coerce (PC-11); must not invent mastery from feelings alone; must pass Educational Explainability speech rules (facts ≠ estimates ≠ advice).

**Horizon placement:** H3 primary; H1 may improve presentation honesty only without Twin write expansion unless ADR.

### 6.6 Curriculum adaptation (SI-C6)

**Meaning:** Adaptation of *pacing, emphasis, revision timing, and topic order within lawful syllabus structure* — not rewriting official curriculum.

| Allowed (design) | Forbidden |
|------------------|-----------|
| Reorder within CurriculumService helpers | Invent parallel syllabus truth |
| Emphasise weak topics / overdue revision | Skip mandatory curriculum gates without policy |
| V1 flat + V2 hierarchical both traversable | Features that break V1 flat curricula |
| Exam-date driven replan | Opaque personalisation that ignores syllabus weight |

**Horizon placement:** H2 with Twin-first planner maturity; always through CurriculumService.

### 6.7 Explainability (SI-C7)

**Law:** P-001.2 mandatory schema + EIP-003 educational speech + Twin explainability contracts.

**Evolution:** Every new intelligence surface declares explanation level before ship; unavailable evidence uses sparse-evidence patterns; K8 movement only with checklist Pass.

**Horizon placement:** Continuous from H1; blocking for any student-facing intelligence programme.

### 6.8 Learning analytics (SI-C8)

**Law:** Product Analytics Architecture — learning over activity; one educational truth; privacy.

**Evolution:** Operationalise metric catalogue against Twin / Evidence / Decision Journal authorities; no parallel scoring brain in templates.

Detail: Outcome Measurement Framework § analytics layer.

### 6.9 Outcome measurement (SI-C9)

**Layers:** Operational usefulness (KSI) → educational release quality (EVF) → north-star research (pass probability). Never conflate layers (PC-02).

Detail: `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md`.

### 6.10 Educational experimentation (SI-C10)

**Foundation:** P4 educational trial architecture (narrow, flag OFF).

**Evolution:** Expand only with measurable educational benefit, locked advisory fields, deterministic cohorts, Independent Review, and STOP when evidence thin (PC-12).

Detail: `SI001_RESEARCH_BACKLOG.md`.

---

## 7. Layering (normative for future implementation)

SI-001 preserves existing layering; future SI programmes must not invent god routes or bypass services.

```
Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON
                     ↑
         Student Intelligence consumers
         (Planner / Readiness / Insight / Analytics read models)
                     ↑
         Twin Foundation (learner-state understanding)
                     ↑
         Runtime A evidence / writes
```

| Layer | May | Must not |
|-------|-----|----------|
| Presentation | Project explainable guidance | Own mastery math or dual educational truth |
| Blueprints | HTTP, authz, forms | Planning / recommendation algorithms |
| Services | Deterministic educational logic | Depend on `flask.request` globals |
| Twin | Interpret evidence → understanding | Teach, execute missions, invent certainty |
| Curriculum Engine | Syllabus order / structure | Student behavioural state |

---

## 8. Cross-cutting invariants

1. **Deterministic cores** — same inputs → same plans, readiness, recommendations (PC-09).  
2. **No opaque LLM authority** in core learning path (Vision AI philosophy; engineering rules).  
3. **One Educational State** — no parallel educational truths for the same student moment.  
4. **One Runtime presentation** — sole-runtime Education OS; legacy Contained until lawfully retired (RR-002).  
5. **Advice remains advisory** — student agency preserved (PC-11).  
6. **Claims ≤ evidence** — flag-OFF capabilities not marketed live (PC-03; ER-002 C7).  
7. **Curriculum V1 and V2** both remain loadable and traversable.  
8. **ADR before structural change** (PC-06); Blueprint → Implementation → Independent Review (PC-07).

---

## 9. Explicit non-goals (SI-001)

- Implementation of any SI-H1…H4 capability  
- Twin Ready (T7) declaration  
- Educational G1 clearance or Version 1 production-ready declaration  
- Amendment of Vision 2030, Educational Constitution, or release artefacts  
- Black-box generative tutoring as educational authority  
- Activity-vanity success metrics  

---

## 10. Traceability summary

| Vision 2030 element | SI capabilities |
|---------------------|-----------------|
| Four daily questions | SI-C1…C7 |
| North star (pass probability) | SI-C9, SI-C10 |
| AI philosophy (explainable) | SI-C2, SI-C7 |
| Educational principles (consistency, feedback, reflection, revision, confidence) | SI-C4, SI-C5, SI-C6, SI-C3 |
| Design principles (what now / progress / blockers / next) | SI-C2, SI-C8 |
| Never-build (opaque AI, unhealthy habits, activity metrics) | Constraints on all |
| Final Test | Gate on every future SI programme |

| Product Constitution | SI enforcement |
|----------------------|----------------|
| PC-01…PC-04 | Trust, independent boards, claim honesty, evidence |
| PC-06…PC-08 | ADR, lifecycle, debt ownership for SI programmes |
| PC-09…PC-12 | Determinism, curriculum truth, agency, STOP |

---

## 11. Related artefacts

| Artefact | Path |
|----------|------|
| Recommendation Engine Roadmap | `SI001_RECOMMENDATION_ENGINE_ROADMAP.md` |
| Digital Twin Evolution | `SI001_DIGITAL_TWIN_EVOLUTION.md` |
| Outcome Measurement Framework | `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md` |
| Research Backlog | `SI001_RESEARCH_BACKLOG.md` |
| Completion Report | `SI001_COMPLETION_REPORT.md` |
| EP-002.9 Baseline | `knowledge/architecture/ep002_9_programme_exit_certification/AUTHORITATIVE_ARCHITECTURE_BASELINE.md` |
| Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Product Constitution | `knowledge/operations/oa001/PRODUCT_CONSTITUTION.md` |
| Product Blueprint | `PRODUCT_BLUEPRINT.md` |

---

**End of SI001_STUDENT_INTELLIGENCE_ARCHITECTURE**
