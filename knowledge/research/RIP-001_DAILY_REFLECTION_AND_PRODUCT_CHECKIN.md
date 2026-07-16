# RIP-001 — Daily Reflection & Product Check-in

**Capability ID:** RIP-001  
**Programme:** Research Intelligence Programme  
**Title:** Daily Reflection & Product Check-in  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-16  
**Nature:** Product research — optional post-study structured check-in  

---

## Purpose

Replace the manual daily text-file feedback process with an integrated,
lightweight product research experience inside Kwalitec.

Students contribute high-quality structured product feedback while adding
almost no friction to the study routine. The experience should feel like the
natural closing step of a study session, not a survey.

Educational feedback (LXP-004) and product feedback remain completely
independent.

---

## Hard boundary

Research Intelligence observes **product experience**.  
Educational Intelligence observes **learning**.

This capability must never:

- write Educational Evidence, Estimated Knowledge/Mastery, Study Progress,
  readiness, mission authority, or Digital Twin educational state;
- replace or mutate LXP-004 Study Session Feedback;
- introduce badges (RIP-002), Founder dashboards (RIP-003), or analytics.

---

## Workflow

```
Study Session Feedback (LXP-004)
        ↓
Continue (optional invitation)
        ↓
Daily Reflection & Product Check-in
        ↓
Thank you → Return to Dashboard
```

Secondary entry:

```
Settings → Share Feedback
  (or sidebar Share Feedback)
        ↓
Daily Reflection & Product Check-in
```

Students may dismiss without penalty. Unlimited submissions are allowed.

---

## Eligibility (invitation)

Display the post-study invitation when:

- today's Study Session has been completed (`Mission.status == Completed`), or
- at least part of today's mission has been completed (any task `completed`).

Settings / sidebar Share Feedback does **not** require eligibility.

---

## Question set

| # | Prompt | Type |
|---|--------|------|
| 1 | How was your experience using Kwalitec today? | Excellent / Good / Okay / Frustrating / Poor |
| 2 | Which part of Kwalitec helped you the most today? | Study Session, Today's Mission, Dashboard, Study Plan, Recommendations, Analytics, Settings, Other |
| 3 | Did anything make studying harder today? | Nothing, Navigation, Terminology, Study Plan, Dashboard, Recommendations, Analytics, Study Session, Performance, Other |
| 4 | How confident are you that Kwalitec helped you study today? | Very Low → Very High |
| 5 | Would you choose to open Kwalitec again tomorrow? | Definitely → Definitely Not |
| Optional | Anything else you'd like us to know? | Free text, max 300 chars |
| If text | Classification | Bug / Suggestion / Praise / Question / Confusing / Other |

---

## Data captured

Each completed check-in stores:

- Timestamp (`submitted_at`)
- User
- Product version (`1.0.0`)
- Study Plan (when known)
- Mission (when known)
- Feature selected (`feature_helped_most`)
- Ratings (experience, friction, confidence, return intent)
- Classification (when free-text present)
- Optional text
- Submission source (`study_session` | `settings`)

Every completed check-in also creates **one Contribution** row.
No badges. No trend computation. Structured for RIP-003.

---

## Routes

| Route | Role |
|-------|------|
| `GET\|POST /research/checkin` | Check-in form |
| `GET /research/thank-you` | Thank-you screen |
| `GET /research/dismiss` | Skip without penalty |
| `GET /settings/share-feedback` | Settings entry → check-in |

---

## Architecture

```
Templates/JS → research blueprint → ResearchFeedbackService → Models → DB
```

Layering is preserved. Research Intelligence remains independent from
Educational Intelligence. Curriculum V1/V2 traversal is untouched.

---

## Files

### Created

- `app/services/research_feedback_service.py`
- `app/models/research_feedback.py`
- `app/research/` (blueprint, forms, routes)
- `app/templates/research/checkin.html`
- `app/templates/research/thank_you.html`
- `migrations/versions/202607160001_create_research_feedback_tables.py`
- `tests/test_rip001_daily_checkin.py`
- `knowledge/research/RIP-001_DAILY_REFLECTION_AND_PRODUCT_CHECKIN.md`

### Modified

- `app/__init__.py` — model import + blueprint registration
- `app/models/__init__.py` — exports
- `app/templates/mission/session_recorded.html` — Continue invitation
- `app/templates/settings/index.html` — Share Feedback nav
- `app/templates/partials/sidebar.html` — Share Feedback link
- `app/settings/routes.py` — `share_feedback` redirect

---

## Out of scope

- Badges / recognition scoring (RIP-002)
- Founder Intelligence Dashboard (RIP-003)
- Insight Engine / trends (RIP-004)
- Changes to Educational Constitution, Evidence Authority, Twin, LXP algorithms
