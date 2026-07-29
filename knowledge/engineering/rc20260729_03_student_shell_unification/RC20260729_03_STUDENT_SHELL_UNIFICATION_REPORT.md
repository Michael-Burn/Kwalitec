# RC20260729_03 — STUDENT SHELL UNIFICATION (CQ-008 Remediation)

## Executive Summary

This RC unifies the authenticated Student journey chrome so **Student Home → Choose Exam → Study Session** run inside **one consistent application shell**.

Before this change, the same learning journey could cross shells: Student Home rendered in the EOS (Education OS) student chrome, while Choose Exam could fall back to legacy Learning Workspace chrome when dual-run/`SOLE_RUNTIME` was not enabled. Study Session also used a different shell family.

After this change, the EOS student shell is the single authenticated Student chrome family for the in-scope surfaces (and Session is also routed through the same shell), eliminating visible product-identity and navigation resets between steps.

## Architecture Before

### Shell selection (root cause)
- `Student Home` used `app/templates/student/base.html` → `layouts/eos_student.html` (EOS chrome).
- `Choose Exam` used templates extending `app/templates/layouts/base.html`.
  - When `SOLE_RUNTIME` was falsy, `layouts/base.html` extended `layouts/legacy_workspace.html` → sidebar/topnav legacy chrome.
- `Study Session` used `app/templates/session/base.html` → a dedicated `ds-session-shell` chrome family.

### Result
The learner experienced a shell transition mid-journey (topbar/nav/spacing/footer family reset), which breaks the “one coherent design language” directive.

## Architecture After

### Single authenticated Student shell
- `app/templates/layouts/base.html` now **always** extends `layouts/eos_student.html`.
- `app/templates/session/base.html` now extends `layouts/eos_student.html` so Session chrome matches Home/Choose Exam.
- EOS student shell owns the shared header + navigation + footer, and student navigation is rendered from the canonical `app/templates/student/components/navigation.html`.

### Legacy chrome retired
- Legacy Learning Workspace templates/partials were removed where safe:
  - `layouts/legacy_workspace.html`
  - `partials/sidebar.html`
  - `partials/topnav.html`

## Shells Removed
- `app/templates/layouts/legacy_workspace.html`
- `app/templates/partials/sidebar.html`
- `app/templates/partials/topnav.html`

## Shells Retained
- `app/templates/layouts/eos_student.html` (canonical authenticated Student shell)
- `app/templates/student/components/navigation.html` (canonical Student navigation rendering)
- `app/templates/session/base.html` (kept as the Session template entrypoint, but unified chrome via EOS shell)

## Navigation Changes

### Stabilized navigation across the journey
- Home / Choose Exam / Session now all render inside the EOS header/nav/footer.

### Active-state mapping
- Student nav active state is stabilized for Session routes by mapping Session endpoints to the Home anchor surface (so the nav does not suggest a different “application” stage).

## Files Modified
- `app/templates/layouts/base.html`
- `app/templates/layouts/eos_student.html`
- `app/templates/session/base.html`
- `app/presentation/consolidation.py`
- `app/presentation/student/navigation.py`
- `app/static/css/student/student.css`
- `app/static/css/tokens.css`
- `app/templates/curriculum_studio/dashboard.html` *(comment/invariant reference only)*
- `app/templates/curriculum_studio/workspace.html` *(comment/invariant reference only)*
- `app/settings/routes.py` *(comment-level clarification only)*
- `app/templates/alpha/onboarding.html`

Test + operational invariant updates:
- `tests/presentation/test_dep003_unification.py`
- `tests/test_rc001_accessibility.py`
- `tests/presentation/session/test_accessibility.py`
- `tests/presentation/session/test_templates.py`
- `tests/presentation/student/test_rr002_1_navigation_educational_consistency.py`
- `tests/test_bi001_brand_identity.py`
- `tests/test_iahf004a_brand_infrastructure.py`
- `tests/test_iahf004b_brand_experience.py`
- `tests/test_ptp004_information_architecture.py`
- `tests/test_v1sp001b_operational_fixes.py`
- `tests/operational/helpers.py`

## Files Deleted
- `app/templates/layouts/legacy_workspace.html`
- `app/templates/partials/sidebar.html`
- `app/templates/partials/topnav.html`

## Behaviour Verification

Validated via automated template + journey regression tests:
- **Shell continuity (chrome):**
  - `tests/presentation/test_dep003_unification.py`
  - Ensures Student surfaces include EOS shell markup and do not include legacy sidebar shell markers.
- **Choose Exam form controls preserved:**
  - Confirms wizard renders with the expected form controls inside the unified shell.
- **Canonical journey continuity:**
  - `tests/presentation/test_canonical_journey.py`
  - Includes checks for Session completion returning to Student Home.

## Accessibility
- **RC-001 navigation / shell accessibility markup:**
  - `tests/test_rc001_accessibility.py`
  - Confirms nav toggle scaffolding and required ARIA labeling exist in EOS shell responses.
- **Session template accessibility invariants:**
  - `tests/presentation/session/test_accessibility.py`
  - Confirms session templates still extend the expected base and preserve landmark structure.

## Responsive
- EOS student shell preserves the existing mobile nav toggle pattern (`student-nav-toggle`) and the responsive CSS targets were preserved/standardized in `app/static/css/student/student.css`.
- Operational template/static invariant tests passed after the shell move.

## Guardian (UI Compliance)
- Ensures “one coherent product identity” by routing all in-scope authenticated Student surfaces through the EOS shell (single header/nav/footer family, shared tokens, shared typography).
- Navigation IA is stabilized: no mid-journey transition to legacy sidebar chrome.

## Journey Audit (walk intent)
Automated coverage matched the RC-2026.07.29-03 journey:
- Home → Choose Exam → Study Session transitions do not cross chrome families.
- Session end behavior returns to Student Home.

## Known Issues / Technical Debt
- **Session chrome parity risk:** Session previously had a dedicated `ds-session-shell` header; after unification, the Session header is now the EOS student topbar. Automated tests validate structure/landmarks, but a manual visual QA is recommended for:
  - Exit/secondary action placement consistency
  - Any session-specific styling expectations tied to the retired `ds-session-shell` wrapper.
- **Scope safety risk:** `layouts/base.html` is now unconditional EOS chrome. While the RC targets authenticated Student surfaces, this can affect any template that extends `layouts/base.html`. The automated suites executed here focus on student journey endpoints; additional manual spot-check for other authenticated pages that extend `layouts/base.html` is recommended.

## Recommendation
GO WITH CONDITIONS

Rationale: Automated regression evidence shows in-scope shell continuity and key journey endpoints are stable, but the RC still benefits from a short manual UX walkthrough specifically around Session entry/exit visuals after the wrapper change.

## Tests Executed
- `python3 -m pytest tests/presentation/test_dep003_unification.py -v`
- `python3 -m pytest tests/test_rc001_accessibility.py tests/presentation/session/test_accessibility.py -v`
- `python3 -m pytest tests/operational/test_alpha_assets.py -v`
- `python3 -m pytest tests/presentation/session/test_templates.py -v`
- `python3 -m pytest tests/test_dx006b_choose_exam.py -v`
- `python3 -m pytest tests/presentation/test_canonical_journey.py -v`
- `ruff check app/presentation/consolidation.py app/presentation/student/navigation.py tests/presentation/test_dep003_unification.py tests/test_rc001_accessibility.py tests/operational/helpers.py tests/presentation/session/test_accessibility.py tests/presentation/session/test_templates.py tests/presentation/student/test_rr002_1_navigation_educational_consistency.py tests/test_bi001_brand_identity.py tests/test_iahf004a_brand_infrastructure.py tests/test_iahf004b_brand_experience.py tests/test_ptp004_information_architecture.py tests/test_v1sp001b_operational_fixes.py`

## Migration Impact
None (no Alembic/schema changes in this RC).

## Architecture Compliance
- Layering preserved: this RC is presentation/layout + template wiring only (Student chrome + navigation rendering).
- Curriculum engine, routing permissions, and curriculum data traversal were not part of this RC’s scope.
- V1/V2 curriculum loadability and traversal compatibility: **N/A for this RC** (no curriculum engine changes).

