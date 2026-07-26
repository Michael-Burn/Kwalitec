# EP-004.2 — Personalisation Rules

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Module:** `app/services/recommendation_personalisation.py`  
**Authority:** RecommendationService (profile = evidence only)  
**Schema version:** `ep004.2/v1`

---

## Global gates (all rules)

1. Attribute `status` must be `available` (ignore `unavailable` / `unsupported`).
2. Attribute `kind` must not be `unsupported`.
3. Confidence ≥ **0.3** and sample_size ≥ **3**, except declared session duration (confidence 1.0, sample ≥ 1).
4. Never change `decision_ladder_rank` for ranks **1–3** (safety, authorised Today’s Mission, blocking deficit) or honest refusal.
5. Never invent educational warrants; never promote categories from accept rate.
6. Fail-open: missing profile → baseline EP-003.1 ordering.

---

## Rule catalogue

### R1 — Ordering (tie-break only)

| Attribute | Condition | Effect | Explainability |
|---|---|---|---|
| `revision_adherence` | adherence_rate ≥ 0.6 | Prefer Revision/Review within same ladder+priority | Factor `prefer_revision_adherence` |
| `recovery_effectiveness` | follow_through_rate ≥ 0.5 | Prefer Weak Topic/Review within band | `prefer_recovery_follow_through` |
| `recovery_effectiveness` | follow_through_rate < 0.3 | Soften Weak Topic pressure within band | `prefer_lighter_recovery` |
| `consistency_trend` | direction = declining | Prefer Rest; soften New Topic within band | wellbeing / soften factors |
| `planning_completion_rate` | completion_rate < 0.4 | Defer Mock Exam within band | `defer_heavy_mock_when_completion_low` |

Sort key after personalisation:

`decision_ladder_rank → legacy priority → personalisation_tie_break → title`

### R2 — Recovery strategy preference

Uses `recovery_effectiveness` as a **behavioural follow-through proxy** (not “recovery fixed the deficit”). Adjusts within-band preference only; does not create recovery missions (Planning remains owner).

### R3 — Session sizing guidance

| Attribute | Condition | Effect |
|---|---|---|
| `preferred_study_session_duration` | declared minutes > 0 | Annotate `session_sizing_guidance` + append to next action |

Never invents minutes when unsupported.

### R4 — Recommendation cadence

| Attribute | Condition | Effect |
|---|---|---|
| `recommendation_responsiveness` | sample ≥ 5 and accept_rate < 0.3 | Cap secondary tips (≤3) and omit Study Strength extras |

High accept rate does **not** promote categories (Art. V §2).

### R5 — Confidence / explanation adjustments

When any factor applies:

- `personalisation_applied = True`
- `personalisation_factors` lists attribute, confidence, claim_boundary, effect, detail
- `supporting_evidence` / `observed_facts` gain student-safe personalisation lines
- `why_recommended` / `reason` note that habits influenced the tip
- `personalisation_profile_id` stamped for provenance

Recommendation educational `confidence_level` remains density-driven (EP-003.1); profile confidence gates *whether* personalisation applies, not a readiness score.

### Unsupported

| Attribute | Rule |
|---|---|
| `preferred_study_windows` | Always no-op until lawful evidence exists |

---

## Ownership reminder

Personal Learning Profile supplies attributes.  
RecommendationService decides whether and how they influence tips.  
RuntimeAPresentationAdapter displays resulting explanations only.
