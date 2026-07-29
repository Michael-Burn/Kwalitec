# Practice Model

**Programme:** DX-005C  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Companions:** `SESSION_ARCHITECTURE.md`, `FEEDBACK_SPEC.md`, `REFLECTION_SPEC.md`  
**Authorities:** DX-003 Terminology; DX-005A Mission Model  

---

## 1. Purpose

The Practice Model defines what a Study Session **is** as a learning object: the units of work, the step cycle, and how Mission maps to practice without turning Session into Home.

---

## 2. Core objects

| Object | Definition | Owner surface |
|---|---|---|
| **Mission** | What to focus on today / next (subject + objective + status) | Home |
| **Session** | The practice vehicle for a Mission slice | Study Session |
| **Activity** | One discrete practice step (read, question, exercise, review) | Session L0 |
| **Attempt** | Student response to a practice item | Session / domain |
| **Finding** | Result that requires acknowledgment or correction path | Session mid-flow or Home Review Findings |
| **Reflection** | Post-practice notice (optional Sensei reflection) | Session end only |

**Mission vs Session (DX-003):** Mission = focus noun. Session = practice vehicle. CTAs use Session verbs.

---

## 3. What the Session owns

| Owns | Does not own |
|---|---|
| Learning (current content) | Choosing next day’s Mission |
| Practice (questions, exercises) | Discovery of exams |
| Immediate feedback | Longitudinal progress dashboards |
| In-session reflection (after Complete) | Archive browsing (History) |
| Restore of practice coordinates | Re-commitment / Choose Exam |

---

## 4. Activity types

| Activity type | Student work | Primary (example) | L1 content |
|---|---|---|---|
| **Read Section** | Consume syllabus section / notes | **Continue** | Section body |
| **Worked Example** | Follow explained solution | **Continue** | Example + steps |
| **Answer Question** | Submit response | **Submit answer** | Stem + input |
| **Complete Exercise** | Multi-part or open exercise | **Complete Exercise** | Exercise body + inputs |
| **Review Finding** | Acknowledge / act on result | **Review Finding** | Finding + required action |
| **Complete Session** | End practice block | **Complete Session** | Brief done state (no celebration) |

Only one activity is **current**. Queue of remaining steps may appear as quiet progress in persistent context (`3/5`), never as a competing destination list.

---

## 5. Practice cycle

```
┌──────────────┐
│   Activity   │
└──────┬───────┘
       │ Primary
       ▼
┌──────────────┐
│   Feedback   │  ← immediate, specific, educational
└──────┬───────┘
       │ Continue (or Retry if product allows)
       ▼
┌──────────────┐
│  Next Activity│  (or Complete Session)
└──────────────┘
```

Rules:

1. Feedback is part of the same Session — not a separate product page with new nav.  
2. Retry is secondary or replaces Primary only when the step requires another attempt; still exactly one Primary.  
3. Reflection does **not** appear in this loop — only after **Complete Session**.

---

## 6. Mapping from Mission

```
Home Mission
  subject + objective + continuity pointer
        │
        ▼
Session opens
  persistent context ← Mission fields
  first/current activity ← continuity or Mission plan
        │
        ▼
Practice cycle until Complete Session
        │
        ▼
Reflection (Session)
        │
        ▼
Home (continuation owns “what next”)
```

Session must not invent a second Mission picker. If the Mission is invalid (revoked subject), Session shows honest block + Return Home / Support — not Choose Exam embedded.

---

## 7. Progress semantics

| Shown | Meaning | Location |
|---|---|---|
| Activity ordinal (e.g. Question 4 of 12) | Position in current activity set | Persistent context |
| Session steps (e.g. 3/5) | Position in today’s session plan | Persistent context |
| Correct / Incorrect | Immediate educational outcome | Feedback on L1 |

| Not shown in Session | Why |
|---|---|
| Mastery % / readiness rings | KPI theatre; Home/elsewhere if ever |
| Streaks / XP / badges | Forbidden |
| Weekly study minutes | History / analytics — not practice |
| Peer percentiles | Forbidden |

Session progress is **orientation**, not a dashboard.

---

## 8. Assessment boundary

| Case | Behaviour |
|---|---|
| Mission Primary is Start/Continue Assessment | Home → Assessment surface (not Session chrome) |
| Session practice item is formative only | Stays in Session |
| Formal evaluation mid-Mission | Hand off to Assessment; Session does not host evaluation UI |

DX-005C does not redesign Assessment. Session must not absorb Assessment questions as a peer “mode” that reintroduces dashboard chrome.

---

## 9. Explainability placement

| Depth | Placement |
|---|---|
| Operational “what now” | L0 activity label + Primary |
| Why this item / why this feedback | L2 — hidden until requested |
| Full coach / MES walls | Forbidden on Session entry |

Deep explainability supports learning when the student asks. It must not delay the Primary.

---

## 10. Acceptance tests

1. Given an open question activity, only one filled Primary exists.  
2. Submitting an answer shows educational feedback before the next activity.  
3. Hint / Reference are collapsed until requested.  
4. Completing the last practice step yields **Complete Session**, then Reflection, then Home.  
5. No streak, badge, or readiness ring appears on Session.
