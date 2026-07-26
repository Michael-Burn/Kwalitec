# EP-004.3 — Personalisation Rules

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Module:** `app/services/planning_personalisation.py`  
**Authority:** PlanningService (profile = evidence only)  
**Schema version:** `ep004.3/v1`

---

## Global gates (all rules)

1. Attribute `status` must be `available` (ignore `unavailable` / `unsupported`).
2. Attribute `kind` must not be `unsupported`.
3. Confidence ≥ **0.3** and sample_size ≥ **3**, except declared session duration (confidence 1.0, sample ≥ 1).
4. Never change educational slot order: **review → recovery/weak → progression**.
5. Never invent missions, mastery, readiness scores, or recommendations.
6. Never use `recommendation_responsiveness` (accept/dismiss) as a plan driver.
7. Fail-open: missing profile → baseline EP-003.3 plan.
8. If educational order would be violated after adaptations → abort personalisation.

---

## Rule catalogue

### P1 — Session duration

| Attribute | Condition | Effect | Explainability |
|---|---|---|---|
| `preferred_study_session_duration` | declared minutes > 0 | Align `recommended_minutes` toward preferred (clamped to available; min 20); rebalance slot minutes; annotate guidance | `session_duration_alignment` / `session_duration_guidance` |

### P2 — Workload pacing

| Attribute | Condition | Effect |
|---|---|---|
| `planning_completion_rate` | completion_rate < 0.4 | Reduce recommended minutes by ~10% (min 20) |
| `consistency_trend` | direction = declining | Reduce recommended minutes by ~10% (min 20) |

Effects: `pace_reduce_when_completion_low`, `pace_reduce_when_consistency_declining`.

### P3 — Recovery sequencing

| Attribute | Condition | Effect |
|---|---|---|
| `recovery_effectiveness` | follow_through ≥ 0.5 and repair + progression present | Transfer up to 5 minutes from progression → recovery/weak |
| `recovery_effectiveness` | follow_through < 0.3 | Lighten repair minutes (up to 5); may return to progression |

Slot **types and order unchanged**. Effects: `recovery_emphasise_follow_through`, `recovery_lighten_low_follow_through`.

### P4 — Revision timing

| Attribute | Condition | Effect |
|---|---|---|
| `revision_adherence` | adherence ≥ 0.6 and review present | Boost review minutes from progression; reinforce review-first next action |
| `revision_adherence` | adherence < 0.3 and review present | Protect review completion messaging (do not remove review) |

Effects: `revision_boost_adherence`, `revision_protect_when_deferred_risk`.

### P5 — Equivalent slot selection

| Attribute | Condition | Effect |
|---|---|---|
| `recovery_effectiveness` | follow_through < 0.3; weak/recovery on revision_priorities[0]; ≥2 priorities | Swap repair topic to priorities[1] (same educational role) |

Effect: `equivalent_repair_topic_preference`. Never invents topics outside the revision pool.

### Unsupported / unused

| Attribute | Rule |
|---|---|
| `preferred_study_windows` | Always no-op until lawful evidence exists |
| `recommendation_responsiveness` | Explicitly unused by Planning (Recommendation authority) |

---

## Explanation contract

When any factor applies:

- `personalisation_applied = True`
- `personalisation_factors` lists attribute, confidence, claim_boundary, effect, detail
- `supporting_evidence` / `observed_facts` gain student-safe personalisation lines
- `why_this_plan` / `change_reasoning` note habit influence
- `personalisation_profile_id` stamped for provenance

---

## Ownership reminder

Personal Learning Profile supplies attributes.  
PlanningService decides whether and how they influence the day plan.  
RuntimeAPresentationAdapter displays resulting explanations only.
