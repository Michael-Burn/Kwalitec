# PR-001B — Test Evidence

**Programme:** PR-001B — Student Pilot Journey  
**Date:** 2026-07-27  

---

## Commands

```bash
python3 -m ruff check \
  app/auth/routes.py \
  app/application/educational_experience/service.py \
  app/presentation/student/forms.py \
  app/presentation/student/routes.py \
  app/presentation/student/educational_view_models.py \
  tests/certification/test_pr001b_student_pilot.py

python3 -m pytest \
  tests/certification/test_pr001b_student_pilot.py \
  tests/application/educational_experience/test_acceptance.py \
  -v --tb=short
```

## Results

| Suite | Outcome |
|---|---|
| Ruff (PR-001B paths) | Clean |
| `test_pr001b_student_pilot.py` | **12 passed** |
| PX-001 acceptance (regression) | **5 passed** |
| **Total** | **17 passed** |

Raw log: [`TEST_EVIDENCE_RAW.txt`](TEST_EVIDENCE_RAW.txt)

## Acceptance coverage map

| Criterion | Test |
|---|---|
| Discover / enrol published subject | `test_discover_published_subject_via_bridge` |
| Understand today’s mission + clarity | `test_home_shows_mission_and_clarity`, `test_four_clarity_questions` |
| Complete mission | `test_complete_mission_updates_progress` |
| Observe progress / journey | `test_journey_shows_advancement_after_complete` |
| Return without wizard | `test_login_lands_on_home_not_wizard` |
| Interrupted session | `test_interrupted_session_keeps_same_mission` |
| Missed-day return | `test_missed_day_return_still_shows_current_topic` |
| Consecutive + multiple missions | `test_next_day_advances_after_completion`, `test_multiple_missions_across_days` |
| Operational recovery | `test_duplicate_complete_is_recoverable` |
| Coexistence | `test_coexistence_runtime_a_unchanged` |
