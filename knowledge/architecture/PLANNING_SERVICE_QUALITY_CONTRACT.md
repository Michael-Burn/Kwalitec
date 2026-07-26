# PlanningService Quality Contract (EP-003.3)

**Status:** Active  
**Authority:** Runtime A planning communication  
**Implements:** P-001.2 Mandatory Explanation Schema for daily plans / mission surfaces  
**Owner module:** `app/services/planning_quality.py` (called only from `PlanningService`)

---

## 1. Purpose

Define the serialisable contract every Runtime A student-facing daily plan and dashboard mission surface must satisfy before presentation.

## 2. Mandatory fields (surface / plan)

| Field | Meaning |
|---|---|
| `judgement` | Stated plan judgement (what is planned today) |
| `why_this_plan` | Why these priorities |
| `supporting_evidence` | Supporting evidence list |
| `confidence_level` | Student-safe confidence label |
| `expected_benefit` | Expected educational benefit |
| `suggested_next_action` / `next_action` | One clear next action |
| `review_point` | When to refresh the plan |
| `plan_drivers` | Explicit named drivers (slots, workload, readiness signal, recovery) |
| `change_reasoning` | What changed (e.g. recovery after misses) |
| `readiness_alignment` | Alignment label vs readiness composite |
| `recommendation_alignment` | Alignment label vs tip titles / ladder order |
| `plan_coherence` | Overall coherence (`aligned` / `advisory` / `recovery` / …) |
| `explanation_schema_version` | `p001.2/v1` |
| `explanation_level` | Default `level_2` |
| `explanation_schema_complete` | `True` when schema attached |

Optional / sentinel:

| Field | Meaning |
|---|---|
| `honest_refusal` | Prefer “no plan ready” over fabricated days |
| `explanation_summary` | Concise L2 speech for presentation pass-through |

### Confidence labels (student-safe)

- `High confidence`
- `Moderate confidence`
- `Low confidence / Suggested`
- `Cannot yet be estimated`

## 3. Application points

1. `PlanningService.build_daily_study_plan` — after assembler payload (`apply_planning_quality_to_daily_plan`).
2. `PlanningService.get_dashboard_mission_surface` — after legacy build or cutover return (`apply_planning_quality_contract`).

## 4. Ownership rules

- **May:** attach schema; balance/recover within planner assembler; label readiness/recommendation alignment; refuse honestly; annotate workload when readiness is low.
- **Must not:** recalculate readiness scores; rank recommendations; invent mastery; generate missions from the quality module.
- **Presentation:** `RuntimeAPresentationAdapter` pass-throughs schema-complete surfaces; must not re-plan.

## 5. Fail-open

Readiness and recommendation lookups catch exceptions and continue with degraded alignment defaults. Cutover / dual-run flags remain governed by EP-002.7. Nested quality depth skips sibling lookups to prevent recursion.

## 6. Personalisation (EP-004.3)

Optional Personal Learning Profile evidence may adjust session duration, workload pacing, recovery/revision minute emphasis, and equivalent repair-topic selection **after** the quality schema is attached.

| Field | Meaning |
|---|---|
| `personalisation_applied` | Whether any profile factor influenced the plan |
| `personalisation_factors` | Traceable attribute / effect / confidence list |
| `personalisation_schema_version` | `ep004.3/v1` |
| `personalisation_profile_id` | Provenance when applied |
| `session_sizing_guidance` | Declared session-length note when available |

**Hard rules:** educational slot order `review → recovery/weak → progression` must not change; unsupported / low-confidence attributes ignored; accept/dismiss never drives planning; fail-open to EP-003.3 baseline. Rules: `../product/ep004_3_adaptive_planning_personalisation/PERSONALISATION_RULES.md`.

**Presentation:** `RuntimeAPresentationAdapter` pass-throughs personalisation fields with the schema-complete surface; must not inspect the profile or invent adaptations.
