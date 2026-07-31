# RF-001A — Test Classification

**Programme:** Release Acceptance Programme RF-001A  
**Date:** 2026-07-31  
**Authority:** RF-001 · BF-001 PASS · RC-002 · PX-004 PASS  
**Scope:** Remaining full-tree failures only (159). No test rewrites.

---

## Regression comparison (Phase 1)

| Metric | RF-001 baseline | RF-001A | Delta |
|--------|-----------------|---------|-------|
| Passed | 45616 | 45654 | **+38** |
| Failed | 159 | 159 | 0 |
| Skipped | 9 | 9 | 0 |
| Duration | 350.92 s | 321.67 s | −29 s |

| Failure set | Count |
|-------------|-------|
| New failures | **0** |
| Resolved failures | **0** |
| Unchanged failures | **159** (identical node ids) |

Evidence: `knowledge/evidence/releases/RF001A/`.

Passed increase is explained by newly collected BF-001 remediation and aligned Studio coverage; the residual failure set is unchanged from RF-001.

---

## Category summary

| Category | Meaning | Groups | Failures | Unresolved A? |
|----------|---------|--------|----------|---------------|
| **A** | Release blocker | 0 in candidate | 0 | **No** |
| **B** | Core regression | 1 | 8 | No — certification lag vs Runtime C |
| **C** | Legacy debt | 7 | ~95 | No |
| **D** | Test maintenance | 6 | ~56 | No |

BF-001 closed the six Founder Studio Category A defects that blocked RF verification. They do **not** appear in this residual set. Live host still serves pre-BF-001 Studio JS until BF-001 is committed and Manual Deployed — tracked in `RF001A_RISK_REGISTER.md` (deployment cutover), not as an open product defect in the candidate under review.

---

## Category A — Release blocker

**None remaining in the RF-001A candidate (RF-001 + BF-001 working tree).**

Operational gates covering Founder Studio remediation and Student primary path: **159/159 PASS** (`ops_gates.txt`).

---

## Category B — Core regression

### B1 — PR-001B student-pilot certification lag (8)

| Field | Detail |
|-------|--------|
| **Root cause** | Pilot certification suite expectations drift relative to Runtime C / commercial-loop student surfaces post V1S-008. |
| **Affected subsystem** | `tests/certification/test_pr001b_student_pilot.py` |
| **Founder impact** | None on daily study. Certification artefact only. |
| **Student impact** | None observed on workflow + alpha smoke (green). |
| **Recommendation** | **Accept during G1** — refresh certification after SB-001 baseline, not a study blocker. |

---

## Category C — Legacy debt

### C1 — Time-engine fixture FK / curriculum id (18)

| Field | Detail |
|-------|--------|
| **Root cause** | `FOREIGN KEY constraint failed` when fixtures omit current curriculum identity requirements. |
| **Affected subsystem** | `tests/test_time_engine.py` / planning time summary |
| **Founder / Student impact** | None on Runtime C primary study path used for G1. |
| **Recommendation** | **Backlog after G1** |

### C2 — Twin / reasoning / mission / assessment FK cascade (≈33)

| Field | Detail |
|-------|--------|
| **Root cause** | Shared SQLite FK integrity on `decision_records` / twin persistence when scaffolding Adaptive Mission, Assessment Pipeline, Digital Twin, Educational Reasoning, Learning Graph, and Intelligent Tutor suites. |
| **Affected subsystem** | Application intelligence scaffolding (non–Runtime C founder spine) |
| **Founder / Student impact** | Does not block Login → Mission → Session → Reflection → Complete. |
| **Recommendation** | **Backlog after G1** |

### C3 — Education OS HTML regression snapshots (13)

| Field | Detail |
|-------|--------|
| **Root cause** | Snapshot baselines stale after design-system / PX presentation changes. |
| **Affected subsystem** | `tests/education_os/adapters/flask/rendering/test_regression_snapshots.py` |
| **Impact** | Cosmetic assertion debt only. |
| **Recommendation** | **Backlog after G1** |

### C4 — Infrastructure session adapter / volume matrix engine (12)

| Field | Detail |
|-------|--------|
| **Root cause** | Legacy session adapter expectations vs current engine composition. |
| **Affected subsystem** | `tests/infrastructure/session/` |
| **Impact** | Presentation workflow Student happy path remains green. |
| **Recommendation** | **Backlog after G1** |

### C5 — Domain session-experience label / volume assertions (5)

| Field | Detail |
|-------|--------|
| **Root cause** | Label vocabulary drift (`dipped` / `improved` / readiness copy). |
| **Affected subsystem** | `tests/domain/session_experience/` |
| **Recommendation** | **Backlog after G1** |

### C6 — Independence / architecture import allowlists (≈5)

| Field | Detail |
|-------|--------|
| **Root cause** | Static import scanners vs evolved application modules (Studio, student experience, authority adapters). |
| **Recommendation** | **Backlog after G1** |

### C7 — Misc legacy surface contracts (≈9)

Includes EIP-006 state aliases, EV-001B gate flag off-path, unified journey outcome assembly, runtime integration probe, educational experience acceptance — all pre-existing RF-001 debt, unchanged.

| **Recommendation** | **Backlog after G1** |

---

## Category D — Test maintenance

### D1 — Session finish → Home vs commercial-loop Summary (12)

| Field | Detail |
|-------|--------|
| **Root cause** | Tests assert finish lands on `/student`; product redirects to `/session/.../summary` under commercial loop (intentional per RC-002). |
| **Evidence** | `assert '/student' in '/session/sess-1/summary'` |
| **Affected subsystem** | `tests/presentation/session/*`, workflow resume/volume meta |
| **Founder / Student impact** | Student completes via Summary — correct product behaviour. |
| **Recommendation** | **Accept during G1** — update assertions post-G1 if desired; do not change product for tests. |

### D2 — Soft CSS/JS budget (1)

| Field | Detail |
|-------|--------|
| **Root cause** | First-party CSS+JS **121284 > 70000** soft budget. |
| **Impact** | Performance hygiene only; pages load on live host. |
| **Recommendation** | **Accept during G1** |

### D3 — Nav / readiness / chrome copy assertions (≈15)

| Field | Detail |
|-------|--------|
| **Root cause** | Outdated expectations for operational health nav, help patterns, V1 readiness snapshot sections, RIP panels, brand tokens, DX-006B session chrome, product-language matrix CTA wording, alpha onboarding telemetry contract. |
| **Impact** | Presentation assertion drift; PX/RF paths remain operationally green. |
| **Recommendation** | **Accept during G1** / backlog |

### D4 — LXP substance / pause-finish review flags (4)

| Field | Detail |
|-------|--------|
| **Root cause** | Flag-gated LXP product tests vs current substance projection defaults. |
| **Recommendation** | **Accept during G1** |

### D5 — Studio publication matrix / snapshot mapping edge cases (4)

| Field | Detail |
|-------|--------|
| **Root cause** | Narrow checklist/matrix and snapshot mapping cases; BF-001 primary Studio path green. |
| **Recommendation** | **Accept during G1** |

### D6 — Student presentation chrome / responsive / trust schema (6)

| Field | Detail |
|-------|--------|
| **Root cause** | CQ/UX assertion wording and shell-class expectations after Home redesign. |
| **Student impact** | Workflow happy path + alpha smoke **PASS**. |
| **Recommendation** | **Accept during G1** |

---

## Release-gate subset (informational)

RF-001 recorded 12 failures inside a presentation/session gate slice. Those 12 remain and map to **D1** (finish→summary) plus related volume/accessibility assertion debt — **not Category A**.

---

## Verdict

Remaining failures are **unchanged RF-001 debt**, classified **B/C/D**. **No unresolved Category A defects** in the RF-001A candidate build.
