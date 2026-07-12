# Capability 2.7.3 — Readiness Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.7 Readiness Aggregation (structural read-side implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md)  
**Aggregation architecture:** [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md)  
**Gate:** Epic 2 Midpoint Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](../reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md))  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`), [`knowledge/subsystems/readiness.md`](../../knowledge/subsystems/readiness.md), Capability 2.5 / 2.6 implementation plans  
**Scope:** Plan the first structural **read-side** ship of Readiness Aggregation — **no code, tests, migrations, services, or scoring formulas in this document’s milestone**

---

## Document purpose

This plan translates the approved Readiness educational analysis and aggregation architecture into a concrete, executable implementation sequence for Capability 2.7.

It answers:

1. What is in / out of scope for the first Readiness Aggregation ship  
2. Which files to create and modify  
3. How `ReadinessState` must be represented  
4. How aggregation flow, factor contracts, warrant, and cold start must work  
5. Public API, testing, migration, compatibility, fidelity, and acceptance gates  

**Hard architectural rules (binding):**

1. Readiness Aggregation never writes Learning Evidence.  
2. Readiness Aggregation never mutates Twin belief domains.  
3. Readiness Aggregation never invents preparedness from absence.  
4. Readiness Aggregation never selects next actions or generates missions.  
5. Every overall readiness claim must decompose into named factors with explicit Evidence Warrant.  
6. Curriculum V1 and V2 remain loadable; weights and order come only from canonical Curriculum helpers (via a domain-safe context object — not via Flask-coupled service imports inside aggregation).

**Governing principle:** Readiness is derived, factorable, and honest under uncertainty — not a write-side belief store and not a next-action engine.  
**Structural discipline:** Structure and honesty first; numeric composites and pass probability later.

**Non-goals of this document**

- Implementing aggregation or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Concrete readiness weights, averages, composites, pass-probability formulas, or Bayesian math  
- UI, analytics cutover, gamification, notifications, Decision Engine, Recommendation Engine, or Mission Generation changes  
- Refactoring or deleting legacy `ReadinessService`  

---

# 1. Scope of implementation

## 1.1 In scope (Capability 2.7 structural ship)

| Item | Intent |
|---|---|
| **`ReadinessState` + factor judgement types** | Immutable, framework-free derived judgement objects — not Twin write-domain peers |
| **Factor identity catalogue** | Stable names for the seven architectural factors (§6) |
| **Posture / unknown vocabulary (structural)** | Explicit postures: unknown / low-warrant / risk-elevating / supportive / not-applicable — **no numeric scores** |
| **`ReadinessAggregation.derive(...)`** | Pure read-side function/class: Twin snapshot + Curriculum context + Goals scope → `ReadinessState` |
| **Attributions + lineage hooks** | Per-factor citations to Twin domains, Curriculum weight context, and evidence ids when available |
| **Evidence Warrant propagation** | Per-factor and overall warrant; overall assertiveness constrained by sparse critical inputs |
| **Cold-start / unknown contracts** | Goals-only and empty-domain Twins yield not-yet-knowable overall posture — never Mid/High fabrication |
| **Confidence omission (v1)** | Self-report Confidence and Knowledge-held `CONFIDENCE_RATING` lineage are **not** readiness inputs |
| **Package exports + domain docs** | Public domain surface and Twin README note that Readiness is read-side |
| **Focused unit tests** | Derive, cold start, warrant, V1/V2 context, immutability, purity, fidelity |

## 1.2 Explicitly deferred

| Item | Why deferred |
|---|---|
| Numeric factor weights / composite readiness % | Structural honesty first; formulas unlocked later |
| Pass-probability models | Sibling Prediction output; not this ship |
| `PredictionSnapshotStrategy` / writing `PredictionState` | Optional adjacent path; derive-first rule remains; snapshot wiring is a follow-up |
| Decision Engine consumption wiring | Capability 2.8 |
| Recommendation / Mission generation | Capabilities 2.9–2.10 |
| Legacy `ReadinessService` refactor / UI cutover | Convergence Stage A coexistence only (§12) |
| Confidence as a readiness factor | Architecture locks omit for v1 |
| Belief engines inside aggregation | Knowledge/Memory/Performance enrichment stays in write strategies |
| Flask services, blueprints, ORM, Alembic | Domain layer only for this capability |
| Curriculum Engine traversal redesign | Aggregation consumes context; does not invent syllabus |
| Adapters that average legacy % with Twin factors | Forbidden hybrid third formula |

## 1.3 Success shape

After implementation:

```
DigitalTwin snapshot
        +
CurriculumContext (ids, order, weights, format — built outside aggregation)
        +
Goals / Identity scope (from Twin)
        ↓
ReadinessAggregation.derive(...)
        ↓
ReadinessState
  - overall posture + Evidence Warrant
  - named factor judgements + attributions
  - unknown / sparse flags
        ↓
(consumers later: Decision Engine / Analytics adapters / optional Prediction snapshot)
```

Same Twin + same CurriculumContext + same Goals → same structural `ReadinessState`. No Twin mutation. No scoring formulas. No Flask. No migrations. No next-action selection.

## 1.4 Package placement (locked recommendation)

Prefer a **sibling domain package**, not a Twin write-domain module:

| Path root | Rationale |
|---|---|
| **`app/domain/readiness/`** | Makes read-side ownership obvious; avoids implying `ReadinessState` is a Knowledge/Memory peer evolved by Update Strategies |

Do **not** add `readiness: ReadinessState` as a required field on `DigitalTwin` in this ship. Live readiness is derived on read. Optional historical copies remain Prediction’s concern (deferred).

---

# 2. Files to create

| Path | Role |
|---|---|
| `app/domain/readiness/__init__.py` | Package exports: `ReadinessState`, factor types, catalogue constants, `ReadinessAggregation` |
| `app/domain/readiness/factors.py` | Stable factor identity constants / enum-like catalogue matching architecture §2 |
| `app/domain/readiness/readiness_state.py` | Frozen `ReadinessState`, `FactorJudgement` (or equivalent), attribution / warrant slots |
| `app/domain/readiness/curriculum_context.py` | Framework-free Curriculum context value object (topic/section identities, weights, format tag, ordered ids) |
| `app/domain/readiness/aggregation.py` | `ReadinessAggregation` (or `derive_readiness`) — pure derive path |
| `tests/test_readiness_aggregation.py` | Unit + fidelity + V1/V2-context + warrant + cold-start suite |

Do **not** create in this capability: services, blueprints, migrations, scoring modules, Decision Engine, Prediction snapshot strategy, or adapters that rewrite legacy `ReadinessService`.

---

# 3. Files to modify

| Path | Why it must change |
|---|---|
| `app/domain/__init__.py` | Optional re-export or docstring note that readiness is a domain package (only if the package already advertises subdomains) |
| `app/domain/twin/README.md` | Document Readiness as **read-side** consumer of Twin; clarify it is not a write strategy; point to `app/domain/readiness/` |
| `app/domain/twin/strategies/base_strategy.py` | Docstring clarification only if needed: Readiness is **not** an Update Strategy (keep `PredictionSnapshotStrategy` as future write-adjacent snapshot path) |

**Do not modify (this capability)**

- `app/domain/twin/update_pipeline.py` algorithms or registration defaults  
- Knowledge / Memory / Behaviour / Performance strategies or frozensets  
- `DigitalTwin` aggregate shape (no required `readiness` field)  
- `PredictionState` schema (snapshot wiring deferred; do not overload `readiness_snapshot: float` as structural factor truth)  
- `app/services/readiness_service.py` or analytics/dashboard blueprints  
- Evidence catalogue, Curriculum JSON, Alembic, Flask app factory  

**Caller note (documentation only in README):** future services that need Curriculum weights must build `CurriculumContext` via `CurriculumService` helpers (`get_all_topics_ordered`, V1 topic weights / V2 section weights) **outside** the domain aggregator — aggregation stays framework-free.

---

# 4. ReadinessState representation

## 4.1 Classification (keep)

| Property | Requirement |
|---|---|
| **Derived** | Produced only by aggregation over Twin + CurriculumContext + Goals |
| **Immutable** | Frozen dataclasses; one derivation per input snapshot |
| **Factorable** | Always carries named factors; never overall posture alone |
| **Warrant-aware** | Evidence Warrant is mandatory, not optional metadata |
| **Non-authoritative for beliefs** | Does not replace Twin domains |
| **Non-authoritative for decisions** | Does not select actions |

## 4.2 Conceptual slots → structural fields

| Architecture slot | Planned structural representation |
|---|---|
| **Scope identity** | Student / curriculum / sitting references copied from Twin Identity + Goals (ids/strings already on Twin) |
| **Overall readiness posture** | Named posture enum/constant — **not** a float % in v1 structural ship |
| **Named factors** | Ordered tuple/list of `FactorJudgement` covering the full catalogue |
| **Factor attributions** | Per-factor attribution records (Twin domain tags, curriculum entity ids, weight context notes, evidence id hooks) |
| **Evidence Warrant** | Overall warrant posture + per-factor warrant contribution |
| **Unknown / sparse flags** | Explicit flags or postures on factors; overall `not_yet_knowable` when cold start |
| **Derivation context** | Curriculum format (`v1` / `v2`), Goal constraint summary used, optional derivation id / as-of timestamp |
| **Optional snapshot metadata** | **Omit from ReadinessState v1** — belongs with Prediction when snapshot path ships |

## 4.3 Recommended types (structural, not schema-locked)

Illustrative shapes for implementers (names may be refined; meanings are binding):

```
FactorId                  # catalogue identity
FactorPosture             # unknown | low_warrant | risk_elevating | supportive | not_applicable
WarrantPosture            # low | medium | high  (or unknown/low/partial/strong — exact tokens locked in code)

FactorAttribution
  twin_domains: ...       # e.g. knowledge, memory, behaviour, performance, goals, curriculum
  curriculum_entity_ids: ...
  evidence_ids: ...       # hooks when Twin lineage exposes them
  notes: ...              # short structural attribution tags — not LLM prose

FactorJudgement
  factor_id
  posture
  warrant
  attribution
  sparse: bool

ReadinessState
  scope: ...
  overall_posture         # includes not_yet_knowable / unknown / fragile / … — no Mid fabrication
  overall_warrant
  factors: tuple[FactorJudgement, ...]
  curriculum_format
  derived_at / derivation_id (optional)
```

## 4.4 What must not be added now

- Required numeric `score: float` as the sole overall representation  
- Mutating methods that write Twin domains  
- Confidence factor field for v1  
- Mission / Decision State fields  
- Parallel TopicProgress-backed fields as Twin substitutes  
- Embedding a full second syllabus tree inside ReadinessState  

## 4.5 Relationship to existing `PredictionState`

`PredictionState.readiness_snapshot: float | None` remains a **legacy-shaped optional float bag** for future snapshots. Structural Capability 2.7 must **not**:

- Treat that float as live readiness authority  
- Write it from aggregation in the first ship (unless a separately approved thin snapshot follow-up is explicitly scoped)  
- Drop warrant when any future snapshot stores an overall claim  

---

# 5. Aggregation flow

## 5.1 Entry contract

```
ReadinessAggregation.derive(
    twin: DigitalTwin,
    curriculum: CurriculumContext,
    *,
    as_of: datetime | None = None,   # optional; default deterministic from inputs only
) -> ReadinessState
```

Binding rules:

1. **Observational only** — read `twin.knowledge`, `.memory`, `.behaviour`, `.performance`, `.goals`, `.identity`; never call Update Strategies.  
2. **Single snapshot** — do not blend Twins from different times.  
3. **CurriculumContext required** — aggregation does not load ORM curricula.  
4. **Deterministic core** — same inputs → equal `ReadinessState` structural fields.  
5. **Framework-free** — no Flask, SQLAlchemy, request/session, network, or LLM.  

## 5.2 Flow steps (structural)

```
1. Validate scope coherence (Identity curriculum id vs CurriculumContext; Goals sitting when present)
2. Inspect domain density (empty / sparse / present) per Knowledge, Memory, Behaviour, Performance
3. For each catalogue factor:
     a. Select allowed inputs only
     b. Assign structural posture (presence/absence / conflict visibility — no numeric scoring)
     c. Attach attributions + lineage hooks
     d. Assign per-factor warrant
4. Propagate Evidence Warrant to overall (§7)
5. Compose overall posture under cold-start / unknown rules (§8)
6. Return frozen ReadinessState
```

## 5.3 Input mapping (binding)

| Input | Used for | Must not |
|---|---|---|
| KnowledgeState | Curriculum Coverage; Knowledge Strength | Invent mastery beliefs; treat Confidence lineage as mastery |
| MemoryState | Memory Stability | Update `last_reinforced`; collapse into Knowledge Strength |
| BehaviourState | Behaviour Reliability | Grant exam readiness from missions/streaks |
| PerformanceState | Assessment Performance | Emit pass probability; equate one mock with overall readiness |
| GoalState | Time / Goal Pressure; scope | Invent Knowledge/Performance from dates/hours alone |
| IdentityState | Scope binding | Invent syllabus |
| CurriculumContext | Denominator, order, weights, V1/V2 format | Parallel topic trees |
| Confidence / Decision State / raw missions | — | Not v1 aggregation inputs |

## 5.4 Explicit non-computations (first ship)

Must **not**:

- Compute readiness percentages, weighted averages, or pass probabilities  
- Fill empty `mastery_belief` / retention bags  
- Select next actions or rank topics for study  
- Generate missions or recommendations  
- Persist Twin, evidence, or Prediction snapshots  
- Import or call `ReadinessService`  
- Absorb orphan evidence types not represented in Twin domains  

## 5.5 CurriculumContext construction (outside this package)

Future service/orchestration layer (not in 2.7 structural domain PR unless a tiny pure helper is unavoidable):

1. Load curriculum via existing Curriculum Engine / models.  
2. Use `CurriculumService.get_all_topics_ordered` (and V2 section weight helpers as applicable).  
3. Project into `CurriculumContext` (ids, display order, weights, format).  
4. Pass into `derive`.  

Domain tests build `CurriculumContext` directly with fixtures — no DB required.

## 5.6 V1/V2 handling inside aggregation

| Format | Structural behaviour |
|---|---|
| **V1** | Topic-weighted coverage / risk emphasis; no Section requirement |
| **V2** | May attribute section-level concentration when section ids exist; same factor catalogue |
| **Both** | Same cold-start / unknown / warrant contracts |

---

# 6. Factor contract implementation

## 6.1 Canonical catalogue (must all appear)

| Factor id (stable) | Educational meaning | Primary inputs |
|---|---|---|
| `curriculum_coverage` | Weighted Twin presence vs syllabus denominator | Knowledge slots + CurriculumContext |
| `knowledge_strength` | Current mastery / honest structural proxy | Knowledge beliefs or named proxy — never fabricate High |
| `memory_stability` | Retention availability at sitting | Memory + Goals sitting date context |
| `behaviour_reliability` | Pace / adherence feasibility | Behaviour + Goals capacity |
| `assessment_performance` | Assessed-condition strength/weakness | Performance |
| `time_goal_pressure` | Calendar/capacity reframe (supporting) | Goals (+ remaining work context) |
| `evidence_warrant` | Meta honesty about support (may be overall field + factor) | Density across domains |

Implementation may represent Evidence Warrant as both a catalogue factor **and** an overall field, but must not omit it.

## 6.2 Per-factor contract (must expose)

| Element | Structural rule |
|---|---|
| **Identity** | Stable id from catalogue |
| **Posture** | From allowed posture set; opacity forbidden |
| **Attribution** | Twin domains + curriculum entities (+ evidence hooks when present) |
| **Warrant** | Per-factor warrant posture |
| **Disagreement** | Factors may conflict; do not force consensus Mid |

## 6.3 Structural posture assignment (no formulas)

First ship uses **presence / absence / conflict visibility** rules, for example:

| Condition | Example posture |
|---|---|
| Domain empty for factor | `unknown` |
| Slots present, beliefs empty | Coverage may be low-warrant structural presence; Knowledge Strength remains `unknown` or explicit structural-proxy (never High) |
| Behaviour lineage present, Performance empty | Behaviour Reliability may be informative; Assessment Performance `unknown`; overall warrant low |
| Performance summaries weak on high-weight ids | Assessment Performance `risk_elevating` (structural signal only — no accuracy engine) |
| Goals with sitting date + thin Twin | Time pressure may be `risk_elevating` as calendar context; does not invent Assessment Performance |

Exact token mapping is an implementation detail; **forbidden** mappings are binding: empty → Mid; empty → High; Behaviour strong → overall ready.

## 6.4 Separations that must remain

- Assessment Performance ≠ Behaviour Reliability  
- Memory Stability ≠ Knowledge Strength  
- Evidence Warrant ≠ self-report Confidence  
- Time / Goal Pressure does not replace content factors  

## 6.5 What is not a factor

Motivation scores, streak lengths, Confidence self-report, mission completion counts as Knowledge Strength, Decision reason codes, mission task lists, dashboard vanity %.

---

# 7. Evidence Warrant propagation

## 7.1 Rules to implement

1. **Per-factor warrant** from density/applicability of that factor’s Twin inputs.  
2. **Overall warrant never stronger** than critical sitting-relevant factors allow — sparse/empty Performance keeps exam-preparedness warrant low even if Behaviour looks strong.  
3. **Absence lowers warrant**; it does not invent Mid content postures.  
4. **Warrant ≠ weakness** — low warrant means “we lack support,” not automatically “student is weak.”  
5. **Warrant travels** with `ReadinessState` and must be assertable in tests even when UI is absent.  
6. Dense evidence on **low-weight** topics must not inflate overall sitting warrant; sparse evidence on **high-weight** topics must constrain it (using CurriculumContext weights as attribution emphasis — still no composite formula required).

## 7.2 Propagation sketch

```
Twin domain density / lineage quality
        ↓
Per-factor Evidence Warrant
        ↓
Overall Evidence Warrant  ───► constrains overall_posture assertiveness
        ↓
(future) Decision / explanation consumers inherit honesty
```

## 7.3 Forbidden warrant behaviours (testable)

- Hiding uncertainty  
- Averaging missing factors as Mid to fill warrant  
- Confidence inflating Assessment Performance warrant  
- Single-mock / narrow-slice evidence claiming high overall warrant  
- Returning overall supportive posture with low warrant and no sparse flags  

---

# 8. Cold-start handling

## 8.1 Detection

Cold start / sparse start when one or more hold:

- Empty/few Knowledge slots or empty mastery beliefs  
- Empty/few Memory reinforcements  
- Thin/empty Behaviour lineage  
- Empty/sparse Performance assessments  
- Goals exist without educational evidence  

**Goals alone never create preparedness.**

## 8.2 Output contract (must implement)

When cold start applies, `ReadinessState` must:

1. Mark overall posture **not yet knowable / unknown / low-warrant** — not Mid, not High.  
2. Emit factors with explicit unknown or low-warrant postures where inputs are absent.  
3. Allow partial structural factors (e.g. coverage started) **without** upgrading exam preparedness.  
4. Keep overall Evidence Warrant low.  
5. Preserve explainability hooks: insufficient evidence is a valid overall narrative input.

## 8.3 Domain-empty mapping (binding)

| Input condition | Factor handling |
|---|---|
| Empty Performance | Assessment Performance = unknown / low warrant |
| Empty mastery beliefs | Knowledge Strength = unknown (or structural-proxy only if slots exist) |
| Empty Memory | Memory Stability = unknown |
| Thin Behaviour | Behaviour Reliability = unknown / low warrant |
| Goals only | Overall = not yet knowable; all exam-preparedness claims low-warrant |
| Strong Behaviour, empty Performance | Behaviour may be informative; overall exam readiness remains low-warrant |

## 8.4 Forbidden cold-start behaviours

- Invent High readiness  
- Default overall to Mid  
- Treat mission adherence as exam readiness  
- Fill empty belief bags inside the aggregator  
- Narrate “on track” without warrant (no product copy in domain — but posture must not imply it)  
- Use Confidence to invent Assessment Performance  
- Write synthetic Twin beliefs to make scoring possible  

## 8.5 Boundary with Decision Engine

Decision Engine (later) may prefer diagnostics under cold start. Aggregation only surfaces unknown — it does not invent Performance or choose diagnostics.

---

# 9. Public API impact

## 9.1 New exports (additive)

From `app.domain.readiness` (names illustrative but should be stable once shipped):

| Symbol | Kind |
|---|---|
| `ReadinessState` | Frozen dataclass |
| `FactorJudgement` (or equivalent) | Frozen dataclass |
| `FactorId` / catalogue constants | Stable identities |
| `FactorPosture` / `WarrantPosture` | Enums or constants |
| `CurriculumContext` | Frozen value object |
| `ReadinessAggregation` (or `derive_readiness`) | Pure derive API |

Optional: re-export key symbols from `app.domain` only if that package already acts as a facade — prefer explicit `app.domain.readiness` imports to keep Twin write-path imports clean.

## 9.2 Unchanged interfaces

| Contract | Impact |
|---|---|
| `TwinUpdatePipeline` / Update Strategies | Unchanged — Readiness is not registered as a strategy |
| `DigitalTwin` fields | Unchanged (no required readiness domain field) |
| `PredictionState` | Unchanged in structural ship |
| `LearningEvidence` / `EvidenceType` | Unchanged |
| HTTP / Flask / `ReadinessService` | No product API change required in this capability |
| ORM / Alembic | None |

## 9.3 API compatibility rules

- Additive domain package only.  
- No breaking renames of Twin write domains.  
- Callers that never import readiness continue to work.  
- Future Decision Engine depends on this API; keep factor ids stable once published.  

---

# 10. Testing strategy

Target module: `tests/test_readiness_aggregation.py`.

## 10.1 Suites

| Suite | Assertions |
|---|---|
| **Contract** | `derive` returns `ReadinessState` with full factor catalogue; frozen/immutable |
| **Purity** | Input Twin unchanged after derive; no strategy registration side effects |
| **Determinism** | Same Twin + CurriculumContext + Goals → equal structural fields |
| **Cold start** | Goals-only Twin → overall not-yet-knowable; factors unknown/low-warrant; never Mid/High |
| **Empty Performance** | Assessment Performance unknown; overall warrant low even if Behaviour present |
| **Empty mastery** | Knowledge Strength unknown; no fabricated High |
| **Empty Memory** | Memory Stability unknown |
| **Factor disagreement** | Supportive Knowledge-proxy beside risk-elevating Memory/Performance remains visible — no forced average |
| **Warrant propagation** | Overall warrant constrained by sparse critical factors; low-weight dense evidence does not inflate sitting warrant |
| **Confidence omission** | Confidence-shaped Twin lineage / self-report bags (if present on fixtures) do not create Assessment Performance or upgrade overall |
| **Curriculum V1 context** | Flat topic-weighted context derives without Section ids |
| **Curriculum V2 context** | Section-aware context derives; same catalogue; no hard Section requirement in aggregator when format=v1 |
| **No Twin mutation** | Knowledge/Memory/Behaviour/Performance equality before/after |
| **Framework purity** | AST/import ban for Flask/SQLAlchemy (same pattern as strategy tests) |
| **Non-scoring** | No readiness % / pass probability fields required; no invented numeric composites |
| **Attribution presence** | Factors cite Twin domains and curriculum entities used |
| **Firewall** | Module does not import Decision/Mission/Recommendation services |

## 10.2 Fixture strategy

- Build minimal `DigitalTwin` via existing `*.create()` helpers.  
- Build `CurriculumContext` fixtures for V1 and V2 shapes in-memory.  
- Prefer structural emptiness over mocking ORM.

## 10.3 Regression

- Existing Twin strategy suites remain green (Knowledge / Memory / Behaviour / Performance).  
- No curriculum engine test changes expected.  
- Suggested command:  
  `python -m pytest tests/test_readiness_aggregation.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py tests/test_behaviour_update_strategy.py tests/test_performance_update_strategy.py -v`  
  and `ruff check app/ tests/`

## 10.4 Out of test scope for this capability

- HTTP / analytics widget integration  
- Persistence / Prediction snapshot round-trips  
- Numeric scoring correctness  
- Decision Engine selection behaviour  
- Legacy `ReadinessService` parity goldens (document divergence as transitional debt; do not force equality)  

---

# 11. Migration impact

| Concern | Impact |
|---|---|
| Database changes | **None** |
| Alembic migrations | **None** |
| ORM / model changes | **None** |
| Persistence changes | **None** |
| Evidence catalogue DB | **None** |
| Curriculum JSON | **None** |
| Data backfill | **None** |
| Legacy readiness tables | **None** — no cutover in this ship |

Twin and readiness domain remain in-memory / framework-free. If a later milestone persists readiness snapshots via Prediction, that is a separate schema plan — not Capability 2.7 structural aggregation.

**Expected answer for this capability: None.**

---

# 12. Backwards compatibility

| Invariant | Confirmation |
|---|---|
| **Twin write path unaffected** | Pipeline and K→M→B→P strategies unchanged |
| **DigitalTwin shape compatible** | No required readiness field added |
| **Curriculum V1/V2 unaffected** | No traversal redesign; context object only |
| **Legacy `ReadinessService` continues** | Coexistence Stage A — not deleted or secretly replaced |
| **No third live formula forced into UI** | Domain aggregation ships; presentation cutover deferred |
| **Evidence append-only** | Preserved |
| **Deterministic cores** | No LLM/network in derive path |
| **Confidence separability** | Confidence omitted from v1 inputs |

### Legacy convergence posture for this ship

Remain at **Stage A — Coexistence (documented)**:

- Twin-first aggregation exists in domain.  
- Legacy service continues for existing surfaces.  
- Do not deepen TopicProgress formulas.  
- Do not invent hybrid averages of legacy % + Twin factors.  

Stages B–D (Decision wiring, UI cutover, retirement) are **out of scope**.

---

# 13. Educational Fidelity Review

Verify the following remain true after structural implementation:

| Fidelity check | Required outcome |
|---|---|
| **Readiness never owns evidence** | Aggregation only cites Twin lineage; never appends Learning Evidence |
| **Readiness never updates the Twin** | Input Twin domains identical after derive |
| **Readiness never invents beliefs** | Empty beliefs stay empty; no fabricated High preparedness |
| **Uncertainty is honest** | Evidence Warrant first-class; cold start never marketed as ready via Mid/High defaults |
| **Activity ≠ readiness** | Behaviour-only Twin does not yield exam-ready overall posture |
| **Confidence ≠ readiness** | Confidence omitted; cannot upgrade Assessment Performance |
| **Performance ≠ whole readiness** | Assessment Performance is one factor; warrant + weights constrain overall |
| **Readiness ≠ Decision** | No action selection APIs or reason-code choosers |
| **Readiness ≠ Missions** | No mission generation |
| **Factor disagreement preserved** | High Knowledge + Low Memory style tensions remain visible |
| **V1/V2 honesty parity** | Same unknown/warrant contracts on both formats |
| **Explainability spine** | Factors carry attributions usable in Curriculum → Evidence → Twin → Factor → Overall |

### Anti-fidelity patterns to reject in review

| Pattern | Reject because |
|---|---|
| Cold-start Mid default | Fabricates preparedness |
| Mission week ⇒ exam ready | Activity theatre |
| Confidence slider upgrades overall | Contamination |
| Opaque overall without factors | Product thesis failure |
| Aggregator writes Twin to “have something to score” | Write/read firewall breach |

---

# 14. Acceptance criteria

Capability 2.7 structural implementation is accepted when all of the following hold:

1. **`app/domain/readiness/` exists** as framework-free domain code with `derive` (or equivalent) producing `ReadinessState`.  
2. **`ReadinessState` is factorable** — full catalogue present; overall posture never ships without factors + warrant.  
3. **Aggregation is read-side only** — Twin domains unchanged; no Update Strategy registration for readiness beliefs.  
4. **Cold-start contract** — Goals-only / empty domains → not-yet-knowable / unknown / low-warrant; never Mid/High fabrication.  
5. **Evidence Warrant** propagates per-factor and overall; sparse Performance constrains exam-preparedness warrant.  
6. **Confidence omitted** from v1 inputs and cannot upgrade Assessment Performance.  
7. **CurriculumContext** supports V1 and V2 fixtures without requiring Sections globally.  
8. **No scoring formulas / pass probability / Decision / Mission / Flask services / migrations** in the Capability 2.7 structural PR unless explicitly re-scoped.  
9. **Public exports** documented; Twin README clarifies read-side ownership.  
10. **Tests green** for readiness suite + Twin strategy regressions; ruff clean on touched paths.  
11. **Hard educational rules** remain true: Activity ≠ readiness; Confidence ≠ mastery; Readiness ≠ Decision; no third formula introduced into live UI.  
12. **Legacy coexistence** — `ReadinessService` not deleted; no hybrid averaging adapter shipped as “temporary truth.”

---

# 15. Definition of Done

A Capability 2.7 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; deferred items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] `ReadinessState` matches §4 (derived, factorable, warrant-aware, no required Twin field)  
- [ ] Aggregation flow matches §5 (pure derive; CurriculumContext; no Twin writes)  
- [ ] Factor contracts match §6 (full catalogue; separations preserved)  
- [ ] Evidence Warrant propagation matches §7  
- [ ] Cold-start handling matches §8  
- [ ] Public API impact is additive only (§9)  
- [ ] Testing strategy §10 executed and green  
- [ ] Migration impact is None (§11) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §12 hold (Twin write path, V1/V2, legacy coexistence)  
- [ ] Educational fidelity review §13 verified by tests and review  
- [ ] Acceptance criteria §14 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No Decision Engine, Mission Generation, Prediction snapshot strategy, numeric composites, or `ReadinessService` deletion shipped under this capability label  

**Stop after Capability 2.7 structural ship + review.** Do not start Capability 2.8 in the same change set unless separately requested.

---

# 16. Recommended Implementation Sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read 2.7.1 analysis + 2.7.2 architecture + this plan | Shared understanding; Confidence omit confirmed |
| **1** | Lock posture/warrant token vocabulary in PR description | Tokens listed; Mid default forbidden |
| **2** | Implement `factors.py` + `readiness_state.py` + `curriculum_context.py` | Types import cleanly; frozen |
| **3** | Implement `aggregation.py` cold-start + empty-domain paths first | Goals-only → not-yet-knowable |
| **4** | Implement remaining factor structural postures + attributions | Full catalogue; disagreement visible |
| **5** | Implement warrant propagation constraints | Sparse Performance constrains overall |
| **6** | Export package + update Twin README | Read-side ownership clear |
| **7** | Write `tests/test_readiness_aggregation.py` | Suite green |
| **8** | Run Twin strategy regressions + ruff | No regressions |
| **9** | Capability review against §14 + fidelity §13 | Checklist complete |
| **10** | Completion report + stop | Do not start 2.8 |

### Suggested PR shape

- **Title:** `feat: structural Readiness Aggregation (read-side, factorable)`  
- **Body:** link this plan + 2.7.1/2.7.2; state Confidence omit; migration None; V1/V2 via CurriculumContext; note deferred numeric scoring, Prediction snapshots, Decision wiring, and legacy cutover  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, Decision Engine, or UI.

Next engineering step (separate milestone): execute §16 steps 1–10 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains consumed without modification |
| **2.7.1** | Readiness Educational Analysis | Approved educational charter |
| **2.7.2** | Readiness Aggregation Architecture | Approved structural contracts |
| **2.7.3** | **Readiness Implementation Plan** | **This document** |
| 2.7 impl | Structural aggregation | Separate milestone after this plan |
| 2.8–2.10 | Decision / Recommendation / Missions | Consume readiness context later; not in this ship |

---

# Appendix B — Risks carried into implementation

| Risk | Mitigation in implementation |
|---|---|
| Treating ReadinessState as write domain | Separate package; no Twin field; no Update Strategy |
| Mid defaults under cold start | Explicit tests; forbidden postures in review |
| Averaging disagreement away | Keep factors separable; no composite formula |
| Confidence contamination | Omit inputs; fidelity tests |
| V1 Section hard-requirement | CurriculumContext format branching; V1 fixture tests |
| Legacy dual truth deepening | Stage A only; no hybrid adapters |
| Belief engines in aggregator | Structural postures only |
| Snapshot-as-truth | Do not write Prediction in this ship |
| Decision conflation | No action selection API |

---

# Appendix C — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.7.3 — Readiness Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; context-object consumption planned; no traversal redesign |
| Application code intentionally untouched | Yes (this milestone) |
| Midpoint gate | APPROVED WITH CONDITIONS — encoded in prior 2.7 docs and herein |
| Preceded by | 2.7.1 Educational Analysis + 2.7.2 Aggregation Architecture (approved) |
| Next | Structural Readiness Aggregation implementation → tests → capability review |

---

*End of Capability 2.7.3 Readiness Implementation Plan.*
