# LXP-003 — Practice Outcome Capture

**Capability ID:** LXP-003  
**Programme:** Learning Experience Programme  
**Sprint:** Sprint 1  
**Title:** Practice Outcome Capture  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product interaction — Observed Practice Outcomes after Finish Study Session  

---

## Purpose

Record objective practice outcomes immediately after a student finishes a Study Session.

These outcomes create **lawful Educational Evidence inputs** (structured question results) so Estimated Knowledge, analytics, and educational guidance can improve when authorised paths allow.

This capability does **not** redesign:

- Educational Evidence Authority  
- Digital Twin  
- Educational Intelligence  
- Learning Mode  
- Recommendation logic  
- Readiness algorithms  

---

## Educational meaning

Submitted values are **Observed Practice Outcomes**.

They are **not**:

- Knowledge  
- Mastery  
- Competence  
- Readiness  

Attempt ≠ Success ≠ Mastery. Practice creates an Observation / Evidence opportunity; it does not certificate the topic.

---

## Workflow

```
Today's Mission
        ↓
Start Study Session (LXP-002)
        ↓
Study Session Screen
        ↓
Finish Study Session
        ↓
Practice Outcome Capture (this capability)
        ↓
Practice Results Recorded (plain-language success)
```

### Routes

| Step | Route |
|------|--------|
| Session | `GET /missions/<id>/session` |
| Capture | `GET\|POST /missions/<id>/session/finish` |
| Recorded | `GET /missions/<id>/session/recorded` |

The previous completion-only Yes / Partially / No review is no longer the student primary path after Finish. Service-level `finish_session` remains for compatibility tests.

---

## Observed facts collected

| Field | Required | Meaning |
|-------|----------|---------|
| Questions Attempted | Yes | Count of practice questions tried (> 0) |
| Questions Correct | Yes | Count answered correctly (0 … Attempted) |
| Time spent answering questions | Optional | Minutes spent on practice questions |
| Notes | Optional | Free-text practice notes |

### Not collected

- Confidence  
- Mastery  
- Understanding ratings  
- Difficulty rating  
- Readiness  

---

## Validation

- Questions Attempted must be greater than zero.  
- Questions Correct must be ≥ 0 and ≤ Questions Attempted.  
- Impossible values are rejected (form + service).  

---

## State transitions

| On successful submit | Effect |
|----------------------|--------|
| Mission | Completed (session closed) |
| StudyAttempt | Created, or updated if a scoreless attempt already exists |
| Educational Evidence Authority | Invoked via existing `LearningService` structured-results gate |
| Estimated Knowledge | May update only through the existing authorised estimation path |
| Study Progress (`completed`) | **Not** written by this capability |
| Readiness maths | **Not** invoked |
| Recommendations | **Not** invoked |

Downstream consumers (analytics, readiness, recommendations, guidance) may later read authorised evidence; this capability does not call them.

### Success message (student-facing)

> Your practice results have been recorded.  
> Kwalitec will use objective practice outcomes to improve future educational guidance when appropriate.

Avoid AI, Twin, and Evidence jargon in the student UI.

---

## Architecture compliance

Preserves:

- Educational Constitution  
- Educational Logic Registry  
- Evidence Authority  
- State Ownership  
- Learning Mode  

Layering: blueprints → `StudySessionService.record_practice_outcome` → `LearningService` / Evidence Authority → models. No Twin, Readiness, or Recommendation redesign.

Service entry point: `app/services/study_session_service.py` (`record_practice_outcome`).

---

## Version 1 limitations

1. Practice results are **student-attributed** (self-reported counts), not an in-app question engine.  
2. Study Progress coverage is not advanced by Practice Outcome Capture (remains a separate lawful path).  
3. Optional time and notes are Observations only — they do not alone authorise understanding Evidence.  
4. No confidence / reflection capture in this capability.  
5. Students who practised zero questions cannot submit (attempted must be > 0).  
6. Legacy mission review form (`/missions/review/...`) redirects to the Study
   Session closure path (PTP-002) and no longer writes educational state.
7. Legacy `POST /missions/<id>/complete` delegates to the same path (PTP-002).

---

## Cross references

- `LEARNING_EXPERIENCE_PROGRAMME.md` (LXP-001) — Step 3 Question Practice  
- `LXP-002_STUDY_SESSION_EXPERIENCE.md` — Study Session before Finish  
- `EDUCATIONAL_EVIDENCE_AUTHORITY.md` / EIP-002 — Structured Question Results gate  
- `KWALITEC_EDUCATIONAL_CONSTITUTION.md`  
- `EDUCATIONAL_LOGIC_REGISTRY.md`  
- `BLIND_INTERNAL_ALPHA_REVIEW.md` — practice outcome gap  
