# KNOWN_ISSUES_RC2.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Sources:** RR-001 reports, EV-001 / FV-002 artefacts, git/alembic/render evidence, Architecture Guardian  
**Rule:** Evidence-based only — no speculative product redesign items

---

## Critical

### KI-C1 — No clean intended release tip (dirty tree + uncommitted inventory)

| Field | Value |
|-------|-------|
| **Description** | Working tree has 10 modified + 117 untracked entries; Campaign Alpha/Beta JSON and `educational_packages` module are not in Git. |
| **Impact** | Cannot reproduce educational inventory on Render from a commit; RR-001 FAIL; PB-001 blocked. |
| **Evidence** | `RR001_RELEASE_READINESS_REPORT.md`; `git status`; `REPOSITORY_AUDIT.md` |
| **Owner** | Release Engineering / Founder |
| **Required before GO?** | **Yes** |

### KI-C2 — LIVE commit ≠ intended local release

| Field | Value |
|-------|-------|
| **Description** | LIVE and `origin/main` are `613722c`; local HEAD is unpushed `f066bcf`; inventory not deployed. |
| **Impact** | PB-001 would study a non-canonical / outdated educational system relative to local intended corpus. |
| **Evidence** | `RR001_DEPLOYMENT_VERIFICATION.md`; `/health.commit` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** |

### KI-C3 — EV-001 educational trust FAIL on current LIVE tip

| Field | Value |
|-------|-------|
| **Description** | Live student audit on `613722c` found placeholder pedagogy (“Today’s topic”), empty reading stages, curriculum address artefact, continuity/progress mismatches, boilerplate explainability. |
| **Impact** | Educational quality insufficient for primary-study trust; RR-001 S1-EDU remains. |
| **Evidence** | `EV001_FINAL_RECOMMENDATION.md`; `EV001_TRUST_BREAK_REGISTER.md` (TB-001+) |
| **Owner** | Educational Operations / Founder Gate Owner |
| **Required before GO?** | **Yes** (for PB-001 as authoritative educational system). Mitigation path: ship certified inventory + overlays that address placeholder substance — then re-validate. |

### KI-C4 — RR-001 smoke incomplete for GO criteria

| Field | Value |
|-------|-------|
| **Description** | Founder/student nav smoke partial PASS; cold session start partial; session completion not executed on LIVE. |
| **Impact** | Cannot claim end-to-end study readiness. |
| **Evidence** | `RR001_LIVE_SMOKE_REPORT.md` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** |

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

### KI-H3 — Unpushed EF-001 freeze commit

| Field | Value |
|-------|-------|
| **Description** | `f066bcf` freezes Educational Framework locally but is not on `origin/main` / LIVE. |
| **Impact** | LIVE EF fingerprint diverges from declared Version 1 Educational Law. |
| **Evidence** | `git log origin/main..HEAD`; `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** |

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

### KI-M3 — Temporary EV-001 evidence dumps pollute tree

| Field | Value |
|-------|-------|
| **Description** | `.ev001_evidence/` (~128 files) + `.ev001_evidence.html` untracked. |
| **Impact** | Blocks clean tree; risk of accidental commit of bulky dumps. |
| **Evidence** | `REPOSITORY_AUDIT.md` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** (exclude/clean from release set; deletion optional after archive) |

### KI-M4 — Version / tag naming collision risk

| Field | Value |
|-------|-------|
| **Description** | Sprint branded VERSION1-RC2 while app version is `2.0.0-beta.1` and tag `v1.0.0-rc2` already exists historically (`f2cbdc5`). |
| **Impact** | Operator confusion; wrong tag deploy risk. |
| **Evidence** | `git tag -l`; `VERSION`; `docs/release/RELEASE_NOTES_v1.0.0-RC2.md` |
| **Owner** | Release Engineering |
| **Required before GO?** | **Yes** to choose a **distinct** new tag name before cut |

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

**Bottom line:** GO remains blocked primarily by Critical hygiene/fingerprint/educational-trust items (KI-C1…C4) plus High release/activation items depending on PB-001 scope.
