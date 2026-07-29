# Student Home Architecture

**Programme:** DX-005A  
**Status:** Binding for Student Home redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, DX-004 operating-system principles  
**Implementation:** Architecture only (UI in later DX-005 execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Student Home |
| **Shell** | Student |
| **Type (DX-002)** | Home — daily decision surface |
| **Page title** | Home |
| **Nav label** | Home |
| **One question** | What should I study next? |
| **One sentence (DX-003)** | Continue today’s study. |
| **Design target** | Mastery First |

Legacy labels forbidden on this surface: Dashboard, Insights Home, Learning Hub, Study Centre, Sensei Home.

---

## 2. Product philosophy

Student Home exists to **continue learning**.

| It is | It is not |
|---|---|
| Where the student resumes study | An analytics page |
| Operational mission continuity | A celebration wall |
| One decision → one action | A multi-CTA launchpad |
| Calm and purposeful | Gamified or childish |
| Encouraging through clarity | Motivational theatre |

The student arrives here to **study next**. Discovery belongs in Choose Exam. Execution belongs in Study Session. Evaluation belongs in Assessment. Reflection belongs in History.

---

## 3. Decision → Action → Feedback

Per DX-003:

```
Decision:  What should I study next?
    ↓
Action:    Exactly one Primary (Continue Session / Resume Mission / Start Assessment / Review Findings / …)
    ↓
Feedback:  Session (or Assessment / Findings) loads; progress persists; return to Home restores Mission
```

| Beat | Student Home manifestation |
|---|---|
| **Decision** | L0 Current Mission (subject + objective + operational why-now) |
| **Action** | One Primary button in L0 |
| **Feedback** | Navigation to Session / Assessment / Findings, or quiet day-complete / empty state |

No second independent decision may appear before Feedback. Queue rows (L1) and recent items (L2) are **context after** Primary is found — they do not introduce competing Primaries.

---

## 4. Information hierarchy (L0–L3)

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **L0** | Current Mission | Single most important learning item + one Primary | Dominant |
| **L1** | Learning Queue | Items requiring attention only (no history) | Secondary list |
| **L2** | Recent Progress | Quiet orientation; max 5 | Supporting / muted |
| **L3** | Navigation | Shell nav only; no in-page Quick Actions | Chrome (not page content) |

```
┌─────────────────────────────────────────────────────────────┐
│ [Shell: Home · Choose Exam · History · Settings · Help] ← L3│
├─────────────────────────────────────────────────────────────┤
│ Home                                              ← title   │
│                                                             │
│ CURRENT MISSION                                   ← L0      │
│   Subject · Objective                                       │
│   Why now (one line, operational)                           │
│   [ Primary ]                                               │
│                                                             │
│ LEARNING QUEUE                                    ← L1      │
│   row · row · row                                           │
│                                                             │
│ RECENT PROGRESS                                   ← L2      │
│   quiet · compact · ≤5                                      │
└─────────────────────────────────────────────────────────────┘
```

Everything must fit in the **first viewport** so “what next” needs no scroll (DX-001 hierarchy; DX-005A performance: mission recognition immediate).

---

## 5. L0 — Current Mission

### Purpose

Answer the one question immediately.

### Content (only)

| Element | Type | Notes |
|---|---|---|
| Section label | Section title 18px | “Current Mission” |
| Subject name | Body 16px semibold | Decision object — which exam/subject |
| Current objective | Body 16px / support | Lesson / objective the student is on |
| Mission status | Supporting 14px | Operational only (In progress / Ready / Assessment ready) |
| Why now | Supporting 14px | **One** operational line — not MES stack |
| Optional after-completion | Supporting 14px | One line: what happens after (Mission Model) |
| Duration (optional) | Supporting 14px | Estimate only when it aids Action |
| **Primary button** | One | Label from state table below |

### Forbidden in L0

Greeting, welcome, narrator name block, multi-why stack, trust/coherence badges, confidence metres, alternatives list, tutor CTA, defer form as peer Primary, progress rings, streak, congratulations.

### Primary label rules

| Learning state | Primary label |
|---|---|
| Open study session mid-flight | **Continue Session** |
| Mission committed / ready, no open session | **Resume Mission** or **Start Session** |
| Assessment unlocked / due | **Start Assessment** |
| Findings / review ready after assessment | **Review Findings** |
| Syllabus-complete revision ack required | **Continue** (ack → then next mission) |
| Day complete; no further attention | No Primary CTA — quiet complete state + optional L1 |
| No subject / no plan | Empty state Primary: **Choose Exam** |

Never more than one Primary. Never a Primary cluster. “Not today” / defer / tutor / Journey links are **not** Primaries — if retained at all, they are tertiary disclosure or shell destinations (prefer omit from Home).

### Selection algorithm (deterministic)

1. Incomplete open session for the active subject → Continue Session.  
2. Else mission requiring acknowledgement (revision ack / findings review) → that Primary.  
3. Else current scheduled / recommended mission ready to start → Start / Resume Mission.  
4. Else highest-priority Learning Queue item (see L1).  
5. Else quiet day-complete or empty state.

Full Mission object: `MISSION_MODEL.md`. Continuity restore: `SESSION_CONTINUITY_SPEC.md`.

---

## 6. L1 — Learning Queue

### Purpose

Show only learning items that **require attention** — not inventory, not motivation, not syllabus map.

### Allowed row kinds

| Status | Meaning |
|---|---|
| Resume Session | Open session waiting |
| Assessment Ready | Evaluation due |
| Revision Due | Supporting revision required for today’s focus |
| Findings Ready | Review results waiting |
| Mission Ready | Next mission queued (only if not already L0) |

### Forbidden in L1

Completed history, “nice to know” tips, readiness %, streak counts, Journey story, Tutor teasers, feature promotion, informational-only rows.

### Ordering

1. Resume Session  
2. Assessment Ready / Findings Ready  
3. Revision Due  
4. Mission Ready  

Max visible rows: **5**. Overflow: omit or “View in History / Journey” via shell — never a second Home.

### Row interaction

Row open = secondary path (same destination family as Primary would take for that item). Must not visually outrank L0 Primary (DX-001 weight rules).

---

## 7. L2 — Recent Progress

### Purpose

Quiet orientation — “what did I just do?” — not motivation.

### Rules

| Rule | Value |
|---|---|
| Max entries | **5** |
| Tone | Compact, muted, factual |
| Content | Subject · activity type · relative time |
| Empty | **Omit section entirely** |
| Forbidden | Charts, % rings, badges, congratulations, weekly stats |

L2 is never a Primary. Opening a row may deep-link to History detail — quiet.

---

## 8. L3 — Shell navigation

Home does not duplicate navigation.

Allowed shell destinations (target Student OS; ≤6 primary):

| Nav item | Owns |
|---|---|
| Home | Continuation |
| Choose Exam | Discovery |
| History | Reflection / archive |
| Settings | Account |
| Help | Unblock |

Journey / Revision / Session are **not** competing Homes. Journey and Revision may remain reachable as secondary destinations (Settings disclosure or contextual links from Session) — never as Quick Actions theatre on Home. See `NAVIGATION_BOUNDARIES.md`.

---

## 9. Empty and quiet states

Per DX-003 empty-state standards:

| State | Reason | Next Action |
|---|---|---|
| No study plan / no subject | No exam selected yet | **Choose Exam** (Primary) |
| Plan exists; mission not ready | Guidance not ready yet — expected quiet | Secondary: open Choose Exam only if plan change needed; else wait / return tomorrow copy (one line) |
| Day complete | Today’s mission finished | No Primary; optional L2; one line: return tomorrow |
| Continuity restore failure | Session state unavailable | Honest error + **Start Session** or Support — never silent loss |

No “Your first insights will appear here” marketing. No insight promises.

---

## 10. Performance goals

| Goal | Target |
|---|---|
| Time-to-primary-action | **<3 seconds** (recognition + click path) |
| Mission recognition | Immediate (L0 first paint, above fold) |
| Resume session | **One click** from Primary |

Implementation must not block Primary behind secondary panel fetches.

---

## 11. Accessibility

| Requirement | Rule |
|---|---|
| Keyboard | Tab order: title → L0 Primary → L1 rows → L2 rows → shell |
| Focus | Visible focus rings per DX-001 |
| Contrast | Body/support on surface meets WCAG AA |
| Responsive | Single column; Primary remains first actionable on mobile |
| Semantics | One `h1` (Home); L0/L1/L2 as sections with headings |

No regressions vs current keyboard reachability of Start/Continue.

---

## 12. Relationship to explainability & recommendations

DX-005A does **not** delete Runtime A / MES / recommendation engines.

It **relocates density**:

| Concern | Lives at |
|---|---|
| One operational why-now | L0 Mission (one line) |
| Deep why / evidence / alternatives | Session overview disclosure or Help — not Home L0 stack |
| Readiness % / drivers | Journey or Profile progress — not Home cards |
| Coach / Guidance panel | Remove from Home; Sensei may appear once in Session if product policy requires |

Home remains explainable by **Mission clarity**, not by multi-panel epistemology.

---

## 13. Non-goals

- Redesigning Choose Exam, Session, Assessment, History layouts  
- Implementing templates/CSS in this programme  
- Changing curriculum V1/V2 traversal  
- Adding gamification “to motivate”  

---

## 14. Authority conflict resolution

On Student Home conflicts:

1. **DX-005A** wins for Home structure (L0–L3), Mission primacy, continuity ownership.  
2. **DX-001** wins for tokens, type, spacing, premium gate.  
3. **DX-003** wins for copy density, empty/success/error tone, Decision → Action → Feedback.  
4. **DX-002** wins for surface type and student nav tree intent.  
5. Product explainability standards remain binding for Session/Insights surfaces — not as Home L0 chrome.
