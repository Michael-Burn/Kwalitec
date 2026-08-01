# RO1-R1 — Implementation Report

**Programme:** RO1-R1 — Tomorrow Preview Honesty Remediation  
**Classification:** PI-S2 (Product Implementation)  
**Authority:** RO-001A PASS WITH RESIDUAL · EF-001 Frozen Educational Law  
**Date:** 2026-08-01  
**Nature:** Presentation / chrome binding only — educational packages, Educational Framework, Runtime substance selection, and recommendation logic unmodified · Wave 2 not started  

---

## Summary

RO1-R1 closes the Finish/Home tomorrow chrome honesty gap by binding every student-facing Tomorrow Preview surface to the approved educational package’s `tomorrow_preview` fields (via `educational_package_id`, campaign chain / `campaign_day`, or unique topic code) instead of shared-`topic_code` first-match or title-keyword inference. Session Finish, Study Summary (sitting report), and Home Adaptive Workspace Tomorrow now resolve from the sitting’s package metadata. Package selection for Guided Reading / activities (PB-002) was already correct and is unchanged.

---

## Root cause

`sitting_report._tomorrow_preview` and Home mission composition called `find_educational_package(topic_title=…)` / first-match on shared `topic_code` `2.1`. That returned Campaign Beta Day-2 (`CS1-CS1002-PKG-2.1-DISCRETE`) tomorrow copy (“continuous univariate distributions (2.1.2)”) after Gamma sittings whose approved package tomorrow pointed at the next campaign day (e.g. CG-D4 → Gamma Revision).

## Smallest Effective Intervention

1. New helper `app/application/educational_packages/tomorrow_chrome.py` — format + resolve chrome package without first-match / title keywords.  
2. Finish / Study Summary — thread `educational_package_id` from session binding → completion opaque → sitting report; prefer `find_package_by_id`.  
3. Home — Adaptive Workspace passes mission / last-completed package id + completed package set into AuthoringContext; composition overlay uses campaign selection.  
4. Persist `educational_package_id` on session binding and activity sequence for durable Finish chrome.

## Surface review

| Surface | Tomorrow Preview source after RO1-R1 | Result |
|---------|--------------------------------------|--------|
| Session finish (`data-tomorrow-preview`) | Sitting `educational_package_id` → package `student_facing` / continuity | Fixed |
| Study summary / Sitting Report | Same as finish | Fixed |
| Home Tomorrow section | Active package id, or last-completed when `day_complete` | Fixed |
| Mission cards (Home hero) | Mission title from Runtime / educational VM (not TP chrome) | N/A for TP text |
| Dashboard (student) | No dedicated Tomorrow Preview chrome | N/A |
| Journey “Up Next” | Syllabus journey path (not Gate-TP Tomorrow Preview chrome) | Out of TP chrome scope; package chain unchanged |

## Explicit non-changes

- Educational package JSON — unmodified  
- Educational Framework (EA/EO/TV/EJ/EW) — unmodified  
- Runtime educational substance selection (PB-002) — unmodified  
- Recommendation ranking / Runtime A — unmodified  
- Wave 2 — not started  

---

## Files Created

- `app/application/educational_packages/tomorrow_chrome.py`
- `tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py`
- `RO1R1_IMPLEMENTATION_REPORT.md`
- `RO1R1_REGRESSION_REPORT.md`
- `RO1R1_LIVE_VERIFICATION.md`

## Files Modified

- `app/application/educational_authoring/dto.py`
- `app/application/educational_authoring/engine.py`
- `app/application/educational_packages/composition_overlay.py`
- `app/application/session_experience/completion_service.py`
- `app/application/student_runtime/coordinator.py`
- `app/infrastructure/adapters/learning_session/persistence.py`
- `app/infrastructure/adapters/learning_session/runtime_engine.py`
- `app/infrastructure/adapters/learning_session/package_activity_engine.py`
- `app/presentation/session/sitting_report.py`
- `app/presentation/session/view_models.py`
- `app/presentation/student/adaptive_workspace.py`

## Tests Executed

```text
python3 -m pytest \
  tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py \
  tests/test_kwp015_educational_authoring.py \
  tests/test_kwp005_sitting_reports.py \
  tests/application/educational_packages/test_ea006_publication.py \
  tests/application/educational_packages/test_pb002_package_selection.py -q
→ 39 passed
```

## Migration Impact

None.

## Architecture Compliance

Presentation and authoring composition only. Layering preserved (templates → presentation → application helpers → package loader/selection). Curriculum V1/V2 untouched. Runtime package selection for session substance unchanged.

## Technical Debt

Legacy sittings without persisted `educational_package_id` and without recoverable sequence package metadata fall back to strategy / syllabus tomorrow language rather than wrong sibling-day package text. New sittings bind package id at session start.

## Known Limitations

- Journey “Up Next” remains syllabus-path projection (not Gate-TP chrome).  
- LIVE chrome honesty verified against delivered package identity (`RO1R1_LIVE_VERIFICATION.md`); harness campaign_day labels may lag ops backdating.  

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

- **Student problem:** Finish/Home could promise the wrong next LO after multi-day shared-topic campaigns.  
- **Student benefit:** Tomorrow Preview matches the approved package handoff the student just completed.  
- **Learning benefit:** Continuity honesty on Gamma (and Alpha/Beta multi-day) paths.  
- **Success metrics:** Finish/Home chrome text equals package `tomorrow_preview.student_facing` (or continuity composition) for CG-D1…CG-R1.  
- **Risks:** Pre-fix open sittings may lack package id until restarted.  
- **Assumptions:** Mission instances continue to carry `educational_package_id` from PB-002 selection.

## Estimated KSI contribution

ΔKSI = 0 (honesty/presentation remediation; no new educational capability). Supports trust hygiene for K8-adjacent claims without claiming KSI movement.

## Evidence collected

- Unit tests: `tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py`  
- Prior residual: `RO001A_EDUCATIONAL_FIDELITY_REPORT.md`, `knowledge/evidence/releases/RO001A/`  
- LIVE re-verify: `RO1R1_LIVE_VERIFICATION.md` / `knowledge/evidence/releases/RO1R1/` (when deployed)

## Lessons learned for student value

Package-path fidelity can PASS while presentation chrome lies. Chrome must bind to package identity, not syllabus leaf code.

## Explainability Review

N/A — no intelligence / recommendation change.

## Recommendation Quality Review

N/A — no ranking change.

## Version 1 readiness residual

RO1-R1 intended to close chrome honesty gate for Wave 1; Wave 2 remains gated until LIVE re-verify PASS.

## CRI domains / ΔCRI

ΔCRI = 0 (presentation honesty; board not updated until LIVE PASS recorded).

---

Signed: RO1-R1 Implementation · 2026-08-01 · Wave 2 not started
