# RF-001A — Risk Register

**Programme:** Release Acceptance Programme RF-001A  
**Date:** 2026-07-31  
**Decision companion:** `RF001A_RELEASE_DECISION.md`

---

## Outstanding risks

| ID | Description | Severity | Category | Mitigation | Decision |
|----|-------------|----------|----------|------------|----------|
| R1 | **BF-001 not yet committed / not on live.** Production `curriculum_preview_tree.js` still initialises `var byId = Object`, so Expand/Collapse is broken on https://kwalitec.onrender.com until cutover. Candidate working tree is fixed. | High (Studio authoring on live) | Deployment / former A | Commit BF-001; Manual Deploy; confirm live JS contains `var byId = {}` and fingerprint refresh | **Fix before G1** *(for production Studio use)* — seal + deploy is operational, not a new engineering programme |
| R2 | Full-tree **159 unchanged** pytest failures (time-engine FK, twin/mission scaffolding, EOS snapshots, finish→summary assertion drift, CSS budget). Identical to RF-001. | Low–Medium | C / D (see classification) | Do not rewrite tests in RF-001A; accept as known debt | **Accept during G1** |
| R3 | Soft first-party CSS/JS budget exceeded (121284 > 70000). | Low | D | No performance incident on live login/assets | **Accept during G1** |
| R4 | `/health/details` remains public operator JSON. | Low | Accepted RF-001 limitation | Auth gate deferred | **Accept during G1** |
| R5 | Legacy Founder Bootstrap islands (Vision / Beta / Findings). | Low | PX-004 debt | Avoid those pages during G1; use Console/Studio | **Backlog after G1** |
| R6 | Settings still hosts advanced lifecycle shortcuts; Pause may appear twice; History generic “Session complete” labels. | Low | PX-003/004 debt | Known polish; does not block study | **Accept during G1** |
| R7 | Render **Manual Deploy** may be required (auto-deploy observed off historically). | Medium | Ops | Operator Manual Deploy after every seal push; verify `/health.commit` | **Fix before G1** *(process)* |
| R8 | Local dogfood SQLite Alembic stamp may lag head. | Low | Ops hygiene | Production already at `202607300005` | **Accept during G1** |
| R9 | PR-001B certification suite lag vs Runtime C. | Low | B | Student workflow/alpha smoke green | **Backlog after G1** |
| R10 | Branding asset path duplication; gunicorn unused in prod start. | Low | Infra debt | No student impact | **Backlog after G1** |
| R11 | Interactive Chromium console session not executed in RF-001A environment. | Low | Verification gap | HTTP asset + static JS + Flask ops gates; Founder can spot-check once after BF-001 deploy | **Accept during G1** |
| R12 | BF-001 Restart resets **stage** only (upload facts retained by design). | Low | Known limitation | Documented in BF-001; avoids duplicate workspaces | **Accept during G1** |

---

## Category A status

| Scope | Unresolved Category A? |
|-------|------------------------|
| RF-001A candidate (RF-001 + BF-001 tree) | **No** |
| Live host without BF-001 deploy | Studio Expand/Collapse still broken — treat as **R1 cutover**, not an open engineering defect in the accepted candidate |

---

## Decisions legend

- **Fix before G1** — must be resolved before productive Founder Validation on the affected surface.
- **Accept during G1** — known; does not prevent daily study.
- **Backlog after G1** — deferred; next programmes after RF-001A are **SB-001** then **RF-002** (no additional engineering programmes recommended here).
