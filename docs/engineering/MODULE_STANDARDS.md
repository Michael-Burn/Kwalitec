# Module Standards

**Programme:** V1S-003  
**Status:** Active  
**Effective:** 2026-07-31

---

## One responsibility

A module owns one coherent job. If the module docstring needs “and” more than once for unrelated jobs, split it.

## Size guidance

| Kind | Soft max (LOC) | Action when exceeded |
|---|---|---|
| Domain pure module | 400 | Split by aggregate / policy |
| Application engine | 500 | Extract dto / rules / guidance |
| Service orchestration | 600 | Extract seams (read vs write vs policy) |
| Presentation view-model | 600 | Extract section composers |
| Routes module | 400 | Extract handlers / forms |

These are **guidance**, not hard CI gates. New code should not grow known god modules without a split plan.

## Known oversized modules (retain until planned split)

| Module | Approx LOC | Planned seam |
|---|---|---|
| `app/services/planning_service.py` | ~1650 | Runtime A mission vs plan CRUD |
| `app/services/recommendation_service.py` | ~1460 | Quality vs personalisation vs core |
| `app/services/research_insight_service.py` | ~1530 | Inbox vs analytics |
| `app/application/educational_runtime_engine/service.py` | ~1390 | Coexistence helpers |
| `app/presentation/student/view_models.py` | ~2360 | Page section builders |
| `app/infrastructure/adapters/evidence_platform/contracts.py` | ~2450 | Contract families |

## Documentation

- Public service / engine methods: purpose docstring; Args / Returns when non-obvious.
- Package `__init__.py`: one-paragraph responsibility + lifecycle disposition when non-ACTIVE.
- Prefer clarifying names over long comments. Do not comment the obvious.

## Type hints

- Target Python 3.11+; use `from __future__ import annotations` in application modules that declare types.
- Prefer built-in generics (`list[str]`, `dict[str, Any]`).
- Avoid `# type: ignore` without a one-line reason.

## Logging & errors

- Module logger: `logger = logging.getLogger(__name__)`.
- No `print()` in committed product code.
- Prefer specific exceptions; broad `except Exception` only on startup / isolation boundaries with logging.
- Do not log secrets, cookies, or full DB URLs with credentials.

## Configuration

- Feature flags and env reads live in dedicated config modules (`app/application/config`, `app/application/platform_integration/flags.py`).
- Do not scatter `os.environ` reads inside educational evaluate paths.
