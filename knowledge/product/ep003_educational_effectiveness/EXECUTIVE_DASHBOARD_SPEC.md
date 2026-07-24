# Executive Dashboard Specification

**Programme:** EP-003 — Workstream 6  
**Version:** 1.0  
**Status:** Spec only — **no implementation in this programme**  
**Updated:** 2026-07-24  
**Audience:** Founder / executive  
**Does not:** Ship UI, collectors, Twin logic, or analytics infrastructure

---

## 1. Purpose

Specify an executive dashboard that shows whether the Version 1 Platform Baseline is **healthy, educationally effective, beta-progressing, privacy-safe, and operationally sound** — with known risks visible.

This extends (does not replace) EP-001 [`PRODUCT_DASHBOARD_SPEC.md`](../ep001_product_validation/PRODUCT_DASHBOARD_SPEC.md) with EP-003 sections required for educational Go / No-Go.

**Implementation** requires a future Approved PRD after Phase 1 events are available in the target environment (EP-002 go-live). Prefer extending existing Founder observability surfaces over a parallel app.

---

## 2. Architecture rules (when implemented)

| Rule | Detail |
|---|---|
| Read models only | Projections from event store + educational authorities |
| One formula | Same as Educational Metrics / Scorecard — no private mastery math |
| Auth | Admin / founder only |
| Privacy | Aggregate + opaque IDs; no reflection body text; no Twin payload |
| Empty states | Below sample thresholds → “insufficient N” |
| No new vendor SDK | Without Security + Privacy review |

---

## 3. Dashboard sections

### 3.1 Platform Health

| Tile | Source | Notes |
|---|---|---|
| App version / last tag | `VERSION` / release notes | |
| CI gate summary | pytest + ruff last green | Link Quality Manual |
| Open P0 / P1 defects | Issue tracker / support | |
| GA residual risks | `docs/ga/CERTIFICATION_REPORT.md` | CSP, DLQ, etc. |
| Analytics flag state | `ANALYTICS_EVENTS_V1` ON/OFF | EP-002 |

### 3.2 Educational KPIs

| Tile | Metric ID | Definition source |
|---|---|---|
| Weekly Active Learners | M1 | EDUCATIONAL_METRICS |
| Sessions per WAL | M2 | |
| Reflection Completion | M3 | |
| Session Completion | M4 | |
| Progress Velocity | M5 | Label provisional if Journey emit off |
| Study Consistency | M6 | |
| Learning Continuity | M7 | |
| Time to Readiness | M8 | Summarise Twin bands only |
| Curriculum Completion | M9 | |

Each tile cites metric ID. Week selector + aggregate CSV export (no free-text PII).

### 3.3 Beta Progress

| Tile | Source |
|---|---|
| Invited / accepted / active N | Ops roster |
| Cohort week number | Protocol |
| Interview completion count | Feedback system |
| Onboarding success (invite → Session ≤7d) | Scorecard Activation |
| Privacy checklist signed? | PRIVACY_REVIEW |
| Protocol exit criteria checklist | PRIVATE_BETA_PROTOCOL §8 |

### 3.4 Privacy Status

| Tile | Source |
|---|---|
| Invite-only enforcement | Config / ops attestation |
| Analytics retention / purge posture | EP-002 privacy ops |
| Open privacy checklist items | PRIVACY_REVIEW |
| Export/delete request SLA | Ops (manual OK in beta) |
| Last privacy incident | Security log (or “none”) |

### 3.5 Operational Status

| Tile | Source |
|---|---|
| Support P0/P1 open | SUPPORT_WORKFLOW |
| Median response by tier | Support ops |
| Error / health endpoints | GA health |
| Outbox / analytics worker health | EP-002 monitoring (when ON) |
| Backup / restore attestation | Ops docs |

### 3.6 Known Risks

| Tile | Source |
|---|---|
| Top educational risks | VERSION_1_EDUCATIONAL_REVIEW §8 |
| Top security residuals | GA CERTIFICATION_REPORT |
| Experiment / PRD holds | EXPERIMENT_FRAMEWORK register |
| Recommendation claim freeze | Explicit banner: excluded until PRD |
| Go / No-Go pending gates | GO_NO_GO_REPORT |

---

## 4. Wireframe (logical)

```text
┌─────────────────────────────────────────────────────────────┐
│  Kwalitec Executive — Educational Effectiveness             │
│  Week: [selector]   Analytics: ON|OFF   Cohort: N=__        │
├───────────────┬───────────────┬───────────────┬─────────────┤
│ Platform      │ Educational   │ Beta Progress │ Privacy     │
│ Health        │ KPIs (M1–M9)  │               │ Status      │
├───────────────┴───────────────┴───────────────┴─────────────┤
│ Operational Status                                          │
├─────────────────────────────────────────────────────────────┤
│ Known Risks (ordered)     │ Go / No-Go summary strip        │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Acceptance criteria (future implementation milestone)

- [ ] All six sections present
- [ ] Each educational tile cites M-ID or “ops/context”
- [ ] Insufficient-N empty states
- [ ] Week selector + aggregate CSV export
- [ ] Tests: aggregation does not import Twin calculators for mastery rewrite
- [ ] Linked from Release Playbook as founder check
- [ ] Separate Approved PRD before build

---

## 6. Non-goals

- Student-facing History redesign
- Real-time vanity clickstream
- Public marketing metrics site
- Implementation under EP-003 authority

---

## 7. Exit criteria (WS6)

| Criterion | Status |
|---|---|
| Spec complete with required sections | COMPLETE |
| Implementation explicitly deferred | COMPLETE |
| Aligns with Metrics + Scorecard | COMPLETE |

---

## References

- [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md)
- [`PRODUCT_SCORECARD.md`](PRODUCT_SCORECARD.md)
- [`../ep001_product_validation/PRODUCT_DASHBOARD_SPEC.md`](../ep001_product_validation/PRODUCT_DASHBOARD_SPEC.md)
- `knowledge/product/analytics/ep002/MONITORING_SPECIFICATION.md`
- Founder dashboard surfaces (`app/founder/dashboard`)
