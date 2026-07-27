# Code Review Checklist

**Document ID:** ENG-STD-004  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** Authors and reviewers  
**Related:** [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md), [`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md), [`TESTING_STANDARD.md`](TESTING_STANDARD.md)

---

## Purpose

Use this checklist before approving a pull request. Mark each section **Pass / Fail / N/A**. Failures block merge unless waived with written rationale.

---

## Architecture

- [ ] Layering preserved: Presentation → Application → Domain ← Infrastructure (ports)
- [ ] Application does not import Infrastructure
- [ ] Routes remain thin; no planning/mastery/recommendation math in blueprints
- [ ] Models / domain do not import blueprints or templates
- [ ] Curriculum ordering uses `CurriculumService` / approved traversal helpers
- [ ] Curriculum V1 and V2 compatibility preserved when curriculum paths touched
- [ ] No architectural shortcuts around ports, composition roots, or authorities
- [ ] Invariants in [`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md) hold

## Business logic

- [ ] Logic lives in services / application use cases with explicit arguments
- [ ] No Flask request/session globals inside domain or core services
- [ ] Behaviour matches the milestone success criteria only (no scope creep)
- [ ] Edge cases and failure modes handled without silent data corruption
- [ ] Idempotent paths remain safe to re-run (import, startup, admin bootstrap)

## Security

- [ ] Authenticated views use `@login_required` (or equivalent)
- [ ] Personal resources scoped to the current user; no IDOR
- [ ] WTForms / server-side validation for POST bodies
- [ ] No secrets committed; no passwords or full DB URLs logged
- [ ] CSRF preserved outside tests; open redirects rejected
- [ ] ORM / bound parameters only — no concatenated SQL from user input

## Testing

- [ ] Tests cover the changed behaviour (unit and/or integration as appropriate)
- [ ] Architecture tests updated or still green when boundaries change
- [ ] No weakened assertions to force green
- [ ] Regression risk for Twin / Reasoning / Mission / Tutor considered
- [ ] Commands in the PR test plan were actually run

## Performance

- [ ] No obvious N+1 queries on hot student paths
- [ ] No unbounded loops or unbounded payloads in request handlers
- [ ] Heavy work not smuggled into template rendering
- [ ] Static/asset budgets respected when JS/CSS layout changes

## Naming

- [ ] Names match educational vocabulary (Twin, Mission, Assessment, Reasoning)
- [ ] Files and symbols follow existing package conventions
- [ ] No misleading names that imply recommendation/ranking when only ordering

## Documentation

- [ ] Milestone completion report present when required
- [ ] ADR or architecture notes updated when boundaries change
- [ ] Changelog entry prepared when the change is user-visible or ship-bound
- [ ] Comments explain non-obvious *why*, not narrate *what*

## Educational correctness

- [ ] Evidence precedes inference
- [ ] Deterministic educational decisions (no hidden randomness / no LLM in reasoning)
- [ ] Twin remains sole learner-state authority; no parallel shadow state
- [ ] Mission Engine consumes decisions; does not invent educational reasoning
- [ ] Tutor explains; does not re-reason
- [ ] Assessment produces observations only
- [ ] Curriculum Retrieval is the evidence interface used (no ad-hoc syllabus scraping)

## Explainability

- [ ] Student-facing suggestions traceable to data and declared rules
- [ ] Copy does not overclaim certainty
- [ ] Explainability review completed when intelligence surfaces changed
- [ ] Recommendation review completed when ranking/selection changed

## UI consistency

- [ ] Matches existing layouts, tokens, and brand patterns for the surface
- [ ] No drive-by redesign outside milestone scope
- [ ] Error and empty states honest and actionable

## Accessibility

- [ ] Forms labelled; controls keyboard-reachable for changed UI
- [ ] Contrast and focus behaviour preserved for changed components
- [ ] Meaningful page titles / headings where structure changed

## Maintainability

- [ ] Small, cohesive change; no unrelated refactor
- [ ] No new dependencies without clear need
- [ ] Future readers can locate ownership of the behaviour
- [ ] Technical debt introduced is named in the completion report

---

## Reviewer decision

| Decision | When |
|---|---|
| Approve | All applicable items Pass or justified N/A |
| Request changes | Any Fail without waiver |
| Escalate | Invariant conflict or educational-authority dispute |

Reviewers should prefer under-claiming educational benefit over approving opaque intelligence.
