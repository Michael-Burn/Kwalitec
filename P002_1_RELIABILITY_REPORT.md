# P-002.1 — Reliability Report

**Programme:** P-002.1  
**Date:** 2026-08-04  
**Gate:** G8  
**Verdict:** **PASS WITH RESIDUAL**

---

## 1. Scope

- Founder walkthrough reliability path  
- Multi-session / Continue Session contracts  
- Recovery posture  
- Deployment / LIVE health validation  

---

## 2. LIVE deployment fingerprint — PASS

| Endpoint | HTTP | Key fields | Evidence |
|----------|------|------------|----------|
| `/health/live` | 200 | status ok · commit `272a0950ca1a65df01badf5e180c3c06a41681e7` | `knowledge/evidence/releases/P002_1/health/health_live.json` |
| `/health/ready` | 200 | ready=true · database ok · migrations current=head `202607310002` | `…/health_ready.json` |
| `/health` | 200 | production environment · components ok | `…/health.json` |

Matches PB-017 / RO-015 tip. No new deploy required for this validation programme.

---

## 3. Founder / session reliability — PASS (contracts)

| Path | Result | Evidence |
|------|--------|----------|
| Session workflow (PX-003) | Green in premium core | `regression/pytest_premium_core.txt` (72 passed) |
| Continue contention craft | Contracts held | PX-005 / PX-007; LIVE re-measure residual **P0021-R6** |
| Finish confirm / no phantom Complete | Held | PX-007 certification |
| Recovery / backup export shape | Green | `tests/ga/test_recovery.py` in session pack |
| Failure modes | Green | `tests/ga/test_failure_modes.py` |

---

## 4. Prior reliability pack — PASS (procedure)

| Artefact | Role |
|----------|------|
| `docs/production/G8_RELIABILITY_EVIDENCE.md` | G8.4 tabletop rollback · G8.5 backup ack |
| `docs/production/BACKUP_AND_RECOVERY.md` | Recovery law |
| PB-017 health finals | Prior LIVE ready fingerprint |

---

## 5. Sev-1 status — PASS

No open Sev-1 production incidents recorded against the invite-only / Private Beta host for this claim window (re-affirmed 2026-08-04).

---

## 6. Residuals

| ID | Item | Severity |
|----|------|----------|
| P0021-R6 | LIVE Continue contention re-measure (carry PX7-R6) | S3 |
| P0021-R8 | Optional live restore drill before GA marketing | S3 |

---

## 7. Gate disposition

| Criterion | Disposition |
|-----------|-------------|
| G8.1 Health live/ready on tip | **PASS** |
| G8.2 Smoke / protocol | **PASS WITH RESIDUAL** (contracts + PB-017; contention LIVE residual) |
| G8.3 Sev-1 clear | **PASS** |
| G8.4 Rollback documented | **PASS** |
| G8.5 Backup posture | **PASS** |

**Overall G8:** **PASS WITH RESIDUAL**

Signed: P-002.1 Reliability Validation · 2026-08-04
