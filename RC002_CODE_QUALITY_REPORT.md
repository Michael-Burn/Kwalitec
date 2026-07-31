# RC-002 — Code Quality Report

**Programme:** Release Candidate RC-002  
**Date:** 2026-07-31  
**Authority:** Release engineering — quality gates for founder deployment

---

## Summary

Educational integrity and founder-critical suites are green. Flask production startup is clean. Full repository pytest still carries **pre-existing / stale** failures outside the Runtime C founder path; these are documented as known debt, not treated as silent product regressions on the frozen educational spine.

---

## Gates executed

| Gate | Command / scope | Result |
|---|---|---|
| Ruff (critical) | `ruff check … --select F821,F811,E9` | **PASS** after TYPE_CHECKING fix for `StudySessionFeedbackNarrative` |
| Ruff (full style) | `ruff check app/ tests/` | **WARN** — ~769 style findings (mostly E501/I001/W293); CI ignores F401; not treated as RC blocker |
| Type checking | mypy | **N/A** — not configured in repo |
| Flask startup | `APP_ENV=production` + `create_app()` + `/health` `/health/live` `/health/ready` | **PASS** — no startup exceptions; CSRF on; secure cookies on |
| Educational integrity | V1S-005…008 + Mission-002 + KWP-015 + alpha smoke student | **78/78 PASS** |
| Ops / language / evidence | operational alpha config, product language matrix, SDT-004, EV-001B, session overview workflow | **PASS** after Alembic/docs/copy/fake-completer fixes |
| Full `tests/` (ignore architecture) | pytest | **43392 passed**, **225 failed**, 9 skipped (pre-fix snapshot); residual debt after RC fixes still expected in time-engine / snapshot / tutor suites |

---

## Startup validation evidence

- Config: `ProductionConfig`, `DEBUG=False`, `WTF_CSRF_ENABLED=True`, `SESSION_COOKIE_SECURE=True`
- Migrations applied to head `202607300005`
- Health JSON: `status=ok`, components database / migrations / instance_storage / queue ok
- Curriculum import idempotent (CS1 / CB2 / CM1 V2)

---

## Import / circular import / SQLAlchemy

| Check | Result |
|---|---|
| Import errors on `create_app` | **None** |
| Circular imports blocking startup | **None** |
| SQLAlchemy warnings at startup | **None** material; test suite still emits `LegacyAPIWarning` / `utcnow` deprecations |
| Flask startup warnings | Secure-key warning only when using default secret in non-prod; production rejects insecure keys |

---

## RC-002 fixes applied (quality only)

1. `StudySessionFeedbackNarrative` forward ref via `TYPE_CHECKING`
2. Alembic head constant → `202607300005` (helpers, CI, adaptive-assessment regressions, Internal Alpha checklist)
3. `_FakeMissionCompleter` accepts `evidence_disposition` / `may_complete_mission`
4. Product Language Guide appendix for Adaptive Workspace vocabulary
5. DF-016 title repair-on-read (`student_facing_identity` + educational experience prefer live syllabus title)
6. Student-visible “study session” → “session” in session substance chrome

---

## Known test debt (not zeroed in RC-002)

| Bucket | Approx. failures | Disposition |
|---|---|---|
| Time engine fixtures (FK `curriculum_id`) | ~18 | Stale fixtures vs schema — deferred |
| EOS / tutor / adaptive snapshot suites | ~40+ | Pre-V1S surface debt — deferred |
| Session workflow complete→Home | several | Finish-review / Sitting Report redirect is intentional under commercial loop |
| Brand / nav chrome assertions | few | Cosmetic copy drift — deferred |

**Honesty vs success criterion “Zero failing tests”:** educational + ops gates required for founder study are green; full-tree zero is **not** claimed. See final RC report recommendation.

---

## Architecture compliance

Layering preserved. No new Runtime A student spine. Curriculum V1/V2 loadability unchanged.
