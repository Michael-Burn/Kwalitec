# EA-003 — Mission Authoring Guide

**Programme:** Educational Excellence Programme EA-003  
**Status:** Binding — how to author a premium Daily Mission  
**Effective:** 2026-08-01  
**Parent:** `EA003_MISSION_BLUEPRINT.md` · `EA003_MISSION_SCHEMA.md`  
**Related:** `EA002_TUTOR_VOICE_GUIDE.md` · `EA002_EDUCATIONAL_STYLE_GUIDE.md` · AF-MS · `EA001_MISSION_PHILOSOPHY.md`  
**Nature:** Authoring process law — not content generation for any live subject  

---

## 1. Purpose

Teach educational authors to conceive and write Missions that students recognise as one Study Sensei — independently of who holds the pen.

**Do not** rewrite CS1 in this programme. **Do not** generate live Missions here. Use this guide when a successor content programme begins.

---

## 2. Authoring stance (Head Tutor)

Before writing a single student-facing line, answer privately:

1. What is the **one** skill or conceptual move of the day?  
2. What did yesterday make possible — and what does tomorrow need?  
3. Where exactly does the candidate open the CMP, and where do they stop?  
4. What will I ask them to demonstrate closed-book when they return?  
5. What misconception am I hunting?  
6. What is my **Tutor Intent** — the coaching move only I (as Sensei) am making today?

If you cannot answer (6), stop. You do not yet have a Mission.

---

## 3. Mission lifecycle (author view)

```text
INPUTS
  → AUTHORING (blueprint pack)
    → EDUCATIONAL REVIEW
      → TUTOR REVIEW
        → CERTIFICATION (Gate MG + Rubric)
          → PUBLICATION
            → MAINTENANCE
              → RETIREMENT
```

Authors own **Inputs** and **Authoring**. They participate in review but do not self-certify commercial packs alone (EA-002).

Full stage definitions: `EA003_MISSION_CERTIFICATION.md`.

---

## 4. Inputs (required before drafting)

Gather these before filling schema fields:

| Input | Source | Why |
|-------|--------|-----|
| Official topic code + title | Syllabus / curriculum package | Lawful identity |
| CMP edition + TOC locus | Authorised CMP | Reading scope |
| Prior topic / Mission or cold-start context | History / plan / Twin | Continuity |
| Mode | Learning / Revision | Honest labelling |
| Exam sitting / weight cues | Twin / syllabus | Why-now / exam focus |
| Linked Session intent plan | Session designers | Study strategy must be real |
| Prior Reflection residuals | Soft evidence | Bridge + misconceptions |
| EA-001/002/003 standards | This programme family | Compliance |

**Block authoring** if topic identity is contaminant, placeholder, or unresolved.

---

## 5. Authoring sequence (recommended order)

Write in this order to prevent syllabus-paste Missions:

### Step 1 — Tutor Intent (internal first)

Draft `tutor_intent` as a private coach note.  
Test: Would another tutor recognise a *specific* coaching move?

### Step 2 — Concept Focus + Learning Objective

Name the day’s centre, then one actionable objective that is **not** the syllabus heading.

### Step 3 — Continuity Bundle

Write `prior_bridge` and `tomorrow_bridge` before the hero title. Continuity first prevents disconnected days.

### Step 4 — CMP Reading Scope

Pin open point, stop condition, and out-of-scope. If you cannot point into CMP, you are inventing a second textbook — stop.

### Step 5 — Success Criteria + Reflection Goal

Define assessable “done when…” and what residual the Reflection must harvest.

### Step 6 — Misconceptions + Study Strategy

List 1–3 misconceptions; design strategy that forces them into the open (recall, justify, compare).

### Step 7 — Load, time, revision signals

Honest cognitive load and minutes; name revision signals.

### Step 8 — Student-facing prose

Only now write `display_title`, `mission_purpose`, `why_now`, `explainability`, `expected_benefit` in Tutor Voice.

### Step 9 — Dependencies + self-checks

Link Session/Episode IDs (or mark draft-linked); deny P1–P12; cite EP IDs.

### Step 10 — Fit test

Read the brief aloud as an IFoA tutor’s night-before note. If it fails, rewrite — do not polish placeholders.

---

## 6. Field-by-field authoring notes

### Mission Purpose

One sentence. Name the day’s educational job. Avoid product verbs (“optimise readiness”).

### Educational Intent

State the cognitive move: connect X to Y; distinguish A from B; apply method M; justify choice C.

### Tutor Intent (mandatory)

Template:

> Today I will **[coaching move]** so that the candidate **[demonstrable outcome]**, because **[educational reason tied to this topic]**.

Reject interchangeable intents.

### Learning Objective

Prefer: Explain / Justify / Calculate / Identify / Derive / Compare.  
Reject: Understand / Engage with / Cover / Study [heading].

### CMP Reading Scope

Always three parts: open · stop · not today.  
Never paste CMP paragraphs into the Mission body.

### Syllabus Coverage

Topic code + title + honest coverage claim + mode.  
First-pass ≠ mastery.

### Prerequisite Knowledge

Bullet skills/topics. Cold start: “Assumes enrolment goal / chapter opener only.”

### Concept Focus

A named chain or concept, not a chapter title.

### Common Misconceptions

Each row: misconception → corrective move. Use in Reflection Goal and Episode design later.

### Study Strategy

Must match real stages. Name active demands (note / recall / solve / justify).

### Reflection Goal

Specific: “Name whether link choice or exponential-family form still feels shaky — and why.”

### Success Criteria

Closed-book preferred. Countable. No readiness ±% as sole criterion.

### Tomorrow Bridge

Skill bridge to next lawful topic — or honest “next focus not yet assigned.”

### Estimated Cognitive Load / Study Time

Align with scope. Heavy + 20 minutes is usually a lie.

### Revision Signals

Examples: failed success check; misconception confirmed; Reflection residual; high exam weight.

### Dependencies

Never orphan. Session and Episodes are co-requisites for publish.

---

## 7. Voice and style (mandatory)

| Follow | Document |
|--------|----------|
| Tutor Voice | `EA002_TUTOR_VOICE_GUIDE.md` |
| Educational Style | `EA002_EDUCATIONAL_STYLE_GUIDE.md` |
| North-star sentence | “Today we do this, because of that, so you can demonstrate this skill — then we continue here.” |

### On the hero surface — never

- Platform essays (“Mission ≠ mastery”, runtime names, milestone IDs)  
- “Highest-value next step” as sole why-now  
- Identical rationale reused across Missions  
- Motivational-poster emptiness  

---

## 8. Worked pattern (illustrative — not live CS1 content)

**Unfit (EV-001 pattern):**

> Title/Objective/Narrative: Study 4.2 — Understand and use generalised linear models  
> Why: highest-value next step toward exam readiness  
> Focus: Today’s topic  
> Tutor Intent: *(missing)*

**Fit (EA-003 pattern):**

| Field | Illustrative content |
|-------|----------------------|
| Tutor Intent | Force the candidate to narrate exponential family → linear predictor → link before deep reading, so CMP pages organise around a map. |
| Concept Focus | Exponential family → linear predictor → link |
| Learning Objective | Explain how a GLM uses a linear predictor and link function for a non-normal response. |
| Prior Bridge | Yesterday you finished classical linear models. Today the same linear machinery expands to non-Normal responses. |
| Why now | Next incomplete syllabus unit after 4.1; exam questions frequently require choosing and justifying a link. |
| CMP Scope | Open CMP §4.2 GLM setup; stop after first worked example; defer full exercise set. |
| Success | Closed-book: name one response distribution and its canonical link; point to where it sits in the CMP example. |
| Reflection Goal | Say whether “which link?” or “which exponential-family form?” remains the sticky point. |
| Tomorrow Bridge | Bayesian foundations (5.1) — likelihood thinking carries forward. |
| Load / Time | Moderate · 45–60 minutes |

---

## 9. Anti-patterns (author must self-reject)

| Pattern | Action |
|---------|--------|
| Generic brief reusable on any topic | Rewrite Tutor Intent and Concept Focus |
| Template stamp with topic-code swap | Rebuild Continuity + why-now + explainability |
| CMP paraphrase as Mission narrative | Delete paste; keep locus only |
| Syllabus restatement | Rewrite objective and title |
| Disconnected day (no yesterday/tomorrow) | Complete Continuity Bundle |
| Educationally purposeless | Write Educational Intent + Success Criteria |
| Missing Tutor Intent | Block — do not submit to review |
| Beautiful brief, empty Session | Do not request publication; joint rule |

Full reject classes and measurable gates: `EA003_MISSION_CERTIFICATION.md`.

---

## 10. Collaboration with Session authors

Missions and Sessions are **one educational day**:

1. Mission Concept Focus = Session Overview focus.  
2. Mission CMP scope = Guided Reading locus.  
3. Mission Success Criteria ⊇ Session “done when” story.  
4. Mission Tomorrow Bridge = Summary / Home Tomorrow Preview.  
5. Mission Reflection Goal = Reflection prompt family.

If Session design changes stages, Mission `study_strategy` and dependencies must be updated and re-reviewed.

---

## 11. Draft → review handoff

Before submitting for Educational Review, the author provides:

1. Complete schema pack (`status=in_review`)  
2. Self-check denials (P1–P12, TB classes)  
3. Linked Session/Episode draft IDs  
4. Rubric self-score (optional but encouraged)  
5. Confirmation: no CS1/live content was fabricated outside the authorised content programme scope  

Reviewers use `EA003_MISSION_CERTIFICATION.md` and `EA003_MISSION_SCORING_RUBRIC.md`.

---

## 12. Generation and tooling (future)

Whether human-written or composition-assisted:

1. Output must satisfy Blueprint + Schema + Gate MG.  
2. Generative polish may not invent syllabus order, mastery, or rankings.  
3. Failed field resolution → block — never placeholders.  
4. Automation may pre-fail; automation alone may not PASS Tutor Review in Version 1.

EA-003 does not implement tooling.

---

## 13. Closing rule

> Write the Tutor Intent first. If the coaching move is clear, the student brief writes itself. If the coaching move is missing, you are labelling a syllabus node.

Same Sensei, many authors — process and fields, not personality.
