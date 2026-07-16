# LXP-002 — Study Session Experience

**Capability ID:** LXP-002  
**Programme:** Learning Experience Programme  
**Sprint:** Sprint 1  
**Title:** Study Session Experience  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product interaction — Study Session between Today's Mission and Mission Completion  

---

## Purpose

Replace the passive Today's Mission checklist with a genuine **Study Session** experience.

Students should clearly understand:

- what topic they are studying  
- why they are studying it  
- approximately how long  
- what success looks like today  

Then take an intentional **Start Study Session** action, work through a dedicated session screen, finish the session, and record only whether planned study was completed.

This capability does **not** redesign Educational Intelligence, Digital Twin, Evidence, Readiness, Recommendations, or Mission generation.

---

## Workflow

```
Today's Mission (briefing)
        ↓
Start Study Session
        ↓
Study Session Screen
        ↓
Finish Study Session
        ↓
Study Session Review (Yes / Partially / No + optional notes)
        ↓
Study Session Recorded (truthful explainability)
```

### Routes

| Step | Route |
|------|--------|
| Briefing | `GET /missions/` |
| Start | `POST /missions/<id>/session/start` |
| Session | `GET /missions/<id>/session` |
| Review | `GET|POST /missions/<id>/session/finish` |
| Recorded | `GET /missions/<id>/session/recorded` |

Legacy `POST /missions/<id>/complete` remains as a PTP-002 compatibility
redirect/delegate into the Study Session path; it does not write educational
state. The student UI uses Study Session → Practice Outcome Capture.

### Study Session screen includes

- Topic  
- Learning objective  
- Estimated duration  
- Recommended activities (educational prompts)  
- Progress checklist (client-side ticks for activities)  
- Elapsed timer (IAHF-001: **active study time** — Pause freezes elapsed; Resume continues without adding paused duration; Version 1 state is browser-local)  
- **Pause Study Session** / **Resume** (timer control on the session screen)  
- **Finish Study Session**  

Recommended activities (Version 1 prompts):

- Read today's topic  
- Work through examples  
- Attempt practice questions  
- Review mistakes  

No question scores are collected here (LXP-003).

---

## Educational meaning

Completing a Study Session means:

> Today's planned learning activity occurred.

It does **not** mean:

- Understanding increased  
- Knowledge increased  
- Mastery increased  
- Educational Evidence of understanding was created  

---

## State transitions

| Reviewer answer | Mission | Study Progress | Estimates | Evidence |
|-----------------|---------|----------------|----------|----------|
| **Yes** | Completed (tasks marked done) | May update (existing lawful coverage path) | Unchanged | No authorised understanding Evidence |
| **Partially** | Completed (day closed) | Unchanged | Unchanged | No authorised understanding Evidence |
| **No** | Remains In Progress | Unchanged | Unchanged | No authorised understanding Evidence |

May update:

- Mission completion  
- Study Progress (existing lawful behaviour on **Yes** only)

May **not** update:

- Estimated Knowledge  
- Estimated Mastery  
- Educational Evidence of understanding  
- Readiness maths  
- Recommendation ranking  

A lightweight `StudyAttempt` may be written with completion notes only (no scores, no confidence). That attempt is **not** authorised Structured Question Results under Educational Evidence Authority.

### Explainability (recorded screen)

Always educationally truthful:

1. Today's study session has been recorded.  
2. Your study progress has been updated. — *or* Your study progress has not been changed.  
3. Question results can be added in a future step to improve educational guidance.  

---

## Architecture compliance

Preserves:

- Educational Constitution  
- Educational Logic Registry  
- Evidence Authority  
- Learning Mode  
- State Ownership  

Layering: blueprints → `StudySessionService` / existing Mission & Learning services → models. No Twin, Readiness, or Recommendation redesign.

Service module: `app/services/study_session_service.py`.

---

## Known limitations

1. Study materials remain external (Core Reading / notes outside the app).  
2. Activity checklist ticks are local (sessionStorage) — not persisted as Educational Observations.  
3. No performance / question-result capture (deferred to LXP-003).  
4. No confidence / soft reflection capture in this capability.  
5. Partially closes the daily Mission without advancing Study Progress (honest understatement).  
6. Legacy mission review form (`/missions/review/...`) redirects to Practice
   Outcome Capture / Study Session Feedback (PTP-002) and is not a student write path.
7. Legacy `POST /missions/<id>/complete` delegates to the Study Session path
   (PTP-002); it no longer records attempts or Study Progress itself.
8. **IAHF-001 timer continuity (Version 1):** active elapsed time and Pause/Resume
   state are stored in the current browser profile (`localStorage`). Clearing
   browser data or switching devices resets the timer. This is acceptable for
   Internal Alpha; server-persisted timer continuity is a candidate for a future
   release if cross-device continuity becomes a common expectation.

---

## Cross references

- `LEARNING_EXPERIENCE_PROGRAMME.md` (LXP-001) — programme design  
- `KWALITEC_EDUCATIONAL_CONSTITUTION.md`  
- `EDUCATIONAL_LOGIC_REGISTRY.md`  
- `EDUCATIONAL_EVIDENCE_AUTHORITY.md`  
- `BLIND_INTERNAL_ALPHA_REVIEW.md` — product evidence for checklist → session gap  
