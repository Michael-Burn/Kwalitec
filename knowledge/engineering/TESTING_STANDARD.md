# Testing Standard

**Document ID:** ENG-STD-005  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** Engineers and AI agents  
**Related:** [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md), [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md), [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

---

## Purpose

This standard defines the kinds of tests Kwalitec expects and the bar for merging. Prefer tests that validate externally observable behaviour and architectural law over brittle implementation coupling.

---

## Test categories

### Unit tests

- Scope: pure domain rules, service helpers, and isolated functions.
- Dependencies: none or lightly faked; no live HTTP.
- Expectation: deterministic; fast; name the educational rule under test when relevant.

### Integration tests

- Scope: application use cases with real (or test-double) persistence, Flask test client journeys, curriculum import/traversal.
- Expectation: prove wiring across layers without requiring production infrastructure.
- Auth, startup, and config changes need focused integration coverage.

### Regression tests

- Scope: lock known bugs and stabilisation fixes so they cannot silently return.
- Expectation: fail clearly if the defect reappears; do not delete without replacing equivalent protection.

### Snapshot tests

- Scope: golden outputs for templates, explainability payloads, or structured educational responses where exact shape matters.
- Expectation: regenerate only when the change is intentional and reviewed; never regenerate to hide unintended drift.

### Architecture tests

- Scope: layer import rules, authority boundaries, forbidden couplings (for example Application → Infrastructure).
- Location: typically `tests/architecture/`.
- Expectation: required green for structural PRs and for every release ([`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md)).

### Performance tests

- Scope: budgets and hot-path checks (query patterns, static asset budgets, unacceptable algorithmic blow-ups).
- Expectation: add or update when a change risks student-facing latency or CI budget harnesses; do not claim performance without evidence.

---

## Educational testing expectations

When changing Twin, Reasoning, Mission, Tutor, Assessment, Learning Graph, or Curriculum Retrieval:

| Concern | Required coverage |
|---|---|
| Determinism | Same inputs → same educational outputs |
| Authority | Wrong layer does not invent Twin/Reasoning decisions |
| Evidence-before-inference | Missing evidence does not fabricate mastery/readiness |
| Curriculum V1/V2 | Both remain loadable/traversable when curriculum code changes |
| Explainability | Explanations remain attached to decisions when intelligence changes |

---

## Expectations before merge

Authors must:

1. Run relevant automated tests locally (full suite preferred; focused suite minimum with rationale).
2. Keep architecture tests green when boundaries are touched.
3. Run Ruff on changed Python surfaces per CI policy.
4. Document the test plan in the PR.
5. Not merge with failing CI without an explicit, documented exception.

Minimum commands for behavioural changes:

```bash
python -m pytest tests/ -v
ruff check app/ src/ tests/
```

When architecture or educational authorities change:

```bash
python -m pytest tests/architecture/ -v
```

When curriculum behaviour changes, include V1 and V2 related modules (engine, importer, section-aware traversal as applicable).

---

## Documentation-only changes

If the milestone forbids application changes:

- Do not modify tests to “prove” docs.
- Still run pytest when the brief requires validation that behaviour is unchanged.
- Record “None (documentation-only)” only when no test run was required **and** the application tree is untouched.

---

## Anti-patterns

- Weakening assertions to obtain a green build
- Testing implementation private details that churn without behavioural meaning
- Skipping architecture tests after moving imports across layers
- Using live external LLM/network calls in core educational tests
- Snapshot churn without human review of the educational meaning of the diff

---

## Definition of tested

A change is adequately tested when failures that would break student trust, educational authority, or architectural law are likely to be caught before merge.
