# Testing Requirements

**Status:** Permanent Cursor governance  
**Companion:** [`.cursor/rules/05-testing.mdc`](05-testing.mdc), [`tests/architecture/`](../../tests/architecture/)

**No implementation is considered complete until tests pass.**

---

## Required coverage per feature

Every feature change must include applicable items from this checklist:

| Category | When required | Location |
|---|---|---|
| **Unit tests** | Always — pure logic, domain rules, mappers | `tests/domain/`, `tests/application/`, package-local `tests/` |
| **Integration tests** | Cross-layer or persistence behaviour | `tests/infrastructure/`, `tests/education_os/`, `@pytest.mark.integration` |
| **Architecture purity tests** | Any import boundary or layer change | `tests/architecture/` |
| **Accessibility validation** | UI exists or changes | Contrast helpers, template a11y assertions, manual checklist |
| **Regression tests** | Behaviour change or bug fix | Adjacent to affected module |
| **Repository tests** | New or changed persistence adapters | `tests/infrastructure/` |
| **Pipeline tests** | Educational Pipeline stage or orchestration change | `tests/application/`, `tests/education_os/` |

---

## Architecture purity tests (mandatory CI gates)

These tests enforce the constitution. Breaking a boundary fails the build:

| Gate | File |
|---|---|
| Layer import purity | `test_layer_dependency_rules.py` |
| Composition root construction | `test_composition_root.py` |
| Student experience non-authority | `test_student_experience_boundary.py` |
| AI enrichment non-authority | `test_ai_enrichment_boundary.py` |
| Pipeline orchestration only | `test_pipeline_orchestration.py` |
| Governance artefacts present | `test_governance_artefacts.py` |

---

## Harness

- **Framework:** pytest (`pyproject.toml` config)
- **Paths:** `tests/`, `src/`, `app/` on `pythonpath`
- **Fixtures:** `app`, `db`, `ctx`, `client`, `runner` in `tests/conftest.py`
- **Database:** Temp SQLite; tables truncated between tests
- **CSRF:** Disabled in test config only

---

## Expectations

1. Add or update tests for every behaviour change.
2. Curriculum work requires **V1 regression** and **V2/section-aware** coverage when relevant.
3. Do not delete failing tests to green CI — fix product code or revise assertions with rationale.
4. Keep tests **deterministic** — inject dates/clocks; no wall-clock flakiness.
5. Use factory helpers from `conftest.py` when available.

---

## Commands

```bash
# Full suite
python -m pytest tests/ -v

# Architecture gates only
python -m pytest tests/architecture/ -v

# Targeted
python -m pytest tests/domain/ -v
python -m pytest tests/application/ -v

# Lint (required alongside tests)
ruff check app/ src/ tests/
```

---

## CI

GitHub Actions runs pytest on Python 3.11–3.13 and ruff. Local runs must match before merge.

---

## Definition of done

A change is test-complete when:

- [ ] Relevant unit and integration tests added or updated
- [ ] `tests/architecture/` green (if boundaries touched)
- [ ] `ruff check` clean on touched paths
- [ ] Full `pytest tests/` green (or scoped suite justified in completion report)
