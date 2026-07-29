# FV-001B Re-run — Regression Audit

**Scope:** Confirm publication safety, preview gates, validation, upload binding, and Subject Catalogue Ready reflection after the Workflow Completion work — evaluated only via visible Founder UI.

**Evidence:** `_evidence/complete.json`, `_evidence/focus.json`, `_evidence/screenshots/regression_*.png`, `phase4_both_docs_ready.png`, `phase9_subjects_not_ready.png`

---

## 1. Publication safety still enforced

| Check | Result | Evidence |
|---|---|---|
| Incomplete workspace cannot publish successfully | **Pass** | CS1T publish flash refuses (`regression_incomplete_publish.png`) |
| Dual-upload workspace still refuses publish when approval incomplete | **Pass** (refusal shown) | CS1U `phase8_publish_refused.png` |
| Founder ever reaches successful publish | **Fail** (journey blocked earlier) | No success publish flash in any capture |

**Notes:** Safety refusals remain visible. The regression concern is not “safety removed” — it is that the **happy path never clears** the same gates.

---

## 2. Approval requires preview

| Check | Result | Evidence |
|---|---|---|
| Empty preview path does not claim success | **Pass** | CS1T: “couldn't build a meaningful preview — no extracted curriculum topics” |
| Approve after claimed preview success | **Fail** | Approve returns **publish** refusal; no approval success (`phase7_approve_confused.png`) |
| Preview status honest after Build Preview | **Fail** | Success flash + `not_ready` simultaneously |

**Notes:** Empty preview gate appears intact. Preview/Approve honesty on the non-empty path regresses trust.

---

## 3. Validation cannot be bypassed

| Check | Result | Evidence |
|---|---|---|
| Validate can fail and block | **Pass** | Blocking flash on CS1U / CS1R |
| Validate can succeed when docs Ready + extraction done | **Fail** | CS1U both Ready, Topics 23, 0 validation errors — still “blocking findings” |
| Findings explain the block | **Fail** | Flash says “review findings below”; findings list absent on CS1U failure screen |

**Notes:** Bypass is not available; **completion** is also not available. That is a launch blocker, not a safety win alone.

---

## 4. Upload bindings remain correct

| Check | Result | Evidence |
|---|---|---|
| Slots labelled Official CMP / Official Syllabus | **Pass** | Workspace Content Sources |
| Correct files can bind to correct slots | **Pass** | CS1U `Official CMP · official_cmp.pdf` + `Official Syllabus · official_syllabus.pdf` |
| Mis-selection can show crossed filenames | **Observed risk** | CS1R first walk showed crossed names when wrong files selected |
| Auto-upload without separate Upload button | **Observed** | Files appear after select; no Upload CTA required |

**Notes:** Binding **can** be correct. Founder still depends on careful file choice; crossed filenames are visible when wrong.

---

## 5. Subject Catalogue accurately reflects publication state

| Check | Result | Evidence |
|---|---|---|
| Unpublished subjects not shown as Ready | **Pass** | CS1R/S/T/U rows are Subject / Content Sources / Draft / Validation |
| After successful publish, Ready + version + date | **Not testable / Fail** | Publish never succeeded; no Ready row (`phase9_subjects_not_ready.png`) |
| Student catalogue shows new Ready subject | **Fail** | Orientation only; no Ready CS1U observed |

---

## Regression summary

| Area | Regressed? | Comment |
|---|---|---|
| Publish safety refusals | No | Still refuse incomplete publish |
| Empty preview success | No | Still refuse empty preview |
| Validation bypass | No | Still blocks |
| Validation completion UX | **Yes (blocker)** | Blocks without actionable findings after Ready docs |
| Preview success honesty | **Yes (blocker)** | Success vs `not_ready` |
| Approve vs Publish messaging | **Yes (blocker)** | Approve shows publish copy |
| Catalogue Ready after publish | **Blocked** | Cannot verify positive path |

**Overall regression verdict:** Safety gates remain. The Founder **complete** workflow still does not work end-to-end on the visible UI.
