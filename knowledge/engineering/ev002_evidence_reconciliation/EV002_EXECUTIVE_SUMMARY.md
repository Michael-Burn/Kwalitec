# EV-002 — Executive Summary

**Programme:** EV-002 — Engineering Evidence Reconciliation  
**Status:** Complete  
**Date:** 2026-07-29  
**Method:** Read-only comparison of EV-001 and FV-001B (Final) artefacts, process/DB evidence, and captured UI records. No application code modified.

---

## Verdict

# Case D — Environment mismatch

EV-001 and FV-001B (Final) did **not** exercise the same system state. Both programmes’ observations are consistent with the environments they actually hit.

| | EV-001 | FV-001B (Final) |
|---|---|---|
| Outcome | Studio lifecycle through Ready | Validate / Preview / Approve / Publish / Ready failed |
| Subject | CS1V / `ws-cs1v` | CS1F / `ws-cs1f` |
| Base URL | `http://127.0.0.1:5141` | `http://127.0.0.1:5130` |
| Database | Fresh `/tmp/ev001_verify.sqlite3` | Long-lived `instance/kwalitec.sqlite3` |
| Process | New Flask process started for EV-001 | Surviving Flask process started ~43 minutes earlier |
| Code image | Loaded **after** PI-002R validation/preview/route edits | Loaded **before** those edits (no reload) |

---

## First point of divergence

**Validate Curriculum.**

- EV-001: `Validation completed successfully · passed` (blocking = 0)
- FV-001B: `We couldn't complete validation because blocking findings remain` (`in_progress`)

All later FV failures (preview contradiction, approve→publish refusal, publish refusal, no Ready) are consequent: approval and publish require `validation_passed`.

---

## Differing assumption (the one that matters)

Both programmes were treated as describing **the same post–PI-002R Studio**.

They did not:

1. **Different runtime process / loaded code** — FV-001B Final used port 5130 process started `2026-07-28T22:04:44Z` (debug off, no reload). PI-002R-related edits to `validation_service.py`, `preview_service.py`, and `routes.py` landed ~`22:27Z`. EV-001’s port 5141 process started after those edits.
2. **Different database** — EV-001 dedicated empty SQLite; FV-001B default instance DB already containing CS1R/CS1S/CS1U workspaces.
3. **Different curriculum inputs** — CS1V vs CS1F PDFs (different chapter/LO density; different SHA-256).

---

## What this does *not* mean

- **Not Case A:** EV-001 still used the visible Studio UI path (no gate bypass, no seeded publication). Ready package for CS1V is in `/tmp/ev001_verify.sqlite3`.
- **Not Case B:** FV-001B’s failures match durable DB state for CS1F (`publication_state=draft`, no package). Workflow genuinely did not reach Ready.
- **Not Case C alone:** Behaviour differs because the *execution environments* differed, not because a single shared process regressed between identical runs.
- **Not Case E as primary:** Pre-existing PI-002-class defects and UI contradictions exist, but they do not reconcile the mutual exclusivity once environment mismatch is accounted for.

---

## Recommendation

Re-run Founder Studio blind validation on a **fresh process** started from the same post–PI-002R/EV-001 tree, against a **dedicated empty DB**, with documented PDF fixtures — then judge GO/NO-GO. See [`RECOMMENDED_ACTION.md`](RECOMMENDED_ACTION.md).

---

## Artefacts

| File | Purpose |
|---|---|
| [`SUBJECT_COMPARISON.md`](SUBJECT_COMPARISON.md) | CS1V vs CS1F identity |
| [`ENVIRONMENT_COMPARISON.md`](ENVIRONMENT_COMPARISON.md) | Process, DB, build, flags |
| [`WORKFLOW_COMPARISON.md`](WORKFLOW_COMPARISON.md) | Stage table + first divergence |
| [`VALIDATION_INPUT_COMPARISON.md`](VALIDATION_INPUT_COMPARISON.md) | Curriculum entering validation |
| [`STATE_TRANSITION_TRACE.md`](STATE_TRANSITION_TRACE.md) | Flag / lifecycle transitions |
| [`UI_STATE_COMPARISON.md`](UI_STATE_COMPARISON.md) | Flash vs DB honesty |
| [`ROOT_CAUSE_RECONCILIATION.md`](ROOT_CAUSE_RECONCILIATION.md) | Case D justification |
| [`RECOMMENDED_ACTION.md`](RECOMMENDED_ACTION.md) | Next steps (no code in EV-002) |
