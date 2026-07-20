# V2-020 — Version 1 Retirement Runbook

**Status:** Operational programme (execute only after ADR-007 evidence gates pass)  
**Authority:** [`ARCHITECTURE_DECISIONS/ADR-007-Legacy-Retirement-Strategy.md`](ARCHITECTURE_DECISIONS/ADR-007-Legacy-Retirement-Strategy.md)  
**Roadmap:** [`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md) § V2-020

This runbook retires Version 1 as the sole student educational path and promotes Version 2. It must not run as a silent traffic switch.

---

## Preconditions (all required)

1. `KWALITEC_V2_DURABLE_STORE=1` proven in production dual-run (restart-safe).
2. `KWALITEC_V2_STUDENT_EXPERIENCE=1` cohort using `/student` + `/session` without dual-authority defects.
3. Founder Curriculum Studio operable at `/founder/studio`.
4. Evidence Gates page (`/founder/evidence-gates`) shows product evidence recorded (not only technical ticks).
5. Backup / restore verified for Postgres.
6. Alembic head includes `202607190001` (V2 aggregate tables).

---

## Dual-run phase (before sole runtime)

| Step | Action | Verify |
|------|--------|--------|
| 1 | Enable durable store + student experience flags | Founder Intelligence dual-run label = `dual-run-active` |
| 2 | Invite alpha cohort via dashboard link to `/student` | Sessions complete; Twin/Adaptive explainability present |
| 3 | Monitor Founder Intelligence for thrash / stalled journeys | No unresolved dual-authority bugs |
| 4 | Keep Mission Adapter as cutover router | V1 dashboard remains available |

Environment (dual-run):

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
# Do NOT set SOLE_RUNTIME yet
```

---

## Sole-runtime cutover (V2-020)

| Step | Action | Verify |
|------|--------|--------|
| 1 | Announce maintenance window | Cohort notified |
| 2 | Take DB backup | Restore dry-run OK |
| 3 | Set `KWALITEC_V2_SOLE_RUNTIME=1` | `/` redirects to `student.home` |
| 4 | Smoke: login → Student Home → Start Session → Complete | End-to-end OK |
| 5 | Keep V1 routes read-only / deprecated for one soak window | No new V1 Twin/recommendation features |
| 6 | Record continuity migration programme if V1 history must move | Separate from this flag flip |

Environment (sole runtime):

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
KWALITEC_V2_SOLE_RUNTIME=1
KWALITEC_V2_FOUNDER_INTELLIGENCE=1
```

---

## Rollback

1. Unset `KWALITEC_V2_SOLE_RUNTIME` (or set to `0`).
2. Redeploy / restart.
3. Confirm `/` redirects to Version 1 dashboard.
4. Leave durable V2 tables intact (do not drop).

---

## Must not

- Drop Version 1 data during first cutover night.
- Treat package completeness as educational proof.
- Enable sole runtime while Evidence Gates product evidence remains open.
