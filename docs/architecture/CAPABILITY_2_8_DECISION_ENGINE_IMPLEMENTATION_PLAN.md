# Capability 2.8.3 — Decision Engine Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.8 Decision Engine (structural read-side implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
**Decision architecture:** [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md)  
**Upstream gate:** Readiness Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/READINESS_ARCHITECTURE_REVIEW.md`](../reviews/READINESS_ARCHITECTURE_REVIEW.md))  
**Companions:** [`CAPABILITY_2_7_READINESS_IMPLEMENTATION_PLAN.md`](CAPABILITY_2_7_READINESS_IMPLEMENTATION_PLAN.md), [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Plan the first structural **read-side** ship of Decision Engine — **no code, tests, migrations, services, or scoring/selection formulas in this document’s milestone**

---

## Document purpose

This plan translates the approved Decision Engine educational analysis and architecture into a concrete, executable implementation sequence for Capability 2.8.

It answers:

1. What is in / out of scope for the first Decision Engine ship  
2. Which files to create and modify  
3. How Decision, candidates, and reason codes must be represented  
4. How evaluation flow and explanation contracts must work  
5. Public API, testing, migration, compatibility, fidelity, and acceptance gates  

**Hard architectural rules (binding):**

1. Decision Engine never writes Learning Evidence as belief authority.  
2. Decision Engine never mutates Twin belief domains.  
3. Decision Engine never invents curriculum identities, weights, or order.  
4. Decision Engine never recomputes a competing readiness truth.  
5. Decision Engine never coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
6. Every Decision must carry reason codes, a candidate set, and lineage hooks.  
7. Curriculum V1 and V2 remain loadable; weights and order come only from canonical Curriculum helpers (via domain-safe context — not Flask-coupled service imports inside the engine).

**Governing principle:** Readiness is derived and factorable; Decision Engine selects next action — explainably, deterministically in the core path, and without engagement theatre.  
**Structural discipline:** Structure, candidates, reason codes, and warrant honesty first; numeric ranking / optimization later.

**Non-goals of this document**

- Implementing evaluation or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Concrete ranking scores, optimization objectives, Bayesian selection math, or multi-objective solvers  
- UI, analytics cutover, gamification, notifications, Recommendation packaging (2.9), or Mission Generation (2.10)  
- Refactoring or deleting legacy `RecommendationService`  
- Full Decision State persistence schema or Decision Journal UX  

---

# 1. Scope

## 1.1 In scope (Capability 2.8 structural ship)

| Item | Intent |
|---|---|
| **`Decision` + supporting value types** | Immutable, framework-free selection result — not a Twin write-domain peer |
| **Candidate action types + candidate set** | Mandatory alternatives with status, attribution, feasibility envelope |
| **Reason-code vocabulary (structural)** | Stable family catalogue + versionable code identities — **no free-text slogans as authority** |
| **Constraints / Goals input shapes** | Framework-free session feasibility + goal scope objects (or thin wrappers over Twin Goals) |
| **`DecisionEngine.evaluate(...)`** | Pure read-side function/class: Twin + ReadinessState + CurriculumContext + Goals + Constraints (+ optional history) → `Decision` |
| **Evaluation pipeline skeleton** | Assemble → validate → interpret readiness → nominate → constrain/order → select → author reasons → emit |
| **Cold-start / low-warrant selection posture** | Prefer evidence-creating / diagnostic-shaped actions; never invent Mid readiness |
| **Explainability hooks** | Lineage references, constraint acknowledgements, warrant posture inheritance |
| **Package exports + domain docs** | Public domain surface; Twin / readiness READMEs note Decision as read-side selector |
| **Focused unit tests** | Evaluate, candidates required, reason codes, cold start, V1/V2, immutability, purity, fidelity, firewall |

## 1.2 Explicitly deferred

| Item | Why deferred |
|---|---|
| Numeric ranking / selection scores | Structural honesty first; formulas unlocked later |
| Optimization solvers / Bayesian policies | Premature before contracts mature |
| Decision State persistence / ORM | Audit materialisation is a follow-up; first ship may emit in-memory Decision only |
| Decision Journal accept/dismiss UX | Product recording path; not selection |
| Recommendation packaging (2.9) | Packages Decision; must not invent ranking |
| Mission generation (2.10) | Projects Decision; must not store private mastery |
| Legacy `RecommendationService` cutover | Convergence Stage A coexistence only (§12) |
| Calibrated Confidence domain | Risk-framing stance enough to start; omit as mastery proxy |
| Prediction snapshots as live selection authority | Non-authoritative context only if present; not required |
| Multi-action session batches | May land later; ownership unchanged |
| Flask services, blueprints, ORM, Alembic | Domain layer only for this capability |
| Curriculum Engine traversal redesign | Engine consumes context; does not invent syllabus |
| Adapters that hybrid-average legacy ranks with Twin Decision | Forbidden temporary third truth |

## 1.3 Success shape

After implementation:

```
DigitalTwin snapshot
        +
ReadinessState          (context only — from ReadinessAggregation)
        +
CurriculumContext       (ids, order, weights, format — reuse readiness VO)
        +
Goals / Constraints     (destination + feasibility bound)
        +
Optional Decision history (anti-thrash context)
        ↓
DecisionEngine.evaluate(...)
        ↓
Decision
  - selected action
  - candidate set (mandatory)
  - reason codes + lineage + constraint acknowledgements
  - warrant posture honesty
        ↓
(consumers later: Recommendation 2.9 / Mission 2.10 / Decision State materialisation)
```

Same inputs → same structural `Decision`. No Twin mutation. No readiness recomputation. No scoring formulas. No Flask. No migrations. No recommendation titles. No missions.

## 1.4 Package placement (locked recommendation)

Prefer a **sibling domain package**, not a Twin write-domain module:

| Path root | Rationale |
|---|---|
| **`app/domain/decision/`** | Makes read-side next-action ownership obvious; mirrors `app/domain/readiness/`; avoids implying Decision is a Knowledge/Memory peer evolved by Update Strategies |

Do **not** add `decision: Decision` as a required field on `DigitalTwin` in this ship. Live selection is derived on read. Decision State materialisation (audit) remains a later persistence concern.

**Reuse:** Import `CurriculumContext` (and related format types) from `app.domain.readiness` — do not fork a second syllabus context object. Decision may define thin Constraints / DecisionHistory value objects local to `app/domain/decision/`.

---

# 2. Files to create

| Path | Role |
|---|---|
| `app/domain/decision/__init__.py` | Package exports: `Decision`, candidate/reason types, catalogue constants, `DecisionEngine` |
| `app/domain/decision/action_types.py` | Stable action-family catalogue (study / revise / assess / diagnostic / rest-or-protect-intensity) |
| `app/domain/decision/reason_codes.py` | Stable reason-code family + code identity catalogue (versionable vocabulary) |
| `app/domain/decision/candidate.py` | Frozen `CandidateAction` (+ status / attribution / feasibility slots) |
| `app/domain/decision/constraints.py` | Framework-free Constraints (+ optional GoalScope helpers if not inlined) |
| `app/domain/decision/decision.py` | Frozen `Decision` (selected action, candidates, reasons, lineage, acknowledgements) |
| `app/domain/decision/engine.py` | `DecisionEngine` (or `evaluate_decision`) — pure evaluate path |
| `tests/test_decision_engine.py` | Unit + fidelity + V1/V2-context + cold-start + firewall suite |

Optional (only if it keeps `engine.py` readable without inventing formulas):

| Path | Role |
|---|---|
| `app/domain/decision/nomination.py` | Pure helpers that nominate structural candidates from Twin + CurriculumContext + ReadinessState |
| `app/domain/decision/history.py` | Optional thin Decision history / anti-thrash input VO |

Do **not** create in this capability: services, blueprints, migrations, scoring modules, Recommendation Engine, Mission Intelligence, Decision State ORM, or adapters that rewrite `RecommendationService`.

---

# 3. Files to modify

| Path | Why it must change |
|---|---|
| `app/domain/twin/README.md` | Document Decision Engine as **read-side** next-action selector; clarify it is not a write strategy; point to `app/domain/decision/`; note Readiness remains context only |
| `app/domain/readiness/__init__.py` | Docstring clarification only if needed: Readiness does not select actions; Decision Engine is a separate consumer |
| `app/domain/__init__.py` | Optional docstring note that decision is a domain package (only if the package already advertises subdomains) |

**Do not modify (this capability)**

- `app/domain/twin/update_pipeline.py` algorithms or registration defaults  
- Knowledge / Memory / Behaviour / Performance strategies or frozensets  
- `DigitalTwin` aggregate shape (no required `decision` field)  
- `app/domain/readiness/aggregation.py` factor math or overall posture rules  
- `app/services/recommendation_service.py`, readiness service, analytics/dashboard blueprints  
- Evidence catalogue, Curriculum JSON, Alembic, Flask app factory  

**Caller note (documentation only in README):** future services that need Curriculum weights must build `CurriculumContext` via `CurriculumService` helpers **outside** the domain engine — same pattern as Readiness. Orchestration that needs readiness must call `ReadinessAggregation.derive(...)` first, then pass `ReadinessState` into `DecisionEngine.evaluate(...)`. Decision Engine must not re-derive readiness internally as a competing truth.

---

# 4. Decision model representation

## 4.1 Classification (keep)

| Property | Requirement |
|---|---|
| **Read-side** | Produced by reasoning over Twin + ReadinessState + CurriculumContext + Goals + Constraints (+ history) |
| **Immutable** | Frozen dataclasses; one evaluation per input snapshot |
| **Action-selecting** | Chooses a next learning action; may surface ordered alternatives |
| **Explainable** | Reason codes + candidates + lineage mandatory |
| **Curriculum-bound** | Curriculum-scoped actions use official syllabus identities only |
| **Warrant-honest** | Citations of readiness inherit Evidence Warrant; unknown stays unknown |
| **Non-authoritative for beliefs** | Does not replace Twin domains; accepting a Decision does not grant mastery |
| **Not Decision State persistence** | First ship emits live `Decision`; optional later materialisation into Decision State |

## 4.2 Conceptual slots → structural fields

| Architecture slot | Planned structural representation |
|---|---|
| **Scope identity** | Student / curriculum / sitting references from Twin Identity + Goals |
| **Selected action** | Canonical action reference (action family + optional curriculum entity id + intent tag) |
| **Candidate set** | Ordered/frozen tuple of `CandidateAction` covering selected + considered + demoted |
| **Reason codes** | Frozen tuple of stable code identities (from catalogue) with optional attribution hooks |
| **Value rationale hooks** | Short structural tags / tension labels — not marketing copy, not LLM prose |
| **Lineage references** | Twin domain tags, Readiness factor ids, curriculum entity ids, evidence id hooks when available |
| **Constraint acknowledgements** | Which constraint classes demoted/reshaped candidates |
| **Evaluation context** | Curriculum format (`v1` / `v2`), optional evaluation id / as-of, engine version tag |
| **Warrant posture** | Inherited honesty when readiness or Twin evidence density is low |

## 4.3 Recommended types (structural, not schema-locked)

Illustrative shapes for implementers (names may be refined; meanings are binding):

```
ActionFamily              # study | revise | assess | diagnostic | rest_protect_intensity
SelectedAction
  family: ActionFamily
  curriculum_entity_id: str | None
  intent: ...             # coverage_gap | retention_risk | assessment_warrant | feasibility_protection | …

DecisionLineage
  twin_domains: ...
  readiness_factor_ids: ...
  curriculum_entity_ids: ...
  evidence_ids: ...

ConstraintAcknowledgement
  constraint_class: ...
  demoted_candidate_ids: ...
  note_tags: ...          # structural — educational need remains visible

Decision
  scope: ...
  selected: SelectedAction
  candidates: tuple[CandidateAction, ...]
  reason_codes: tuple[ReasonCodeRef, ...]
  lineage: DecisionLineage
  constraint_acknowledgements: tuple[ConstraintAcknowledgement, ...]
  warrant_posture: ...    # inherit / reflect readiness overall warrant honesty
  curriculum_format: ...
  evaluation_id / evaluated_at (optional)
  engine_version: ...     # additive audit tag
```

## 4.4 What must not be added now

- Required numeric `score: float` as the sole selection representation  
- Mutating methods that write Twin domains or append Evidence  
- Recommendation title / urgency badge fields  
- Mission / MissionTask fields  
- Parallel TopicProgress-backed “next topic” as Twin substitute  
- Embedding a full second syllabus tree inside Decision  
- Coerced Mid/High readiness fields invented by the engine  

## 4.5 Decision vs Decision State

| Artefact | First structural ship |
|---|---|
| **Decision** | **In scope** — live evaluate output |
| **Decision State** | **Out of scope for persistence** — may document hooks; do not add ORM/Alembic |
| **Decision Journal** | **Out of scope** — accept/dismiss recording later |

---

# 5. Candidate representation

## 5.1 Purpose

A **candidate action** is a structured alternative considered before selection. The **candidate set is mandatory** on the core educational path — opaque single-action output without alternatives is forbidden.

## 5.2 Conceptual slots → structural fields

| Architecture slot | Planned structural representation |
|---|---|
| **Action type** | `ActionFamily` from catalogue |
| **Curriculum scope** | Canonical topic / section / LO id when applicable — never free-text invention |
| **Intent toward Goal** | Named tension the candidate addresses |
| **Feasibility envelope** | Session-length / intensity fit relative to Constraints (structural tags, not scores) |
| **Attribution hooks** | Twin / Readiness / Curriculum factors that nominated this candidate |
| **Status in set** | `selected` / `considered` / `demoted_by_constraint` / `blocked` (e.g. prerequisite when available) |

## 5.3 Action-type families (must remain separable)

| Family | Educational meaning | Typical nominating signals |
|---|---|---|
| **Study / coverage** | Build Knowledge on underserved weighted identities | Knowledge gaps; Curriculum Coverage risk |
| **Revise / reinforce** | Restore Memory Stability on stale high-value identities | Memory staleness; High Knowledge + Low Memory disagreement |
| **Assess / exam-condition** | Create or strengthen Performance evidence under assessment conditions | Thin Assessment Performance warrant; Behaviour strong / Performance weak |
| **Diagnostic / evidence-creating** | Reduce uncertainty when warrant is low | Cold start; `not_yet_knowable`; sparse Twin |
| **Rest / protect intensity** | Protect learning sustainability when Behaviour / capacity flags risk | Burnout / feasibility constraints without erasing educational need |

Collapsing revise into study, or rest into “do nothing without reason,” is forbidden.

## 5.4 Candidate set principles (binding for implementation)

1. Candidate set **required** on every core `Decision`.  
2. Selected action must appear in (or be explicitly derived from) the considered set.  
3. Demotion is **visible** — constraint demotion remains in the set with acknowledgement.  
4. Candidates that name syllabus work are curriculum-bound.  
5. Batches of multiple selected actions are deferred; single selected action is enough for v1.

## 5.5 What a candidate is not

- A Recommendation title or urgency badge  
- A MissionTask row  
- A mastery belief  
- A readiness factor  
- An LLM-invented topic  

---

# 6. Reason code representation

## 6.1 Definition

**Reason codes** are stable, machine-readable educational justifications authored **only** by Decision Engine. Recommendation packaging may narrate them later; it must not invent competing codes that disagree with the Decision.

## 6.2 Architectural properties → structural rules

| Property | Structural rule |
|---|---|
| **Stable identity** | Versionable catalogue entries (constants / enum), not free-text slogans |
| **Educational meaning** | Each code maps to a named tension family |
| **Attributable** | Codes may carry lineage hooks to Twin / Readiness / Curriculum / Constraints |
| **Warrant-aware** | Codes that cite readiness inherit Evidence Warrant honesty |
| **Comparable** | Analytics may aggregate codes without opaque scores |
| **Non-marketing** | Codes are educational factors, not urgency stickers |

## 6.3 Catalogue families (must cover; exact strings lock in code)

| Family | Educational meaning |
|---|---|
| **Curriculum weight** | Official exam weight / coverage value |
| **Knowledge gap** | Weak or absent mastery on scoped identity |
| **Retention risk** | Memory staleness / stability risk |
| **Assessment warrant gap** | Thin or weak Performance evidence |
| **Time / goal pressure** | Remaining calendar / capacity context |
| **Feasibility demotion** | Constraints / Behaviour sustainability reshape |
| **Cold-start / low warrant** | Prefer evidence-creating actions under uncertainty |
| **Factor disagreement** | Explicit Twin/Readiness tension preserved (e.g. knows-now / may-not-retain) |
| **History / anti-thrash** | Prior dismiss/accept lineage (when history input present) |
| **Confidence risk framing** | Over/under-confidence noted as risk — never as mastery upgrade |

Exact code strings and version tags live in `reason_codes.py`. Meanings and authorship ownership are binding.

## 6.4 Authorship rules (binding)

1. Decision Engine alone authors reason codes for a Decision.  
2. No opaque “recommended for you” without at least one educational reason code.  
3. Version codes additively — preserve audit of older Decisions via `engine_version` / code version.  
4. Do not invent evidence, syllabus topics, or Twin beliefs in reason payloads.  
5. Confidence-related codes are risk framing only.

## 6.5 What reason codes are not

- Readiness factors (Decision may *cite* them)  
- Recommendation titles  
- Mission task labels  
- Mastery scores  
- Engagement badges  

---

# 7. Decision evaluation flow

## 7.1 Entry contract

```
DecisionEngine.evaluate(
    twin: DigitalTwin,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    constraints: Constraints,
    *,
    decision_history: DecisionHistory | None = None,
    as_of: datetime | None = None,   # optional; default deterministic from inputs only
) -> Decision
```

Goals scope is taken from `twin.goals` / `twin.identity` (and mirrored in readiness scope when present). Do not invent a second Goals authority.

Binding rules:

1. **Observational only** — read Twin domains and ReadinessState; never call Update Strategies; never mutate readiness.  
2. **Single snapshot** — do not blend Twins or ReadinessStates from different times.  
3. **CurriculumContext required** — engine does not load ORM curricula.  
4. **ReadinessState required as context** — engine does not call `ReadinessAggregation.derive` as a hidden side path that could diverge; callers assemble readiness first.  
5. **Deterministic core** — same inputs → equal `Decision` structural fields.  
6. **Framework-free** — no Flask, SQLAlchemy, request/session, network, or LLM.  

## 7.2 Pipeline stages (structural)

```
1. Assemble inputs
        ↓
2. Validate / scope (Goal sitting, CurriculumContext, Twin snapshot identity, readiness scope coherence)
        ↓
3. Interpret readiness context (factors, warrant, cold-start, disagreement — context only)
        ↓
4. Nominate candidate actions (Twin + Curriculum value tensions + feasibility envelopes)
        ↓
5. Apply educational priority ordering (posture, not numeric scores) and constraint handling
        ↓
6. Select action + retain candidate set
        ↓
7. Author reason codes + lineage hooks + constraint acknowledgements
        ↓
8. Emit Decision
```

## 7.3 Stage responsibilities

| Stage | Owns | Must not |
|---|---|---|
| **Assemble inputs** | Gather Twin, ReadinessState, CurriculumContext, Goals, Constraints, history | Mutate Twin; invent Curriculum; recompute readiness |
| **Validate / scope** | Sitting / curriculum identity coherence; V1/V2 format awareness | Invent Mid readiness when sparse |
| **Interpret readiness** | Use factors/warrant/disagreement as context | Select via “readiness said do X”; coerce unknown → Mid/High |
| **Nominate candidates** | Produce curriculum-bound alternatives with attribution hooks | Invent topics; treat streaks as value |
| **Order / constrain** | Apply educational priority posture and feasibility demotion | Erase high-weight need via feasibility alone |
| **Select** | Choose highest-value feasible action (structural rules) | Opaque selection without candidates/reasons |
| **Author reasons** | Emit stable reason codes + lineage | Invent evidence or disagree with inputs |
| **Emit** | Frozen Decision | Write Twin beliefs; generate missions; package recommendations |

## 7.4 Structural selection posture (no formulas)

First ship uses **presence / tension / warrant visibility** rules, for example:

| Condition | Example selection posture |
|---|---|
| Cold start / `not_yet_knowable` / low warrant | Prefer diagnostic / evidence-creating candidate on high-weight identity |
| Supportive Knowledge + risk-elevating Memory | Prefer revise on high-weight stale identity; keep disagreement in reason codes |
| Strong Behaviour + unknown/thin Assessment Performance | Prefer assess / diagnostic within feasible intensity |
| High time pressure + high-weight Knowledge gap | Prefer study/coverage on high-weight identity over low-weight polish |
| Burnout / feasibility risk + real educational need | Prefer smaller high-value or rest/protect-intensity; keep need visible |
| Empty candidate nomination | Still emit Decision with diagnostic/evidence-creating fallback + honest low-warrant reasons — never empty “do anything” |

Exact nomination mapping is an implementation detail; **forbidden** mappings are binding: unknown readiness → Mid polish; streaks → learning value; Confidence → mastery upgrade; readiness overall → action chooser.

## 7.5 Explicit non-computations (first ship)

Must **not**:

- Compute ranking scores, weighted averages, or optimization objectives  
- Recompute readiness factors or overall posture  
- Fill empty Twin belief bags  
- Generate missions or recommendation titles  
- Persist Decision State / Journal  
- Import or call `RecommendationService`  
- Call LLM / network for selection  

## 7.6 CurriculumContext + V1/V2

| Format | Structural behaviour |
|---|---|
| **V1** | Topic-weighted nomination; no Section requirement |
| **V2** | May scope candidates to section-aware identities when present; same action-family catalogue |
| **Both** | Same cold-start / warrant / candidate-set contracts |

Reuse `app.domain.readiness.CurriculumContext` — do not fork.

## 7.7 Constraint handling (binding)

1. Constraints **bound ambition**; they do not invent educational need.  
2. Demotions appear as candidate status + acknowledgements — not silent deletion of need.  
3. Behaviour sustainability is feasibility, not learning value.  
4. Rest / protect-intensity is a first-class family when sustainability risk dominates.  
5. Unsustainable cram selections despite Behaviour risk are fidelity failures; “rest always” despite high-weight exam risk is equally a failure.

---

# 8. Decision explanation contract

## 8.1 Mandatory chain

Every educational next-action Decision must support **Why?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → (later) Recommendation explanation (Capability 2.9 packaging)
```

## 8.2 Layer obligations (structural)

| Layer | Obligation on `Decision` |
|---|---|
| **Curriculum** | Selected/candidates cite official identity / weight context — never invented topics |
| **Evidence** | Lineage may cite evidence ids when Twin exposes them |
| **Twin** | Lineage cites domain factors that nominated candidates |
| **Readiness** | Reason codes that cite readiness inherit warrant; never narrate supportive Knowledge Strength as exam readiness |
| **Decision** | Reason codes + selected vs considered candidates + constraint acknowledgements always present |
| **Recommendation (2.9)** | Out of scope — must later package without inventing disagreeing ranking |

## 8.3 Attribution requirements (testable)

1. Selected action cites ≥1 reason code tied to Twin / Readiness / Curriculum / Constraints inputs.  
2. Candidate set supports “why not the alternative?” without post-hoc invention.  
3. Warrant honesty appears whenever readiness overall is unknown / low-warrant / `not_yet_knowable`.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. Factor disagreement (e.g. High Knowledge + Low Memory) remains explicit in reason codes when that tension nominates revise.  

## 8.4 Forbidden explanation patterns (reject in review/tests)

- Single opaque “recommended for you” without reason codes  
- Explanations that cite UI labels but not Twin/evidence lineage  
- LLM-generated rationales as selection authority  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory into a bland Mid story  
- Treating dismissals as proof the topic is mastered  
- Packaging fields that disagree with Decision reason codes (when 2.9 exists — not in this ship)

## 8.5 Audit artefacts (this ship)

| Artefact | Role in structural ship |
|---|---|
| `Decision` | Candidates + selected action + reason codes + lineage |
| Twin / Readiness inputs | Unchanged; cited only |
| Decision State / Journal / Recommendation / Mission | Deferred — document hooks only |

---

# 9. Public API impact

## 9.1 New exports (additive)

From `app.domain.decision` (names illustrative but should be stable once shipped):

| Symbol | Kind |
|---|---|
| `Decision` | Frozen dataclass |
| `SelectedAction` / `CandidateAction` | Frozen dataclasses |
| `ActionFamily` / catalogue constants | Stable identities |
| `ReasonCodeId` / reason catalogue | Stable identities |
| `Constraints` | Frozen value object |
| `DecisionEngine` (or `evaluate_decision`) | Pure evaluate API |
| Optional: `DecisionHistory`, `DecisionLineage`, `ConstraintAcknowledgement` | Supporting types |

Prefer explicit `app.domain.decision` imports. Do not force Twin write-path packages to import decision.

## 9.2 Unchanged interfaces

| Contract | Impact |
|---|---|
| `TwinUpdatePipeline` / Update Strategies | Unchanged — Decision is not registered as a strategy |
| `DigitalTwin` fields | Unchanged (no required decision domain field) |
| `ReadinessAggregation` / `ReadinessState` | Unchanged — consumed as input |
| `CurriculumContext` | Reused from readiness package |
| `LearningEvidence` / `EvidenceType` | Unchanged |
| HTTP / Flask / `RecommendationService` | No product API change required in this capability |
| ORM / Alembic | None |

## 9.3 API compatibility rules

- Additive domain package only.  
- No breaking renames of Twin write domains or readiness types.  
- Callers that never import decision continue to work.  
- Future Recommendation (2.9) and Mission (2.10) depend on this API; keep action families and reason-code ids stable once published.  
- Decision Engine must not expose “select via readiness” shortcuts that bypass candidate/reason contracts.

---

# 10. Testing strategy

Target module: `tests/test_decision_engine.py`.

## 10.1 Suites

| Suite | Assertions |
|---|---|
| **Contract** | `evaluate` returns `Decision` with selected action, non-empty candidate set, ≥1 reason code; frozen/immutable |
| **Purity** | Input Twin and ReadinessState unchanged after evaluate; no strategy registration side effects |
| **Determinism** | Same Twin + ReadinessState + CurriculumContext + Constraints → equal structural fields |
| **Cold start** | Goals-only / not-yet-knowable readiness → diagnostic/evidence-creating preference; reason codes state low warrant; never Mid preparedness coercion |
| **Candidate set mandatory** | Opaque single-action without alternatives fails contract tests |
| **Selected ∈ set** | Selected action present in (or explicitly derived from) candidates |
| **Constraint demotion visible** | Feasibility-limited runs keep demoted candidates + acknowledgements |
| **High Knowledge + Low Memory** | Prefer revise-shaped posture; disagreement reason codes preserved |
| **High Behaviour + Low Performance** | Prefer assess/diagnostic within feasibility; streaks do not unlock “ready polish” |
| **Confidence risk framing** | Confidence-shaped inputs (if present) do not upgrade to exam-rehearsal-only as mastery |
| **Readiness firewall** | Engine does not recompute readiness; does not coerce unknown → Mid/High; no “readiness said do X” API |
| **Curriculum V1 context** | Flat topic-weighted context evaluates without Section ids |
| **Curriculum V2 context** | Section-aware context evaluates; same action-family catalogue |
| **No Twin mutation** | Knowledge/Memory/Behaviour/Performance equality before/after |
| **Framework purity** | AST/import ban for Flask/SQLAlchemy (same pattern as readiness/strategy tests) |
| **Non-scoring** | No required ranking float / optimization objective fields |
| **Lineage presence** | Decision cites Twin domains and curriculum entities used |
| **Firewall** | Module does not import Recommendation/Mission services; does not import Update Strategies for writes |
| **Educational priority posture** | High-weight gap preferred over low-weight polish under scarcity-shaped fixtures (structural, not numeric) |

## 10.2 Fixture strategy

- Build minimal `DigitalTwin` via existing `*.create()` helpers.  
- Build `CurriculumContext` + `ReadinessState` via readiness fixtures / `ReadinessAggregation.derive` for coherent readiness inputs.  
- Prefer structural emptiness and disagreement fixtures over mocking ORM.  
- Constraints fixtures: ample time vs scarce time vs burnout/protect-intensity.

## 10.3 Regression

- Existing Twin strategy suites remain green.  
- Existing readiness aggregation suite remains green.  
- No curriculum engine test changes expected.  
- Suggested command:  
  `python -m pytest tests/test_decision_engine.py tests/test_readiness_aggregation.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py tests/test_behaviour_update_strategy.py tests/test_performance_update_strategy.py -v`  
  and `ruff check app/ tests/`

## 10.4 Out of test scope for this capability

- HTTP / recommendation UI integration  
- Persistence / Decision State round-trips  
- Numeric ranking correctness  
- Mission generation behaviour  
- Legacy `RecommendationService` parity goldens (document divergence as transitional debt; do not force equality)  
- LLM narration  

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
| Legacy recommendation tables | **None** — no cutover in this ship |

Twin, readiness, and decision domain remain in-memory / framework-free. If a later milestone persists Decision State, that is a separate schema plan — not Capability 2.8 structural evaluation.

**Expected answer for this capability: None.**

---

# 12. Backwards compatibility

| Invariant | Confirmation |
|---|---|
| **Twin write path unaffected** | Pipeline and K→M→B→P strategies unchanged |
| **DigitalTwin shape compatible** | No required decision field added |
| **Readiness Aggregation unaffected** | Consumed as context; not rewritten |
| **Curriculum V1/V2 unaffected** | No traversal redesign; context object reuse only |
| **Legacy `RecommendationService` continues** | Coexistence Stage A — not deleted or secretly replaced |
| **No third live ranker forced into UI** | Domain Decision ships; presentation cutover deferred |
| **Evidence append-only** | Preserved |
| **Deterministic cores** | No LLM/network in evaluate path |
| **Confidence separability** | Risk framing only; not mastery/readiness upgrade |

### Legacy convergence posture for this ship

Remain at **Stage A — Coexistence (documented)** per Decision architecture §12:

- Twin-first Decision Engine exists in domain.  
- Legacy `RecommendationService` continues for existing surfaces.  
- Do not deepen TopicProgress recommendation formulas.  
- Do not invent hybrid averages of legacy ranks + Twin Decision as temporary authority.  
- Dual truth must remain **named** — not papered over as one score.  

Stages B–D (adapters, Twin-first product authority, retirement of divergent math) are **out of scope**.

---

# 13. Educational Fidelity Review

Verify the following remain true after structural implementation:

| Fidelity check | Required outcome |
|---|---|
| **Decision never owns evidence as belief authority** | Engine only cites lineage; never appends Learning Evidence |
| **Decision never updates the Twin** | Input Twin domains identical after evaluate |
| **Decision never invents beliefs or syllabus** | Empty beliefs stay empty; curriculum ids only from CurriculumContext |
| **Decision never coerces unknown readiness** | Inherits warrant; cold start prefers diagnostics / evidence-creating actions |
| **Decision always remains explainable** | Reason codes + candidates + lineage mandatory |
| **Learning value over activity theatre** | Behaviour/constraints bound feasibility; streaks do not define value |
| **Readiness ≠ Decision** | No action selection inside readiness package; Decision consumes context only |
| **Decision ≠ Recommendation packaging** | No titles/urgency badges as authority |
| **Decision ≠ Missions** | No mission generation |
| **Factor disagreement preserved** | High Knowledge + Low Memory style tensions remain visible in reasons |
| **Constraints do not erase need** | Demotion visible; high-weight risk remains attributable |
| **Confidence ≠ mastery** | Self-report cannot unlock exam-rehearsal-only as mastery upgrade |
| **V1/V2 honesty parity** | Same cold-start / candidate / warrant contracts on both formats |
| **Explainability spine** | Curriculum → Evidence → Twin → Readiness → Reason codes chain supportable |

### Anti-fidelity patterns to reject in review

| Pattern | Reject because |
|---|---|
| Cold-start Mid readiness used to justify advanced rehearsal | Fabricates preparedness |
| Mission week / streaks ⇒ harder polish content | Activity theatre |
| Confidence slider upgrades next-action aggressiveness as mastery | Contamination |
| Opaque Decision without candidates/reasons | Product thesis failure |
| Engine writes Twin to “have something to select” | Write/read firewall breach |
| “Readiness said do X” API | Wrong owner |
| Rest never allowed despite burnout flags | Feasibility denial |
| Rest always preferred despite high-weight exam risk | Avoidance theatre |
| RecommendationService hybrid rank as temporary Twin Decision | Dual-authority lie |

---

# 14. Acceptance criteria

Capability 2.8 structural implementation is accepted when all of the following hold:

1. **`app/domain/decision/` exists** as framework-free domain code with `evaluate` (or equivalent) producing `Decision`.  
2. **`Decision` is explainable by construction** — selected action, mandatory candidate set, ≥1 reason code, lineage hooks.  
3. **Evaluation is read-side only** — Twin domains unchanged; ReadinessState unchanged; no Update Strategy registration for Decision beliefs.  
4. **Cold-start contract** — low-warrant / `not_yet_knowable` → evidence-creating / diagnostic preference; never Mid/High readiness coercion.  
5. **Readiness firewall** — `ReadinessState` is context only; engine does not recompute competing readiness or select via readiness alone.  
6. **Constraint acknowledgements** — feasibility demotions remain visible; educational need not silently erased.  
7. **CurriculumContext** reused from readiness package; V1 and V2 fixtures evaluate without requiring Sections globally.  
8. **No scoring formulas / optimization / Recommendation packaging / Mission generation / Flask services / migrations** in the Capability 2.8 structural PR unless explicitly re-scoped.  
9. **Public exports** documented; Twin README clarifies Decision as read-side selector.  
10. **Tests green** for decision suite + readiness + Twin strategy regressions; ruff clean on touched paths.  
11. **Hard educational rules** remain true: Activity ≠ learning value; Confidence ≠ mastery; Readiness ≠ Decision; Decision ≠ Recommendation; Decision ≠ Missions.  
12. **Legacy coexistence** — `RecommendationService` not deleted; no hybrid averaging adapter shipped as “temporary truth.”

---

# 15. Definition of Done

A Capability 2.8 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; deferred items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] `Decision` model matches §4 (read-side, immutable, explainable, no required Twin field)  
- [ ] Candidate representation matches §5 (mandatory set; separable action families; visible demotion)  
- [ ] Reason code representation matches §6 (stable catalogue; Decision authorship only)  
- [ ] Evaluation flow matches §7 (pure evaluate; readiness context only; no Twin writes; no formulas)  
- [ ] Explanation contract matches §8 (chain supportable; forbidden patterns rejected)  
- [ ] Public API impact is additive only (§9)  
- [ ] Testing strategy §10 executed and green  
- [ ] Migration impact is None (§11) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §12 hold (Twin write path, readiness, V1/V2, legacy coexistence)  
- [ ] Educational fidelity review §13 verified by tests and review  
- [ ] Acceptance criteria §14 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No Recommendation Engine, Mission Generation, Decision State ORM, numeric ranking, or `RecommendationService` deletion shipped under this capability label  

**Stop after Capability 2.8 structural ship + review.** Do not start Capability 2.9 / 2.10 in the same change set unless separately requested.

---

# 16. Recommended Implementation Sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read 2.8.1 analysis + 2.8.2 architecture + this plan | Shared understanding; readiness firewall confirmed |
| **1** | Lock action-family + reason-code vocabulary in PR description | Catalogues listed; Mid coercion forbidden |
| **2** | Implement `action_types.py` + `reason_codes.py` + `candidate.py` + `constraints.py` + `decision.py` | Types import cleanly; frozen |
| **3** | Implement `engine.py` cold-start + low-warrant paths first | not-yet-knowable → diagnostic/evidence-creating + honest reasons |
| **4** | Implement nomination for study / revise / assess / rest families | Candidate set always present; demotions visible |
| **5** | Implement priority posture + constraint acknowledgements | Disagreement preserved; need not erased |
| **6** | Wire lineage + warrant inheritance on readiness-citing codes | Warrant honesty assertable |
| **7** | Export package + update Twin README (+ readiness docstring if needed) | Read-side ownership clear |
| **8** | Write `tests/test_decision_engine.py` | Suite green |
| **9** | Run readiness + Twin strategy regressions + ruff | No regressions |
| **10** | Capability review against §14 + fidelity §13 | Checklist complete |
| **11** | Completion report + stop | Do not start 2.9 / 2.10 |

### Suggested PR shape

- **Title:** `feat: structural Decision Engine (read-side, explainable)`  
- **Body:** link this plan + 2.8.1/2.8.2; state readiness firewall; migration None; V1/V2 via CurriculumContext reuse; note deferred numeric ranking, Decision State persistence, Recommendation packaging, Mission projection, and legacy cutover  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring/selection formulas, Recommendation Engine, Mission Generation, or UI.

Next engineering step (separate milestone): execute §16 steps 1–11 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains consumed without modification |
| 2.7 | Readiness Aggregation | Supplies `ReadinessState` context; firewall preserved |
| **2.8.1** | Decision Engine Educational Analysis | Approved educational charter |
| **2.8.2** | Decision Engine Architecture | Approved structural contracts |
| **2.8.3** | **Decision Engine Implementation Plan** | **This document** |
| 2.8 impl | Structural evaluation | Separate milestone after this plan |
| 2.9–2.10 | Recommendation / Missions | Package / project Decision later; not in this ship |

---

# Appendix B — Risks carried into implementation

| Risk | Mitigation in implementation |
|---|---|
| Treating Decision as write domain | Separate package; no Twin field; no Update Strategy |
| Readiness → Decision conflation | Context-only input; firewall tests; no action chooser API on readiness |
| Opaque selection | Mandatory candidates + reason codes from first ship |
| Mid defaults under cold start | Explicit tests; forbidden postures in review |
| Averaging disagreement away | Keep revise vs study separable; disagreement reason codes |
| Confidence contamination | Risk-framing codes only; fidelity tests |
| Constraints erase need | Demotion visible; acknowledgements required |
| V1 Section hard-requirement | CurriculumContext format branching; V1 fixture tests |
| Legacy dual truth deepening | Stage A only; no hybrid adapters |
| Premature scoring | Structural postures only |
| Recommendation invents ranking | No 2.9 packaging in this ship |
| Mission rows as mastery | No mission generation in this ship |
| LLM ownership creep | Framework purity + no network selection |

---

# Appendix C — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.8.3 — Decision Engine Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; CurriculumContext reuse planned; no traversal redesign |
| Application code intentionally untouched | Yes (this milestone) |
| Upstream gate | Readiness Architecture Review — APPROVED WITH CONDITIONS — encoded in prior 2.8 docs and herein |
| Preceded by | 2.8.1 Educational Analysis + 2.8.2 Architecture (approved) |
| Next | Structural Decision Engine implementation → tests → capability review |

---

*End of Capability 2.8.3 Decision Engine Implementation Plan. STOP.*
