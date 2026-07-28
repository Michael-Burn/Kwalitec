# G10 — Operational Security Evidence (EI-001.3)

**Programme:** EI-001.3 — Release Operations & Deployment Evidence  
**Authority:** P-002.1 Gate G10 · ER-RB-04 (operational portion) · EI-001.2 (G10.5)  
**Date:** 2026-07-28  
**Scope:** Operational / engineering release evidence only — **does not** implement security features or close the privacy signature pack

---

## 1. What this artefact covers

ER-RB-04 residual after EI-001.2:

| Portion | Status |
|---------|--------|
| G10.5 Dependency critical policy | **Closed** (EI-001.2) — cite `docs/security/DEPENDENCY_ASSURANCE_POLICY.md` |
| Privacy Review signatures (Stage 1 / expanded cohort) | **Open** — Product / Privacy; **out of EI-001.3 implementation scope** |
| Operational G10.2 / G10.6 / G10.7 evidence | **Advanced** below |

---

## 2. Operational evidence catalogue

| Criterion | Evidence |
|-----------|----------|
| G10.1 Security review current | `docs/ga/SECURITY_REVIEW.md` — residuals acknowledged (CSP); no new Criticals introduced by EI-001.3 (docs/ops only) |
| G10.2 Production `SECRET_KEY` | Factory rejects default insecure key; `render.yaml` uses `generateValue: true` for `SECRET_KEY` |
| G10.3 CSRF / cookies / headers | Unchanged in this WP; GA review remains authority |
| G10.4 Ownership scoping | Unchanged in this WP; architecture / GA tests remain authority |
| G10.5 Dependency audit | `./scripts/dependency_audit.sh` hard gate; HOLD register for accepted Medium/Low |
| G10.6 No secrets in artefacts | Release Protocol / Playbook forbid committing `.env`; EI-001.3 adds no secrets |
| G10.7 Migrations / StartupService | Deploy uses `flask db upgrade` / `releaseCommand`; StartupService idempotent admin path documented in `DEPLOYMENT.md` |

---

## 3. Reproducible operator checks

```bash
# Dependency assurance (G10.5)
./scripts/dependency_audit.sh

# Confirm no .env committed
git ls-files .env && echo "FAIL: .env tracked" || echo "OK: .env not tracked"

# Migration head readable in app context (local/CI)
.venv/bin/python -m pytest tests/ga/test_recovery.py::TestDatabaseRestoreVerification -q
```

---

## 4. Explicit residual (ER-RB-04)

**Privacy pack / Stage 1 signatures** remain **OPEN**. EI-001.3 does **not** claim G10 PASS for cohort-expansion or Version 1 declaration claim classes that require signed Privacy Review.

Invite-only Alpha may continue under existing Privacy / EP-008.2B HOLD conditions.

---

## 5. Gate score (engineering)

| Criterion | Status after EI-001.3 |
|-----------|----------------------|
| G10.5 | PASS (EI-001.2) |
| G10.2 / G10.6 / G10.7 operational ack | Advanced / documented |
| Privacy signatures | **Open** (ER-RB-04 residual) |
| Overall G10 for V1 declaration | **IN PROGRESS** until privacy pack closed for intended claim class |

---

**End of G10_OPERATIONAL_EVIDENCE**
