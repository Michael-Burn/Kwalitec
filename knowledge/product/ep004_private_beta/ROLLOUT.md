# Private Beta Rollout Log

**Programme:** EP-004 — Workstream 2  
**Version:** 1.0  
**Updated:** 2026-07-26 (Stage 1 Go under C2)  
**Rule:** Every stage requires a **Go decision**, a **Rollback decision**, and a **Monitoring report** before advancement.

---

## Stage map

```text
Stage 0 — Internal team
        ↓ (Go + monitoring green + privacy path ready)
Stage 1 — Small pilot (5–10 external)
        ↓ (Go + monitoring green + Privacy Review signed)
Stage 2 — Expanded private beta (20–50)
```

No public registration. No marketing launch.

---

## Stage 0 — Internal team

| Field | Value |
|---|---|
| Window | 2026-07-24 (ops day 0) onward |
| Population | BETA-INT-001 … 003 ([`BETA_COHORT.md`](BETA_COHORT.md)) |
| Analytics | Internal-only path authorized — see [`ANALYTICS_ACTIVATION.md`](ANALYTICS_ACTIVATION.md) |
| Educational behaviour | Unchanged |

### Go decision — Stage 0

| Check | Result |
|---|---|
| GA certification retained | Pass — `docs/ga/CERTIFICATION_REPORT.md` |
| EP-002 operational readiness | Pass — READY FOR STAGED ACTIVATION |
| EP-003 protocol approved | Pass — protocol document |
| Educational smoke (Session / Reflection / Journey / Twin) | Pass — Platform Baseline |
| Support workflow ready | Pass — founder-operated |
| Public registration still closed | Pass |

**Decision:** **GO** for Stage 0 (2026-07-24)  
**Owner:** Product  
**Rationale:** Internal dogfood under closed accounts; no external data subjects; measurement labelled exploratory.

### Rollback decision — Stage 0

| Trigger | Action |
|---|---|
| P0 security / data incident | Disable affected accounts; freeze invites; follow `../analytics/ep002/INCIDENT_RESPONSE.md` |
| Educational regression attributed to analytics emit | Set `ANALYTICS_EVENTS_V1=false`; restart; re-run educational smoke |
| Platform instability | Halt Stage 1 planning; restore last known-good deploy per Release Playbook |

**Rollback rehearsed:** Kill switch = env flag OFF (EP-002). **Status:** Ready.

### Monitoring report — Stage 0

See [`OPERATIONS_MONITORING.md`](OPERATIONS_MONITORING.md) § Stage 0 snapshot.

| Signal | Result |
|---|---|
| Dispatch / outbox (flag OFF default) | Healthy dark path — `events_disabled` expected when OFF |
| Worker | Optional dry-run; no backlog requirement while OFF |
| P0 / P1 open | None attributed to EP-004 |
| Educational paths | Unchanged |

**Monitoring verdict:** **GREEN** for Stage 0 continue.

---

## Stage 1 — Small pilot

| Field | Value |
|---|---|
| Target N | 5–10 external invite-only |
| Prerequisite | Privacy Review **signed**; Stage 0 monitoring GREEN; §E Pass; invite pack + consent process; OR-06 C2 |
| Analytics | **C2 — OFF** (`manual` / `exploratory` measurement); no Pilot analytics ON |
| Status | **GO** (2026-07-26) — authorized to invite; candidates not yet selected |

### Go decision — Stage 1

| Check | Result (2026-07-26) |
|---|---|
| Privacy Review signed | **SIGNED** — Product Owner + Privacy Owner (Courage T Shumba) |
| Consent artefacts ready | Invite pack + consent log template **READY**; live capture at send |
| Support export/delete owners named | Courage T Shumba (§E4) |
| Export/delete dry-run + kill-switch | **Pass** §E (internal local) |
| Analytics path | **C2** — flag OFF; scorecard `manual` / `exploratory` |
| Stage 0 monitoring GREEN | Pass (2026-07-24 snapshot; reconfirm 2026-07-26) |
| Enrollment clearance | **FILED** — `../ep008_2a_stage1_operational_readiness/STAGE1_CHECKLIST.md` §B |

**Decision:** **GO** for Stage 1 invite-only enrolment under **C2** (2026-07-26).  
**Owner:** Courage T Shumba (Product Board Chair / Product Owner / Privacy Owner capacities)  
**Rationale:** Critical privacy and ops evidence filed; measurement honesty preserved (analytics OFF).  
**Still required before each send:** OR-07 select candidate; provision account; fill support channel; capture consents in ops store; update `BETA_COHORT.md` (pseudonymous only).  
**Forbidden claims:** educationally effective; Version 1 production-ready; Pilot analytics ON.

### Rollback decision — Stage 1 (pre-armed)

| Trigger | Action |
|---|---|
| Privacy incident | Flag OFF (already OFF under C2); pause invites; incident response |
| Outbox lag / DLQ growth | N/A while flag OFF; if later C1: pause Sessions if UX impacted; drain / replay; flag OFF |
| ≥2 P1 “cannot study” open > SLA | Freeze invites; triage before expansion |

### Monitoring report — Stage 1

*Template ready in [`OPERATIONS_MONITORING.md`](OPERATIONS_MONITORING.md). First Stage 1 monitoring row due after first accepted invite.*

---

## Stage 2 — Expanded private beta

| Field | Value |
|---|---|
| Target N | 20–50 external |
| Prerequisite | Stage 1 GO exit (≥1 week measurement, no open P0, privacy intact) |
| Analytics | Private beta stage ON; hardened cron |
| Status | **HOLD** |

### Go decision — Stage 2

| Check | Result (2026-07-24) |
|---|---|
| Stage 1 completed with monitoring GO | Not started |
| Cohort size path to ≥20 active | Not started |
| EP-002 private-beta go-live row | Not signed |
| Interview schedule planned | Protocol ready |

**Decision:** **NO-GO (hold)** — blocked on Stage 1.

### Rollback decision — Stage 2 (pre-armed)

Same kill switch + invite freeze as Stage 1; additionally stop expansion immediately if continuity (M7) collapses with unexplained P1 spike.

### Monitoring report — Stage 2

*Not started.*

---

## Advancement summary

| From → To | Allowed? | Condition |
|---|---|---|
| — → Stage 0 | **Yes** | Executed 2026-07-24 |
| Stage 0 → Stage 1 | **Yes** | Executed 2026-07-26 — enrollment clearance + Stage 1 Go (C2) |
| Stage 1 → Stage 2 | **Not yet** | Stage 1 monitoring GO + N path |

---

## Exit criteria (WS2)

| Criterion | Status |
|---|---|
| Stage 0 Go / Rollback / Monitoring recorded | COMPLETE |
| Stage 1–2 decision templates + holds recorded | COMPLETE |
| Expanded beta live | OPEN (conditional) |
