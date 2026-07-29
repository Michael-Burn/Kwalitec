# Discovery Architecture

**Programme:** DX-005B  
**Status:** Binding for Choose Exam redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, DX-005A, Brand Guidelines  
**Implementation:** Architecture only (UI in later execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Choose Exam |
| **Shell** | Student |
| **Type (DX-002)** | Catalogue / commitment wizard — discover → confirm → begin |
| **Page title** | Choose Exam |
| **Nav label** | Choose Exam |
| **One question** | Which exam do I want to begin? |
| **One sentence (DX-003)** | Select a published curriculum. |
| **Design target** | Discovery First |
| **Primary action** | Begin Learning |

Legacy labels forbidden as the surface purpose: Study Plan Dashboard, Course Catalogue Marketing, Subject Hub, Pick a Module, Today’s Mission (on this page).

**Founder Subjects** (DX-004B) is a different surface. This architecture binds the **student** discovery surface only.

---

## 2. Product philosophy

Discovery is about **commitment**.

| It is | It is not |
|---|---|
| Where a learner begins a course of study | A second Home |
| A confidence-building selection | An analytics or readiness report |
| Ready-first, meaningful offerings only | A maximised choice wall |
| One Primary: Begin Learning | A multi-CTA launchpad |
| The handoff into Home continuation | Curriculum management |

Show only curricula that are meaningful to the student. Prefer Ready, recently updated, and Recommended (where applicable). Keep Coming Soon separate and visually secondary.

---

## 3. Decision → Action → Feedback

Per DX-003:

```
Decision:  Which exam do I want to begin?
    ↓
Action:    Begin Learning (after select + confirm)
    ↓
Feedback:  Mission created → redirect Home
```

| Beat | Choose Exam manifestation |
|---|---|
| **Decision** | L0 Ready list + L1 find/filter |
| **Action** | Select Ready curriculum → Confirm → **Begin Learning** |
| **Feedback** | Home loads with Current Mission ready (DX-005A) |

Search, filters, and sort change **what is visible**. They are not competing Primaries.

Confirm is part of the commitment path, not a second discovery question. Confirm may be a quiet confirmation step or panel — it must not introduce competing Primaries or promotional content.

---

## 4. Information hierarchy (L0–L3)

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **L0** | Ready curricula | Published offerings ready to begin; hosts Primary | Dominant |
| **L1** | Search & filters | Exam family, Status, Alphabetical | Tooling above list |
| **L2** | Supporting information | Brief description, estimated study scope, last updated | Quiet within rows / detail |
| **L3** | Navigation | Shell only; no duplicate local nav | Chrome |

```
┌─────────────────────────────────────────────────────────────┐
│ [Shell: Home · Choose Exam · History · …]          ← L3    │
├─────────────────────────────────────────────────────────────┤
│ Choose Exam                                                 │
│                                                             │
│ [ Search exams…             ]  Family ▾  Status ▾  Sort ▾ ←L1│
│                                                             │
│ Ready to begin                                    ← L0     │
│ ─────────────────────────────────────────────────────────   │
│ ○ CS1 Valuation                                             │
│   Brief description…                          Updated …     │
│   Estimated study scope: …                      ← L2       │
│                                                             │
│ ○ CS1 Financial                                             │
│   …                                                         │
│                                                             │
│                              [ Begin Learning ]   ← Primary │
│                                                             │
│ Coming soon                                       ← secondary│
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   CM2 …                         [ Notify when available ]   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. L0 — Published curricula Ready to begin

### Purpose

Answer the one question via recognition: which Ready exam should I commit to?

### Form

Dense **selectable list** (radio or equivalent single-select). Not KPI tiles. Not marketing cards. Not a Founder-style operator table.

B-025 (DX-002): prefer list recognition over heavy card chrome. Selection affordance must remain obvious; decoration must not.

### Density rules

| Rule | Value |
|---|---|
| One row = one curriculum / subject offering | Mandatory |
| Default ordering | Ready first; within Ready: Recommended (if any) → recently updated → alphabetical |
| Coming Soon | Separate secondary band below Ready — never interleaved as peers |
| First viewport | Ready offerings dominate; Coming Soon may peek or sit below fold |
| Scale | Tens without redesign; search becomes habit as list grows |

### Row answers (only)

1. **What is this?** — Subject / exam title  
2. **Can I begin?** — Ready (implicit by band; badge optional, quiet)  
3. **Is it worth selecting?** — Brief description + estimated study scope + last updated (L2)

### Forbidden on L0

- Readiness percentages / progress rings  
- Recommendation essays  
- Feature lists / marketing bullets  
- Multiple Primaries per row  
- “Continue today’s mission”  
- Operator pipeline language (Publish, Validation, Knowledge Graph)

---

## 6. Primary action — Begin Learning

| Rule | Value |
|---|---|
| **Label** | Begin Learning |
| **Count** | Exactly one filled Primary on the commitment path |
| **Enabled when** | Exactly one Ready curriculum is selected **and** confirm succeeds |
| **Disabled when** | No selection, Coming Soon selected (impossible by UI), or subject not enrolable |
| **Effect** | Create Mission / enrol → redirect **Home** |

No competing Primaries: no peer “Next”, “Explore features”, “Open Study Plan”, “Start Session” on this surface.

Wizard intermediate steps (exam date, availability), if retained at implementation, use **Continue** as a quiet step control — never as a second page Primary competing with Begin Learning. Prefer collapsing capture into confirm where Alpha allows (see `IMPLEMENTATION_PLAN.md`).

---

## 7. Ready rule

Only **Ready** curricula may expose **Begin Learning**.

| Availability | Student affordance |
|---|---|
| **Ready** (selectable + enrolable) | Select → Confirm → Begin Learning |
| **Coming Soon** | Notify when available (secondary) — never Begin Learning |
| **Ready badge but enrolment gated** | Visible, non-selectable; quiet reason — no false Begin |
| **Not supported / Unavailable** | Omitted from catalogue |

No false affordances. See `READY_STATE_SPEC.md` and `COMING_SOON_SPEC.md`.

---

## 8. Selection flow

```
Student
  ↓
Chooses curriculum (Ready)
  ↓
Confirms (quiet confirm — identity + essential plan facts only)
  ↓
Mission created (enrolment / study plan)
  ↓
Redirect Home
```

Home now owns continuation (DX-005A). Choose Exam does not show the new Mission as a second Home hero.

### Confirm content (allowed)

- Subject title  
- Essential scheduling facts the student set (exam date, availability) if those steps exist  
- One quiet line for applied defaults the student did not choose (or omit defaults entirely)

### Confirm content (forbidden)

- Position / learning style / target presented as if user-chosen without disclosure  
- Tutorial paragraphs  
- Feature promotion  
- Dual equal CTAs (“Yes, begin” / “No, make changes” as twin filled Primaries) — prefer one filled **Begin Learning** + text Secondary **Change selection**

---

## 9. Recommended (where applicable)

| Rule | Value |
|---|---|
| When | Product has a deterministic, explainable recommendation signal |
| Presentation | Quiet “Recommended” marker on at most one Ready row, **or** sort priority without essay |
| Forbidden | Recommendation paragraphs, multi-why stacks, coach essays on Choose Exam |

If no recommendation signal exists for Alpha, omit Recommended entirely — do not invent theatre.

---

## 10. Empty state

```
Reason
  ↓
Return later
```

Nothing else. See empty detail in `READY_STATE_SPEC.md` / wireframe.

Canonical Reason (DX-003 aligned): **No Ready subjects yet.**  
Next Action: **Return later** (or Return Home if entered from Home empty — same intent: wait, do not invent work).

---

## 11. Boundaries (DX-005A §4 refined)

Choose Exam **may**:

- Catalogue Ready / Coming Soon offerings  
- Capture essential commitment facts (exam date, availability) if required for Mission creation  
- Begin Learning into enrolment / plan  
- Offer Notify when available on Coming Soon  

Choose Exam **must not**:

- Show “today’s mission” as page purpose  
- Become daily resume surface  
- Host Session / Assessment UI  
- Duplicate Founder Subjects operator catalogue  
- Compete with Home after Begin Learning  

Cross-link contract:

| From | To | When |
|---|---|---|
| Home empty Primary | Choose Exam | No plan / no mission |
| Choose Exam complete | Home | Mission ready |
| Coming Soon notify | Stay / quiet ack | No false begin |

---

## 12. Nav label reconciliation

| Context | Canonical (DX-005B) |
|---|---|
| Shell nav | **Choose Exam** |
| Page title | **Choose Exam** |
| Legacy live label “Study Plan” / “Planning” | Retire as discovery nav label at implementation |
| Internal noun for the list | Subject Catalogue (DX-003) — quiet; not page H1 if redundant |

Active plan management (view/edit existing plan), if still required, is **not** this page’s L0. Prefer Settings / plan detail — do not resurrect a Study Plan dashboard as Choose Exam.

---

## 13. Relationship to Founder catalogue

| | Founder Subjects (DX-004B) | Student Choose Exam (DX-005B) |
|---|---|---|
| Audience | Operator | Learner |
| Question | Which subject do I work on? | Which exam do I begin? |
| Primary | Create Subject | Begin Learning |
| Status language | Pipeline stages + Published | Ready / Coming Soon |
| Open | Workspace | Confirm → Home |

Shared noun **Subject** must not blur surfaces. Never deep-link students into Console Subjects.

---

## 14. Acceptance tests (architecture)

1. Page answers only: Which exam do I want to begin?  
2. Exactly one filled Primary: Begin Learning (on commitment).  
3. Coming Soon cannot trigger Begin Learning.  
4. Ready + enrolment gate honest (no false Begin).  
5. After Begin Learning, user lands on Home with Mission — not back on Choose Exam as Home.  
6. Empty state is Reason → Return later only.  
7. No marketing, KPI, or recommendation essay blocks on L0.
