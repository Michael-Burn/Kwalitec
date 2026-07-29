# Session Continuity Spec

**Programme:** DX-005C  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Companions:** DX-005A `SESSION_CONTINUITY_SPEC.md` (Home resume contract); `PERSISTENT_CONTEXT_SPEC.md`  
**Principle:** Leaving restores practice state. No recovery workflow.

---

## 1. Goal

Leaving the Session and returning (same day or next day via Home **Continue Session**) must restore context so the student never asks:

> Where was I?

And never performs a manual recovery ritual.

DX-005A defines Home’s resume Primary. DX-005C defines what Session must **persist and apply** on load.

---

## 2. Must restore

| Dimension | Restore to |
|---|---|
| **Current chapter** | Last active chapter / section |
| **Current question** | Last unanswered / in-progress item |
| **Scroll position** | Last scroll offset within L1 (best effort; chapter anchor minimum) |
| **Input** | Draft response text / selected choices not yet submitted |
| **Timer** | Remaining / elapsed — do not reset silently |
| **Assessment state** | Only if Session hosts formative state; formal Assessment owns its own surface — restore pointer so handoff is correct |

Also restore (identity):

| Dimension | Restore to |
|---|---|
| **Subject** | Same enrolled curriculum |
| **Objective** | Mission objective |
| **Activity** | Current activity type + ordinal |
| **Session progress** | Step index / total |
| **Feedback state** | If feedback was showing and Continue not taken — restore feedback view |

---

## 3. Must not require

- Re-selecting subject  
- Re-running Choose Exam  
- Re-committing the Mission solely to resume  
- Manually finding session id  
- Restarting from chapter 1 after accidental leave  
- Completing a “Recover session” wizard  
- Re-entering reflection to unlock practice  

---

## 4. Leave paths

| Leave event | Persist | On return |
|---|---|---|
| Browser close mid-session | Full restore set | Home → Continue Session → restored Session |
| Exit / navigate Home mid-session | Full restore set | Same |
| Navigate History / Settings | Full restore set | Same |
| Soft navigation within Session | Update coordinates continuously | N/A |
| **Complete Session** | Close practice pointer; mark complete | Reflection then Home — no Continue Session for closed id |
| Mid-assessment (Assessment surface) | Assessment progress (Assessment owner) | Home Assessment Primary |
| Explicit abandon (if allowed) | Mark abandoned; clear open pointer | Home next ready Mission — never zombie Continue |

---

## 5. Persistence responsibilities

| Layer | Responsibility |
|---|---|
| **Domain / services** | Canonical session position, draft answers, timers, completion |
| **Session UI** | Apply restore on load; debounce draft saves; report scroll/input |
| **Client storage** | Optional UX cache (scroll) — **not** source of truth for answers/timers |
| **Home view-model** | Read continuity pointer only (DX-005A) |

If Home render fails, Session deep-link must still restore.

---

## 6. Continuity DTO (Session-facing)

```
session_continuity:
  session_id
  subject_id
  subject_code?
  subject_name
  objective_id
  objective_label
  chapter_id
  chapter_label
  activity_type
  activity_label
  question_id?
  question_ordinal?
  activity_total?
  session_step_index
  session_step_total
  draft_input?
  draft_input_updated_at?
  scroll:
    anchor_id?
    offset_px?
  timer:
    kind?                    # countdown | elapsed | none
    remaining_seconds?
    elapsed_seconds?
  ui_phase:                  # practice | feedback | complete | reflection
  feedback_payload?          # when ui_phase = feedback
  updated_at
```

Missing optional fields → degrade honestly (open correct chapter/question) — never fabricate content.

---

## 7. Resume performance

| Target | Detail |
|---|---|
| **Instant resume** | First paint: persistent context + L0 Primary + skeleton/cached L1 |
| **Time-to-primary-action** | <3 seconds from Home Continue click to usable Primary |
| **Draft restore** | Available when L1 interactive; do not block Primary paint on L2 explainability |

Do not await coach / readiness / History before showing Primary.

---

## 8. Failure modes

| Failure | Student-facing behaviour |
|---|---|
| Session id invalid | Honest: Session unavailable + Return Home / Start Session |
| Draft corrupt | Open item blank; quiet notice — do not invent answers |
| Timer skew | Prefer server remaining time |
| Subject unpublished | Blocked + Return Home / Support — not stale practice |
| Scroll restore fails | Land at activity anchor (chapter/question start) |

Never silent data loss. Never “start over” without confirmation when progress existed.

---

## 9. Cross-day behaviour

Returning tomorrow with open incomplete session:

1. Home Primary = **Continue Session** (DX-005A).  
2. Session applies full restore set.  
3. Do not force yesterday’s reflection if practice incomplete.  
4. Do not reset timer silently because the date rolled.

---

## 10. What Session must not do

| Anti-pattern | Why |
|---|---|
| Show a recovery wizard | Violates “no recovery workflow” |
| Clear drafts on soft navigation | Continuity violation |
| Reset timers on paint | Continuity violation |
| Require reflection before resume | Reflection after practice only |
| Duplicate Home Mission picker “to help resume” | Wrong owner |

---

## 11. Acceptance tests

1. Mid-question with draft → Home → Continue Session restores chapter, question, draft, scroll (or anchor).  
2. Mid-timer → leave → return restores remaining time (server-authoritative).  
3. Feedback showing → leave → return shows feedback + Continue Primary.  
4. Complete Session → no Continue Session for that id; Home advances.  
5. Invalid session → honest recovery, not blank chrome.  
6. Resume path meets <3s to Primary under normal local/dev conditions (instrument later in prod).

---

## 12. Relationship to DX-005A

| Concern | Authority |
|---|---|
| When Home shows Continue Session | DX-005A |
| What gets restored inside Session | **DX-005C (this doc)** |
| Conflict | Session restore coordinates win for practice state; Home must not invent question numbers |
