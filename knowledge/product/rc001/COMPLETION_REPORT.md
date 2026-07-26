# RC-001 — Release Candidate Hardening — Completion Report

**Programme:** RC-001 — Release Candidate Hardening
**Status:** Complete
**Purpose:** Resolve every verified release blocker from PX-003 (`knowledge/product/px003/RELEASE_BLOCKERS.md`, treated as authoritative and not challenged, per programme instructions).

---

## Summary

All ten PX-003 release blockers (B1-B10) are resolved with cited code changes, dedicated regression tests, and live/automated evidence. No blocker was marked resolved on inspection alone, per the programme's validation requirement.

- **B1** — the Reflection screen's "stays with your session record" promise is now true: the note is persisted via a new `SessionRuntimePort.record_reflection_note` method into the same `SessionDocumentStore`/`NS_REFLECTION` namespace every other reflection fact already uses.
- **B2** — Profile's "Current Examination" now reads from the same `StudyPlanService.get_user_active_plan` source as Dashboard/Study Plan/Settings, resolved in the presentation layer to respect the application layer's architectural-independence boundary.
- **B3** — Mission's duration is now resolved once, via the same `mission_date`-aware resolver Home and Session already use, replacing a duplicated template-local fallback chain.
- **B4** — the Welcome modal now has real focus entry/trap/return, Escape dismissal, and `aria-describedby`; the script implementing this now actually loads on the canonical Student shell that renders the dialog (it previously didn't).
- **B5** — the mobile navigation drawer now has `aria-expanded`/`aria-controls`, a focus trap, and focus return to the toggle — verified live via Playwright keyboard simulation, not just static markup inspection.
- **B6** — the sidebar section-label contrast failure (3.21:1) is fixed to 5.18:1, comfortably clearing WCAG AA's 4.5:1; every other sidebar token was also measured and locked in with regression tests.
- **B7** — 162 screenshots now exist across all 9 required breakpoints (there were previously zero anywhere in the repository); one of PX-003's two named "plausible but unconfirmed" mobile defect candidates (the appearance-switcher touch target) was confirmed real via live measurement and fixed; the other (`.mission-grid` at 320px) was tested and found not to reproduce.
- **B8** — onboarding is now guaranteed at login, checked before the study-plan-wizard branch, so there is exactly one onboarding decision regardless of entry path.
- **B9** — the legacy `/settings/` index now redirects to canonical Student Profile under `SOLE_RUNTIME=1`, matching the same pattern already used by Dashboard/Analytics/Mission.
- **B10** — "Internal Alpha" / "Learning profile status" language is removed from the one page any authenticated student (not just alpha testers) could reach; raw engineering-flag fields were removed rather than relabelled, since they have no honest student-facing equivalent.

Full per-blocker detail (Issue/Cause/Implementation/Evidence/Tests/Screens/Risk/Status) is in `BLOCKER_RESOLUTION_MATRIX.md`.

---

## Files Created

**Programme documentation (`knowledge/product/rc001/`):**
- `BLOCKER_RESOLUTION_MATRIX.md`
- `RESPONSIVE_VALIDATION.md`
- `ACCESSIBILITY_VALIDATION.md`
- `SCREENSHOT_INDEX.md`
- `RELEASE_EVIDENCE.md`
- `FINAL_RENDER_CHECKLIST.md`
- `COMPLETION_REPORT.md` (this file)
- `screens/` — 162 PNG screenshots (see `SCREENSHOT_INDEX.md` for the complete, categorised list)

**Evidence-capture tooling (`knowledge/product/rc001/_evidence/`, not application code):**
- `seed_rc001.py` — seeds an isolated SQLite database with real curriculum data and three test accounts (full-data, empty-state, onboarding-eligible)
- `capture_rc001.py` — Playwright capture across 9 breakpoints for all static student-facing screens, plus live B4/B5/B8/B9/B10 behavioural checks
- `capture_session_flow.py` — Playwright capture of the Session flow (Overview/Activity/Reflection/Summary) via Flask's test client + `FakeActivityEnginePort`, across all 9 breakpoints
- `capture_dark_mode.py` — dark/light theme screenshot pairs
- `results.json` — machine-readable evidence output from the above scripts

**New test files:**
- `tests/presentation/test_canonical_journey.py` — B3, B8, B9 regression coverage (10 tests)
- `tests/test_rc001_accessibility.py` — B5, B7 touch-target regression coverage (3 tests)
- `tests/test_rc001_contrast.py` — B6 contrast-ratio regression coverage (6 tests)

## Files Modified

**Application code:**
- `app/application/session_experience/facade.py` — B1: `continue_from_reflection(..., note=None)` parameter threading
- `app/application/session_experience/ports/session_runtime_port.py` — B1: new `record_reflection_note` port method
- `app/application/session_experience/reflection_service.py` — B1: persists the note before advancing to Summary
- `app/infrastructure/session/defaults.py` — B1: `student_note` key added to the default reflection shape
- `app/infrastructure/session/runtime_adapter.py` — B1: `record_reflection_note` implementation
- `app/presentation/session/routes.py` — B1: passes `form.reflection_note.data` through
- `app/presentation/session/views.py` — B1: `continue_reflection(..., note=None)` parameter threading
- `app/presentation/student/view_models.py` — B2: `_authoritative_examination_label`; B9: `primary_cta_endpoint` updated
- `app/auth/routes.py` — B8: onboarding-gate check added before the study-plan-wizard branch
- `app/settings/routes.py` — B9: `redirect_if_sole_runtime` guard on `index()`; B10: "Account Status" title/label
- `app/static/css/app.css` — B6: `.nav-section-label` contrast fix; B4: focus-visible outline on the welcome card; B7: appearance-switcher touch-target fix
- `app/static/js/app.js` — B4: focus trap/entry/return utilities and welcome-modal wiring; B5: drawer ARIA state + focus trap/return
- `app/templates/mission/index.html` — B3: single `estimated_minutes` value via `format_minutes`, template fallback chain removed
- `app/templates/partials/welcome_modal.html` — B4: `tabindex="-1"`, `aria-describedby`, `id`s for the described paragraphs
- `app/templates/settings/index.html` — B10: "Account Status" section/label rename; internal build-flag fields removed
- `app/templates/student/base.html` — B4: `app.js` now loaded on the canonical Student shell

  *Note on shared files:* `app/mission/routes.py` and `app/templates/settings/index.html` contained substantial pre-existing, uncommitted work from other, unrelated in-flight programmes (e.g. recommendation-coherence/commitment-echo logic, an icon-macro/appearance-switcher-macro extraction) already present in the working tree before RC-001 began. Only the specific hunks cited in `BLOCKER_RESOLUTION_MATRIX.md` (marked inline with `B3 (PX-003)` / `B10 (PX-003)` code comments) are RC-001's contribution to these two files; the rest of each file's diff predates and is unrelated to this programme.

**Test files (existing files, new test cases added):**
- `tests/presentation/session/test_routes.py` — B1: `test_reflection_note_is_persisted_via_runtime_port`
- `tests/presentation/student/test_accessibility.py` — B4: `TestWelcomeModalOnCanonicalStudentHome` (2 tests)
- `tests/presentation/student/test_view_models.py` — B2: `test_profile_vm_examination_label_agrees_with_active_study_plan`, `test_profile_vm_falls_back_when_no_active_plan_or_non_numeric_id`

## Tests Executed

- **RC-001-specific regression suite:** `python -m pytest tests/presentation/test_canonical_journey.py tests/presentation/student/test_accessibility.py tests/test_rc001_accessibility.py tests/test_rc001_contrast.py tests/presentation/session/test_routes.py tests/presentation/student/test_view_models.py -q` → **100 passed, 0 failed**.
- **Full repository suite:** `python -m pytest tests/ -q` → 42,896 passed, 265 failed, 7 skipped. All 265 failures were individually investigated and traced to three pre-existing, out-of-scope root causes (Alembic dual migration heads from unrelated uncommitted work; a pre-existing `/dashboard/` legacy-route redirect; a pre-existing feature-flag posture mismatch in `test_v2_flags.py`) — none are regressions introduced by RC-001. Full investigation and spot-check evidence: `RELEASE_EVIDENCE.md` §3.
- **Static analysis:** `ruff check` on every file RC-001 touched → 3 pre-existing findings, all on lines outside RC-001's edited hunks in `app/settings/routes.py`; zero new findings introduced. Full detail: `RELEASE_EVIDENCE.md` §4.
- **Live browser evidence:** Playwright-driven keyboard/focus/ARIA-state checks for B4/B5, redirect verification for B9, content verification for B10, onboarding-landing verification for B8, and horizontal-overflow measurement across all 144 screen×breakpoint combinations for B7 — all captured in `knowledge/product/rc001/_evidence/results.json` and referenced throughout `BLOCKER_RESOLUTION_MATRIX.md`.

## Migration Impact

**None.** No Alembic migration was added or changed by this programme. B1's persistence reuses the existing `SessionDocumentStore`/`NS_REFLECTION` namespace and schema; no new table, column, or document shape was introduced.

*(Separately, and explicitly out of RC-001's scope: the working tree already contains an unrelated, untracked migration file — `migrations/versions/202607260001_create_recommendation_commitments.py` — from other in-flight work, which creates a dual-head condition. This predates RC-001, is not touched by it, and is called out in `RELEASE_EVIDENCE.md` and `FINAL_RENDER_CHECKLIST.md` as an item that must be resolved by whoever owns that other work before its own deployment — not an RC-001 deliverable gap.)*

## Architecture Compliance

- **Layering preserved.** All fixes stayed within their correct layer: B1's persistence logic lives in the application layer (`ReflectionService`) calling through a port (`SessionRuntimePort`) to an infrastructure adapter (`SessionRuntimeAdapter`) — no route contains persistence logic. B2's fix was deliberately placed in the **presentation** layer (`view_models.py`), not the application layer, specifically because an initial attempt to resolve it in `app/application/student_experience/profile_service.py` violated `tests/application/student_experience/test_independence.py::test_application_no_forbidden_imports` (the application layer must not import `app/services/`). This is documented as a design decision, not a workaround.
- **Curriculum V1/V2 invariants:** untouched. No blocker required any curriculum-ordering or engine change; B3's duration fix touches only session/mission duration resolution, not curriculum traversal.
- **No Runtime A redesign, no opportunistic refactor.** Every change above is the smallest change that makes its specific blocker's claim true — confirmed by the file-level diffs cited in `BLOCKER_RESOLUTION_MATRIX.md`. The one exception considered and rejected was fixing the pre-existing Alembic dual-head condition found during test investigation; this was explicitly left untouched as outside RC-001's chartered scope.
- **Composition root / DI unaffected.** No new adapters or services were registered; `record_reflection_note` extends an existing port interface implemented by the existing `SessionRuntimeAdapter` singleton wiring.

## Technical Debt

- The pre-existing Alembic dual-migration-head condition (§ Migration Impact) will continue to cause `no such table` failures for any test requiring a fresh-migrated database until it is merged by whoever owns the unrelated work that introduced it.
- The pre-existing `/dashboard/` legacy-route 302 behaviour (`RELEASE_EVIDENCE.md` §3b) remains unresolved; RC-001's B5/B9 fixes route around it (using `/settings/profile` for B5's test target) rather than fixing it, since it is unrelated to any PX-003 blocker.
- No literal manual screen-reader (VoiceOver/NVDA/JAWS) session was performed for B4/B5; Chromium's accessibility tree was inspected directly as the closest automatable proxy. Documented in `ACCESSIBILITY_VALIDATION.md`.
- Cross-browser (non-Chromium) rendering was not verified.

## Known Limitations

- **Loading state screenshots:** not captured. This is a server-rendered (Flask/Jinja2) application with no client-side loading/skeleton state to photograph — documented as an architectural fact in `SCREENSHOT_INDEX.md`, not an oversight.
- **High-zoom testing:** approximated via the WCAG 1.4.10 Reflow equivalence (320px viewport ≈ 400% zoom on a 1280px display) rather than a literal browser-zoom screenshot at a fixed viewport; stated explicitly in `ACCESSIBILITY_VALIDATION.md`.
- **B7's evidence** was captured against a locally-seeded database (`_evidence/seed_rc001.py`), never against production data — appropriate for a design/accessibility/layout review, but not a substitute for post-deploy production smoke testing.
- Scope was strictly B1-B10; no other defect, however tempting, was fixed. The touch-target fix under B7 is the one addition beyond the ten blockers' literal text, and it exists only because B7 itself explicitly instructed "if any breakpoint fails: fix it" for exactly this kind of live-measurement finding.

---

## Version 1 readiness residual

This programme was chartered against PX-003's ten specific, cited release blockers, not the full Version 1 Release Framework (P-002.1) gate set. No claim is made here about overall Version 1 production-readiness or KSI score beyond: **all ten PX-003-identified blockers to Stage 1 external-student release are now closed with evidence.** Any broader V1 gate closure (G1-G12) is outside this programme's chartered scope and is not asserted by this report.
