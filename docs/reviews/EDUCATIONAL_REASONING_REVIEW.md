# Educational Reasoning Review

**Status:** APPROVED WITH CONDITIONS  
**Date:** 11 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Scope reviewed:** Full Educational Intelligence reasoning stack through Capability 2.8 (Curriculum → Twin → Write Strategies → Readiness → Decision)  
**Gate:** Before Capability 2.9 (Explainable Recommendation Engine)  
**Review type:** Architecture / fidelity review only — no implementation in this milestone  
**Governing architecture:** [`docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](../architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Prior gates:**

- Curriculum Architecture Review — Accepted ([`CURRICULUM_ARCHITECTURE_REVIEW.md`](CURRICULUM_ARCHITECTURE_REVIEW.md))
- Epic 2 Midpoint Architecture Review — APPROVED WITH CONDITIONS ([`EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md))
- Readiness Architecture Review — APPROVED WITH CONDITIONS ([`READINESS_ARCHITECTURE_REVIEW.md`](READINESS_ARCHITECTURE_REVIEW.md))

**Companions:** [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin README (`app/domain/twin/README.md`), Decision Engine architecture notes (`docs/architecture/CAPABILITY_2_8_*.md`)

---

## Summary

Capabilities **2.1–2.8** establish a coherent **structural Educational Reasoning stack**: Curriculum as syllabus truth, Learning Evidence as the only legitimate belief input, an immutable Student Digital Twin with four write-path Update Strategies, read-side Readiness Aggregation, and a read-side Decision Engine that selects the next learning action with mandatory candidates, reason codes, lineage, and warrant honesty.

The stack answers Epic 2’s guiding question at the **structural** layer:

> What is the highest-value thing this student should do next?

Write and read intelligence are correctly separated. Domain ownership (Knowledge ≠ Memory ≠ Behaviour ≠ Performance; Readiness ≠ Decision) holds. Explainability is designed into Decision outputs rather than bolted on later. Curriculum V1/V2 compatibility is preserved in domain contracts.

Proceeding to Capability **2.9 Explainable Recommendation Engine** is **conditionally approved**. Recommendation packaging may begin, but only if it remains a **projection** of Decision Engine authority — not a second ranker — and if the binding conditions in §15 are accepted: no legacy hybrid truth, no Confidence-as-mastery, no Twin mutation from recommend paths, CurriculumContext via canonical helpers before production wiring, and honest warrant/cold-start narration.

**Application / production code was not modified by this review.**

---

## Scope Reviewed

| Layer | Primary artefacts |
|---|---|
| **Curriculum Intelligence** | Epic 1 Curriculum Engine + `CurriculumService`; domain `CurriculumContext` |
| **Student Digital Twin** | `app/domain/twin/` aggregate + pipeline |
| **Knowledge / Memory / Behaviour / Performance** | Structural Update Strategies 2.3–2.6 |
| **Readiness** | `app/domain/readiness/` + Capability 2.7 review |
| **Decision** | `app/domain/decision/` + Capability 2.8 architecture/plan/implementation |
| **Explainability** | Architecture §10; Decision lineage + reason codes; Readiness attributions |
| **Legacy consumers** | `ReadinessService`, `RecommendationService`, analytics / missions / burnout / exam timeline |

**Explicitly out of scope for this gate:** Implementing 2.9/2.10; scoring formulas; Alembic / Twin persistence; UI cutover; Belief-enrichment engines.

---

## 1. Curriculum Intelligence

### Verdict: PASS

Curriculum remains the **sole syllabus authority**. Educational Intelligence domains **reference** curriculum identities; they do not invent parallel trees, weights, or order.

| Property | Assessment |
|---|---|
| V1 flat + V2 hierarchical loadable | Preserved from Epic 1; Decision/Readiness tests exercise flat and sectioned `CurriculumContext` |
| Canonical traversal / weights | Owned by Curriculum Engine + `CurriculumService` helpers |
| Domain coupling | `CurriculumContext` is a framework-free value object consumed by Readiness and Decision |
| Forbidden parallel syllabus | Enforced by architecture + Decision nomination (identities only from context) |

### Residual gap

There is still **no production `CurriculumContext` builder** from `CurriculumService` in the service layer. Domain packages correctly refuse Flask/ORM coupling; orchestration remains a precondition for any live Recommendation / Decision consumer.

---

## 2. Student Digital Twin

### Verdict: PASS (structural authority established)

The Twin matches the Educational Intelligence operating model:

```
Learning Evidence → UpdateContext → TwinUpdatePipeline → Update Strategies → new DigitalTwin snapshot
```

| Property | Assessment |
|---|---|
| Single educational-state aggregate | Identity, Goals, Knowledge, Memory, Behaviour, Performance, Predictions |
| Immutable snapshots | Frozen dataclasses; `DigitalTwin.create`; no in-place mutation API |
| Evidence-backed evolution | Pipeline coordinates; strategies own domain evolution |
| Framework independence | Domain package free of Flask / SQLAlchemy / HTTP |
| Read-side peers correctly external | Readiness and Decision are sibling packages — not required Twin fields |

### Gaps relative to full Twin vision (acceptable if conditions hold)

| Concern | Status |
|---|---|
| **ConfidenceState** | Absent — Confidence remains separable only by convention |
| **Decision State on Twin** | Correctly **not** a write-domain peer; in-memory `DecisionState` lives in `app/domain/decision/` |
| **Goals / Identity update strategies** | Structural fields only; goal-change evidence mostly unowned |
| **Production persistence / pipeline factory** | Not shipped — registration order lives in docs/tests |

These absences do **not** block Recommendation packaging if 2.9 treats Twin + Decision as inputs and does not invent substitute learner state.

---

## 3. Knowledge

### Verdict: PASS (structural)

| Owns | Does not own |
|---|---|
| Per-topic mastery slots, evidence lineage, preserved `mastery_belief` bags | Forgetting curves, readiness composites, next-action selection |

`KnowledgeUpdateStrategy` evolves structure from assessment-shaped evidence (and currently also absorbs `CONFIDENCE_RATING` into Knowledge lineage — see Confidence debt). Belief math is correctly deferred; empty bags stay empty.

**Fidelity rule held:** Knowledge answers “know now,” not “still know” and not “exam ready.”

---

## 4. Memory

### Verdict: PASS (structural)

| Owns | Does not own |
|---|---|
| Retention slots, `last_reinforced`, revision evidence refs, preserved `retention_belief` | Mastery scoring, mission generation, curriculum weights |

Complementarity with Knowledge is preserved (disjoint primary evidence catalogues for attempts vs revision; separate belief fields).

**Fidelity rule held:** Memory never becomes a second mastery store.

---

## 5. Behaviour

### Verdict: PASS (structural)

| Owns | Does not own |
|---|---|
| Session/pattern lineage, evidence refs, preserved `consistency_metrics` | Mastery, retention beliefs, pass probability |

Hard educational rule observed: Behaviour never grants or revokes mastery. Mission adherence is not exam readiness.

Decision Engine correctly treats Behaviour primarily as **feasibility / sustainability** (protect intensity, demotion), not as learning value.

---

## 6. Performance

### Verdict: PASS (structural)

| Owns | Does not own |
|---|---|
| Assessment lineage, scoped summaries, evidence refs | Daily scheduling, second Knowledge mastery store |

Performance remains the strongest assessed-signal domain into Readiness and Decision (assessment warrant / diagnose / assess families).

**Residual risk:** Assessment risk elevation still depends on **string tags** in summary dicts (`weak`, `fail`, …). Acceptable for structural ship; Recommendation narration must not over-claim scored accuracy from tag heuristics.

---

## 7. Readiness

### Verdict: PASS (structural derivation) — prior gate upheld

Capability 2.7 delivers factorable, warrant-aware, cold-start-honest `ReadinessState` as a **read-side** judgement:

```
Twin + CurriculumContext + Goals → ReadinessAggregation.derive → ReadinessState
```

| Invariant | Status |
|---|---|
| Write/read firewall | Pass — never mutates Twin domains |
| Factor catalogue complete | Pass — seven factors always present |
| Evidence Warrant honesty | Pass — overall never Mid/High fabrication |
| Confidence omitted (v1) | Pass — intentional |
| Activity ≠ exam readiness | Pass — Behaviour-only paths do not yield exam-ready overall |
| Readiness ≠ Decision | Pass — Decision consumes context only |

Readiness is **sufficient as Decision / Recommendation context**, not as a finished preparedness percentage. Structural overall postures remain capped at fragile / mixed / unknown / not_yet_knowable.

---

## 8. Decision

### Verdict: PASS (structural next-action reasoner)

Capability 2.8 ships `DecisionEngine.evaluate(...)` as Epic 2’s authoritative **next-action** reasoner:

```
Twin + ReadinessState + CurriculumContext + Goals + Constraints (+ history)
        ↓
nominate → constrain/order → select → author reasons → emit Decision
        ↓
optional DecisionState.materialise (in-memory audit)
```

| Contract | Assessment |
|---|---|
| Candidate set mandatory | Pass — selected action appears in candidate set |
| Reason codes authored by Decision only | Pass — versioned catalogue (`REASON_CODE_VOCABULARY_VERSION`) |
| Lineage hooks | Pass — Twin domains, readiness factors, curriculum ids, evidence ids |
| Warrant inheritance | Pass — readiness-citing codes inherit honesty; cold start prefers diagnostic |
| Deterministic structural fields | Pass — tested |
| No Twin / Readiness mutation | Pass — tested |
| No Recommendation / Mission ownership | Pass — package isolation tested |
| V1/V2 CurriculumContext | Pass — both evaluate |
| Confidence risk framing ≠ mastery | Pass — explicit reason code; detection is provisional |

Action families remain separable (Study / Revise / Assess / Diagnostic / Rest-protect). Educational priority posture is structural (tension classes), not a numeric optimizer — correctly deferred.

**Decision is ready to be packaged by 2.9.** It is not yet a production-wired product path.

---

## 9. Explainability Chain

### Verdict: PASS FOR REASONING CORE; PACKAGING DEFERRED TO 2.9

Mandatory chain (Architecture §10):

```
Curriculum factor
    → Learning Evidence (or aggregate)
        → Twin domain state factor(s)
            → Readiness factor + Evidence Warrant
                → Decision Engine reason code(s)
                    → Recommendation explanation (2.9)
```

| Layer | Status before Recommendation Engine |
|---|---|
| Curriculum | Hooks via `CurriculumContext` + Decision lineage |
| Evidence | Twin domain evidence id lineage when present |
| Twin | Domain tags on candidates / lineage |
| Readiness | Factor attributions + warrant on `ReadinessState` |
| Decision | Reason codes + candidates + constraint acknowledgements |
| Recommendation | **Not yet** — 2.9 must package, not invent |

**Forbidden patterns remain binding for 2.9:** opaque “recommended for you,” LLM-invented evidence, narrating supportive Knowledge Strength as exam readiness, post-hoc stories that disagree with Decision reason codes, averaging away High Knowledge + Low Memory tension.

---

## 10. Educational Fidelity

### Verdict: PASS (structural phase)

| Principle | Compliance |
|---|---|
| Learning ≠ study / activity / motivation alone | Behaviour and streaks do not write mastery |
| Evidence over assumption | Cold start → diagnostic / evidence-creating |
| Confidence ≠ mastery | Framing only; no Confidence domain yet |
| Behaviour ≠ learning | Feasibility demotion, not value invention |
| Performance ≠ single-mock readiness | Warrant-constrained; no pass probability in domain |
| Readiness ≠ next action | Firewall held through 2.8 |
| Curriculum-first | No invented topics in Decision nomination |
| Deterministic cores | No LLM ownership of selection |
| Educational fidelity over engagement theatre | Rest/protect is first-class; not empty completion theatre |

Structural honesty intentionally limits product claims: no bold Mid/High readiness, no belief engines, no optimization scores. That is a **feature** of this phase, not a defect — Recommendation Engine must inherit the restraint.

---

## 11. Layering

### Verdict: PASS

```
Templates / JS
      ↓
Blueprints
      ↓
Services (orchestration / persistence bridges / product projections)  ← legacy still live here
      ↓
Domain: Evidence + Twin + Strategies + Readiness + Decision
      ↓
Models + Curriculum Engine
      ↓
DB / JSON
```

| Check | Result |
|---|---|
| Domain packages free of Flask / ORM / HTTP | Pass (tested) |
| Update Strategies do not recommend or compute readiness | Pass |
| Readiness does not select actions | Pass |
| Decision does not mutate Twin or recompute readiness | Pass |
| Curriculum Engine remains syllabus truth | Pass |
| No Alembic / Twin ORM introduced by 2.1–2.8 domain work | Pass |

**Layering debt:** product services still implement parallel readiness/recommendation logic outside Twin-first domain. That is Stage A coexistence — not a layering violation inside `app/domain/`, but it is the dominant program risk for 2.9.

---

## 12. Legacy Convergence

### Verdict: STAGE A — CONTROLLED COEXISTENCE; NOT CONVERGED

| Surface | Current authority | Twin-first status |
|---|---|---|
| `ReadinessService` | TopicProgress / weighted % composites | Parallel — still consumed by dashboard, analytics, settings, missions, recommendations, burnout, exam timeline |
| `RecommendationService` | Heuristic generators over legacy readiness | Parallel — **direct competitor** to Decision Engine for next-action product meaning |
| Domain Readiness / Decision | Twin-first structural truth | Complete in domain; **not product-wired** |

Architecture intent (additive migration, no third hybrid formula) remains correct. Convergence has **not** begun at the service/UI boundary.

**Binding rule for Capability 2.9:** Recommendation Engine must package **Decision Engine** outputs. It must not deepen `RecommendationService` heuristics as a permanent Twin-first authority, and must not average legacy readiness % with Twin factors as temporary truth.

---

## 13. Technical Debt

| ID | Debt | Severity | Target |
|---|---|---|---|
| E2-TD-01 | No `ConfidenceState` / Confidence update path; `CONFIDENCE_RATING` still Knowledge-primary; Decision confidence detection scans Behaviour metrics only | High for calibrated risk framing | Before Decision/Recommendation risk narratives claim calibration |
| E2-TD-02 | Legacy `ReadinessService` + `RecommendationService` dual authority vs Twin-first domain | **Critical–High** for product trust | Stage B: new intelligence paths Twin/Decision-first; freeze legacy deepening |
| E2-TD-03 | No production Twin persistence or Evidence → pipeline service bridge | High for live loop | Persistence / adapter milestone |
| E2-TD-04 | No default registered pipeline factory (`Knowledge → Memory → Behaviour → Performance`) | Medium | First service wiring |
| E2-TD-05 | No `CurriculumContext` builder from `CurriculumService` | Medium–High before production consumers | Thin orchestration helper outside domain |
| E2-TD-06 | Belief / metric bags largely unpopulated; Decision gap heuristics treat missing belief as gap | Medium (intentional structural) | Belief enrichment milestones — not inside Recommendation packaging |
| E2-TD-07 | Choice A omits Evidence Matrix Secondary columns | Medium (documented) | Architecture note before Choice B |
| E2-TD-08 | Goals / plan / exam-date evidence types largely unowned by strategies | Medium | Goals update path |
| E2-TD-09 | Performance summary string-tag risk vocabulary | Medium | Defined fact schema before richer assessment claims |
| E2-TD-10 | Canonical docs drift — Educational Intelligence Architecture and Epic 2 kickoff still show 2.5 as NEXT / 2.5–2.10 Planned | Medium | Doc hygiene with 2.9 kickoff |
| E2-TD-11 | `PredictionState.readiness_snapshot` float unused; temptation for snapshot-as-truth | Low–Medium | Derive-first snapshot strategy with warrant |
| E2-TD-12 | Decision State materialisation in-memory only; no Decision Journal product loop | Medium | 2.9 recording path + later persistence |
| E2-TD-13 | Subsystem docs (`knowledge/subsystems/readiness.md`) still legacy-primary | Medium | Update before/with Stage B |

No new schema/security debt was introduced by the domain reasoning stack itself.

---

## 14. Remaining Architectural Risks

| Risk | Status after 2.8 | Mitigation for 2.9 |
|---|---|---|
| **Parallel learner-state / next-action stores** | Active — legacy RecommendationService vs Decision Engine | 2.9 must consume Decision; freeze heuristic deepening; Stage B cutover plan |
| **Recommendation invents ranking** | Watch | Narrate Decision reason codes; never author competing selection |
| **Opaque product copy** | Controlled in domain; risk at packaging | Mandatory chain packaging; no “recommended for you” without codes |
| **Warrant stripped at presentation** | Future UI risk | Carry warrant / cold-start honesty into recommendation text |
| **Confidence collapse into mastery** | Partially controlled | Do not narrate Knowledge confidence lineage as calibrated Confidence |
| **Domain collapse (Memory≈Knowledge, Performance≈Knowledge)** | Controlled structurally | Preserve family separations in packaging (revise ≠ study) |
| **Evidence → Twin bypass when services wire writes** | Deferred until persistence | All belief changes via Evidence + Update Strategies only |
| **Readiness coerced to Mid/High in copy** | Controlled in domain | Packaging must not invent preparedness |
| **CurriculumContext invented inside services** | Open | Builder via canonical helpers only |
| **LLM ownership creep** | Not present in core | Coach may narrate chain; must not select |
| **Strategy / evaluation order hazards** | Controlled in tests | Preserve registration and evaluation determinism |
| **Premature scoring complexity** | Correctly deferred | Do not smuggle ranking scores into 2.9 “just for UX” |
| **Mission rows as private mastery** | Deferred to 2.10 | Missions remain projections |

---

## 15. Acceptance Decision

### Decision

# APPROVED WITH CONDITIONS

The Educational Intelligence **reasoning architecture** through Capabilities **2.1–2.8** is coherent, layered, educationally faithful at the structural layer, and ready to support **Capability 2.9 Explainable Recommendation Engine** as a **read-side packaging / projection** of Decision Engine outputs — not as a second educational reasoner.

### Conditions (binding)

1. **Decision Engine remains selection authority** — Recommendation Engine packages `Decision` (selected action, candidates, reason codes, lineage, warrant posture). It must not invent a competing rank, score, or topic priority list.
2. **Preserve the explainability chain end-to-end** — every product recommendation must be able to answer Why? via Curriculum → Evidence → Twin → Readiness (when cited) → Decision reason codes → packaged explanation. No opaque single score; no post-hoc stories that disagree with reason codes.
3. **No legacy hybrid truth** — do not average legacy `ReadinessService` percentages with Twin/Decision factors as temporary authority; do not deepen `RecommendationService` heuristics as Twin-first truth while 2.9 lands.
4. **Write/read firewall** — Recommendation paths must not mutate Twin beliefs, bypass the Update Pipeline, recompute competing readiness, or grant mastery on accept.
5. **Warrant and cold-start honesty** — packaging must inherit `not_yet_knowable` / low-warrant / cold-start postures; never coerce unknown into Mid/High preparedness narratives.
6. **Confidence separability** — do not treat Knowledge-held `CONFIDENCE_RATING` lineage or Behaviour confidence-shaped bags as mastery or calibrated exam readiness.
7. **Curriculum V1/V2 invariants** — curriculum-scoped recommendations use canonical identities only; build `CurriculumContext` via canonical Curriculum helpers before any production consumer.
8. **Accept/dismiss is preference, not mastery** — Decision Journal / recommendation_decision evidence updates Behaviour/Decision history later; accepting a recommendation never writes Knowledge/Memory beliefs directly.
9. **Documentation hygiene** — sync Epic 2 kickoff and Educational Intelligence Architecture status tables to mark 2.5–2.8 complete and 2.9 next, before or with 2.9 kickoff.
10. **Structural discipline** — do not introduce numeric selection/ranking formulas inside Recommendation packaging “for polish”; scoring remains owned by later Decision enrichment milestones if approved separately.

### Not approved as unconditional

Unconditional **APPROVED** is withheld while legacy dual next-action/readiness authority remains live, Confidence ownership remains incomplete, and production orchestration (CurriculumContext builder, Twin persistence, default pipeline wiring) is absent.

**REJECTED** is not warranted: the structural reasoning stack does not violate Epic 2 principles and does not block a carefully scoped Explainable Recommendation Engine.

---

## Recommendations

1. **Start Capability 2.9** with an architecture note that locks packaging contracts: Decision in → attributable Recommendation out; journal/evidence out; no private ranking.
2. **Ship a thin `CurriculumContext` builder** (service/orchestration layer) before any live Recommendation consumer.
3. **Plan Stage B cutover** so new Educational Intelligence surfaces never call `RecommendationService.generate_recommendations` / `ReadinessService.get_overall_readiness` as Twin-first authority.
4. **Keep Mission Generation (2.10) separate** — 2.9 packages Decisions; 2.10 projects session/day structure later.
5. **Schedule Confidence separability** before product risk-framing claims “calibrated confidence.”
6. **Refresh subsystem docs** (`knowledge/subsystems/readiness.md` and related) to distinguish legacy analytics owners vs Twin-first derivation / Decision selection.
7. **When first service wires Twin updates**, introduce one default registration helper (`Knowledge → Memory → Behaviour → Performance`).

---

## Architecture Compliance Summary

| Invariant | Status |
|---|---|
| Twin sole educational-state authority (domain) | Preserved |
| Curriculum sole syllabus authority | Preserved |
| Evidence → Strategy → Twin snapshot write path | Intact |
| Readiness derived and factorable | Intact |
| Decision selects next action explainably | Intact (structural) |
| Services must not invent competing educational state | Domain OK; legacy service debt open |
| Plans/missions are consequences, not the learner model | Preserved (2.10 not yet started) |
| V1/V2 curriculum compatibility | Preserved |
| Deterministic cores free of LLM ownership | Preserved |
| Migration impact of this review | **None** |
| Application code intentionally untouched by this review | **Yes** |

---

## Files Examined (review only — none modified)

### Domain

- `app/domain/twin/` (aggregate, states, pipeline, strategies)
- `app/domain/evidence/` (type catalogue cross-check)
- `app/domain/readiness/`
- `app/domain/decision/`

### Architecture / reviews

- `docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`
- `docs/architecture/CAPABILITY_2_5_*.md` … `CAPABILITY_2_8_*.md`
- `docs/reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`
- `docs/reviews/READINESS_ARCHITECTURE_REVIEW.md`
- `docs/reviews/CURRICULUM_ARCHITECTURE_REVIEW.md`
- `docs/epics/EPIC_2_KICKOFF.md`

### Tests (coverage presence)

- `tests/test_*_update_strategy.py`, `tests/test_twin_update_pipeline.py`, `tests/test_digital_twin_domain.py`
- `tests/test_readiness_aggregation.py`
- `tests/test_decision_engine.py`

### Legacy consumers (risk scan)

- `app/services/readiness_service.py`
- `app/services/recommendation_service.py`
- `app/services/analytics_service.py`
- `app/services/burnout_monitor.py`
- `app/services/exam_timeline.py`

---

## Tests Executed

None (documentation-only architecture review). Domain test suites for Twin strategies, Readiness Aggregation, and Decision Engine were inspected for architectural coverage (immutability, firewalls, V1/V2, explainability hooks, fidelity); they were not re-run as part of this review milestone.

---

## Migration Impact

**None.** This review creates documentation only.

---

## Known Limitations of This Review

- Does not re-execute the full pytest suite or ruff.
- Does not deep-audit Learning Evidence extractors/transformers beyond ownership implications.
- Does not design Capability 2.9 packaging algorithms — only gate conditions.
- Does not update `docs/TECHNICAL_DEBT_REGISTER.md` (debt items listed here for the gate; register sync is a follow-up if desired).
- Canonical roadmap docs remain stale relative to shipped 2.5–2.8 (called out as condition / debt).

---

## Stop

Educational Reasoning Review complete. **No implementation. No production file changes beyond this review document.** Capability 2.9 may begin only under the conditions above.
