# ROOT CAUSE ANALYSIS — Home → Start Session HTTP 500

**Priority:** P0 (Critical Beta Blocker)  
**Date:** 2026-07-24  
**Status:** FIXED  
**Scope:** Defect correction only — no redesign, no educational-behaviour change

---

## Cause

When Student Home posts **Start Session**, `ExperienceMissionAdapter.start_session` calls the injected Mission opaque engine (`MissionOpaqueBridge.start_opaque` under `KWALITEC_V2_INJECT_ENGINES=1`).

That opaque result is a dict with `session_id` / `mission_id` / `status` but **without** `experience_session_id`.

The adapter then did:

```python
str(result["experience_session_id"])  # KeyError
```

Unhandled `KeyError` → raw Flask **HTTP 500** on `POST /student/session/start`.

### Stack trace (pre-fix)

```
File app/presentation/student/routes.py, start_session
File app/presentation/student/views.py, start_todays_session
File app/application/student_experience/student_experience_service.py, start_session
File app/infrastructure/adapters/mission/experience_adapter.py, start_session
KeyError: 'experience_session_id'
```

### Why the exception occurs

- Production composition injects opaque engine bridges when V2 inject-engines is on.
- `MissionOpaqueBridge.start_opaque` returns a Mission-shaped opaque document, not a full Experience session start document.
- The adapter treated any dict from `start_opaque` as a complete Experience start result and required `experience_session_id`.
- Default path (`_default_start_result`) always set that key — so unit tests without an engine never failed.

**Category:** service invocation / missing field on opaque engine result (legacy incomplete contract between opaque bridge and Experience Mission adapter).

---

## Why Dashboard worked

Dashboard → Session uses the **legacy Mission study-session** path:

| Step | Route | Method |
|---|---|---|
| Missions list | `/missions/` | GET |
| Start study session | `/missions/<id>/session/start` | POST |
| Active session | `/missions/<id>/session` | GET |

That path goes through `StudySessionService.start_session` and Mission routes. It never calls `ExperienceMissionAdapter.start_session`, so it never touched the missing `experience_session_id` key.

---

## Why Home failed

Home → Start Session uses the **Student Experience → Session Experience** hand-off:

| Step | Route | Method |
|---|---|---|
| Student Home | `/student/` | GET |
| Start Session CTA | `/student/session/start` | POST |
| Intended landing | `/session/<session_id>/overview` | GET (redirect target) |

First divergence from Dashboard: different blueprint (`student` vs `mission`), different endpoint, and a Mission **Experience** adapter with an opaque engine.

Failure happened **on the POST** (before redirect). The overview route was never reached while the KeyError stood.

---

## Behaviour before

1. Student opens `/student/`.
2. Clicks **Start Session** (`POST /student/session/start` with `mission_id` + `session_id`).
3. Server raises `KeyError: 'experience_session_id'`.
4. Browser shows raw **Internal Server Error** (HTTP 500).

Evidence retained from review capture:

- `knowledge/reviews/V1_REVIEW_PACKAGE/screens/58-error-500-raw.png`
- `knowledge/reviews/V1_REVIEW_PACKAGE/screens/35-session-overview-error.png`

---

## Behaviour after

1. Student opens `/student/`.
2. Clicks **Start Session**.
3. `POST /student/session/start` returns **302**.
4. Browser lands on `/session/<session_id>/overview` (Session Overview) with success flash.
5. Dashboard → `/missions/<id>/session` remains unchanged and healthy.

Evidence (post-fix):

| Screenshot | Meaning |
|---|---|
| [`screens/fix-home-before-start-session.png`](screens/fix-home-before-start-session.png) | Home with Start Session CTA |
| [`screens/fix-home-start-session-overview.png`](screens/fix-home-start-session-overview.png) | Successful Overview after Start Session |
| [`screens/fix-session-overview-fresh.png`](screens/fix-session-overview-fresh.png) | Fresh session Overview |
| [`screens/fix-dashboard-session-ok.png`](screens/fix-dashboard-session-ok.png) | Dashboard Session path still OK |
| [`screens/fix-return-home.png`](screens/fix-return-home.png) | Return to Student Home |

Server log after fix (excerpt):

```
POST path=/student/session/start status=302
GET  path=/session/sess-29/overview status=200
```

---

## Fix

Smallest safe correction in the Mission Experience adapter:

1. Always build `_default_start_result` (includes `experience_session_id`).
2. If an opaque engine returns a dict, **merge** via `_normalize_start_result` so Experience-required identity keys are never dropped.
3. Belt-and-suspenders: `MissionOpaqueBridge.start_opaque` now also emits `experience_session_id`.

No changes to Educational State, Twin math, analytics event types, Dashboard Mission routes, or Session Experience educational policies.

---

## Files modified

| Path | Change |
|---|---|
| `app/infrastructure/adapters/mission/experience_adapter.py` | Normalize opaque `start_opaque` results; add `_normalize_start_result` |
| `app/infrastructure/engines/opaque_bridges.py` | Include `experience_session_id` in Mission opaque start doc |
| `tests/infrastructure/adapters/student_experience/test_adapters.py` | Regression: incomplete opaque engine + bridge |
| `tests/presentation/student/test_routes.py` | HTTP regression: POST must 302, not 500 |

---

## Tests executed

```bash
.venv/bin/python -m pytest \
  tests/infrastructure/adapters/student_experience/test_adapters.py::test_start_session_normalizes_opaque_engine_without_experience_id \
  tests/infrastructure/adapters/student_experience/test_adapters.py::test_start_session_with_mission_opaque_bridge \
  tests/presentation/student/test_routes.py::test_start_session_post \
  tests/presentation/student/test_routes.py::test_start_session_opaque_engine_missing_experience_id \
  tests/presentation/student/test_routes.py::test_begin_revision_post \
  tests/operational/test_alpha_smoke_student.py -q --tb=short
# → 11 passed

.venv/bin/ruff check \
  app/infrastructure/adapters/mission/experience_adapter.py \
  app/infrastructure/engines/opaque_bridges.py \
  tests/infrastructure/adapters/student_experience/test_adapters.py \
  tests/presentation/student/test_routes.py
# → All checks passed
```

### Manual / Playwright verification (local `:5055`, V2 inject-engines on)

| Check | Result |
|---|---|
| Home → Start Session | 302 → `/session/.../overview` (200), no 500 |
| Dashboard → Session (`/missions/17/session`) | 200 |
| Return to Home (`/student/`) | 200 |
| Mission flow (legacy session) | Unchanged / OK |

---

## Success criteria

**Met:** Clicking **Start Session** from Home launches Session Experience Overview without errors, while Dashboard → Session continues to work.

---

## Architecture / migration notes

- **Migration impact:** None  
- **Curriculum V1/V2:** Unaffected  
- **Application educational kernels:** Untouched  
- **Presentation:** Routes/templates unchanged; adapter contract hardening only
