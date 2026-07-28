# ER-002 — Independent Engineering Audit

**Programme:** ER-002 — Engineering Recertification  
**Date:** 2026-07-28  
**Nature:** Independent audit only — no application code, schema, UI, tests, educational systems, or existing documentation modified by this programme  
**Audit SHA:** `11d8a224cb4f40de94d7e48e65d467e569408d1c` (`docs(ei-001.3): record completion report commit hash`)  
**Independence rule:** EI-001 documentation treated as historical evidence only; certification rests on live repository state verified in this audit  
**Educational governance:** Approved baseline (DG-001 · EGC-001 · RR-001 · RP-002 · RR-002) — **not reassessed**; no engineering evidence of educational regression discovered

---

## 1. Purpose

Determine whether engineering improvements since ER-001.1 sufficiently address prior engineering findings, and whether Engineering may issue a Version 1 engineering recommendation (GO / Conditional GO / HOLD / NO GO).

Educational usefulness (KSI / G1–G6), Mission Intelligence, recommendation algorithms, student experience, educational terminology, curriculum, and business logic are **out of scope** except where they create engineering defects.

---

## 2. Independence method

| Step | Action |
|------|--------|
| 1 | Re-read ER-001.1 findings as the prior baseline inventory (not as proof of current state) |
| 2 | Inspect live paths: `.github/workflows/`, `docs/production/`, `docs/security/`, `scripts/`, `render.yaml`, `requirements.txt`, `app/`, `src/`, architecture tests |
| 3 | Execute local hard gates used as engineering controls: `./scripts/dependency_audit.sh`; `pytest` on CI integrity / dependency assurance / release-operations suites |
| 4 | Score domains and gates from observed state; cite EI-001 only as historical provenance |
| 5 | Issue recommendation without assuming EI-001 success narratives |

**Local verification executed (2026-07-28):**

| Check | Result |
|-------|--------|
| `.github/workflows/` contains only `ci.yml` | Pass — `tests.yml` absent |
| `./scripts/dependency_audit.sh` | Exit 0 — 4 accepted ignores; no unaccepted advisories |
| `pytest tests/architecture/test_ci_integrity.py tests/architecture/test_dependency_assurance.py tests/architecture/test_release_operations.py` | **27 passed** |
| Flask pin | Still `Flask==3.1.0` (accepted Medium HOLD register current) |
| `_ensure_src_on_path()` in `app/__init__.py` | Still present — dual-stack residual live |
| Production entry | `wsgi:app` → `create_app()`; `render.yaml` Waitress startCommand |

Full remote GitHub Actions green on a Version 1 annotated RC tag was **not** re-proven in this audit (see G11).

---

## 3. Scope coverage matrix

| Domain | Reviewed | Primary live evidence | Verdict |
|--------|:--------:|-----------------------|---------|
| CI integrity | Yes | `.github/workflows/ci.yml`; `tests/architecture/test_ci_integrity.py` | **Pass** |
| Release evidence | Yes | `docs/production/G7_*`, `G8_*`, `G10_*`, `VERSION_1_FLAG_MATRIX.md`, `RELEASE_CANDIDATE_FINGERPRINT.md` | **Conditional** |
| Dependency assurance | Yes | Policy + script + accepted register + CI hard wiring | **Pass** (accepted Medium HOLDs) |
| Operational documentation | Yes | `docs/production/*`, runbooks, Release Protocol pointers | **Pass** |
| Deployment readiness | Yes | `render.yaml`, `wsgi.py`, StartupService path, DEPLOYMENT.md | **Pass** (invite-only) |
| Release gates G7–G12 | Yes | Artefacts + `Release_Gates.md` + live checks | **Mixed** — see §5 |
| Technical debt | Yes | ER-001 inventory vs live residuals | **Contained High** structural |
| Architecture integrity | Yes | Factory, blueprints, `src/` bridge, sole-runtime flags | **Conditional Pass** |
| Repository governance | Yes | Sole CI authority; fingerprint process; architecture gates | **Pass** |
| Engineering documentation | Yes | Production pack, CONTRIBUTING, readiness tracker | **Pass** with Low drift |
| Test infrastructure | Yes | Layered `tests/`, CI job scopes, architecture purity | **Pass** with Medium unit-scope residual |
| Security controls | Yes | Factory secrets, CSRF, headers, auth surface, G10 ops | **Conditional Pass** (Alpha) |
| Release reproducibility | Yes | Fingerprint process + dependency audit reproducibility | **Process Pass**; tagged RC execution pending |

---

## 4. Domain findings

### 4.1 CI integrity

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-CI-01 | Sole workflow `.github/workflows/ci.yml` present; no `tests.yml` | Accepted Risk → **Cleared residual** | **Closed** vs ER-001 Critical |
| ER2-CI-02 | Unit matrix Python 3.11–3.13 only; no 3.14 in `ci.yml` | Accepted Risk | Pass |
| ER2-CI-03 | Jobs: architecture → unit → integration → EI cert → lint → production-gates → release-build | Accepted Risk | Pass |
| ER2-CI-04 | Architecture suite asserts sole CI authority | Accepted Risk | Pass (9 CI integrity tests green locally) |
| ER2-CI-05 | Unit job still scopes to `tests/education_os/`, `tests/domain/`, `tests/architecture/` — broader suites deferred to integration | Medium | Open residual (ER-001 ER-TD-H10) |

### 4.2 Dependency assurance

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-DEP-01 | `scripts/dependency_audit.sh` hard-fails unaccepted advisories | Accepted Risk | **Closed** vs ER-001 soft-gate |
| ER2-DEP-02 | Policy + accepted findings + machine ID list present and architecture-tested | Accepted Risk | Pass |
| ER2-DEP-03 | CI `production-gates` / `release-build` invoke hard script (no `\|\| true`) | Accepted Risk | Pass |
| ER2-DEP-04 | Flask==3.1.0 retained under Security HOLD (PYSEC-2026-1377 / 2151) | Medium | Open residual (bump ≥3.1.3) |
| ER2-DEP-05 | pytest / python-dotenv Low advisories accepted | Low | Accepted for non-prod / mitigated paths |

### 4.3 Release evidence & gates G7–G12

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-G7-01 | `docs/production/G7_PERFORMANCE_HOLD.md` present; claim restriction explicit; architecture/GA tests guard artefact | High → HOLD | **Dispositioned HOLD** (not PASS) |
| ER2-G7-02 | No staging/production operator concurrency sample; load test not started | High | Residual under HOLD |
| ER2-G8-01 | `G8_RELIABILITY_EVIDENCE.md` — tabletop rollback + backup ack filed | Accepted Risk | Procedure pack **met** for invite-only |
| ER2-G8-02 | Tagged-deploy health/smoke fingerprint still required at Version 1 declaration | Medium | Open at declaration |
| ER2-G9-01 | Analytics / telemetry remain production-OFF; claim-safe if not overclaimed | Accepted Risk | Pass with honesty |
| ER2-G10-01 | Dependency critical policy (G10.5) enforced live | Accepted Risk | Pass |
| ER2-G10-02 | `G10_OPERATIONAL_EVIDENCE.md` documents SECRET_KEY / no-secrets / migration ack | Accepted Risk | Ops advanced |
| ER2-G10-03 | Stage 1 / expanded-cohort privacy claim class remains restricted (enrollment HOLD / board residual) | High | Open for Stage 1 / V1 expansion claims |
| ER2-G11-01 | RC fingerprint **process** published and architecture-linked | Accepted Risk | Process Pass |
| ER2-G11-02 | No Version 1 engineering RC fingerprint filed for current sole-CI post-EI tree | High | Open (Release operator) |
| ER2-G12-01 | `VERSION_1_FLAG_MATRIX.md` published; ON/OFF, owners, kill-switch; render / `.env.example` pointers | Accepted Risk | **Pass** (invite-only class) |
| ER2-G12-02 | Production-ON sole-runtime stack matches `render.yaml` values sampled in this audit | Accepted Risk | Pass |

### 4.4 Operational documentation & deployment

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-OPS-01 | Production pack present (DEPLOYMENT, ENVIRONMENT, RUNBOOK, BACKUP, INCIDENT, RELEASE_PROCESS, …) | Accepted Risk | Pass |
| ER2-OPS-02 | Render: Waitress `wsgi:app`, `flask db upgrade` releaseCommand, generated SECRET_KEY | Accepted Risk | Pass |
| ER2-OPS-03 | Dual migration path (releaseCommand + StartupService) remains | Medium | Accepted / hygiene residual |
| ER2-OPS-04 | Free-tier Render capacity limits under growth | Medium | Watch (not Alpha blocker) |

### 4.5 Architecture integrity & technical debt

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-A-01 | Single `create_app()` production path via `wsgi.py` | Accepted Risk | Pass |
| ER2-A-02 | Quarantined `src/` (~1,095 `.py`) still injected on `sys.path` | High | Contained residual |
| ER2-A-03 | CI still verifies Education OS `web.app` factory alongside legacy factory | High | Contained — do not overclaim one-stack |
| ER2-A-04 | Dual educational authorities (legacy services vs EIP/domain) unchanged | High | Contained (educational programmes not reopened) |
| ER2-A-05 | Legacy Contained presentation shells still registered under sole-runtime redirects | Medium | Contained soak |
| ER2-A-06 | Layering: services free of `flask.request` (spot-check consistent with ER-001) | Accepted Risk | Pass |
| ER2-A-07 | Curriculum V1/V2 loadability not retested end-to-end here; architecture suite remains CI-gated | Accepted Risk | No regression evidence |

### 4.6 Security controls

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-S-01 | Production rejects insecure/short SECRET_KEY; CSRF must stay on | Accepted Risk | Pass |
| ER2-S-02 | Invite-only posture; no public student registration surface found on auth routes | Accepted Risk | Pass |
| ER2-S-03 | CSP retains `'unsafe-inline'` + jsDelivr | Medium | Accepted for Alpha hardening residual |
| ER2-S-04 | No application login rate limiting / lockout | Medium | Open before cohort expansion |
| ER2-S-05 | Flask remember-me / backup restore Medium residuals from V1SP-004 remain in debt inventory | Medium | Open |
| ER2-S-06 | Security Critical dependency findings: none open (hard gate + HOLD register) | Accepted Risk | Pass |

### 4.7 Test infrastructure & repository governance

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-T-01 | Large layered suite + architecture purity + GA/ops gates | Accepted Risk | Pass |
| ER2-T-02 | Coverage package still unwired as CI artefact | Medium | Optional residual |
| ER2-T-03 | Release-operations + CI integrity + dependency assurance architecture tests present | Accepted Risk | Pass |
| ER2-GOV-01 | Sole CI authority documented and enforced by test | Accepted Risk | Pass |
| ER2-GOV-02 | `VERSION_1_READINESS.md` summary still mentions historical soft dependency gate wording in one Security row — tracker drift | Low | Doc drift (not remediated by this audit) |

### 4.8 Engineering documentation & release reproducibility

| ID | Finding | Class | Disposition |
|----|---------|-------|-------------|
| ER2-DOC-01 | Production + GA + release playbook surface is strong for invite-only ops | Accepted Risk | Pass |
| ER2-REP-01 | Dependency audit + RC fingerprint templates make tag-day evidence reproducible | Accepted Risk | Process Pass |
| ER2-REP-02 | Formal annotated Version 1 RC + Actions URL + deploy health match not filed for current tree | High | Blocks unqualified Engineering GO |

---

## 5. Engineering release gates G7–G12 (rescored)

| Gate | ER-001.1 baseline | Live ER-002 score | Notes |
|------|-------------------|-------------------|-------|
| **G7** Performance | Incomplete | **HOLD** | Formal HOLD artefact + G7.1 CI path; high-traffic claims forbidden |
| **G8** Reliability | Incomplete | **Partially met** | G8.4/G8.5 filed; G8.1 fingerprint at declaration still required |
| **G9** Telemetry | COMPLETE (flag OFF) | **Pass (claim-honest OFF)** | Do not claim live Journey KPIs |
| **G10** Security | Incomplete | **IN PROGRESS / Conditional** | G10.5 Pass; ops ack filed; Stage 1 expansion / privacy claim-class residual |
| **G11** Tests | Incomplete | **IN PROGRESS** | Process ready; tagged green RC fingerprint pending |
| **G12** Flags | Not scored | **PASS** (invite-only / engineering class) | Matrix live + render alignment verified |

Educational G1–G6 are **context only** (Product / Educational). Board still records G1 FAIL — outside ER-002 scoring.

---

## 6. ER-001 blocker recertification (independent)

| Prior ID | Topic | Live verification | ER-002 status |
|----------|-------|-------------------|---------------|
| ER-RB-01 | Stale `tests.yml` | Absent; sole `ci.yml`; architecture tests | **Cleared** |
| ER-RB-02 | G7 evidence | HOLD artefact present; sample/load open | **Cleared via HOLD** |
| ER-RB-03 | G8 evidence | Pack present | **Cleared** (declaration fingerprint residual) |
| ER-RB-04 | G10 claim-class | Dep policy Pass; ops ack; expansion privacy residual | **Partial — residual open** |
| ER-RB-05 | G11 fingerprinted RC | Process only | **Partial — process Cleared; tag Open** |
| ER-RB-06 | G12 matrix | Published + gated | **Cleared** |
| ER-RB-07 | Soft pip-audit | Hard script; exit 0 locally | **Cleared** |
| ER-RB-08…10 | Dual-stack / dual-authority / legacy shells | Still live | **Contained** (not Alpha stop; blocks converged-architecture claims) |

---

## 7. Educational governance boundary

No new educational regression evidence was discovered. Contained dual-authority / `src/` residuals remain **engineering sustainment** debt and do not reopen DG-001 / EGC-001 / RR-001 / RP-002 / RR-002.

---

## 8. Companions

| Deliverable | Path |
|-------------|------|
| Non-compliance register | `ER002_NON_COMPLIANCE_REGISTER.md` |
| Scorecard | `ER002_ENGINEERING_SCORECARD.md` |
| Traceability matrix | `ER002_TRACEABILITY_MATRIX.md` |
| Release recommendation | `ER002_RELEASE_RECOMMENDATION.md` |
| Certification report | `ER002_CERTIFICATION_REPORT.md` |

---

## 9. Classification legend

| Class | Meaning |
|-------|---------|
| **Critical** | Blocks any engineering clearance including invite-only integrity |
| **High** | Blocks unqualified Version 1 engineering GO or claim-class expansion |
| **Medium** | Material hardening / maintainability debt |
| **Low** | Hygiene / doc drift |
| **Accepted Risk** | Intentional / mitigated / fit for invite-only Alpha |
| **Contained** | Known residual with disclosure; not Alpha-stop |

---

## 10. Executive verdict (preview)

Kwalitec engineering controls have **materially improved** since ER-001.1. Critical CI integrity and dependency soft-gate failures are **cleared** on live evidence. G7–G12 evidence is largely filed, with **G7 HOLD**, **G11 tag pending**, and **G10 claim-class residual** preventing an unqualified Engineering GO.

**Engineering recommendation:** see `ER002_RELEASE_RECOMMENDATION.md` — **Engineering Conditional GO**.

---

**End of ER-002 Engineering Audit**
