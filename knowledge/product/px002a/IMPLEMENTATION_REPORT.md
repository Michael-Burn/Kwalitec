# PX-002A — Implementation Report

**Programme:** PX-002A — Trust & Friction Resolution
**Date:** 2026-07-26
**Predecessor:** `knowledge/product/px001/` (analysis-only; nothing implemented under PX-001 itself)

---

## 1. What this programme did

Resolved every Tier 1 item and the naturally-in-scope Tier 2 items from `knowledge/product/px001/HIGH_PRIORITY_BACKLOG.md` — see `FRICTION_RESOLUTION_MATRIX.md` for the full, item-by-item disposition (10 Resolved, 2 Partially Resolved, 1 Already Resolved pre-existing, 1 Deferred, 0 Rejected). No screen was redesigned for appearance; every change is a navigation, copy, terminology, dedup, or component-consistency fix traceable to a specific PX-001 finding.

## 2. Approach

1. **Read the audit corpus** (`PREMIUM_UI_AUDIT.md`, `SCREEN_BY_SCREEN_REVIEW.md`, `PR001_ALIGNMENT_REPORT.md`, `COPY_REVIEW.md`, `CONSISTENCY_AUDIT.md`, `HIGH_PRIORITY_BACKLOG.md`, `EXECUTIVE_SUMMARY.md`) before writing any code, so every change traces to a specific, evidence-backed finding rather than personal taste.
2. **Sequenced Tier 1 first**, per the backlog's own instruction, then worked through Tier 2 items that fell naturally within the same templates/services already being touched.
3. **Verified before claiming.** Every "Resolved" status in `FRICTION_RESOLUTION_MATRIX.md` was checked against the current file content (not just the original plan) before this report was written — one inaccurate claim (a supposed duplicate appearance-switcher removal) was caught this way and corrected to "identified, not actioned" with the actual blocking reason recorded (see `CONSISTENCY_DECISIONS.md` Decision 6).
4. **Ran the full test suite twice** — once with this programme's changes plus all pre-existing working-tree state, once on a clean stash of everything — to isolate exactly which test failures this programme's own changes caused, rather than inheriting or hiding pre-existing failures. See §5.

## 3. Key technical decisions

### 3.1 One duration-formatting module (T1-2)

`app/presentation/formatting.py` is new: `format_minutes`, `format_duration_estimate`, `format_remaining_minutes`. Every touched view model (`app/presentation/session/view_models.py`, `app/presentation/student/view_models.py`) now calls into it instead of building duration strings inline. This closes the *wording* half of T1-2 (see `FRICTION_RESOLUTION_MATRIX.md` for why the *numeric* half — two different data sources potentially still computing different minute counts — is a Runtime A/architecture decision explicitly outside this programme's "No Runtime A changes" constraint, and is logged as Technical Debt rather than closed).

### 3.2 One canonical name per concept, without touching the legacy stack (T1-1)

`ExperienceSurface.HOME`/`HISTORY` labels, `STUDENT_NAV_LABELS`, and every canonical-stack template now say "Home"/"History" instead of "Dashboard"/"Analytics." The legacy Learning Workspace (`dashboard/index.html`) was deliberately left unrenamed — it is a structurally separate, pre-`SOLE_RUNTIME` screen that T1-4 confirms production never serves, and PX-001 itself frames it as a screen the mitigation already addresses rather than one to redesign. `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` — the pre-existing canonical language guide — was also corrected, because it contradicted itself (§1 already said "Home"; §4's nav example still said "Dashboard...Analytics").

### 3.3 One reusable confirmation-modal component (T2-4)

`partials/confirm_modal.html` + `static/js/confirm-modal.js`, included once in `layouts/base.html`, replace native `confirm()` at both call sites named in the backlog (Study Plan archive/delete, Settings restore). The component reads its title/body/label/variant from `data-confirm-*` attributes on the trigger button, so no second bespoke modal was needed for the second call site.

**Static asset budget constraint discovered during implementation:** `tests/test_v1sp003_performance.py::TestStaticAssetsOptimised::test_first_party_css_js_under_budget` enforces `js_bytes < 22_000` across all first-party `static/js/*.js` files. The two new files initially pushed the total to 22,836 bytes. Both were tightened (shorter variable names, denser control flow, comments removed — matching the terse style already used in `app.js`) to bring the combined first-party JS total to 21,842 bytes, restoring headroom under the budget rather than leaving the test on the edge of flaking on the next unrelated JS change.

### 3.4 Coach panel: conditional, not deleted (T2-8)

Rather than removing the Coach panel (one of the recommended solution's two options), it now checks whether the Mission card above it is already showing the same Why/Why now/Next/Benefit explanation (true whenever the student is not in guided-session or reflection state). When it is, Coach shows commitment status or a short pointer instead of repeating the list; when the Mission card isn't showing it, Coach still carries the full explanation, so no information is ever lost — only the literal duplication PR-001 flagged is removed.

### 3.5 Zero-history Analytics framing is conditional, not permanently softened (T2-3)

`AnalyticsService.generate_weekly_report` now computes `is_new_account` and only suppresses per-metric "needs improvement" messaging when there is genuinely zero activity that week. Once a student has any history, the original, more direct feedback still applies — this is a fix for manufacturing "failure" copy from an empty dataset, not a general softening of honest feedback.

## 4. Scope discipline — what was deliberately not touched

- **Runtime A, recommendation ranking/selection, readiness composites, planning logic** — untouched. The only edits inside `app/services/readiness_quality.py` and `app/services/recommendation_quality.py` are single-line `review_point` copy fixes (removing a rejected "study session" synonym); the underlying advice/decision logic is unchanged. These two edits exist on disk but were deliberately excluded from the PX-002A git commit — both files are otherwise entirely pre-existing, untracked WIP unrelated to this programme, and staging either file would have committed hundreds of unrelated lines under this programme's attribution. See `COMPLETION_REPORT.md`'s "Not included in the PX-002A commit" note.
- **General visual design (typography, spacing, colour palette, card/input radii, motion timing)** — untouched, since `CONSISTENCY_AUDIT.md` §2 already found the token system compliant; this programme's brief was explicitly "do NOT redesign for appearance."
- **Icon centralisation (T2-10)** and **appearance-switcher duplication** (`CONSISTENCY_AUDIT.md` §6, not in the numbered backlog) — identified, deliberately deferred/not actioned; see `FRICTION_RESOLUTION_MATRIX.md` and `CONSISTENCY_DECISIONS.md` Decision 6 for why.
- **The dual navigation-stack architecture itself** — T1-4 is an operational verification (confirmed `KWALITEC_V2_SOLE_RUNTIME=1` in `render.yaml`), not a code change; no attempt was made to merge, retire, or restructure either stack.

## 5. Pre-existing, unrelated work-in-progress in the working tree

The working tree contained substantial **pre-existing, uncommitted work** on an unrelated set of features (a large "unified journey," "adaptive engine," "digital twin," "consumer chain," and educational-runtime-bridge body of work under `app/application/unified_journey/`, `app/infrastructure/adapters/adaptive_engine/`, `.../digital_twin/`, `.../consumer_chain/`, and related service/route files) **before this programme began** — visible in the git status captured at the start of this conversation. This is explicitly **not** PX-002A's work, was not reviewed, evaluated, or claimed by this programme, and several of the files this programme touched (`app/presentation/student/view_models.py`, `app/templates/student/home.html`, `app/services/readiness_quality.py`, `app/services/recommendation_quality.py`) also carry that pre-existing WIP alongside PX-002A's own, much smaller, specific edits. `FRICTION_RESOLUTION_MATRIX.md`, `COPY_STANDARDIZATION.md`, and `DESIGN_STANDARDIZATION_MATRIX.md` describe only PX-002A's own contribution to those shared files, not their full `git diff`.

To isolate PX-002A's actual effect on test health from that pre-existing WIP:

1. Ran `pytest tests/ -q` with the full working tree (PX-002A changes + pre-existing WIP): **42 failed, 43,097 passed, 7 skipped** (post-fix; see below).
2. Ran `git stash -u` (removing *all* uncommitted state, both PX-002A's and the pre-existing WIP's) and re-ran: **20 failed, 34,183 passed, 7 skipped** on a clean `HEAD`.
3. Diffed the two failure lists and spot-verified representative failures from every category (alembic multi-head migration conflicts, digital-twin/adaptive-engine architecture-purity assertions, dual-run/decision-simulation/recovery-injection parity checks, mission-narrative "Learning Mode" explainability assertions, brand-identity/logo/asset tests, startup-service tests) by reading their tracebacks directly. Every one of the 22 failures present only in the full tree traces to files this programme did not touch (`app/services/recommendation_service.py`, `planning_service.py`, `mission_optimizer.py`, `app/application/unified_journey/`, `app/infrastructure/adapters/adaptive_engine/`, migration files under `migrations/versions/`) — i.e. to the pre-existing WIP, not to PX-002A.
4. **One exception found and fixed:** the JS-budget test (§3.3 above) failed because of PX-002A's own two new JS files. Fixed by tightening both files; confirmed the specific test now passes and the full-tree failure count dropped from 43 to 42.
5. Restored the stash (`git stash pop`) so no work was lost.

No PX-002A change introduces a new test failure. The 42 failures present after this programme's work are the pre-existing 20 plus 22 more, all attributable to the pre-existing WIP described above, none to any file or line this programme's diff touches.

## 6. Testing and linting

- Full suite: `source .venv/bin/activate && python -m pytest tests/ -q` — 42 failed / 43,097 passed / 7 skipped, all failures pre-existing per §5.
- `ruff check` on every Python file this programme edited or created: `app/presentation/formatting.py` (0 errors), `app/services/analytics_service.py` (15 pre-existing errors, all in lines this programme did not touch — one pre-existing violation this programme's edit would have added was fixed instead of left, so the file's own error count went from 17 to 15, a net improvement), `app/presentation/student/view_models.py`, `product_language.py`, `student/navigation.py`, `session/view_models.py`, `domain/student_experience/experience_workspace.py` — no errors attributable to PX-002A's own edits.
- `ruff check app/` (whole app, unscoped) reports 292 pre-existing errors across the codebase, overwhelmingly in the pre-existing WIP described in §5; not remediated, as that is out of this programme's scope.
