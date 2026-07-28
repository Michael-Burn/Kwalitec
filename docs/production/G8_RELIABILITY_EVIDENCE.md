# G8 Reliability — Evidence Pack (EI-001.3)

**Programme:** EI-001.3 — Release Operations & Deployment Evidence  
**Authority:** P-002.1 Gate G8 · ER-RB-03 · `docs/production/DEPLOYMENT.md` · `docs/production/BACKUP_AND_RECOVERY.md`  
**Date:** 2026-07-28  
**Claim class:** Invite-only Internal Alpha / engineering Version 1 evidence  
**Disposition:** G8.4 + G8.5 artefacts filed; G8.1–G8.3 procedures bound to Release Protocol

---

## 1. Scope

Closes ER-RB-03 clearance: *G8.4 + G8.5 artefacts filed for claim window.*

| Criterion | Artefact in this pack |
|-----------|------------------------|
| G8.1 Health live/ready | Verification commands (§2); executed on tagged deploy by Release operator |
| G8.2 Production smoke | Pointer to Protocol + GA checklist (§3) |
| G8.3 Sev-1 incidents | Claim-window statement (§4) |
| G8.4 Rollback path | Tabletop drill note (§5) |
| G8.5 Backup / recovery | Release-class acknowledgement (§6) |

---

## 2. G8.1 — Health verification (reproducible)

On the deployed fingerprint (`KWALITEC_GIT_COMMIT` / platform commit env matching the RC tag):

```bash
export BASE_URL="https://<host>"
curl -fsS "$BASE_URL/health/live"
curl -fsS "$BASE_URL/health/ready"
curl -fsS "$BASE_URL/health"
```

Pass criteria: HTTP 200; ready payload indicates database / migration readiness per Runbook.

Local / CI surrogate (factory health, not production SLO): covered by GA / architecture suites — see EI-001.3 test report.

---

## 3. G8.2 — Smoke pack

Execute as applicable for the release class:

1. `docs/process/RELEASE_PROTOCOL.md` — production smoke section  
2. `docs/ga/RELEASE_CHECKLIST.md`  
3. `knowledge/release/RELEASE_CHECKLIST.md` (EI educational-intelligence smoke when EI is in scope)  
4. Canonical student home under sole runtime (`KWALITEC_V2_SOLE_RUNTIME=1`)

---

## 4. G8.3 — Sev-1 incident status (claim window)

**Engineering statement (2026-07-28):** No open Sev-1 production incidents are recorded against the invite-only Alpha host for the EI-001.3 evidence window. Re-affirm at declaration time in the Version 1 Evidence Package.

If a Sev-1 opens before declaration: G8.3 → FAIL until resolved / accepted with Product disclosure.

---

## 5. G8.4 — Rollback drill note (tabletop, 2026-07-28)

**Type:** Tabletop verification of documented rollback path (no production traffic cutover performed in this WP — application behaviour frozen).  
**Authority paths:** `docs/production/DEPLOYMENT.md` (Rollback) · `knowledge/RELEASE_PLAYBOOK.md` §3 · `docs/production/BACKUP_AND_RECOVERY.md`

### Drill steps reviewed

1. Identify last known-good git tag / Render deploy.  
2. Redeploy previous release artefact / tag (prefer redeploy over in-place mutation).  
3. If a migration must be reversed: **restore from backup first** (do not rely on `alembic downgrade` in production).  
4. Confirm `/health/ready` → 200.  
5. Smoke: admin/student login paths; sole-runtime home; console overview for Founder.  
6. Record outcome in release / incident report.

### Drill outcome

| Check | Result |
|-------|--------|
| Rollback steps documented and operator-actionable | **Pass** |
| Migration reverse strategy prefers restore | **Pass** (documented) |
| Health + smoke post-rollback criteria defined | **Pass** |
| Live production rollback executed in this WP | **Not performed** (behaviour freeze; tabletop only) |

**Residual:** Live restore / rollback under maintenance window remains an operator exercise before high-stakes GA claims; debt watch via ER-TD-H06 closure (procedure filed).

---

## 6. G8.5 — Backup / recovery acknowledgement

For the **invite-only Internal Alpha / engineering claim class**, Engineering + Release acknowledge:

| Item | Posture |
|------|---------|
| Strategy | `docs/production/BACKUP_AND_RECOVERY.md` — Render automated Postgres backups + pre-migrate manual `pg_dump` |
| Secrets | Platform secret store; never in git |
| Curriculum source | Git history |
| Restore procedure | Documented `pg_restore` + health + smoke |
| Known limitation | In-process JobRunner DLQ not durable across restarts |
| Dual DB note | If Education OS dual-run DB enabled, both URLs must be backed up |

**Acknowledgement:** Backup/recovery documentation is accepted as the release-class posture for EI-001.3 / invite-only Alpha. A **live restore drill** is recommended before marketing push / Stage 1 expansion but is not required to close ER-RB-03 procedure evidence.

---

## 7. Gate score (engineering)

| Criterion | Status |
|-----------|--------|
| G8.1 | Procedure met; production fingerprint at tag time = Release operator |
| G8.2 | Procedure met |
| G8.3 | Clear for EI-001.3 window (re-affirm at declaration) |
| G8.4 | **Met** — tabletop drill note filed |
| G8.5 | **Met** — backup/recovery acknowledgement filed |

**Overall G8:** **Advanced to Partially met / procedure-complete** for invite-only claim class. Full PASS at Version 1 declaration still requires tagged-deploy health/smoke fingerprint in the Evidence Package.

---

**End of G8_RELIABILITY_EVIDENCE**
