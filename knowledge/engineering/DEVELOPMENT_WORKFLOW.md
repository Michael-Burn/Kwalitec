# Development Workflow

**Document ID:** ENG-STD-002  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** Engineers and AI agents delivering capabilities  
**Related:** [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md), [`TESTING_STANDARD.md`](TESTING_STANDARD.md), [`CODE_REVIEW_CHECKLIST.md`](CODE_REVIEW_CHECKLIST.md), [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md), [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

---

## Purpose

This document defines the standard end-to-end workflow for every capability. Git naming and commit conventions live in [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md); this document owns the sequence of work.

---

## Standard flow

```
Feature branch
      ↓
Engineering Design Pack
      ↓
Implementation
      ↓
Testing
      ↓
Architecture review
      ↓
Pull Request
      ↓
Merge
      ↓
Release
```

Skip a stage only when the milestone explicitly allows it (for example, documentation-only packs may omit implementation). Do not invent alternate flows for convenience.

---

## 1. Feature branch

Create a short-lived branch from an up-to-date `main`.

```bash
git checkout main
git pull origin main
git checkout -b feature/<slug>
# or: milestone/<id>-<slug> | fix/<slug> | chore/<slug>
```

Confirm scope before coding: in-scope paths, out-of-scope constraints, and success criteria from the milestone brief.

---

## 2. Engineering Design Pack

Before non-trivial implementation, produce a design pack sufficient for review:

| Artefact | Required when |
|---|---|
| Problem / student impact statement | Product-facing change |
| Affected bounded contexts and authorities | Any educational or architectural change |
| Layer plan (Presentation → Application → Domain → Infrastructure) | Structural change |
| Data / migration impact | Schema or durable state change |
| Curriculum V1/V2 impact | Curriculum traversal or import change |
| Explainability notes | Student-facing intelligence |
| Test plan | Always for behavioural change |
| Explicit non-goals | Always |

Documentation-only milestones may replace the design pack with the brief itself when scope is purely governance docs.

Do not implement architectural invention during coding that was not approved in design (or an ADR).

---

## 3. Implementation

Implement the smallest change that satisfies the success criteria.

```bash
# typical local loop
source .venv/bin/activate
# edit only in-scope paths
ruff check app/ src/ tests/   # when code changes
```

Rules during implementation:

- Obey [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md) and [`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md).
- Keep routes thin; put logic in services/application.
- Do not expand into the next milestone.
- Leave unrelated WIP untouched.

---

## 4. Testing

Run the test plan defined in [`TESTING_STANDARD.md`](TESTING_STANDARD.md).

```bash
python -m pytest tests/ -v
# focused suites as applicable, e.g.:
python -m pytest tests/architecture/ -v
ruff check app/ src/ tests/
```

Do not weaken assertions to force green. Fix the code or update tests with a clear reason.

---

## 5. Architecture review

Self-review (and peer review when required) against:

- [`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md)
- [`CODE_REVIEW_CHECKLIST.md`](CODE_REVIEW_CHECKLIST.md) — Architecture and Educational correctness sections
- Curriculum V1/V2 loadability when curriculum paths changed

Stop and redesign if an invariant would be broken.

---

## 6. Pull Request

```bash
git push -u origin HEAD
gh pr create --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary
- …

## Scope check
- Out-of-scope areas untouched: …

## Test plan
- [ ] pytest
- [ ] ruff
- [ ] architecture tests (if applicable)

## Migration notes
- none | revision id …

## Architecture notes
- curriculum V1/V2: …
EOF
)"
```

CI must be green unless an explicit, documented exception exists. See [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) for PR and branch-protection rules.

---

## 7. Merge

Merge only after review approval and required checks. Prefer merge commits or the repository’s protected-branch policy; never force-push `main`.

```bash
# after approval — typically via GitHub UI or:
gh pr merge --merge
git checkout main
git pull origin main
```

Delete the feature branch after merge when local cleanup is needed:

```bash
git branch -d feature/<slug>
git push origin --delete feature/<slug>
```

---

## 8. Release

Releases follow [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md) and version rules in [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md). Not every merged PR is a release; release when the agreed ship set is complete and gates pass.

---

## Documentation-only workflow

When the milestone forbids application changes:

1. Branch as usual (`chore/` or `milestone/`).
2. Design pack may be the brief.
3. Create/update only documentation (and explicitly allowed governance paths).
4. Validation: confirm no application diff; run pytest if the brief requires it.
5. PR → merge → optional docs-noted release (usually patch or no version bump per [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md)).

---

## Stop conditions

**STOP** the workflow and escalate when:

- An architecture invariant would be violated
- Educational reasoning would require an LLM or hidden heuristic
- Scope expands beyond the milestone
- Tests fail for reasons outside the change and cannot be honestly excluded
