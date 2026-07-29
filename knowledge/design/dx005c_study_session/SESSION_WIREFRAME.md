# Session Wireframe

**Programme:** DX-005C  
**Status:** Binding layout authority (ASCII)  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** `SESSION_ARCHITECTURE.md`, DX-001 spacing/type  

---

## 1. Desktop — Answer Question (reference)

```
┌─ Student shell ─────────────────────────────────────────────────────────┐
│ Home   Choose Exam   History   Settings   Help          [Exit session]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CS1 · Probability                                                      │
│  Chapter 3 · Bayes' theorem                                             │
│  Objective: Apply Bayes to exam-style items                             │
│  Activity: Question 4 of 12 · Session step 3 of 5                       │
│                                                                         │
│  ┌─ Now ──────────────────────────────────────────────────────────────┐ │
│  │ Answer Question                                                    │ │
│  │ [ Submit answer ]                                                  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  A bag contains 3 red and 2 blue balls. …                               │
│                                                                         │
│  Your answer                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │                                                                  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ▶ Hint   ▶ Reference   ▶ Previous attempt   ▶ Why this question        │
│                                                                         │
│  ▶ Technical details                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Desktop — Immediate feedback (incorrect)

```
│  CS1 · Probability                                                      │
│  Chapter 3 · Bayes' theorem · Question 4 of 12                          │
│                                                                         │
│  ┌─ Now ──────────────────────────────────────────────────────────────┐ │
│  │ Continue                                                           │ │
│  │ [ Continue ]                                                       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Incorrect.                                                             │
│  Review Bayes' theorem before continuing.                               │
│                                                                         │
│  Your answer: 3/5                                                       │
│  Expected approach: condition on colour given prior …                   │
│                                                                         │
│  ▶ Show worked approach   ▶ Reference                                   │
```

No “Don’t worry!” / “You’re doing great!” / confetti.

---

## 3. Desktop — Read Section

```
│  CS1 · Probability                                                      │
│  Chapter 3 · Bayes' theorem                                             │
│  Objective: Apply Bayes to exam-style items                             │
│  Activity: Read section · Session step 1 of 5                           │
│                                                                         │
│  ┌─ Now ──────────────────────────────────────────────────────────────┐ │
│  │ Read Section                                                       │ │
│  │ [ Continue ]                                                       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ## Bayes' theorem                                                      │
│  (section body — only content needed now)                               │
│                                                                         │
│  ▶ Reference                                                            │
```

---

## 4. Desktop — Blocking issue

```
│  ┌─ Now ──────────────────────────────────────────────────────────────┐ │
│  │ Answer Question                                                    │ │
│  │ [ Submit answer ]           Blocking: Answer required              │ │
│  └────────────────────────────────────────────────────────────────────┘ │
```

Blocking is status, not a second Primary. Focus returns to the input.

---

## 5. Desktop — Complete Session → Reflection

```
│  CS1 · Probability                                                      │
│  Session practice complete                                              │
│                                                                         │
│  ┌─ Now ──────────────────────────────────────────────────────────────┐ │
│  │ Complete Session                                                   │ │
│  │ [ Complete Session ]                                               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
```

Then:

```
│  Reflection                                                             │
│  What mattered in this practice?                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │                                                                  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [ Save & return Home ]          Skip to Home                           │
```

Skip is quiet text. Primary is Save & return Home when reflection is offered; if product allows skip-as-primary when reflection is optional, still only one filled Primary (**Return Home**).

---

## 6. After return (not a Session celebration page)

```
Home
  L0 Current Mission → next ready step (or quiet complete)
  L2 Recent Progress
     · Probability · Session completed
```

Session does not retain a “Great job today” dashboard.

---

## 7. Mobile / narrow

```
┌──────────────────────┐
│ Shell (collapsed)    │
│ Exit                 │
├──────────────────────┤
│ CS1 · Probability    │
│ Ch 3 · Bayes         │
│ Obj: Apply Bayes …   │
│ Q4/12 · Step 3/5     │
├──────────────────────┤
│ Answer Question      │
│ [ Submit answer ]    │
├──────────────────────┤
│ Stem…                │
│ [ input ]            │
├──────────────────────┤
│ ▶ Hint ▶ Reference   │
│ ▶ Technical          │
└──────────────────────┘
```

Persistent context may compress to two lines; fields must remain present. Primary stays above the fold.

---

## 8. Focus order (keyboard)

1. Skip to content (if used)  
2. Persistent context (readable, not a trap)  
3. L0 Primary  
4. L1 interactive controls (inputs, choices)  
5. L2 disclosure triggers  
6. Exit / Return Home  
7. L3 disclosure  

After Submit → focus moves to feedback heading, then to next Primary (**Continue**).

---

## 9. Layout invariants

| Rule | Detail |
|---|---|
| One composition | First viewport = context + Primary + current L1 start |
| No cards in hero | Activity is not a KPI card cluster |
| Cards only if needed | Input grouping only when interaction requires a container |
| No decorative illustration | — |
| Shell quiet during practice | Prefer collapsed secondary nav; Exit always available |
| L2/L3 collapsed | Default closed |

---

## 10. Anti-wireframes (forbidden)

Do not implement layouts that show:

- Progress rings / mastery % beside the question  
- Streak / badge / XP strip  
- “Welcome back to your session” essay  
- Coach chat panel open by default  
- Sidebar of all chapters as peer Primaries  
- Dual filled CTAs (Submit + Skip Question as peers)  
- Pre-practice journal modal blocking L1  

ASCII in this file is the layout authority until a later Figma (if any) is explicitly adopted.
