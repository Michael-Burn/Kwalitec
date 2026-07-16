# PTP-002 — Single Source of Truth

**Capability ID:** PTP-002  
**Programme:** Product Trust Programme  
**Title:** Single Source of Truth (Single Daily Workflow)  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product trust — one authoritative student workflow per educational event  

---

## Purpose

Ensure every educational event in Version 1 has **exactly one** authoritative
student workflow.

This capability removes duplicate educational paths that create uncertainty
about which interaction is the “real” one. It does **not** redesign Educational
Constitution, Learning Experience educational meaning, Evidence Authority,
Digital Twin, Educational Intelligence, Recommendation logic, or Readiness.

The objective is **workflow authority**, not code deletion.

---

## Authoritative Version 1 daily closure

```
Today's Mission
        ↓
Start / Resume Study Session          (LXP-002)
        ↓
Study Session screen
        ↓
Finish Study Session
        ↓
Practice Outcome Capture              (LXP-003)
  ├── Record practice results
  └── or “I didn't practise today”
        ↓
Study Session Feedback                (LXP-004)
```

This is the **only** student journey that may record today’s study completion,
practice outcomes, and educational feedback for a daily mission.

---

## 1. Workflow Authority Matrix

| Educational event | Student meaning | State owner (write) | Authoritative student workflow | Student-visible |
|-------------------|-----------------|---------------------|--------------------------------|-----------------|
| **Study Session start** | Today’s study has begun | Mission status → In Progress (`StudySessionService.start_session`) | `POST …/session/start` → `GET …/session` | Yes |
| **Study completion / Mission Completed** | Today’s planned study was engaged and closed | Mission status → Completed (`MissionService.complete_mission` via Study Session service only) | Practice Outcome Capture submit **or** skip-practice finish | Yes (as closure of the Study Session path) |
| **Practice outcomes** | Observed practice counts for today | `StudyAttempt` + Evidence Authority path (`StudySessionService.record_practice_outcome`) | `GET\|POST …/session/finish` (Practice Outcome Capture) | Yes |
| **Session feedback** | Honest narrated reflection of what was recorded | Presentation only (`StudySessionService.build_session_feedback`) | `GET …/session/recorded` | Yes |
| **Study Progress (`TopicProgress.completed`)** | “I have studied this syllabus topic” | `_apply_mission_topic_progress` / lawful Mission Completion callers | Not a competing student form — may be applied by callers of lawful Mission Completion; **not** written by legacy HTTP redirects | Internal + existing surfaces |
| **Reflection (retired)** | Formerly: confidence + mistakes + practice | — (no student write) | Redirects to Practice Outcome Capture / Feedback | Legacy URL only |

### HTTP authority (student)

| Step | Route | Role |
|------|--------|------|
| Briefing | `GET /missions/` | Opens the day; CTAs point only into Study Session |
| Start | `POST /missions/<id>/session/start` | Authoritative start |
| Session | `GET /missions/<id>/session` | Authoritative study container |
| Practice / close | `GET\|POST /missions/<id>/session/finish` | Authoritative practice + close |
| Feedback | `GET /missions/<id>/session/recorded` | Authoritative feedback |

### Internal (not competing journeys)

| Mechanism | Role after PTP-002 |
|-----------|--------------------|
| `MissionService.complete_mission` | Internal status transition used by `StudySessionService` |
| `StudySessionService.finish_session` | Service-level / skip-practice compatibility |
| `POST /missions/tasks/<id>/toggle` | Optional task UI helper; does not close the day alone |
| `POST /missions/<id>/complete` | **Legacy** — redirects / JSON-delegates; **never** writes educational state |
| `GET\|POST /missions/review/<id>` | **Legacy** — redirects; **never** creates StudyAttempt / mistakes / completion |

---

## 2. Duplicate Workflow Audit

Identified from Blind Internal Alpha Review v2 and route inventory.

| Workflow | Purpose (historical) | Competing with | Student visibility before PTP-002 | Verdict |
|----------|----------------------|----------------|-----------------------------------|---------|
| Study Session → Practice Outcome → Feedback | Record and close today’s study honestly | — | Primary CTA on Daily Mission | **Authority** |
| `POST /missions/<id>/complete` | Mark mission complete + create attempt + Study Progress | Mission Completed + practice recording | Called from legacy `mission.js` “Mark Complete” | **Deprecate → delegate** |
| `GET\|POST /missions/review/<id>` (“Reflect on Your Learning”) | Confidence, notes, mistakes, practice counts | Practice Outcome Capture + Feedback | Full second form | **Deprecate → redirect** |
| `mission/session_review.html` (Yes / Partially / No) | Completion-only review | Practice Outcome Capture | Orphan template (no student route) | **Internal / retired UI** |
| Dashboard loading `mission.js` with Mark Complete semantics | Alternate close | Study Session path | Script present without active CTA | **Removed from Dashboard** |

### Student pain this closes

> “Two different ‘how did it go?’ screens… I wasn’t sure which was the real one.”  
> — Blind Internal Alpha Review v2

---

## 3. Migration strategy

1. **Keep LXP Sprint 1 loop as-is** for educational meaning and Evidence rules.
2. **Stop student-facing writes** on legacy complete and review HTTP handlers.
3. **Redirect or JSON-delegate** those URLs into `…/session/finish` (open mission) or
   `…/session/recorded` (already completed).
4. **Preserve service APIs** (`MissionService.complete_mission`,
   `StudySessionService.finish_session`) for tests and orchestration.
5. **Leave templates/forms** in the tree for a short compatibility window, but
   unhook them from student journeys.

### Compatibility behaviour

| Legacy entry | Open mission | Completed mission |
|--------------|--------------|-------------------|
| `POST /missions/<id>/complete` (JSON) | `{ delegated: true, redirect_url: …/session/finish }` | `{ delegated: true, redirect_url: …/session/recorded }` |
| `POST /missions/<id>/complete` (HTML) | 302 → finish | 302 → recorded |
| `GET /missions/review/<id>` | 302 → finish | 302 → recorded |
| `POST /missions/review/<id>` | Flash + 302 → finish (no DB write) | Flash + 302 → recorded (no DB write) |

Pending missions touched via legacy redirect are started first (same posture as
opening the Study Session screen), then sent to Practice Outcome Capture.

---

## 4. Deprecation plan

| Artefact | Near term | Later |
|----------|-----------|--------|
| `POST …/complete` | Delegate only | Remove after no external clients remain |
| `GET\|POST …/review/…` | Redirect only | Remove route + `mission/review.html` |
| `MissionReviewForm` / `MistakeForm` | Retained, documented retired | Delete with review template |
| `session_review.html` | Unrouted | Delete when LXP-002 compatibility tests no longer need the pattern |
| `mission.js` Mark Complete fetch | Navigates to `/session/finish` | Delete Mark Complete binder when no page uses `data-mission-id` complete buttons |

---

## Student guarantees

A student must never be able to:

- record the same educational event twice through parallel student forms;
- complete the same mission using a second path that also writes StudyAttempts;
- wonder which screen represents today’s study (Daily Mission CTAs + redirects
  all converge on the Study Session path).

Re-submitting Practice Outcome Capture after Mission Completed is rejected by
`StudySessionService` (`This study session has already been recorded.`).

---

## Out of scope

- Redesign of Educational Constitution, Evidence Authority, Twin, EI,
  Recommendations, or Readiness
- Changes to practice field definitions or feedback narrative content
- Deleting all legacy files in this milestone

---

## Cross references

| Document | Relationship |
|----------|--------------|
| `PRODUCT_TRUST_PROGRAMME.md` | Programme parent; Capability 2 brief |
| `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` | Release Blocker 2 — dual “how did it go?” |
| `LXP-002_STUDY_SESSION_EXPERIENCE.md` | Study Session authority |
| `LXP-003_PRACTICE_OUTCOME_CAPTURE.md` | Practice outcome authority |
| `LXP-004_STUDY_SESSION_FEEDBACK.md` | Feedback authority |
| `tests/test_ptp002_single_source_of_truth.py` | Regression coverage |

---

## Implementation map

| Area | Location |
|------|----------|
| Legacy complete / review HTTP | `app/mission/routes.py` |
| Closure orchestration | `app/services/study_session_service.py` |
| Legacy JS navigation | `app/static/js/mission.js` |
| Dashboard script cleanup | `app/templates/dashboard/index.html` |
