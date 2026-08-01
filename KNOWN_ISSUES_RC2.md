# KNOWN_ISSUES_RC2.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Sources:** RR-001 reports, EV-001 / FV-002 artefacts, git/alembic/render evidence, Architecture Guardian  
**Rule:** Evidence-based only — no speculative product redesign items

---

## Critical

### KI-C1 — No clean intended release tip (dirty tree + uncommitted inventory) — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | ~~Working tree dirty; inventory uncommitted.~~ Resolved: keep-set committed; EV-001 dumps removed/ignored; working tree clean on tagged tip. |
| **Impact** | Cleared for local reproducibility. |
| **Evidence** | `REPOSITORY_HYGIENE_REPORT.md`; `RC2_POST_HYGIENE_REPORT.md`; tag `v2.0.0-beta.1-rc2` @ `75c29d2` |
| **Owner** | Release Engineering / Founder |
| **Required before GO?** | **Yes** — **CLOSED** (Sprint A) |

### KI-C2 — LIVE commit ≠ intended local release — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | Authoritative tip `0d3fc72137ba0ea51d1baa522c52aa526cf04438` / tag `v2.0.0-beta.1-rc2` is on `origin/main` and LIVE `/health.commit`. |
| **Impact** | Cleared for RC fingerprint GO. |
| **Evidence** | `VERSION1_RELEASE_MANIFEST.md`; `RC2_FINAL_RELEASE_REPORT.md`; deploy `dep-d9mr7o6417fc73c1o9h0` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** — **CLOSED** (Sprint C) |

### KI-C3 — EV-001 educational trust FAIL on current LIVE tip — **CLOSED** (consistency)

| Field | Value |
|-------|-------|
| **Description** | Sprint B consistency remediations deployed; Sprint C fresh-account LIVE re-check shows Progress/Coverage/EK agreement at honest 0%, no postal-address topic, no high-EK-without-practice theatre. Residual: Runtime C `/study-plan/` wizard redirect limits LO panel exercise; session chrome may show “Today's topic”. |
| **Impact** | Critical consistency blockers cleared for RC GO. |
| **Evidence** | `EV001_REMEDIATION_REPORT.md`; `RC2_FINAL_RELEASE_REPORT.md` Educational Trust |
| **Owner** | Educational Operations / Founder Gate Owner |
| **Required before GO?** | **Yes** — **CLOSED** for consistency (Sprint C) |

### KI-C4 — RR-001 smoke incomplete for GO criteria — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | Independent fresh-account smoke completed including session overview → start → answer → Continue → reflection → Finish Review → complete. Sprint C fixed answer→Continue persistence (`0d3fc72`). |
| **Impact** | Cleared for RC session GO. |
| **Evidence** | `RC2_FINAL_RELEASE_REPORT.md` Smoke; tip `0d3fc72` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** — **CLOSED** (Sprint C) |

---

## High

### KI-H1 — Volumes `publication_ready` but not `released` (DSH = 0)

| Field | Value |
|-------|-------|
| **Description** | CS1-001 / CS1-002 registered `publication_ready`; student-reachable released path still gated; DSH = 0. |
| **Impact** | Ordinary-student daily companion path unavailable; FV-002 companion FAIL. |
| **Evidence** | `PR001_VOLUME_REGISTER.md`; `CS1002_EDUCATIONAL_VOLUME.md`; `FV002_FINAL_RECOMMENDATION.md` |
| **Owner** | Publication Approver + Activation Engineering |
| **Required before GO?** | **Yes** if GO means PB-001 on released Pilot Arc. **No** only if GO is explicitly narrowed to a documented non-released Validation-mode scope (not recommended by RR-001). |

### KI-H2 — No Render deploy automation in operator environment

| Field | Value |
|-------|-------|
| **Description** | No `RENDER_API_KEY` / deploy hook in operator `.env`; deploys are manual dashboard. |
| **Impact** | Slows fingerprint-matched cutovers; RR-001 could not deploy. |
| **Evidence** | `RR001_DEPLOYMENT_VERIFICATION.md` §3 |
| **Owner** | Operations |
| **Required before GO?** | **No** (manual deploy acceptable if executed and verified) |

### KI-H3 — Unpushed EF-001 freeze commit — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | EF-001 freeze and subsequent RC tip are on `origin/main` / LIVE (`0d3fc72` lineage). |
| **Impact** | Cleared. |
| **Evidence** | `RC2_FINAL_RELEASE_REPORT.md`; LIVE `/health.commit` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** — **CLOSED** (Sprint C) |

### KI-H4 — Joint activation / multi-day `topic_code` loader limits

| Field | Value |
|-------|-------|
| **Description** | Ops registers record activation engineering blocker (multi-day same `topic_code` / day-key) preventing Volume `released`. |
| **Impact** | Even after Approver, pathway may not activate jointly. |
| **Evidence** | `PR001_PUBLICATION_BLOCKERS.md`; `PR001_VOLUME_REGISTER.md` DEP-ACT-01 / VD-02 |
| **Owner** | Engineering (activation successor) |
| **Required before GO?** | **Yes** for released-path PB-001; document explicitly if RC scopes Validation-mode only |

---

## Medium

### KI-M1 — LIVE `build_number` reports `local`

| Field | Value |
|-------|-------|
| **Description** | `/health` shows `build_number: local` while commit is present. |
| **Impact** | Weaker operator fingerprinting; commit remains usable. |
| **Evidence** | RR-001 `/health` JSON |
| **Owner** | Operations |
| **Required before GO?** | **No** (improve via `KWALITEC_BUILD_NUMBER`) |

### KI-M2 — Local SQLite Alembic behind head

| Field | Value |
|-------|-------|
| **Description** | Operator DB at `202607300004` while script head is `202607310002`. |
| **Impact** | Local verification can diverge from LIVE. |
| **Evidence** | `flask db heads` / startup warning |
| **Owner** | Release Engineering (workstation) |
| **Required before GO?** | **No** for LIVE GO; **Yes** before trusting local RC pytest against migrated schema |

### KI-M3 — Temporary EV-001 evidence dumps pollute tree — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | ~~Untracked dumps.~~ Deleted and gitignored (`.ev001_evidence*`). |
| **Impact** | Cleared. |
| **Evidence** | `REPOSITORY_HYGIENE_REPORT.md`; `.gitignore` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** — **CLOSED** |

### KI-M4 — Version / tag naming collision risk — **CLOSED**

| Field | Value |
|-------|-------|
| **Description** | Distinct tag `v2.0.0-beta.1-rc2` chosen; app version remains `2.0.0-beta.1`. Historical `v1.0.0-rc2` / `VERSION1-RC2` not reused. |
| **Impact** | Cleared for this tip. |
| **Evidence** | `git show-ref --tags`; `VERSION1_RELEASE_MANIFEST.md` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** — **CLOSED** |

### KI-M5 — Architecture Guardian score 40/100

| Field | Value |
|-------|-------|
| **Description** | Static guardian reports significant pre-existing layering/route-size debt. |
| **Impact** | Technical debt; not shown as new dirty-tree exclusive regression. |
| **Evidence** | `python tools/architecture_guardian.py` |
| **Owner** | Engineering |
| **Required before GO?** | **No** for RR-001 criteria; still run CI architecture tests per Release Protocol |

---

## Low

### KI-L1 — Confusing migration revision date prefixes

| Field | Value |
|-------|-------|
| **Description** | Some revisions use `202609*` / `202610*` / `202611*` IDs but sit as ancestors of head `202607310002`. |
| **Impact** | Operator confusion only; single head remains. |
| **Evidence** | `flask db history` |
| **Owner** | Engineering |
| **Required before GO?** | **No** |

### KI-L2 — Probe 404s on non-canonical paths

| Field | Value |
|-------|-------|
| **Description** | `/student/begin`, `/mission/`, `/admin/` 404 or unused; real CTAs differ. |
| **Impact** | None if smoke uses canonical links from Home. |
| **Evidence** | `RR001_LIVE_SMOKE_REPORT.md` |
| **Owner** | n/a |
| **Required before GO?** | **No** |

### KI-L3 — Public registration disabled

| Field | Value |
|-------|-------|
| **Description** | Product policy: no public registration; Private Beta is invite/admin path. |
| **Impact** | Student registration smoke N/A. |
| **Evidence** | Auth design; RR-001 smoke |
| **Owner** | Product |
| **Required before GO?** | **No** (document invite procedure instead) |

### KI-L4 — `gunicorn` pinned but Render starts waitress

| Field | Value |
|-------|-------|
| **Description** | Both servers in `requirements.txt`; startCommand uses waitress. |
| **Impact** | Slight image bloat only. |
| **Evidence** | `requirements.txt`; `render.yaml` |
| **Owner** | Engineering |
| **Required before GO?** | **No** |

---

## Summary counts

| Severity | Count | Required-before-GO (Yes) |
|----------|------:|--------------------------:|
| Critical | 4 | 4 |
| High | 4 | 3 (H2 No) |
| Medium | 5 | 2 (M3, M4) |
| Low | 4 | 0 |

**Bottom line (post Sprint B):** KI-C1 closed; local C2 fingerprint closed (`v2.0.0-beta.1-rc2`). KI-C3 **local consistency remediations landed** (coverage/EK/status/LOs/readiness explainability); LIVE EV re-check + deploy remain. GO still blocked by LIVE deploy match (KI-C2 remainder), KI-C3 LIVE re-validation, KI-C4 smoke, plus High release/activation items depending on PB-001 scope.
