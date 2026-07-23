# GA-001 Workflow Validation Results

**Programme:** GA-001 — Workstream 1 (Release Candidate Validation)  
**Runtime under test:** legacy production Flask app (`wsgi.py` → `app.create_app()`)  
**Automated evidence:** `tests/ga/test_e2e_workflows.py`

## Critical path matrix

| Workflow | Entry path(s) | Verification | Status |
|---|---|---|---|
| Student onboarding | `/alpha/onboarding` | Authenticated GET 200 | Pass (automated) |
| Mission lifecycle | `/missions/`, `/session/<id>/{overview,activity,reflection,summary,complete}` | Surfaces return 200 after workspace navigation | Pass (automated) |
| Revision planner | `/student/revision` | GET 200 | Pass (automated) |
| Reflection | `/session/<id>/reflection` | GET 200 in mission lifecycle | Pass (automated) |
| Journey | `/student/journey` | GET 200 | Pass (automated) |
| Readiness | `/analytics/` (readiness panels) | GET 200 | Pass (automated) |
| Coach | Client telemetry `coach_opened` via `/alpha/telemetry` | Ingest 200 + persisted event | Pass (`test_observability`) |
| Console | `/console/` + ops surfaces | Founder 200 | Pass (automated) |
| Platform Intelligence | `/console/alpha-observability` | Founder 200; title present | Pass (automated) |
| Support | `/alpha/help`, `/alpha/feedback/*` | GET 200 | Pass (automated) |
| Settings | `/settings/`, `/settings/export/backup` | GET 200; JSON backup without secrets | Pass (automated) |

## Portal separation

| Actor | Student portal | Console |
|---|---|---|
| Student role | Allowed | **403** |
| Founder + Administrator | Allowed (when student surfaces wired) | **200** |
| Anonymous | Redirect to `/auth/login` | Redirect to `/auth/login` |

## Health regression

| Endpoint | Expectation | Status |
|---|---|---|
| `/health/live` | Always 200 | Pass |
| `/health/ready` | 200 when DB + migrations ok | Pass (test harness) |
| `/health` | Compatibility probe | Pass |
| `/health/details` | Includes dead letters + alerts | Pass |

## Notes

- Coach and readiness do not have dedicated legacy HTTP routes; coach is validated via telemetry ingest, readiness via `/analytics/`.
- Education OS (`/eos/*`) is dual-run optional and **out of redesign scope**; production deploy docs target the legacy app.
- No educational algorithm or recommendation behaviour was changed for this validation.
