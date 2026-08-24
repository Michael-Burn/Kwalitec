# EC-001 — Remediation Plan

**Programme:** EC-001 CMP Partnership Remediation  
**Authority:** EF-001 · PB-001 F1/F2  
**Classification:** EC-S1  
**Date:** 2026-08-01  
**Nature:** Educational content remediation only  

---

## 1. Objective

Eliminate Reading activities that leave a diligent student uncertain how to use the CMP, by authoring explicit CMP partnership guidance in every published educational package — without modifying Educational Framework, Runtime, SCI, recommendation engines, Study Plan algorithms, or product architecture.

---

## 2. Root-cause map (PB-001 → EC-001)

| Observation | Layer | In EC-001 scope? | Action |
|-------------|-------|------------------|--------|
| Catalogue Guided Reading lacked explicit Q6 next-activity naming and front-loaded purpose | Educational content | **Yes** | Remediate `reading_guidance` fields |
| LIVE Study 1.1 showed empty LO Reading shell with zero CMP strings | Delivery of catalogue vs fallback shell | **Content ready; activation residual** | Document pathway; do not redesign Runtime in EC-001 |
| Volumes `publication_ready` ≠ `released`; campaign packs not in live `publication_approved` set | Publication / activation (KI-H1, KI-H4, PR-001 B-01/B-02) | **No (ops/activation)** | Hand off after content PASS |

---

## 3. Remediation executed (content)

### 3.1 Fields updated (every inventory package)

For each package’s `reading_guidance`:

| Field | Remediation intent |
|-------|--------------------|
| `lead_line` | Explicit **purpose of this reading/revision** (Q2) + CMP-as-authority |
| `exit_line` | Open/keep-closed instruction (Q1), partnership sentence, hunt/ignore (Q3/Q4), stop (Q5), **named next activity** (Q6) |
| `return_cue` | Finished criteria (Q5) + immediate next activity (Q6) |
| `reentry_line` | Immediate next activity with CMP closed (Q6) |

Preserved unchanged in structure: `open_point`, `stop_condition`, `focus_questions`, `misconception_watch`, `out_of_scope_today`, `annotation_task`, `attempt_before_reveal`, `pause_points` (already carried Q1/Q3/Q4/Q5 locus detail).

### 3.2 Packages remediated

1. `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json`  
2. `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/packages/1.1-purpose-function-ep001.json`  
3. `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/packages/1.2-eda-summaries-ep001.json`  
4. `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/packages/1.2-eda-association-ep001.json`  
5. `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/packages/revision-purpose-eda-ep001.json`  
6. `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/packages/1.2-pca-cs1002.json`  
7. `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/packages/2.1-discrete-cs1002.json`  
8. `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/packages/2.1-continuous-cs1002.json`  
9. `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/packages/revision-pca-distributions-cs1002.json`  

Each package `certification_refs` now cites `EC001_CMP_PARTNERSHIP_AUDIT.md`.

### 3.3 Partnership copy rules used

- Name the CMP edition and syllabus locus (or “CMP closed first” on Revision).  
- State that Kwalitec is the guide and the CMP is authoritative — this screen is not a substitute textbook.  
- Name ignore list and stop condition in student speech.  
- Name the immediate next in-app activity (Worked-example re-entry → Knowledge Checks, or revision Knowledge Checks).  
- Never assume the student already knows how to study the CMP.

---

## 4. Validation

| Check | Result |
|-------|--------|
| Q1–Q6 desk audit on all 9 Reading activities | **9/9 PASS** — `EC001_READING_ACTIVITY_AUDIT.md` |
| EA-006 publication / substance tests | `pytest tests/application/educational_packages/test_ea006_publication.py` — **7 passed** |
| Runtime / framework / SCI / recs / Study Plan code | **Unmodified** |

---

## 5. Residual plan (not executed in EC-001)

These clear PB-001 LIVE re-test of the trust claim; they are **not** Educational Framework work and were **not** Runtime changes inside this programme.

| Step | Owner | Why required |
|------|-------|--------------|
| Publication Approver sign-off for CS1-001 / CS1-002 | Publication Approver | Catalogue → `approved` (PR-001 B-01) |
| Joint activation / release onto student pathway | Activation engineering | `released` without partial inventory (PR-001 B-02; KI-H1/H4) |
| Re-run adversarial / Founder walk on LIVE after release | Educational Validation | Confirm F1/F2 closed on student-reachable path |
| Do **not** cherry-pick single-day copies into `educational_packages/` before Approver | Editorial Office | EO-001 joint inventory / FR-02 |

Until those steps complete, LIVE enrolment on topics without a live `publication_approved` package may still present the empty fallback Reading shell. Catalogue Reading activities themselves are partnership-complete.

---

## 6. Definition of done (EC-001)

| Criterion | Status |
|-----------|--------|
| Every published package Reading activity audited PASS/FAIL with justification | **Done** |
| No inventory Reading activity fails Q1–Q6 | **Done** |
| `EC001_CMP_PARTNERSHIP_AUDIT.md` produced | **Done** |
| `EC001_READING_ACTIVITY_AUDIT.md` produced | **Done** |
| `EC001_REMEDIATION_PLAN.md` produced | **Done** |
| Educational content remediated; Runtime/framework untouched | **Done** |
| LIVE claim re-validated on released pathway | **Deferred** to activation successor |

---

## 7. Stop

EC-001 educational-content remediation is complete for the published package inventory. Do not start Runtime, framework, or activation programmes under this mission ID.
