# RIP-002 — Contributor Recognition

**Capability ID:** RIP-002  
**Programme:** Research Intelligence Programme  
**Title:** Contributor Recognition  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-16  
**Nature:** Product research — gratitude and journey visibility for Internal Alpha participants  

---

## Purpose

Thank Internal Alpha participants for helping improve Kwalitec through structured
Product Check-ins. Recognition celebrates consistency and constructive
participation — never competition, volume, or verbosity.

This capability is **not gamification**.

---

## Recognition philosophy

Recognition rewards:

- consistency
- constructive participation
- meaningful contribution

Recognition does **not** reward:

- longest comments
- most submissions
- competition
- leaderboard position

Research Principle: recognition should celebrate contribution, never create
pressure to contribute.

---

## Contributor journey

```
Explorer
    ↓
Research Partner
    ↓
Core Contributor
    ↓
Product Shaper
    ↓
Founder's Circle
```

| Badge | Award |
|-------|-------|
| Explorer | First completed Product Check-in |
| Research Partner | 10 Product Check-ins |
| Core Contributor | 25 Product Check-ins |
| Product Shaper | Founder marks feedback **Implemented** |
| Founder's Circle | Founder invitation only |

Students see their **current** badge (highest earned), progress toward the
**next** badge, and contribution count. No rankings. No leaderboards.

---

## Hard boundary

Research Intelligence observes **product experience**.  
Educational Intelligence observes **learning**.

This capability must never:

- write Educational Evidence, Estimated Knowledge/Mastery, Study Progress,
  readiness, mission authority, or Digital Twin educational state;
- introduce leaderboards, daily streaks, competition, or visible points;
- mutate LXP-004 Study Session Feedback.

---

## Founder controls

Founders may review any Product Check-in submission:

| Mark | Effect |
|------|--------|
| Helpful | Qualitative signal for RIP-003 (no badge) |
| Insightful | Qualitative signal for RIP-003 (no badge) |
| Implemented | Awards **Product Shaper** when feedback influenced a shipped improvement |

Founders may also award **Founder's Circle** by invitation via a dedicated
Founder route.

---

## Architecture

```
Templates → research / settings blueprints → Services → Models → DB
```

- `ContributorRecognitionService` — badge rules, journey summary, Founder review
- `ResearchFeedbackService.submit_checkin` — creates Contribution, then evaluates automatic badges
- Layering preserved. Curriculum V1/V2 untouched.

---

## Routes

| Route | Role |
|-------|------|
| `GET /research/thank-you` | Journey summary after check-in |
| `GET /settings/profile` | Persistent Research Journey |
| `GET\|POST /research/founder/review/<id>` | Founder marks on feedback |
| `POST /research/founder/award-founders-circle/<user_id>` | Invitation-only award |

---

## Files

### Created

- `app/services/contributor_recognition_service.py`
- `migrations/versions/202607160002_create_contributor_recognition_tables.py`
- `app/templates/research/founder_review.html`
- `tests/test_rip002_contributor_recognition.py`
- `knowledge/research/RIP-002_CONTRIBUTOR_RECOGNITION.md`

### Modified

- `app/models/research_feedback.py` — `ResearchContributorBadge`, `ResearchFeedbackReview`
- `app/models/__init__.py`
- `app/__init__.py` — model registration
- `app/services/research_feedback_service.py` — badge evaluation after check-in
- `app/research/routes.py` — thank-you context, Founder review routes
- `app/research/forms.py` — `FounderFeedbackReviewForm`
- `app/settings/routes.py` — profile journey context
- `app/templates/research/thank_you.html` — appreciation and progress
- `app/templates/settings/index.html` — Research Journey section

---

## Out of scope

- Founder Intelligence Dashboard integration (RIP-003)
- Insight Engine / trends (RIP-004)
- Leaderboards, streaks, points, or competition mechanics
- Changes to Educational Constitution or learning algorithms
