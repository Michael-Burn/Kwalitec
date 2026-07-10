# Contributing to Kwalitec

Thank you for contributing. This guide defines how humans and AI agents change the codebase safely. Product and architecture orientation: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable integration branch; CI must pass |
| `milestone/<id>-<slug>` | Preferred for scoped milestone work (e.g. `milestone/0.1-ai-infra`) |
| `feature/<slug>` | Optional for small features outside a numbered milestone |
| `fix/<slug>` | Bug fixes |
| `chore/<slug>` | Tooling, docs-only, dependency bumps |

Guidelines:

- Prefer short-lived branches merged via pull request.
- Do not force-push `main`.
- Keep milestone branches focused on the milestone’s stated scope.
- Documentation-only milestones must not touch application source.

---

## Commit Message Format

Use concise, imperative subjects. Prefer Conventional Commit prefixes when they fit:

```
<type>: <short summary>
```

Common types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`.

Milestone completion commits may use the explicit milestone title when required by the milestone brief, for example:

```
Milestone 0.1 - Establish AI development infrastructure
```

Rules:

- Explain **why** in the body when the change is non-obvious.
- Never commit secrets (`.env`, credentials, private keys).
- Do not use `--no-verify` unless explicitly instructed.
- Do not amend pushed commits unless explicitly instructed and safe.

---

## Pull Request Expectations

Every PR should include:

1. **Summary** — what changed and why (1–3 bullets).
2. **Scope check** — confirm out-of-scope areas were not modified.
3. **Test plan** — commands run and scenarios checked.
4. **Migration notes** — if Alembic revisions are included (or “none”).
5. **Architecture notes** — especially for curriculum V1/V2 impact.

CI expectations (see `.github/workflows/ci.yml`):

- `pytest` on Python 3.11, 3.12, 3.13
- `ruff check app/ tests/`
- Deploy dry-run checks on `main`

Do not merge with failing CI without an explicit, documented exception.

---

## Coding Conventions

| Area | Convention |
|---|---|
| Python version | 3.11+ |
| Imports | `from __future__ import annotations` in modules that use modern typing |
| Style | Match surrounding code; ruff for lint (`E`, `F`, `I`, `N`, `W`, `UP`) |
| Quotes | Double quotes (ruff format config) |
| Docstrings | Prefer clear Args/Returns on public service methods |
| HTTP | Blueprints only |
| Business logic | Services only |
| Persistence | SQLAlchemy models + Alembic |
| Templates | Jinja2 under `app/templates/` mirroring feature folders |

Avoid:

- Drive-by refactors unrelated to the task
- New dependencies without a clear need
- Editing generated or cache directories (`.venv`, `__pycache__`, `.pytest_cache`)

Detailed rules: `.cursor/rules/02-python.mdc`, `03-flask.mdc`, `04-services.mdc`.

---

## Testing Expectations

Before claiming a change is complete:

```bash
python -m pytest tests/ -v
ruff check app/ tests/
```

When changing curriculum behaviour:

- Run V1-related tests (`test_curriculum_engine.py`, importer/integration as applicable).
- Run V2/section-aware tests (`test_curriculum_engine_v2.py`, `test_curriculum_section_aware.py`, section/topic relationship tests).

When changing auth, startup, or config:

- Include the corresponding focused test modules.

Do not weaken assertions to make tests pass. Fix the code or update tests with a clear reason.

---

## Architecture Rules

1. **Blueprints → Services → Models/Engine** — never invert.
2. **Curriculum traversal** — use `CurriculumService.get_all_topics_ordered` (and related helpers); do not invent parallel ordering.
3. **V1 compatibility** — preserve flat curricula and nullable `section_id`.
4. **V2 canonical hierarchy** — Section → Topic → Learning Objective; weights at section level.
5. **Determinism** — no hidden randomness in planning/recommendation cores.
6. **Idempotent imports/startup** — safe to re-run.
7. **No public registration** — admin bootstrap only.

See `.cursor/rules/01-architecture.mdc` and `08-curriculum-v2.mdc`.

---

## AI Development Workflow

Cursor Agent sessions should treat the following as permanent project memory:

| Asset | Role |
|---|---|
| `PROJECT_CONTEXT.md` | Product + status orientation |
| `ARCHITECTURE.md` | Structural map |
| `CONTRIBUTING.md` | This workflow |
| `.cursor/rules/*.mdc` | Enforceable conventions |
| `prompts/*.md` | Task-start templates |

Recommended loop:

1. Open the matching prompt under `prompts/` (feature, bugfix, refactor, migration, review).
2. Confirm milestone constraints (especially “do not modify …” lists).
3. Implement the smallest change that satisfies the success criteria.
4. Run the relevant tests/linters.
5. Produce a completion report if the milestone requires one (see `.cursor/rules/07-reporting.mdc`).
6. Commit/PR only when asked or when the milestone completion steps require it.

Agents must not:

- Expand scope into the next milestone unprompted
- Modify application code during documentation-only milestones
- Skip architecture compliance notes for curriculum changes

---

## Milestone Workflow

Milestones are the primary delivery unit.

### Starting a milestone

1. Read the milestone brief completely.
2. List in-scope and out-of-scope paths.
3. Identify which rules/prompts apply.
4. Implement only in-scope artefacts.

### Completing a milestone

Unless the brief says otherwise, completion typically requires:

1. Verify scope compliance (only allowed files changed).
2. Run required verification (tests if code changed; file inventory if docs-only).
3. Write a completion report with the standard sections:
   - Summary
   - Files Created
   - Files Modified
   - Tests Executed
   - Migration Impact
   - Architecture Compliance
   - Technical Debt
   - Known Limitations
4. Stage and commit as specified by the milestone.
5. **STOP** — do not start the next milestone unless asked.

### Documentation-only milestones

- Create/update docs and `.cursor` / `prompts` only.
- Leave existing application WIP untouched and unstaged unless the brief says otherwise.
- Still produce the completion report and commit hash.

---

## Local Setup (quick reference)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
flask db upgrade
flask create-admin
flask run
```

Full setup: [README.md](README.md).

---

## Security Notes for Contributors

- Never commit `.env` or real credentials.
- Do not log passwords or full connection strings.
- Prefer parameterized SQLAlchemy queries; avoid string-built SQL.
- Preserve CSRF on forms; keep `WTF_CSRF_ENABLED` true outside tests.

Details: `.cursor/rules/10-security.mdc`.
