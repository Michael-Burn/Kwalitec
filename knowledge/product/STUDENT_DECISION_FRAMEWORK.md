# Student Decision Framework

**Programme:** ILE-011 — Student Decision Framework  
**Version:** 1.0  
**Status:** Active — permanent governing framework for decision support  
**Effective:** 2026-07-28  
**Authority:** Product philosophy (subordinate to Vision 2030; complementary to ILE-010 Sensei philosophy and Educational Constitution)  

---

## Purpose

Define the **complete decision model** for Kwalitec: which learning decisions a student owns, when Kwalitec may guide, and the principles that keep guidance trustworthy.

This document is the governing frame. Companions supply catalogue, responsibility, confidence, silence, and lifecycle detail.

| Document | Role |
|---|---|
| [`DECISION_CATALOGUE.md`](DECISION_CATALOGUE.md) | Every major learner decision and its constraints |
| [`GUIDANCE_RESPONSIBILITY_MATRIX.md`](GUIDANCE_RESPONSIBILITY_MATRIX.md) | Who decides vs who recommends |
| [`DECISION_CONFIDENCE_MODEL.md`](DECISION_CONFIDENCE_MODEL.md) | Evidence levels before guidance |
| [`SILENCE_PRINCIPLE.md`](SILENCE_PRINCIPLE.md) | When Kwalitec deliberately stays quiet |
| [`DECISION_LIFECYCLE.md`](DECISION_LIFECYCLE.md) | Observe → guide → act → reflect loop |

Does **not** change production code, architecture, educational algorithms, or UI. Runtime behaviour remains under Educational Intelligence, P-001.2, and P-001.3 law.

**Builds on:** [`STUDY_SENSEI_PHILOSOPHY.md`](STUDY_SENSEI_PHILOSOPHY.md), [`DECISION_MAKING_PRINCIPLES.md`](DECISION_MAKING_PRINCIPLES.md)

---

## Philosophy of decision support

Kwalitec is a **Study Sensei**.

> A Sensei does not make decisions for the learner.  
> A Sensei helps the learner make better decisions.

Product thesis remains: **Reduce decisions. Increase learning.**

“Reduce decisions” means reduce *decision overload and noise* — not strip the student of agency. Kwalitec surfaces one clear, explainable option when warranted; the student still chooses to accept, defer, modify, or ignore.

Decision support is therefore:

1. **Curriculum-first** — grounded in official syllabus truth (V1/V2).
2. **Evidence-first** — observations before advice.
3. **Explainable** — what / why now / what next / what is uncertain.
4. **Proportional** — effort matches available time and stakes.
5. **Honest** — silence and uncertainty beat false certainty.
6. **Non-manipulative** — never use guilt, FOMO, or engagement theatre.

---

## Decision ownership

**Default owner: the student.**

Every significant learning decision ultimately belongs to the learner. Kwalitec may inform, recommend, strongly recommend, or withhold comment — it may **never** silently decide high-stakes personal, career, or exam-administration outcomes on the student’s behalf.

| Owner | Meaning |
|---|---|
| **Student** | Final choice always rests with the learner |
| **Sensei (Kwalitec)** | May recommend when evidence and responsibility allow |
| **Shared** | Sensei proposes; student confirms, adjusts, or declines |

Shared responsibility (e.g. Daily Mission) is still *shared*: the Sensei constructs a lawful proposal; the student owns acceptance and execution.

---

## Shared responsibility

Shared decisions exist where:

- Educational Intelligence can lawfully propose a next action, **and**
- Execution requires the student’s time, attention, and consent, **and**
- Dismissal or adjustment must remain possible without punishment.

Examples of shared responsibility:

- What to study in today’s Mission
- Whether to revise a weak topic now vs later (Sensei ranks; student acts)
- Whether to shorten a session under workload pressure

Shared does **not** mean Kwalitec books the exam, chooses the career path, or overrides the student’s stated constraints.

---

## Evidence before guidance

No guidance without a warrant.

| Rule | Implication |
|---|---|
| Observe before interpret | Thin or missing evidence → wait, ask, or remain silent |
| Interpret through certified intelligence | Do not invent ranking, mastery, or readiness outside Educational Intelligence |
| Explain before asserting | If what/why/next/uncertain cannot be answered, do not claim a firm recommendation |
| Prefer one primary action | Multiple tips without a winner create decision overload |

See [`DECISION_CONFIDENCE_MODEL.md`](DECISION_CONFIDENCE_MODEL.md) for evidence levels and learner-facing behaviour.

---

## When Kwalitec should advise

Advise when **all** of the following hold:

1. The decision is in-scope for educational guidance (see Responsibility Matrix).
2. Evidence meets at least **Emerging confidence** for soft advice, or **Reliable guidance** for a primary recommendation (see Confidence Model).
3. The advice is explainable to P-001.2 quality at the surface default.
4. The action is proportional to available session time and plan coherence.
5. Speaking reduces decision load more than silence would.

Typical advise moments: study-today focus, topic selection, continue vs revise, readiness honesty, sustainable pacing adjustments tied to educational evidence.

---

## When Kwalitec should ask questions instead

Ask instead of advise when:

- Evidence is ambiguous and a short clarifying input would unlock lawful guidance (availability, exam date, confidence self-report, preference among close alternatives).
- The decision is shared but depends on student constraints Kwalitec cannot observe (energy, life events, tutor homework).
- Challenge or calibration needs the student’s own perception (“how ready do you feel?”) without treating self-report as mastery.
- Multiple lawful options are close and ranking would fake precision — present the trade-off and ask which fits today.

Questions must be few, purposeful, and optional where possible. Interrogation is not Sensei behaviour.

---

## When Kwalitec should remain silent

Remain silent when:

- Evidence is insufficient or conflicting (see Silence Principle).
- The decision is **Student only** or **Sensei never decides**.
- A recommendation would overclaim readiness, mastery, or exam outcome.
- The student is mid-authorised Mission and interruption would create competing tips.
- Outside educational responsibility (career, health diagnosis, financial/legal advice).
- High-stakes personal choices where software certainty would be dishonest.

Silence is a designed product behaviour, not an empty screen failure. Documented in [`SILENCE_PRINCIPLE.md`](SILENCE_PRINCIPLE.md).

---

## Mapping rule for future capabilities

Every future feature, tip, Coach surface, or Mission behaviour must map to **one or more** catalogue decisions and declare:

- Decision ID(s)
- Responsibility class
- Minimum confidence level
- Explainability obligation
- Silence conditions

If a capability cannot map to a learner decision, it is not Sensei guidance — it is noise, content theatre, or out of scope.

---

## Evaluation questions

1. Whose decision is this — and does the student still own the final call?
2. What evidence warrants speaking, asking, or staying silent?
3. Can we explain the guidance without inventing educational meaning?
4. Does this reduce decision overload without replacing learner agency?

---

**End of STUDENT_DECISION_FRAMEWORK**
