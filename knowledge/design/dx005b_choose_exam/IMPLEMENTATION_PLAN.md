# Implementation Plan

**Programme:** DX-005B  
**Status:** Plan for subsequent UI execution (not executed in DX-005B)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003 / DX-005A  

---

## Scope boundary

| DX-005B (this programme) | Later execution |
|---|---|
| Architecture, wireframe, Ready/Soon, search/filter, scorecard | Templates + CSS + view-model |
| Documentation only | Routes / nav label alignment |
| No application code | Choose Exam discovery UI + Begin Learning → Home |

DX-005B does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts.

---

## Phase 0 — Preconditions

1. Treat `DISCOVERY_ARCHITECTURE.md` + `DISCOVERY_WIREFRAME.md` as binding.  
2. Confirm catalogue projection still supplies Ready / Coming Soon honesty (`SubjectCatalogueService` / support service).  
3. Align Home empty Primary label to **Choose Exam** (DX-005A) when Home UI ships.  
4. Prefer Home UI contracts clear before or tightly coupled with Choose Exam UI so empty/resume/handoff stay coherent.  
5. No curriculum engine / V1–V2 / publication pipeline changes in this UI milestone.

---

## Phase 1 — Content & structure (discovery)

Per DX-003: content and IA before chrome polish.

1. Replace Choose Exam step body (`wizard_step_1.html` or successor) with L0 Ready / L1 controls / L2 metadata / secondary Soon band.  
2. Remove marketing helper essays, duplicated Soon paragraphs, decorative badge chrome, multi-CTA patterns.  
3. Single-select Ready list; **Begin Learning** as sole filled Primary on commitment path.  
4. Coming Soon: secondary band + **Notify when available** (or omit/disabled until backend exists).  
5. Empty: Reason → Return later.  
6. Prefer list pattern over heavy radio cards (B-025).

**Exit:** One question answerable; Ready dominates; Soon cannot Begin.

---

## Phase 2 — Commitment path

1. Collapse or quiet intermediate wizard steps:  
   - Keep exam date / availability if required for Mission creation.  
   - Use quiet **Continue** — not competing Primaries.  
2. Confirm / review: subject + student-set facts only; one line for applied defaults or omit.  
3. Remove twin filled Yes/No; use **Begin Learning** + text **Change selection**.  
4. On success: create Mission / enrol → **`redirect` Home** (canonical student home).  
5. Runtime A Calibration: if still required, keep as brief gate **after** Begin — do not reintroduce discovery theatre; Home remains post-commit OS entry once Calibration completes. Prefer documenting Calibration as Session-prep, not Choose Exam L0.

**Exit:** Begin Learning → Home with Mission ready (or Calibration then Home without returning to Choose Exam as Home).

---

## Phase 3 — View-model

1. Build discovery DTO:  
   - `ready_offerings[]`: id, title, description, scope_label, updated_at, recommended?, selectable  
   - `coming_soon[]`: id, title, notify_available?  
   - `filters`: families, status, sort  
2. Do not send KPI aggregates, readiness %, or recommendation essays.  
3. Preserve fail-closed support gate on POST.  
4. Enrolment-gated Ready: `selectable=false` + quiet prep line.

**Exit:** Template renders without legacy marketing / multi-section review fields.

---

## Phase 4 — Search & filters

1. Implement L1 per `SEARCH_FILTER_SPEC.md`.  
2. Status Ready / Coming Soon / All; Family when data exists; Sort recency / A–Z.  
3. Zero-result: Clear query / Clear filters.  
4. Optional URL presets from Home — still one page.

**Exit:** Search/filter acceptance tests pass.

---

## Phase 5 — Navigation chrome

1. Rename student shell nav **Study Plan** / **Planning** → **Choose Exam**.  
2. Page title **Choose Exam**.  
3. Ensure Choose Exam is not a second Home (no mission hero).  
4. Align product_language / terminology tests.  
5. Update UI Guardian for discovery rules + one Primary + Ready/Soon honesty.

**Exit:** Nav boundaries acceptance tests pass (with DX-005A).

---

## Phase 6 — Premium validation

1. Re-score live UI with `PREMIUM_SCORECARD.md`.  
2. Any dimension ≤8 → redesign before Alpha claim.  
3. Dogfood: select Ready → Begin → land Home with Mission; try Soon → no Begin; empty Ready → Return later only.

**Exit:** Scorecard ≥9/10 live; exit criteria of DX-005B satisfied in product.

---

## Explicit non-goals (execution milestone)

- Founder Subjects redesign (DX-004B)  
- Study Session redesign (DX-005C)  
- Notify backend if not scheduled — honesty over fake  
- Curriculum JSON / V1–V2 engine changes  

---

## Suggested file touch list (execution)

| Area | Likely paths |
|---|---|
| Templates | `study_plan/wizard_step_1.html`, `review.html`, wizard base |
| Routes / forms | `app/study_plan/routes.py`, `forms.py` |
| Catalogue | `subject_catalogue.py`, support gate partial |
| Nav / language | `presentation/student/navigation.py`, `product_language.py` |
| Home empty CTA | `student/home.html` (coordinate DX-005A) |
| CSS | `wizard/wizard.css` or student discovery stylesheet |
| Tests | Wizard / catalogue / terminology / enrolment redirect |

Path list is indicative — implementers follow architecture, not this list as a mandate to expand scope.
