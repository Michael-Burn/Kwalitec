# Prompt: Code Review

Use this prompt to review a Kwalitec change set (PR, branch, or local diff).

---

## Agent instructions

You are reviewing changes for **Kwalitec**.

Review against:

1. `PROJECT_CONTEXT.md` / `ARCHITECTURE.md` / `CONTRIBUTING.md`
2. `.cursor/rules/` — especially architecture, services, curriculum V1/V2, security, testing
3. Milestone scope if provided (flag out-of-scope edits)

## Review target

**Branch / PR / diff:** \<identifier\>

**Intended milestone or goal:** \<text\>

**Focus areas (optional):** \<curriculum / auth / migrations / UI\>

## Review checklist

### Correctness
- [ ] Logic matches the stated goal
- [ ] Edge cases and empty states handled
- [ ] Errors logged/handled appropriately

### Architecture
- [ ] Blueprints stay thin; services own business rules
- [ ] No layer violations (models↔routes, request in services)
- [ ] Curriculum traversal uses `CurriculumService` helpers
- [ ] V1 compatibility preserved when syllabus/schema touched

### Security
- [ ] AuthZ scoping to current user
- [ ] CSRF / validation intact
- [ ] No secrets in code or logs
- [ ] SQL remains parameterized

### Tests & quality
- [ ] Tests cover new behaviour / regressions
- [ ] Ruff-clean expectations met
- [ ] Migrations coherent with models

### Product
- [ ] Deterministic learning paths not replaced with opaque AI
- [ ] User-facing copy/templates consistent with existing UI patterns

## Output format

1. **Verdict:** Approve / Approve with nits / Request changes
2. **Findings:** ordered by severity (blocker → nit), with file references
3. **Questions:** anything ambiguous
4. **Test gaps:** missing coverage
5. **Migration / architecture notes:** if relevant

Do not implement fixes unless explicitly asked after the review.
