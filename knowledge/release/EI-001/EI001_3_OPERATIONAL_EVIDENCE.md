# EI-001.3 — Operational Evidence

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.3 — Release Operations & Deployment Evidence  
**Date:** 2026-07-28  
**Environment class:** Local / CI regression + documented production operator procedures  
**Application behaviour:** Unchanged

---

## 1. Index of durable evidence

| Gate | Durable path | WP status |
|------|--------------|-----------|
| G7 | `docs/production/G7_PERFORMANCE_HOLD.md` | HOLD filed; G7.1 green |
| G8 | `docs/production/G8_RELIABILITY_EVIDENCE.md` | G8.4 + G8.5 filed |
| G10 ops | `docs/production/G10_OPERATIONAL_EVIDENCE.md` | Ops ack; privacy open |
| G12 | `docs/production/VERSION_1_FLAG_MATRIX.md` | Published + aligned |
| Deploy | `docs/production/DEPLOYMENT.md` | Unchanged content; referenced |
| Backup | `docs/production/BACKUP_AND_RECOVERY.md` | Acknowledged for claim class |
| RC fingerprint | `docs/production/RELEASE_CANDIDATE_FINGERPRINT.md` | Prior EI-001.1 |

Board status cells: `knowledge/product/p003_1_version1_release_dossier/Release_Gates.md`.

---

## 2. Deployment documentation reproducibility

Operators can reproduce deploy / verify / rollback using:

1. `docs/production/DEPLOYMENT.md` — sequence, health, rollback  
2. `docs/production/ENVIRONMENT.md` — secrets / env  
3. `docs/process/RELEASE_PROTOCOL.md` — release classification + smoke  
4. `knowledge/RELEASE_PLAYBOOK.md` — operator summary + G12 pointer  
5. `docs/production/VERSION_1_FLAG_MATRIX.md` — production flag defaults  

No application code changes were required for reproducibility.

---

## 3. Environment verification (this WP)

| Check | Command / method | Outcome |
|-------|------------------|---------|
| Architecture release-ops integrity | `pytest tests/architecture/test_release_operations.py` | Pass (see test report) |
| Production docs presence | `pytest tests/ga/test_documentation.py` | Pass |
| G7.1 soft budgets | `pytest tests/ga/test_performance_benchmarks.py` | Pass |
| Backup / recovery docs + migration readability | `pytest tests/ga/test_recovery.py` | Pass |
| Dependency assurance (G10.5) | `./scripts/dependency_audit.sh` | Pass (prior EI-001.2; re-run in test report) |
| `.env` not tracked | `git ls-files .env` | Empty |
| `render.yaml` production-ON flags | Architecture test via `render_env_map()` | Pass |

Staging/production HTTP operator sample: **not executed** (G7 HOLD).

---

## 4. Feature-flag evidence

Production-ON set (Render) matches matrix §2:

- `KWALITEC_V2_SOLE_RUNTIME=1`  
- `KWALITEC_V2_STUDENT_EXPERIENCE=1`  
- `KWALITEC_V2_DURABLE_STORE=1`  
- `KWALITEC_V2_INJECT_ENGINES=1`  
- `KWALITEC_V2_SEED_DEMO=0`  
- `KWALITEC_V2_FOUNDER_INTELLIGENCE=1`  
- `KWALITEC_EI_INTERNAL_ALPHA=1`  

Educational Twin / Journey / personalisation / adaptive assessment / analytics emit remain **OFF** and must not be marketed as live.

---

## 5. Operational checklists used

- `knowledge/release/RELEASE_CHECKLIST.md` (updated with EI-001.3 pointers)  
- `docs/ga/RELEASE_CHECKLIST.md`  
- `docs/production/G8_RELIABILITY_EVIDENCE.md` disaster-recovery / rollback checklist references  

---

## 6. Residual operator actions (not closed by this WP)

| Action | Owner | Blocks |
|--------|-------|--------|
| Staging/production G7.2 sample + load test | Release | Lifting G7 HOLD / high-traffic claims |
| Tagged RC + green Actions URL | Release | G11 declaration package |
| Live restore drill (optional for Alpha) | Release | Stronger G8 for GA marketing |
| Privacy Review signatures | Privacy / Product | ER-RB-04 / Stage 1 / V1 claim class |

---

**End of EI001_3_OPERATIONAL_EVIDENCE**
