# Epic 2 Midpoint Architecture Review

**Status:** APPROVED WITH CONDITIONS  
**Date:** 11 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Scope reviewed:** Capabilities 2.1–2.6 (Student Digital Twin → Performance Update Strategy)  
**Gate:** Before Capability 2.7 (Readiness Aggregation)  
**Review type:** Architecture only — no implementation in this milestone  
**Governing architecture:** [`docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](../architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Companions:** [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`ARCHITECTURE.md`](../../ARCHITECTURE.md), Twin package README (`app/domain/twin/README.md`)

---

## Summary

Capabilities 2.1–2.6 establish a coherent **structural write path** for Educational Intelligence: an immutable Student Digital Twin aggregate, a registry-backed Twin Update Pipeline, and four domain Update Strategies (Knowledge, Memory, Behaviour, Performance) that evolve Twin state only from Learning Evidence.

The architecture is **sound for the structural phase**. Domain ownership is clear, strategies share a consistent contract, pipeline registration order is documented and tested, educational anti-patterns are respected (Behaviour is not mastery; Performance is not a second Knowledge store; activity is not readiness), and layering invariants hold (`app/domain/twin/` remains free of Flask/ORM/HTTP).

Proceeding to Capability 2.7 is **conditionally approved**. Readiness Aggregation may begin, but only if the conditions in §13 are accepted: explicit cold-start / empty-belief contracts, no new parallel learner-state forks, Confidence treated as separable (not collapsed into Knowledge), and documentation drift corrected. Belief math, Confidence as a Twin domain, Decision State, and production Twin persistence remain deferred — correctly so for this midpoint — but they are material risks if Readiness invents substitute authority outside the Twin.

**Application / production code was not modified by this review.**

---

## Scope Reviewed

| Capability | Deliverable | Primary artefacts |
|---|---|---|
| **2.1** Student Digital Twin Domain | Immutable aggregate + domain states | `app/domain/twin/digital_twin.py`, `*_state.py` |
| **2.2** Twin Update Pipeline | Registry coordinator | `update_pipeline.py`, `update_context.py`, `update_result.py`, `strategies/base_strategy.py` |
| **2.3** Knowledge Update Strategy | Structural Knowledge evolution | `strategies/knowledge_update_strategy.py` |
| **2.4** Memory Update Strategy | Structural Memory evolution | `strategies/memory_update_strategy.py` |
| **2.5** Behaviour Update Strategy | Structural Behaviour evolution | `strategies/behaviour_update_strategy.py` |
| **2.6** Performance Update Strategy | Structural Performance evolution | `strategies/performance_update_strategy.py` |

**Also reviewed (read-only):** Evidence catalogue (`app/domain/evidence/`), capability architecture notes for 2.5/2.6, Educational Intelligence Architecture §§2–7 / §10 / §12–13, legacy `ReadinessService` / analytics consumers, Epic 2 kickoff roadmap status.

**Explicitly out of scope for this gate:** Capability 2.7+ design detail beyond prerequisites; scoring formulas; Alembic / Twin persistence; UI; Decision Engine implementation.

---

## 1. Digital Twin Architecture

### Verdict: PASS (structural phase)

The Twin matches the Educational Intelligence operating model:

```
Learning Evidence → UpdateContext → TwinUpdatePipeline → Update Strategies → new DigitalTwin snapshot
```

| Property | Assessment |
|---|---|
| **Single educational-state aggregate** | `DigitalTwin` composes Identity, Goals, Knowledge, Memory, Behaviour, Performance, Predictions |
| **Immutable snapshots** | Frozen dataclasses; strategies return new Twins via `DigitalTwin.create`; no in-place mutation API |
| **Evidence-backed evolution** | Pipeline is the only write coordinator; strategies require Learning Evidence types |
| **Curriculum-referenced slots** | Knowledge/Memory require non-empty `topic_id`; Performance scopes prefer curriculum/assessment identity and never invent syllabus trees |
| **Framework independence** | Domain package imports evidence + twin only; tests ban Flask/SQLAlchemy imports |
| **Deterministic structural rules** | Session/assessment/scope id resolution priorities are fixed and documented |

### Gaps relative to full Epic 2 Twin vision

| Domain in architecture diagram | Present in `DigitalTwin`? | Midpoint note |
|---|---|---|
| Identity / Goals | Yes | Structural only; no Goals update strategy yet |
| Knowledge / Memory / Behaviour / Performance | Yes | Structural strategies complete |
| Predictions | Yes | Snapshot slots only; no `PredictionSnapshotStrategy` |
| **Confidence** | **No dedicated state** | Architecture requires Confidence to remain separable from mastery |
| **Decision State** | **No** | Expected later (2.8 / 2.9); not required to *start* 2.7 if Readiness stays read-side |
| Readiness | Derived (correct) | May store snapshots in `PredictionState` later — must not become a write-side invent |

These absences are **acceptable for a structural midpoint** if Readiness Aggregation treats missing Confidence / empty beliefs as explicit low warrant, and does not invent a Confidence-as-mastery shortcut inside Knowledge.

---

## 2. Domain Ownership

### Verdict: PASS

Each delivered domain answers a distinct educational question and refuses foreign authority:

| Domain | Owns | Explicitly does not own | Strategy |
|---|---|---|---|
| **Knowledge** | Topic mastery *slots*, evidence refs, preserved `mastery_belief` | Forgetting curves, readiness composites, recommendations | `KnowledgeUpdateStrategy` |
| **Memory** | Retention slots, `last_reinforced`, `revision_ids`, preserved `retention_belief` | Mastery scoring, mission generation | `MemoryUpdateStrategy` |
| **Behaviour** | Session/pattern lineage, evidence refs, preserved `consistency_metrics` | Mastery/retention beliefs, pass probability | `BehaviourUpdateStrategy` |
| **Performance** | Assessment lineage, scoped summaries, evidence refs | Second mastery store, Behaviour adherence as exam strength | `PerformanceUpdateStrategy` |
| **Goals / Identity** | Scoping / capacity / sitting context | Syllabus invention | No update strategy yet |
| **Predictions** | Stored readiness / pass snapshots | Derivation algorithms | Deferred snapshot strategy |

Hard educational rules observed in code and docs:

1. Behaviour never grants or revokes mastery.  
2. Performance never becomes a second Knowledge mastery store.  
3. Mission adherence never invents strong Performance.  
4. Structural strategies never invent belief/score math.

Complementarity Knowledge ↔ Memory is preserved (separate slots, separate belief fields, disjoint primary evidence catalogues for attempts vs revision).

---

## 3. Evidence Ownership Matrix

### Verdict: PASS WITH DOCUMENTED NARROWING (Choice A)

Canonical matrix (Educational Intelligence Architecture §4) vs shipped primary catalogues:

| Evidence (illustrative) | Canonical primary | Shipped primary owner | Midpoint status |
|---|---|---|---|
| Question attempt / correct / incorrect | Knowledge | Knowledge | Aligned |
| Quiz / mock / past paper / diagnostic | Knowledge **and** Performance | Knowledge + Performance (when topic-scoped Knowledge supports) | Aligned for dual primary |
| Post-exam outcome | Performance | Performance | Aligned |
| Revision / flashcard | Memory | Memory | Aligned |
| Mission completed/missed, skip, abandon, study session, time on task, study break | Behaviour | Behaviour | Aligned |
| Confidence rating | Confidence | **Knowledge only** (in `KNOWLEDGE_EVIDENCE_TYPES`) | **Gap** — no Confidence domain; Knowledge secondary absorption without Confidence primary |
| Recommendation accept/dismiss | Decision State | Unowned by strategies | Deferred (expected) |
| Plan / exam date / goal change | Goals | Unowned by strategies | Deferred |
| Readiness self-review | Confidence (primary) | Unowned | Deferred |

**Choice A (Behaviour 2.5, Performance 2.6):** primary sets only — no secondary weak updates. That is an intentional, documented narrowing of the canonical matrix (which allows Secondary columns). It is architecturally acceptable for the structural phase **if**:

1. Choice A remains explicit in capability docs / Twin README (it does).  
2. Secondary columns are not silently reintroduced inside Readiness Aggregation.  
3. Expanding to Choice B requires an architecture note before coding.

**Orphan / deferred evidence types** (catalogue exists; no Twin strategy primary): e.g. `HINT_REQUESTED`, `DAILY_CHECK_IN`, `AI_TUTOR_INTERACTION`, `REFLECTION_JOURNAL`, `NOTIFICATION_ENGAGEMENT`, `RECOMMENDATION_DECISION`, `PLAN_RESCHEDULED`, `EXAM_DATE_CHANGE`, `MANUAL_GOAL_CHANGE`, `READINESS_REVIEW`. Acceptable at midpoint; must not be absorbed ad hoc by Readiness.

---

## 4. Strategy Consistency

### Verdict: PASS

All four strategies share the same contract and discipline:

| Contract element | Knowledge | Memory | Behaviour | Performance |
|---|---|---|---|---|
| Extends `BaseUpdateStrategy` | ✓ | ✓ | ✓ | ✓ |
| Stable `name` | `knowledge_update` | `memory_update` | `behaviour_update` | `performance_update` |
| `supports(context)` via evidence catalogue | ✓ | ✓ | ✓ | ✓ |
| Topic id required | Yes | Yes | No | No (scope optional) |
| Append-only evidence lineage + dedupe | ✓ | ✓ | ✓ | ✓ |
| Preserves unknown belief/metric bags | `mastery_belief` | `retention_belief` | `consistency_metrics` | summary fact overlay only |
| Returns new Twin; never mutates input | ✓ | ✓ | ✓ | ✓ |
| No readiness / recommend / persist | ✓ | ✓ | ✓ | ✓ |
| Primary-only (Choice A) where applicable | N/A (broader Knowledge set) | Yes | Yes | Yes |

Consistency risks that remain controlled (not failures):

- **Knowledge includes `CONFIDENCE_RATING`** while Confidence is not a Twin domain — structural topic slots may accumulate self-report evidence under Knowledge. Condition for 2.7+: do not treat those refs as calibrated mastery; plan a Confidence path before Decision Engine risk framing.  
- **Performance summary bags** accept supplied facts only — good for structure; Readiness must not interpret arbitrary payload keys as scored accuracy without a defined fact vocabulary.

---

## 5. Pipeline Registration

### Verdict: PASS

`TwinUpdatePipeline`:

- Coordinates only (open for extension via constructor list / `register`).  
- Invokes every supporting strategy in **registration order**.  
- Chains via `context.with_twin(...)` so mixed batches remain sequential and reproducible.  
- Does **not** hard-code educational algorithms or strategy class lists.  
- Empty registry / no applicable strategies return successful no-op with messages.

**Documented structural registration order:**

```
Knowledge → Memory → Behaviour → Performance
```

Rationale (capability 2.5/2.6 architecture notes + Twin README) is coherent for the structural phase: preserve shipped Knowledge→Memory order; Behaviour after Memory; Performance after Behaviour so mixed mission+quiz batches stay reproducible without requiring belief-enrichment reordering yet.

**Observed gap:** there is still **no production default pipeline factory / service wiring**. Registration composition lives in tests and documentation. That is acceptable for domain completeness at this midpoint, but Capability 2.7 (and any persistence bridge) must not invent a second coordinator or a divergent default order.

When belief enrichment lands, architecture already anticipates possible reorder (e.g. Performance before Knowledge enrichment). That reorder must be an explicit later decision — not silent drift.

---

## 6. Explainability Chain

### Verdict: PASS FOR WRITE-PATH FOUNDATION; INCOMPLETE FOR PRODUCT EXPLANATIONS (expected)

Mandatory chain (Architecture §10):

```
Curriculum → Evidence → Twin factors → Readiness factors → Decision reason codes → Recommendation
```

**What 2.1–2.6 already provide**

| Artefact | Role in explainability |
|---|---|
| Learning Evidence ids on domain states | Immutable lineage anchors |
| Per-topic / assessment / session lineage ids | Structural “what was observed” |
| `UpdateResult.applied_strategies` + processing messages | Audit of which write strategies ran |
| Immutable Twin snapshots | Stable inputs for later factor attribution |

**What is not yet present (correctly deferred)**

- Named readiness factors and attributions (2.7)  
- Decision State / reason codes (2.8)  
- Recommendation packaging / Decision Journal loop (2.9–2.10)  
- Populated belief fields that explanations can cite as “mastery low / retention overdue”

**Midpoint rule for 2.7:** Readiness Aggregation must be **factorable** from Twin structure + Curriculum + Goals even when beliefs are empty — citing evidence density / coverage / assessment lineage / reinforcement clocks / session adherence lineage — and must never emit an opaque single score without factors. It must not invent LLM or post-hoc stories that disagree with Twin evidence refs.

---

## 7. Educational Fidelity

### Verdict: PASS

The shipped architecture represents **learning structure**, not engagement theatre:

| Principle | Midpoint compliance |
|---|---|
| Learning ≠ study / activity / motivation alone | Behaviour and time-on-task do not write Knowledge/Memory beliefs |
| Evidence over assumption | Cold-start empty domains are valid; strategies do not fabricate High Performance or perfect adherence |
| Confidence ≠ mastery | Not fully modelled yet — **condition** (see §13); Knowledge must not permanently own confidence narrative |
| Behaviour ≠ learning | Explicit hard rule in Behaviour strategy + docs |
| Performance ≠ single-mock readiness | Strategy stores lineage/summaries; does not emit pass probability |
| Curriculum-first | Topic/scope identities required or refused; no parallel syllabus |
| Deterministic cores | Fixed id-resolution priorities; no network/LLM in write path |
| Structural-first, beliefs later | Intentional and consistently applied across 2.3–2.6 |

Educational fidelity risk if 2.7 missteps: treating mission completion counts or empty cold-start Twins as exam readiness. Architecture forbids this; Capability 2.7 must encode it as named factors with low warrant, not as optimistic composites.

---

## 8. Layering Compliance

### Verdict: PASS

Relative to application architecture:

```
Templates / JS → Blueprints → Services → Domain (Twin + Evidence + Strategies) → Models + Curriculum Engine → DB / JSON
```

| Check | Result |
|---|---|
| Twin/strategies free of Flask / SQLAlchemy / request globals | Pass (enforced in strategy tests) |
| Pipeline contains no educational scoring | Pass |
| Strategies do not persist, recommend, or plan | Pass |
| Curriculum Engine remains syllabus truth | Pass — Twin references identities only |
| No Alembic / Twin ORM introduced by 2.1–2.6 | Pass |
| V1/V2 curriculum loadability | Unaffected by Twin domain work (traversal N/A to strategy modules) |
| Application factory / blueprint surface unchanged by Twin write path | Pass for this scope |

**Layering debt outside Twin package (known, not introduced by 2.1–2.6):** legacy `ReadinessService` and analytics still derive readiness/mastery narratives from `TopicProgress` and related product tables — a **parallel learner-state** relative to the Twin authority principle. Capability 2.7 must converge toward Twin-first inputs and must not deepen that fork.

---

## 9. Technical Debt

Honest leftover risk introduced or crystallised by 2.1–2.6:

| ID | Debt | Severity | Target |
|---|---|---|---|
| E2-TD-01 | **No ConfidenceState / Confidence update path** while `CONFIDENCE_RATING` feeds Knowledge | High for Decision/Readiness narrative | Before Decision Engine; clarify for 2.7 factor set |
| E2-TD-02 | **Legacy ReadinessService / analytics mastery formulas** coexist with Twin | High for dual authority | Explicit convergence plan during/after 2.7 |
| E2-TD-03 | **No production Twin persistence or evidence→pipeline service bridge** | Medium | Persistence / adapter milestone (not 2.7 math) |
| E2-TD-04 | **Choice A omits matrix Secondary columns** | Medium (documented) | Architecture note before Choice B |
| E2-TD-05 | **Belief / metric bags never populated** | Medium for numeric readiness | Later strategy enrichment or Memory/Knowledge engines |
| E2-TD-06 | **Goals / Decision State evidence types unowned** | Medium | Goals strategy / Decision materialisation |
| E2-TD-07 | **Canonical docs drift** — Educational Intelligence Architecture still lists 2.5–2.6 as Planned; Epic 2 kickoff still marks 2.5 as NEXT | Low–Medium | Doc hygiene before/with 2.7 kickoff |
| E2-TD-08 | **No default registered pipeline helper** | Low–Medium | Shared factory when first service wires Twin updates |
| E2-TD-09 | Performance `scope_id` may mix topic vs assessment-instance namespaces | Low | Document scope vocabulary when scoring lands |

No schema migrations or security debt were introduced by the Twin write-path capabilities.

---

## 10. Remaining Architectural Risks

| Risk | Impact | Midpoint mitigation status |
|---|---|---|
| Parallel learner-state stores | Divergent readiness; broken trust | Twin authority established in domain; **legacy services not yet redirected** |
| Domain collapse (Memory≈Knowledge, Performance≈Knowledge, Confidence≈mastery) | Unexplainable dual scores | Structural separation strong; Confidence collapse risk remains |
| Evidence → Twin bypass from services | Silent mutations | No Twin persist path yet — risk rises when services wire writes |
| Premature scoring complexity | Unmaintainable math | Correctly deferred; 2.7 must stay factorable and not invent belief engines inside aggregation |
| Strategy order hazards | Non-reproducible mixed batches | Order locked in docs + tests for structural phase |
| Readiness conflated with next action | Wrong ownership | Architecture separates 2.7 vs 2.8 — keep that firewall |
| Opaque composites | Product thesis failure | Explainability foundation present; 2.7 must emit factors |
| V1 breakage | Legacy plans fail | Twin work does not alter curriculum traversal; 2.7 must use canonical helpers for weights |
| LLM ownership creep | Non-determinism | Not present in write path; keep out of readiness core |

---

## 11. Readiness Prerequisites

Capability 2.7 (Readiness Aggregation) may proceed if it treats the following as binding inputs/constraints.

### Ready now

| Prerequisite | Status |
|---|---|
| Twin domains for Knowledge / Memory / Behaviour / Performance structure | Ready |
| Goals (exam/completion date, weekly hours) + Identity (curriculum/sitting) | Ready as structural fields |
| PredictionState slots for optional snapshots | Ready (empty) |
| Curriculum weights / order via Curriculum Engine + `CurriculumService` | Ready (Epic 1) |
| Evidence lineage ids on Twin domains | Ready |
| Write/read separation (aggregation must not mutate Knowledge/Memory) | Ready as architectural rule |
| Registration-order-stable Twin snapshots for mixed evidence | Ready when callers register K→M→B→P |

### Must be designed explicitly in 2.7 (conditions)

| Prerequisite | Requirement |
|---|---|
| **Empty beliefs / cold start** | Missing `mastery_belief` / `retention_belief` / metrics / summaries ⇒ named low-warrant factors — never fabricated High readiness |
| **Structural proxies** | Coverage from topic slots, reinforcement freshness from `last_reinforced`, assessment warrant from assessment lineage/summaries, pace feasibility from Behaviour lineage + Goals hours — without inventing scoring engines inside the aggregator if owned elsewhere |
| **Confidence** | Either omit as a readiness factor initially, or consume only as an explicitly provisional signal — **do not** equate Knowledge evidence refs from `CONFIDENCE_RATING` with calibrated mastery |
| **Legacy ReadinessService** | Additive migration stance: do not create a third formula; plan Twin-first convergence; no new analytics fork |
| **V1/V2 safety** | Weight/order via canonical curriculum helpers only; no global Section requirement |
| **Snapshot path** | If storing readiness in PredictionState, derive first — storage must not skip aggregation |
| **Non-goals** | No next-action selection; no mission generation; no Twin write strategies inside 2.7 |

### Not required to start 2.7

- Decision State / Decision Engine  
- Mission Generation Intelligence  
- Full Confidence domain (if factored out of readiness v1)  
- Belief-enrichment strategy math  
- Twin ORM persistence (aggregation can be domain-pure on in-memory Twin snapshots in tests)

---

## 12. Recommendations

1. **Proceed to Capability 2.7** under the acceptance conditions in §13.  
2. **Publish a short Readiness Aggregation architecture note** before coding: factor list, cold-start semantics, V1/V2 weight handling, relationship to legacy `ReadinessService`, and PredictionState snapshot rules.  
3. **Update roadmap / canonical status tables** so Educational Intelligence Architecture and Epic 2 kickoff reflect 2.5–2.6 complete and 2.7 next.  
4. **Keep Choice A** until a deliberate Choice B architecture note exists; do not smuggle secondary updates into readiness.  
5. **Schedule Confidence separability** (domain or dedicated update path) before Decision Engine risk framing; until then, document that `CONFIDENCE_RATING` under Knowledge is lineage-only.  
6. **When first service wires Twin updates**, introduce a single default registration helper (`Knowledge → Memory → Behaviour → Performance`) — do not scatter orders.  
7. **Do not deepen TopicProgress-based readiness formulas** in analytics while 2.7 lands; prefer adapters that can later read Twin factors.  
8. **Preserve structural-first discipline** — resist filling belief bags inside 2.7 “just to make a score.”

---

## 13. Acceptance Decision

### Decision

# APPROVED WITH CONDITIONS

The Digital Twin write-path architecture for Capabilities **2.1–2.6** is coherent, layered, educationally faithful, and ready to support **Capability 2.7 Readiness Aggregation** as a **read-side, factorable derivation** over Twin + Curriculum + Goals.

### Conditions (binding)

1. **Cold-start / empty-belief contract** — Readiness Aggregation must define named factors for missing beliefs, empty Behaviour metrics, and sparse Performance; it must never invent High readiness or High Performance from absence or from mission adherence alone.  
2. **No parallel authority** — Capability 2.7 must not create a new permanent learner-state store or a third readiness formula that ignores Twin structure; legacy `ReadinessService` may remain temporarily but must be on an explicit convergence path.  
3. **Confidence separability** — Do not treat Knowledge-held `CONFIDENCE_RATING` lineage as mastery or as calibrated Confidence; either omit Confidence from readiness v1 or introduce an explicit provisional factor with lower warrant than Performance.  
4. **Write/read firewall** — Readiness Aggregation must not mutate Twin domains, bypass the Update Pipeline, select next actions, or generate missions.  
5. **Curriculum V1/V2 invariants** — Weights and ordering only via canonical Curriculum helpers; no Section-global assumptions.  
6. **Documentation hygiene** — Sync Epic 2 kickoff / Educational Intelligence Architecture status tables to mark 2.5–2.6 complete before or as part of 2.7 kickoff.  
7. **Registration order stability** — Any future default Twin update wiring must preserve Knowledge → Memory → Behaviour → Performance until a documented belief-phase reorder is approved.

### Not approved as unconditional

Unconditional **APPROVED** is withheld until Confidence ownership is clarified for readiness narratives and legacy dual-readiness risk is acknowledged in the 2.7 architecture note.  
**REJECTED** is not warranted: the structural write path does not violate Epic 2 principles and does not block a carefully scoped Readiness Aggregation.

---

## Files Examined (review only — none modified)

### Domain

- `app/domain/twin/` (aggregate, states, pipeline, context, result, strategies)  
- `app/domain/evidence/evidence_type.py` (catalogue cross-check)

### Architecture / product docs

- `docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`  
- `docs/architecture/CAPABILITY_2_5_*.md`, `docs/architecture/CAPABILITY_2_6_*.md`  
- `docs/epics/EPIC_2_KICKOFF.md`  
- `STUDENT_DIGITAL_TWIN.md`  
- `app/domain/twin/README.md`

### Tests (coverage presence)

- `tests/test_digital_twin_domain.py`  
- `tests/test_twin_update_pipeline.py`  
- `tests/test_knowledge_update_strategy.py`  
- `tests/test_memory_update_strategy.py`  
- `tests/test_behaviour_update_strategy.py`  
- `tests/test_performance_update_strategy.py`

### Legacy consumers (risk scan)

- `app/services/readiness_service.py`  
- `app/services/analytics_service.py`

---

## Tests Executed

None (documentation-only architecture review). Strategy and pipeline test suites exist and were inspected for architectural coverage (immutability, ownership isolation, registration order, framework-import bans); they were not re-run as part of this review milestone.

---

## Migration Impact

**None.** This review creates documentation only. Capabilities 2.1–2.6 introduced no Alembic migrations.

---

## Architecture Compliance

- **Layering:** Pass — Twin/strategies remain domain-pure.  
- **Curriculum V1/V2:** Preserved / unaffected by Twin write-path modules; readiness work must continue to honour traversal invariants.  
- **Twin as educational-state authority:** Established in domain; service convergence still open (condition).  
- **Evidence → Strategy → Twin snapshot:** Intact.

---

## Known Limitations of This Review

- Does not re-execute the full pytest suite or ruff.  
- Does not deep-audit Learning Evidence extractors/transformers/validators beyond type catalogue ownership.  
- Does not design Capability 2.7 algorithms — only prerequisites and gate conditions.  
- Does not update `docs/TECHNICAL_DEBT_REGISTER.md` (debt items listed here for the gate; register sync is a follow-up if desired).

---

## Stop

Architecture review complete. **No implementation. No production file changes beyond this review document.** Capability 2.7 may begin only under the conditions above.
