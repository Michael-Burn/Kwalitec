# FV-002 — End-to-End Founder Dogfood Report

**Programme:** Founder Validation  
**Status:** P0 Integration Validation  
**Host:** local `http://127.0.0.1:5056` (Waitress)  
**Baseline commit:** `6abacdd7d14176a0ada980bf08ea8595295c7b2f`  
**Subject:** CS1 — Actuarial Statistics (canonical code, not synthetic)  
**Sources:** ActEd CS1 CMP 2019 PDF + CS1 Syllabus 2026 PDF (operator Downloads)  
**Workspace:** `ws-cs1` · package `CS1` / `2026.1`  
**Date:** 2026-07-29 / 2026-07-30 (UTC)

---

## Executive Summary

The Founder → Student educational publishing pipeline was executed end-to-end against real CS1 documents. After bounded-context recovery and publication-integrity fixes, a Student enrolled via **Begin Learning**, received a Runtime C mission, and completed that mission from Student Home (progress advanced Topic 1 → Topic 2).

**FINAL DECISION: END-TO-END PIPELINE CERTIFIED**

Certification is for pipeline connectivity and lawful publish→enrol→mission write-back. CIP structure quality remains noisy (thousands of extracted “topics”); that is tracked as outstanding educational-quality debt, not a pipeline blocker.

---

## Complete workflow timeline

| Stage | Result | Notes |
|-------|--------|-------|
| Founder login | Pass | Local admin via `.env` / `flask sync-admin` |
| Experience → Founder Console | Pass | |
| Create Subject CS1 + `ws-cs1` | Pass | Resumed durable workspace; no synthetic code |
| Upload Syllabus | Pass | CIP Ready |
| Upload CMP | Pass | Required `data-doc-kind="cmp"` file input (UI binding pitfall) |
| Processing (CIP) | Pass after recovery | CMP job stuck `queued` after SQLite lock; recovered via `PipelineCoordinator.run_job` |
| Validate / Preview / Approve / Publish | Pass | Authenticated HTTP POSTs after Management rehydration |
| Founder Home ↔ Publications agree | Pass | Settled copy when publications exist |
| Student Discovery | Pass | `Published:CS1` · edition `2026.1` Ready |
| Choose Exam → wizard → review | Pass | |
| Begin Learning | Pass | Flash: enrolled `CS1:2026.1` (Runtime C) |
| Mission available | Pass | After Home `complete_runtime_c` wiring |
| Learning loop write-back | Pass | Mark mission complete → Topic 2 · 1 complete |

Evidence: `knowledge/evidence/releases/FV002/` (screenshots + `student_evidence.json`).

---

## Every defect discovered

1. **Management vs durable Studio after restart** — Curriculum Management is in-memory; workspace projections are durable. After Flask restart, CS1/`version-1` vanished → validate/publish `empty_package`.
2. **Founder Home empty vs Recent Publications** — Empty CTA (“No subjects have been created yet”) while Recent Publications listed CS1.
3. **CMP upload UI binding** — First “upload” only bound the wrong file input; required `article[data-doc-kind="cmp"]`.
4. **CIP job stuck queued** — SQLite lock + concurrent polls interrupted auto-run; `retry` only for failed/cancelled.
5. **Objective IDs not unique in published structure** — Structure prep used objective titles as IDs and collapsed objectives under one topic → `learning_objective_refs must be unique` on derive.
6. **Publish INSERT uniqueness** — Republish of same `subject_code`+`version_label` failed UNIQUE on `published_curriculum_packages`.
7. **Runtime C mission invisible on Student Home** — Educational VM set `session_control=complete_runtime_c`, but Home selection only recognised `start`/`resume` → quiet “session will be ready…” despite an open mission.

---

## Root cause analysis

| Defect | Root cause |
|--------|------------|
| Restart empty package | Bounded-context split: Management not rehydrated from durable Studio/Foundation facts |
| Home empty CTA | `FounderHomeService` treated missing `current_work` as first-time empty even when `recent_publications` non-empty |
| Derive uniqueness | CIP entity IDs ignored; titles reused; `structure_dict` flattened objectives |
| Republish UNIQUE | `publish_curriculum` always INSERT after deactivate-active |
| Quiet Home with mission | SOP-001 `_select_mission` unaware of PR-001B Runtime C control |

---

## Fixes applied

| Fix | Location |
|-----|----------|
| Management reconciliation after restart (subject, stable version, asset refs) | `app/application/curriculum_studio/management_reconciliation_service.py` + Studio service/factory/validation/publication/upload hooks |
| Founder Home settled state when publications exist | `app/founder/dashboard/services/founder_home_service.py` |
| Structure prep: entity IDs, parent topic refs, unique objectives | `app/application/curriculum_studio/structure_preparation_service.py` |
| Publication bridge always rebuilds structure on publish | `app/application/platform_integration/publication_bridge.py` |
| Foundation publish upsert by subject+version_label | `app/application/curriculum_studio_foundation/service.py` |
| Student Home actionable `complete_runtime_c` + complete form | `student_home_service.py`, `home.html`, `routes.py` |

Tests: `tests/application/curriculum_studio/test_management_reconciliation.py`, `tests/test_dx006b_founder_home.py`, `tests/test_dx006b_student_home.py` (incl. Runtime C mission control).

---

## Regression checks

- `pytest tests/test_dx006b_student_home.py tests/application/curriculum_studio/test_management_reconciliation.py` — pass
- Management reconcile on Studio boot / get_workspace — log: `Management reconciled workspace=ws-cs1 … assets_restored=True`
- Active package derive after upsert republish — `DERIVE OK 1931 5024 21`

---

## Publication integrity verification

| Check | Result |
|-------|--------|
| Active package `CS1` / `2026.1` | Yes |
| Structure non-empty sections/topics/objectives | 1931 / 5024 / 21 |
| Unique `objective_id`s | 21 / 21 |
| `EducationalArtefactDeriver.derive` | Pass |
| Lawful upsert republish (no raw SQL package rewrite) | Pass |

---

## Founder verification

- Console Home: settled (“No curriculum work needs attention”) + **Recent Publications → CS1**
- Subjects / Studio links resolve to CS1 workspace
- Post-restart reconciliation restores Management subject/version/assets so Validate/Publish remain lawful

---

## Student verification

- Discovery lists **CS1 · 2026.1** Ready (`Published:CS1`)
- Choose Exam → date → availability → review → **Begin Learning**
- Enrolment flash: `Enrolled in published curriculum CS1:2026.1 (Runtime C)`
- Student Home shows Current Examination **CS1** with syllabus position

---

## Study Plan verification

- Wizard step 1 selection enables Continue only after `subject_key` radio
- Exam date 2027-04-15; weekday 60 / weekend 120 / session 60
- Review confirms CS1 before Begin Learning
- Runtime study plan instance created (`curriculum_identity=CS1:2026.1`, status active)

---

## Mission verification

- Runtime mission instance generated for today (`status=generated`, then completable)
- After Home fix: primary CTA **Mark mission complete** (not quiet empty)
- POST `/student/mission/complete` succeeds

---

## Learning session verification

Runtime C pilot loop (not Runtime A Guided Session):

1. Begin Learning creates enrolment + plan + mission authority  
2. Home presents today’s mission with PR-001B complete control  
3. Completing the mission advances journey (**Topic 1 → Topic 2 · 1 complete**) with flash confirming mission complete  

This satisfies “learning session starts” for the published Runtime C path: the student can enter and close the daily study loop on the founder-published package.

---

## Outstanding issues

1. **CIP structure noise** — ~5024 topics / 1931 sections; first topic title “Associateship Qualification” (front-matter). Educational usefulness is weak; pipeline integrity holds.
2. **Student Home latency** — `/student/` ~5s under local SQLite with large artefact sets.
3. **SQLite locking** under concurrent CIP + status polls — operational hazard for large CMP jobs; Waitress helps but does not eliminate.
4. **Live Waitress process** may need restart to pick up Student Home template/service changes (verified via Flask test client with fresh app load).

---

## Recommendations

1. Tighten CIP → structure filters (syllabus LO entities only; drop TOC/front-matter topics) before claiming educational quality for CS1.
2. Keep Management reconciliation as permanent restart recovery (Choice A) — do not treat missing Management objects as one-off patches.
3. Prefer upsert semantics for republish of the same edition label.
4. Add an integration test: publish package → Begin Learning → Home shows `complete_runtime_c` → complete advances topic index.
5. For production dogfood, restart the web process after deploying these fixes; re-verify Home CTA in browser.

---

## Summary (completion reporting)

What was delivered: autonomous FV-002 dogfood of real CS1 CMP+syllabus through Publish and Begin Learning, plus recovery/integrity/Home fixes so Founder and Student read models agree and the Runtime C mission loop is actionable.

### Files Created

- `app/application/curriculum_studio/management_reconciliation_service.py`
- `tests/application/curriculum_studio/test_management_reconciliation.py`
- `knowledge/engineering/fv002_end_to_end_founder_dogfood/` (workflow log, scripts, this report)
- `knowledge/evidence/releases/FV002/` (screenshots, evidence JSON)

### Files Modified

- Curriculum Studio services (structure prep, validation, publication, document upload, studio service, factory)
- `publication_bridge.py`, `curriculum_studio_foundation/service.py`
- `founder_home_service.py` + founder home tests
- Student Home service/routes/template/DTO + student home tests

### Tests Executed

- `pytest tests/test_dx006b_student_home.py tests/application/curriculum_studio/test_management_reconciliation.py` — pass  
- Flask test-client dogfood: Begin Learning enrolment (prior), Home Mark mission complete, mission complete write-back — pass  
- Package derive verification — pass  

### Migration Impact

None.

### Architecture Compliance

- Layering preserved (presentation → application → domain/engine).  
- Curriculum V1/V2 JSON import path unchanged; discovery flag keeps unpublished seed curricula off Choose Exam.  
- Management reconciliation restores in-memory Management from durable Studio facts without inventing curriculum content.  
- Runtime C remains the enrolment path for founder-published subjects.

### Technical Debt

CIP over-segmentation (~5k topics); Home slow on large packages; SQLite concurrency during CIP.

### Known Limitations

Certification does not claim Exam-Ready educational quality of the CS1 CIP extract—only that the publish→discover→enrol→mission pipeline works on the real documents.

### Student Impact Assessment

- **Problem:** Founders could not lawfully publish real docs into a student-ready catalogue after restarts; students hit derive/Home dead-ends.  
- **Benefit:** Student can choose published CS1 and enter the daily mission loop.  
- **Learning benefit:** Progress write-back works; topic titles/order need CIP quality work before high educational value.  
- **Success metrics:** Begin Learning success; mission complete advances position; surfaces agree on CS1 `2026.1`.  
- **Risks:** Noisy syllabus order may confuse learners.  
- **Assumptions:** Runtime C enrolment flags remain on for published subjects.

### Estimated KSI contribution

Provisional ΔKSI ≈ 0 for product scores (integration validation; not a scored K-category lift). Pipeline risk reduced for K2/K8 delivery paths.

### Evidence collected

- `knowledge/evidence/releases/FV002/`  
- Local package row `CS1`/`2026.1` active; derive OK  
- Test-client Home + mission complete transcript (this dogfood)

### Lessons learned for student value

Publication without unique structure IDs and without Home wiring for Runtime C produces a false “published” state students cannot study. Recovery must reconcile bounded contexts, not only insert missing rows.

### Explainability Review

N/A for new recommendation algorithms; mission rationale comes from existing EQ-001 envelopes. No K8 claim.

### Recommendation Quality Review

N/A for ranking changes; Runtime C next-topic order is syllabus order. No K2 claim.

### Version 1 readiness residual

Does not close G1–G12; reduces founder-validation residual for publish→learn. Residual: CIP quality, production dogfood on Render with restarted workers.

### CRI domains improved

CR (founder publish / student activation) operational risk reduced; **ΔCRI = 0** (provisional dogfood, not board update).

### Estimated CRI delta

0 (provisional).

### Evidence supporting the increase

N/A (ΔCRI 0).

### Remaining blockers

Educational quality of CIP-derived CS1 structure (not pipeline connectivity).

### Provisional or validated

**Provisional certification** of the end-to-end pipeline on local Waitress with the fixes above. Production re-verification after deploy/restart recommended.

---

## FINAL DECISION

# END-TO-END PIPELINE CERTIFIED
