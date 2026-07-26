# Learning Explainability

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS001 — Learning Progression Model  
**Classification:** Explainability contract for learning progression judgements  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **learning progression** to students in clear educational language.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `EDUCATIONAL_LOGIC_REGISTRY.md` (especially EL-008, EL-010)
4. `LEARNING_PROGRESSION_MODEL.md`
5. `LEARNING_OBJECTIVES.md`
6. `LEARNING_EVIDENCE_MODEL.md`
7. `LEARNING_PROGRESSION_STATES.md`
8. `../learning_interventions/INTERVENTION_EXPLAINABILITY.md` (and compatibility pointer `LEARNING_INTERVENTIONS.md`)
9. `../EDUCATIONAL_EVIDENCE_MODEL.md`
10. `../student_profile/PROFILE_EXPLAINABILITY.md`

> **Students should understand why Kwalitec believes learning is progressing,  
> what evidence supports that belief,  
> and what the next educational priority is.  
> Explainability never invents educational certainty.**

---

## 1. Purpose

Students should never have to guess whether Kwalitec thinks they are genuinely learning — or why.

Learning Coach explainability exists so every material progression judgement answers — in plain educational language — what is known, what is estimated, which evidence trail supports the belief, and what to do next.

Without Learning Coach explainability:

- coverage looks like mastery;
- stalls feel like unexplained judgement;
- interventions feel arbitrary;
- exam-readiness speech becomes theatre.

With Learning Coach explainability:

- the student trusts the long-horizon tutor posture;
- claim types stay honest;
- thin history stays dignified and clear;
- next educational priority is actionable.

---

## 2. Traceability Obligation (Architectural)

Every material Learning Coach progression judgement must be traceable through:

| Trace link | Student-facing role |
|------------|---------------------|
| **Syllabus scope** | “For [topic / area]…” |
| **Learning objective(s)** | “We’re judging [understanding / retrieval / application / …]…” |
| **Accumulated educational evidence** | “Because across recent study / practice / return…” |
| **Progression posture** | “So your learning looks like…” |
| **Student Educational Profile alignment** | “That fits where you are overall…” / “We need to revisit your overall diagnosis because…” |
| **Next educational priority / intervention** | “So the next priority is…” |

Internal IDs (LPS-XX, LO-XX, LI-XX, EV-XX, EL-XXX) may exist for algorithms and audits. They must not appear as student-facing jargon.

A progression claim with no evidence trail (or no explicit insufficient-warrant statement) is invalid — even if the explanation sounds motivating.

**Architectural requirement restated:**

> The Learning Coach must never infer mastery from completion alone.  
> Every judgement about progression must be traceable to accumulated educational evidence.

---

## 3. Explainability Principles

1. **Three answers every time.** Why we believe progression is (or is not) happening; what evidence supports that; what the next educational priority is.
2. **Facts and estimates stay distinct.** Coverage and completion are facts of activity/coverage; understanding and readiness are estimates when claimed.
3. **Name the objective.** Say *what kind* of learning is progressing (LO vocabulary in plain words).
4. **Prefer one primary reason.** Avoid multi-factor dumps; add secondary detail only if needed for honesty.
5. **Conflict is spoken.** Do not hide disagreeing sessions.
6. **Silence beats stretch.** “Too early to judge understanding” is better educational speech than invented trajectories.
7. **Interventions are labelled as guidance.** Recommendations are not Mission obligations unless Daily Coach / plan authority makes them so.
8. **No score theatre.** No progression percentages, streak-as-mastery, or opaque “learning scores” in Learning Coach narration.
9. **Dignity in stall and decay.** Supportive, specific, non-shaming language.
10. **EIP-003 hierarchy.** Advice / estimate / fact claim types remain visible.

---

## 4. Four-Question Framework (Learning Coach Specialisation)

Aligned to EIP-003’s four-question explainability framework:

| Question | Learning Coach obligation |
|----------|---------------------------|
| **What do we know?** | Coverage completed; sessions undertaken; practice outcomes recorded — as facts of observation |
| **What do we estimate?** | Understanding, retrieval, application, retention, exam-readiness progression — labelled as estimates / provisional judgements |
| **Why this judgement?** | Plain link from accumulated evidence pattern → LPS posture |
| **What next?** | Primary educational priority (often an LI intervention in plain language) |

---

## 5. Required Narrative Elements

Every material student-facing progression explanation should include:

1. **Scope** — which syllabus area the judgement concerns.
2. **Belief** — whether learning is progressing, stalling, inconsistent, decaying, or too early to judge — in plain words.
3. **Evidence support** — at least one concrete educational trail reference (practice across sessions, return after a gap, coverage without practice, etc.).
4. **Claim type honesty** — estimate vs fact wording.
5. **Next priority** — one clear educational next step.

Optional when useful:

- comparison to earlier posture (“stronger than last month on application…”);
- explicit non-claims (“this is not mastery yet…”);
- Profile consistency note when overall diagnosis colours the story.

---

## 6. Language Rules

### 6.1 Preferred vocabulary

| Prefer | Avoid |
|--------|-------|
| “Evidence across recent practice suggests…” | “The algorithm scored you…” |
| “You’ve covered this part of the syllabus” | “You’ve mastered this” (from coverage) |
| “You can retrieve this more reliably” | “You know this cold” (without warrant) |
| “Practice shows you can apply…” | “Mission complete means you’re ready” |
| “This held up when you returned” | “Permanent mastery unlocked” |
| “Too early to judge understanding” | Invented confidence from thin history |
| “Sessions are happening, but growth isn’t showing yet” | “You’re failing” / shame language |
| “Next priority: rebuild foundations / retrieval / …” | Opaque “optimise your trajectory” |

### 6.2 Forbidden speech patterns

- Inferring mastery, durable knowledge, or exam readiness from completion, streaks, or minutes studied alone.
- Presenting a single session as long-term progression proof.
- Soft confidence narrated as strong understanding.
- Numeric Learning Coach scores as student-facing educational truth.
- Silent contradiction of the Student Educational Profile without acknowledging re-diagnosis need.
- Engineering or optimiser jargon as the reason for progression belief.

---

## 7. Explanation Templates (Educational, Not UI Copy Mandates)

Templates illustrate required meaning. Product copy may vary if meaning is preserved.

### 7.1 Genuine progression (application forming)

> **For [topic],** evidence across several practice sessions suggests your **application is developing**.  
> **Because** recent question work shows improving use of the method — not merely that you finished study tasks.  
> **Next priority:** keep varied practice and add a **spaced return** soon so we can check whether this holds.

### 7.2 Coverage without understanding warrant

> **For [topic],** you’ve **covered more of the syllabus**, which is real progress on study coverage.  
> **We do not yet have enough practice evidence** to say understanding is progressing.  
> **Next priority:** focused practice so we can judge understanding honestly.

### 7.3 Stall

> **For [topic],** you’re putting in study sessions, but **the evidence isn’t showing growth yet** on [retrieval / application].  
> **Because** the same difficulty pattern is repeating across recent attempts.  
> **Next priority:** [prerequisite review / misconception repair / method change] before more of the same.

### 7.4 Inconsistency (immediate vs spaced)

> **For [topic],** you can often succeed **soon after study**, but results **weaken when you return later**.  
> **So we won’t call this durable knowledge yet.**  
> **Next priority:** retrieval practice with deliberate spacing.

### 7.5 Decay after break

> **For [topic],** earlier practice was encouraging; **after the break**, we need to rebuild before claiming the same strength.  
> **Coverage remains;** understanding is being re-checked.  
> **Next priority:** gentle retrieval rebuild, not punishment catch-up.

### 7.6 Acceleration with challenge

> **For [topic],** evidence is **accumulating quickly and holding** across sessions.  
> **Because** practice outcomes are consistently strong — not because you completed more ticks.  
> **Next priority:** carefully **increase challenge** while still checking retention.

### 7.7 Insufficient warrant

> **For [topic],** it’s **too early to judge** whether understanding is progressing.  
> **We mainly have study contact so far**, without enough performance evidence.  
> **Next priority:** complete focused practice so a fair judgement becomes possible.

### 7.8 Exam-readiness caution

> **Overall preparation** is **not yet something we can call exam-ready** on the evidence we have.  
> **Because** [coverage is incomplete / practice is thin / retention untested / mocks absent] — **not** because you haven’t been busy.  
> **Next priority:** [named educational priority], and we’ll keep readiness language honest.

---

## 8. Explaining Interventions

When an intervention is recommended, explanation must include:

| Element | Example |
|---------|---------|
| Trigger | “Because growth has stalled on application…” |
| Intervention | “…we recommend prerequisite review…” |
| Educational aim | “…so current practice can start working.” |
| Boundary | “This is coaching guidance under your Study Plan — not a rewrite of your long-term plan.” (unless LI-12 escalation is the message) |

Escalation (LI-12) must be explicit and calm:

> “Local coaching isn’t enough to fix this honestly within the current plan envelopes. We should adjust the longer-term plan.”

---

## 9. Surface Contracts

Wherever Learning Coach progression meaning is surfaced (future UI, coaching copy, Profile narration adjuncts):

| Surface obligation | Rule |
|--------------------|------|
| Progression summary | Must answer the three answers (§3.1) |
| Topic / domain cards | Must not show “Mastered” from coverage alone |
| Timeline / history views | Must distinguish completion events from performance evidence |
| Readiness widgets | Must not consume Learning Coach LPS-7 without EIP-006 / Profile warrant |
| Empty / cold start | Must use insufficient-warrant speech, not fake trajectories |

Implementation of surfaces is out of scope for MS001; the contract binds future surfaces.

---

## 10. Audit Checklist (Educational)

Before releasing student-facing progression narration, confirm:

- [ ] Scope named
- [ ] Objective(s) named in plain language
- [ ] Belief stated without overclaim
- [ ] Evidence trail referenced (or insufficient warrant explicit)
- [ ] Completion not used as mastery proof
- [ ] Estimate vs fact distinction visible
- [ ] Next educational priority clear
- [ ] Intervention (if any) linked to trigger
- [ ] Profile consistency respected or re-diagnosis acknowledged
- [ ] No numeric progression theatre

---

## 11. Cross References

| Document | Relationship |
|----------|--------------|
| `../EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | Global speech law |
| `LEARNING_PROGRESSION_MODEL.md` | What must be explained |
| `LEARNING_OBJECTIVES.md` | Objective vocabulary |
| `LEARNING_EVIDENCE_MODEL.md` | Evidence trail meanings |
| `LEARNING_PROGRESSION_STATES.md` | Posture vocabulary |
| `../learning_interventions/INTERVENTION_CATALOGUE.md` | Next-priority vocabulary (MS003) |
| `LEARNING_INTERVENTIONS.md` | Compatibility pointer to MS003 |
| `../student_profile/PROFILE_EXPLAINABILITY.md` | Diagnosis speech (sibling, not replacement) |
| `../daily_coach/DAILY_COACH_EXPLAINABILITY.md` | Day-horizon speech (sibling) |
