# Engineering Conventions

**Status:** Permanent Cursor governance  
**Companion:** [`.cursor/rules/02-python.mdc`](02-python.mdc), [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

---

## Python

| Rule | Detail |
|---|---|
| **Version** | Python **3.14** (target). CI currently runs 3.11–3.13; `pyproject.toml` requires `>=3.11`. New code must remain compatible until the runtime is upgraded. |
| **Typing** | Full typing required on public APIs. Use `from __future__ import annotations` in typed modules. |
| **Dataclasses** | Preferred for DTOs, value objects, and immutable facts. |
| **Frozen dataclasses** | Use `@dataclass(frozen=True)` whenever mutation is not required. |
| **Modules** | Small, cohesive modules with one clear responsibility. |
| **Imports** | Explicit imports only. No wildcard imports. Group: stdlib → third-party → local. |

---

## Architecture

| Pattern | Guidance |
|---|---|
| **Ports before adapters** | Define abstract ports in `application.ports` before implementing infrastructure adapters. |
| **Dependency inversion** | Inner layers never depend on outer layers. Dependencies point inward toward domain meaning. |
| **Immutable DTOs** | Application DTOs and read models are frozen or treated as immutable at boundaries. |
| **Result objects** | Prefer explicit `Result` / success-failure types over ambiguous `None` returns where the codebase provides them. |
| **Domain exceptions** | Raise domain-specific exceptions (`domain.*.errors`); translate to HTTP at the adapter boundary. |

---

## Error handling

- **Never swallow exceptions** without logging and an explicit recovery path.
- **Never return `None` where a `Result` type exists** for that operation.
- **Fail explicitly.** Prefer clear errors over silent defaults that mask educational or data integrity issues.
- Use module loggers: `logger = logging.getLogger(__name__)`.
- Avoid bare `except:`; catch specific exceptions.

---

## Code style

| Tool | Requirement |
|---|---|
| **Ruff** | Must be clean. `ruff check` on touched paths before completion. |
| **Readability** | Readability before cleverness. Self-documenting names over comments. |
| **Comments** | Only for non-obvious business logic or architectural constraints. |
| **Scope** | Implement only what the current milestone asks. No drive-by refactors. |

### Commands

```bash
python -m pytest tests/ -v
ruff check app/ src/ tests/
```

---

## Working rules

1. Read [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) and [`.cursor/PROJECT_INDEX.md`](../PROJECT_INDEX.md) before structural changes.
2. Obey [`.cursor/rules/99-CURRENT_MILESTONE.md`](99-CURRENT_MILESTONE.md) allowed/forbidden scopes literally.
3. Match existing naming, typing, and docstring patterns in the touched package.
4. Do not add dependencies outside the task scope.
5. Leave secrets in environment variables; never commit `.env`.
