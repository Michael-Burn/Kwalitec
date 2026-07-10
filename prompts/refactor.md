# Prompt: Architecture-Safe Refactor

Use this prompt for refactors that must not change product behaviour.

---

## Agent instructions

You are refactoring **Kwalitec** without altering external behaviour unless explicitly allowed.

Rules:

1. Read `ARCHITECTURE.md` and `.cursor/rules/01-architecture.mdc`.
2. Keep blueprint → service → model/engine layering intact.
3. Preserve curriculum V1/V2 behaviour and canonical traversal.
4. Do not change routes, templates, or public URLs unless the task says so.
5. Run the relevant existing tests before and after when behaviour could regress.
6. Prefer incremental moves (extract function/module) over large rewrites.

## Refactor request

**Goal:** \<why this refactor is needed\>

**Target modules:**
- \<paths\>

**Allowed changes:**
- \<e.g. extract helper, rename internal symbol, split module\>

**Forbidden changes:**
- \<e.g. schema, API URLs, recommendation formulas\>

**Behaviour lock:**
- Existing tests in \<modules\> must still pass.
- Manual checks: \<optional\>

## Verification

```bash
python -m pytest tests/<relevant> -v
ruff check app/ tests/
```

## Completion

Report behavioural equivalence, files touched, tests executed, Migration Impact (usually None), Architecture Compliance, and any residual debt. Commit only if asked.
