# ReadinessService Quality Contract (EP-003.2)

**Status:** Active  
**Authority:** Runtime A readiness communication  
**Implements:** P-001.2 Mandatory Explanation Schema for readiness assessments  
**Owner module:** `app/services/readiness_quality.py` (called only from `ReadinessService`)

---

## 1. Purpose

Define the serialisable contract every Runtime A student-facing readiness surface (and intelligence assessment packaging) must satisfy before presentation.

## 2. Mandatory fields (surface)

| Field | Meaning |
|---|---|
| `judgement` | Stated readiness judgement (Recommendation mapping for non-tip guidance) |
| `why_this_estimate` | Why this estimate |
| `supporting_evidence` | Supporting evidence list |
| `confidence_level` | Student-safe confidence label |
| `expected_benefit` | Expected educational benefit |
| `suggested_next_action` / `next_action` | One clear next action |
| `review_point` | When to reassess |
| `readiness_drivers` | Explicit named drivers with influence / rationale |
| `change_reasoning` | What is supporting / holding back the estimate (+ optional delta) |
| `explanation_schema_version` | `p001.2/v1` |
| `explanation_level` | Default `level_2` |
| `explanation_schema_complete` | `True` when schema attached |

Optional / sentinel:

| Field | Meaning |
|---|---|
| `honest_refusal` | Prefer “cannot yet be estimated” over fabricated scores |
| `explanation_summary` | Concise L2 speech for presentation pass-through |

### Confidence labels (student-safe)

- `High confidence`
- `Moderate confidence`
- `Low confidence / Suggested`
- `Cannot yet be estimated`

Internal Twin bands (`very_low`…`high`) are mapped before student presentation.

## 3. Application points

1. `ReadinessService.get_dashboard_readiness_surface` — after legacy build or cutover return.
2. `ReadinessService.build_readiness_intelligence` — after assessment assemble (`apply_readiness_quality_to_assessment`).

**Must not** wrap `get_overall_readiness` (collector recursion / TwinInput safety).

## 4. Ownership rules

- **May:** attach schema; synthesise explicit drivers from authorised composite components; map confidence; label Mission-aligned next actions; refuse honestly.
- **Must not:** recalculate readiness scores; generate missions; rank recommendations; invent mastery.
- **Presentation:** `RuntimeAPresentationAdapter` pass-throughs schema-complete surfaces; must not re-evaluate.

## 5. Fail-open

Mission surface lookups catch exceptions and continue with degraded next-action defaults. Cutover / dual-run flags remain governed by EP-002.6.
