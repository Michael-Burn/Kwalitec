# RP-001.2 — Student Decision Points

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.2  
**Date:** 2026-07-28  
**Purpose:** Catalogue every meaningful choice a student makes on the Alpha journey, what Sensei expects, and whether the choice is explainable and recoverable.  
**Companion:** `END_TO_END_JOURNEY_CERTIFICATION.md`, `JOURNEY_TRANSITION_MATRIX.md`

---

## How to read this register

| Field | Meaning |
|-------|---------|
| **DP-ID** | Decision point id |
| **Stage** | Journey stage |
| **Student choice** | What the learner decides |
| **Sensei intent** | Educational purpose of offering the choice |
| **Consequence** | What changes in product / learning state |
| **Reversible?** | Can the student undo or recover? |
| **Explainable?** | Can they answer why this choice is offered now? |
| **Risk** | Confusion / trust / educational risk if mishandled |
| **Alpha note** | Default production posture |

---

## Decision points — default Alpha path

### Authentication

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-01 | Login | Submit credentials / Remember me | Establish identity | Session starts; routed by plan/onboarding | Logout | Yes | Low (invalid flash) | Pass |
| DP-02 | Login | Follow `next` after login | Resume interrupted deep link | Safe local next or canonical home | N/A | Partial | Open redirect blocked | Pass |

### Product onboarding

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-03 | Onboarding | Complete steps | Orient to Sensei product thesis | Marks onboarding done; continues routing | No (one-time) | Yes | Low | Dual chrome |
| DP-04 | Onboarding | Skip | Allow progress without orientation | Same as complete for gate | No | Partial | Under-orientation | Conditional |
| DP-05 | Onboarding | Open Help | Support escape hatch | Leaves to Help | Yes (back) | Yes | Dual chrome | Pass |

### Study plan wizard

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-06 | Wizard 1–2 | Exam / paper | Bind official syllabus | Curriculum selection | Back within wizard | Yes | Unsupported exam flash | Pass |
| DP-07 | Wizard 3 | Exam date | Deadline-driven planning | Plan horizon | Back | Yes | Unrealistic date | Pass |
| DP-08 | Wizard 4 | Current position | Fair start topic | Planning offset | Back | Yes | Misdeclaration | Pass |
| DP-09 | Wizard 5 | Availability | Workload realism | Session sizing inputs | Back | Yes | Over/under commit | Pass |
| DP-10 | Wizard 6 | Learning style | Preference (not black-box AI) | Plan preference fields | Back | Partial (weak “why”) | Overclaim if read as AI | Pass |
| DP-11 | Wizard 7 | Target | Ambition vs pace | Target fields | Back | Yes | Overambition | Pass |
| DP-12 | Review | Confirm plan | Commit planning inputs | Creates plan → Calibration | Create new plan later via Study Plan | Yes | Dual chrome | Pass |
| DP-13 | Review | Abandon / leave | Avoid forced plan | No plan; login will re-route to wizard | Yes | Yes | Stuck without plan | Pass |

### Calibration

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-14 | Calibration | Declare known topics | Twin birth / fair recommendations | Twin + declared sync | Resume/re-calibrate paths limited | Yes | Under/over declare | Pass |
| DP-15 | Calibration | Beginner skip | Honest cold start | Welcome Home; weaker Twin | Partial | Yes | Tutor soft-fail later | Conditional |
| DP-16 | Calibration | Abandon | Exit without Twin | Home without Twin | Partial | Partial | Silent quality loss | Conditional |

### Home / mission / commitment

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-17 | Welcome modal | Dismiss | Clear first-arrival chrome | Modal suppressed | No | Yes | CTA ≠ session start | Conditional |
| DP-18 | Welcome modal | “Start Today's Session” | Drive into daily work | Lands Home under sole runtime | N/A | Partial | Extra click | Conditional |
| DP-19 | Home | Start today’s mission | Commit to Sensei recommendation | Commitment + session overview | Defer instead; session resume | Yes (when MES/MI present) | Empty CTA disabled | Core |
| DP-20 | Home | Defer (“Not today”) + reason | Capture preference; do not punish | Deferred chrome; **ranking unchanged** | Same day stay deferred | Yes if disclosed | Expectation mismatch | Disclose R-18 |
| DP-21 | Home | Open defer details | Inspect reasons | UI expand only | Yes | Yes | — | Pass |
| DP-22 | Home | Ack post-session reflection | Close commitment arc | Reflection dismissed | No for that arc | Yes when shown | Often **not shown** after V2 finish | **Gap** |
| DP-23 | Home | Navigate Journey / Revision / History / Plan / Help | Self-directed exploration | Leaves Today centre | Yes | Partial on empty Revision | Thin Revision | Conditional |
| DP-24 | Home | Tutor explain mission (if offered) | Extra Sensei explanation | Flash explanation / soft-fail | N/A | Partial without Twin | Soft-fail trust | Conditional |

### Session

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-25 | Overview | Begin session | Enter learning activity | Activity surface | Resume if leave | Yes | — | Pass |
| DP-26 | Activity | Answer / advance | Practice / progress | Item progress | Limited | Yes | — | Pass |
| DP-27 | Reflection (session) | Continue | Educational pause then wrap | Summary | No | Yes | Confused with ILE-005 | Conditional |
| DP-28 | Complete | Finish session | Seal session | Home + flash | No | Yes | Commitment not marked completed | **Gap** |

### Quick Check (OFF by default)

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-29 | Session (if ON) | Start Quick Check | Short adaptive probe | QC phase flow | Pause/resume within QC | Yes with framing | Scope honesty if claimed OFF | **Excluded** |
| DP-30 | QC completion (if framing ON) | Accept/defer framed tip | Telemetry / preference | Framing telemetry | N/A | Yes | Not ranking authority unless designed | Excluded |

### Archive and feedback

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-31 | Decision Journal | Reflect on entry | Educational feedback loop (ILE-005) | Reflection saved; Sensei review internal | No | Yes (flash clarifies not scoring) | Multi-reflection confusion | Pass |
| DP-32 | Journal / Timeline | Browse / navigate | Continuity of decisions | Read-only exploration | Yes | Yes | Sparse early empty | Pass |
| DP-33 | History | Open past session card / archives | Evidence continuity | Navigation | Yes | Yes | Expect charts | Conditional |
| DP-34 | Help / Alpha feedback | Submit mission helpful / clarity / problem / suggest | Operational learning | Feedback stored; flash | N/A | Yes | No student closed loop | Low |
| DP-35 | Research check-in | Participate / skip when eligible | Product research (RIP-001) | Research record | Skip | Partial vs ILE-005 | Confused with educational reflection | Brief |
| DP-36 | Profile / Settings | Edit prefs / data export paths | Account control | Profile/settings state | Partial | Partial (notifications copy) | Implies push | Conditional |

### Lifecycle (gap)

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-37 | Syllabus complete | Acknowledge revision mode | Mark conscious shift to revision | `revision_acknowledged` | One-way | Would be Yes | **UI unreachable under sole runtime** | **Fail** |

### Non-decisions (presentation-only — risk)

| DP-ID | Stage | Student choice | Sensei intent | Consequence | Reversible? | Explainable? | Risk | Alpha note |
|-------|-------|----------------|---------------|-------------|-------------|--------------|------|------------|
| DP-38 | Home guided reflection preview | “Done reflecting” / “Skip for today” spans | UJ preview chrome | **Nothing saved** | N/A | Copy says optional/not saved | Looks like real controls | **Fail affordance** |

---

## Decision continuity review

| Continuity question | Answer |
|---------------------|--------|
| Does every major action leave a Sensei-visible trail? | Start/defer/present generally yes via Journal when wired; V2 session finish may omit commitment completion trail. |
| Are deferrals educationally honest? | Yes if students are told ranking does not change. |
| Are reflections distinguishable? | Session vs Journal vs Research vs preview — **not** clearly mapped for students. |
| Can a student recover from a bad choice? | Wizard backs; session resume; defer is soft; skip onboarding is permanent; abandon calibration weakens Twin. |
| Is there a forced choice with no good option? | Empty Home with disabled CTA — wait / browse — highest “stuck” feeling. |

---

## Highest-stakes decisions (Alpha briefing)

1. **DP-19 Start mission** — primary educational commitment of the day.  
2. **DP-12 Confirm study plan** — binds syllabus and deadline.  
3. **DP-14 Calibration declarations** — shapes Twin fairness.  
4. **DP-20 Defer** — preference only; must not be oversold.  
5. **DP-31 Journal reflect** — educational calibration evidence.  
6. **DP-37 Revision ack** — currently missing on EOS.  
7. **DP-38 Fake controls** — must not be treated as real decisions.

---

## Counts

| Category | Count |
|----------|------:|
| Decision points catalogued | 38 |
| Core daily-path decisions | ~10 (DP-01, 03, 12, 14, 19, 20, 25–28) |
| Flag-gated / excluded | DP-29, DP-30 |
| Known broken / false affordances | DP-22 (often missing), DP-37, DP-38 |

---

## Document control

Documentation only. No decision UX was changed in RP-001.2.
