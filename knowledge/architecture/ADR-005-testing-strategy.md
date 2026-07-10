# ADR-005: Testing Strategy

# Status

Accepted

# Date

2026-07-10

# Context

Kwalitec’s correctness depends on deterministic services, curriculum V1/V2 coexistence, and safe production bootstrap. Regressions in topic ordering, import idempotency, or auth boundaries are product-breaking, not cosmetic.

The project needed a testing strategy that:

- Runs reliably in CI across Python 3.11–3.13
- Isolates tests on temporary SQLite with truncated tables
- Forces curriculum changes to prove **both** V1 and V2 paths
- Prefers focused unit/integration tests over brittle full-UI scripts

# Decision

Use **pytest** under `tests/` with fixtures from `conftest.py` (`app`, `db`, `ctx`, `client`, `runner`, factories). CSRF is disabled only in the test app config. Lint with **ruff**. CI (GitHub Actions) runs pytest on 3.11 / 3.12 / 3.13 plus ruff; deploy dry-run checks run on `main`.

### Unit tests

- Target models, pure service methods, and Curriculum Engine loaders/validators/repository.
- Prefer deterministic dates (inject dates; avoid wall-clock flakiness).
- Use factory helpers (`_make_user`, etc.) from `conftest.py`.

### Integration tests

- Cover blueprint → service → DB paths with the Flask test client.
- Include auth, study-plan wizard smoke, missions, settings, CLI (`create-admin`), and `StartupService` behaviour.
- Assert ownership scoping and redirect/security behaviour where relevant.

### Regression tests

- Protect previously fixed bugs and critical workflows (`test_smoke.py` and focused modules).
- Do not delete failing tests to green CI; fix product code or revise assertions with rationale.
- When changing curriculum behaviour, re-run both V1 and V2 suites (below).

### Backwards compatibility tests

Curriculum work **requires** dual coverage:

| Concern | Representative modules |
|---|---|
| V1 engine / flat load | `test_curriculum_engine.py`, importer paths |
| V2 engine / hierarchical load | `test_curriculum_engine_v2.py` |
| Section-aware DB behaviour | `test_curriculum_section_aware.py`, `test_section_model.py`, `test_topic_section_relationship.py` |
| Import idempotency | `test_curriculum_importer.py` |

Compatibility assertions include: nullable `section_id`, V1 traversal without sections, V2 section-then-topic order, and continued loadability of flat JSON.

### Commands

```bash
python -m pytest tests/ -v
python -m pytest tests/test_curriculum_engine_v2.py tests/test_curriculum_section_aware.py -v
ruff check app/ tests/
```

# Consequences

### Positive consequences

- Layered tests match layered architecture ([ADR-001](ADR-001-service-layer.md), [ADR-002](ADR-002-blueprint-architecture.md)).
- V1/V2 invariants are enforceable in CI, not only in docs ([ADR-003](ADR-003-curriculum-v1-v2.md), [ADR-004](ADR-004-canonical-topic-traversal.md)).
- Contributors have a clear “definition of done” before merge ([`CONTRIBUTING.md`](../../CONTRIBUTING.md)).

### Trade-offs

- Dual curriculum suites increase runtime — accepted for safety.
- Temp SQLite differs from production PostgreSQL; dialect-specific issues need occasional prod-like checks.
- End-to-end browser automation is intentionally light; smoke + service tests carry most weight.

### Future considerations

- Add targeted tests whenever traversal, import, or readiness formulas change.
- Prefer freezegun-style or injected clocks if more time-dependent logic lands.
- Keep test DB setup idempotent and isolated; never point tests at developer `instance/` data.

**See also:** `.cursor/rules/05-testing.mdc`, [coding-standards.md](../development/coding-standards.md).
