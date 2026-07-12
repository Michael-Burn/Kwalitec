# Capability 2.9.3 — Recommendation Engine Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.9 Explainable Recommendation Engine (structural read-side packaging implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
**Recommendation architecture:** [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md)  
**Upstream gate:** Educational Reasoning Review — APPROVED WITH CONDITIONS ([`docs/reviews/EDUCATIONAL_REASONING_REVIEW.md`](../reviews/EDUCATIONAL_REASONING_REVIEW.md))  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_IMPLEMENTATION_PLAN.md`](CAPABILITY_2_8_DECISION_ENGINE_IMPLEMENTATION_PLAN.md), [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`), Decision package (`app/domain/decision/`), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Plan the first structural **read-side packaging** ship of Recommendation Engine — **no code, tests, migrations, services, or ranking/scoring formulas in this document’s milestone**

---

## Document purpose

This plan translates the approved Recommendation Engine educational analysis and architecture into a concrete, executable implementation sequence for Capability 2.9.

It answers:

1. What is in / out of scope for the first Recommendation Engine ship  
2. Which files to create and modify  
3. How Recommendation, reasons, warrant posture, and journal affordances must be represented  
4. How the projection pipeline and explanation contract must work  
5. Public API, testing, migration, compatibility, fidelity, and acceptance gates  

**Hard architectural rules (binding):**

1. Recommendation Engine never selects or re-selects next actions.  
2. Recommendation Engine never invents ranking that disagrees with Decision reason codes.  
3. Recommendation Engine never mutates Twin belief domains.  
4. Recommendation Engine never recomputes readiness or coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
5. Recommendation Engine never invents curriculum identities, evidence ids, or Twin beliefs.  
6. Every Recommendation must be attributable to exactly one Decision and walk the mandatory explainability chain.  
7. Accepting a Recommendation does not grant mastery; completion / assessment evidence does.  
8. Curriculum V1 and V2 remain loadable; presented identities come only from Decision / Curriculum lineage.

**Governing principle:** Recommendation remains a projection of Decision — explainably, deterministically in the core attribution path, and without engagement theatre.  
**Structural discipline:** Structure, narration fidelity, warrant honesty, and journal affordances first; copy polish and coach phrasing later. No ranking ever inside this layer.

**Non-goals of this document**

- Implementing packaging or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Ranking formulas, selection math, priority scores, match %, or optimization objectives  
- UI, analytics cutover, gamification, notifications, or coach/LLM phrasing models  
- Mission Generation Intelligence design beyond projection boundaries (Capability 2.10)  
- Refactoring or deleting legacy `RecommendationService`  
- Decision Journal ORM / persistence schema  
- Full Decision State materialisation UX  

---

# 1. Scope

## 1.1 In scope (Capability 2.9 structural ship)

| Item | Intent |
|---|---|
| **`Recommendation` + supporting value types** | Immutable, framework-free packaging result — not a Twin write-domain peer |
| **Actionable suggestion surface** | Project Decision selected action (family + curriculum scope) into a student-facing suggestion — no re-selection |
| **Recommendation Reasons** | Narration slots mapped 1:N to Decision reason codes — not a private ranking vocabulary |
| **Explanation chain presentation** | Structural chain layers: Curriculum → Evidence → Twin → Readiness (when cited) → Decision → Recommendation |
| **Warrant / Recommendation Confidence posture** | Inherit Decision warrant honesty into packaging confidence — distinct from self-report Confidence and Mastery |
| **Urgency / duration presentation** | Communication of Decision-derived feasibility — not an independent priority optimizer |
| **Candidate contrast** | “Why not Y?” drawn only from Decision candidate set |
| **Response affordances** | Accept / dismiss / defer as journalable outcomes (structural hooks — not mastery writes) |
| **`RecommendationEngine.package(...)`** | Pure read-side function/class: Decision (+ optional communication context) → `Recommendation` |
| **Projection pipeline skeleton** | Bind → validate → project suggestion → package explanation → propagate warrant → urgency → contrast → affordances → emit |
| **Cold-start communication posture** | Preserve diagnostic / evidence-creating honesty; never Mid/High preparedness theatre |
| **Student context adaptation (communication only)** | Goals / Decision-carried constraints / journal history shape phrasing — never change selected action |
| **Package exports + domain docs** | Public domain surface; Twin / Decision READMEs note Recommendation as read-side packaging |
| **Focused unit tests** | Package fidelity, warrant inheritance, explanation contract, cold start, V1/V2, immutability, purity, firewall |

## 1.2 Explicitly deferred

| Item | Why deferred |
|---|---|
| Numeric packaging scores / match % | Forbidden as educational authority; never a secret ranker |
| Coach / LLM phrasing models | Narration assistance later; core attribution must not depend on LLM |
| Exact UX copy templates / components | Presentation polish after structural contracts |
| Decision Journal persistence / ORM | Affordance hooks first; product recording path later |
| Mission generation (2.10) | Sibling projection; packaging ≠ day composition |
| Legacy `RecommendationService` cutover | Convergence Stage A coexistence only (§12) |
| Batch packaging of Decision sequences | May land later; ordering authority remains Decision |
| Flask services, blueprints, ORM, Alembic | Domain layer only for this capability |
| Curriculum Engine traversal redesign | Packaging consumes Decision lineage; does not invent syllabus |
| Adapters that hybrid-average legacy ranks with Twin Decision packaging | Forbidden temporary third truth |
| CurriculumContext production builder | Orchestration follow-up before live consumers needing syllabus beyond Decision-carried ids |

## 1.3 Success shape

After implementation:

```
Decision
  - selected action
  - candidate set
  - reason codes + lineage + warrant posture
  - constraint acknowledgements
        +
Optional communication context
  (Goals scope language, journal history, Decision-cited Confidence framing)
        ↓
RecommendationEngine.package(...)
        ↓
Recommendation
  - Decision reference (selection authority)
  - actionable suggestion (projected, not re-selected)
  - Recommendation Reasons (narrate Decision codes)
  - explanation chain presentation
  - lineage citations (from Decision only)
  - Recommendation Confidence / warrant honesty
  - urgency / duration presentation
  - candidate contrast (from Decision candidates)
  - response affordances (accept / dismiss / defer)
        ↓
(consumers later: Decision Journal recording / Mission 2.10 / product surfaces)
```

Same Decision (+ same bound communication context) → same attributable `Recommendation`. No Twin mutation. No readiness recomputation. No re-selection. No ranking formulas. No Flask. No migrations. No missions.

## 1.4 Package placement (locked recommendation)

Prefer a **sibling domain package**, not a Twin write-domain module and not a Decision submodule that blurs selection with packaging:

| Path root | Rationale |
|---|---|
| **`app/domain/recommendation/`** | Makes read-side packaging ownership obvious; mirrors `app/domain/readiness/` and `app/domain/decision/`; avoids implying Recommendation is a belief domain or a second Decision Engine |

Do **not** add `recommendation: Recommendation` as a required field on `DigitalTwin` in this ship. Live packaging is derived on read from a Decision.

**Reuse:** Import `Decision`, `SelectedAction`, `CandidateAction`, `ReasonCodeRef`, `DecisionWarrantPosture`, and related types from `app.domain.decision` — do not fork selection types. Recommendation may define thin communication-context value objects local to `app/domain/recommendation/`.

---

# 2. Files to create

| Path | Role |
|---|---|
| `app/domain/recommendation/__init__.py` | Package exports: `Recommendation`, supporting types, `RecommendationEngine` |
| `app/domain/recommendation/recommendation.py` | Frozen `Recommendation` (+ Decision reference, suggestion, reasons, chain, warrant, urgency, contrast, affordances) |
| `app/domain/recommendation/suggestion.py` | Frozen actionable suggestion projected from `SelectedAction` (family + curriculum scope + structural presentation tags) |
| `app/domain/recommendation/reasons.py` | Frozen `RecommendationReason` (+ mapping to Decision reason-code identities; chain layer tags) |
| `app/domain/recommendation/explanation.py` | Frozen explanation-chain presentation slots (Curriculum / Evidence / Twin / Readiness / Decision layers) |
| `app/domain/recommendation/warrant.py` | Recommendation Confidence / warrant posture vocabulary (inherits Decision warrant honesty) |
| `app/domain/recommendation/affordances.py` | Accept / dismiss / defer response affordance types (+ structural journal linkage hooks) |
| `app/domain/recommendation/context.py` | Optional communication-context VO (Goals language, journal history refs, Decision-cited Confidence framing) |
| `app/domain/recommendation/engine.py` | `RecommendationEngine` (or `package_recommendation`) — pure package path |
| `tests/test_recommendation_engine.py` | Unit + fidelity + cold-start + V1/V2-context + firewall suite |

Optional (only if it keeps `engine.py` readable without inventing ranking):

| Path | Role |
|---|---|
| `app/domain/recommendation/contrast.py` | Pure helpers that project candidate contrast from Decision candidate set |
| `app/domain/recommendation/narration.py` | Structural narration tags / templates keyed by Decision reason-code family — no free-text LLM authority |

Do **not** create in this capability: services, blueprints, migrations, scoring modules, Mission Intelligence, Decision Journal ORM, or adapters that rewrite `RecommendationService`.

---

# 3. Files to modify

| Path | Why it must change |
|---|---|
| `app/domain/twin/README.md` | Document Recommendation Engine as **read-side packaging** of Decision; clarify it is not a write strategy, not a selector, and not Mission generation; point to `app/domain/recommendation/` |
| `app/domain/decision/__init__.py` | Docstring clarification only if needed: Decision selects; Recommendation packages; Decision does not own product titles |
| `app/domain/__init__.py` | Optional docstring note that recommendation is a domain package (only if the package already advertises subdomains) |

**Do not modify (this capability)**

- `app/domain/decision/engine.py` selection algorithms or reason-code authorship  
- `app/domain/twin/update_pipeline.py` algorithms or registration defaults  
- Knowledge / Memory / Behaviour / Performance strategies or frozensets  
- `DigitalTwin` aggregate shape (no required `recommendation` field)  
- `app/domain/readiness/aggregation.py` factor math or overall posture rules  
- `app/services/recommendation_service.py`, readiness service, analytics/dashboard blueprints  
- Evidence catalogue, Curriculum JSON, Alembic, Flask app factory  

**Caller note (documentation only in README):** future services that need live Recommendations must obtain a `Decision` first via `DecisionEngine.evaluate(...)`, then call `RecommendationEngine.package(decision, ...)`. Packaging must not call Decision Engine as a hidden re-selection path, must not re-derive readiness, and must not mutate Twin. Orchestration that needs syllabus beyond Decision-carried identities must build `CurriculumContext` via `CurriculumService` helpers **outside** the domain package before Decision evaluation — same pattern as Readiness / Decision.

---

# 4. Recommendation model

## 4.1 Classification (keep)

| Property | Requirement |
|---|---|
| **Read-side** | Produced by projecting a Decision (+ optional communication context) |
| **Decision-bound** | Every Recommendation cites exactly one Decision as selection authority |
| **Immutable** | Frozen dataclasses; one packaging evaluation per input set |
| **Explainable by construction** | Completes mandatory explainability chain; narrates Decision reason codes |
| **Curriculum-bound** | Curriculum-scoped suggestions use official syllabus identities from Decision only |
| **Warrant-honest** | Evidence Warrant / cold-start posture survives into Recommendation Confidence and tone |
| **Non-authoritative for beliefs** | Accept does not grant mastery; journal outcomes become preference / intent evidence |
| **Not selection authority** | Decision Engine alone selects; Recommendation never re-ranks |
| **Not Mission** | Outputs Recommendation only — not Mission / MissionTask artefacts |

## 4.2 Conceptual slots → structural fields

| Architecture slot | Planned structural representation |
|---|---|
| **Decision reference** | Identity / evaluation hooks from Decision (`evaluation_id`, `engine_version`, scope) — selection authority citation |
| **Actionable suggestion** | Projected from `SelectedAction` (action family + optional curriculum entity id + intent tags) |
| **Recommendation Reasons** | Frozen tuple of reasons; each maps to ≥1 Decision `ReasonCodeRef` / code identity |
| **Explanation chain presentation** | Layered presentation object with Curriculum / Evidence / Twin / Readiness (optional) / Decision slots |
| **Lineage citations** | Copied/cited from `Decision.lineage` — never fabricated |
| **Warrant / Recommendation Confidence posture** | Inherited from `Decision.warrant_posture` (+ structural honesty band) |
| **Urgency / duration presentation** | Structural tags derived from Decision constraint acknowledgements / feasibility — not a priority score |
| **Candidate contrast** | Frozen contrasts built only from Decision `candidates` (status + attribution) |
| **Response affordances** | Accept / dismiss / defer as enum + journal linkage hooks |
| **Evaluation context** | Packaging version + Decision engine / reason-code vocabulary version tags for audit |

## 4.3 Recommended types (structural, not schema-locked)

Illustrative shapes for implementers (names may be refined; meanings are binding):

```
ActionableSuggestion
  family: ActionFamily          # from Decision SelectedAction — not re-chosen
  curriculum_entity_id: str | None
  intent_tags: ...              # structural — coverage_gap | retention_risk | diagnostic | …
  presentation_tags: ...        # structural communication tags — not marketing slogans

RecommendationReason
  reason_id: ...                # packaging reason identity (versionable)
  decision_reason_codes: ...    # maps to Decision ReasonCodeId / ReasonCodeRef
  chain_layers: ...             # which explainability layers this reason narrates
  tension_tags: ...             # preserve Knowledge vs Memory etc. — never collapse

ExplanationChainPresentation
  curriculum: ...               # from Decision lineage / selected scope
  evidence: ...                 # evidence ids or honest absence under cold start
  twin: ...                     # domain factors Decision cited
  readiness: ... | None         # only when Decision cites readiness
  decision: ...                 # selected vs candidates + reason codes + acknowledgements

RecommendationConfidencePosture
  # inherits Decision warrant honesty
  # low / cold_start / not_yet_knowable must remain first-class
  # distinct from self-report Confidence and Mastery

CandidateContrast
  rejected_or_considered: ...   # from Decision candidates only
  status: CandidateStatus       # considered / demoted / blocked — never invented

ResponseAffordance
  outcomes: accept | dismiss | defer
  journal_linkage_hooks: ...    # structural — preference/intent only

Recommendation
  decision_ref: ...
  suggestion: ActionableSuggestion
  reasons: tuple[RecommendationReason, ...]
  explanation_chain: ExplanationChainPresentation
  lineage: ...                  # cited from Decision
  confidence_posture: RecommendationConfidencePosture
  urgency_duration: ...
  candidate_contrast: tuple[CandidateContrast, ...]
  affordances: ...
  packaging_version: ...
  decision_engine_version: ...
  reason_code_vocabulary_version: ...
```

## 4.4 What must not be added now

- Required numeric `score: float` / `match_percent` as educational authority  
- Mutating methods that write Twin domains or append Evidence  
- Re-selection among Decision candidates  
- Mission / MissionTask fields  
- Parallel TopicProgress-backed “next topic” as Twin / Decision substitute  
- Private packaging reason codes that disagree with Decision reason codes  
- Coerced Mid/High readiness or inflated Recommendation Confidence under thin warrant  
- LLM-authored free-text as selection or lineage authority  

## 4.5 Recommendation vs Decision vs Mission

| Artefact | First structural ship |
|---|---|
| **Decision** | **Upstream input** — already owned by `app/domain/decision/` |
| **Recommendation** | **In scope** — live packaging output |
| **Decision Journal persistence** | **Out of scope for ORM** — affordance hooks only |
| **Mission / MissionTask** | **Out of scope** — Capability 2.10 |

---

# 5. Projection pipeline

## 5.1 Entry contract

```
RecommendationEngine.package(
    decision: Decision,
    *,
    communication_context: RecommendationContext | None = None,
) -> Recommendation
```

Binding rules:

1. **Decision is the sole selection authority** — packaging never re-ranks or re-selects.  
2. **Observational only** — read Decision (+ optional context); never call Update Strategies; never mutate Twin; never recompute readiness; never call `DecisionEngine.evaluate` as a hidden side path that could diverge.  
3. **Single Decision** — one Decision → one Recommendation on the core educational path.  
4. **Deterministic attribution** — same Decision (+ same bound context) → equal attributable structural fields. Presentation template choice may be versioned; educational authority must not vary.  
5. **Framework-free** — no Flask, SQLAlchemy, request/session, network, or required LLM.  

## 5.2 Pipeline stages (structural)

```
1. Bind Decision
        ↓
2. Validate projection preconditions
   (selected action present; reason codes present; lineage hooks; warrant posture)
        ↓
3. Project actionable suggestion
   (action family + curriculum identity from Decision — no re-selection)
        ↓
4. Package explanation chain
   (Curriculum → Evidence → Twin → Readiness when cited → Decision reason codes)
        ↓
5. Propagate warrant / Recommendation Confidence posture
        ↓
6. Present urgency / duration from Decision-derived feasibility
        ↓
7. Attach candidate contrast (from Decision candidate set)
        ↓
8. Attach response affordances (accept / dismiss / defer)
        ↓
9. Apply communication-context adaptation (phrasing tags only)
        ↓
Recommendation
```

## 5.3 Stage responsibilities

| Stage | Owns | Must not |
|---|---|---|
| **Bind Decision** | One Decision is sole selection authority | Package without Decision; invent a Decision |
| **Validate preconditions** | Require selected action + ≥1 reason code; warrant posture present | Opaque suggestions without codes |
| **Project suggestion** | Map `SelectedAction` → `ActionableSuggestion` | Re-select among candidates; invent topics |
| **Package explanation** | Narrate Decision reason codes + chain layers | Invent evidence, syllabus, Twin beliefs, or disagreeing codes |
| **Propagate warrant** | Carry Decision warrant / cold-start honesty into Recommendation Confidence | Mid/High preparedness theatre under thin warrant |
| **Urgency / duration** | Present Decision-derived feasibility / constraint acknowledgements | Independent priority optimizer; engagement urgency theatre |
| **Candidate contrast** | Use Decision candidate set only | Invent “why not” alternatives Decision never considered |
| **Response affordances** | Expose journalable outcomes as preference / intent | Treat accept as mastery grant |
| **Context adaptation** | Shape phrasing / affordance emphasis from Goals / journal / cited Confidence | Change selected action; invent ranking |

## 5.4 Pipeline principles (binding)

1. **Projection only** — no selection enrichment inside packaging.  
2. **One Decision → one Recommendation** on the core educational path (batches are ordered Decision packaging later; ordering authority remains Decision).  
3. **Deterministic attribution** — packaging may version presentation templates; it may not vary educational authority.  
4. **Write/read firewall** — no Twin Update Pipeline bypass; no readiness recomputation.  
5. **No ranking stage** — there is no packaging score that can change which action is suggested.  
6. **Cold-start first-class** — diagnostic / evidence-creating Decisions must remain clearly diagnostic in packaging.

## 5.5 Explicit non-computations (first ship)

Must **not**:

- Compute ranking scores, match %, weighted averages, or optimization objectives  
- Re-select or re-order Decision candidates as educational authority  
- Recompute readiness factors or overall posture  
- Fill empty Twin belief bags or fabricate evidence ids  
- Generate missions or MissionTask rows  
- Persist Decision Journal / Recommendation ORM  
- Import or deepen `RecommendationService.generate_recommendations` as Twin-first truth  
- Call LLM / network for packaging authority  

## 5.6 Curriculum V1/V2

| Format | Structural behaviour |
|---|---|
| **V1** | Topic-scoped suggestions from Decision; no Section requirement |
| **V2** | Section-aware identities when Decision carries them; same action-family catalogue |
| **Both** | Same warrant / explanation / cold-start / affordance contracts |

Packaging does not load ORM curricula. Identities come from Decision lineage / selected action only.

---

# 6. Warrant propagation

## 6.1 Definition

**Warrant propagation** is the requirement that Evidence Warrant / cold-start / `not_yet_knowable` posture on the Decision flows end-to-end into Recommendation Confidence and student-facing tone tags.

## 6.2 Propagation path

```
ReadinessState Evidence Warrant / cold-start posture
        ↓
Decision warrant posture (inherited in selection)
        ↓
Recommendation Confidence + explanation tone tags
```

## 6.3 Propagation rules (binding for implementation)

1. **Warrant is non-optional** — packaging may not strip warrant for polish.  
2. **Low warrant → low Recommendation Confidence honesty** — never inflate for engagement.  
3. **`not_yet_knowable` / `cold_start` remain first-class** — never rewritten into Mid or High preparedness narratives.  
4. **Readiness language only when Decision cites readiness** — packaging does not introduce preparedness claims Decision did not authorize.  
5. **Performance tag honesty** — string-tag heuristics must not be narrated as scored accuracy certainty.  
6. **No legacy percentage fill** — do not substitute TopicProgress / `ReadinessService` % for missing Twin warrant.

## 6.4 Recommendation Confidence (structural meaning)

| Term | Meaning | Distinct from |
|---|---|---|
| **Recommendation Confidence** | Appropriateness / evidence-density honesty of the packaged suggestion | Self-report Confidence; Mastery; Readiness overall |

Recommendation Confidence is a **communication honesty posture**, not a selection score and not calibrated student Confidence.

## 6.5 Cold-start packaging posture (binding)

| Do | Do not |
|---|---|
| Say evidence is still thin / not yet enough to judge preparedness | Claim Mid or High readiness to “motivate” |
| Frame suggestion as diagnostic / evidence-creating when Decision selected that family | Frame polish, advanced rehearsal, or “you’re nearly ready” |
| Keep Recommendation Confidence low/honest | Inflate Recommendation Confidence for engagement |
| Cite Decision cold-start / low-warrant reason codes in Recommendation Reasons | Invent Mid readiness as packaging convenience |
| Prefer curiosity / clarity tags | Shame tags for lacking history |
| Preserve curriculum weight honesty when Decision scopes high-weight first coverage | Invent a fake personalised mastery map |

---

# 7. Recommendation explanation contract

## 7.1 Definition

The **Recommendation explanation contract** is the structural obligation that packaging narrates Decision authority faithfully: selected action, reason codes, candidate contrast, constraint acknowledgements, and lineage — without inventing or contradicting them.

## 7.2 Mandatory chain

Every educational Recommendation must support **Why?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → Recommendation explanation
```

## 7.3 Contract slots (binding)

| Slot | Packaging obligation |
|---|---|
| **Selected action fidelity** | Presented action family and curriculum scope match Decision selected action |
| **Reason-code narration** | Every core Recommendation Reason maps to one or more Decision reason codes |
| **Candidate contrast** | “Why not Y?” uses Decision candidate set statuses only |
| **Constraint honesty** | Feasibility demotions remain visible; packaging does not restore demoted ambition |
| **Lineage citation** | Twin / evidence / curriculum / readiness citations come from Decision lineage |
| **Warrant inheritance** | Readiness-adjacent language inherits Decision warrant posture |
| **Version attribution** | Packaging names Decision evaluation / reason-code vocabulary / packaging version for audit |
| **Tension preservation** | High Knowledge + Low Memory (and similar) must not collapse into bland Mid copy |

## 7.4 Authorship rules (binding)

1. **Decision Engine alone authors** reason codes and selected action.  
2. **Recommendation Engine narrates**; it does not invent ranking codes that contradict the Decision.  
3. **LLM / coach may restate** chain-supported attributions later; they must not author selection or fabricate lineage in this ship.  
4. **Post-hoc stories that disagree with reason codes are forbidden.**  
5. **Accept is commitment, not competence** — affordance language must not imply mastery change.

## 7.5 Forbidden explanation contract breaches (reject in review/tests)

- Softening reason codes to remove educational tension  
- Presenting supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Dropping cold-start / low-warrant codes for friendlier engagement copy  
- Adding unofficial reason codes as if they were Decision authority  
- Narrating a different action family than Decision selected (e.g. revise → study collapse)  
- Opaque “recommended for you” without Decision reason-code mapping  
- Hybrid stories that mix legacy readiness % with Twin/Decision factors as temporary truth  
- Private packaging “match %” as educational authority  
- Inventing evidence ids, syllabus topics, or Twin beliefs  

## 7.6 Audit artefacts (this ship)

| Artefact | Role in structural ship |
|---|---|
| `Decision` (input) | Selection authority + reason codes + lineage + warrant |
| `Recommendation` (output) | Product packaging consequence — not authority |
| Twin / Readiness | Unchanged; cited only via Decision lineage |
| Decision Journal / Mission | Deferred — affordance hooks / boundary docs only |

---

# 8. Student context adaptation

## 8.1 Definition

**Student context adaptation** is communication-layer adaptation using Goals, Decision-carried Constraints, Decision Journal history, and Decision-cited Confidence framing — **without** authorizing a second selection path.

## 8.2 Adaptation catalogue

| Context | Allowed packaging use | Forbidden use |
|---|---|---|
| **Goals (sitting, capacity, deadline)** | Scope “toward the sitting” language; capacity-honest duration presentation | Change selected action; invent topics |
| **Constraints on Decision** | Present feasible ambition; explain intensity demotion | Restore demoted polish; erase high-weight need |
| **Decision Journal history** | Avoid thrashing copy; acknowledge prior dismiss respectfully | Treat dismiss as mastery; invent preference Twin writes |
| **Self-report Confidence (Decision-cited)** | Risk-framing narration only | Upgrade mastery/readiness; skip foundations |
| **Behaviour feasibility (Decision-cited)** | Sustainability language when intensity was demoted | Treat streaks as learning-value justification |

## 8.3 Adaptation principles (binding)

1. Context adapts **phrasing and affordances**, not educational authority.  
2. Adaptation must remain **deterministic for attribution** — same Decision + same bound context → same attributable meaning.  
3. Journal-aware packaging respects preference without silent Twin mutation.  
4. Capacity honesty is educational fidelity, not reduced ambition theatre.  
5. Communication context is optional; missing context must not invent Mid readiness or ranking.

## 8.4 Structural representation

Prefer a thin frozen `RecommendationContext`:

```
RecommendationContext
  goals_language_tags: ...      # sitting / capacity / deadline communication only
  journal_history_refs: ...     # prior accept/dismiss/defer identities when available
  confidence_framing: ...       # only if Decision already cited Confidence as risk
  notes: ...                    # structural — never selection overrides
```

Packaging reads this object; it never writes Twin Goals, Behaviour, or Knowledge from it.

---

# 9. Public API impact

## 9.1 New exports (additive)

From `app.domain.recommendation` (names illustrative but should be stable once shipped):

| Symbol | Kind |
|---|---|
| `Recommendation` | Frozen dataclass |
| `ActionableSuggestion` | Frozen dataclass |
| `RecommendationReason` | Frozen dataclass |
| `ExplanationChainPresentation` | Frozen dataclass |
| `RecommendationConfidencePosture` | Enum / frozen posture |
| `CandidateContrast` | Frozen dataclass |
| `ResponseAffordance` / outcome enum | Stable identities |
| `RecommendationContext` | Optional communication VO |
| `RecommendationEngine` (or `package_recommendation`) | Pure package API |
| Packaging version constant | Audit tag |

Prefer explicit `app.domain.recommendation` imports. Do not force Twin write-path packages to import recommendation.

## 9.2 Unchanged interfaces

| Contract | Impact |
|---|---|
| `DecisionEngine` / `Decision` | Unchanged — consumed as input |
| `TwinUpdatePipeline` / Update Strategies | Unchanged — Recommendation is not registered as a strategy |
| `DigitalTwin` fields | Unchanged (no required recommendation domain field) |
| `ReadinessAggregation` / `ReadinessState` | Unchanged — not recomputed by packaging |
| `CurriculumContext` | Unchanged — Decision already carries format / identities |
| `LearningEvidence` / `EvidenceType` | Unchanged |
| HTTP / Flask / `RecommendationService` | No product API change required in this capability |
| ORM / Alembic | None |

## 9.3 API compatibility rules

- Additive domain package only.  
- No breaking renames of Twin write domains, readiness types, or Decision types.  
- Callers that never import recommendation continue to work.  
- Future Mission (2.10) and product surfaces depend on this API; keep Decision-reference fields, reason mappings, and affordance identities stable once published.  
- Recommendation Engine must not expose “re-rank Decision” or “select via packaging score” shortcuts that bypass Decision authority.  
- Action families remain those authored by Decision (`ActionFamily`); packaging must not introduce a competing family catalogue.

---

# 10. Testing strategy

Target module: `tests/test_recommendation_engine.py`.

## 10.1 Suites

| Suite | Assertions |
|---|---|
| **Contract** | `package` returns `Recommendation` with Decision ref, suggestion matching selected action, ≥1 Recommendation Reason mapped to Decision codes, frozen/immutable |
| **Purity** | Input Decision unchanged after package; no Twin / readiness / strategy side effects |
| **Determinism** | Same Decision (+ same context) → equal structural fields |
| **No re-selection** | Suggestion family + curriculum id equal Decision selected action; candidates never reordered as authority |
| **Explanation contract** | Every Recommendation Reason maps to ≥1 Decision reason code; chain layers present; no invented evidence ids |
| **Candidate contrast** | Contrast entries ⊆ Decision candidate set; statuses preserved |
| **Warrant inheritance** | Cold-start / `not_yet_knowable` / low warrant Decision → honest low Recommendation Confidence; never Mid/High preparedness coercion |
| **Cold-start communication** | Diagnostic / evidence-creating Decision remains framed as diagnostic; cold-start codes survive narration |
| **Constraint honesty** | Feasibility demotions remain visible; packaging does not restore demoted ambition |
| **Tension preservation** | High Knowledge + Low Memory style Decision reasons remain visible in Recommendation Reasons |
| **Accept ≠ mastery** | Affordance docs/hooks expose preference outcomes only; no Twin write APIs |
| **Context adaptation** | Goals/journal context changes phrasing tags only — never selected action |
| **Curriculum V1 context** | Flat topic-scoped Decision packages without Section ids |
| **Curriculum V2 context** | Section-aware Decision packages; same action-family catalogue |
| **No Twin mutation** | Packaging path does not import/call Update Strategies for writes |
| **Framework purity** | AST/import ban for Flask/SQLAlchemy (same pattern as decision/readiness tests) |
| **Non-scoring** | No required ranking float / match % / optimization objective fields |
| **Firewall** | Module does not import Mission services; does not call `DecisionEngine.evaluate`; does not import Update Strategies for writes; does not average legacy `RecommendationService` ranks |
| **Mission boundary** | Output type is Recommendation only — no Mission/MissionTask fields |

## 10.2 Fixture strategy

- Build minimal `Decision` objects via Decision domain constructors / `DecisionEngine.evaluate` fixtures already used in `tests/test_decision_engine.py`.  
- Prefer structural Decision fixtures (cold start, revise-over-study tension, constraint demotion, V1/V2) over mocking ORM.  
- Communication context fixtures: none / goals-only / prior-dismiss journal — assert selection unchanged.  
- Do **not** require equality with legacy `RecommendationService` outputs.

## 10.3 Regression

- Existing Decision Engine suite remains green.  
- Existing readiness aggregation + Twin strategy suites remain green.  
- No curriculum engine test changes expected.  
- Suggested command:  
  `python -m pytest tests/test_recommendation_engine.py tests/test_decision_engine.py tests/test_readiness_aggregation.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py tests/test_behaviour_update_strategy.py tests/test_performance_update_strategy.py -v`  
  and `ruff check app/ tests/`

## 10.4 Out of test scope for this capability

- HTTP / recommendation UI integration  
- Persistence / Decision Journal round-trips  
- Numeric packaging score correctness (forbidden)  
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

Recommendation domain remains in-memory / framework-free. If a later milestone persists Decision Journal outcomes or Recommendation artefacts, that is a separate schema plan — not Capability 2.9 structural packaging.

**Expected answer for this capability: None.**

---

# 12. Backwards compatibility

| Invariant | Confirmation |
|---|---|
| **Twin write path unaffected** | Pipeline and K→M→B→P strategies unchanged |
| **DigitalTwin shape compatible** | No required recommendation field added |
| **Decision Engine unaffected** | Consumed as input; selection algorithms not rewritten by packaging |
| **Readiness Aggregation unaffected** | Not recomputed by packaging |
| **Curriculum V1/V2 unaffected** | No traversal redesign; identities via Decision lineage only |
| **Legacy `RecommendationService` continues** | Coexistence Stage A — not deleted or secretly replaced |
| **No third live ranker forced into UI** | Domain Recommendation ships; presentation cutover deferred |
| **Evidence append-only** | Preserved |
| **Deterministic cores** | No required LLM/network in package path |
| **Confidence separability** | Recommendation Confidence ≠ self-report ≠ Mastery ≠ readiness |
| **Mission boundary** | No Mission artefacts produced |

### Legacy convergence posture for this ship

Remain at **Stage A — Coexistence (documented)** per Recommendation architecture §11:

- Twin-first Decision → Recommendation packaging exists in domain.  
- Legacy `RecommendationService` continues for existing surfaces.  
- Do not deepen TopicProgress recommendation formulas.  
- Do not invent hybrid averages of legacy ranks + Twin Decision packaging as temporary authority.  
- Dual truth must remain **named** — not papered over as one score.  

Stages B–D (adapters, Twin-first product authority, retirement of divergent math) are **out of scope**.

---

# 13. Educational Fidelity Review

Verify the following remain true after structural implementation:

| Fidelity check | Required outcome |
|---|---|
| **Recommendation is a projection of Decision** | Suggestion matches selected action; no re-selection |
| **Recommendation never invents ranking** | No competing priority / match % authority |
| **Recommendation never updates the Twin** | No Update Strategy calls; no belief writes |
| **Recommendation never invents beliefs or syllabus** | Lineage and curriculum ids only from Decision |
| **Recommendation never coerces unknown readiness** | Inherits warrant; cold-start honesty mandatory |
| **Recommendation always remains explainable** | Reasons map to Decision codes; chain supportable |
| **Accept ≠ mastery** | Affordance hooks are preference / intent only |
| **Learning value over activity theatre** | Streaks do not justify Mid readiness polish in copy tags |
| **Decision ≠ Recommendation packaging** | Packaging narrates; does not select |
| **Recommendation ≠ Missions** | No mission generation |
| **Factor disagreement preserved** | Knowledge vs Memory / Behaviour vs Performance tensions remain visible |
| **Constraints do not erase need** | Demotion visible; high-weight risk remains attributable |
| **Confidence ≠ mastery** | Self-report framing cannot unlock exam-rehearsal-only as mastery upgrade |
| **V1/V2 honesty parity** | Same cold-start / warrant / explanation contracts on both formats |
| **Explainability spine** | Curriculum → Evidence → Twin → Readiness (when cited) → Decision → Recommendation chain supportable |
| **Fidelity over engagement theatre** | No Mid/High fabrication; no streak-as-readiness copy; no inflated Recommendation Confidence |

### Anti-fidelity patterns to reject in review

| Pattern | Reject because |
|---|---|
| “Recommended for you” with no reason-code mapping | Opaque; breaks Epic 2 thesis |
| Packaging re-ranks Decision candidates by engagement heuristics | Secret second Decision Engine |
| Cold-start Mid readiness used to sell advanced rehearsal | Fabricates preparedness |
| Confidence slider upgrades recommendation aggressiveness as if mastery | Contamination |
| Recommendation copy/tags that disagree with Decision reason codes | Broken explainability |
| Accept writes Knowledge/Memory directly | Evidence/Twin bypass |
| Mission generator writing private “priority scores” as mastery | Parallel authority (also out of scope) |
| Legacy hybrid % + Twin factors as temporary truth | Dual authority; untrustable |
| LLM invents evidence ids for nicer stories | Audit fraud |
| Inflated Recommendation Confidence under thin warrant | Engagement theatre |
| Revise narrated as study (or rest as failure) | Domain / action-family collapse |

---

# 14. Acceptance criteria

Capability 2.9 structural implementation is accepted when all of the following hold:

1. **`app/domain/recommendation/` exists** as framework-free domain code with `package` (or equivalent) producing `Recommendation`.  
2. **`Recommendation` is explainable by construction** — Decision reference, suggestion matching selected action, ≥1 Recommendation Reason mapped to Decision reason codes, explanation chain, lineage citations, warrant posture, response affordances.  
3. **Packaging is read-side only** — Twin domains unchanged; Decision unchanged; no Update Strategy registration for Recommendation beliefs; no readiness recomputation.  
4. **No re-selection / no ranking** — suggestion equals Decision selected action; no match % / priority score as educational authority.  
5. **Cold-start contract** — low-warrant / `not_yet_knowable` / cold-start Decisions package with honest low Recommendation Confidence and diagnostic framing when Decision selected evidence-creating actions.  
6. **Explanation contract** — every core Recommendation Reason maps to Decision reason codes; candidate contrast ⊆ Decision candidates; constraint demotions remain visible.  
7. **Student context adaptation** — communication only; never changes selected action.  
8. **Curriculum V1 and V2** Decision fixtures package without requiring Sections globally.  
9. **No scoring formulas / optimization / Mission generation / Flask services / migrations** in the Capability 2.9 structural PR unless explicitly re-scoped.  
10. **Public exports** documented; Twin README clarifies Recommendation as read-side packaging of Decision.  
11. **Tests green** for recommendation suite + decision + readiness + Twin strategy regressions; ruff clean on touched paths.  
12. **Hard educational rules** remain true: Recommendation remains a projection of Decision; Accept ≠ mastery; Recommendation Confidence ≠ self-report ≠ Mastery; Recommendation ≠ Missions; Activity ≠ learning value.  
13. **Legacy coexistence** — `RecommendationService` not deleted; no hybrid averaging adapter shipped as “temporary truth.”

---

# 15. Definition of Done

A Capability 2.9 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; deferred items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] `Recommendation` model matches §4 (read-side, Decision-bound, immutable, explainable, no required Twin field)  
- [ ] Projection pipeline matches §5 (pure package; no re-selection; no ranking; no Twin writes)  
- [ ] Warrant propagation matches §6 (cold-start / low-warrant honesty; no Mid/High coercion)  
- [ ] Explanation contract matches §7 (reason-code narration; chain supportable; forbidden patterns rejected)  
- [ ] Student context adaptation matches §8 (communication only; deterministic attribution)  
- [ ] Public API impact is additive only (§9)  
- [ ] Testing strategy §10 executed and green  
- [ ] Migration impact is None (§11) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §12 hold (Twin write path, Decision, readiness, V1/V2, legacy coexistence, Mission boundary)  
- [ ] Educational fidelity review §13 verified by tests and review  
- [ ] Acceptance criteria §14 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No Mission Generation, Decision Journal ORM, numeric packaging ranking, or `RecommendationService` deletion shipped under this capability label  

**Stop after Capability 2.9 structural ship + review.** Do not start Capability 2.10 in the same change set unless separately requested.

---

# 16. Recommended Implementation Sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read 2.9.1 analysis + 2.9.2 architecture + this plan; confirm Decision types to consume | Shared understanding; projection-only firewall confirmed |
| **1** | Lock Recommendation Confidence / affordance / chain-layer vocabulary in PR description | Catalogues listed; Mid coercion forbidden; accept ≠ mastery |
| **2** | Implement `suggestion.py` + `reasons.py` + `explanation.py` + `warrant.py` + `affordances.py` + `context.py` + `recommendation.py` | Types import cleanly; frozen |
| **3** | Implement `engine.py` cold-start + low-warrant packaging paths first | not-yet-knowable / cold_start → honest confidence + diagnostic framing when Decision selected it |
| **4** | Implement explanation packaging + reason-code mapping | Every reason maps to Decision codes; tensions preserved |
| **5** | Implement candidate contrast + constraint honesty + urgency/duration presentation | Contrast ⊆ candidates; demotions visible; no priority score |
| **6** | Implement response affordances + optional communication-context adaptation | Accept/dismiss/defer hooks; selection unchanged by context |
| **7** | Export package + update Twin README (+ decision docstring if needed) | Read-side packaging ownership clear |
| **8** | Write `tests/test_recommendation_engine.py` | Suite green |
| **9** | Run decision + readiness + Twin strategy regressions + ruff | No regressions |
| **10** | Capability review against §14 + fidelity §13 | Checklist complete |
| **11** | Completion report + stop | Do not start 2.10 |

### Suggested PR shape

- **Title:** `feat: structural Recommendation Engine (Decision packaging, explainable)`  
- **Body:** link this plan + 2.9.1/2.9.2; state projection-only firewall; migration None; V1/V2 via Decision lineage; note deferred Mission generation, Decision Journal persistence, coach phrasing, numeric packaging scores, and legacy cutover  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, ranking/scoring formulas, Mission Generation, Decision Journal ORM, or UI.

Next engineering step (separate milestone): execute §16 steps 1–11 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited via Decision; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Recommendation narrates without modification |
| 2.7 | Readiness Aggregation | May appear in explanation when Decision cites readiness; firewall preserved |
| 2.8 | Decision Engine | Supplies Decision authority that Recommendation projects |
| **2.9.1** | Recommendation Engine Educational Analysis | Approved educational charter |
| **2.9.2** | Recommendation Engine Architecture | Approved structural contracts |
| **2.9.3** | **Recommendation Engine Implementation Plan** | **This document** |
| 2.9 impl | Structural packaging | Separate milestone after this plan |
| 2.10 | Mission Generation Intelligence | Project Decision into daily structure later; not in this ship |

---

# Appendix B — Risks carried into implementation

| Risk | Mitigation in implementation |
|---|---|
| Treating Recommendation as write domain | Separate package; no Twin field; no Update Strategy |
| Recommendation invents ranking | Package Decision only; no match % / priority authority; firewall tests |
| Opaque packaging | Mandatory reason-code mapping + chain presentation from first ship |
| Warrant stripped at presentation | Explicit cold-start / low-warrant tests; forbidden Mid coercion |
| Post-hoc stories disagree with codes | Reasons must map to Decision codes; fidelity tests |
| Accept treated as mastery | Affordance hooks preference-only; no Twin writes |
| Confidence collapse | Vocabulary separation; risk-framing only when Decision cited |
| Domain / action-family collapse in copy | Preserve revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect |
| Mission conflation | No Mission types in package; boundary docs |
| Legacy dual truth deepening | Stage A only; no hybrid adapters |
| Premature scoring | Structural postures only |
| LLM ownership creep | Framework purity + no network packaging authority |
| V1 Section hard-requirement | Package Decision identities as-is; V1 fixture tests |
| Curriculum invention | Cite Decision lineage only |
| Thrashing / preference blindness | Optional journal context; dismiss ≠ mastery |

---

# Appendix C — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.9.3 — Recommendation Engine Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; Decision lineage reuse planned; no traversal redesign |
| Application code intentionally untouched | Yes (this milestone) |
| Upstream gate | Educational Reasoning Review — APPROVED WITH CONDITIONS — encoded in prior 2.9 docs and herein |
| Preceded by | 2.9.1 Educational Analysis + 2.9.2 Architecture (approved) |
| Next | Structural Recommendation Engine implementation → tests → capability review |

---

*End of Capability 2.9.3 Recommendation Engine Implementation Plan. STOP.*
