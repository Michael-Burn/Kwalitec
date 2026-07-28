# SI-001 — Recommendation Engine Roadmap

**Programme:** SI-001 — Student Intelligence  
**Version:** 1.0  
**Status:** Active — architectural roadmap (design only)  
**Effective:** 2026-07-28  
**Companion to:** `SI001_STUDENT_INTELLIGENCE_ARCHITECTURE.md`  
**Constraint:** No recommendation algorithms, UI, or APIs modified by this programme.

---

## 1. Purpose

Define the multi-release evolution of Kwalitec’s **Recommendation Engine** so that student-facing guidance becomes more educationally useful, trustworthy, and measurable — without inventing a second educational brain or opaque AI authority.

The engine’s permanent job is Vision 2030’s daily design question:

> What is the highest-value thing this student should do next?

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| Vision 2030 | Explainable, evidence-based, educationally defensible recommendations; never-build opaque AI |
| Product Constitution PC-01, PC-09, PC-11 | Trust > feature count; deterministic cores; advice advisory |
| Product Blueprint | Decision framework maximises expected educational value |
| P-001.3 Recommendation Quality Standard | What to recommend / how to prioritise; K2 law |
| P-001.2 Explainability Standard | Mandatory explanation schema; K8 law |
| EP-001.4 / EP-002.9 | Insight owns communication; Twin owns state; Planner owns planning; Readiness owns evaluation |
| Educational Constitution / EIP-003 | Lawful speech (facts ≠ estimates ≠ advice) |

---

## 3. Current architecture (baseline)

```
Foundation (learner state)
   + Planner (daily plan)
   + Readiness (evaluation)
        ↓
Insight / RecommendationService consumers
        ↓
Consumer Chain gates (observe / dual-run / cutover)
        ↓
Sole-runtime presentation (Education OS)
```

| Path | Role | Caveat |
|------|------|--------|
| EP-001.4 `build_study_insights` | Constitutional insight consumer | Twin-gated; production defaults OFF |
| Legacy `generate_recommendations` | Fail-open Runtime A path | Remains until lawful cutover |
| Decision Journal | Accept / dismiss audit trail | Substrate for quality measurement |
| P4 Educational Trial | Policy-weighted vs baseline (narrow field) | Flag OFF; advisory field locked |

**Quarantine:** Do not rewire `MissionOptimizer.generate_balanced_mission` to production without ADR (EP-002.2).

---

## 4. Target architecture (end-state sketch)

```
Curriculum weights + Twin understanding + Evidence + Time/Deadline
                        ↓
              Decision Engine (deterministic)
                        ↓
         Ranked Recommendation Candidates
                        ↓
         P-001.3 Decision Framework filter
                        ↓
         P-001.2 Explanation assembly
                        ↓
         Single primary recommendation (+ bounded alternatives)
                        ↓
         Student agency (accept / defer / reject) → Decision Journal
                        ↓
         Outcome signals → analytics / trials (not silent self-mutation)
```

**Ownership remains separated:** Decision/Insight communicate; they do not rewrite Twin or curriculum.

---

## 5. Quality contract (permanent)

Every recommendation programme must satisfy:

| Gate | Standard | Fail mode |
|------|----------|-----------|
| Right next action | P-001.3 Decision Framework | Do not ship |
| Explainability | P-001.2 Mandatory Schema at declared level | Do not show |
| Determinism | Same inputs → same output (PC-09) | Defect |
| Honesty | Thin evidence → humble / refuse (PC-03) | Defect |
| Agency | Advisory only (PC-11) | Defect |
| Non-conflict | Align with authorised plan / Learning Mode | Defect |
| Curriculum lawfulness | Via CurriculumService helpers | Defect |

---

## 6. Multi-release roadmap

### RE-H1 — Trust & usefulness (aligns SI-H1)

**Intent:** Raise educational usefulness of guidance already lawfully authorised under invite-only claim class.

| Workstream (design) | Outcome | Vision / PC / KSI |
|---------------------|---------|-------------------|
| Primary-recommendation consolidation | One clear “do next”; bounded secondary tips | Design principles; K2 |
| Confidence / sparse-evidence speech | Humble bands; lawful refusal patterns | AI philosophy; K8 |
| Conflict resolution with Today’s Session | Recommendations reinforce authorised plan | PC-10; K2 |
| Decision Journal completeness | Accept/defer/reject capture for measurement | PC-04; Outcome Framework |
| Recommendation Review Checklist as exit gate | Every SI recommendation programme | PC-07 |

**Not in RE-H1:** Twin-first sole path marketing; LLM ranking; autonomous policy updates.

### RE-H2 — Twin-enriched decisioning (aligns SI-H2)

**Intent:** Deepen Decision Engine inputs from Twin Foundation under Authority / Cutover ADRs.

| Workstream (design) | Outcome |
|---------------------|---------|
| Facet-aware ranking | Rhythm, consistency, revision behaviour, cognitive load as *evidence-bound* inputs |
| Readiness-coupled next actions | Drivers → proportionate actions (not score theatre) |
| Workload sustainability | Burnout/pacing signals as soft constraints |
| Dual-run → cutover readiness | Consumer Chain gates; fail-open until certified |
| Quarantine disposition | ADR for MissionOptimizer or permanent deprecation |

**Gate:** Twin Ready / Authority claims only with EVF + engineering + G12 honesty.

### RE-H3 — Closed-loop effectiveness (aligns SI-H3)

**Intent:** Measure whether accepted recommendations improve learning outcomes; run controlled experiments.

| Workstream (design) | Outcome |
|---------------------|---------|
| Effectiveness metrics | Acceptance → completion → mastery/readiness movement | 
| Controlled policy trials | Expand P4 trial framework under locked fields + Independent Review |
| Recovery / revision recommendation classes | Typed recommendation families with shared quality law |
| Reflection-informed candidates | Optional reflection evidence as weak prior — never sole mastery proof |

**Gate:** Claims of “effectiveness” require Outcome Measurement Framework evidence packs — not anecdote.

### RE-H4 — Longitudinal recommendation (aligns SI-H4)

**Intent:** Multi-week / multi-exam trajectory recommendations still daily-operationalised as next action.

| Workstream (design) | Outcome |
|---------------------|---------|
| Horizon-aware planning tips | Near-term next action consistent with long-term trajectory |
| Cross-syllabus caution | Multi-qualification support without parallel educational truths |
| Institutional advisory modes | Secondary audiences (Blueprint) without diluting student agency |

---

## 7. Recommendation families (catalogue)

| Family | Educational purpose | Primary evidence | Horizon |
|--------|---------------------|------------------|---------|
| **Today’s focus** | Highest-value Session action | Plan + Twin + readiness | H1 |
| **Weak-topic repair** | Close knowledge gaps | Mastery / attempts | H1–H2 |
| **Revision timing** | Intelligent spaced revision | Retention / revision behaviour | H2 |
| **Workload recovery** | Sustainable intensity | Cognitive load / consistency | H2 |
| **Readiness honesty** | Correct false confidence / despair | Readiness drivers + sparse evidence | H1 |
| **Reflection prompt** | Understand mistakes (optional) | SessionOutcome | H3 |
| **Trajectory nudge** | Long-horizon coherence | Longitudinal Twin | H4 |

Each family must declare: evidence requirements, explanation pattern, refusal conditions, and KSI categories affected (typically K2, K8; sometimes K3 readiness, K4 consistency).

---

## 8. Anti-patterns (never-build for recommendations)

Aligned with Vision never-build and P-001.3:

- Opaque model scores without educational narrative  
- Tip volume as engagement theatre  
- Gamified pressure that encourages unhealthy study  
- Recommendations that invent mastery or pass guarantees  
- Silent conflict with Today’s Session / Learning Mode  
- LLM-generated advice as core educational authority  
- Self-mutating policies without trial + review  

---

## 9. Measurement (design pointers)

Detail in `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md`. Recommendation-specific KPIs:

| KPI | Use |
|-----|-----|
| Acceptance / defer / reject rates | Trust substrate |
| Completion of accepted actions | Usefulness substrate |
| Explainability compliance rate | K8 process metric |
| Recommendation Review Pass rate | Quality process metric |
| Controlled trial lift (when authorised) | Effectiveness research |

Activity vanity (clicks on tip chrome) is not a success metric.

---

## 10. Traceability

| Vision 2030 | Roadmap element |
|-------------|-----------------|
| Four questions / design question | All horizons; Today’s focus family |
| AI philosophy | Explainability gates; no opaque AI |
| Success metrics: recommendation acceptance | RE-H1 Decision Journal; Outcome Framework |
| Final Test | Explicit gate on every RE programme |

| Product Constitution | Roadmap element |
|----------------------|-----------------|
| PC-01 | Prefer fewer trustworthy tips |
| PC-06–PC-07 | ADR + Independent Review before engine changes |
| PC-09 | Deterministic ranking |
| PC-11 | Accept/defer/reject agency |
| PC-12 | STOP when trial evidence thin |

---

## 11. Explicit non-goals

- Changing `RecommendationService` or Insight code in SI-001  
- Declaring K2 Pass or recommendation-effectiveness marketing  
- Expanding P4 advisory fields without a dedicated programme  
- Replacing curriculum order with opaque personalisation  

---

**End of SI001_RECOMMENDATION_ENGINE_ROADMAP**
