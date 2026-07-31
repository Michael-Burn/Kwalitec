# Naming Standards

**Programme:** V1S-003  
**Status:** Active  
**Effective:** 2026-07-31

---

## Packages

- Use `snake_case` directory names matching the capability (`learning_strategy`, not `LearningStrategy`).
- Prefer **one noun phrase** for the capability. Avoid stacking synonyms (`educational_experience_engine` vs `educational_experience` — pick one public name).
- Suffixes:
  - `_engine` — deterministic educational authority with `evaluate` / `generate` entry points
  - `_service` — orchestration / I/O facing facade
  - `_adapter` — boundary translation only
  - `_foundation` — shared substrate for a family (not a second authority)

## Twin vocabulary (debt)

Until twin consolidation closes, **do not** create a fourth twin package. Prefer extending `student_twin` (session evidence consumer) or documenting aliases. Target canonical name will be recorded in the package lifecycle matrix when chosen.

## Symbols

- Classes: `PascalCase`
- Functions / modules: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Lifecycle markers: `V1S003_DISPOSITION` / package registry `lifecycle` field — use the Package Lifecycle Policy vocabulary only

## Student-facing language

Engineering package names must **not** appear in student copy. Follow `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` and `app/presentation/product_language.py`.

## Tests

- Programme suites: `tests/test_<programme_id>_*.py` (e.g. `test_v1s003_repository_health.py`)
- Architecture: `tests/architecture/`
- Avoid duplicate suite names that re-test the same behaviour under different programme prefixes without a delta.

## Forbidden patterns

- `utils.py` god modules without a domain noun
- Parallel packages that differ only by version suffix (`*_v2`) on the student spine — versioned packages require an explicit ARCHIVE lifecycle
- Reusing rejected product synonyms in code comments that may leak to UI strings
