# Mission Integrity Review

**Final decision:** APPROVED WITH CONDITIONS  
**Date:** 12 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Capability:** 2.10 Mission Generation Intelligence  
**Review type:** Independent release-quality integrity review — documentation only  
**Governing architecture:** [`docs/architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](../architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`docs/architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](../architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md)  
**Implementation plan:** [`docs/architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_IMPLEMENTATION_PLAN.md`](../architecture/CAPABILITY_2_10_MISSION_INTELLIGENCE_IMPLEMENTATION_PLAN.md)  
**Upstream gates:**

- Educational Reasoning Review — APPROVED WITH CONDITIONS ([`EDUCATIONAL_REASONING_REVIEW.md`](EDUCATIONAL_REASONING_REVIEW.md))
- Recommendation Integrity Review — APPROVED WITH CONDITIONS ([`RECOMMENDATION_INTEGRITY_REVIEW.md`](RECOMMENDATION_INTEGRITY_REVIEW.md))

**Artefacts under review:** `app/domain/mission/` · `tests/test_mission_intelligence.py`  
**Companions:** Twin README (`app/domain/twin/README.md`), Decision package (`app/domain/decision/`), Recommendation package (`app/domain/recommendation/`), legacy `app/services/planning_service.py` + `app/services/mission_service.py` + ORM `app/models/mission.py`

**Application / production code was not modified by this review.**

---

## Summary

Capability 2.10 ships a coherent **execution / projection layer**: `MissionIntelligence.compose(decision_or_batch, execution_context, recommendation_language=…)` operationalises immutable, Decision-bound `Mission` / `MissionTask` structure without selecting actions, inventing ranking or filler, mutating Twin beliefs, recomputing readiness, calling `DecisionEngine`, or owning Recommendation packaging / WeekPlan policy.

Against every Epic 2 invariant checked below, **domain Mission remains a faithful operationalisation of Decision**. Educational reasoning stays upstream; warrant and cold-start honesty inherit with thin-warrant precedence; load shaping demotes volume/intensity or omits trailing authorised work with acknowledgement; every MissionTask remains attributable through the explainability chain.

The residual risk is **program dual truth**, not execution math: product surfaces still generate day’s work via `PlanningService` → `MissionService` (ORM rows) while Twin-first Decision → Mission composition exists only in domain. That withholds unconditional release approval — not a rejection of the domain engine.

---

## 1. Educational Responsibility

| Expectation | Verdict | Evidence |
|---|---|---|
| Mission executes Decisions | **PASS** | `MissionIntelligence.compose` binds Decision(s), preserves batch order, maps selected actions → MissionTasks (`engine.py`) |
| Mission never decides | **PASS** | No `DecisionEngine` import/call; `_validate_preconditions` requires Decision.selected + reason codes; tests ban `DecisionEngine.evaluate` in engine source |
| Mission never ranks | **PASS** | No `score` / `priority_score` / `ranking_score` / `packing_score` / `optimization_objective` fields; sequencing is identity-preserving (`sequencing.preserve_decision_order`) |
| Mission never owns planning | **PASS** | Package docs forbid WeekPlan policy; engine docstring: never owns WeekPlan; no planning-service imports |

**Verdict:** Mission’s educational responsibility is execution. Decision remains the reasoner and selector; Planning retains multi-day / WeekPlan ownership.

---

## 2. Decision Authority

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Mandatory Decision attribution | **PASS** | `Mission.create` requires non-empty `decision_citations`; every MissionTask requires ≥1 Decision reason-code citation; `DecisionAttribution.from_decision` refuses empty codes |
| No re-selection | **PASS** | Tasks copy `decision.selected.family` / `curriculum_entity_id` / `intent`; family/entity/intent must match citation (`task.py`); load shaping uses authorised prefix only |
| No rejected candidate promotion | **PASS** | `CandidateContrastHook` skips `SELECTED`; contrast drawn only from Decision candidates; tight/zero capacity yields empty Mission — never substitutes rejected candidates (`TestNoReselection`) |
| Educational objective unchanged | **PASS** | Action family, curriculum scope, and intent preserved 1:1; intensity demotion sets `intensity_demoted` / feasibility tags without changing family; Decision snapshot unchanged after compose |

Optional Recommendation language is Decision-faithful only (family + curriculum entity must match primary selected); mismatch raises `ValueError`. Language never sequences tasks.

**Verdict:** Decision authority is preserved end-to-end in the domain package.

---

## 3. Execution Fidelity

```
Decision (or ordered Decision batch)
   ↓
MissionIntelligence.compose(...)
   ↓
Mission (MissionTasks + feasibility acknowledgements)
```

| Property | Verdict | Evidence |
|---|---|---|
| Faithful operationalisation | **PASS** | Pipeline: bind → validate → preserve order → resolve include count → authorise prefix → operationalise tasks → aggregate warrant → emit |
| Execution expands work | **PASS** | Selected Decision action(s) become executable MissionTask units with attribution, warrant, feasibility, evidence hooks, regeneration identity |
| Execution never changes educational meaning | **PASS** | Family / entity / intent locked to Decision selected; constraints demote volume/intensity or omit trailing authorised work — they do not swap educational actions |
| Deterministic | **PASS** | Same Decision + context → equal scope, tasks, warrant, feasibility, regeneration (`TestDeterminism`) |
| Immutable output | **PASS** | Frozen dataclasses; version `mission-intelligence/2.10.4-structural` |

**Verdict:** Decision → Mission is a deterministic structural operationalisation with no second educational judgement layer.

---

## 4. Explainability

Mandatory chain (Recommendation optional):

```
Curriculum
   ↓
Evidence
   ↓
Twin
   ↓
Readiness (when Decision cites it)
   ↓
Decision
   ↓
Recommendation (optional packaging language)
   ↓
Mission / MissionTask
```

| Layer | How Mission presents it | Verdict |
|---|---|---|
| Curriculum | Lineage `curriculum_entity_ids` + task `curriculum_entity_id` from Decision selected | **PASS** |
| Evidence | Evidence ids or `evidence_honest_absence` when lineage empty | **PASS** |
| Twin | Cited twin domains + value-rationale tags from Decision lineage | **PASS** |
| Readiness | Present in `layers_present` only when Decision cites readiness factors / warrant inheritance | **PASS** |
| Decision | Selected family/intent, reason codes, candidate contrast, constraint acknowledgement tags | **PASS** |
| Recommendation | Optional `RecommendationLanguageHook` on primary task — never required; never selection authority | **PASS** |
| Mission | `MISSION_TASK` always appended in `layers_present` | **PASS** |

Every MissionTask maps reason codes ⊆ Decision codes; lineage is copied (`decision.lineage`), never fabricated (`TestDecisionAttribution`). Mission-level `decision_citations` retain full batch lineage even when trailing Decisions are omitted under capacity.

**Verdict:** Every MissionTask remains attributable through the mandatory chain.

---

## 5. Educational Fidelity

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Completion ≠ mastery | **PASS** | `MissionEvidenceHooks.mastery_implied` forced `False`; notes include `completion_not_mastery` / `completion_not_exam_readiness` |
| Completion ≠ readiness | **PASS** | Same hooks; category hint restricted to Behaviour / Planning only |
| Behaviour hooks only | **PASS** | `BehaviourEvidenceCategoryHint` ∈ {behaviour, planning}; recording deferred to product → Learning Evidence → Behaviour Strategy |
| No Twin mutation | **PASS** | No Twin write imports; Twin domain snapshot unchanged after compose; Update Strategies / pipeline banned by AST firewall |
| No Knowledge update | **PASS** | No Knowledge strategy / model imports |
| No Memory update | **PASS** | Same firewall |
| No Behaviour update directly | **PASS** | Hooks are structural linkage slots only — no Behaviour strategy calls |
| No Performance update | **PASS** | Same firewall |

**Verdict:** Educational fidelity holds; Mission is read-only with respect to Twin belief domains. Completion/failure recording is out-of-band by design.

---

## 6. Constraint Handling

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Constraints shape feasibility | **PASS** | `resolve_include_count` applies remaining minutes, `max_tasks`, already-committed capacity, sustainability protect; effects recorded as `FeasibilityAcknowledgement` |
| Constraints never erase educational need | **PASS** | Omitted authorised Decisions appear in `omitted_task_refs` + mission-level `decision_citations`; omission tagged `omission_not_reselection` — need remains visible |
| Unused capacity never invents work | **PASS** | Ample leftover minutes still yield only Decision-authored tasks (`test_leftover_capacity_does_not_invent_tasks`); zero capacity → empty Mission with `EMPTY_CAPACITY_REMAINDER` / `no_filler_invented` |
| Intensity demotion ≠ family swap | **PASS** | `protect_intensity` sets `intensity_demoted` and `INTENSITY_DEMOTED` / `SUSTAINABILITY_PROTECT`; action family unchanged (`rest_protect_not_failure`) |

Structural slot size (`_STRUCTURAL_SLOT_MINUTES = 25`) bounds how many authorised Decisions fit — capacity honesty, not educational ranking.

**Verdict:** Feasibility shapes load without inventing educational need or silently erasing Decision authority.

---

## 7. Layering

| Constraint | Verdict | Evidence |
|---|---|---|
| Framework free | **PASS** | AST firewall bans `flask`, `sqlalchemy`, `wtforms`, and related roots (`TestFrameworkPurity`) |
| Domain only | **PASS** | Package lives under `app/domain/mission/` |
| No ORM | **PASS** | No SQLAlchemy / `app.models` imports; domain `Mission` / `MissionTask` explicitly distinct from ORM peers |
| No Flask | **PASS** | No Flask / blueprint imports; ban on `app.mission` (HTTP blueprint) inside domain |
| No Services | **PASS** | Ban on `app.services.*`; no `PlanningService` / `MissionService` import |
| No Database | **PASS** | No `db` / persistence coupling |

Imports are Decision (+ optional Recommendation type for language hook) + mission-internal modules + `CurriculumFormat` from readiness curriculum context only.

**Verdict:** Layering matches Epic 2 domain contracts.

---

## 8. Legacy Coexistence

| Checkpoint | Verdict | Evidence |
|---|---|---|
| Stage A coexistence with PlanningService | **PASS (Stage A)** | Legacy `PlanningService.generate_today_mission` / `_generate_mission_for_date` still builds ORM missions via topic selection + day-type task packs; domain does not import PlanningService |
| No hybrid planning authority | **PASS** | No adapter averaging legacy plan heuristics with Twin/Decision Mission composition; named dual truth in package docs (`mission.py`, `__init__.py`) |
| Product surfaces remain legacy | **Named residual** | `app/mission/routes.py` and `app/dashboard/routes.py` call `MissionService` / `PlanningService` only — zero `MissionIntelligence` / `domain.mission` references in product HTTP |

**Named residual:** Product “today’s mission” is still PlanningService selection + MissionService persistence, while Twin-first Mission Intelligence is domain-only. That is Stage A dual execution authority — documented, not a hybrid merge inside Mission Intelligence.

**Verdict:** Stage A coexistence is clean. Dual authority remains a program risk, not an integrity breach inside the domain execution layer.

---

## 9. Risks

Evidence-based only — no hypothetical invention.

| ID | Risk | Severity | Basis |
|---|---|---|---|
| **R-01** | Dual mission-generation authority still live in product | **High (program)** | Dashboard / mission routes use `PlanningService` + `MissionService`; Twin-first path is domain-only |
| **R-02** | No production orchestration for live consumers | **High before product wiring** | No service path calling `DecisionEngine` → (optional `RecommendationEngine`) → `MissionIntelligence.compose` → persistence |
| **R-03** | Legacy PlanningService still selects topics / invents task packs | **High (cutover)** | `_select_topic_for_today` + `_generate_mission_tasks` remain a parallel educational author — Stage A freeze deepening required |
| **R-04** | Structural tags ≠ student-facing copy | **Medium (cutover)** | Attribution / feasibility / warrant are tag catalogues; UI can strip Decision lineage unless Stage C binds copy |
| **R-05** | Completion → Behaviour evidence loop not shipped | **Medium** | Evidence hooks are structural; product completion still marks ORM `completed` without Twin/Evidence pipeline |
| **R-06** | Named dual type identity (`domain.Mission` vs `models.Mission`) | **Medium (hygiene)** | Coexistence requires careful naming at any future adapter boundary to avoid silent conflation |
| **R-07** | Canonical docs drift | **Medium (hygiene)** | Epic 2 / EI status tables can still lag shipped 2.10 reality |

Controlled in domain (not active defects): ranking invention, secret re-selection, rejected-candidate promotion, filler under leftover capacity, Twin write paths, Mid/High coercion under thin warrant, WeekPlan absorption.

---

## 10. Technical Debt

Mission-specific remaining debt:

| Item | Classification | Next step |
|---|---|---|
| Legacy `PlanningService` mission generation vs Decision-first composition | **Critical–High** | Stage B named dual-truth adapters → Stage C Twin-first product authority → Stage D retire divergent selection |
| Legacy ORM `Mission` / `MissionTask` without Decision attribution | **High** | Adapter / persistence milestone; never treat ORM rows as Twin truth |
| No Decision → Mission orchestration service path | **Medium–High** | Thin orchestration outside domain before any live consumer |
| Completion / Failure → Learning Evidence → Behaviour Strategy | **Medium** | Recording milestone via Evidence → Strategies — never silent Mission Twin writes |
| Product copy / mission UI templates | **Medium** | Must restate Decision reason codes + warrant; forbid post-hoc “busy day” stories |
| `_STRUCTURAL_SLOT_MINUTES` constant | **Low** | Keep as capacity bound only; never evolve into packing solver / re-ranker |
| Subsystem / kickoff / EI Architecture status drift | **Medium** | Documentation hygiene before Epic 2 close communications |

No new High debt was introduced *inside* `app/domain/mission/` relative to the approved implementation plan. High items are Stage A coexistence and cutover costs.

---

## 11. Recommendations

**Is Mission ready for Epic 2 release?**

**Yes — as a domain capability ship**, under conditions. Structural Mission integrity holds. Epic 2 may treat Capability 2.10 as architecturally closed for the domain package.

**Not yet ready as unconditional product Mission integrity.** Stage A dual authority, missing orchestration, unbound student-facing copy, and unfinished Completion → Behaviour evidence recording keep product Twin-first Mission incomplete.

Binding follow-ups before claiming product integrity:

1. Keep Decision Engine sole selection authority; do not reopen ranking or topic selection inside Mission.
2. Name Stage A honestly — surfaces on `PlanningService` / ORM missions are not Twin-first Educational Intelligence.
3. Ship thin Decision → (optional Recommendation) → Mission orchestration before live consumers.
4. Plan Stage B cutover; freeze deepening of legacy mission ranking / filler generation; no hybrid averages.
5. Wire Completion / Failure so outcomes become Behaviour / planning evidence — never mastery or readiness writes.
6. Bind student-facing mission UI to Decision reason codes, warrant honesty, and feasibility acknowledgements.
7. Keep Planning / WeekPlan ownership distinct — Mission must not absorb multi-week strategy.
8. Sync Epic 2 / EI Architecture status docs with shipped 2.10.

---

## 12. Final Decision

### APPROVED WITH CONDITIONS

**Justification:** Domain Mission Intelligence is a faithful, deterministic operationalisation of Decision. It does not decide, rank, re-select, promote rejected candidates, invent filler, change educational meaning under constraints, mutate Twin belief domains, or breach framework-free layering. Stage A legacy coexistence with PlanningService is clean (no hybrid planning authority, no ownership drift into domain Mission).

Unconditional **APPROVED** is withheld while dual mission-generation authority remains product-live, production orchestration and Completion → Behaviour evidence recording are absent, and student-facing mission copy is not yet bound to Decision attribution.

**REJECTED** is not warranted: execution does not violate Epic 2 operationalisation rules and does not invent a second educational reasoner or planner inside the domain package.

### Binding conditions

1. Decision Engine remains sole selection authority.  
2. Explainability chain preserved end-to-end into every MissionTask; no opaque “today’s tasks.”  
3. No legacy hybrid truth; do not deepen `PlanningService` mission generation as Twin-first truth.  
4. Write/read firewall — no Twin / Knowledge / Memory / Behaviour / Performance updates from Mission composition.  
5. Completion ≠ mastery and ≠ readiness; Behaviour / planning hooks only.  
6. Constraints shape feasibility only; empty / leftover capacity never invents educational work.  
7. Warrant and cold-start honesty inherited; never Mid/High theatre under thin warrant.  
8. Recommendation language optional and Decision-faithful; never sequencing authority.  
9. Curriculum V1/V2 via Decision / Curriculum lineage only.  
10. Planning / WeekPlan ownership remains outside Mission Intelligence.  
11. Stage B cutover planned before claiming product Mission integrity.  
12. Documentation hygiene before Epic close communications.

### Not in scope of this review

- Implementing Stage B adapters or UI cutover  
- Mission persistence schema / Alembic migrations  
- Completion → Evidence recording services  
- Product copy templates or coach models  
- Changing Decision Engine selection math or Recommendation packaging  
- Deleting `PlanningService` / ORM `Mission`  
- Application code, tests, or migrations (none performed)

---

## Architecture Compliance Summary

| Invariant | Status |
|---|---|
| Mission operationalises Decision (does not decide) | Preserved |
| Decision sole next-action selector | Preserved in domain |
| No hidden mission ranking / packing scores | Preserved |
| No rejected-candidate promotion | Preserved |
| Twin sole educational-state authority | Preserved (read-only snapshot ref / lineage citation) |
| Readiness not recomputed by Mission | Preserved |
| Completion ≠ mastery / readiness | Preserved |
| Constraints shape feasibility, not educational need | Preserved |
| No filler under unused capacity | Preserved |
| Warrant / cold-start honesty | Preserved structurally |
| Curriculum V1/V2 via Decision lineage | Preserved |
| Framework-free domain layering | Preserved |
| Legacy Stage A coexistence (no hybrid planning) | Preserved / named |
| Product Twin-first Mission cutover | **Not done** — condition |

---

## Review artefacts

| Artefact | Path |
|---|---|
| Domain package | `app/domain/mission/` |
| Engine | `app/domain/mission/engine.py` |
| Mission / MissionTask | `app/domain/mission/mission.py`, `task.py` |
| Attribution / load shaping | `app/domain/mission/attribution.py`, `load_shaping.py`, `sequencing.py` |
| Evidence hooks | `app/domain/mission/evidence_hooks.py` |
| Tests | `tests/test_mission_intelligence.py` |
| Twin README call order | `app/domain/twin/README.md` |
| Legacy peers (untouched) | `app/services/planning_service.py`, `app/services/mission_service.py`, `app/models/mission.py` |

**Migration impact:** None (review-only).  
**Curriculum V1/V2:** Compatibility preserved; Mission inherits format from Decision lineage and does not require Sections globally.  
**Tests:** Integrity contracts encoded in `tests/test_mission_intelligence.py` (attribution, no re-selection, load shaping / no filler, warrant/cold-start, completion ≠ mastery, no Twin mutation, no DecisionEngine call, AST firewall, V1/V2). This review did not modify application code or re-run the suite.

---

*End of Mission Integrity Review. STOP.*
