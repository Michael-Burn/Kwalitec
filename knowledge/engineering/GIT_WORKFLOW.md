# Git Workflow

**Document ID:** ENG-STD-007  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** Engineers and AI agents  
**Related:** [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md), [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md), [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md), [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

---

## Purpose

This document owns branch strategy, naming, commits, pull requests, protection rules, tags, and how they connect to releases. End-to-end delivery sequence lives in [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md).

---

## Branch strategy

| Branch | Purpose |
|---|---|
| `main` | Protected integration branch; CI must pass |
| `milestone/<id>-<slug>` | Preferred for scoped milestone work |
| `feature/<slug>` | Product/capability work outside a numbered milestone |
| `fix/<slug>` | Bug fixes |
| `chore/<slug>` | Tooling, docs-only, dependency bumps |

Guidelines:

- Prefer short-lived branches merged via pull request.
- Keep one capability (or one docs pack) per branch.
- Documentation-only milestones must not touch application source.
- Never force-push `main`.

---

## Branch naming convention

```
<type>/<descriptor>
```

Examples:

```
milestone/eng-001-engineering-standards
feature/assessment-observation-pipeline
fix/twin-cold-start-honesty
chore/eng-001-engineering-standards
```

Rules:

- Lowercase kebab-case descriptors
- Include programme/milestone id when one exists
- Avoid personal names and vague labels (`temp`, `wip`, `stuff`)

---

## Commit message conventions

Prefer Conventional Commits:

```
<type>(optional-scope): <short summary>
```

Common types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`.

Rules:

- Imperative mood (“add”, “fix”, “establish”)
- Explain **why** in the body when non-obvious
- Milestone briefs may mandate an exact subject — use it verbatim
- Never commit secrets
- Do not use `--no-verify` unless explicitly instructed
- Commit only when asked or when the milestone requires it

Example:

```bash
git add knowledge/engineering/
git commit -m "$(cat <<'EOF'
docs(engineering): establish engineering standards and development governance

EOF
)"
```

### Staging discipline

- For documentation-only milestones, stage **only** docs/rules/prompts.
- Review `git status` / `git diff` before commit.
- Prefer path-specific `git add` when the working tree contains mixed work.

---

## Pull requests

Every PR should include:

1. **Summary** — what changed and why
2. **Scope check** — out-of-scope areas untouched
3. **Test plan** — commands run
4. **Migration notes** — Alembic revisions or “none”
5. **Architecture notes** — especially curriculum V1/V2 and Educational Intelligence authorities

CI expectations:

- `pytest` on supported Python versions
- `ruff check` on application/test paths per workflow
- No merge with failing CI without documented exception

Use [`CODE_REVIEW_CHECKLIST.md`](CODE_REVIEW_CHECKLIST.md) during review.

```bash
git push -u origin HEAD
gh pr create --title "docs(engineering): …" --body "…"
```

---

## Branch protection

`main` is protected. Required practice:

- Changes enter via pull request
- Required status checks must pass
- No force-push to `main`
- No direct commits to `main` except emergency process explicitly authorised by maintainers
- Reviews required for behavioural and architectural changes (docs-only may follow lighter review if repository settings allow)

---

## Version tags

Release tags follow semantic versioning ([`VERSIONING_POLICY.md`](VERSIONING_POLICY.md)):

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

Rules:

- Tag only release commits that pass [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md)
- Tags are immutable; fix-forward with a new patch/minor/major
- Tag must match `VERSION` / `pyproject.toml` / `APP_VERSION`

---

## Release process (git view)

1. Merge ship-ready PRs to `main`
2. Verify release gates (pytest, Ruff, Alembic, architecture, changelog)
3. Align version identity files
4. Create annotated tag `vX.Y.Z`
5. Create GitHub Release for that tag
6. Deploy and verify fingerprint per detailed release procedure

Git operations do not replace educational or architecture verification.

---

## Forbidden practices

- Force-push to `main`
- Rewriting published release tags
- Committing `.env` or credentials
- Interactive rebase flags unsupported in automation when avoidable for shared branches
- Using `--no-verify` to bypass hooks without explicit instruction
- Mixing unrelated application WIP into a documentation-only commit
