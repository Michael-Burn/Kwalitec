# Reviewer Framework

**Status:** Permanent research infrastructure  
**Programme origin:** EP-004 Private Beta Blind Review (SV-001–SV-020)  
**Operator entry point:** short instructions such as `Run reviewer SV-011`

This directory replaces one-off mega-prompts. Future blind review programmes should load these artefacts and execute — not recreate persona prompts manually.

---

## Contents

| File | Role |
|---|---|
| [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md) | Master table of all twenty reviewers |
| [`REVIEW_PROTOCOL.md`](REVIEW_PROTOCOL.md) | Permanent methodological rules |
| [`REVIEW_TEMPLATE.md`](REVIEW_TEMPLATE.md) | Canonical review output structure |
| [`REVIEW_EXECUTION_GUIDE.md`](REVIEW_EXECUTION_GUIDE.md) | How to run / repeat / filter reviewers |
| [`REVIEW_SCORING_GUIDE.md`](REVIEW_SCORING_GUIDE.md) | Definitions for every scoring dimension |
| [`personas/`](personas/) | Structured parameters for SV-001 … SV-020 |

Review outputs continue to live in [`../blind_reviews/`](../blind_reviews/).

---

## Minimum operator instructions

```
Run reviewer SV-014
Run only workflow reviewers
Repeat SV-007
Run all CM1 reviewers
Run all reviewers
```

Each of those is sufficient. The agent must load protocol → template → persona YAML and produce the review file automatically.

---

## Design rules

- Personas store **structured parameters only** (no embedded mega-prompt prose beyond background/task facts).
- One hypothesis per reviewer.
- Independence: no cross-reviewer comparison during a run.
- No interim synthesis inside persona reviews.
- Student-facing evaluation only.

---

## Extending the cohort

1. Add `personas/SV-0XX.yaml` using an existing file as schema reference.
2. Register the row in `REVIEWER_REGISTRY.md`.
3. Execute with `Run reviewer SV-0XX`.
