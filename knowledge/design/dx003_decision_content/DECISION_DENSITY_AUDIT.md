# Decision Density Audit

**Programme:** DX-003  
**Release Candidate:** `RC-2026.07.29-01`  
**Definition:** An **independent decision** is a choice the user must resolve that is not a trivial confirmation of the same Action.

**Target:** **One** independent decision per screen.  
**Maximum:** **Three.**  
Anything higher requires redesign (split, sequence, or disclose).

---

## Scoring method

Count distinct questions of the form “Should I A or B?” that compete in the same viewport before Feedback.

Do **not** count: typing into a field that is part of one Decision; paging; opening a disclosure that is not required.

---

## Audit table

| ID | Screen | Decisions now | What they are | Target | Verdict |
|---|---|---|---|---|---|
| A1 | Login | 1 | Sign in? | 1 | Pass (after cutting marketing) |
| B1 | Onboarding | 2–3 | Continue? Skip? Help? | 1 | Fail |
| B2 | Help | 3–5 | Learn ontology? Search? Contact? Which topic family? | 1–2 | Fail |
| C1 | Choose Exam | 1 | Which subject? | 1 | Pass |
| C2 | Exam date | 1 | Which date? | 1 | Pass |
| C3 | Availability | 1 | How much time? | 1 | Pass |
| C4 | Begin Learning | 2–4 | Confirm plan? Edit defaults? Start? | 1 | Fail |
| C8 | Calibration | 1–2 | Coverage level? Continue? | 1 | Borderline |
| D1 | Student Home | 4–7 | Start? Why dive? Defer? Tutor? Complete? Readiness? | 1 | **Fail** |
| D2 | Journey | 1–2 | Scan vs return Home | 1 | Pass if quiet |
| D3 | Revision | 1–2 | Begin this revision? (Mission primacy copy is not a decision) | 1 | Pass |
| D4 | History | 3–4 | Browse? Learn epistemology? Journal? Timeline? | 1 | Fail |
| D5 | Decision Journal | 1–2 | Reflect? | 1 | Pass |
| D6 | Timeline | 1 | Leave? | 1 | Pass |
| D7 | Profile | 2–4 | Which card/section to edit? | 1–2 | Fail mild |
| E1 | Session overview | 1 | Begin? | 1 | Pass |
| E2 | Session activity | 1 | Answer / advance | 1 | Pass |
| E3 | Reflection | 1 | What to record? | 1 | Pass |
| E4–E5 | Summary / Complete | 1 | Return Home? | 1 | Pass |
| G1 | Console Overview | 4–6 | Which KPI meaning? Which Quick Action? Which attention? Shortcuts? | 1 | **Fail** |
| G3 | Attention | 1 | Which item? | 1 | Pass |
| G4 | Support | 1 | Which submission? | 1 | Pass |
| G8 | Students | 1 | Which participant? | 1 | Pass |
| H1 | Studio list | 1–2 | Which workspace? (plus hub essay distraction) | 1 | Borderline |
| H2 | Subjects hub | 2–3 | Create? Open? Jump Studio? | 1 | Fail |
| H3–H6 | Peer hubs | 2–3 | Same + filter identity | 0 (fold) | Fail — delete pages |
| H7 | Curriculum Workspace | 6–9 | Upload? Advance? Validate? Preview? Approve? Publish? Tab? Diagnose? | 1 | **Fail** |
| I* | Secondary reports | 1–3 | Inspect which metric? | 1 | Pass if demoted |
| J2 | Welcome modal | 1 | Dismiss? | 0 | **Delete** |
| J4 | Support gate | 1 | Choose other subject? | 1 | Pass |

---

## Failures requiring redesign (priority)

| Priority | Screen | Now → Target | Redesign move |
|---|---|---|---|
| P0 | Curriculum Workspace | 6–9 → 1 | Stage-gated single Primary; disclose rest |
| P0 | Console Overview | 4–6 → 1 | Decision list; remove KPI/Quick Action decisions |
| P0 | Student Home | 4–7 → 1 | One Primary; overflow secondary |
| P0 | Studio hubs H2–H6 | 2–3 → 1 / 0 | One catalogue; delete peer hubs |
| P1 | History | 3–4 → 1 | Archive only; merge Progress |
| P1 | Help | 3–5 → 1–2 | Search/contact; cut ontology |
| P1 | Begin Learning | 2–4 → 1 | Hide unchosen defaults |
| P1 | Onboarding | 2–3 → 1 | One Continue; quiet Skip |

---

## Decision density vs cognitive load

| Density | Typical cognitive load (DX-002) |
|---|---|
| 1 | Low–Moderate |
| 2–3 | Moderate (max allowed) |
| 4+ | High / Very High — mandatory redesign |

---

## Rule for DX-004+

Before visual polish, every Founder screen in scope must score **≤3** independent decisions, with **1** as the design target. Document any intentional 2–3 (e.g. Create vs Open on an empty Subjects catalogue) in the screen’s Decision Architecture row.
