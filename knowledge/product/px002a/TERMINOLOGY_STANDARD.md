# PX-002A — Terminology Standard

**Programme:** PX-002A — Trust & Friction Resolution
**Purpose:** One name, one action, one workflow — the vocabulary every screen must use. Restates and closes gaps in `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` (the pre-existing canonical guide, updated alongside this programme — see below) with the specific decisions this programme made and enforced in code.

---

## 1. Canonical vocabulary (student-facing)

| Concept | One approved name | Rejected synonyms found in the codebase | Where enforced |
|---|---|---|---|
| Student landing surface | **Home** | Dashboard | `app/domain/student_experience/experience_workspace.py`, `app/presentation/product_language.py`, `app/presentation/student/view_models.py`, `partials/sidebar.html` |
| Study-history / progress-over-time surface | **History** | Analytics | Same as above |
| The focused study workflow | **Session** | Study Session, Learning Session, Mission (as UI label) | `app/presentation/product_language.py:REJECTED_SYNONYMS`, `tests/presentation/student/test_terminology.py` |
| Today's recommended session | **Today's Session** | Today's Mission, Daily Mission | Same |
| Progress through topics toward exam readiness | **Journey** | Roadmap, Progress Path, Learning Path, Curriculum Graph | Same |
| Explainable readiness / progress summaries | **Learning Insights** | Twin Insights, Student Analysis, Digital Twin, Mastery Score | Same |
| Highest-value review work | **Revision** | Remediation, Intervention (learner UI) | Same |
| Readiness toward the exam | **Exam Readiness** | Mastery score, Twin score | Same |
| Destructive-action confirmation | **Styled confirmation modal** (`partials/confirm_modal.html`) | Native browser `confirm()` | `study_plan/view.html`, `study_plan/list.html`, `settings/index.html`, `static/js/confirm-modal.js` |

Rows 3–7 pre-existed this programme (`app/presentation/product_language.py`); rows 1, 2, and 8 are PX-002A additions/corrections.

## 2. What changed and why

### "Home," not "Dashboard" (T1-1)

Both the legacy Learning Workspace home and the canonical Student Experience home rendered the label "Dashboard" — PR-001's single lowest-variance complaint (Navigation, mean 4.60, σ 0.58). "Dashboard" is retired as the label for the canonical home and reserved, if ever needed, for an actual multi-metric overview screen. "Home" is now the one name for "what to do next today."

### "History," not "Analytics" (T1-1, consistency)

The canonical Student Experience's history/progress screen was labelled "Analytics" in the nav while its own page content and route already spoke of study history. "Analytics" is a Founder-facing term (Founder Command Centre nav retains "Analytics" for its own, unrelated systems-analytics screen — that is a different audience and a different concept, not a violation of "one name, one concept"). Student-facing history is now "History" everywhere.

### Canonical guide corrected to match

`knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` §1 already listed **Home** as the approved term, but §4's own nav-label example still said "Dashboard · ... · Analytics" — the guide contradicted itself. Both sections now say **Home · Journey · Revision · History · Settings · Study Plan · Help**, and §1 gained an explicit **History** row. Leaving this uncorrected would have meant the *documentation* — not just the product — disagreed with itself, which is exactly the kind of trust failure this programme exists to close.

### One duration-formatting vocabulary (T1-2)

Prior to this programme, `student/home.html` and `mission/index.html`-adjacent view models each built duration strings independently (e.g. one path could produce "30 minutes," another "90 min," with no shared rounding or phrasing rule). `app/presentation/formatting.py` is now the single place that turns a minute count into student-facing words (`format_minutes`, `format_duration_estimate`, `format_remaining_minutes`), and every touched view model calls into it rather than re-implementing the phrase.

### Confirmation dialogs are one workflow, not two (T2-4)

Destructive confirmation previously had two implementations: the app's own styled Bootstrap modal (already used for the welcome modal) for nothing destructive, and the browser's native `confirm()` for the two highest-stakes actions in the product (plan archive/delete, backup restore). There is now exactly one confirmation workflow (`confirm_modal.html` + `confirm-modal.js`), reused by both call sites.

## 3. Legacy exceptions (explicitly not silently renamed)

- The **legacy** Learning Workspace home (`dashboard/index.html`) still says "Dashboard." T1-4 confirms production (`SOLE_RUNTIME=1`) never serves this screen to a real student; renaming a screen that PX-001 itself treats as being phased out was judged out of this programme's scope (see `FRICTION_RESOLUTION_MATRIX.md` T1-1).
- `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` §9 already documents that "Older Mission / Dashboard templates may still show **Study Session** in places owned by pre-V2 flows" — this programme did not attempt to migrate pre-V2 flows; it fixed the specific "study session" occurrences PX-001 found on the **canonical** `student/home.html` empty state and in `readiness_quality.py` / `recommendation_quality.py` review-point copy, all of which are canonical (not legacy pre-V2) surfaces.

## 4. Enforcement

Presentation tests assert the approved labels and forbid rejected synonyms on student-facing routes:

- `tests/presentation/student/test_navigation.py`, `test_routes.py`, `test_view_models.py`, `test_terminology.py`
- `tests/presentation/workflows/test_workflow_consistency.py`, `test_workflow_student_session.py`
- `tests/application/unified_journey/test_navigation.py`, `test_feature_flags.py`

Per `PRODUCT_LANGUAGE_GUIDE.md` §7's own naming checklist, any future new user-visible concept should add a row to §1 of that guide and a presentation test in the same change — this programme followed that existing convention rather than introducing a new one.
