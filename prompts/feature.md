# Prompt: Feature Implementation

Use this prompt to start a Kwalitec feature task in Cursor.

---

## Agent instructions

You are working on **Kwalitec**, a Flask adaptive learning platform.

Before coding:

1. Read `PROJECT_CONTEXT.md` and `ARCHITECTURE.md`.
2. Read relevant `.cursor/rules/` (especially architecture, services, curriculum, security).
3. Confirm the feature scope and out-of-scope constraints below.
4. Prefer blueprints for HTTP and services for business logic.
5. Preserve curriculum V1/V2 compatibility if the feature touches syllabuses or topic ordering.

## Feature request

**Title:** \<short name\>

**Goal:** \<what the user should be able to do\>

**In scope:**
- \<paths / layers\>

**Out of scope:**
- \<explicit exclusions\>

**Acceptance criteria:**
- [ ] \<criterion 1\>
- [ ] \<criterion 2\>
- [ ] Tests updated/added
- [ ] `ruff check` clean for touched Python

## Implementation notes

- Match existing patterns in neighbouring modules.
- Do not add dependencies unless necessary and justified.
- Use `CurriculumService` traversal helpers for topic order.
- Keep recommendations/planning deterministic.

## Completion

When done, provide a completion report per `.cursor/rules/07-reporting.mdc` (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance, Technical Debt, Known Limitations). Commit only if asked.
