# Release Checklist

**Status:** Permanent Cursor governance  
**Canonical detail:** [`docs/process/RELEASE_PROTOCOL.md`](../docs/process/RELEASE_PROTOCOL.md), [`docs/release/V2_RELEASE_CHECKLIST.md`](../docs/release/V2_RELEASE_CHECKLIST.md)

Use this checklist before tagging or deploying any release. All items must pass unless explicitly waived with documented rationale.

---

## Pre-release gates

| # | Requirement | Verification |
|---|---|---|
| 1 | **Architecture clean** | `pytest tests/architecture/ -v` green; no layer violations introduced |
| 2 | **Tests passing** | `pytest tests/ -v` green |
| 3 | **Ruff clean** | `ruff check app/ src/ tests/` |
| 4 | **Security review** | No secrets committed; CSRF enabled; auth scoped; Argon2 in production wiring; RBAC roles assigned (PR-001) |
| 5 | **Accessibility review** | Contrast tokens valid; forms labelled; keyboard navigable (for UI changes) |
| 6 | **Performance review** | No obvious N+1 queries; no unbounded loops in hot paths |
| 7 | **Migration review** | Alembic head applied; upgrade path tested; backup taken before production migrate |
| 8 | **Documentation updated** | ADRs, architecture docs, or governance docs updated if boundaries changed |
| 9 | **No TODOs in production code** | No `TODO`/`FIXME`/`HACK` left in shipped paths |
| 10 | **Version tagged** | Git tag matches `APP_VERSION`; release notes prepared |
| 11 | **Health green** | `/health/live` and `/health/ready` return 200 on staging |
| 12 | **Production gates CI** | `production-gates` job green (PR-001 + GA-001) |
| 13 | **GA readiness** | `pytest tests/ga/ -v` green; [`docs/ga/RELEASE_CHECKLIST.md`](../docs/ga/RELEASE_CHECKLIST.md) completed for the deploy |
| 14 | **GA certification** | [`docs/ga/CERTIFICATION_REPORT.md`](../docs/ga/CERTIFICATION_REPORT.md) reviewed; staging backup/restore acknowledged |

---

## Classification-specific additions

Apply the union of requirements when a release spans multiple types (see Release Protocol §2).

| Type | Extra checks |
|---|---|
| **Hotfix** | Targeted smoke on fixed path |
| **Feature** | Smoke on affected student/founder journeys |
| **Architecture** | Full architecture gates + compatibility decision |
| **Migration** | DB backup + `flask db upgrade` verified before deploy |
| **Internal Alpha** | Dual-run flags correct; V1 home preserved |

---

## Deploy verification

| # | Check |
|---|---|
| D1 | `GET /health` returns `status: ok` |
| D2 | Deploy fingerprint matches expected commit/tag |
| D3 | Production smoke tests pass |
| D4 | Curriculum import idempotent (V1 + V2 loadable) |
| D5 | No traceback in startup logs |

---

## Stop conditions

**STOP** the release if:

- Architecture tests fail
- Educational Pipeline behaviour regresses without intentional ADR
- Schema migration untested
- Secrets detected in diff
- Unrelated changes bundled into release commit

Report blockers; do not silently fix unrelated issues during a release.

---

## Commands (quick reference)

```bash
python -m pytest tests/ -v
python -m pytest tests/architecture/ -v
python -m pytest tests/ga/ -v
ruff check app/ src/ tests/
flask db current    # expect head
flask db upgrade    # staging first
```

Deploy operators: complete [`docs/ga/RELEASE_CHECKLIST.md`](../docs/ga/RELEASE_CHECKLIST.md) (Configuration, Database, Health, Telemetry, Background jobs, Console, Student portal, Rollback).
