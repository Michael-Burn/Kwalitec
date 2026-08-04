# PX-005 reliability evidence notes

## PX-B-006 — First-sitting campaign engagement race

**Fix:** In `generate_daily_mission`, before idempotent return of an existing GENERATED/ACCEPTED mission, compare bound `educational_package_id` to owed package from `resolve_active_educational_package` / `pending_post_tip_front_package`. On mismatch with both ids present, delete and regenerate.

**Does not change** selection policy — only invalidates stale persisted inventory (RO15-R1 class).

**Regression:** Static contract in `test_px005_phase3_microcopy_reliability.py`. LIVE campaign-join dogfood remains desirable.

## PX-B-008 — Continue Session contention

**Fix:**
1. `FLASH_WARNING["continue_contention"]` / `continue_retry`
2. Session blueprint `_session_contention_boundary` maps OptimisticLockError / transient DB errors → calm flash + Home
3. `StudentRuntimeCoordinator.resume_session` retries once on OptimisticLockError

**Never** scores infra as educational failure.

**LIVE re-measure:** Residual PX5-R2 (PB-014…017 pattern).

## PX-B-009 — Perceived wait craft

**Student path:** Quiet Home shows `skeleton_student_home` + preparing support when `preparing_mission`.

**Ops path:** Render create-user / seed / backdate SLOs remain ops-owned (PX5-R4). Full skeleton transitions on Mission/Plan owned by WS-09 (PX-B-032).
