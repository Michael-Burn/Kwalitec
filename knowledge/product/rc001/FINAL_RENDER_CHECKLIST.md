# RC-001 — Final Render Deployment Checklist

Stage 1 external-pilot readiness checklist, scoped strictly to what RC-001 was chartered to verify (PX-003's ten blockers) plus the production configuration those fixes depend on. This is not a general infrastructure/ops checklist — see Known Limitations for what remains outside this programme's scope.

---

## PX-003 blocker closure

- [x] **B1** — Reflection note is persisted (`SessionRuntimePort.record_reflection_note`), durable under `ENABLE_DURABLE_STORE=1` (production posture — see below).
- [x] **B2** — Profile's "Current Examination" reads from `StudyPlanService.get_user_active_plan`, the same source as Dashboard/Study Plan/Settings.
- [x] **B3** — Mission's duration resolves via the same `resolve_planned_session_minutes(..., mission_date=...)` call Home/Session use; template fallback chain removed.
- [x] **B4** — Welcome modal has focus entry, trap, return, Escape, and `aria-describedby`; `app.js` now loads on the canonical Student shell that actually renders it.
- [x] **B5** — Nav drawer has `aria-expanded`/`aria-controls`, focus trap, focus return; verified live via Playwright keyboard simulation.
- [x] **B6** — Sidebar section-label contrast raised from 3.21:1 to 5.18:1 (AA-passing); all other sidebar tokens verified ≥ 4.5:1.
- [x] **B7** — 162 screenshots across 9 breakpoints captured; 0px horizontal overflow found; 1 real mobile touch-target defect found and fixed.
- [x] **B8** — `AlphaOnboardingService.should_show(...)` checked at login, before the study-plan-wizard branch — guarantees exactly one onboarding decision regardless of entry path.
- [x] **B9** — `GET /settings/` redirects to `student.profile` under `SOLE_RUNTIME=1`; verified against a running server with the production flag set.
- [x] **B10** — "Learning profile status" / "Internal Alpha" language removed from the one page any authenticated student could reach; internal build-flag fields removed rather than relabelled.

## Production flag posture (`render.yaml`) — confirmed consistent with what RC-001 tested against

| Flag | Production value | Relevance to RC-001 |
|---|---|---|
| `KWALITEC_V2_SOLE_RUNTIME` | `1` | B8/B9 fixes were tested with this flag set — matches production exactly, not a dual-run assumption. |
| `KWALITEC_V2_DURABLE_STORE` | `1` | B1's reflection-note persistence is durable (not process-memory-only) in this configuration — the fix's real-world behaviour in production is durable storage, as the on-screen promise requires. |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `1` | Canonical Student Experience shell (where B2/B4's fixes apply) is active. |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` | Internal Alpha features enabled for the founding cohort; B10 removed internal-sounding labels from the page this flag gates access to the *route* of (not the content), consistent with "any authenticated student," not just alpha testers, being able to reach it. |
| `KWALITEC_V2_SEED_DEMO` | `0` | Production does not seed demo data — B7's evidence was captured against a locally-seeded database (`_evidence/seed_rc001.py`), never against production data. |

## Regression and quality gates

- [x] 100/100 RC-001-specific regression tests passing (`RELEASE_EVIDENCE.md` §1).
- [x] Zero new ruff findings introduced by RC-001 changes (`RELEASE_EVIDENCE.md` §4).
- [x] Full suite's 265 pre-existing failures investigated and attributed to 3 causes entirely outside B1-B10 scope, none regressions from this programme (`RELEASE_EVIDENCE.md` §3).
- [ ] **Not closed by RC-001 (explicitly out of scope):** the Alembic dual-migration-head condition (`RELEASE_EVIDENCE.md` §3a) exists in the current working tree from unrelated, pre-existing uncommitted work. This does not block RC-001's own deliverables (RC-001's own migrations are not implicated), but **must be resolved before that unrelated work is deployed** — merging migration heads is a one-line `alembic merge` operation for whoever owns that separate body of work, not something RC-001 is chartered to touch.

## Pre-deploy operational reminders (general Kwalitec deployment hygiene, not RC-001-specific)

- [ ] Confirm `ADMIN_EMAIL`/`ADMIN_PASSWORD` are set as Render secrets (not committed) before first boot — `StartupService` creates the admin idempotently from these.
- [ ] Confirm `SECRET_KEY` is Render's `generateValue: true` output, not a default/dev value (the app factory already validates this and refuses to run insecurely in production — verify no override).
- [ ] Confirm the Alembic dual-head condition above is resolved (single head) before `StartupService`'s migration step runs against the production database, or startup's migration step will skip with a warning (fail-open, not fail-closed — verified in `app/services/startup_service.py`'s existing behaviour) and the app will run against whatever schema state the production DB is already in.

## What this checklist does not cover (Known Limitations, stated honestly)

- General performance/load testing of the Render `free` plan tier.
- Cross-browser testing beyond Chromium (no Firefox/Safari/WebKit engine pass was run).
- A literal manual screen-reader (VoiceOver/NVDA/JAWS) session — see `ACCESSIBILITY_VALIDATION.md`'s Known Limitation.
- Any blocker, feature, or defect outside PX-003's ten named items — explicitly out of RC-001's chartered scope.

## Sign-off

All ten PX-003 release blockers are resolved with cited code, live evidence, and dedicated regression tests. No blocker remains open. The one operational item above (migration head merge) belongs to pre-existing work outside this programme's scope and should be tracked as a release-gate item by whoever owns that work, not as an RC-001 deliverable gap.

**RC-001 programme status: complete. Product is ready for Stage 1 Render deployment on the B1-B10 dimensions this programme was chartered to verify.**
