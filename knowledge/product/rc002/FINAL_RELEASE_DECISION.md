# RC-002 — Final Release Decision

**Programme:** RC-002 — Final Release Failure Classification  
**Date:** 2026-07-27  
**Evidence suite:** `.venv/bin/pytest tests/ -q --tb=no` → **31 failed, 43325-class pass band** (this run: `43130` passed under slightly different collection noise; `--lf` reconfirm: **31 failed, 1 intermittent passed**). Stable failure set documented in `FAILURE_CLASSIFICATION_MATRIX.md`.  
**Alembic:** single head `202607260001` (MIG-002/003).

---

## Decision rule (programme charter)

| Condition | Decision |
|-----------|----------|
| Category A > 0 | **DO NOT DEPLOY** |
| Category A = 0 | **Render deployment approved**; list B–D as post-release work |

---

## Classification counts

| Category | Count |
|----------|------:|
| A — Critical Release Blocker | **0** |
| B — High Priority Quality Issue | **4** |
| C — Technical Debt | **8** |
| D — Outdated Test | **19** |
| **Total classified** | **31** |

---

## Decision

### **Render deployment approved**

No Category A failure remains among the residual suite failures.

This decision is scoped to **release-blocker classification of remaining pytest failures**. It does not replace:

- RC-001 Stage 1 checklist sign-off (B1–B10 already closed)
- Ops secrets / flag hygiene (`SECRET_KEY`, admin env, `render.yaml` flags)
- Founder judgment on whether Category B explainability vocabulary should be fixed *before* inviting external pilots

---

## Post-release work (ordered)

### Category B — preferably before or early in pilot

1. Align Runtime A mission narration (`/missions/` schema path) with EIP-003 / EIP-006 / IA-004 Learning Mode / Estimated Knowledge vocabulary **or** formally supersede those standards for the sole-runtime student shell and update the four failing tests.
2. Prefer validating explainability on `/student/*` under `SOLE_RUNTIME=1` (production posture), not only legacy `/missions/`.

Detail: `QUALITY_ISSUES.md`.

### Category C — safe after deploy

Architecture purity / line budgets / CSS soft budget (+362 B). Detail: `TECHNICAL_DEBT.md`.

### Category D — test maintenance only

Snapshots, CLI/startup log strings, 500 copy, login PTP constant, timestamp equality, PIL dependency, founder header strings, Jinja-comment scan. Detail: `OUTDATED_TESTS.md`.

---

## Explicit non-blockers confirmed

| Concern | Evidence |
|---------|----------|
| Migration dual-head | Resolved — head `202607260001` |
| Fresh DB / upgrade | MIG-002/003 PASS |
| Startup admin creation | Succeeds; log wording only differs |
| Production 500 page | Renders student-safe copy (`Something Went Wrong`) |
| Education OS `/eos/` snapshot drift | `/eos/` not mounted on production Flask Stage 1 path |
| Dual-run / simulation / recovery “mutating” recommendations | Diff is `generated_at` only |

---

## Sign-off statement

**On the criterion “any remaining failing test is a genuine release blocker?” — No.**

Kwalitec may proceed to Stage 1 Render deployment with Categories B–D tracked as follow-up.
