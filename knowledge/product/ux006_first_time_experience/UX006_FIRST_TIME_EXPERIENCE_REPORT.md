# UX-006 — First-Time Experience & Founder Polish Report

**Programme:** Premium Product Experience  
**Status:** Complete (presentation + catalogue-membership pass)  
**Date:** 2026-07-29  
**Scope:** Refine Founder Console and Student Experience for first-time clarity, presentation, and information hierarchy before Founder Validation. No learning-algorithm, recommendation-engine, curriculum-traversal, or routing changes. No placeholder curriculum data.

---

## Summary

UX-006 makes an empty product feel intentional. Founder branding no longer duplicates the wordmark beside a white-on-light logo; the approved logo sits on a navy plate with a subtle Founder context badge. Founder Home empty state now explains the first curriculum step. Choose Exam no longer surfaces legacy on-disk IFoA V1 artefacts when published-subject discovery is enabled — students see only the founder-published catalogue (or a clear empty state). Settings answers “how does Kwalitec work for me?” instead of stacking performance KPIs. The Student topbar uses a compact appearance cycle control. Light Mode label contrast, footer chrome, Student OS content width, and empty-state craft were standardised across Founder and Student surfaces.

---

## Issues addressed

| # | Issue | Resolution |
|---|--------|------------|
| 1 | Logo low contrast in Light Mode; “Kwalitec” + “Kwalitec Console” duplication | Navy brand plate behind approved logo; removed sidebar wordmark; Founder badge + browser title retain Console context |
| 2 | Generic Founder Home empty (“No publication work in progress.”) | First-time hierarchy: title, explanation, Create Subject, helpful context |
| 3 | Legacy V1 exams in Choose Exam with no founder subjects | When discovery is on, catalogue is published-only; empty copy + Go to Founder Console |
| 4 | Settings KPI overload | Removed Overview KPI strip; intro points progress to History; Appearance is its own group |
| 5 | Wide Appearance Light/Dark/System chrome | Compact cycle button in Student topbar; full three-option control retained in Settings |
| 6 | Soft Light Mode labels | Darkened `--text-muted` / `--text-secondary`; section labels and meta use secondary |
| 7 | Tall Student footer | Reduced vertical padding; thesis retained |
| 8 | Narrow Student OS column on desktop | `--student-max-width` 48rem; large-desktop cap 60rem |
| 9 | Inconsistent empty states | `ds_empty_operational` supports title / explanation / context / primary action |
| 10 | Visual consistency across shells | Token + empty + appearance alignment across Founder / Student / Light / Dark |

---

## Screens updated

| Surface | Change |
|---------|--------|
| Founder Console sidebar / mobile topbar | Logo-only brand + Founder badge; no duplicated Console wordmark |
| Founder Home (empty) | First-time Create Subject experience |
| Choose Exam (empty catalogue) | “No exams are available yet.” + explanation + Founder Console CTA |
| Student Home / Journey / History / Revision empties | Standardised `ds_empty_operational` craft |
| Student Settings | Configuration-first hub; KPIs removed |
| Student topbar | Compact appearance cycle (no Appearance label) |
| Student footer | More compact |
| Student OS content column | Slightly wider on desktop |

---

## Files modified

### Presentation / templates
- `app/founder/dashboard/templates/founder_dashboard/_sidebar.html`
- `app/founder/dashboard/templates/founder_dashboard/overview.html`
- `app/templates/layouts/console_base.html`
- `app/templates/layouts/eos_student.html`
- `app/templates/partials/appearance_switcher.html`
- `app/templates/design_system/macros.html`
- `app/templates/study_plan/wizard_step_1.html`
- `app/templates/student/profile.html`
- `app/templates/student/home.html`
- `app/templates/student/journey.html`
- `app/templates/student/history.html`
- `app/templates/student/revision.html`

### Services / DTOs (presentation + catalogue membership only)
- `app/founder/dashboard/services/founder_home_service.py`
- `app/founder/dashboard/dto/founder_home.py`
- `app/presentation/student/dto/choose_exam.py`
- `app/application/platform_integration/discovery.py`
- `app/application/platform_integration/subject_catalogue.py`

### Theme / CSS / JS
- `app/static/js/theme.js`
- `app/static/css/tokens.css`
- `app/static/css/app.css`
- `app/static/css/student/student.css`
- `app/static/css/design_system.css`
- `app/founder/dashboard/static/css/founder_dashboard.css`

### Tests
- `tests/test_px002_product_experience.py`
- `tests/test_dx006b_founder_home.py`
- `tests/test_console_001_kwalitec_console.py`
- `tests/test_theme_system.py`
- `tests/presentation/student/test_templates.py`

### Created
- `knowledge/product/ux006_first_time_experience/UX006_FIRST_TIME_EXPERIENCE_REPORT.md`

---

## Legacy exam investigation

### Root cause

Choose Exam was not “broken” — it was merging two independent sources:

1. **Static examination catalogue** (`examination_catalogue.get_categories()`) — IFoA, CFA, ACCA, …
2. **On-disk V1 curricula** — `app/curriculum/data/ifoa/{cs1,cm1,cb2}/2026.json` make those papers `SupportStatus.SUPPORTED` / Ready
3. **Founder Published category** — additive via `PublishedSubjectDiscoveryService`, not exclusive

So with zero founder-created subjects, CS1 / CM1 / CB2 still appeared as selectable Ready exams.

### Fix (UX-006)

When `ENABLE_PUBLISHED_SUBJECT_DISCOVERY` is on (development default and Founder Validation bridge):

- `augmented_categories()` returns **only** the Published category
- `SubjectCatalogueService.list_entries()` skips non-Published categories

Result:

- No published subjects → zero selectable exams → empty state
- After create → publish → available → only those subjects appear

When discovery is **off** (safe production default / test harness `APP_ENV=testing`), the legacy Runtime A catalogue path is unchanged — curriculum engines and on-disk JSON were not deleted or altered.

### Educational logic untouched

No changes to recommendation engines, planning math, curriculum traversal, or JSON syllabus content. Catalogue membership for student discovery is a presentation/bridge policy change only.

---

## Theme refinements

| Token / control | Before | After |
|-----------------|--------|-------|
| Light `--text-secondary` | `#4a5568` | `#3d4654` |
| Light `--text-muted` | `#5c6570` | `#4a5568` |
| Student topbar appearance | Label + 3 buttons | Compact cycle (icon + current mode) |
| Settings appearance | Inside Learning | Dedicated Appearance group (full 3-option control) |
| Founder logo field | Bare on white surface | Navy chrome plate (approved white wordmark remains visible) |
| Student footer padding | `--student-space-5` | `--student-space-3` vertical |
| Student content width | 44rem → 56rem @1280 | 48rem → 60rem @1280 |

Saved preference key remains `kwalitec-appearance`. Cycle order: Light → Dark → System → Light. Keyboard: focusable button; `aria-label` announces current mode.

---

## Accessibility improvements

- Logo remains approved PNG (no filters); contrast restored via dark brand plate rather than recolouring the asset
- Appearance cycle keeps accessible name (“Appearance: Light. Activate to switch.”) and touch-target min height
- Full three-option switcher retained in Settings for explicit selection
- Section / meta labels moved toward `--text-secondary` for Light Mode readability while staying visually secondary to body/title text
- Empty states use `role="status"` with clear title + explanation + single primary

---

## Empty-state review

| Surface | Title | Primary action |
|---------|-------|----------------|
| Founder Home | No subjects have been created yet. | Create Subject |
| Choose Exam (empty catalogue) | No exams are available yet. | Go to Founder Console |
| Student Home (no exam) | Existing empty reason | Choose Exam |
| Journey | Your journey will take shape after your first session | Go to Home |
| History | Your history starts with your first session / No sessions yet | Go to Home |
| Revision | No revision support yet / Revision opens after practice | Return to today's Mission |

Shared contract via `ds_empty_operational(title, explanation, context, action)`:

1. Clear title  
2. Short explanation  
3. Single primary action  
4. Helpful context line  
5. Consistent spacing / surface treatment  

---

## Remaining technical debt

1. **Approved logo is white-wordmark only** — Light Mode shells without a navy plate still need a dark-field treatment; a dedicated light-surface approved master would be cleaner long-term (brand pack constraint: do not invent SVG wordmarks).
2. **Auth / public footers** still use the three-button appearance control — intentional; only Student topbar was compacted.
3. **Choose Exam empty CTA** always points to Founder Console — correct for Founder Validation; pure students without Console access may need a softer secondary later.
4. **Legacy KPI CSS** (`.settings-kpi-*`) remains unused in CSS — safe to delete in a cleanup pass.
5. **Parallel empty patterns** (`educational_empty` vs `ds_empty_operational`) still coexist on older surfaces outside SOP-001 pages.
6. Pre-existing `test_founder_hubs_render` expects 200 on redirected Studio hub presets (`/console/studio/review-queue` → 302) — unrelated to UX-006.

---

## Recommendations

1. Capture Founder Validation screenshots (Founder Light/Dark, Student Home/Journey/History/Revision/Settings, Choose Exam empty) into `knowledge/evidence/releases/` once the founder walks the empty path.
2. After first subject publish, confirm Choose Exam shows only that subject and enrolment still routes correctly.
3. Consider a brand-approved dark-text logo master for future light chrome that cannot use a navy plate.
4. When production enables the Founder→Student bridge, keep published-only catalogue policy on — do not re-merge legacy on-disk Ready papers into student discovery.

---

## Testing

### Automated

```bash
python3 -m pytest \
  tests/test_px002_product_experience.py::TestSubjectCatalogue \
  tests/test_dx006b_founder_home.py \
  tests/test_console_001_kwalitec_console.py::TestConsoleRouting::test_console_home_renders \
  tests/test_theme_system.py::TestThemeSurface::test_dashboard_includes_theme_bootstrap_and_switcher \
  tests/presentation/student/test_templates.py::test_settings_hub_groups_present \
  tests/application/platform_integration/test_subject_catalogue.py \
  tests/test_dx006b_choose_exam.py \
  tests/test_smoke.py::TestSmokeStudyPlanWizard \
  -q
```

Outcome: targeted suite green (catalogue, Founder Home, Console home, theme cycle, Settings hub, published discovery, Choose Exam, smoke wizard).

`ruff check` on touched Python modules: pass.

### Manual checklist (Founder Validation)

- [ ] Founder Light — logo visible; no duplicated “Kwalitec Console” beside logo
- [ ] Founder Dark — brand plate / logo readable
- [ ] Founder Home empty — first-step copy + Create Subject
- [ ] Student Home / Journey / History / Revision — empty craft consistent
- [ ] Settings — no KPI wall; History link for progress
- [ ] Appearance cycle — Light → Dark → System; preference persists
- [ ] Choose Exam with no published subjects — empty; no CS1/CM1/CB2
- [ ] No console errors / CSS regressions

---

## Success criteria

| Criterion | Status |
|-----------|--------|
| Founder branding simplified | ✓ |
| Logo clearly visible in Light Mode | ✓ (navy plate) |
| No duplicated branding | ✓ |
| Founder Home first step clear | ✓ |
| Legacy exams hidden without published content (discovery on) | ✓ |
| Settings hierarchy improved | ✓ |
| Appearance control compact | ✓ |
| Light Mode label contrast stronger | ✓ |
| Footer more compact | ✓ |
| Student pages use desktop space better | ✓ |
| Empty states consistent | ✓ |
| Ready for Founder Validation | ✓ |

---

## Architecture compliance

- Layering preserved: templates → presentation/services → catalogue discovery; no business math in routes
- Curriculum V1/V2 on-disk engines untouched and still loadable
- Application code for learning/recommendation/routing not modified
- Catalogue change is discovery membership only when the Founder→Student bridge is enabled
