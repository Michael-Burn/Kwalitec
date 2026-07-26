# RecommendationService Quality Contract (EP-003.1)

**Status:** Active  
**Authority:** Runtime A recommendation communication  
**Implements:** P-001.2 Mandatory Explanation Schema; P-001.3 Decision Framework  
**Owner module:** `app/services/recommendation_quality.py` (called only from `RecommendationService`)

---

## 1. Purpose

Define the serialisable contract every Runtime A recommendation row must satisfy before student presentation.

## 2. Mandatory fields

| Field | Meaning |
|---|---|
| `title` | Recommendation (what) |
| `why_recommended` / `reason` | Why it is recommended |
| `supporting_evidence` | Supporting evidence list |
| `confidence_level` | Honest confidence label |
| `expected_benefit` | Expected educational benefit |
| `suggested_next_action` / `next_action` | One clear next action |
| `review_point` | When to reassess |
| `decision_ladder_rank` | P-001.3 ladder rank (1–9, or 99 deferred) |
| `plan_coherence` | `aligned` / `advisory` / `wellbeing` / `deferred` / … |
| `explanation_schema_version` | `p001.2/v1` |
| `explanation_level` | Default `level_2` |
| `explanation_schema_complete` | `True` when schema attached |

Optional / sentinel:

| Field | Meaning |
|---|---|
| `honest_refusal` | Prefer “No recommendation yet” over fabricated tips |
| `source_authority` | `legacy` / `study_insights` |

## 3. Ranking

1. Apply hard gates (schema readiness; thin-evidence refusal for mock/technique theatre).
2. Sort by `decision_ladder_rank`, then legacy priority, then title (baseline Decision Framework).
3. Deduplicate by title.
4. **EP-004.2:** optional Personal Learning Profile consumer view may apply bounded
   personalisation (`recommendation_personalisation.py`):
   - confidence-gated tie-breaks (`personalisation_tie_break`) within the same
     ladder + priority band
   - session-sizing guidance from declared preferred minutes
   - tip cadence softening on high dismiss rate (never category promotion from accepts)
   - never reclassify safety / authorised Today’s Mission / blocking deficit ranks
5. Slice to limit.

Personalisation fields (when applied): `personalisation_applied`,
`personalisation_factors`, `personalisation_schema_version`, optional
`session_sizing_guidance`, `personalisation_profile_id`.

## 4. Ownership rules

- **May:** rank authorised candidates; attach schema; label Mission coherence; refuse honestly; apply bounded profile-evidence personalisation.
- **Must not:** invent readiness scores, generate missions, recalculate Planning maths, or delegate ranking to the Personal Learning Profile.
- **Presentation:** `RuntimeAPresentationAdapter` pass-throughs schema-complete rows (including personalisation fields); must not re-rank or inspect the profile.

## 5. Fail-open

Mission surface, evidence-density, and profile personalisation lookups catch exceptions and continue with degraded coherence/confidence/baseline ranking defaults.
Profile flag OFF or resolve failure → identical to EP-003.1 baseline ordering.
