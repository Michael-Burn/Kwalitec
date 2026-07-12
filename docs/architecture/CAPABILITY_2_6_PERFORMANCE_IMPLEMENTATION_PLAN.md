# Capability 2.6.3 — Performance Update Strategy Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.6 Performance Update Strategy (structural implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Domain charter:** [`CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md`](CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md)  
**Update strategy architecture:** [`CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md`](CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md)  
**Precedents:** Capability 2.3 `KnowledgeUpdateStrategy`, Capability 2.4 `MemoryUpdateStrategy`, Capability 2.5 `BehaviourUpdateStrategy`  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`), [`CAPABILITY_2_5_BEHAVIOUR_IMPLEMENTATION_PLAN.md`](CAPABILITY_2_5_BEHAVIOUR_IMPLEMENTATION_PLAN.md)  
**Scope:** Plan the structural write-path implementation of `PerformanceUpdateStrategy` — **no code, tests, migrations, services, or scoring formulas in this document’s milestone**

---

## Document purpose

This plan translates the approved Performance domain analysis and update-strategy architecture into a concrete, executable implementation sequence for Capability 2.6.

It answers:

1. What is in / out of scope for the first Performance strategy ship  
2. Which files to create and modify  
3. Which domain model additions are required vs deferred  
4. How strategy behaviour, lineage, and immutability must work  
5. How to register Performance after Knowledge → Memory → Behaviour  
6. How to test, migrate (or not), and accept the work  

**Hard educational rules (binding):**

1. Performance never becomes a second Knowledge mastery store.  
2. High mission adherence never invents strong Performance.  
3. A single mock never becomes the whole readiness or pass-probability story.  
4. Self-reported confidence never overrides dense contrary Performance evidence in educational narrative.

**Governing principle:** Assessment trends are not session activity; Performance is not a second mastery store; a single mock is not the whole readiness story.  
**Structural discipline:** Structure first, beliefs later — mirror Knowledge/Memory/Behaviour.

**Non-goals of this document**

- Implementing `PerformanceUpdateStrategy` or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Concrete accuracy / IRT / partial-credit / pass-probability formulas  
- UI, gamification, notifications, Readiness, Decision Engine, or Mission Generation changes  

---

# 1. Implementation scope

## 1.1 In scope (Capability 2.6 structural ship)

| Item | Intent |
|---|---|
| **`PerformanceUpdateStrategy`** | New `BaseUpdateStrategy` subclass; framework-free; immutable Twin snapshots |
| **Primary evidence `supports` set** | Quiz / mock / past paper / diagnostic / post-exam outcomes |
| **Structural `apply` rules** | Append `assessment_ids` (deduped); create/extend scoped `performance_summaries`; set `last_updated`; preserve unknown summary facts |
| **Optional additive lineage** | Prefer optional state-level `evidence_ids` and optional summary condition / evidence tags if needed for audit parity |
| **Pipeline registration exports** | Re-export strategy + type frozenset from `strategies` and `twin` packages |
| **Domain README update** | Document Performance strategy alongside Knowledge/Memory/Behaviour |
| **Focused unit + pipeline tests** | Mirror Knowledge / Memory / Behaviour strategy harnesses |

## 1.2 Explicitly deferred

| Item | Why deferred |
|---|---|
| Accuracy / strength / IRT / partial-credit scoring | Structural phase only; fill summary bags later |
| Mistake taxonomy beliefs | Derived Performance enrichment |
| Exam-condition vs formative delta scores | Derived; structural tags only when evidence supplies them |
| Pass probability / readiness composites | Predictions / Readiness Aggregation (Capability 2.7+) |
| Belief-enrichment reorder (Performance before Knowledge) | Not required for structural 2.6; dedicated architecture note if/when both compute beliefs |
| Secondary weak updates (question attempts; incomplete abandons) | Documented optional; default first ship is primary-only — see §5 |
| Confidence calibration ownership | Confidence remains separable; Performance supplies measured pole only |
| Readiness Aggregation / Decision Engine / Mission Generation | Capabilities 2.7–2.10 (read Performance; do not write it) |
| Persistence, ORM, Alembic, HTTP, Flask services | Domain layer only; no Twin DB in this capability |
| Curriculum Engine / V1–V2 traversal changes | Performance must not invent syllabus |
| Hard-coding Performance inside `TwinUpdatePipeline` | Pipeline remains a registration shell |

## 1.3 Success shape

After implementation:

```
Learning Evidence (Performance-primary types)
      → UpdateContext
            → TwinUpdatePipeline
                  → KnowledgeUpdateStrategy (if supports)
                  → MemoryUpdateStrategy (if supports)
                  → BehaviourUpdateStrategy (if supports)
                  → PerformanceUpdateStrategy (if supports)
                        → new PerformanceState in new DigitalTwin snapshot
```

Same Twin + same ordered evidence batch → same structural Performance outcome. No scoring. No Flask. No migrations.

---

# 2. Files to Create

| Path | Role |
|---|---|
| `app/domain/twin/strategies/performance_update_strategy.py` | `PerformanceUpdateStrategy` + `PERFORMANCE_EVIDENCE_TYPES` (primary set; optional secondary frozenset if Choice B) |
| `tests/test_performance_update_strategy.py` | Unit + pipeline + ownership + fidelity tests mirroring Knowledge/Memory/Behaviour harnesses |

Do **not** create: services, blueprints, migrations, scoring modules, a separate Performance engine package, or nested gradebook stores outside `PerformanceState`.

---

# 3. Files to Modify

| Path | Why it must change |
|---|---|
| `app/domain/twin/strategies/__init__.py` | Import/export `PerformanceUpdateStrategy`, `PERFORMANCE_EVIDENCE_TYPES`; update package docstring so the strategies package advertises Performance as shipped |
| `app/domain/twin/__init__.py` | Re-export Performance strategy symbols in `__all__` for the public Twin domain surface |
| `app/domain/twin/README.md` | Document Performance Update Strategy purpose, non-goals, ownership, and registration order Knowledge → Memory → Behaviour → Performance |
| `app/domain/twin/performance_state.py` | **Only if** additive fields are chosen (§4): e.g. optional `evidence_ids` on state; optional condition / evidence tags on `PerformanceSummary`; keep existing fields and `create()` backwards-compatible |
| `app/domain/twin/strategies/base_strategy.py` | Docstring mention only if needed (already anticipates `PerformanceUpdateStrategy`) |
| Existing Knowledge/Memory/Behaviour strategy tests (optional) | Add one mixed-batch / registration-order assertion that includes Performance if those suites already assert full pipeline composition — prefer keeping Performance assertions in the new test module |

**Do not modify (this capability)**

- `app/domain/twin/update_pipeline.py` algorithm (registration API already sufficient)  
- Knowledge / Memory / Behaviour strategy ownership frozensets (except confirming they still do not absorb Performance-primary post-exam as Behaviour; already true)  
- Services, blueprints, templates, models, Alembic  
- Evidence catalogue enum unless a missing type blocks the primary set (current `EvidenceType` already covers the primary set)  
- Curriculum JSON / engine traversal  

---

# 4. Domain Model Changes

## 4.1 Existing contract (keep)

`PerformanceState` already ships structural slots:

| Field | Strategy duty |
|---|---|
| `assessment_ids` | Append deduped assessment / attempt evidence ids when applicable |
| `performance_summaries` | Create or merge by `scope_id`; preserve unknown `summary` bag keys/values |
| `last_updated` | Set to latest processed applicable evidence timestamp |

`PerformanceSummary` already provides `scope_id` + `summary` facts bag.  
`DigitalTwin` already composes `performance: PerformanceState`. No aggregate redesign.

## 4.2 Recommended additive changes (structural ship only)

| Addition | Recommendation | Rationale |
|---|---|---|
| **`evidence_ids: tuple[str, ...]` on `PerformanceState`** | **Yes — additive optional default `()`** | Parity with Knowledge/Behaviour lineage; audit of applied Performance evidence; architecture allows state-level evidence ids |
| **Optional condition tag on `PerformanceSummary`** | **Optional — only if evidence already carries formative / exam-condition / diagnostic / incomplete metadata that should not live inside the opaque `summary` bag alone** | Prefer additive optional field over inventing scoring; if deferred, store condition keys inside `summary` when supplied by evidence |
| **Optional per-scope `evidence_ids` on `PerformanceSummary`** | **Optional — prefer state-level `evidence_ids` first** | Nested scope provenance can wait unless contradiction-aware tests need it in the first ship |
| **Belief/scoring fields** | **No** | Accuracy trends, strength scores, IRT, pass probability remain deferred |

If `evidence_ids` is added:

- Update `PerformanceState.create(...)` with a defaulted parameter  
- Defensive copy to tuple  
- Preserve frozen dataclass immutability  
- Do not rename or remove existing fields  

## 4.3 Scope identity extraction

`LearningEvidence` may carry `topic_id` and payload keys. Structural strategy should resolve `scope_id` deterministically from, in priority order to be fixed in implementation and documented in the strategy module:

1. Explicit payload / metadata keys when present (e.g. `assessment_id`, `scope_id`, quiz/mock instance id)  
2. Else non-empty `topic_id` for topic-scoped summaries (curriculum identity required)  
3. Else assessment-instance scope from `originating_event_id` when non-empty  
4. Else append assessment / evidence reference only (weak lineage) — **do not fabricate** a topic summary  

Never invent syllabus topics. Assessment-instance scopes may exist without `topic_id`. Topic-scoped summaries require curriculum identity on evidence.

## 4.4 What must not be added now

- Mutable accuracy counters or mastery-like belief fields  
- Parallel quiz-service gradebook inside Performance  
- `retention_belief` / `mastery_belief` / Behaviour adherence metrics  
- Readiness composites or Decision State fields  
- Required V2 section fields that would break flat V1 curricula  

---

# 5. Strategy Behaviour

## 5.1 Class contract (match Knowledge/Memory/Behaviour)

```
PerformanceUpdateStrategy(BaseUpdateStrategy)
  name → "performance_update"          # stable UpdateResult audit id
  supports(context) → bool
  apply(context) → DigitalTwin         # new snapshot; never mutate input
```

Export:

```
PERFORMANCE_EVIDENCE_TYPES: frozenset[EvidenceType]   # primary (required)
# Optional if secondary weak updates ship in same PR:
# PERFORMANCE_SECONDARY_EVIDENCE_TYPES: frozenset[EvidenceType]
```

## 5.2 Supported evidence (primary — must implement)

Map architecture §5.3 onto existing `EvidenceType` members:

| Architecture concept | `EvidenceType` |
|---|---|
| Quiz outcome | `QUIZ_COMPLETED` |
| Mock / timed mock outcome | `MOCK_EXAM` |
| Past-paper outcome | `PAST_PAPER_ATTEMPT` |
| Diagnostic assessment outcome | `DIAGNOSTIC_ASSESSMENT` |
| Post-exam outcome | `POST_EXAM_OUTCOME` |

**`supports` rule:** at least one evidence item whose `evidence_type` is in `PERFORMANCE_EVIDENCE_TYPES`.  
**Topic requirement:** do **not** require `topic_id` for all primary types — assessment-instance and post-exam scopes may apply without topic mapping. Topic-scoped *summaries* still require curriculum identity when creating a topic `scope_id`.

## 5.3 Ignored evidence (must not own)

| Evidence type / class | Owner | Performance action |
|---|---|---|
| `REVISION_SESSION` / `FLASHCARD_REVIEW` | Memory primary | Ignore (no `supports`) |
| `MISSION_COMPLETED` / `MISSION_MISSED` / time-on-task / study break / study session | Behaviour primary | Ignore in primary set |
| `CONFIDENCE_RATING` / `READINESS_REVIEW` | Confidence primary | Ignore |
| `RECOMMENDATION_DECISION` | Decision State primary | Ignore |
| Plan / goal changes | Goals / Planning | Ignore — do not erase Performance history |
| Dashboard views / coach narration / cosmetic badges | Non-events | Not catalogue ownership for Performance |

## 5.4 Secondary evidence (implementation choice)

Architecture allows optional weak updates. This plan recommends:

| Choice | Decision for first ship |
|---|---|
| **A — Primary only (recommended)** | Ship primary set only; document secondary as follow-up. Keeps ownership clearest vs Knowledge for question attempts and vs Behaviour for abandons. |
| **B — Primary + documented secondary** | Also append weak assessment references for `QUESTION_ATTEMPT` / `QUESTION_CORRECT` / `QUESTION_INCORRECT`, and incomplete Performance signal for assessment-abandon cases — **without** stealing Knowledge or Behaviour primary ownership |

If Choice B is taken, secondary must:

- Only append ids / incomplete-tagged lineage  
- Never invent full-mock strength from partial attempts  
- Never compute accuracy engines  
- Never mutate Knowledge/Memory/Behaviour  
- Be listed explicitly in frozensets and tests  

**Default recommendation: Choice A.**

## 5.5 Lineage updates

1. Filter applicable evidence (primary; + secondary if Choice B).  
2. Append deduped assessment / attempt references to `assessment_ids` (prefer assessment instance id when present; else `evidence_id`).  
3. If state-level `evidence_ids` exists, append deduped `evidence.evidence_id`.  
4. For each applicable item with a usable `scope_id`, create or merge `PerformanceSummary` by identity.  
5. Merge into existing scope: defensive-copy `summary` bag; overlay only facts **supplied** by evidence; preserve unknown keys.  
6. When evidence carries condition metadata (formative / exam-condition / diagnostic / incomplete), store as structural fact/tag — do not narrate formative as exam-condition.  
7. Do not invent scopes from free text.

## 5.6 Timestamp updates

Set `PerformanceState.last_updated` to the latest processed applicable evidence timestamp (max of existing `last_updated` and applicable item timestamps). Do not invent timestamps for non-applicable evidence.

## 5.7 Immutable snapshot behaviour

1. Never mutate the input `DigitalTwin`, `PerformanceState`, or nested `PerformanceSummary` instances.  
2. Build new `PerformanceState` via `create(...)`.  
3. Return `DigitalTwin.create(...)` copying all other domains by reference from the input Twin, replacing only `performance`.  
4. Pipeline chains via `context.with_twin(...)` so later strategies (none after Performance in structural phase) see the new snapshot.

## 5.8 Explicit non-computations

Must **not**:

- Compute accuracy trends, strength scores, or IRT / partial-credit models  
- Emit readiness composites or pass probabilities  
- Grant/revoke Knowledge mastery or Memory retention beliefs  
- Absorb Behaviour adherence into “study quality” Performance  
- Select recommendations or generate missions  
- Persist Twin or evidence  
- Import Flask / SQLAlchemy / request globals  
- Fabricate High Performance from Goals, Behaviour, or empty cold start  

## 5.9 Idempotence and determinism

- Dedupe id appends on replay of the same evidence id  
- Scope merge by `scope_id` must be deterministic for the same Twin + ordered batch  
- Same Twin + same ordered evidence batch → same structural Performance outcome  
- No network / LLM on the write path  

---

# 6. Pipeline Registration

## 6.1 Registration order (structural phase — locked)

| Order | Strategy | Status |
|---|---|---|
| 1 | `KnowledgeUpdateStrategy` | Existing |
| 2 | `MemoryUpdateStrategy` | Existing |
| 3 | `BehaviourUpdateStrategy` | Existing |
| 4 | `PerformanceUpdateStrategy` | This capability |

```
Knowledge → Memory → Behaviour → Performance
```

Rationale (from approved architecture):

1. Preserves shipped Knowledge → Memory → Behaviour order.  
2. Structural Performance does not require prior Behaviour mutation to be correct; dual updates on mixed batches remain valid once order is fixed.  
3. Mixed batches stay reproducible when order is fixed and documented.  
4. Knowledge already receives assessment evidence independently; structural Performance need not precede Knowledge to materialise summaries.

**Belief-enrichment caveat (deferred):** if later both Knowledge and Performance compute beliefs, ordering may need Performance before Knowledge. That reorder is **not** part of structural Capability 2.6 and must not be done silently.

## 6.2 Integration mechanics (no hard-coded ordering)

- Callers construct  
  `TwinUpdatePipeline([KnowledgeUpdateStrategy(), MemoryUpdateStrategy(), BehaviourUpdateStrategy(), PerformanceUpdateStrategy()])`  
  **or** `register` in that order.  
- Pipeline class must **not** hard-code Performance algorithms or import Performance by default inside `update_pipeline.py`.  
- Composition remains registration-based — same extension point as Knowledge/Memory/Behaviour.  
- Each `apply` receives context whose Twin reflects prior strategies.  
- `UpdateResult.applied_strategies` must include `"performance_update"` when Performance ran.  
- Empty strategy list remains a valid no-op success (existing pipeline semantics).

## 6.3 Mixed-batch expectations

| Batch shape | Expected strategies |
|---|---|
| Quiz / mock / diagnostic only | Knowledge + Performance (topic-scoped Knowledge when `topic_id` present) |
| Post-exam only | Performance primary; Knowledge only if Knowledge `supports` still matches (may be no-op if topic missing) |
| Revision only | Memory; Performance no-op |
| Mission completed only | Behaviour; Performance no-op |
| Mission completed + embedded quiz | Knowledge + Behaviour + Performance |
| Abandoned mid-mock | Behaviour (abandon); Performance incomplete signal only if Choice B — Choice A: Behaviour only unless abandon is typed as primary assessment outcome |
| Flashcard + quiz | Memory + Knowledge + Performance |

Mission completion must not overwrite or replace quiz-driven Knowledge/Performance updates.

## 6.4 Decision Engine loop (read-side note only)

Assessment outcomes and accept/dismiss/complete events become Learning Evidence and re-enter this pipeline. Decision Engine must not mutate Performance in place. No Decision Engine code changes in Capability 2.6.

---

# 7. Public API Impact

## 7.1 New exports (additive)

From `app.domain.twin` / `app.domain.twin.strategies`:

| Symbol | Kind |
|---|---|
| `PerformanceUpdateStrategy` | Class |
| `PERFORMANCE_EVIDENCE_TYPES` | `frozenset[EvidenceType]` |

If `PerformanceState.evidence_ids` is added, it is a **backwards-compatible additive field** with default empty tuple — existing `PerformanceState.create()` call sites remain valid.

## 7.2 Unchanged interfaces

| Contract | Impact |
|---|---|
| `TwinUpdatePipeline` constructor / `register` / `process` | Unchanged API; callers opt in by registering Performance |
| `UpdateContext` / `UpdateResult` | Unchanged |
| `BaseUpdateStrategy` | Unchanged |
| `LearningEvidence` / `EvidenceType` | Unchanged (types already exist) |
| `KnowledgeUpdateStrategy` / `MemoryUpdateStrategy` / `BehaviourUpdateStrategy` | Unchanged contracts and frozensets |
| HTTP / Flask / services | No public product API change |
| ORM / Alembic | None |

## 7.3 Backwards compatibility (API)

- Existing callers that register only Knowledge → Memory → Behaviour continue to work; Performance is additive registration.  
- Empty `PerformanceState` remains a valid cold start.  
- Prefer optional defaults; no breaking renames of `PerformanceState` / `PerformanceSummary` fields.  
- Twin pipeline composition remains open for extension via registration — no required hard-coded Performance import in the pipeline class.

---

# 8. Testing Strategy

Target coverage equivalent to `KnowledgeUpdateStrategy`, `MemoryUpdateStrategy`, and `BehaviourUpdateStrategy`.

## 8.1 New module

`tests/test_performance_update_strategy.py`:

| Suite | Assertions |
|---|---|
| **Contract** | Subclasses `BaseUpdateStrategy`; `name == "performance_update"` |
| **supports (primary)** | True for quiz / mock / past paper / diagnostic / post-exam; False for revision-only, mission-only, confidence-only, empty batch |
| **Topic optional for supports** | Assessment-instance / post-exam without `topic_id` still supports when primary-typed |
| **Scoped summaries** | Topic-scoped summary requires curriculum identity; assessment-instance scope without topic is allowed; no fabricated scopes from free text |
| **Structural apply** | Appends `assessment_ids`; creates/merges summaries; sets `last_updated`; preserves unknown summary keys |
| **Idempotence** | Replaying same evidence id does not duplicate assessment / evidence ids |
| **Immutability** | Input Twin / PerformanceState unchanged after `apply` |
| **Non-scoring** | No accuracy / strength / pass-probability computation; summary bags not invented |
| **Cross-domain isolation** | Quiz-only leaves Behaviour unchanged (except if Behaviour secondary — not in Performance tests); mission-only does not run Performance; revision-only does not run Performance; Knowledge/Memory/Behaviour structural fields untouched by Performance apply |
| **Ownership boundary** | Performance does not write `mastery_belief` / retention clocks / Behaviour metrics |
| **Pipeline integration** | Knowledge → Memory → Behaviour → Performance registration; mixed mission+quiz applies expected strategies in order; `applied_strategies` contains `"performance_update"` when applicable |
| **Educational fidelity** | Mission completion alone does not invent Performance; formative condition tags (if present) are not upgraded to exam-condition strength; cold start stays empty; incomplete invent-full-mock forbidden |
| **Framework purity** | AST / import ban for Flask/SQLAlchemy (same pattern as sibling strategy tests) |
| **Determinism** | Same inputs → equal Performance structural fields |

## 8.2 Pipeline integration tests

Within the same module (or shared helpers already used by Behaviour tests):

- Register all four strategies; process mixed batches; assert order of `applied_strategies` when multiple `supports` are true.  
- Assert Knowledge quiz updates and Performance quiz updates both apply without either absorbing the other’s state.  
- Assert Behaviour mission lineage and Performance quiz lineage remain distinct on mission+quiz batches.

## 8.3 Ownership boundary tests

- Performance primary types are not claimed as Behaviour-primary.  
- Memory revision types do not `supports` Performance.  
- Post-exam is Performance-primary; Behaviour must not absorb it.  
- Question attempts remain Knowledge-primary; if Choice A, Performance ignores them.

## 8.4 Educational fidelity tests

- Empty Performance remains empty after Behaviour-only evidence.  
- No fabricated High Performance from Goals or empty cold start.  
- Contradictory scoped facts remain visible as separate scopes or preserved bags — no silent average score.  
- Abandoned / incomplete invent-full-mock strength is forbidden (especially if Choice B ships).

## 8.5 Regression

- Existing `tests/test_knowledge_update_strategy.py`, `tests/test_memory_update_strategy.py`, and `tests/test_behaviour_update_strategy.py` must remain green.  
- No curriculum V1/V2 engine test changes expected.  
- Run:  
  `python -m pytest tests/test_performance_update_strategy.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py tests/test_behaviour_update_strategy.py -v`  
  and `ruff check app/ tests/`

## 8.6 Out of test scope for this capability

- HTTP integration  
- Persistence round-trips  
- Scoring correctness / IRT  
- Readiness Aggregation numeric weights  
- Decision Engine assessment-shaped selection  
- Belief-enrichment reorder (Performance before Knowledge)  

---

# 9. Migration Impact

| Concern | Impact |
|---|---|
| Database changes | **None** |
| Alembic migrations | **None** |
| ORM / model changes | **None** |
| Persistence changes | **None** |
| Evidence catalogue DB | **None** |
| Curriculum JSON | **None** |
| Data backfill | **None** |

Twin domain remains in-memory / framework-free. If a later persistence milestone stores Twin snapshots, additive `evidence_ids` on Performance would require a separate schema plan then — not now.

**Expected answer for this capability: None.**

---

# 10. Backwards Compatibility

| Invariant | Confirmation |
|---|---|
| **Knowledge unaffected** | Knowledge strategy contract and frozenset unchanged; Performance does not write mastery |
| **Memory unaffected** | Memory strategy contract unchanged; Performance does not write retention |
| **Behaviour unaffected** | Behaviour strategy contract unchanged; Performance does not write adherence / session metrics |
| **Twin pipeline remains compatible** | Registration API unchanged; Performance is additive; Knowledge → Memory → Behaviour callers keep working |
| **Curriculum V1/V2 unaffected** | No traversal changes; Performance must not invent syllabus or require Sections globally |
| Empty `PerformanceState` cold start | Remains valid |
| Additive fields only | Prefer optional defaults; no breaking renames |
| Evidence append-only semantics | Preserved |
| Deterministic cores | No LLM/network on write path |

Cold start: empty `assessment_ids` / summaries remain valid. Downstream consumers must treat missing Performance as explicit low assessment confidence — strategy must not invent “High Performance” defaults.

---

# 11. Risks

| Risk | Impact | Mitigation in implementation |
|---|---|---|
| **Ownership overlap** | Performance steals Knowledge attempt ownership or Behaviour mission ownership | Primary-only default; frozenset review; ownership tests |
| **Evidence leakage** | Revision / confidence / recommendation evidence updates Performance | Explicit ignore set; supports tests for non-events |
| **Accidental scoring** | Accuracy / IRT / pass probability sneak into structural ship | Non-scoring tests; preserve unknown summary bags only |
| **Registration-order coupling** | Hard-coded order inside pipeline class; non-reproducible mixed batches | Register only; lock Knowledge → Memory → Behaviour → Performance in docs + tests |
| **Performance becoming a mastery store** | Domain collapse into Knowledge | Separate `PerformanceState`; never write `mastery_belief`; fidelity tests |
| **Mission completion as Performance** | Activity theatre replaces assessed learning | Mission-only must not `supports` Performance |
| **Single-mock overclaim** | False readiness narrative | Structural phase stores lineage only; no readiness emission |
| **Partial attempts as full mocks** | Misleading exam-condition beliefs | Choice A avoids abandon secondary; Choice B requires incomplete tags only |
| **Invented topic scopes** | Syllabus invention / V1–V2 breakage | Curriculum identity mandatory for topic scopes; nullable sections |
| **Silent belief-phase reorder** | Non-auditable update differences | Defer Performance-before-Knowledge to dedicated architecture note |
| **In-place Twin mutation** | Broken snapshot audit | Frozen dataclasses; immutability tests |
| **Parallel Performance stores in quiz services** | Divergent learner state | Evidence → strategy → Twin only; no service forks in this capability |
| **Post-exam erasure of history** | Broken calibration / audit | Append-only lineage; preserve prior mock summaries |
| **Confidence conflation** | Self-report treated as measured accuracy | Exclude confidence types from primary set |

---

# 12. Educational Fidelity Review

Verify the following remain true after structural implementation:

| Fidelity check | Required outcome |
|---|---|
| **Performance never changes mastery** | `apply` replaces only `performance`; Knowledge `mastery_belief` / topic records unchanged by Performance |
| **Performance never changes memory** | Memory retention slots / `last_reinforced` unchanged by Performance |
| **Performance never computes readiness** | No readiness composite, pass probability, or weighted preparedness score in strategy |
| **Performance only records assessment-conditioned educational beliefs (structural)** | Assessment lineage + scoped summary facts/tags from evidence; unknown bags preserved; no invented High Performance |
| **Condition honesty** | Formative success is not stored/narrated as exam-condition strength |
| **Activity ≠ assessed competence** | Mission completion alone does not create Performance strength |
| **Uncertainty honesty** | Cold start / sparse assessment remains empty or sparse — never fabricated readiness |
| **Explainability spine** | Structural facts remain evidence-linked via ids for later Readiness/Decision narration |

Keeping Performance distinct from Knowledge and Behaviour is itself an educational fidelity mechanism: assessment trends stay visible, and activity/mastery cannot silently substitute for assessed outcomes.

---

# 13. Acceptance Criteria

Capability 2.6 structural implementation is accepted when all of the following hold:

1. **`PerformanceUpdateStrategy` exists** as framework-free domain code under `app/domain/twin/strategies/`.  
2. **Primary evidence types** in §5.2 are supported; topic is not universally required for `supports`.  
3. **`apply` is structural only** — assessment lineage + scoped summaries + `last_updated` + preserve unknown summary facts; no scoring.  
4. **Immutability** — new Twin snapshot; input Twin unchanged.  
5. **Idempotent dedupe** of assessment / evidence id appends; deterministic scope merge.  
6. **Registration order** Knowledge → Memory → Behaviour → Performance documented and tested via registration composition (not hard-coded in the pipeline class).  
7. **Ownership isolation** — mission/revision/confidence-only batches do not run Performance; Performance does not mutate Knowledge/Memory/Behaviour.  
8. **Public exports** updated (`PERFORMANCE_EVIDENCE_TYPES`, `PerformanceUpdateStrategy`).  
9. **README** documents Performance strategy purpose, non-goals, and pipeline position.  
10. **Tests green** for Performance + Knowledge + Memory + Behaviour strategy suites; ruff clean on touched paths.  
11. **No migrations, no Flask/service/UI changes** in the Capability 2.6 PR unless an unforeseen blocker is explicitly approved.  
12. **Hard educational rules** remain true: Performance is not a second mastery store; missions do not invent Performance; no readiness emission; Confidence types excluded.  
13. **Curriculum V1/V2** remain loadable; Performance does not invent syllabus or require Sections globally.

---

# 14. Definition of Done

A Capability 2.6 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; out-of-scope items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] Domain additions match §4 decision (additive `evidence_ids` recommended; no scoring fields)  
- [ ] Strategy follows §5 structural rules and primary ownership (Choice A default)  
- [ ] Pipeline integration matches §6 order without hard-coding the pipeline class  
- [ ] Public API impact is additive only (§7)  
- [ ] Testing strategy §8 executed and green (unit, pipeline, ownership, fidelity)  
- [ ] Migration impact is None (§9) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §10 hold (Knowledge/Memory/Behaviour/Twin/V1–V2)  
- [ ] Educational fidelity review §12 verified by tests and review  
- [ ] Acceptance criteria §13 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No scoring formulas, Decision Engine, Readiness, Confidence strategy, or belief-enrichment reorder shipped under this capability label  

**Stop after Capability 2.6 structural ship + review.** Do not start Capability 2.7 in the same change set unless separately requested.

---

# 15. Recommended Implementation Sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read Domain Analysis + Update Strategy architecture + this plan | Shared understanding; Choice A vs B confirmed (default A) |
| **1** | Decide additive model: ± `evidence_ids` on `PerformanceState`; condition tags placement (summary bag vs optional field) | Written decision in PR description |
| **2** | If adding `evidence_ids` (recommended), extend `PerformanceState` / `create()` additively | Existing Performance construction still works |
| **3** | Implement `performance_update_strategy.py` (`name`, `supports`, `apply`, frozenset, scope helpers) | Module imports cleanly; framework-free |
| **4** | Export from `strategies/__init__.py` and `twin/__init__.py` | `from app.domain.twin import PerformanceUpdateStrategy` works |
| **5** | Update `app/domain/twin/README.md` | Performance section + registration diagram Knowledge → Memory → Behaviour → Performance |
| **6** | Write `tests/test_performance_update_strategy.py` (supports, apply, ownership, pipeline, fidelity, purity) | Focused suite green |
| **7** | Run Knowledge + Memory + Behaviour regression + ruff | No regressions |
| **8** | Capability review against acceptance criteria §13 and fidelity §12 | Checklist complete |
| **9** | Completion report + stop | Do not start 2.7 |

### Suggested PR shape

- **Title:** `feat: structural PerformanceUpdateStrategy for Twin pipeline`  
- **Body:** link this plan + architecture docs; state Choice A (primary-only); migration None; V1/V2 N/A for traversal; note deferred secondary types, scoring, and belief-enrichment reorder  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): execute §15 steps 1–9 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Host aggregate and registration shell (unchanged algorithms) |
| 2.3–2.5 | Knowledge / Memory / Behaviour strategies | Structural precedents and registration predecessors |
| **2.6** | **Performance Update Strategy** | **This implementation plan** |
| 2.6.1 / 2.6.2 | Domain analysis + update strategy architecture | Approved inputs to this plan |
| 2.7 | Readiness | Consumes Performance as assessment strength/weakness factor — not in this ship |
| 2.8–2.10 | Decision / Recommendation / Missions | Read Performance; write back only via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.6.3 — Performance Update Strategy Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; no traversal changes planned |
| Application code intentionally untouched | Yes (this milestone) |
| Preceded by | Performance Domain Analysis + Performance Update Strategy Architecture (approved) |
| Next | Structural `PerformanceUpdateStrategy` implementation → tests → capability review |

---

*End of Capability 2.6.3 Performance Update Strategy Implementation Plan.*
