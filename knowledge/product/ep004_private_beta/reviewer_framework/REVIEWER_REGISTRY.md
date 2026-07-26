# Reviewer Registry

**Programme:** EP-004 Private Beta Blind Review (permanent research infrastructure)  
**Framework root:** `knowledge/product/ep004_private_beta/reviewer_framework/`  
**Persona definitions:** [`personas/`](personas/)  
**Review outputs:** [`../blind_reviews/`](../blind_reviews/)  
**Status:** Permanent — SV-001 through SV-020 frozen as canonical cohort

This registry is the master index of independent student reviewers. Each row maps to a structured persona file and a review output path. Re-running a reviewer does **not** require recreating prompts.

---

## Master table

| Reviewer ID | Name | Exam | Attempt | Weeks to Exam | Occupation | Educational Hypothesis | Primary Evaluation Dimension | Review File |
|---|---|---|---|---|---|---|---|---|
| SV-001 | Emma Wilson | CS1 | First Sitting | 12 | University Graduate | First-use clarity | Adoption | [`blind_reviews/SV-001.md`](../blind_reviews/SV-001.md) |
| SV-002 | Sarah Mitchell | CM1 | First Sitting | 14 | Actuarial Analyst | Weeknight time efficiency | Workflow | [`blind_reviews/SV-002.md`](../blind_reviews/SV-002.md) |
| SV-003 | Daniel Foster | CS2 | First Sitting | 12 | University Student | Value against mature study system | Trust | [`blind_reviews/SV-003.md`](../blind_reviews/SV-003.md) |
| SV-004 | Michael Dube | CS1 | Second Sitting | 9 | Actuarial Student | Restart after missed study days | Motivation | [`blind_reviews/SV-004.md`](../blind_reviews/SV-004.md) |
| SV-005 | Priya Patel | CM1 | First Sitting | 10 | Graduate Actuarial Consultant | Explainability of recommendations | Trust | [`blind_reviews/SV-005.md`](../blind_reviews/SV-005.md) |
| SV-006 | James Walker | CM1 | Second Sitting | 4 | Graduate Actuarial Analyst | Late-revision adoption value | Urgency | [`blind_reviews/SV-006.md`](../blind_reviews/SV-006.md) |
| SV-007 | Emily Roberts | CS1 | First Sitting | 10 | Graduate Actuarial Consultant | Habit retention after novelty | Habit | [`blind_reviews/SV-007.md`](../blind_reviews/SV-007.md) |
| SV-008 | Rachel Evans | CM1 | Second Sitting (possible) | Results day | Graduate Actuarial Consultant | Emotional recovery after failure | Trust | [`blind_reviews/SV-008.md`](../blind_reviews/SV-008.md) |
| SV-009 | Alex Morgan | CS1 | Second Sitting | — | Senior Actuarial Analyst | Substitution against existing tools | Workflow | [`blind_reviews/SV-009.md`](../blind_reviews/SV-009.md) |
| SV-010 | Hannah Brooks | CS1 | First Sitting | 9 | Graduate Actuarial Consultant | Error recovery and recoverability | Trust | [`blind_reviews/SV-010.md`](../blind_reviews/SV-010.md) |
| SV-011 | Oliver Hughes | CM1 | First Sitting | 14 | Graduate Actuarial Consultant | Improvement awareness / educational feedback | Educational Feedback | [`blind_reviews/SV-011.md`](../blind_reviews/SV-011.md) |
| SV-012 | Nathan Cole | CM1 | First Sitting | 11 | Graduate Actuarial Analyst | Adaptation after poor performance | Adaptation | [`blind_reviews/SV-012.md`](../blind_reviews/SV-012.md) |
| SV-013 | Charlotte Green | CM1 | Second Sitting | 6 | Graduate Actuarial Consultant | Overconfidence / calibration safety | Calibration | [`blind_reviews/SV-013.md`](../blind_reviews/SV-013.md) |
| SV-014 | Benjamin Clarke | CS1 | First Sitting | 10 | Graduate Actuarial Analyst | System explainability / mental model | Trust | [`blind_reviews/SV-014.md`](../blind_reviews/SV-014.md) |
| SV-015 | Sophie Turner | CM1 | First Sitting | 9 | Graduate Actuarial Consultant | Study decision quality | Decision Support | [`blind_reviews/SV-015.md`](../blind_reviews/SV-015.md) |
| SV-016 | Emily Foster | CS1 | First Sitting | 8 | Graduate Actuarial Analyst | Cognitive load / organisational burden | Workflow | [`blind_reviews/SV-016.md`](../blind_reviews/SV-016.md) |
| SV-017 | Daniel Morris | CM1 | Second Sitting | 7 | Actuarial Consultant | Deliberate practice vs busywork | Deliberate Practice | [`blind_reviews/SV-017.md`](../blind_reviews/SV-017.md) |
| SV-018 | Rebecca Lawson | CS1 | Second Sitting | 5 | Senior Actuarial Analyst | Workflow essentiality after sustained use | Workflow | [`blind_reviews/SV-018.md`](../blind_reviews/SV-018.md) |
| SV-019 | James Whitfield | CM1 | Second Sitting | 4 | Actuarial Consultant | Exam performance transfer | Exam Transfer | [`blind_reviews/SV-019.md`](../blind_reviews/SV-019.md) |
| SV-020 | Michael Edwards | CS1 | First Sitting | 12 | Graduate Actuarial Consultant | Bounded commitment as study companion | Adoption | [`blind_reviews/SV-020.md`](../blind_reviews/SV-020.md) |

---

## Counts

| Slice | N | Reviewer IDs |
|---|---:|---|
| All | 20 | SV-001 … SV-020 |
| CS1 | 9 | SV-001, SV-004, SV-007, SV-009, SV-010, SV-014, SV-016, SV-018, SV-020 |
| CM1 | 10 | SV-002, SV-005, SV-006, SV-008, SV-011, SV-012, SV-013, SV-015, SV-017, SV-019 |
| CS2 | 1 | SV-003 |
| First Sitting | 12 | SV-001, SV-002, SV-003, SV-005, SV-007, SV-010, SV-011, SV-012, SV-014, SV-015, SV-016, SV-020 |
| Second Sitting (incl. possible) | 8 | SV-004, SV-006, SV-008, SV-009, SV-013, SV-017, SV-018, SV-019 |
| Workflow-tagged | 5 | SV-002, SV-007, SV-009, SV-016, SV-018 |
| Trust-tagged | 6 | SV-003, SV-005, SV-008, SV-010, SV-013, SV-014 |

---

## Primary dimension index

- **Adaptation:** SV-012
- **Adoption:** SV-001, SV-020
- **Calibration:** SV-013
- **Decision Support:** SV-015
- **Deliberate Practice:** SV-017
- **Educational Feedback:** SV-011
- **Exam Transfer:** SV-019
- **Habit:** SV-007
- **Motivation:** SV-004
- **Trust:** SV-003, SV-005, SV-008, SV-010, SV-014
- **Urgency:** SV-006
- **Workflow:** SV-002, SV-009, SV-016, SV-018

---

## How to use

1. Choose a Reviewer ID from the table.
2. Follow [`REVIEW_EXECUTION_GUIDE.md`](REVIEW_EXECUTION_GUIDE.md).
3. Load the matching `personas/SV-XXX.yaml`.
4. Write the review to the Review File path (overwrite on repeat runs unless archived).

Do not invent a new persona when an existing reviewer already tests the needed hypothesis.
