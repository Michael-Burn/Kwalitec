# RF-001A — Release Acceptance Report

**Programme:** Release Acceptance Programme RF-001A  
**Phase:** Founder Validation Release Decision  
**Date:** 2026-07-31  
**Authority:** RF-001 · BF-001 PASS · RC-002 · PX-004 PASS  
**Verdict:** **PASS — GO WITH ACCEPTED DEBT**

---

## Summary

RF-001A re-executed full regression, classified every residual failure, verified Founder and Student operational paths, probed live deployment, and assessed release confidence. The question answered is whether the Founder can rely on this build as a primary daily study system — not whether Kwalitec is perfect.

**Answer:** Yes, with accepted debt. The candidate (RF-001 seal + BF-001 Studio remediation) has **no unresolved Category A defects**. The residual **159** full-tree failures are **identical** to the RF-001 baseline and are Category B/C/D only. Live production is healthy on RF-001 tip `e4d5a1b` but still serves pre-BF-001 Studio tree JS until BF-001 is committed and Manual Deployed.

---

## Deliverables

| Document | Purpose |
|----------|---------|
| `RF001A_RELEASE_ACCEPTANCE_REPORT.md` | This report |
| `RF001A_TEST_CLASSIFICATION.md` | Failure clusters A–D |
| `RF001A_RISK_REGISTER.md` | Outstanding risks + G1 decisions |
| `RF001A_RELEASE_DECISION.md` | Single recommendation |
| `RF001A_OPERATIONAL_VERIFICATION.md` | Founder / Student / browser evidence |
| `knowledge/evidence/releases/RF001A/` | Raw pytest + health artefacts |

---

## Phase 1 — Full regression suite

| Metric | Value |
|--------|-------|
| Command | `.venv/bin/python -m pytest tests/ -q --tb=no` |
| Total (passed+failed+skipped) | 45822 |
| Passed | **45654** |
| Failed | **159** |
| Skipped | **9** |
| Duration | **321.67 s (0:05:21)** |
| Warnings | ~67576 (SQLAlchemy LegacyAPI / `utcnow` — non-blocking) |

### Comparison to RF-001 baseline

| | RF-001 | RF-001A | Delta |
|--|--------|---------|-------|
| Passed | 45616 | 45654 | +38 |
| Failed | 159 | 159 | 0 |
| Skipped | 9 | 9 | 0 |
| Duration | 350.92 s | 321.67 s | −29 s |
| New failures | — | **0** | |
| Resolved failures | — | **0** | |
| Unchanged failures | — | **159** | |

---

## Phase 2 — Failure classification

See `RF001A_TEST_CLASSIFICATION.md`.

| Category | Status |
|----------|--------|
| A Release blocker | **0** in candidate |
| B Core regression | PR-001B certification lag (8) |
| C Legacy debt | Time-engine / twin-mission FK / EOS snapshots / infra session (~95) |
| D Test maintenance | Finish→summary redirect assertions, CSS budget, chrome copy (~56) |

---

## Phase 3–4 — Operational verification

See `RF001A_OPERATIONAL_VERIFICATION.md`.

| Path | Result |
|------|--------|
| Founder Studio full RF-001A path (incl. BF-001 controls) | **PASS** |
| Student Login→Mission→Session→Reflection→Complete→History→Revision→Logout | **PASS** |
| Ops gates (159 tests) | **159 passed** |

---

## Phase 5 — Deployment verification

| Field | Value |
|-------|--------|
| Live host | https://kwalitec.onrender.com |
| Commit hash (live) | `e4d5a1b6271630f5bcd6047239d087fa075176da` |
| Deployment identifier | Render service `kwalitec` / build_number `local` |
| Environment | `production` |
| Database | `connected` (latency ~21 ms at probe) |
| Migrations | `current=head=202607300005` |
| Application version | `2.0.0-beta.1` |
| Static fingerprint | `2.0.0-beta.1-rf001` |
| Health | `/health` `/health/live` `/health/ready` → **200** |
| Authentication surface | `/auth/login` → **200** |
| Static assets | CSS/JS first-party → **200** |
| Logging | Request observability present in app; production INFO posture unchanged |

| Check | Result |
|-------|--------|
| DB connectivity | **PASS** |
| Static assets | **PASS** |
| Auth entry | **PASS** |
| Health components (db, migrations, instance_storage, queue) | **PASS** |
| BF-001 on live | **FAIL / PENDING** — live tree JS still `var byId = Object` |

Repo HEAD at review: `e4d5a1b` (matches live). BF-001 changes present only as **dirty working tree** (+ BF-001 report files).

---

## Phase 6 — Manual browser verification

| Item | Result |
|------|--------|
| Platform | macOS 26.5.2 arm64 |
| Live login + assets | **PASS** |
| Candidate tree JS integrity | **PASS** (plain-object forest) |
| Live tree JS Expand/Collapse | **WARNING** until BF-001 deploy |
| Interactive Chromium console | Not available — HTTP/static/Flask evidence used |

---

## Phase 7 — Release confidence assessment

| Dimension | Confidence | Evidence |
|-----------|------------|----------|
| Architecture | **High** | V1S-008 integrity suite green; layering unchanged; no RF-001A product architecture edits |
| Founder workflows | **High** (candidate) / **Medium** (live until BF-001) | BF-001 + founder workflow PASS; live Studio JS lag = R1 |
| Student workflows | **High** | Workflow happy path, alpha smoke, DX home green |
| Deployment | **Medium** | Host healthy on RF-001 tip; Manual Deploy + BF-001 seal still required for Studio parity |
| Presentation | **High** | PX-004 PASS retained; polish debt accepted |
| Operational stability | **High** | Health/ready/live 200; DB+migrations ok; no new regressions vs RF-001 |

---

## Phase 8 — Outstanding risk register

See `RF001A_RISK_REGISTER.md`. Highest priority: **R1 BF-001 cutover** before production Studio authoring.

---

## Phase 9 — Release decision

See `RF001A_RELEASE_DECISION.md`.

### **GO WITH ACCEPTED DEBT**

The Founder can rely on this build for daily study. Residual full-tree debt and presentation limitations do not prevent effective learning. Seal and deploy BF-001 before depending on production Curriculum Studio Expand/Collapse and related remediated controls.

---

## Success criteria

| Criterion | Met |
|-----------|-----|
| Complete regression executed | Yes |
| Remaining failures classified | Yes |
| Founder walkthrough succeeds (candidate) | Yes |
| Student walkthrough succeeds | Yes |
| Deployment verified | Yes (with R1 Studio cutover note) |
| No unresolved Category A in candidate | Yes |
| Recommendation supported by evidence | Yes |

**RF-001A programme result: PASS**

---

## Files created

- `RF001A_RELEASE_ACCEPTANCE_REPORT.md`
- `RF001A_TEST_CLASSIFICATION.md`
- `RF001A_RISK_REGISTER.md`
- `RF001A_RELEASE_DECISION.md`
- `RF001A_OPERATIONAL_VERIFICATION.md`
- `knowledge/evidence/releases/RF001A/*`

## Files modified

None (verification only). Application changes in the working tree belong to **BF-001**, not RF-001A.

## Tests executed

```text
.venv/bin/python -m pytest tests/ -q --tb=no
→ 45654 passed, 159 failed, 9 skipped in 321.67s

.venv/bin/python -m pytest [ops gates listed in operational verification]
→ 159 passed in 13.49s

Path evidence subset → 22 passed
```

## Migration impact

None.

## Architecture compliance

No architecture changes in RF-001A. Curriculum V1/V2 loadability and Runtime C integrity gates remain green. Traversal/import compatibility: preserved / N/A for verification-only work.

## Technical debt

Unchanged 159 full-tree failures; soft CSS budget; PX polish debt; BF-001 awaiting commit/deploy.

## Known limitations

Interactive browser console not captured; live Studio JS lag until BF-001 Manual Deploy; full-tree zero not claimed.

## Next programme

**SB-001 — Student Baseline & Continuity**, then **RF-002**, before G1 evidence. No further engineering programmes recommended by RF-001A.
