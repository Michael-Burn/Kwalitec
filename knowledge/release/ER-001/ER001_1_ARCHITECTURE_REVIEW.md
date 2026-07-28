# ER-001.1 — Architecture Review

**Programme:** ER-001 — Engineering Readiness  
**Work Package:** ER-001.1 — Version 1 Engineering Baseline Assessment  
**Date:** 2026-07-28  
**Nature:** Architecture assessment only — no structural changes  
**Companions:** `ER001_1_ENGINEERING_AUDIT.md`, `ER001_1_TECHNICAL_DEBT_REGISTER.md`  
**Canonical docs:** `ARCHITECTURE.md`, `knowledge/engineering/ARCHITECTURE_INVARIANTS.md`, `knowledge/engineering/ENGINEERING_STANDARD.md`

---

## 1. Review question

Is the as-built engineering architecture suitable to sustain Version 1 operation and eventual Version 1 production-ready declaration from an **engineering** standpoint?

**Answer:** **Conditionally suitable for invite-only Alpha; not cleared for Version 1 production-ready declaration** without dual-stack containment discipline and G7–G12 evidence.

Educational governance baselines (DG-001, RR-001, RP-002, RR-002) are **not reopened**.

---

## 2. Intended layering

```
Templates/JS → Blueprints → Services / Application → Domain + Curriculum Engine → Models / DB
```

Documented in `ARCHITECTURE.md` and Engineering Standard:

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Presentation | `app/presentation/`, feature blueprints, templates | HTTP, forms, templates |
| Application | `app/application/` | Use-case orchestration (incl. EIP) |
| Domain | `app/domain/` | Pure educational rules (no Flask) |
| Infrastructure | `app/infrastructure/` | Adapters, diagnostics, workers |
| Legacy services | `app/services/` | Operational business logic still live |
| Curriculum | `app/curriculum/` | Deterministic JSON → dataclasses |
| Quarantined EOS | `src/` | Parallel Education OS — bridged via `sys.path` |

---

## 3. Runtime ownership (engineering)

| Runtime | Entry | Production role |
|---------|-------|-----------------|
| **Authoritative student presentation** | `app` factory → `student` / `session` under `KWALITEC_V2_SOLE_RUNTIME` | Render start: `waitress-serve … wsgi:app` |
| Legacy Contained shells | `dashboard` / `mission` / `analytics` | Redirect soak (RR-002.3) |
| Standalone EOS factory | `src/web/app.py` | CI-verified; **not** Render entry |
| Educational Intelligence Pipeline | `app/application/educational_intelligence_pipeline/` | Orchestration + health probe |

**Invariant for operators:** Do not claim `src/web` as the Alpha sole student story. Authority is sole-runtime `app/` presentation (RR-002.3 / RR-001.3E residual F).

---

## 4. Blueprint map (engineering)

### Certified

- `student` (`/student`)
- `session` (`/session`)
- `assessment` / `adaptive_assessment`

### Contained / redirect

- `dashboard`, `mission`, `analytics` — READY FOR MIGRATION per RR-002.3

### Shared / ops

- `auth`, `study_plan`, `settings`, `research`, `calibration`, `alpha`
- Founder Console + diagnostics under `/console` and `/founder/*` (redirect)

**Finding:** Blueprint registration remains coherent; residual cost is dual-run soak until retirement WP (PC-001).

**Class:** Medium (intentional Contained) / Accepted Risk for Alpha.

---

## 5. Dependency direction

| Rule | Status | Notes |
|------|--------|-------|
| Models ↛ blueprints | Pass | Grep clean |
| Domain ↛ Flask | Pass | Grep clean |
| Services ↛ `flask.request` | Pass | Grep clean |
| Application ↛ `app.infrastructure` (direct) | Pass within `app/` | |
| **App ↛ `src/` via sys.path** | **Fail** | Bridge + cross-imports |
| Curriculum traversal via `CurriculumService` | Drift | ORM model methods duplicate helpers |

**Class of bridge:** High (ER-TD-H01).

---

## 6. Dual authority (engineering view)

Without reopening educational governance, architecture records:

| Concern | Legacy path | Certified / target path |
|---------|-------------|-------------------------|
| Planning | `app/services/planning_service.py` | Quality contracts + application adapters |
| Recommendation | `app/services/recommendation_service.py` | Decision / MES paths |
| Readiness | `app/services/readiness_service.py` | Readiness quality contracts |
| Mission | `mission_service` / optimizer quarantine | `mission_engine` / `mission_engine_v2` + adapter |
| Pipeline | N/A | EIP orchestrator stages |

**Class:** High technical debt (ER-TD-H02) — Accepted as Contained for Alpha only with consumer-chain discipline; blocks clean “one educational brain” architecture claim until consolidation.

Curriculum V1/V2 loadability remains an architecture invariant and must stay green in CI (G2.6 / G11.3) — no regression found in this audit’s document review.

---

## 7. Data architecture

Strengths:

- Alembic-managed schema; production Postgres required.
- Newer intelligence tables carry composite indexes.
- StartupService: production migrations + idempotent admin; curriculum import all envs; fail-open logging; no drops.

Risks:

- Lazy relationships → N+1 on new list UIs.
- Dual Mission type identities across domain/ORM.
- Topic traversal performance deferred (TD-007).

**Class:** Medium residuals; Accepted Risk on indexing of new tables.

---

## 8. Observability & ops architecture

| Capability | Assessment |
|------------|------------|
| Liveness / readiness / details / EI health | Present |
| Correlation IDs + slow requests | Present |
| Pipeline privacy-safe logging | Present |
| Query profiling opt-in | Present |
| Always-on background workers | Absent by design |
| Analytics outbox | CLI cron when enabled |

**Class:** Accepted Risk for Alpha with analytics OFF; Medium if analytics ON without cron (ER-TD-M15).

---

## 9. Security architecture

| Control | Assessment |
|---------|------------|
| Invite-only auth | Sound |
| CSRF + session cookies (prod) | Sound |
| Open redirect hardening | Sound |
| Ownership + founder RBAC | Sound |
| CSP unsafe-inline | Accepted Medium residual |
| Rate limiting | Missing — Medium before expansion |

No Critical security architecture defects found for invite-only Alpha.

---

## 10. Test & CI architecture

Strengths: architecture-first CI job; multi-Python unit matrix; EI certification job; production-gates; release-build validating both factories.

Weaknesses: stale `tests.yml`; unit subset exclusions; soft pip-audit; coverage unwired.

**Class:** Critical (tests.yml) + High (gate evidence).

---

## 11. Architecture compliance summary

| Invariant | Status |
|-----------|--------|
| Application factory sole construction path | Pass |
| Feature HTTP in blueprints | Pass (with large route modules) |
| Business rules primarily in services/application/domain | Pass with dual-authority debt |
| Curriculum V1/V2 loadable | Pass (must remain CI-green) |
| Sole-runtime student presentation documented | Pass (RR-002.3) |
| No second educational brain in **production defaults** | Contained — legacy services still present; redirects limit Contained shells |
| Dependency rules (ENG-004) | Mostly Pass; `src/` bridge Fail |
| Additive change preference | N/A (audit only) |

---

## 12. Architecture recommendations (no implementation in this WP)

1. Publish **Runtime Ownership** one-pager for operators (already substantially in RR-002.3; keep fingerprinted).  
2. Schedule **stack consolidation** epic for `src/` bridge retirement criteria.  
3. Publish **consumer-chain map** for readiness/recommendation/mission (legacy vs application).  
4. Retire or align **`tests.yml`** immediately.  
5. Do **not** delete Contained shells without parity proof (governance rule in technical debt register).

---

## 13. Architecture review outcome

| Field | Value |
|-------|-------|
| **Outcome** | **CONDITIONAL PASS for Alpha operation** |
| **Version 1 production-ready architecture clearance** | **NOT APPROVED** |
| **Blocking themes** | Dual stack/authority; G7–G12 engineering evidence; CI integrity |
| **Educational architectures** | Not reopened; Contained residuals preserved |

---

**End of ER-001.1 Architecture Review**
