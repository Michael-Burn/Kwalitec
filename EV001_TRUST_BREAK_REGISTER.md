# EV-001 — Trust Break Register

**Programme:** Educational Validation Programme EV-001  
**Environment:** Production — https://kwalitec.onrender.com  
**Student:** ctshumba01@gmail.com  
**Live commit observed:** `613722cffa16e6badbdb3a1161e4feaa35fd02db`  
**Subject under study:** CS1 (CS1) · Chapter 4 · Topic 4.2  
**Audit date:** 2026-08-01  
**Method:** Live student-experience walkthrough only (no production changes; no source-led redesign)

---

## Purpose

Record every moment where a diligent student following only Kwalitec might think:

- “This mission is too generic.”
- “This doesn’t follow naturally from yesterday.”
- “I don’t understand why I’m studying this now.”
- “This feels copied from the CMP.”
- “I should probably go back to the textbook instead.”

Each entry is observational. Remedies are suggestions only — **not implemented**.

---

## Register

### TB-001 — Session content collapses to “Today’s topic”

| Field | Evidence |
|-------|----------|
| **Day / mission** | Current mission: *Study 4.2 — Understand and use generalised linear models* (`msn_105914561dfc4acc9a0c85e6a98269ef`); Session `lsr-18e4b384b9cc` overview + activity |
| **What caused the loss of trust** | Home names GLM correctly, but Session Overview and Learning Activity replace the topic with the literal placeholder string **“Today’s topic”** in title, objective, concept focus, reading prompt, checkpoint, and reflection copy. |
| **Educational impact** | The student cannot tell *what* to study inside the session. An IFoA candidate preparing GLMs is given no exponential-family, link-function, or deviance guidance — only a shell. Trust that Kwalitec can teach collapses immediately. |
| **Suggested remedy** | Bind session templates to the real topic title and learning objectives from the published curriculum node; refuse to open a session if topic resolution fails (show an honest error instead of placeholders). |

---

### TB-002 — Mission reads as syllabus paste, not a tutor brief

| Field | Evidence |
|-------|----------|
| **Day / mission** | Home → Today’s Mission (4.2) |
| **What caused the loss of trust** | Mission title, objective, and narrative are the same syllabus heading: *Study 4.2 — Understand and use generalised linear models*. Supporting line explains platform semantics (“Mission completion is study progress only, not mastery”) rather than *why GLM today after linear regression*. |
| **Educational impact** | Feels administrative, not tutorial. Student may conclude Kwalitec is a checklist over the syllabus PDF. |
| **Suggested remedy** | Write mission narrative as a short tutor brief: yesterday’s bridge from 4.1, today’s GLM purpose, success criterion, and tomorrow’s Bayesian handoff — without platform jargon. |

---

### TB-003 — Postal address appears as a syllabus topic

| Field | Evidence |
|-------|----------|
| **Day / mission** | Syllabus (`/student/journey`) Remaining Topics; Curriculum Map pathway + hierarchy |
| **What caused the loss of trust** | A future/remaining topic is titled **`1 Jln Kilang Timor #06-01 · Singapore 159303`** — a physical address, not an IFoA learning outcome. It sits in the student pathway as a Future topic and under Remaining Topics. |
| **Educational impact** | Catastrophic credibility failure. The student reasonably concludes curriculum ingestion copied CMP/publisher metadata. Primary-study trust ends here; textbook/CMP becomes safer. |
| **Suggested remedy** | Quarantine non-syllabus nodes from publication; add a curriculum linter rejecting address/contact/boilerplate strings; republish CS1 without the node. |

---

### TB-004 — “Why this guidance?” is the same sentence every time

| Field | Evidence |
|-------|----------|
| **Day / mission** | Decision Journal — entries for 1.1 (×2) and 4.2 (31 Jul 2026) |
| **What caused the loss of trust** | Every recommendation uses interchangeable copy: “highest-value next step…”, “steady progress toward exam readiness”, “Emerging confidence”, “Some uncertainty remains”. Nine repetitions of “highest-value next step” across three entries. |
| **Educational impact** | Explainability feels fake. The student cannot distinguish intentional sequencing from a template stamp. |
| **Suggested remedy** | Require decision-journal rationales to cite specific prior topic, prerequisite, and exam-skill gap in plain tutor language; block publish of generic boilerplate strings. |

---

### TB-005 — Progress claims mastery theatre without practice memory

| Field | Evidence |
|-------|----------|
| **Day / mission** | Home Progress 80% / Syllabus 12 topics complete vs History “0 completed sessions” / Learning Journey empty / Revision “Nothing to revise yet” |
| **What caused the loss of trust** | The product congratulates first-pass coverage and “High confidence” while admitting there is no sitting history and nothing to revise. Decision Journal also claims “Mission completed” for 4.2 while Home still assigns 4.2 as today’s mission. |
| **Educational impact** | Student cannot trust the scoreboard. Either prior work was invisible/erased, or completion is decoupled from actual study — both destroy long-term reliance. |
| **Suggested remedy** | One progress truth: topic completion must require completed sittings (or an explicit Founder-marked waiver). Align Decision Journal outcomes with Home/History. |

---

### TB-006 — Learning objectives marked Not started under Completed topics

| Field | Evidence |
|-------|----------|
| **Day / mission** | Curriculum Map hierarchy for completed topics 1.1–4.1 |
| **What caused the loss of trust** | Topics show **Completed** while every nested learning objective shows **Not started**. Chapters containing completed topics still show **Future**. |
| **Educational impact** | Hierarchy contradicts itself. A tutor would never say “you finished linear regression” and “you have not started any of its objectives” in the same breath. |
| **Suggested remedy** | Derive topic status from LO/evidence rollup; never mark a parent complete while all children are untouched unless an explicit override is disclosed. |

---

### TB-007 — Session asks student to “read the material” but supplies none

| Field | Evidence |
|-------|----------|
| **Day / mission** | Session activity `act-read-1` — Reading · Activity 1 of 3 |
| **What caused the loss of trust** | Prompt: “Read the material for Today’s topic.” No reading passage, worked numbers, GLM definitions, or CMP-referenced exposition appears — only a reflection textarea. |
| **Educational impact** | Forces the student back to the textbook/CMP mid-session. Kwalitec stops being a primary study system. |
| **Suggested remedy** | Each Reading activity must include authored or licensed study prose (or a precise CMP page/section citation with paraphrase teaching). Empty reading stages must not ship. |

---

### TB-008 — Answer recorded, but session does not educationally advance

| Field | Evidence |
|-------|----------|
| **Day / mission** | Session `lsr-18e4b384b9cc` after multiple `/activity/answer` posts |
| **What caused the loss of trust** | Flash: “Answer recorded. Review the feedback, then continue.” No feedback body and no Continue control appear; activity remains Reading 1 of 3 indefinitely. |
| **Educational impact** | Study flow feels broken. Even a tolerant student cannot complete the mission arc (worked example → practice → reflection). |
| **Suggested remedy** | After answer, show tutor feedback and a single Continue CTA that advances activity index; add an integration test for the 3-activity path. |

---

### TB-009 — Timing story disagrees with itself

| Field | Evidence |
|-------|----------|
| **Day / mission** | Home mission chip **1 h** vs Session overview **About 30 minutes** / activity timer **About 24 minutes remaining** |
| **What caused the loss of trust** | Allocated time for the same mission changes depending on surface. |
| **Educational impact** | Planning trust erodes; student cannot schedule the day. Depth expectations become arbitrary. |
| **Suggested remedy** | Single mission duration authority shared by Home, Session, and plan pacing. |

---

### TB-010 — Tomorrow preview jumps over a nonsense node, then to Bayesian

| Field | Evidence |
|-------|----------|
| **Day / mission** | Syllabus Up Next: 5.1 Bayesian; Remaining Topics list shows the Singapore address; Map also lists address as Future |
| **What caused the loss of trust** | Continuity messaging says completing 4.2 unlocks 5.1, while Remaining Topics surfaces a non-topic address. Map pathway inserts the address among real CS1 topics. |
| **Educational impact** | “Yesterday → today → tomorrow” narrative cannot be trusted. Student anticipates a surreal next mission. |
| **Suggested remedy** | Remove the address node; make Up Next / Remaining / Map share one ordered incomplete queue. |

---

### TB-011 — Learning-objective order inside topics looks machine-shuffled

| Field | Evidence |
|-------|----------|
| **Day / mission** | Curriculum Map hierarchy for 4.2 and 5.1 |
| **What caused the loss of trust** | Under 4.2, LO **4.2.4** appears before **4.2.1–4.2.3**. Under 5.1, **5.1.6** appears before **5.1.1**. |
| **Educational impact** | Feels like CMP/database export order, not tutor sequencing. Undermines curriculum fidelity claims. |
| **Suggested remedy** | Enforce syllabus numeric order at publish time; display LOs in official sequence only. |

---

### TB-012 — Mid-journey “High confidence” with empty practice record

| Field | Evidence |
|-------|----------|
| **Day / mission** | Syllabus Learning Insights at Topic 13/15 |
| **What caused the loss of trust** | Insight label **High confidence** while History shows no sessions and Learning Journey says the story has not begun. |
| **Educational impact** | Affective guidance feels unearned — the opposite of a calm, evidence-based tutor. |
| **Suggested remedy** | Gate confidence language on sitting evidence; otherwise say “Not enough practice yet to judge confidence.” |

---

### TB-013 — Platform explains itself instead of teaching

| Field | Evidence |
|-------|----------|
| **Day / mission** | Home mission aftermath line; Session “Why today’s topic”; Decision Journal uncertainty boilerplate |
| **What caused the loss of trust** | Copy teaches Kwalitec concepts (mission ≠ mastery, readiness ±3%, provisional guidance) more than GLM. |
| **Educational impact** | Breaks the principle of guide-don’t-lecture-about-the-platform. Student comes for actuarial teaching and receives product meta-commentary. |
| **Suggested remedy** | Move product semantics to Help; keep mission/session voice on the mathematics and exam skill. |

---

### TB-014 — Revision surface is unavailable when a primary system needs it most

| Field | Evidence |
|-------|----------|
| **Day / mission** | `/student/revision` at 80% first-pass coverage |
| **What caused the loss of trust** | “Nothing to revise yet — Finish today’s Session first.” After twelve allegedly completed topics, spaced revision still has no programme. |
| **Educational impact** | Long-term retention strategy is absent precisely when earlier CS1 chapters should be recycling. Exam readiness trust falls. |
| **Suggested remedy** | Seed revision from completed topics even before today’s sitting closes; schedule weak-topic revisits from Baseline/Twin evidence. |

---

## Summary counts

| Severity | Count | IDs |
|----------|------:|-----|
| Catastrophic (would abandon Kwalitec) | 4 | TB-001, TB-003, TB-007, TB-008 |
| Severe (would dual-track with textbook) | 6 | TB-002, TB-004, TB-005, TB-006, TB-010, TB-014 |
| Material (erodes quiet confidence) | 4 | TB-009, TB-011, TB-012, TB-013 |

**Register status:** Open — sufficient alone to withhold primary-study reliance for CS1 on this live build.
