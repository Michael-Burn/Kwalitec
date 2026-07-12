# Recommendation Integrity Review

**Final decision:** APPROVED WITH CONDITIONS  
**Date:** 12 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Capability:** 2.9 Explainable Recommendation Engine  
**Review type:** Independent release-quality integrity review — documentation only  
**Governing architecture:** [`docs/architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](../architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md)  
**Educational charter:** [`docs/architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](../architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
**Implementation plan:** [`docs/architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_IMPLEMENTATION_PLAN.md`](../architecture/CAPABILITY_2_9_RECOMMENDATION_ENGINE_IMPLEMENTATION_PLAN.md)  
**Upstream gates:**

- Educational Reasoning Review — APPROVED WITH CONDITIONS ([`EDUCATIONAL_REASONING_REVIEW.md`](EDUCATIONAL_REASONING_REVIEW.md))
- Readiness Architecture Review — APPROVED WITH CONDITIONS ([`READINESS_ARCHITECTURE_REVIEW.md`](READINESS_ARCHITECTURE_REVIEW.md))

**Artefacts under review:** `app/domain/recommendation/` · `tests/test_recommendation_engine.py`  
**Companions:** Twin README (`app/domain/twin/README.md`), Decision package (`app/domain/decision/`), Mission language hook (`app/domain/mission/`), legacy `app/services/recommendation_service.py`

**Application / production code was not modified by this review.**

---

## Summary

Capability 2.9 ships a coherent **read-side packaging layer**: `RecommendationEngine.package(decision, …)` projects an immutable, Decision-bound `Recommendation` without selecting actions, inventing ranking, mutating Twin, recomputing readiness, or composing missions.

Against every Epic 2 invariant checked below, **domain Recommendation remains a faithful projection of Decision**. Educational reasoning stays upstream; warrant and cold-start honesty inherit 1:1; accept/dismiss are preference-only; layering is framework-free.

The residual risk is **program dual truth**, not packaging math: product surfaces still call legacy `RecommendationService` while Twin-first Decision → Recommendation packaging exists only in domain. Orchestration (`CurriculumContext` builder, service path, Decision Journal recording) and student-facing copy binding remain unmet. That withholds unconditional release approval — not a rejection of the domain engine.

---

## 1. Educational Responsibility

| Expectation | Verdict | Evidence |
|---|---|---|
| Recommendation owns packaging only | **PASS** | `RecommendationEngine.package` maps Decision → suggestion, reasons, explanation chain, warrant posture, urgency tags, contrast, affordances (`engine.py`) |
| Never owns educational reasoning | **PASS** | Reason codes authored only upstream; packaging narrates via `RecommendationReason.from_decision_ref` — no new selection factors |
| Never becomes a second Decision Engine | **PASS** | Engine imports `Decision` type only; tests assert no `DecisionEngine.evaluate` / no `from app.domain.decision.engine`; Twin README states Recommendation is not a second Decision Engine |

**Verdict:** Recommendation’s educational responsibility is packaging. Decision remains the reasoner and selector.

---

## 2. Decision Authority

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Recommendation never selects actions | **PASS** | `ActionableSuggestion.from_selected(decision.selected)` only; no candidate re-ranking API |
| Recommendation never changes priorities | **PASS** | No `score` / `ranking_score` / `match_percent` / `priority_score` fields; urgency tags present feasibility only (`urgency_duration_tags`) |
| Recommendation never promotes rejected candidates | **PASS** | `project_candidate_contrast` skips `CandidateStatus.SELECTED`; contrast drawn only from Decision candidates; no invented alternatives |
| Recommendation preserves selected Decision | **PASS** | `Recommendation.create` requires `suggestion.family` and `curriculum_entity_id` match `decision_ref`; tests assert family/entity identity across postures; Decision snapshot unchanged after `package` |

Communication context adds phrasing tags (`selection_authority_unchanged`, `context_adapts_phrasing_only`) and does not alter selected family or curriculum entity.

**Verdict:** Decision authority is preserved end-to-end in the domain package.

---

## 3. Projection Integrity

```
Decision
   ↓
RecommendationEngine.package(...)
   ↓
Recommendation
```

| Property | Verdict | Evidence |
|---|---|---|
| Deterministic projection | **PASS** | Same Decision → equal suggestion, reasons, lineage, confidence, contrast, urgency, communication tags (`TestDeterminism`) |
| No additional educational judgement | **PASS** | Pipeline: validate → suggest from selected → narrate Decision codes → explain from lineage → inherit warrant → urgency from acknowledgements → contrast from candidates → affordances; no ReadinessAggregation recompute; no Twin belief synthesis |
| Immutable output | **PASS** | Frozen dataclasses; packaging version `recommendation-engine/2.9.4-structural` |

**Verdict:** Decision → Recommendation is a deterministic structural projection with no second educational judgement layer.

---

## 4. Explainability

Mandatory chain:

```
Curriculum → Learning Evidence → Digital Twin → Readiness → Decision → Recommendation
```

| Layer | How Recommendation presents it | Verdict |
|---|---|---|
| Curriculum | `ExplanationChainPresentation.curriculum` from Decision lineage / scope / format | **PASS** |
| Evidence | Evidence ids or `honest_absence` when lineage empty | **PASS** |
| Twin | Cited twin domains + value-rationale tags from Decision lineage | **PASS** |
| Readiness | Present only when Decision cites readiness factors / warrant inheritance | **PASS** |
| Decision | Selected family, reason codes, candidate statuses, constraint acks | **PASS** |
| Recommendation | Always appended in `layers_present` | **PASS** |

Every Recommendation Reason maps ≥1 Decision reason code; all Decision codes are narrated (`TestExplainability`). Lineage is copied (`decision.lineage`), never fabricated.

**Caveat (non-blocking for structural integrity):** Per-reason `chain_layers` may omit Evidence even when the overall chain presentation always includes an Evidence slot (honest absence or ids). Attribution remains Decision-bound.

**Verdict:** Every Recommendation remains attributable through the mandatory chain.

---

## 5. Warrant Integrity

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Warrant propagates unchanged | **PASS** | `inherit_confidence_posture` maps `DecisionWarrantPosture` → `RecommendationConfidencePosture` 1:1 (`warrant.py`) |
| Cold-start honesty preserved | **PASS** | Cold-start → `COLD_START` confidence; presentation tags `cold_start_communication`, `thin_warrant_honesty`, `no_mid_high_preparedness_claim` |
| Unknown remains unknown | **PASS** | `NOT_YET_KNOWABLE` first-class; tags `not_yet_knowable_first_class`; no Mid coercion path |
| No strengthening of certainty | **PASS** | `THIN_WARRANT_CONFIDENCE_POSTURES` (`honest_low` / `cold_start` / `not_yet_knowable`) never upgraded in packaging; tests assert thin postures stay thin |

**Verdict:** Warrant and cold-start honesty survive packaging without certainty theatre.

---

## 6. Educational Fidelity

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Accept ≠ mastery | **PASS** | `ResponseAffordances.mastery_implied` forced `False`; hooks `preference_intent_only` / `not_mastery`; emphasis `accept_is_commitment_not_competence` |
| Dismiss ≠ failure | **PASS** | History narration preserves `dismiss_not_mastery` / `PRIOR_DISMISS_RESPECTED`; journal tags `dismiss_not_mastery` |
| Recommendation never updates Twin | **PASS** | No Twin write imports; domain snapshot unchanged after `package`; Update Strategies / pipeline banned by AST firewall |
| Recommendation never updates Knowledge | **PASS** | No Knowledge strategy / model imports in package |
| Recommendation never updates Memory | **PASS** | Same firewall |
| Recommendation never updates Behaviour | **PASS** | Same firewall |
| Recommendation never updates Performance | **PASS** | Same firewall |

Recommendation also never recomputes readiness and never generates missions (no mission fields; no `MissionTask` / `app.mission` imports). Mission Intelligence may optionally consume an already-packaged Recommendation as a language hook — sibling projection, not ownership here.

**Verdict:** Educational fidelity holds; packaging is read-only with respect to Twin belief domains.

---

## 7. Layering

| Constraint | Verdict | Evidence |
|---|---|---|
| Framework free | **PASS** | AST firewall bans `flask`, `sqlalchemy`, `wtforms`, and related roots |
| Domain only | **PASS** | Package lives under `app/domain/recommendation/` |
| No Flask | **PASS** | No Flask imports |
| No ORM | **PASS** | No SQLAlchemy / models imports; Decision Journal ORM explicitly deferred in affordances comments |
| No Routes | **PASS** | No blueprint / route modules |
| No Services | **PASS** | Ban on `app.services.*`; no `RecommendationService` import |
| No Database | **PASS** | No `db` / persistence coupling |

Imports are Decision domain types + recommendation-internal modules only.

**Verdict:** Layering matches Epic 2 domain contracts.

---

## 8. Legacy Coexistence

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Stage A coexistence remains clean | **PASS (Stage A)** | Legacy `RecommendationService` untouched; domain does not import it; tests forbid `RecommendationService` / `recommendation_service` strings in domain package |
| No hybrid truth | **PASS** | No adapter averaging legacy readiness % with Twin/Decision packaging; legacy service still uses AdaptiveLearning + `ReadinessService` heuristics independently |
| No RecommendationService ownership drift | **PASS** | Twin-first packaging ownership stays in `app/domain/recommendation/`; legacy service remains the Stage A product peer, not renamed as Twin-first authority |

**Named residual:** Product surfaces (dashboard / planning consumers) still call `RecommendationService.generate_recommendations` while Twin-first packaging is domain-only. That is Stage A dual next-action authority — documented, not a hybrid merge inside Recommendation Engine.

**Verdict:** Stage A coexistence is clean. Dual authority remains a program risk, not an integrity breach inside packaging.

---

## 9. Risks

Evidence-based only — no hypothetical invention.

| ID | Risk | Severity | Basis |
|---|---|---|---|
| **R-01** | Dual next-action authority still live in product | **High (program)** | Live consumers still use `RecommendationService`; Twin-first path is domain-only |
| **R-02** | No production orchestration for live consumers | **High before product wiring** | No `CurriculumContext` builder from `CurriculumService`; no service path calling `DecisionEngine` → `RecommendationEngine` |
| **R-03** | Structural tags ≠ student-facing copy | **Medium (cutover)** | Narration is tag catalogues; product UI/coach can strip warrant or collapse tensions unless Stage C binds copy to chain |
| **R-04** | `confidence_framing` caller-supplied, not Decision-validated | **Low–Medium** | Architecture allows Confidence framing only when Decision cited it; engine accepts tags without checking Decision Confidence-risk codes |
| **R-05** | Decision Journal product loop not shipped | **Medium** | Affordances are structural hooks; accept/dismiss not yet Learning Evidence in production |
| **R-06** | Canonical docs drift | **Medium (hygiene)** | Epic 2 kickoff / EI status tables can still lag shipped 2.9 reality |

Controlled in domain (not active defects): ranking invention, secret re-selection, Twin write paths, Mid/High coercion under thin warrant, Mission conflation.

---

## 10. Technical Debt

Recommendation-specific remaining debt:

| Item | Classification | Next step |
|---|---|---|
| Legacy `RecommendationService` heuristics vs Decision-first packaging | **Critical–High** | Stage B named dual-truth adapters → Stage C Twin-first product authority → Stage D retire divergent math |
| Legacy `ReadinessService` % still product-facing | **High** | Same Stage B/C path; never hybrid-average with Twin packaging |
| No `CurriculumContext` builder | **Medium–High** | Thin orchestration helper outside domain before any live consumer |
| Decision Journal / `recommendation_decision` evidence path | **Medium** | Recording milestone via Evidence → Strategies — never silent Recommendation Twin writes |
| Confidence ownership incomplete | **Medium** | Keep risk-framing only until Confidence domain exists |
| Product copy / coach templates | **Medium** | Must restate chain-supported attributions; forbid post-hoc stories |
| Enforce `confidence_framing` precondition | **Low** | Reject or ignore framing unless Decision cites Confidence-risk codes |
| Subsystem / kickoff / EI Architecture status drift | **Medium** | Documentation hygiene before Epic 2 close communications |

No new High debt was introduced *inside* `app/domain/recommendation/` relative to the approved implementation plan. High items are Stage A coexistence and cutover costs.

---

## 11. Recommendations

**Is Recommendation ready for Epic 2 release?**

**Yes — as a domain capability ship**, under conditions. Structural Recommendation integrity holds. Epic 2 may treat Capability 2.9 as architecturally closed for the domain package.

**Not yet ready as unconditional product Recommendation integrity.** Stage A dual authority, missing orchestration, and unbound student-facing copy keep product Twin-first Recommendation incomplete.

Binding follow-ups before claiming product integrity:

1. Keep Decision Engine sole selection authority; do not reopen ranking inside Recommendation.
2. Name Stage A honestly — surfaces on `RecommendationService` are not Twin-first Educational Intelligence.
3. Ship thin `CurriculumContext` builder + Decision → Recommendation orchestration before live consumers.
4. Plan Stage B cutover; freeze legacy heuristic deepening; no hybrid averages.
5. Wire Decision Journal so accept/dismiss/defer become preference evidence — never mastery.
6. Harden `confidence_framing` validation before production wiring.
7. Bind student-facing copy to chain-supported tags (warrant, action-family separations).
8. Sync Epic 2 / EI Architecture status docs with shipped 2.9.

---

## 12. Final Decision

### APPROVED WITH CONDITIONS

**Justification:** Domain Recommendation Engine is a faithful, deterministic projection of Decision. It does not select actions, change priorities, promote rejected candidates, invent educational judgement, strengthen warrant, mutate Twin belief domains, or breach framework-free layering. Stage A legacy coexistence is clean (no hybrid truth, no ownership drift into `RecommendationService`).

Unconditional **APPROVED** is withheld while dual next-action authority remains product-live, production orchestration and Decision Journal recording are absent, and student-facing copy is not yet bound to chain-supported warrant honesty.

**REJECTED** is not warranted: packaging does not violate Epic 2 projection rules and does not invent a second educational reasoner.

### Binding conditions

1. Decision Engine remains sole selection authority.  
2. Explainability chain preserved end-to-end; no opaque “recommended for you.”  
3. No legacy hybrid truth; do not deepen `RecommendationService` as Twin-first truth.  
4. Write/read firewall — no Twin / Knowledge / Memory / Behaviour / Performance updates from Recommendation.  
5. Warrant and cold-start honesty inherited; never Mid/High theatre under thin warrant.  
6. Communication is phrasing only; Confidence framing remains Decision-cited risk language.  
7. Curriculum V1/V2 via Decision / Curriculum lineage only.  
8. Accept/dismiss is preference, not mastery.  
9. Stage B cutover planned before claiming product Recommendation integrity.  
10. Documentation hygiene before Epic close communications.

### Not in scope of this review

- Implementing Stage B adapters or UI cutover  
- Decision Journal ORM / migrations  
- Product copy templates or coach models  
- Changing Mission Intelligence or Decision Engine selection math  
- Deleting `RecommendationService`  
- Application code, tests, or migrations (none performed)

---

## Architecture Compliance Summary

| Invariant | Status |
|---|---|
| Recommendation is a projection of Decision | Preserved |
| Decision sole next-action selector | Preserved in domain |
| No hidden packaging ranking | Preserved |
| Twin sole educational-state authority | Preserved (read-only lineage citation) |
| Readiness not recomputed by packaging | Preserved |
| Missions not generated by packaging | Preserved |
| Warrant / cold-start honesty | Preserved structurally |
| Accept ≠ mastery | Preserved |
| Curriculum V1/V2 via Decision lineage | Preserved |
| Framework-free domain layering | Preserved |
| Legacy Stage A coexistence (no hybrid) | Preserved / named |
| Product Twin-first Recommendation cutover | **Not done** — condition |

---

## Review artefacts

| Artefact | Path |
|---|---|
| Domain package | `app/domain/recommendation/` |
| Engine | `app/domain/recommendation/engine.py` |
| Model | `app/domain/recommendation/recommendation.py` |
| Tests | `tests/test_recommendation_engine.py` |
| Twin README call order | `app/domain/twin/README.md` |
| Legacy peer (untouched) | `app/services/recommendation_service.py` |

**Migration impact:** None (review-only).  
**Curriculum V1/V2:** Compatibility preserved; packaging does not require Sections globally.  
**Tests:** Integrity contracts encoded in `tests/test_recommendation_engine.py` (projection, reason fidelity, warrant/cold-start, no Twin mutation, no DecisionEngine call, AST firewall, V1/V2). This review did not modify application code.

---

*End of Recommendation Integrity Review. STOP.*
