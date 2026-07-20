# Validation

## Purpose

Executable architecture governance for Kwalitec Version 2. Documentation without green gates is incomplete.

## Owner

Architecture Governance

## Status

Active — mandatory CI gate (APP-003)

## Contents

| Gate suite | Path |
|---|---|
| Architecture governance tests | `tests/architecture/` |
| Layer dependency rules | `tests/architecture/test_layer_dependency_rules.py` |
| Composition root | `tests/architecture/test_composition_root.py` |
| Student experience boundary | `tests/architecture/test_student_experience_boundary.py` |
| AI enrichment boundary | `tests/architecture/test_ai_enrichment_boundary.py` |
| Pipeline orchestration | `tests/architecture/test_pipeline_orchestration.py` |
| Governance artefacts | `tests/architecture/test_governance_artefacts.py` |

### CI

GitHub Actions job **Architecture Governance** runs:

```bash
python -m pytest tests/architecture/ -v --tb=short
```

The job is required before the broader test and lint jobs. Release protocol requires the same gate (see `docs/process/RELEASE_PROTOCOL.md`).

### Governing documents

- [`docs/ARCHITECTURE_CONSTITUTION.md`](../../../docs/ARCHITECTURE_CONSTITUTION.md)
- [`docs/DEPENDENCY_RULES.md`](../../../docs/DEPENDENCY_RULES.md)
