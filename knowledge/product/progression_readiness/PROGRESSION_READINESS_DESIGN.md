# Progression Readiness Design

**Status:** Locked design for the Progression Readiness evaluator (standalone; unwired)  
**Date:** 2026-09-12  
**Scope:** Demonstrated competence for progression on six fully evidenced CS1 objectives  
**Related:** Objective Evidence Architecture (OEA); Study Progress ownership Phases 1–3; Phase 6 grounding inventory

---

## Purpose

This document locks the Progression Readiness evaluator design so it lives in the repository, not only in external conversation.

The evaluator answers one question only:

> Does available Assessment Evidence justify introducing the next material for this objective?

It does **not** claim permanent mastery, Estimated Knowledge, or exam readiness.

---

## Terminology

| Term | Meaning |
|------|---------|
| **Progression Readiness** | Demonstrated competence sufficient to introduce next material |
| **READY** | Evidence supports progression for this objective under its authored contract |
| **NOT_READY** | Evidence shows the student has not yet demonstrated that competence |
| **INSUFFICIENT_EVIDENCE** | Evidence is too thin, incomplete, or blocked to decide READY or NOT_READY; always carries a reason code |
| **Authored contract** | Per-objective, readable rule describing which items matter and how outcomes map to readiness |

Correct framing: **demonstrated competence for progression**, not permanent mastery.

---

## Philosophy

### Contract-based, not score-based

Each objective has its own authored contract. No single universal rule spans all objectives. The six locked objectives do not share an equivalent evidentiary structure. Forcing one rule through all of them would be mathematically tidy but educationally arbitrary.

### No arbitrary numerical weighting

Where an objective requires more than one capability (for example both conceptual recognition and independent calculation), the contract states this as a **required capability**, not a point value or percentage split.

### Demonstrated performance, not mere participation

Only Assessment Evidence with `scored_correct is True` or `scored_correct is False` counts. Records with `scored_correct is None` (unscored attempts) are excluded from both correct and incorrect tallies. Prerequisite verification likewise requires at least one `scored_correct is True` row for the prerequisite objective.

---

## Standing principles (evaluator)

1. **INSUFFICIENT_EVIDENCE always carries a reason code:** `INSUFFICIENT_SAMPLE`, `REQUIRED_PREREQUISITE_UNVERIFIED`, `REQUIRED_MODALITY_NOT_OBSERVED`, or `CONFLICTING_EVIDENCE` when a contradictory pattern does not fit the other three. Never a bare, reasonless insufficient result.
2. **Read-only with respect to evidence.** The evaluator never writes Assessment Evidence; it only reads and evaluates.
3. **No general prerequisite graph** in this pass (deferred).
4. **No evidence-independence / diversity scoring** in this pass (deferred).
5. **Critical-misconception override.** If a wrong choice is authored and flagged as representing a critical misconception, selecting it forces `NOT_READY` regardless of aggregate correct counts (or numeric outcome on mixed contracts), once any prerequisite gate (if present) is past.
6. **Standalone until proven.** This evaluator must not be wired into live student-facing decisions, pages, or flows until a separate scoped brief authorizes consumers.

---

## Correction note (topic 1.1 rule-class assignment)

During implementation, a later restatement of this design transposed the two conceptual rule classes for topic 1.1:

- Restatement error assigned the **2-item** rule to LO01/LO02 and the **3-item** rule to LO03/LO04.
- The **live tagged catalogue** (and the original Phase 6 grounding investigation) show the opposite: LO01 and LO02 each have **three** tagged items; LO03 and LO04 each have **two**.

**This document records the corrected assignment.** The original grounding investigation and the original design decision were always correct. Only the later restatement transposed the two rule classes. The mismatch was catchable only by checking the real live catalogue against the restated text — exactly the verification discipline this project values.

Corrected assignment (binding):

| Objective | Live tagged item count | Rule class |
|-----------|------------------------|------------|
| `CS1-A-T01-LO01` | 3 | 3-item conceptual |
| `CS1-A-T01-LO02` | 3 | 3-item conceptual |
| `CS1-A-T01-LO03` | 2 | 2-item conceptual |
| `CS1-A-T01-LO04` | 2 | 2-item conceptual |

Every real tagged item remains evidence for its objective. Do not drop the third LO01/LO02 item. Do not invent a third item for LO03/LO04.

---

## Six locked contracts

Critical misconception tags are **empty** for all six today: no real distractor on these objectives is flagged as critical. The override capability remains present in the contract structure.

### CS1-A-T01-LO01 (1.1.1 aims) — conceptual, 3 items

Evidence items: `cs1017-1.1.1-ar-01`, `cs1017-1.1.1-cp-01`, `ep001-1.1-ar-01`

| Outcome among the 3 items | Result |
|---------------------------|--------|
| 3/3 correct | READY |
| 2/3 correct | READY |
| 1/3 correct | INSUFFICIENT_EVIDENCE (`INSUFFICIENT_SAMPLE`) |
| 0/3 correct | NOT_READY |

Critical-misconception override: available; unused today.

### CS1-A-T01-LO02 (1.1.2 stages/tools) — conceptual, 3 items

Evidence items: `cs1017-1.1.2-ar-01`, `cs1017-1.1.2-cp-01`, `ep001-1.1-cp-01`

Same rule as LO01.

### CS1-A-T01-LO03 (1.1.3 data sources) — conceptual, 2 items

Evidence items: `cs1017-1.1.3-ar-01`, `cs1017-1.1.3-cp-01`

| Outcome among the 2 items | Result |
|---------------------------|--------|
| 2/2 correct | READY |
| 1/2 correct | INSUFFICIENT_EVIDENCE (`INSUFFICIENT_SAMPLE`) |
| 0/2 correct | NOT_READY |

Critical-misconception override: available; unused today.

### CS1-A-T01-LO04 (1.1.4 reproducibility) — conceptual, 2 items

Evidence items: `cs1017-1.1.4-ar-01`, `cs1017-1.1.4-cp-01`

Same rule as LO03.

### CS1-B-T03-LO01 (2.3.1 conditional expectation) — mixed modality + prerequisite

Evidence items:

- MCQ: `cs1006-2.3.1-ar-01`
- Numeric: `cs1006-2.3.1-cp-01`

**Prerequisite:** `CS1-B-T02-LO01` (joint-distribution / 2.2.1 material). Verified means at least one Assessment Evidence record for that objective with `scored_correct is True`. Attempt-only or incorrect evidence does not verify.

Evaluate in order:

1. If prerequisite unverified → `INSUFFICIENT_EVIDENCE` (`REQUIRED_PREREQUISITE_UNVERIFIED`), regardless of this objective’s own evidence.
2. Only if prerequisite verified, evaluate mixed-modality evidence:

| MCQ | Numeric | Result |
|-----|---------|--------|
| correct | correct | READY |
| correct | incorrect | NOT_READY |
| incorrect | correct | INSUFFICIENT_EVIDENCE (`REQUIRED_MODALITY_NOT_OBSERVED`) |
| incorrect | incorrect | NOT_READY |

Missing scored observation for a required modality → `REQUIRED_MODALITY_NOT_OBSERVED`. Critical misconception on the MCQ incorrect choice forces NOT_READY (capability present; unused today).

**Catalogue honesty:** `CS1-B-T02-LO01` is a real syllabus objective id. No OEA-tagged items exist for it yet. Until topic 2.2 is tagged, the genuine check correctly returns unverified for every live student. That is intended behaviour: refuse a false READY rather than skip an unenforceable check. The mechanism must not be hard-coded to always fail; it starts working when 2.2 evidence appears.

### CS1-B-T03-LO02 (2.3.2 tower / total variance) — mixed modality, no prerequisite

Evidence items:

- MCQ: `cs1006-2.3.2-ar-01`
- Numeric: `cs1006-2.3.2-cp-01`

Same four-cell mixed-modality matrix as LO01 Step 2. No prerequisite. Critical override available; unused today.

---

## Non-goals (this implementation)

- Wiring into any live route, template, Home / Study / Journey surface, or student-facing decision
- Twin, Policy V1, OEA write path, Spacing, VP-001, or arbitration changes
- Expanding objective tagging beyond the six already tagged
- General prerequisite graphs or evidence-diversity scoring

---

## Implementation location

- Design: this file under `knowledge/product/progression_readiness/`
- Code: `app/application/progression_readiness/` (standalone application package; OEA read consumer only)
- Tests: `tests/application/progression_readiness/`
