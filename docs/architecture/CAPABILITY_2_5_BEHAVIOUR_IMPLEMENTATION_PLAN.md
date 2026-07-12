# Capability 2.5.3 — Behaviour Update Strategy Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.5 Behaviour Update Strategy (structural implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Domain charter:** [`CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md`](CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md)  
**Update strategy architecture:** [`CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md`](CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md)  
**Precedents:** Capability 2.3 `KnowledgeUpdateStrategy`, Capability 2.4 `MemoryUpdateStrategy`  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`)  
**Scope:** Plan the structural write-path implementation of `BehaviourUpdateStrategy` — **no code, tests, migrations, services, or scoring formulas in this document’s milestone**

---

## Document purpose

This plan translates the approved Behaviour domain analysis and update-strategy architecture into a concrete, executable implementation sequence for Capability 2.5.

It answers:

1. What is in / out of scope for the first Behaviour strategy ship  
2. Which files to create and modify  
3. Which domain model additions are required vs deferred  
4. How to register Behaviour in the Twin Update Pipeline  
5. How evidence ownership maps onto `supports` / `apply`  
6. How to test, migrate (or not), and accept the work  

**Hard educational rule (binding):** Behaviour never grants or revokes mastery by itself.  
**Governing principle:** Behaviour is not learning; Activity is not readiness.  
**Structural discipline:** Structure first, beliefs later — mirror Knowledge/Memory.

**Non-goals of this document**

- Implementing `BehaviourUpdateStrategy` or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Concrete adherence / consistency / burnout / velocity formulas  
- UI, gamification, notifications, or Decision Engine changes  

---

# 1. Scope of implementation

## 1.1 In scope (Capability 2.5 structural ship)

| Item | Intent |
|---|---|
| **`BehaviourUpdateStrategy`** | New `BaseUpdateStrategy` subclass; framework-free; immutable Twin snapshots |
| **Primary evidence `supports` set** | Mission completed/missed, skipped/abandoned session, study session, time on task, study break |
| **Structural `apply` rules** | Append session/history lineage (deduped); preserve `consistency_metrics`; set `last_updated`; optional pattern ids only when already supplied |
| **Optional additive lineage** | Prefer adding optional `evidence_ids` on `BehaviourState` if needed for audit parity with Knowledge; prefer id-list-only over nested records in the first ship |
| **Pipeline registration exports** | Re-export strategy + type frozenset from `strategies` and `twin` packages |
| **Domain README update** | Document Behaviour strategy alongside Knowledge/Memory |
| **Focused unit tests** | Mirror `tests/test_knowledge_update_strategy.py` / `tests/test_memory_update_strategy.py` |

## 1.2 Explicitly out of scope

| Item | Why deferred |
|---|---|
| Consistency / adherence / streak scoring | Structural phase only; fill `consistency_metrics` later |
| Burnout, velocity, preferred-window models | Derived Behaviour / Predictions / Motivation |
| Nested `BehaviourRecord` map (unless id-list proves insufficient) | Architecture allows either; first ship prefers id-list-only |
| Secondary weak updates (accept/dismiss, plan reschedule, assessment/revision presence) | Documented optional; may land in a thin follow-up within 2.5 or stay deferred — see §5 |
| `PerformanceUpdateStrategy` | Capability 2.6 |
| Confidence calibration ownership | Confidence remains separable |
| Readiness Aggregation / Decision Engine / Mission Generation | Capabilities 2.7–2.10 (read Behaviour; do not write it) |
| Persistence, ORM, Alembic, HTTP, Flask services | Domain layer only; no Twin DB in this capability |
| Curriculum Engine / V1–V2 traversal changes | Behaviour must not invent syllabus |
| Hard-coding Behaviour inside `TwinUpdatePipeline` | Pipeline remains a registration shell |

## 1.3 Success shape

After implementation:

```
Learning Evidence (Behaviour-primary types)
      → UpdateContext
            → TwinUpdatePipeline
                  → KnowledgeUpdateStrategy (if supports)
                  → MemoryUpdateStrategy (if supports)
                  → BehaviourUpdateStrategy (if supports)
                        → new BehaviourState in new DigitalTwin snapshot
```

Same Twin + same ordered evidence batch → same structural Behaviour outcome. No scoring. No Flask. No migrations.

---

# 2. Files to create

| Path | Role |
|---|---|
| `app/domain/twin/strategies/behaviour_update_strategy.py` | `BehaviourUpdateStrategy` + `BEHAVIOUR_EVIDENCE_TYPES` (primary set; optional secondary set if in-scope) |
| `tests/test_behaviour_update_strategy.py` | Unit tests mirroring Knowledge/Memory strategy harness (framework-import bans, immutability, ownership, pipeline registration order) |

**Optional (only if §4 chooses nested records in the same milestone)**

| Path | Role |
|---|---|
| Nested types inside `app/domain/twin/behaviour_state.py` | e.g. `BehaviourRecord` frozen dataclass — prefer co-locating with `BehaviourState` like `TopicMasteryRecord` / `RetentionRecord` |

Do **not** create: services, blueprints, migrations, scoring modules, or a separate Behaviour engine package.

---

# 3. Files to modify

| Path | Change |
|---|---|
| `app/domain/twin/strategies/__init__.py` | Import/export `BehaviourUpdateStrategy`, `BEHAVIOUR_EVIDENCE_TYPES`; update package docstring |
| `app/domain/twin/__init__.py` | Re-export Behaviour strategy symbols in `__all__` |
| `app/domain/twin/README.md` | Add Behaviour Update Strategy section; registration order Knowledge → Memory → Behaviour; ownership notes |
| `app/domain/twin/behaviour_state.py` | **Only if** additive fields are chosen (§4): e.g. optional `evidence_ids`; keep existing fields and `create()` backwards-compatible |
| `app/domain/twin/strategies/base_strategy.py` | Docstring mention only if needed (already anticipates Behaviour) |
| Existing Knowledge/Memory strategy tests (optional) | Add one mixed-batch / registration-order assertion that includes Behaviour if those suites already assert pipeline composition — prefer keeping Behaviour assertions in the new test module |

**Do not modify (this capability)**

- `app/domain/twin/update_pipeline.py` algorithm (registration API already sufficient)  
- Knowledge/Memory strategy ownership frozensets (except ensuring they still exclude Behaviour-primary types — already true)  
- Services, blueprints, templates, models, Alembic  
- Evidence catalogue enum unless a missing type blocks primary set (current `EvidenceType` already covers the primary set)

---

# 4. Domain model additions

## 4.1 Existing contract (keep)

`BehaviourState` already ships structural slots:

| Field | Strategy duty |
|---|---|
| `consistency_metrics` | **Preserve** unknown keys/values; never invent scores |
| `session_history_ids` | Append deduped session/history/practice-unit ids when applicable |
| `study_pattern_ids` | Append only when evidence/metadata/prior Twin supplies pattern ids; do not invent clusters |
| `last_updated` | Set to latest processed applicable evidence timestamp |

`DigitalTwin` already composes `behaviour: BehaviourState`. No aggregate redesign.

## 4.2 Recommended additive change (structural ship)

| Addition | Recommendation | Rationale |
|---|---|---|
| **`evidence_ids: tuple[str, ...]` on `BehaviourState`** | **Yes — additive optional default `()`** | Parity with Knowledge lineage; audit for applied Behaviour evidence; architecture allows state-level evidence ids |
| **Nested `BehaviourRecord`** | **No for first ship** | Id-list-only phase is architecture-compliant; avoids premature practice-unit schema; can add later without breaking renames if `evidence_ids` + session ids suffice |
| **Belief/scoring fields** | **No** | Consistency quality, adherence ratio, burnout contribution remain deferred |

If `evidence_ids` is added:

- Update `BehaviourState.create(...)` with a defaulted parameter  
- Defensive copy to tuple  
- Preserve frozen dataclass immutability  
- Do not rename or remove existing fields  

## 4.3 Session / practice-unit identity extraction

`LearningEvidence` has no first-class `session_id` / `mission_id` field. Structural strategy should resolve lineage ids deterministically from, in priority order to be fixed in implementation:

1. Explicit payload keys when present (e.g. `session_id`, `mission_id`, `practice_unit_id`)  
2. Else `originating_event_id` when non-empty  
3. Else `evidence_id` as the session-history reference for that event  

Document the chosen priority in the strategy module docstring and tests. Never invent curriculum `topic_id` when absent.

## 4.4 What must not be added now

- Mutable streak counters  
- Parallel mission store inside Behaviour  
- `retention_belief` / `mastery_belief` / performance summaries  
- Readiness composites or Decision State fields  

---

# 5. Strategy implementation order

## 5.1 Class contract (match Knowledge/Memory)

```
BehaviourUpdateStrategy(BaseUpdateStrategy)
  name → "behaviour_update"          # stable UpdateResult audit id
  supports(context) → bool
  apply(context) → DigitalTwin       # new snapshot; never mutate input
```

Export:

```
BEHAVIOUR_EVIDENCE_TYPES: frozenset[EvidenceType]   # primary (required)
# Optional second frozenset if secondary weak updates ship in same PR:
# BEHAVIOUR_SECONDARY_EVIDENCE_TYPES: frozenset[EvidenceType]
```

## 5.2 Primary evidence types (must implement)

Map architecture §5.3 onto existing `EvidenceType` members:

| Architecture concept | `EvidenceType` |
|---|---|
| Mission completed | `MISSION_COMPLETED` |
| Mission missed / expired | `MISSION_MISSED` |
| Skipped session | `SKIPPED_SESSION` |
| Abandoned session | `SESSION_ABANDONED` |
| Study session started/completed | `STUDY_SESSION` |
| Time on task | `TIME_ON_TASK` |
| Study break | `STUDY_BREAK` |

**`supports` rule:** at least one evidence item whose `evidence_type` is in `BEHAVIOUR_EVIDENCE_TYPES`.  
**Do not require `topic_id`.** Incomplete topic mapping must not block Behaviour updates.

## 5.3 Secondary evidence types (implementation choice)

Architecture allows optional weak updates. This plan recommends:

| Choice | Decision for first ship |
|---|---|
| **A — Primary only (recommended)** | Ship primary set only; document secondary as follow-up. Keeps scope tight and ownership clearest. |
| **B — Primary + documented secondary** | Also append weak lineage for `RECOMMENDATION_DECISION`, `PLAN_RESCHEDULED`, and optionally assessment/revision types — **without** stealing Knowledge/Memory/Performance primary ownership |

If Choice B is taken, secondary must:

- Only append ids / timestamps  
- Never compute preference scores  
- Never mutate Knowledge/Memory/Performance  
- Be listed explicitly in frozensets and tests  

**Default recommendation: Choice A.**

## 5.4 Structural `apply` algorithm (intended behaviours)

1. Filter applicable evidence (primary; + secondary if Choice B).  
2. Preserve `consistency_metrics` via defensive copy of the existing bag.  
3. For each applicable item, append deduped practice-unit / session id to `session_history_ids`.  
4. Append pattern ids to `study_pattern_ids` only when supplied on evidence payload/metadata or already present — never invent.  
5. If `evidence_ids` exists on state, append deduped `evidence.evidence_id`.  
6. Set `last_updated` to max(existing, applicable timestamps).  
7. Build new `BehaviourState` via `create(...)`.  
8. Return `DigitalTwin.create(...)` copying all other domains by reference from the input Twin, replacing only `behaviour`.  

## 5.5 Explicit non-computations

Must **not**:

- Compute consistency scores, adherence ratios, streak lengths  
- Infer burnout or motivation  
- Grant/revoke Knowledge or Memory beliefs  
- Absorb quiz/mock score summaries  
- Select recommendations or generate missions  
- Persist Twin or evidence  
- Import Flask / SQLAlchemy / request globals  

## 5.6 Idempotence and determinism

- Dedupe id appends on replay of the same evidence id  
- Same Twin + same ordered batch → same Behaviour structural outcome  
- No network / LLM on the write path  

---

# 6. Twin Pipeline integration

## 6.1 Registration order (structural phase — locked)

| Order | Strategy | Status |
|---|---|---|
| 1 | `KnowledgeUpdateStrategy` | Existing |
| 2 | `MemoryUpdateStrategy` | Existing |
| 3 | `BehaviourUpdateStrategy` | This capability |
| 4 | `PerformanceUpdateStrategy` | Capability 2.6 — not registered yet |

Rationale (from approved architecture):

1. Preserves shipped Knowledge → Memory order  
2. Behaviour structural updates do not require prior Knowledge/Memory mutation  
3. Mixed batches stay reproducible when order is fixed  
4. Future belief enrichment that reads other domains can rely on Knowledge/Memory already refreshed  

## 6.2 Integration mechanics

- Callers construct `TwinUpdatePipeline([KnowledgeUpdateStrategy(), MemoryUpdateStrategy(), BehaviourUpdateStrategy()])` **or** `register` in that order  
- Pipeline class must **not** hard-code Behaviour algorithms or import Behaviour by default inside `update_pipeline.py`  
- Each `apply` receives context whose Twin reflects prior strategies (`context.with_twin(...)`)  
- `UpdateResult.applied_strategies` must include `"behaviour_update"` when Behaviour ran  

## 6.3 Mixed-batch expectations

| Batch shape | Expected strategies |
|---|---|
| Quiz only | Knowledge (+ Performance later); Behaviour no-op unless secondary Choice B |
| Revision only | Memory; Behaviour no-op unless secondary Choice B |
| Mission completed only | Behaviour |
| Mission completed + quiz | Knowledge + Behaviour (mission primary; quiz Knowledge-primary) |
| Flashcard + skipped session | Memory + Behaviour |

Mission completion must not overwrite quiz-driven Knowledge updates.

## 6.4 Decision Engine loop (read-side note only)

Accept/dismiss becomes Learning Evidence later and re-enters this pipeline. Decision Engine must not mutate Behaviour in place. No Decision Engine code changes in Capability 2.5.

---

# 7. Evidence ownership implementation

## 7.1 Ownership matrix → code mapping

| Evidence type | Behaviour role | Strategy action |
|---|---|---|
| `MISSION_COMPLETED` / `MISSION_MISSED` | Primary | Must `supports`; structural lineage |
| `SKIPPED_SESSION` / `SESSION_ABANDONED` | Primary | Must `supports`; structural lineage |
| `TIME_ON_TASK` / `STUDY_BREAK` / `STUDY_SESSION` | Primary | Must `supports`; structural lineage |
| `RECOMMENDATION_DECISION` | Secondary | Decision State primary; Behaviour weak only if Choice B |
| `PLAN_RESCHEDULED` / goal changes | Secondary / Goals primary | Weak only if Choice B; Goals facts stay out of Behaviour ownership |
| Question / quiz / mock / diagnostic | Secondary; Knowledge/Performance primary | Not in primary frozenset |
| `REVISION_SESSION` / `FLASHCARD_REVIEW` | Secondary; Memory primary | Not in primary frozenset |
| `CONFIDENCE_RATING` / `READINESS_REVIEW` | Secondary; Confidence primary | Not Behaviour-owned |
| `POST_EXAM_OUTCOME` | — | Must not `supports` |

## 7.2 Hard rules in implementation

1. Domains reference evidence ids; they never rewrite the evidence log.  
2. Secondary never steals primary.  
3. Mixed batches are valid.  
4. Non-events (dashboard view, open-without-decision, cosmetic streaks, coach narration) are not Learning Evidence types for Behaviour ownership — do not invent synthetic Behaviour evidence in strategy tests as if they were catalogue types.  
5. Attribution (`provenance`) may be preserved on lineage metadata later; structural strategy need not score by attribution.  

## 7.3 Relationship to sibling frozensets

Confirm (do not expand) that:

- `KNOWLEDGE_EVIDENCE_TYPES` does not include Behaviour-primary mission/skip/time types (already true)  
- `MEMORY_EVIDENCE_TYPES` remains revision/flashcard only (already true)  

Behaviour must not absorb those primary columns.

---

# 8. Public API impact

## 8.1 Domain public surface (additive)

New exports from `app.domain.twin` / `app.domain.twin.strategies`:

| Symbol | Kind |
|---|---|
| `BehaviourUpdateStrategy` | Class |
| `BEHAVIOUR_EVIDENCE_TYPES` | `frozenset[EvidenceType]` |

If `BehaviourState.evidence_ids` is added, it is a **backwards-compatible additive field** with default empty tuple — existing `BehaviourState.create()` call sites remain valid.

## 8.2 Unchanged public contracts

| Contract | Impact |
|---|---|
| `TwinUpdatePipeline` constructor / `register` / `process` | Unchanged API; callers opt in by registering Behaviour |
| `UpdateContext` / `UpdateResult` | Unchanged |
| `BaseUpdateStrategy` | Unchanged |
| `LearningEvidence` / `EvidenceType` | Unchanged (types already exist) |
| HTTP / Flask / services | No public product API change |
| ORM / Alembic | None |

## 8.3 Caller expectations

Any future service that builds a default pipeline for Twin updates should register Knowledge → Memory → Behaviour in that order. Capability 2.5 does not require inventing that service wiring if none exists yet — domain package completeness is the deliverable.

---

# 9. Testing strategy

## 9.1 New module

`tests/test_behaviour_update_strategy.py` — mirror Memory/Knowledge strategy tests:

| Suite | Assertions |
|---|---|
| **Contract** | Subclasses `BaseUpdateStrategy`; `name == "behaviour_update"` |
| **supports** | True for each primary type; False for revision-only, quiz-only, post-exam, empty batch |
| **No topic_id required** | Mission completed without `topic_id` still supports and applies |
| **Structural apply** | Appends session lineage; sets `last_updated`; preserves `consistency_metrics` keys/values |
| **Idempotence** | Replaying same evidence id does not duplicate lineage / evidence ids |
| **Immutability** | Input Twin / BehaviourState unchanged after `apply` |
| **Non-scoring** | `consistency_metrics` not invented; no mastery/retention fields touched |
| **Cross-domain isolation** | Mission-only batch leaves Knowledge/Memory unchanged; quiz-only does not run Behaviour (primary-only Choice A) |
| **Pipeline order** | Knowledge → Memory → Behaviour registration; mixed mission+quiz applies Knowledge then Behaviour; `applied_strategies` contains expected names |
| **Framework purity** | AST / import ban for Flask/SQLAlchemy (same pattern as Memory tests) |
| **Determinism** | Same inputs → equal Behaviour structural fields |

## 9.2 Regression

- Existing `tests/test_knowledge_update_strategy.py` and `tests/test_memory_update_strategy.py` must remain green  
- No curriculum V1/V2 engine test changes expected  
- Run: `python -m pytest tests/test_behaviour_update_strategy.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py -v` and `ruff check app/ tests/`

## 9.3 Out of test scope for this capability

- HTTP integration  
- Persistence round-trips  
- Scoring correctness  
- Decision Engine feasibility consumption  
- Performance strategy dual updates (document as 2.6 follow-up)  

---

# 10. Migration impact

| Concern | Impact |
|---|---|
| Alembic / schema | **None** — Twin domain remains in-memory/framework-free; no ORM Twin tables in this capability |
| Data backfill | **None** |
| Evidence catalogue DB | **None** |
| Curriculum JSON | **None** |

If a later persistence milestone stores Twin snapshots, additive `evidence_ids` on Behaviour would require a separate schema plan then — not now.

---

# 11. Backwards compatibility

| Invariant | Plan |
|---|---|
| Curriculum V1 and V2 loadable/traversable | Unchanged; Behaviour does not invent syllabus or require Sections |
| Existing Knowledge → Memory registration | Continues to work; Behaviour is additive registration |
| Existing empty `BehaviourState` | Remains valid cold start |
| Additive fields only | Prefer optional defaults; no breaking renames of `BehaviourState` fields |
| Evidence append-only semantics | Preserved |
| Deterministic cores | No LLM/network on write path |
| Knowledge/Memory complementary stores | Behaviour must not become a third mastery/retention store |
| Legacy services | Untouched; no parallel Behaviour truth in analytics/missions |

Cold start: empty references remain valid. Consumers must treat missing Behaviour as low-confidence default feasibility — not implemented in 2.5, but strategy must not invent “perfect adherence” defaults in metrics.

---

# 12. Risks

| Risk | Impact | Mitigation in implementation |
|---|---|---|
| Equating mission completion with learning | False mastery | Tests prove Knowledge unchanged on mission-only; strategy non-goals |
| Premature consistency scoring | Unmaintainable math | Preserve metric bag only; forbid score keys in structural ship |
| Requiring `topic_id` | Missed Behaviour updates | Explicit supports without topic; dedicated tests |
| Inventing pattern clusters | Opaque fake lineage | Append pattern ids only when supplied |
| Secondary evidence theft | Behaviour owns quizzes/revisions | Primary-only default; frozenset review |
| Strategy order drift | Non-reproducible mixed batches | Lock Knowledge → Memory → Behaviour; document + test |
| Nested `BehaviourRecord` overbuild | Scope creep | Defer nested records unless id-list insufficient |
| In-place Twin mutation | Broken snapshot audit | Frozen dataclasses; immutability tests |
| Hard-coding pipeline | Closed extension | Register only; do not edit pipeline algorithms |
| Mission rows as Behaviour authority | Stale private state | Reference evidence/ids only; no mission ORM |
| Confidence/Behaviour conflation | Self-report as habit truth | Exclude confidence types from primary set |
| Parallel analytics engagement formula | Second truth | No service forks in this capability |
| V1/V2 mistaken exemption | Invented topic trees | Never invent `topic_id`; optional tags only when present |

---

# 13. Acceptance criteria

Capability 2.5 structural implementation is accepted when all of the following hold:

1. **`BehaviourUpdateStrategy` exists** as framework-free domain code under `app/domain/twin/strategies/`.  
2. **Primary evidence types** in §5.2 are supported without requiring `topic_id`.  
3. **`apply` is structural only** — lineage + `last_updated` + preserve `consistency_metrics`; no scoring.  
4. **Immutability** — new Twin snapshot; input Twin unchanged.  
5. **Idempotent dedupe** of session/evidence id appends.  
6. **Registration order** Knowledge → Memory → Behaviour documented and tested.  
7. **Ownership isolation** — mission-only does not change Knowledge/Memory; Behaviour does not claim revision/quiz primary types.  
8. **Public exports** updated (`BEHAVIOUR_EVIDENCE_TYPES`, `BehaviourUpdateStrategy`).  
9. **README** documents Behaviour strategy purpose, non-goals, and pipeline position.  
10. **Tests green** for Behaviour + Knowledge + Memory strategy suites; ruff clean on touched paths.  
11. **No migrations, no Flask/service/UI changes** in the Capability 2.5 PR unless an unforeseen blocker is explicitly approved.  
12. **Hard educational rule** remains true: Behaviour never grants/revokes mastery.

---

# 14. Definition of Done

A Capability 2.5 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; out-of-scope items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] Domain additions match §4 decision (id-list-first; additive `evidence_ids` if chosen)  
- [ ] Strategy follows §5 structural rules and primary ownership  
- [ ] Pipeline integration matches §6 order without hard-coding the pipeline class  
- [ ] Evidence ownership matches §7  
- [ ] Public API impact is additive only (§8)  
- [ ] Testing strategy §9 executed and green  
- [ ] Migration impact is None (§10) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §11 hold (especially V1/V2 and Knowledge/Memory complementarity)  
- [ ] Acceptance criteria §13 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No scoring formulas, Decision Engine, Readiness, or Performance strategy shipped under this capability label  

**Stop after Capability 2.5 structural ship + review.** Do not start Capability 2.6 in the same change set unless separately requested.

---

# 15. Recommended implementation sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read Domain Analysis + Update Strategy architecture + this plan | Shared understanding; Choice A vs B confirmed (default A) |
| **1** | Decide additive model: id-list-only ± `evidence_ids` (recommended: add `evidence_ids`) | Written decision in PR description |
| **2** | If adding `evidence_ids`, extend `BehaviourState` / `create()` additively | Existing Behaviour construction still works |
| **3** | Implement `behaviour_update_strategy.py` (`name`, `supports`, `apply`, frozenset, helpers) | Module imports cleanly; framework-free |
| **4** | Export from `strategies/__init__.py` and `twin/__init__.py` | `from app.domain.twin import BehaviourUpdateStrategy` works |
| **5** | Update `app/domain/twin/README.md` | Behaviour section + registration diagram |
| **6** | Write `tests/test_behaviour_update_strategy.py` (supports, apply, ownership, pipeline, purity) | Focused suite green |
| **7** | Run Knowledge + Memory regression + ruff | No regressions |
| **8** | Capability review against acceptance criteria §13 | Checklist complete |
| **9** | Completion report + stop | Do not start 2.6 |

### Suggested PR shape

- **Title:** `feat: structural BehaviourUpdateStrategy for Twin pipeline`  
- **Body:** link this plan + architecture docs; state Choice A (primary-only); migration None; V1/V2 N/A for traversal; note deferred secondary types and scoring  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): execute §15 steps 1–9 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Host aggregate and registration shell (unchanged algorithms) |
| 2.3–2.4 | Knowledge / Memory strategies | Structural precedents and registration predecessors |
| **2.5** | **Behaviour Update Strategy** | **This implementation plan** |
| 2.5.1 / 2.5.2 | Domain analysis + update strategy architecture | Approved inputs to this plan |
| 2.6 | Performance | Distinct assessment domain; register later |
| 2.7–2.10 | Readiness / Decision / Recommendation / Missions | Read Behaviour; write back only via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.5.3 — Behaviour Update Strategy Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; no traversal changes planned |
| Application code intentionally untouched | Yes (this milestone) |
| Preceded by | Behaviour Domain Analysis + Behaviour Update Strategy Architecture (approved) |
| Next | Structural `BehaviourUpdateStrategy` implementation → tests → capability review |

---

*End of Capability 2.5.3 Behaviour Update Strategy Implementation Plan.*
