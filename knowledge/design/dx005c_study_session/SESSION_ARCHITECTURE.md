# Session Architecture

**Programme:** DX-005C  
**Status:** Binding for Study Session redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, DX-005A, DX-005B  
**Implementation:** Architecture only (UI in later execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Study Session |
| **Shell** | Student (minimal chrome during practice) |
| **Type (DX-002)** | Workspace — guided practice loop on one Mission |
| **Page title** | Subject name + current activity (not “Session” as hero) |
| **Nav entry** | Opened from Home Primary (Continue Session / Start Session) — not a primary-nav destination |
| **One question** | What should I do right now? |
| **One sentence (DX-003)** | Complete the current practice step. |
| **Design target** | Practice First |

**Forbidden labels as page identity:** Dashboard, Hub, Learning Centre, Progress Centre, Mission Control, Coach Home.

Session is reached from Home. It is not a second Home and not a discovery surface.

---

## 2. Product philosophy

The Study Session exists for one purpose:

**Build mastery.**

| It is | It is not |
|---|---|
| Where the student practices | A progress report |
| Learning + practice + immediate feedback | A platform tutorial |
| One decision → one Primary → feedback | An encouragement engine |
| Continuity of one Mission’s practice | A navigation hub |
| Reflection **after** practice | Pre-practice journaling theatre |

```
Nothing on this page exists unless it helps answer:
“What should I do right now?”
```

Explicit non-purposes:

- Not report progress  
- Not explain the platform  
- Not encourage  
- Not motivate  

Only support learning.

---

## 3. Decision → Action → Feedback

Per DX-003, every practice step follows:

```
Decision:  What should I do right now?
    ↓
Action:    Exactly one Primary (activity-specific)
    ↓
Feedback:  Immediate, specific, educational — then next step or Complete Session
```

| Beat | Session manifestation |
|---|---|
| **Decision** | Persistent context + current activity label + (if any) blocking issue |
| **Action** | One Primary control in L0 |
| **Feedback** | Inline result on L1; advance within session URL family |

No loops. No dead ends. No emotional padding. No unnecessary confirmations (Complete Session may keep a single confirm only if irreversible discard of in-progress work — prefer soft complete).

Secondary controls (Hint, Reference, Explain, Exit) must never look equal-weight to the Primary.

---

## 4. Information hierarchy (L0–L3)

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **Persistent** | Learning context | Identity + position — always visible | Stable header |
| **L0** | Practice decision | Current activity · Primary · Blocking issue | Dominant |
| **L1** | Practice content | Exactly what is needed for the current step | Primary work area |
| **L2** | Supporting material | Hints, reference, previous attempt, explainability | Hidden until requested |
| **L3** | Technical metadata | Time, IDs, diagnostics | Collapsed by default |

```
┌─────────────────────────────────────────────────────────────┐
│ [Student shell — quiet; Exit → Home]                        │
├─────────────────────────────────────────────────────────────┤
│ PERSISTENT CONTEXT                                          │
│   CS1 · Probability                                         │
│   Chapter 3 · Bayes' theorem                                │
│   Objective: Apply Bayes to exam-style items                │
│   Activity: Question 4 of 12 · Session 3/5 steps            │
├─────────────────────────────────────────────────────────────┤
│ L0  Answer Question                                         │
│     [ Submit answer ]  ← exactly one Primary                │
│     (blocking: none | e.g. Answer required)                 │
├─────────────────────────────────────────────────────────────┤
│ L1  Question stem + response area                           │
├─────────────────────────────────────────────────────────────┤
│ L2  ▶ Hint  ▶ Reference  ▶ Previous attempt  ▶ Why this     │
├─────────────────────────────────────────────────────────────┤
│ L3  ▶ Technical details                                     │
└─────────────────────────────────────────────────────────────┘
```

Shell navigation is escape, not page content. Do not duplicate Home / Choose Exam / History as in-page destination cards during practice.

---

## 5. Practice-based architecture (not page-based)

Replace competing destinations with **modes of one session**.

```
Read → Practice → Feedback → (next step) → Complete → Reflect → Home
```

| Mode | Owns | Primary family |
|---|---|---|
| **Read** | Section / worked example | Continue / Mark read |
| **Practice** | Question / exercise | Answer / Submit / Complete Exercise |
| **Feedback** | Immediate result | Continue / Retry / Review Finding |
| **Complete** | End of session practice | Complete Session |
| **Reflect** | Post-practice reflection | Save & return Home / Skip to Home |

Never present Progress, Coach, Journey, History, and Practice as competing top-level destinations that feel like separate products inside the Session.

---

## 6. Primary action law

Exactly one Primary at all times. The label changes with context; the page still contains only one Primary.

| Context | Primary label (examples) |
|---|---|
| Mid-read section | **Continue** |
| Open question, answer incomplete | **Answer Question** (or **Submit answer**) |
| Open exercise | **Complete Exercise** |
| Feedback shown, more steps remain | **Continue** |
| Finding to acknowledge mid-session | **Review Finding** |
| All practice steps done | **Complete Session** |
| Reflection form | **Save & return Home** (or **Return Home** if skip allowed) |

Blocking issue (if any) sits beside or above the Primary — never as a second filled CTA.

Quiet secondary: Exit / Return Home (text link), Hint / Reference (L2 disclosure).

---

## 7. Ownership boundaries

| Session may | Session must not |
|---|---|
| Execute chapter / question / exercise flow | Become a second Home for “what next today” |
| Show current objective for the active session | Host Choose Exam catalogue |
| Host L2 explainability for the current step | Host KPI dashboards / streaks / badges |
| Host reflection **after** practice | Force reflection before practice |
| Offer Return Home | Embed Assessment as a peer dashboard |
| Hand off to Assessment when Mission requires | Replace Assessment surface |

After Complete Session → Reflection → **Return Home**. Home owns continuation.

---

## 8. Entry and exit

### Entry

| Source | Behaviour |
|---|---|
| Home **Continue Session** | Restore chapter, question, scroll, input, timer, assessment-related session state |
| Home **Start Session** / **Resume Mission** | Open at Mission’s first ready step |
| Deep link (notification) | Same restore contract as Continue |

Time-to-primary-action target: **<3 seconds**. Resume: **instant** (cached shell + restore coordinates).

### Exit

| Event | Result |
|---|---|
| Mid-session Exit / navigate Home | Persist state; Home Primary = Continue Session |
| **Complete Session** | Close practice; open Reflection |
| Reflection done / skipped | Return Home; Home shows next Mission or quiet complete |
| Browser close | Persist; no recovery workflow on return |

No manual recovery wizard. Continuity is automatic — see `SESSION_CONTINUITY_SPEC.md`.

---

## 9. Forbidden on Session

| Forbidden | Why |
|---|---|
| Large navigation / destination grids | Distracts from practice |
| Progress dashboards / study statistics | Home/History own reporting; Session owns doing |
| Gamification, badges, streaks, leaderboards | Violates Practice First + DX-001 |
| Marketing, announcements, welcome panels | Not learning |
| Tutorial essays / platform explainers | Not learning |
| Decorative illustrations | Cognitive noise |
| Emotional encouragement (“You’re doing great!”) | Feedback Spec forbids |
| Pre-practice reflection | Reflection Spec: after only |
| Multiple Primaries | Decision Clarity |
| Peer Coach / Insights walls | L2 disclosure only when requested for current step |

---

## 10. Accessibility

| Requirement | Detail |
|---|---|
| **Keyboard-first** | Primary reachable without pointer; Tab order: context → L0 Primary → L1 inputs → L2 disclosures → Exit |
| **Focus management** | After submit/feedback, move focus to feedback then to next Primary |
| **Responsive** | Same L0–L3; persistent context stacks; Primary remains early |
| **No regressions** | WCAG targets already claimed for student surfaces must hold |

---

## 11. Performance

| Metric | Target |
|---|---|
| Resume session | Instant (first paint shows context + Primary; content may follow) |
| Time-to-primary-action | <3 seconds from Continue Session click |
| L2 / L3 | Lazy — not on critical path |

Do not block Primary on coach, readiness aggregates, or History payloads.

---

## 12. Success test

Cover L1 content. From persistent context + L0 alone, the student must answer:

1. Which subject?  
2. Which chapter / objective?  
3. What activity am I in?  
4. What is the one thing I do next?
