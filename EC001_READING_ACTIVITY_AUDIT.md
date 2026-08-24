# EC-001 — Reading Activity Audit

**Programme:** EC-001 CMP Partnership Remediation  
**Authority:** EF-001 · PB-001 F1/F2 · EA-004 Reading Guidance Architecture  
**Date:** 2026-08-01  
**Unit of audit:** Guided Reading activity (`reading_guidance`) per published educational package  

**Verdict key**

| Verdict | Meaning |
|---------|---------|
| **PASS** | Q1–Q6 each answered so a diligent student knows how to use the CMP for this activity |
| **FAIL** | One or more of Q1–Q6 unanswered or ambiguous |

Post-remediation results are authoritative. Pre-remediation notes record why EC-001 was required.

---

## Audit checklist (applied to every Reading activity)

| ID | Question |
|----|----------|
| Q1 | Exactly what CMP material should be opened? |
| Q2 | What is the educational purpose of reading it? |
| Q3 | What should the student pay attention to? |
| Q4 | What should the student ignore if applicable? |
| Q5 | How should the student know they are finished? |
| Q6 | What activity follows immediately after the reading? |

---

## Summary

| Package | Mode | Pre-EC-001 | Post-EC-001 |
|---------|------|------------|-------------|
| `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-EP001-PKG-REV-PURPOSE-EDA` | Revision | FAIL (Q6 naming soft) | **PASS** |
| `CS1-CS1002-PKG-1.2-PCA` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-CS1002-PKG-2.1-DISCRETE` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-CS1002-PKG-2.1-CONTINUOUS` | Learning | FAIL (Q6; Q2 weak) | **PASS** |
| `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | Revision | FAIL (Q6 naming soft) | **PASS** |

**Inventory result after remediation: 9/9 PASS.**

---

## 1. `CS1-EA005-PKG-4.2-GLM-STRUCTURE` — Guided Reading

**Artefact:** `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json`  
**Status:** `publication_approved` (live loader)  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | `open_point` = CMP · Syllabus 4.2 GLM setup (4.2.1–4.2.3); `exit_line` opens IFoA CS1 CMP 2026 at that locus |
| Q2 | PASS | `lead_line` states purpose: extract GLM chain so link choice is structural, not software habit |
| Q3 | PASS | Four focus questions; Family/η/Link sketch; attempt-before-reveal on first worked example; misconception watch |
| Q4 | PASS | `out_of_scope_today` + exit ignore clause (deviance, factor theatre, Bayesian 5.1, coding marathon) |
| Q5 | PASS | Stop after first structural non-identity-link example; `return_cue` defines finished = example complete + focus questions answerable from notes |
| Q6 | PASS | Explicit next: Worked-example re-entry (CMP closed), then Knowledge Checks (Active Recall → Checkpoint) |

**Pre-EC-001 FAIL justification:** Q6 only implied (“we will check what the reading fixed”); partnership purpose not front-loaded in `lead_line`.

---

## 2. `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` — Guided Reading

**Artefact:** `.../campaign-alpha-ep001/packages/1.1-purpose-function-ep001.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 1.1 purpose-and-function (1.1.1–1.1.4 centre); edition named in `exit_line` |
| Q2 | PASS | Purpose: build professional purpose map (aims/stages/sources/reproducibility) from CMP, not from Kwalitec prose |
| Q3 | PASS | Focus questions on aims/stages/sources/reproducibility; annotation four-box sketch; misconception watch |
| Q4 | PASS | Ignore EDA recipes, correlation/PCA, coding marathon, distribution catalogue |
| Q5 | PASS | Finished when aims–stages–sources–reproducibility block complete and focus questions answerable from notes |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Strong locus already existed, but next activity unnamed; LIVE PB-001 empty shell was fallback delivery, not absence of this packet’s CMP locus fields.

---

## 3. `CS1-EP001-PKG-1.2-EDA-SUMMARIES` — Guided Reading

**Artefact:** `.../packages/1.2-eda-summaries-ep001.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 1.2.1 summaries and exploratory visualisations |
| Q2 | PASS | Purpose: choose summaries/visualisations for a stated aim and variable type |
| Q3 | PASS | Focus questions + annotation + misconception watch |
| Q4 | PASS | Ignore correlation, PCA, coding marathon, distribution catalogue |
| Q5 | PASS | Stop/finish after 1.2.1 summaries-and-visualisations block |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Q6 unnamed; purpose implicit.

---

## 4. `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` — Guided Reading

**Artefact:** `.../packages/1.2-eda-association-ep001.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 1.2.2 correlation measures |
| Q2 | PASS | Purpose: distinguish Pearson / Spearman / Kendall and supported association claims |
| Q3 | PASS | Focus questions + annotation + misconception watch |
| Q4 | PASS | Ignore PCA, new summary deep-dives, coding marathon, Chapter 2 |
| Q5 | PASS | Stop before PCA; finished when 1.2.2 block complete |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Q6 unnamed; purpose implicit.

---

## 5. `CS1-EP001-PKG-REV-PURPOSE-EDA` — Revision Reading Guidance

**Artefact:** `.../packages/revision-purpose-eda-ep001.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Authoritative instruction: **do not open a new CMP chapter first**; targeted reopen only after failed retrieval at Day 1 / 1.2.1 / 1.2.2 loci |
| Q2 | PASS | Purpose: strengthen retrieval of Campaign Alpha chain without a fresh chapter read |
| Q3 | PASS | Focus on closed-book Campaign chain sketch; retrieval checks; reopen only failed locus |
| Q4 | PASS | Do not begin 1.2.3 or 2.1; no fresh chapter read |
| Q5 | PASS | Finished with guidance stage when CMP stays closed and student is ready for revision checks |
| Q6 | PASS | Immediate next: revision Knowledge Checks (retrieval) |

**Pre-EC-001 FAIL justification:** Retrieval-first CMP policy was present, but “next activity” naming was soft relative to EC-001 Q6 bar.

---

## 6. `CS1-CS1002-PKG-1.2-PCA` — Guided Reading

**Artefact:** `.../campaign-beta-cs1002/packages/1.2-pca-cs1002.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 1.2.3 PCA |
| Q2 | PASS | Purpose: dimensionality reduction accountability (what early components capture; unsafe claims) |
| Q3 | PASS | Focus questions + annotation + misconception watch |
| Q4 | PASS | Ignore Chapter 2 / univariate distributions and coding marathon |
| Q5 | PASS | Finished when 1.2.3 PCA block complete |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Q6 unnamed; purpose implicit.

---

## 7. `CS1-CS1002-PKG-2.1-DISCRETE` — Guided Reading

**Artefact:** `.../packages/2.1-discrete-cs1002.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 2.1.1 discrete univariate distributions |
| Q2 | PASS | Purpose: situation-led discrete family choice |
| Q3 | PASS | Focus questions + annotation + misconception watch |
| Q4 | PASS | Ignore continuous families and coding marathon beyond stop |
| Q5 | PASS | Finished when 2.1.1 discrete block complete |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Q6 unnamed; purpose implicit.

---

## 8. `CS1-CS1002-PKG-2.1-CONTINUOUS` — Guided Reading

**Artefact:** `.../packages/2.1-continuous-cs1002.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | Open CMP at Syllabus 2.1.2 continuous distributions |
| Q2 | PASS | Purpose: support-led continuous family choice |
| Q3 | PASS | Focus questions + annotation + misconception watch |
| Q4 | PASS | Ignore discrete re-cataloguing and coding marathon beyond stop |
| Q5 | PASS | Finished when 2.1.2 continuous block complete |
| Q6 | PASS | Next: Worked-example re-entry → Knowledge Checks |

**Pre-EC-001 FAIL justification:** Q6 unnamed; purpose implicit.

---

## 9. `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` — Revision Reading Guidance

**Artefact:** `.../packages/revision-pca-distributions-cs1002.json`  
**Post-EC-001 verdict: PASS**

| Q | Verdict | Justification |
|---|---------|---------------|
| Q1 | PASS | CMP closed first; targeted reopen only after fail at PCA / 2.1.1 / 2.1.2 loci |
| Q2 | PASS | Purpose: retrieve Campaign Beta chain without new chapter open |
| Q3 | PASS | Closed-book chain sketch; retrieval checks; locus-limited reopen |
| Q4 | PASS | Do not begin 2.1.3 or 2.2 |
| Q5 | PASS | Guidance finished when ready for revision checks with CMP closed |
| Q6 | PASS | Immediate next: revision Knowledge Checks |

**Pre-EC-001 FAIL justification:** Soft Q6 naming relative to EC-001 bar.

---

## Non-inventory observation (not a package Reading activity)

| Surface | Verdict | Justification |
|---------|---------|---------------|
| LIVE RC2 Study 1.1 fallback Reading (`substance_planner` LO shell) | **FAIL** (delivery) | PB-001 F1/F2: no CMP direction, no reading substance. This is **not** package #2’s Guided Reading packet. Clearing it requires Publication Approver + joint Volume activation (see `EC001_REMEDIATION_PLAN.md`) — outside EC-001’s Runtime-change ban. |

EC-001 does not reclassify that delivery residual as an Educational Framework deficiency (EF-001 Check remains YES).

---

## Success criterion

For every Reading activity in the published educational package inventory: **PASS**.

A diligent student following any remediated package Guided Reading knows how to use the CMP (or, on Revision days, when *not* to open it first) and what to do next in Kwalitec.
