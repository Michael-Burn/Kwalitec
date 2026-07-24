# Kwalitec Engineering Standards

**Version:** 1.0  
**Status:** Active  
**Authority:** Engineering practice (subordinate to Vision, Blueprint, Architecture Constitutions)  
**Related:** `knowledge/GOVERNANCE.md`, `docs/ENGINEERING_CHARTER.md`, `CONTRIBUTING.md`, `knowledge/engineering/handbook/ENG-001_ENGINEERING_HANDBOOK.md`

This standard is the permanent engineering bar for Pull Requests after Architecture Consolidation.

It does **not** redesign the Educational OS, Twin, or educational algorithms.

---

## 1. Architecture rules

1. **Layering (Flask `app/`):** Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON.
2. **Layering (EOS `src/`):** Domain → Application → Infrastructure → Web adapters — obey `docs/DEPENDENCY_RULES.md` and Architecture Constitution.
3. Routes must not contain planning, mastery, readiness, or recommendation math.
4. Services must not depend on `flask.request` / session globals; take explicit arguments.
5. Models must not import blueprints or templates.
6. Curriculum ordering goes through `CurriculumService` helpers / canonical traversal ADRs.
7. **One Educational Truth / One Runtime / One Navigation / One Educational State** (Vision 2030 engineering principles).
8. Application factory (`create_app`) remains the only app construction path.
9. Schema changes go through Alembic under `migrations/versions/`.
10. V1 and V2 curricula must both remain loadable and traversable.
11. No duplicate educational logic; no hidden calculations; no unexplained recommendations.
12. Do not invent black-box LLM calls into core learning paths (ADR-008 AI enrichment boundary).

Anti-patterns: god routes/services; duplicating topic ordering; treating engine dataclasses as ORM models (or vice versa); feature work that silently breaks flat (V1) curricula.

---

## 2. Coding standards

- Prefer existing naming, typing, and docstring patterns in the touched package.
- Python: explicit types on new public functions; avoid unnecessary comments.
- Match repository style (ruff-clean for changed files).
- Prefer small, focused diffs; no drive-by refactors.
- Secrets only in environment variables; never commit `.env`.
- Full conventions: `knowledge/development/coding-standards.md`, `.cursor/rules/10-ENGINEERING.md`.

---

## 3. Testing requirements

| Change type | Minimum |
|---|---|
| Behaviour change | Unit and/or integration tests that fail without the fix |
| Architecture / layering | `tests/architecture/` green |
| Student HTTP surfaces | Relevant presentation / operational / GA tests as applicable |
| Curriculum | V1 and V2 load/traversal coverage if loaders touched |
| Release candidate | Full `pytest` + GA package when tagging |

- Deterministic educational cores must remain reproducible from the same inputs.
- Do not weaken tests to force green without product owner agreement.
- CI must be green on pytest + ruff unless an explicit exception is documented.

---

## 4. Accessibility

For any UI-impacting change:

- Keyboard path reaches primary actions
- Landmarks present on changed shells
- Visible focus retained
- `prefers-reduced-motion` respected for new animation
- Meaningful text alternatives for charts that convey educational meaning

Reference: `docs/production/ACCESSIBILITY_AUDIT.md`, Quality Manual.

---

## 5. Security

- Flask-Login; `@login_required` on authenticated views; login view `auth.login`.
- Registration is not publicly exposed.
- Scope queries to the current user for personal resources.
- Reject open redirects (local `next` only).
- Prefer WTForms for POST; server-side validation always.
- CSRF enabled outside tests; preserve security headers / CSP behaviour.
- ORM or bound parameters only — never concatenate user input into SQL.
- Treat new network calls / third-party script CDNs as CSP-sensitive.
- Reference: `.cursor/rules/10-security.mdc`, `docs/ga/SECURITY_REVIEW.md`.

---

## 6. Documentation

| Change | Documentation expectation |
|---|---|
| Feature | PRD (`knowledge/prd/`) before significant work; update user/ops docs if behaviour changes |
| Architecture boundary | ADR + ADR index update |
| Public behaviour | Product language compliance |
| Milestone | Completion report when required |
| Governance-only | Update readiness / debt / playbooks as needed — no silent doc drift |

Prefer linking Vision / Blueprint over copying philosophy text.

---

## 7. Logging

- Use existing observability patterns (`kwalitec.observability` / structured logs where present).
- Never log passwords, session cookies, or full DB URLs with credentials.
- Prefer actionable messages; avoid PII beyond what operations already require.
- Slow-request / SQL profiling hooks: follow `docs/ga/PERFORMANCE_BASELINE.md` (`PROFILE_SQL`, thresholds).

---

## 8. Performance budgets

Soft CI budgets (not production SLOs) — from GA Performance Baseline:

| Surface | Response budget (ms) | SQL budget |
|---|---:|---:|
| Student Dashboard `/student/` | 2500 | 80 |
| Session overview | 2500 | — |
| Journey `/student/journey` | 2500 | 80 |
| Console Home `/console/` | 3500 | 120 |
| Platform Intelligence | 3500 | 120 |
| Health live | 500 | — |
| Health ready | 1500 | 40 |

PRs that knowingly regress budgets need justification and Quality Manual / debt register entry.

---

## 9. Pull Request checklist

Every PR must satisfy:

- [ ] **Tests** — relevant automated tests added/updated and green
- [ ] **Documentation** — PRD/ADR/user docs as required; no contradictory philosophy
- [ ] **Accessibility** — UI gates above (or N/A documented)
- [ ] **Security** — authz, CSRF, input, secrets, SQL safety reviewed
- [ ] **Performance** — budgets considered; no unjustified N+1 on hot paths
- [ ] **Architecture** — layering, one educational truth, Vision/Blueprint alignment

PR description should include summary, test plan, migration impact, and curriculum/architecture notes when relevant.

---

## 10. Definition of Done

A change is **Done** when:

1. Scope matches the approved PRD or task (no silent scope creep).
2. Vision Final Test passes for product behaviour.
3. Architecture invariants hold (especially curriculum V1/V2 and no second educational brain).
4. Required tests and ruff pass (or docs-only N/A).
5. Accessibility / security / performance gates for the change type are met.
6. Documentation and ADR/index updates (if needed) are merged with the change.
7. Technical debt newly accepted is recorded in `docs/TECHNICAL_DEBT_REGISTER.md`.
8. Completion report produced when the milestone requires it.

Handbook detail: ENG-001 Chapter 16.

---

## 11. Explicit non-goals of this standard

- Redesigning the application UX
- Introducing new educational features
- Modifying Student Digital Twin or EducationalStateService
- Changing educational algorithms

When uncertain: STOP → Document → Recommend (Governance §3.3).
