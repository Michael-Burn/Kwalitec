# V1SP-001C — Founder Operational Health Dashboard

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001C  
**Status:** Implementation complete  
**Date:** 2026-07-17  

---

## Summary

V1SP-001C transforms the Founder Command Centre from a reporting surface into an **operational decision dashboard**.

The Founder opens **Operational Health** and immediately sees:

1. **Needs Attention** — deterministic counts of what requires awareness  
2. **Healthy Activity** — current platform health signals  
3. **Trends** — short-term Version 1 activity series (no forecasting)

Overview high-level metrics are retained. Operational Health is the actionable layer beneath Overview. All insights are explainable counts derived exclusively from existing Version 1 data — no AI, scoring, weighting, student ranking, or Version 2 educational intelligence.

---

## Operational Health

| Path | Gate |
|---|---|
| `/founder/operational-health` | `@founder_required` |

Primary Command Centre navigation (updated):

Overview · **Operational Health** · Feedback · Research · Vision Journal · Releases · Settings  

Secondary destinations (Attention, Findings, Internal Alpha, Participants, System Operations) remain reachable from Overview / Operational Health footers.

Overview **Needs action** now deep-links to Operational Health.

---

## Needs Attention

Insights appear only when `count > 0`. Each card answers what happened, why it matters, and provides a primary action.

### Student Activity

| Rule ID | Definition | Action |
|---|---|---|
| `no_study_activity_7d` | Learners with an **active** plan who completed at least one session, last activity ≥ **7** days ago | Open Participants |
| `plan_never_started` | Learners with a non-archived plan and **zero** completed missions / study attempts | Open Participants |
| `prolonged_inactivity` | Active-plan learners who started, last activity ≥ **14** days ago | Open Participants |
| `revision_no_sessions` | Active plans with `revision_entered_at` set and **no** completed mission on/after that date | Open Participants |

### Engagement

| Rule ID | Definition | Action |
|---|---|---|
| `help_seeking_checkins` | Open Product Check-ins (`new` / `under_review` / `clarification_requested`) with classification **Question**, **Confusing**, or **Bug**, count ≥ **2** | Review Feedback |
| `consecutive_negative_sentiment` | Learners whose **two most recent** check-ins are both **Frustrating** or **Poor** | Review Feedback |
| `repeated_feedback` | Learners with **3+** Product Check-ins total | Open Participants |

### Product Operations

| Rule ID | Definition | Action |
|---|---|---|
| `alpha_awaiting_review` | Distinct participants with check-ins in status **New** | Open Internal Alpha |
| `feedback_awaiting_triage` | Submissions in **New** or **Clarification Requested** | Review Feedback |
| `vision_promoted_not_researched` | Vision entries with a promotion placeholder that **never** transitioned to status **research** (excludes rejected/archived) | View Vision Journal |

**Not implemented (no V1 model):** Release task due dates are not stored; overdue release tasks are omitted rather than invented.

---

## Healthy Activity

| Metric ID | Definition |
|---|---|
| `active_learners_today` | Distinct users with a completed mission or study attempt **today** |
| `study_sessions_week` | Completed missions in the last **7** calendar days |
| `revision_sessions_week` | Completed missions in-window on/after plan `revision_entered_at` |
| `missions_completed_week` | Same window as study sessions (mission completions) |
| `vision_entries_week` | Non-deleted Vision entries created in the last 7 days |
| `alpha_feedback_week` | Product Check-ins submitted in the last 7 days |
| `plans_completed_week` | Non-archived plans that entered Revision in the last 7 days |

Timezone policy: calendar day (server local date), declared on the page.

---

## Trends

Six 7-day series with CSS bar sparklines, numeric legends, and textual summaries (`role="img"` + visible summary). No Chart.js dependency; colour is not the sole state indicator.

| Series ID | Calculation |
|---|---|
| `daily_study_sessions` | Completed missions per day |
| `revision_activity` | Revision sessions per day |
| `feedback_volume` | Product Check-ins per day |
| `active_learners` | Distinct active learners per day |
| `product_checkins` | Same daily series as feedback volume (explicit product label) |
| `vision_growth` | Cumulative new Vision entries across the window |

No forecasting, projection, or smoothing beyond raw daily counts.

---

## Performance

- Prefer SQL aggregates (`COUNT`, `GROUP BY`, `MAX`) over loading full tables.  
- Study inactivity uses aggregated last-activity maps from missions + attempts.  
- Trend series are single grouped queries per signal for the 7-day window.  
- Revision-without-sessions iterates active Revision plans (Alpha-scale; count query per plan). Acceptable for Internal Alpha; may be collapsed to a left-join aggregate later if cohort size grows.

---

## Tests

### Automated

`tests/test_v1sp001c_operational_health.py`

- Founder access / student 403 / nav presence  
- Needs Attention rules (activity, engagement, product ops, vision promotion)  
- Healthy Activity counts  
- Trend length / summaries  
- Honest empty Needs Attention state  
- Overview link + Operations route regression  

Related suites re-run green: IAHF-003 Command Centre, Founder Dashboard, V1SP-001D Vision Journal.

### Manual

- Keyboard focus through insight action buttons  
- Mobile wrap of sparkline legends  
- Founder Overview → Operational Health path  

### Regression

- Overview metrics retained  
- `/founder/operations` still available as secondary System Operations  
- Student Product Check-in and learning workflows untouched  

---

## Known Limitations

| Limitation | Reason |
|---|---|
| No overdue release tasks | Version 1 has no release-task due-date model |
| No per-student Founder detail page | Actions route to Participants / Feedback / Vision |
| No notifications or email alerts | Explicitly out of scope |
| No risk scores / ranking / ML | Forbidden by milestone |
| Exam Ready / Version 2 EI | Deferred; educational cores unchanged |
| Revision idle uses per-plan counts | Fine for Alpha; not yet a single set-based query |

---

## Architecture Compliance

- Layering: routes → `OperationalHealthService` → models / aggregates  
- Observes educational evidence only; does **not** write Twin, mastery, readiness, or curriculum state  
- Deterministic, explainable counts (DP-005, DP-008, DP-012 operational analogue)  
- V1/V2 curriculum traversal untouched  

---

## Files

### Created

- `app/founder/dashboard/dto/operational_health.py`  
- `app/founder/dashboard/services/operational_health_service.py`  
- `app/founder/dashboard/templates/founder_dashboard/operational_health.html`  
- `tests/test_v1sp001c_operational_health.py`  
- `knowledge/releases/V1SP-001C_FOUNDER_OPERATIONAL_HEALTH.md`  

### Modified

- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/services/__init__.py`  
- `app/founder/dashboard/templates/founder_dashboard/overview.html`  
- `app/founder/dashboard/static/css/founder_dashboard.css`  

---

## Acceptance

| Criterion | Status |
|---|---|
| Founder identifies operational priorities immediately | Met |
| Needs Attention surfaces actionable deterministic insights | Met |
| Healthy Activity shows platform health | Met |
| Trends summarise recent activity | Met |
| Every insight links to a workflow | Met |
| No Version 2 intelligence | Met |
| Performance acceptable for Alpha | Met |
| No regressions introduced | Met (related suites green) |
