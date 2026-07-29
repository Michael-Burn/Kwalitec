# Session Continuity Spec

**Programme:** DX-005A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Companions:** `MISSION_MODEL.md`, `STUDENT_HOME_ARCHITECTURE.md`  
**Principle:** The platform remembers. The student progresses. No manual recovery.

---

## 1. Goal

Leaving a learning activity and returning via Home must restore context so the student never asks:

> Where was I?

Home is the **recognition + resume** surface. Session / Assessment own execution state. Persistence is server-side (and client only as cache), not “remember in your head.”

---

## 2. Continuity contract

### Must restore on return (tomorrow or same day)

| Dimension | Restore to | Surface that shows it |
|---|---|---|
| **Subject** | Active exam / curriculum identity | Home L0 subject |
| **Current lesson / objective** | Syllabus position in progress | Home L0 objective |
| **Mission status** | Operational enum | Home L0 status |
| **Open session** | Same `session_id` | Primary → Session |
| **Current chapter** | Last active chapter/section | Session (Home may hint in why-now) |
| **Current question** | Last unanswered / in-progress item where appropriate | Session; Home why-now may say “continue question N” |
| **Assessment progress** | Item index / answered set | Assessment; Home Primary Start/Continue Assessment |
| **Timer state** | Remaining / elapsed where product uses timers | Assessment/Session — restore, do not reset silently |
| **Findings pending** | Unreviewed results | Home Primary **Review Findings** |

### Must not require

- Re-selecting subject  
- Re-running Choose Exam  
- Re-committing the same mission solely to resume  
- Manually finding session id  
- Restarting from chapter 1 after accidental leave  

---

## 3. Leave paths

| Leave event | Persist | Home on return |
|---|---|---|
| Browser close mid-session | Session state + pointer | Continue Session |
| Navigate to Home mid-session | Same | Continue Session |
| Navigate to History / Settings | Same | Continue Session |
| Complete session | Close session; advance mission pointer | Next mission or quiet complete |
| Mid-assessment exit | Assessment progress | Start / Continue Assessment |
| Findings generated, not reviewed | Findings flag | Review Findings |
| Explicit abandon (if product allows) | Mark abandoned; clear open pointer | Next ready mission — never zombie Continue |

---

## 4. Home Primary resume rules

```
IF open_session EXISTS for active subject
  → Primary = Continue Session
  → href/post restores session at chapter + question
ELSE IF findings_pending
  → Primary = Review Findings
ELSE IF assessment_in_progress OR assessment_ready
  → Primary = Start Assessment / Continue Assessment
ELSE IF mission_ready
  → Primary = Start Session / Resume Mission
ELSE
  → quiet complete OR empty (Choose Exam)
```

**One click** from Primary to restored execution surface.

---

## 5. Persistence responsibilities

| Layer | Responsibility |
|---|---|
| **Domain / services** | Canonical session, assessment, mission pointers |
| **Home view-model** | Read continuity DTO; never invent progress |
| **Session UI** | Apply restore coordinates on load |
| **Client storage** | Optional UX cache only — not source of truth |

Home must not hold the only copy of continuity. If Home render fails, Session deep-link from a notification must still restore.

---

## 6. Continuity DTO (Home-facing)

```
continuity:
  subject_id
  subject_name
  objective_id
  objective_label
  mission_id
  mission_status
  session_id?
  chapter_id?
  question_id?
  question_ordinal?          # for why-now copy only
  assessment_id?
  assessment_item_index?
  assessment_answered_count?
  timer:
    kind?                    # countdown | elapsed | none
    remaining_seconds?
    elapsed_seconds?
  findings_id?
  updated_at
```

Missing optional fields → degrade honestly (still open correct session) — never fabricate question numbers.

---

## 7. Failure modes

| Failure | Student-facing behaviour |
|---|---|
| Session id missing but mission ready | Start Session (new) — state reason quietly if useful |
| Session id invalid | Honest: “Session unavailable” + Start Session or Support |
| Assessment progress corrupt | Restart assessment **with confirmation** on Assessment surface — not silent |
| Subject unpublished / revoked | Empty / blocked with Choose Exam or Support — not stale Continue |
| Clock skew on timer | Prefer server remaining time |

Never silent data loss. Never “start over” without Assessment/Session confirmation when progress existed.

---

## 8. Cross-day behaviour

Returning tomorrow:

1. Load last active subject.  
2. Resolve mission for that calendar/study day (or continuing incomplete mission — product rule must be deterministic).  
3. If yesterday’s session still open and incomplete → Continue Session (same continuity).  
4. Else show today’s ready mission.  
5. L2 may show yesterday’s completed items for orientation.

Students must not lose subject context because the date rolled.

---

## 9. What Home must not do

| Anti-pattern | Why |
|---|---|
| Force re-commitment POST to resume | Breaks one-click; CQ-003 resume principle |
| Show Continue without session_id | Lying Primary |
| Reset timers on Home paint | Continuity violation |
| Clear assessment answers on soft navigation | Continuity violation |
| Duplicate Session UI on Home “to help resume” | Wrong owner |

---

## 10. Acceptance tests

1. Mid-session → Home → Continue Session returns to same chapter and question.  
2. Mid-assessment → Home → Assessment Primary restores item index and timer.  
3. Findings ready → Home Primary Review Findings; after review, Primary advances.  
4. Next calendar day with open session → still Continue Session.  
5. No open work → no Continue Session Primary.  
6. Invalid session → honest recovery, not blank hero.

---

## 11. Implementation notes

- Prefer existing resume deep-links (`session.overview` + resume flags) over new parallel stacks.  
- Slim Home first paint: continuity fields needed for L0 only; do not wait on readiness/coach payloads.  
- Instrument (later): time-to-Primary and resume success rate — architecture target <3s recognition, one-click resume.
