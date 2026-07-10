# AI Development Workflow

How ChatGPT, Cursor, and humans collaborate on Kwalitec milestones. Permanent memory assets:

| Asset | Role |
|---|---|
| [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) | Product + status orientation |
| [`ARCHITECTURE.md`](../../ARCHITECTURE.md) | Structural map |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | Branching, PRs, milestones |
| [`knowledge/`](../README.md) | ADRs, subsystems, this workflow |
| [`.cursor/rules/`](../../.cursor/rules/) | Enforceable agent conventions |
| [`prompts/`](../../prompts/) | Task-start templates |

## ChatGPT responsibilities

ChatGPT (or equivalent planning chat outside the repo) is best used for:

- Drafting milestone briefs and success criteria
- Exploring product options before coding
- Reviewing completion reports for clarity
- Helping authors write ADRs or subsystem outlines that Cursor will land in-repo

ChatGPT should **not** be treated as the source of truth for repository state. Prefer pasting concrete paths, constraints, and “do not modify” lists into Cursor prompts. Do not invent Kwalitec APIs that contradict `knowledge/` or `ARCHITECTURE.md`.

## Cursor responsibilities

Cursor Agent implements against the live tree:

1. Read `PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, relevant `knowledge/` docs, and `.cursor/rules/`.
2. Open a matching prompt under `prompts/` (`feature`, `bugfix`, `refactor`, `migration`, `review`) when starting structured work.
3. Obey milestone scope and literal “do not modify …” constraints.
4. Prefer services over routes; prefer `CurriculumService` traversal helpers.
5. Run required tests/linters for code milestones.
6. Produce a completion report when the milestone requires one.
7. Commit **only** when the user or milestone completion steps explicitly require it.

Cursor must not expand into the next milestone unprompted, modify application code during documentation-only milestones, or introduce LLM calls into core learning paths.

## Milestone workflow

```
Brief ready
    → read brief + list in-scope / out-of-scope paths
    → identify ADRs / subsystem docs / rules that apply
    → implement smallest change that meets success criteria
    → verify (tests or docs inventory)
    → completion report
    → stage + commit as specified
    → STOP
```

### Documentation-only milestones

- Touch only allowed doc / rules / prompt paths.
- Leave unrelated application WIP **unstaged**.
- Still produce the completion report and commit hash when required.

### Code milestones

- Respect layering ([ADR-001](../architecture/ADR-001-service-layer.md), [ADR-002](../architecture/ADR-002-blueprint-architecture.md)).
- Curriculum work: dual V1/V2 tests ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md), [ADR-005](../architecture/ADR-005-testing-strategy.md)).
- Schema changes: Alembic only under `migrations/versions/`.

## Review workflow

1. Prefer the `prompts/review.md` template for structured review sessions.
2. Check scope compliance first (wrong files changed?).
3. Check architecture invariants: thin routes, service placement, canonical traversal, V1 compatibility.
4. Check security: authz scoping, CSRF, secrets, open redirects.
5. Check tests: new behaviour covered; curriculum dual-path if relevant.
6. Do not merge with failing CI without an explicit, documented exception.

Human reviewers remain accountable for product judgement; agents assist with consistency against documented ADRs.

## Completion workflow

Unless the brief says otherwise:

1. Verify only allowed files changed (`git status` / path inventory).
2. Run verification (pytest/ruff for code; file list for docs-only).
3. Write the completion report with **all** required sections:

   - Summary  
   - Files Created  
   - Files Modified  
   - Tests Executed  
   - Migration Impact  
   - Architecture Compliance  
   - Technical Debt  
   - Known Limitations  

4. Stage and commit with the milestone’s mandated message when required.
5. Include the commit hash in the report when a commit was made.
6. **STOP** — do not start the next milestone unless asked.

## Prompt map

| Situation | Start with |
|---|---|
| New feature | `prompts/feature.md` |
| Bug | `prompts/bugfix.md` |
| Refactor | `prompts/refactor.md` |
| Schema / Alembic | `prompts/migration.md` |
| Review | `prompts/review.md` |

**See also:** [`CONTRIBUTING.md`](../../CONTRIBUTING.md) “AI Development Workflow” and “Milestone Workflow”, `.cursor/rules/07-reporting.mdc`.
