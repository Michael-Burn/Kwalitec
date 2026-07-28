# ER-001.1 — Version 1 Engineering Baseline Audit

**Programme:** ER-001 — Engineering Readiness  
**Work Package:** ER-001.1 — Version 1 Engineering Baseline Assessment  
**Date:** 2026-07-28  
**Nature:** Audit only — no application code, schema, UI, tests, or educational copy modified  
**Authority:** Engineering assessment independent of educational governance  
**Baseline posture:** DG-001 · EGC-001 · RR-001 · RP-002 · RR-002 treated as approved educational/governance baselines — not reopened (no new regression evidence discovered)

---

## 1. Purpose

Comprehensive engineering assessment of Kwalitec against Version 1 operational and release-engineering expectations. Educational usefulness (KSI / G1), educational terminology, Mission model semantics, Reflection Architecture, and Study Sensei identity are **out of scope** except where they create engineering defects.

---

## 2. Scope coverage matrix

| Domain | Reviewed | Primary evidence | Verdict |
|--------|:--------:|------------------|---------|
| Application architecture | Yes | `app/__init__.py`, `ARCHITECTURE.md` | Mature factory; dual-stack residual |
| Flask blueprint organisation | Yes | `_register_blueprints()`, RR-002.3 inventory | Certified + Contained shells |
| Domain boundaries | Yes | `app/domain/`, `app/application/`, `app/services/` | Dual authority debt |
| Service layer | Yes | 54 modules under `app/services/` | No `flask.request` leakage |
| Dependency direction | Yes | Grep + ENG-004 rules | `src/` bridge is main breach |
| Data model quality | Yes | `app/models/` (29 modules) | Good indexes on new tables; lazy N+1 residual |
| Configuration management | Yes | `app/config.py`, factory validation | Strong production gates |
| Error handling | Yes | 403/404/500 handlers + rollback | Adequate |
| Logging | Yes | `_configure_logging`, HTTP observability | Adequate |
| Observability | Yes | Health probes, EIP observability, guides | PR-001 complete for ops |
| Security | Yes | Headers, CSRF, V1SP-004, GA review | Invite-only Alpha fit |
| Authentication | Yes | `app/auth/`, invite-only | Pass |
| Authorisation | Yes | Ownership + founder guards | Pass with Low residuals |
| Session management | Yes | Cookie flags ProductionConfig | Pass with Medium remember-me residual |
| Performance | Yes | GA budgets, query profiling, PERFORMANCE_GUIDE | Soft budgets only |
| Database access | Yes | SQLite/Postgres, bound SQL only | Pass |
| Query efficiency | Yes | Eager-load hot paths + residual lazy | Medium residual |
| Caching opportunities | Yes | No Redis/flask-caching (intentional) | Accepted Risk |
| Background processing | Yes | Sync + CLI workers only | By design |
| Test architecture | Yes | `tests/`, `pyproject.toml`, ~1k modules | Strong breadth; coverage unwired |
| CI/CD readiness | Yes | `ci.yml`, `tests.yml` | Dual-workflow risk |
| Deployment | Yes | `render.yaml`, Waitress, StartupService | Operational |
| Environment configuration | Yes | Config classes + `.env.example` | Pass; dual EOS config residual |
| Secrets management | Yes | gitignore, Render generateValue, deny-list | Pass |
| Package dependencies | Yes | `requirements.txt`, DEPENDENCY_AUDIT_V2 | Flask pin Medium |
| Technical debt | Yes | `docs/TECHNICAL_DEBT_REGISTER.md` | Active; prioritised in companion |
| Documentation completeness | Yes | CONTRIBUTING, runbooks, production pack | Strong; G12 matrix gap |
| Version 1 release gates (eng) | Yes | P-002.1 G7–G12, Release_Gates.md | Not cleared |

---

## 3. Executive verdict

| Question | Answer |
|----------|--------|
| Fit for invite-only Internal Alpha operation? | **Yes** — authn/authz, CSRF, secrets, health, sole-runtime defaults |
| Engineering cleared for **Version 1 production-ready** declaration? | **No** |
| Engineering readiness status | **NOT CLEARED** — see §10 |
| Product behaviour changed by this WP? | **No** |

Dominant engineering themes:

1. **Parallel stacks** — Flask `app/` + clean-architecture packages + quarantined `src/` (~1,100 files) still on `sys.path`.
2. **Dual educational authorities** — legacy `app/services/` live paths vs certified Educational Intelligence pipeline (`app/application/` / `app/domain/`) — documented debt, not reopened as educational governance.
3. **Engineering release gates G7–G12 incomplete** — board statuses IN PROGRESS / Not scored.
4. **CI integrity gap** — stale `.github/workflows/tests.yml` (Python 3.14, unscoped pytest) conflicts with canonical `ci.yml`.

---

## 4. Domain findings

### 4.1 Application architecture

| ID | Finding | Class |
|----|---------|-------|
| ER-A-01 | Single `create_app()` factory with documented layering | Accepted Risk |
| ER-A-02 | Three coexisting stacks: `app/` monolith, `app/{application,domain,infrastructure}/`, quarantined `src/` | High |
| ER-A-03 | `_ensure_src_on_path()` injects `src/` at runtime (`app/__init__.py`) | High |
| ER-A-04 | Production entry `wsgi:app` → legacy factory; `src/web/app.py` verified in CI but not Render start | High |
| ER-A-05 | Sole-runtime Education OS (`/student`, `/session`) documented and flag-gated | Accepted Risk |

### 4.2 Blueprint organisation

| ID | Finding | Class |
|----|---------|-------|
| ER-BP-01 | Canonical student/session (+ assessment) blueprints registered | Accepted Risk |
| ER-BP-02 | Legacy dashboard/mission/analytics still registered; redirect under sole runtime (PC-001 / RR-002.3) | Medium |
| ER-BP-03 | `app/study_plan/routes.py` ~1,372 lines (TD-002) | Medium |
| ER-BP-04 | Founder/console + diagnostics blueprints founder-gated | Accepted Risk |

### 4.3 Domain boundaries & service layer

| ID | Finding | Class |
|----|---------|-------|
| ER-D-01 | `app/services/` free of `flask.request` | Accepted Risk |
| ER-D-02 | Dual readiness/recommendation/mission/planning authorities (E2-PI / PC-003 / PC-004) | High |
| ER-D-03 | Oversized services (`planning_service` ~1.6k, `recommendation_service` ~1.5k lines) | Medium |
| ER-D-04 | EIP orchestrator + health endpoint present (PR-001) | Accepted Risk |
| ER-D-05 | Models do not import blueprints | Accepted Risk |
| ER-D-06 | `Curriculum` ORM traversal methods drift from `CurriculumService` canonical helpers | Medium |

### 4.4 Data model

| ID | Finding | Class |
|----|---------|-------|
| ER-M-01 | Intelligence tables (Twin, assessment, tutor, etc.) well indexed | Accepted Risk |
| ER-M-02 | Mission / StudyPlan / TopicProgress indexes present | Accepted Risk |
| ER-M-03 | Topic/Curriculum traversal filters lack composite indexes (TD-007 territory) | Medium |
| ER-M-04 | Default `lazy=True` on many relationships — residual N+1 risk | Medium |
| ER-M-05 | Dual type identity `domain.Mission` vs `models.Mission` (E2-PE-03) | High |

### 4.5 Configuration, errors, logging, observability

| ID | Finding | Class |
|----|---------|-------|
| ER-C-01 | Production rejects insecure/short `SECRET_KEY`; requires `DATABASE_URL`; CSRF must stay on | Accepted Risk |
| ER-C-02 | Insecure deny-list includes `.env.example` placeholder `change-this-secret-key` | Accepted Risk |
| ER-C-03 | 403/404/500 handlers allocate error reference IDs; 500 rolls back session | Accepted Risk |
| ER-C-04 | Health: `/health`, `/live`, `/ready`, `/details`, `/health/educational-intelligence` | Accepted Risk |
| ER-C-05 | HTTP correlation IDs + slow-request warnings + optional `PROFILE_SQL` | Accepted Risk |
| ER-C-06 | Parallel EOS settings module under `src/infrastructure/config/` | Medium |

### 4.6 Security, authentication, authorisation, sessions

| ID | Finding | Class |
|----|---------|-------|
| ER-S-01 | Invite-only login; no public registration on main app | Accepted Risk |
| ER-S-02 | Open-redirect hardening on `next` (`_safe_next_url`) with tests | Accepted Risk |
| ER-S-03 | CSRF enabled outside tests; production startup fails if disabled | Accepted Risk |
| ER-S-04 | Security headers + HSTS in production; CSP allows `'unsafe-inline'` + jsDelivr | Medium |
| ER-S-05 | Ownership checks on plans/missions/sessions; founder Console gated | Accepted Risk |
| ER-S-06 | Study-plan cross-user often flash+redirect (not 403/404) | Low |
| ER-S-07 | No login rate limiting / lockout | Medium |
| ER-S-08 | Remember-me cookie clear may omit Secure flags (Flask-Login 0.6.3) | Medium |
| ER-S-09 | Backup restore size/allowlist residuals (V1SP-004 M-3) | Medium |
| ER-S-10 | Production session cookies HttpOnly + Secure + SameSite=Lax | Accepted Risk |

### 4.7 Performance, DB, caching, background work

| ID | Finding | Class |
|----|---------|-------|
| ER-P-01 | GA soft performance budgets present; staging/production load sample missing (G7) | High |
| ER-P-02 | Hot-path eager loads exist (missions, readiness); residual lazy N+1 | Medium |
| ER-P-03 | No Redis / Celery / APScheduler — intentional sync architecture | Accepted Risk |
| ER-P-04 | Analytics outbox drained via CLI cron when flag ON — no Render worker | Medium |
| ER-P-05 | Raw SQL reviewed paths use bound/`db.text` static statements | Accepted Risk |
| ER-P-06 | Educational-output caching forbidden by PERFORMANCE_GUIDE policy | Accepted Risk |

### 4.8 Tests, CI/CD, deployment, dependencies, docs

| ID | Finding | Class |
|----|---------|-------|
| ER-T-01 | Large layered suite (`tests/` + founder packages); architecture purity gates | Accepted Risk |
| ER-T-02 | `coverage` pinned but not wired into pytest/CI | Medium |
| ER-T-03 | Canonical `ci.yml`: architecture → unit matrix → integration → EI cert → lint → production-gates → release-build | Accepted Risk |
| ER-T-04 | Stale `tests.yml` uses Python **3.14**, unscoped pytest, no ruff/cert gates | Critical |
| ER-T-05 | CI unit job excludes `tests/application/`, `tests/infrastructure/`, many root `tests/test_*.py` | High |
| ER-T-06 | `pip-audit` soft-fails (warnings only) | High |
| ER-T-07 | Flask==3.1.0 below patched ≥3.1.3 (DEPENDENCY_AUDIT_V2) | Medium |
| ER-T-08 | Render: Waitress + `flask db upgrade` + StartupService dual migration path | Medium |
| ER-T-09 | Production pack + EI runbooks present and CI-gated | Accepted Risk |
| ER-T-10 | G12 Version 1 flag matrix not published as declaration artefact | High |
| ER-T-11 | CONTRIBUTING ruff scope omits `src/` vs CI | Low |

---

## 5. Educational governance boundary

| Programme | Treatment in ER-001.1 |
|-----------|------------------------|
| DG-001 / EGC-001 / RR-001 / RP-002 / RR-002 | **Approved baselines** — not reopened |
| Curriculum / Mission model / Reflection / Sensei copy | **Frozen** — no findings that require change |
| Parallel `src/` / legacy shells | Documented as **engineering** debt / Contained residual (RR-002.3 / RR-001.3E) |
| G1 Validated KSI | **Out of engineering scope** — Product gate; recorded as context only |

No new educational regression evidence was discovered during this audit.

---

## 6. Prior certification context

| Artefact | Snapshot | Use in ER-001.1 |
|----------|----------|-----------------|
| `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Engineering Readiness **58/100** (2026-07-15) | Directional; supersede with this baseline |
| `docs/TECHNICAL_DEBT_REGISTER.md` v0.6.0 | TD + E2 + PC items | Sourced into debt companion |
| `Release_Gates.md` (P-003.1) | G7–G12 IN PROGRESS / Not scored | Engineering gate baseline |
| V1SP-004 Security Verification | Medium residuals M-1…M-6 | Security section |

---

## 7. Companions

| Deliverable | Path |
|-------------|------|
| Architecture review | `ER001_1_ARCHITECTURE_REVIEW.md` |
| Technical debt register | `ER001_1_TECHNICAL_DEBT_REGISTER.md` |
| Release blockers | `ER001_1_RELEASE_BLOCKERS.md` |
| Risk register | `ER001_1_RISK_REGISTER.md` |
| Completion report | `ER001_1_COMPLETION_REPORT.md` |

---

## 8. Classification legend

| Class | Meaning |
|-------|---------|
| **Critical** | Blocks Version 1 engineering clearance or CI integrity |
| **High** | Resolve within next 1–2 engineering epics / before V1 declaration |
| **Medium** | Material maintainability or hardening debt |
| **Low** | Minor hygiene |
| **Accepted Risk** | Intentional / mitigated / fit for invite-only Alpha |
| **Enhancement** | Optional improvement after V1 engineering clearance |

---

## 9. Counts (this audit)

| Class | Count (approx.) |
|-------|----------------:|
| Critical | 1 |
| High | 12 |
| Medium | 18 |
| Low | 3 |
| Accepted Risk | 22 |
| Enhancement | See debt register |

Exact prioritised IDs live in `ER001_1_TECHNICAL_DEBT_REGISTER.md`.

---

## 10. Version 1 engineering readiness status

**Status: NOT CLEARED**

Kwalitec is **operationally suitable for invite-only Alpha** from an engineering controls perspective (authn/authz, CSRF, secrets, health, sole-runtime production defaults, observability stack).

Kwalitec is **not** engineering-cleared for an unqualified **Version 1 production-ready** declaration because:

1. Engineering hard gates **G7, G8, G10, G11** remain **IN PROGRESS** (board).
2. **G12** is **Not scored** (flag matrix evidence unavailable).
3. **CI integrity** is compromised by a stale secondary workflow (`tests.yml`).
4. **Structural dual-stack / dual-authority** debt remains High priority for sustainment velocity.

Educational gates (G1–G6) are acknowledged as Product/Educational authorities and are **not scored by this programme**.

---

**End of ER-001.1 Engineering Audit**
