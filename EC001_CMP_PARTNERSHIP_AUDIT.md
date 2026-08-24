# EC-001 — CMP Partnership Audit

**Programme:** EC-001 CMP Partnership Remediation  
**Authority:** EF-001 (Frozen Educational Law) · PB-001 Findings F1 and F2  
**Classification:** EC-S1  
**Date:** 2026-08-01  
**Scope:** Educational content only — Educational Framework, Runtime, SCI, recommendation engine, Study Plan algorithms, and product architecture intentionally untouched  

---

## 1. Claim under remediation

Kwalitec must be an **explicit guide for using the CMP**, not an implicit replacement for it.

A diligent student completing any Guided Reading activity must know:

1. Exactly what CMP material to open  
2. Why that reading matters educationally  
3. What to pay attention to  
4. What to ignore (if applicable)  
5. How to know they are finished  
6. What in-app activity follows immediately after  

---

## 2. EF-001 Operational Reviews (mandatory)

### Review A — PB-001 F1 No CMP direction

1. **Observation:** LIVE RC2 Study 1.1 mission/session surfaces never directed CMP / Core Reading / page-section use; students were told to begin reading inside the product.  
2. **Classification:** EC  
3. **Severity:** S1  
4. **Evidence:** `PB001_ADVERSARIAL_EDUCATIONAL_VALIDATION_REPORT.md` F1; `knowledge/evidence/releases/PB001_RC2/` (`mentions_cmp=false` cohort).  
5. **Smallest Effective Intervention:** Author explicit CMP-use instructions on every Reading activity (locus, purpose, attention, ignore, stop, next activity) under existing Reading Guidance Architecture (EA-004).  
6. **EF-001 Check:** **YES** — content/authoring under existing Educational Law; no framework unfreeze.

### Review B — PB-001 F2 Empty Reading activity

1. **Observation:** LIVE Reading activity for Study 1.1 prompted “Study the reading…” with essentially no instructional body and no CMP redirect.  
2. **Classification:** EC  
3. **Severity:** S1  
4. **Evidence:** PB-001 F2; LIVE HTML samples under `knowledge/evidence/releases/PB001_RC2/html_samples/`.  
5. **Smallest Effective Intervention:** Ensure every published package’s Guided Reading body is certified CMP partnership guidance (not an empty LO shell). Live delivery of catalogue packages remains a Publication Approver / activation concern (not Runtime redesign in this programme).  
6. **EF-001 Check:** **YES**.

---

## 3. Inventory audited (“currently published educational packages”)

| # | Package ID | Path class | Status | Mode | Topic |
|---|------------|------------|--------|------|-------|
| 1 | `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | Live EA-006 loader (`educational_packages/`) | `publication_approved` | Learning | 4.2 |
| 2 | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | Volume CS1-001 catalogue | `campaign_member_certified` | Learning | 1.1 |
| 3 | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | Volume CS1-001 catalogue | `campaign_member_certified` | Learning | 1.2.1 |
| 4 | `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | Volume CS1-001 catalogue | `campaign_member_certified` | Learning | 1.2.2 |
| 5 | `CS1-EP001-PKG-REV-PURPOSE-EDA` | Volume CS1-001 catalogue | `campaign_member_certified` | Revision | Alpha return |
| 6 | `CS1-CS1002-PKG-1.2-PCA` | Volume CS1-002 catalogue | `campaign_member_certified` | Learning | 1.2.3 |
| 7 | `CS1-CS1002-PKG-2.1-DISCRETE` | Volume CS1-002 catalogue | `campaign_member_certified` | Learning | 2.1.1 |
| 8 | `CS1-CS1002-PKG-2.1-CONTINUOUS` | Volume CS1-002 catalogue | `campaign_member_certified` | Learning | 2.1.2 |
| 9 | `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | Volume CS1-002 catalogue | `campaign_member_certified` | Revision | Beta return |

**Notes**

- Volumes CS1-001 / CS1-002 remain `publication_ready` (not student `released`) per EO-001 / PR-001 honesty.  
- Catalogue packages stay outside the EA-006 live `publication_approved` auto-load set until Approver + joint activation (KI-H1 / KI-H4).  
- LIVE Study 1.1 empty Reading observed in PB-001 was the **Runtime C fallback shell**, not the catalogue Guided Reading packet for package #2.

---

## 4. Partnership standard applied

| ID | Question | Content fields that must answer it |
|----|----------|-------------------------------------|
| Q1 | Exactly what CMP material should be opened? | `open_point` + `exit_line` (edition + locus); Revision: explicit “CMP closed first” |
| Q2 | Educational purpose of reading it? | `lead_line` (purpose of this reading / revision) |
| Q3 | What should the student pay attention to? | `focus_questions` + `annotation_task` / `misconception_watch` / `attempt_before_reveal` |
| Q4 | What should the student ignore? | `out_of_scope_today` + ignore clause in `exit_line` |
| Q5 | How should the student know they are finished? | `stop_condition` + finished criteria in `return_cue` |
| Q6 | What activity follows immediately after? | Explicit next-activity naming in `return_cue` / `exit_line` / `reentry_line` |

**Partnership rule:** Kwalitec guides; the CMP remains authoritative exposition. Reading activities must never assume the student already knows how to study the CMP.

---

## 5. Baseline partnership finding (pre-remediation)

| Finding | Severity | Detail |
|---------|----------|--------|
| Catalogue Learning packs had strong Q1–Q5 locus/attention/stop | — | EA-004 Reading Guidance already present |
| **Q6 weak / missing** across Learning packs | S1 for partnership claim | `reentry_line` said “we will check” without naming Worked-example re-entry → Knowledge Checks |
| Purpose framing (Q2) implicit rather than explicit “purpose of this reading” | S2→S1 under EC-001 bar | Lead lines described extract targets more than partnership purpose |
| LIVE fallback Reading for topics without live packages | S1 delivery | Empty LO shell (PB-001 F1/F2) — **activation / publication pathway**, not missing catalogue prose for 1.1 |

---

## 6. Post-remediation partnership verdict

| Package Reading activity | Partnership verdict |
|--------------------------|---------------------|
| All 9 inventory packages (see §3) | **PASS** — Q1–Q6 answered explicitly in `reading_guidance` |

**Success criterion (content inventory):** There no longer exists a Reading activity **inside the currently published educational package inventory** that leaves a diligent student uncertain how to use the CMP, provided that package’s Guided Reading is the activity presented.

**Residual (out of EC-001 Runtime-forbidden scope):** Until catalogue Volumes are Approver-approved and jointly activated onto the student pathway, ordinary LIVE enrolment on early spine topics can still receive the empty fallback shell. That is a **publication/activation** residual (KI-H1 / KI-H4), not an Educational Framework gap and not an unfinished package Reading packet.

---

## 7. What was not changed

- Educational Framework (EA / EO / TV / EJ / EW)  
- Runtime / SCI / recommendation engine / Study Plan algorithms / product architecture  
- Application loaders and substance mappers  

---

## 8. Evidence pointers

- Per-activity PASS/FAIL justifications: `EC001_READING_ACTIVITY_AUDIT.md`  
- Remediation sequence and residuals: `EC001_REMEDIATION_PLAN.md`  
- Authority observations: `PB001_ADVERSARIAL_EDUCATIONAL_VALIDATION_REPORT.md` F1–F2  
- Content artefacts: `app/curriculum/data/educational_campaigns/**/packages/*.json`, `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json`
