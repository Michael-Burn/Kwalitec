# GA-001 Performance Baseline

**Programme:** GA-001 — Workstream 3  
**Evidence:** `tests/ga/test_performance_benchmarks.py` (soft budgets for CI)  
**Profiling hook:** `PROFILE_SQL=1` + `app.infrastructure.diagnostics.query_profiling`

## Soft budgets (CI)

These budgets are intentionally conservative for GitHub Actions runners. Staging/production measurements should be recorded separately under load.

| Surface | Path | Response budget (ms) | SQL statement budget |
|---|---|---|---|
| Student Dashboard | `/student/` | 2500 | 80 |
| Workspace (session overview) | `/session/<id>/overview` | 2500 | — |
| Journey | `/student/journey` | 2500 | 80 |
| Console Home | `/console/` | 3500 | 120 |
| Platform Intelligence | `/console/alpha-observability` | 3500 | 120 |
| Health live | `/health/live` | 500 | — |
| Health ready | `/health/ready` | 1500 | 40 |

## Measures collected

| Metric | Mechanism |
|---|---|
| Response time | `time.perf_counter` around Flask test-client GET |
| SQL queries | `count_queries()` SQLAlchemy `before_cursor_execute` counter |
| Request duration (runtime) | `kwalitec.observability` `http_request` / `slow_request` logs |
| Memory | Not asserted in CI (process RSS varies); operators sample via host metrics |

## Operator sampling (staging)

```bash
# Enable per-request SQL counts in logs
PROFILE_SQL=1

# Lower slow-request threshold temporarily to calibrate
SLOW_REQUEST_THRESHOLD_MS=300

curl -fsS -o /dev/null -w '%{time_total}\n' "$BASE_URL/student/"
curl -fsS -o /dev/null -w '%{time_total}\n' "$BASE_URL/console/"
curl -fsS "$BASE_URL/health/ready"
```

## Status

| Item | Result |
|---|---|
| Soft budgets encoded & tested | Pass when `pytest tests/ga/test_performance_benchmarks.py` is green |
| N+1 hot-path work from PR-001 | Retained (dashboard/console) |
| Production load test under cohort traffic | **Open** — run before high-traffic marketing launch |

## Known limitations

- CI timings are not production SLOs.
- In-process SQLite test harness under-represents Postgres latency and pool behaviour.
- Memory budgets are operational (host monitoring), not pytest assertions.
