# EV-001 — Learning Episode Audit

**Programme:** Educational Validation Programme EV-001  
**Environment:** https://kwalitec.onrender.com · commit `613722c…`  
**Session audited:** `lsr-18e4b384b9cc` (mission 4.2 GLM)  
**Date:** 2026-08-01

---

## Episode path observed

```text
Home → Start Today's Session
  → /session/.../overview
  → Begin Session
  → /session/.../activity  (Reading · Activity 1 of 3)
  → Submit Answer (repeated)
  → Flash “Answer recorded… continue” without Continue / without advance
```

Worked example and Practice stages were **advertised** (“Next · Worked example”, “Activity 1 of 3”) but **not reached** because the activity index did not advance after answers.

---

## Evaluation rubric (live episode)

| Criterion | Observation | Flag |
|-----------|-------------|------|
| Educational coherence | Overview banner once names 4.2; body uses “Today’s topic” | Mechanically broken |
| Natural flow | Skeleton Read→Example→Practice→Reflect is fine; content does not flow | Templated |
| Depth | No GLM mathematics, no exponential family, no link functions | Educationally weak |
| Accuracy | Cannot assess accuracy — no substantive claims | N/A / empty |
| Transitions | “Next · Worked example” never arrives | Broken |
| Examples | None | Educationally weak |
| Learning objective quality | “Strengthen today’s focus topic” / bullet “Today’s topic” | Generic · Topic-title driven |
| Success criteria | “explain Today’s topic… without notes” | Placeholder |
| Tutor vs database export | Reads as unfilled template over a topic key | **Database export / templated** |

---

## Flags raised (mandatory list)

| Flag | Present? | Evidence |
|------|----------|----------|
| Generic | **Yes** | “Today’s topic”, “Strengthen today’s focus topic” |
| Templated | **Yes** | Same shell fields; readiness ±3% boilerplate |
| Mechanically concatenated | **Yes** | “Strengthen Today’s topic by focusing on Strengthen today’s focus topic.” |
| CMP pasted | **Indirect** | Home/Syllabus use CMP-like stems; session fails to teach them |
| Syllabus pasted | **Yes** on Home; **failed substitution** in session | Title vs placeholder split |
| Topic-title driven | **Yes** | Mission = syllabus heading |
| Educationally weak | **Yes** | No teachable content in Reading stage |

---

## Reading activity (Episode 1) — verbatim character

Student is told to “Read the material for Today’s topic” and “Note one idea,” with a free-text box and hint “Underline the objective that feels least clear.” **No material is provided.**

That is not a Learning Episode. It is a prompt pointing off-platform.

---

## Progression defect

After `POST .../activity/answer`:

- Notification claims feedback exists  
- Page re-renders the same Reading 1 of 3 form  
- No feedback panel, no Continue CTA  

This blocks the remainder of the episode sequence and prevents Reflection / Summary from being audited as completed student work.

---

## Episode quality score

**1 / 10** — below the minimum bar for primary study.

An experienced IFoA tutor would not permit a student to spend an examination-prep hour inside this episode without opening the CMP.

**Related trust breaks:** TB-001, TB-007, TB-008, TB-013.
