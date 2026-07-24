# PRD-001 Revision Summary

**Document:** `PRD_001_REVISION_SUMMARY.md`  
**Subject:** [`PRD-001_LEARNING_ANALYTICS_PHASE1.md`](PRD-001_LEARNING_ANALYTICS_PHASE1.md) v1.1  
**Source review:** [`PRD_001_REVIEW.md`](PRD_001_REVIEW.md) — APPROVE WITH CHANGES  
**Revision date:** 2026-07-24  
**Constraint:** Documentation only — no application code modified  

---

## Outcome

| Item | Result |
|---|---|
| Prior recommendation | APPROVE WITH CHANGES |
| Post-revision PRD status | **Approved** (v1.1) |
| Governance blockers | **Resolved** in document |
| Implementation | Still requires milestone + Phase A ADR + flag discipline; external cohort needs Privacy Review checklist |

---

## Every review finding → action taken

### Review 1 — Vision

| Finding | Action |
|---|---|
| Student benefit missing design-question map | §2 table maps all four Vision design questions (indirect) |
| Privacy conditional (retention/export open) | §7–§8 close retention, deletion, export, purpose limitation |
| O1–O8 overclaim risk | Scope limited to O1, O2, O7 (+ observe journey/ESS/Twin); O3/O8 removed from claims |

### Review 2 — Blueprint

| Finding | Action |
|---|---|
| Revision adherence claimed without events | Removed O3 from educational benefit, rollout, and success criteria |
| Terminology / dual responsibility | Authority clarification §5; Student History preserved |

### Review 3 — Architecture

| Finding | Action |
|---|---|
| ESS “sole authority” wording imprecise | §5: ESS = sole assembler; Twin/Evidence/Mission remain domain authorities; analytics never authoritative |
| Analytics Architecture Q1–Q2 open | Closed in §7.1–§7.4 and §21 |
| Framework freeze vs PRD scope (O3/O8) | PRD defers O3/O8; Framework §9 amended to match |
| Recommendation optional thin emit ambiguity | Hard exclude; future PRD only |

### Review 4 — Data governance

| Finding | Action |
|---|---|
| Retention TBD | Raw 18 months; aggregates 36 months; snapshots = raw (§7.1) |
| Deletion unspecified | Student 30-day cascade; scheduled purge; cascade rules (§7.2) |
| Export unspecified | Student JSON; admin aggregate; audit export (§7.3) |
| Hash vs payload deferred | Hash + metadata only for ESS/Twin; full payload fields enumerated per event (§7.4) |

### Review 5 — Performance

| Finding | Action |
|---|---|
| No budgets | §10 measurable budgets (latency, hash overhead, storage, payload, batch, outbox delay, path regression) |

### Review 6 — Security

| Finding | Action |
|---|---|
| Tamper / replay underspecified | §9: server-side only, append-only, idempotency keys, optional row HMAC, AuthZ matrix, fail-open + outbox, audit log |

### Review 7 — Privacy

| Finding | Action |
|---|---|
| Consent / visibility / deletion incomplete | §8 minimum collection, purpose limitation, visibility, consent assumptions, deletion workflow, Privacy Review checkpoint |

### Review 8 — Test strategy

| Finding | Action |
|---|---|
| Incomplete test plan | §17 unit / integration / load / failure / regression |

### Review 9 — Risks

| Finding | Action |
|---|---|
| Risks section missing from PRD | §14 risk register with mitigations |

### Review 10 — Decision / template

| Finding | Action |
|---|---|
| Missing Metrics, Risks, DoD | §12–§15 |
| Missing Out of scope / Dependencies | §18, §21 |
| Added per revision directive | Rollback §19, Release §20, Phases §11, Traceability §22 |
| Status | Set to **Approved** after blocker closure |

---

## Scope synchronisation (CHANGE 2)

| Outcome | PRD-001 v1.1 |
|---|---|
| O1 Study consistency | In scope (via Session events) |
| O2 Session completion | In scope |
| O3 Revision adherence | **Deferred** — no claims |
| O4 Retention | Observe only via hash snapshots — no mastery math |
| O7 Reflection completion | In scope |
| O8 Recommendation acceptance | **Deferred** — no claims |
| O5/O6/O9 | Out of scope |

Educational Validation Framework freeze text updated to match.

---

## Remaining risks (accepted / residual)

| Risk | Status |
|---|---|
| Fail-open emit undercounts metrics until outbox drains | Accepted residual — mitigated by alerts + coverage metric |
| Manual student export SLA (14 days) in beta | Accepted until automated export ships |
| Cohort Privacy Review checklist still unsigned operationally | **Operational gate** — not a PRD text gap; blocks external invites |
| Aggregate anonymisation method for admin CSV (research tokens) | Residual design detail for Phase A ADR |
| Optional `row_hmac` may be deferred to ADR if operational cost high | Allowed if append-only + no UPDATE enforced |

---

## Outstanding questions

| # | Question | Owner | Blocks PRD-001 Approved? |
|---|---|---|---|
| 1 | Pass-rate methodology (Analytics Architecture former §9.3) | Future O9 PRD | **No** |
| 2 | Decision Journal as sole O8 acceptance source (former §9.4) | Future recommendation PRD | **No** |
| 3 | Exact HMAC secret rotation for `row_hmac` if enabled | Phase A ADR | **No** |
| 4 | Automated vs manual export implementation date | Engineering + Support | **No** |

Former blockers (retention, hash vs payload) are **closed**.

---

## Exit criteria checklist

| Criterion | Met? |
|---|---|
| All governance blockers from PRD_001_REVIEW resolved | **Yes** |
| No unresolved template gaps | **Yes** |
| Scope consistent with Framework | **Yes** |
| Privacy complete in PRD | **Yes** |
| Security complete in PRD | **Yes** |
| Performance budgets defined | **Yes** |
| Definition of Done complete | **Yes** |
| Implementation phases defined | **Yes** |

**PRD-001 Status = Approved.**

Implementation remains prohibited until an implementation milestone begins under this Approved PRD (Phase A ADR + feature flag). No application code was modified in this revision.
