# Repository Standards

**Programme:** V1S-003 — Engineering Quality & Repository Simplification  
**Status:** Active  
**Effective:** 2026-07-31  
**Authority:** V1S-003 · `docs/ENGINEERING_CHARTER.md` · `ARCHITECTURE.md`

---

## Purpose

Define how the Kwalitec repository is organised so engineers can navigate, extend, and maintain it without guessing which tree or package is authoritative.

---

## Canonical trees

| Path | Role | Dogfood authority? |
|---|---|---|
| `app/` | Commercial Flask product | **Yes** |
| `src/` | Education OS (APP-003) parallel library | No — MAINTENANCE / archive candidate |
| `tests/` | Verification | N/A |
| `docs/` | Engineering governance | N/A |
| `docs/engineering/` | App-facing engineering standards (V1S-003) | N/A |
| `knowledge/` | Product / educational / constitutional law | N/A |
| `migrations/` | Schema truth | N/A |

**Rule:** New student-facing educational capabilities ship under `app/` unless a programme explicitly adopts `src/` as product runtime.

**Rule:** Do not dual-implement the same capability in `app/` and `src/`.

---

## Root hygiene

- Keep at the repository root: `README.md`, `ARCHITECTURE.md`, `PRODUCT_BLUEPRINT.md`, `PROJECT_CONTEXT.md`, `CONTRIBUTING.md`, `V1_RELEASE_CRITERIA.md`, active `V1S*_IMPLEMENTATION_REPORT.md` for the current stabilisation train.
- Completed programme reports move under `docs/reports/` (or `knowledge/archive/`) once superseded.
- Never commit `.env`, credentials, or private keys.

---

## Package map

Every package under audit must appear in `app/services/package_lifecycle.py` with:

1. **One path**
2. **One responsibility**
3. **One owner**
4. **One lifecycle** (`ACTIVE` | `MAINTENANCE` | `DEPRECATED` | `ARCHIVED` | `REMOVE`)

Founder observability: `/founder/v1-readiness` → Repository Health / Package Lifecycle.

---

## Layering (app/)

```
Templates / static
        ↓
Presentation blueprints (app/presentation, legacy shells)
        ↓
Application engines + app/services orchestration
        ↓
Domain (app/domain) + Curriculum engine (app/curriculum)
        ↓
Infrastructure adapters + models + DB
```

HTTP handlers must not own planning / mastery / recommendation math.  
Presentation must consume educational authorities, not reimplement them.

---

## Related standards

| Document | Covers |
|---|---|
| [NAMING_STANDARDS.md](NAMING_STANDARDS.md) | Package and symbol naming |
| [MODULE_STANDARDS.md](MODULE_STANDARDS.md) | Module size and responsibility |
| [DEPENDENCY_RULES_APP.md](DEPENDENCY_RULES_APP.md) | Import direction for `app/` |
| [PACKAGE_LIFECYCLE_POLICY.md](PACKAGE_LIFECYCLE_POLICY.md) | Lifecycle transitions |
| [../DEPENDENCY_RULES.md](../DEPENDENCY_RULES.md) | Import direction for `src/` |
| [../ENGINEERING_CHARTER.md](../ENGINEERING_CHARTER.md) | Engineering principles |
