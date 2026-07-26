# EP-001.3 — Gap Analysis

**Milestone:** EP-001.3 — Readiness Intelligence  
**Phase:** 3 — Gap Analysis  
**Date:** 2026-07-26

Compare current Runtime A readiness vs Canonical Learner State / Planner consumption success criteria.

---

## 1. Capability matrix

| Capability | Status | Evidence | Gap |
|---|---|---|---|
| Overall readiness score | **Implemented** | `get_overall_readiness` | Score not packaged with CLS-enriched intelligence object |
| Confidence level | **Missing** | No Runtime A confidence band | Primary gap |
| Strongest / weakest areas | **Implemented** | ORM topic lists | Duplicate Twin mastery when Twin ON |
| Readiness drivers | **Partially implemented** | Coverage/mastery/review weights implicit | Not named/provenance-linked to CLS |
| Recommended next actions | **Missing** on readiness | Planner has missions/revisions | Primary gap |
| Mission influence | **Implemented** | Review discipline | Not composed with CLS mission_completion when Twin ON |
| Mastery influence | **Implemented** | Composite + topic lists | Should prefer CLS `topic_mastery` for areas |
| Study behaviour influence | **Missing** | Foundation facets unused by readiness | Primary gap |
| Consume `CanonicalLearnerState` | **Missing** | Foundation exists; readiness does not consume | Primary gap |
| Consume Planner outputs | **Missing** | EP-001.2 daily plan unused | Primary gap |
| Avoid collector recursion | **Constraint** | Collector → `get_overall_readiness` | Must add additive API, not mutate getter |
| Parallel stack consolidation | **N/A this milestone** | Epic / V2 / OS remain | Explicitly do **not** delete |

---

## 2. Duplicated calculations

| Calculation | Locations | Risk |
|---|---|---|
| Overall readiness % | `ReadinessService` → collector → Foundation `readiness_overall`; consumers also call service directly | Acceptable pass-through today; intelligence should **reuse** CLS `readiness_overall` rather than invent a second formula |
| Weak / strong topics | `ReadinessService` ORM vs Foundation `topic_mastery` | Duplicate when Twin ON — prefer CLS for intelligence areas |
| Streaks | `ReadinessService` + Foundation `streaks` (from collector) | Prefer CLS streaks for drivers |
| Mission completion | Review discipline query vs Foundation `mission_completion` | Prefer CLS for drivers when Twin ON |

---

## 3. Duplicated state

| State | Owners today | Rule |
|---|---|---|
| Mastery / progress | ORM write SoT; Twin CLS consumer SoT | Readiness must not invent mastery maps |
| Planning slots | Planner | Readiness must not re-plan; only cite actions |
| Structural posture/warrant | Epic `ReadinessAggregation` | Leave parallel; do not merge formulas |

---

## 4. Missing readiness inputs (relative to CLS)

1. Behaviour reliability labels (`study_behaviour`)
2. Consistency label (`study_consistency`)
3. Evidence density (`learning_evidence.attempt_count`)
4. Practice mean accuracy (`practice_performance`)
5. Exam countdown / lifecycle (`study_state`) as pressure drivers
6. Planner today missions / revision priorities as next actions

---

## 5. Consolidation opportunities

1. **Extend** `ReadinessService` with `build_readiness_intelligence` — Twin-gated, fail-open.
2. **Add** thin infrastructure consumer (`readiness_intelligence`) projecting CLS + optional planner dict → assessment DTOs (mirror EP-001.2).
3. **Reuse** CLS `study_state.readiness_overall.score` as the readiness score when available (Runtime A formula remains authoritative; Twin pass-through).
4. **Derive** confidence from evidence density + coverage completeness + mission adherence (deterministic bands).
5. **Derive** strongest/weakest from CLS `topic_mastery` (fallback empty when unavailable).
6. **Derive** drivers from CLS dimensions with explicit source tags.
7. **Cite** planner daily plan slots / revisions as recommended next actions when present.
8. **Leave** `get_overall_readiness` and collector unchanged (no recursion).
9. **Leave** Epic / V2 / OS readiness stacks untouched.

---

## 6. What must not be done

| Anti-goal | Why |
|---|---|
| New parallel `ReadinessIntelligenceService` replacing `ReadinessService` | Violates “extend existing readiness” |
| New learner-state store inside readiness | Twin owns learner state |
| New planner inside readiness | Planner owns planning |
| Change `get_overall_readiness` to call Foundation | Collector recursion |
| Fabricate mock performance | Foundation marks unavailable |
| Average Epic posture with Runtime A % | Forbidden hybrid third formula |
| Rewrite RecommendationService / dashboard cutover | Out of scope |

---

## 7. Recommendation

Implement EP-001.3 by extending Runtime A `ReadinessService` to **consume** EP-001.1 `CanonicalLearnerState` and EP-001.2 planner outputs, packaging a richer readiness assessment without introducing a duplicate readiness architecture or learner-state / planning ownership.
