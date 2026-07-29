# Mission Model

**Programme:** DX-005A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Companion:** `STUDENT_HOME_ARCHITECTURE.md`  
**Principle:** The Mission is operational, not motivational.

---

## 1. Definition

A **Mission** is the student’s current learning commitment — the unit Home displays so the learner can continue without reconstructing context.

| Mission is | Mission is not |
|---|---|
| What I am doing now | A badge or streak |
| Why this is next (operational) | A pep talk |
| What happens after completion | A celebration script |
| Continuity anchor across days | A dashboard widget |

---

## 2. Questions the Mission must answer

Exactly three — no more on L0:

| # | Question | L0 field |
|---|---|---|
| 1 | **What am I doing?** | Subject + current objective (lesson / focus) |
| 2 | **Why now?** | One operational reason line |
| 3 | **What happens after completion?** | One after-completion line (or deferred to Session if space-tight; must exist in Mission DTO) |

If any of the three cannot be answered from data, show an honest quiet state — never invent motivational filler.

---

## 3. Mission object (DTO)

```
Mission
├── subject_id / subject_name
├── objective_id / objective_label          ← current lesson / focus
├── mission_id (stable)
├── status                                 ← operational enum
├── why_now                                ← one line
├── after_completion                       ← one line
├── estimated_duration_label?              ← optional
├── primary_action                         ← label + href/post target
├── continuity                             ← see SESSION_CONTINUITY_SPEC
│   ├── session_id?
│   ├── chapter_id?
│   ├── question_id?
│   ├── assessment_progress?
│   └── timer_state?
└── queue_priority                         ← for L0 selection / L1
```

---

## 4. Status vocabulary (Home)

Align with DX-003 status system — Progress / Attention language only.

| Status | Student-facing label | Typical Primary |
|---|---|---|
| `ready` | Ready | Start Session |
| `in_progress` | In progress | Continue Session |
| `assessment_ready` | Assessment ready | Start Assessment |
| `findings_ready` | Findings ready | Review Findings |
| `revision_due` | Revision due | Resume Mission / Begin Revision |
| `complete_today` | Complete for today | (no Primary) |
| `blocked` | Waiting | Honest reason + secondary unblock |
| `unavailable` | Not ready yet | Quiet empty / Choose Exam if no plan |

Forbidden status chrome: “Crushing it”, “Almost there!”, flame streaks, XP.

---

## 5. Why-now rules

**Allowed (operational):**

- Syllabus sequence — next topic after last completed  
- Open session — continue where left off  
- Assessment gate — evaluation due for this objective  
- Spaced revision — due for retention of X  
- Findings — results waiting for review  

**Forbidden:**

- Motivational quotes  
- Social comparison  
- Vague “Sensei thinks you should…” without operational basis  
- Stacking why_recommended + why_it_matters + timeliness + benefit + coherence  

Maximum on Home L0: **one** why-now sentence (≤140 characters preferred).

Deep evidence stays in Session disclosure or Journey — not Home.

---

## 6. After-completion rules

One factual line:

| Pattern | Example |
|---|---|
| Sequence | “Next: Topic 3.2 — Lease liability measurement.” |
| Gate | “Then: short assessment on this objective.” |
| Day end | “Today’s mission ends after this session.” |
| Revision | “Returns you to today’s focus mission.” |

Never: “Great job unlock!” / badge promises / streak threats.

---

## 7. Primary action binding

Mission status → exactly one Primary (see Architecture §5). The Primary is a **property of the Mission**, not a separate Quick Action.

```
Mission.status  ──determines──►  primary_action.label
Mission.continuity ──routes──►  primary_action.target
```

If continuity exists (open session / mid-assessment), Primary **must** deep-link restore — never restart from chapter 1 without explicit user choice on Session surface.

---

## 8. Continuity fields (summary)

Home restores recognition of:

| Field | Purpose |
|---|---|
| Subject | Which exam track |
| Current lesson / objective | Where in syllabus |
| Mission status | Operational state |
| Current question (when appropriate) | Shown as support line or implied by Continue Session |
| Assessment progress | When Primary is Assessment / Findings |

Full persistence contract: `SESSION_CONTINUITY_SPEC.md`.

---

## 9. Multi-mission / multi-subject

| Case | Behaviour |
|---|---|
| One active subject | L0 = that subject’s current mission |
| Multiple subjects | L0 = most recently active incomplete mission; others may appear in L1 if attention-required |
| No active mission | Empty or Choose Exam Primary |

Home never shows two Primaries for two subjects.

---

## 10. Mission vs Session vs Assessment

| Object | Owner surface | Role |
|---|---|---|
| **Mission** | Home (display) + planning services (truth) | Continuation unit |
| **Session** | Study Session | Execution of mission practice |
| **Assessment** | Assessment | Evaluation gate |
| **Findings** | Assessment / Findings review | Post-evaluation feedback |

Home displays Mission; it does not re-implement Session UI.

---

## 11. Anti-patterns

| Anti-pattern | Why forbidden |
|---|---|
| Mission as hero marketing | Competes with Action |
| Mission Intelligence wall on Home | Decision density failure (DX-002/003) |
| Parallel “Guidance” panel restating Mission | Duplicate Decision |
| Timeline of today’s journey on Home | Process chrome; belongs in Session if anywhere |
| Commitment defer as peer CTA | Second decision before Feedback |

---

## 12. Acceptance tests (architecture)

1. A returning student can state subject + objective from L0 in **<3 seconds**.  
2. Why now is **one** sentence and operational.  
3. After completion is knowable without opening another panel.  
4. Primary label matches status table.  
5. No motivational or gamified mission chrome on Home.
