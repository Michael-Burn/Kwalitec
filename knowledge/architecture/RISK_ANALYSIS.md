# MS-001 — Educational Runtime Bridge Risk Analysis

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`  
**Companions:** `MIGRATION_PLAN.md`, `ROLLBACK_PLAN.md`, `TEST_STRATEGY.md`

For every migration step: **technical risk**, **educational risk**, **rollback strategy**, **verification strategy**.

---

## Severity scale

| Level | Meaning |
|---|---|
| Critical | Fabricated study, mastery corruption, or sole-runtime false safety |
| High | Session desync, ownership bugs, Evidence bypass |
| Medium | UX empty states, narrative mismatch, ops fragility |
| Low | Telemetry noise, cosmetic projection differences |

---

## P0 — Contracts & golden fixtures

| Dimension | Assessment |
|---|---|
| **Technical risk** | Low — docs/tests only; wrong fixtures later mislead implementers |
| **Educational risk** | Medium if dual-“next” policy left ambiguous — Bridge encodes wrong product law |
| **Rollback** | Revert docs |
| **Verification** | Product sign-off on §5.3 policy; fixture review against live legacy Dashboard |

---

## P1 — Read-path Mission + Learning State

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — ID mapping, lifecycle edge cases, Planning ↔ StudyPlan import fragility when wiring |
| **Educational risk** | Medium — stale mission if ensure not called; empty Home if plan missing (honest but surprising vs demo) |
| **Rollback** | Bridge read flag off (`ROLLBACK_PLAN` P1) |
| **Verification** | Contract tests: Home topic == SQL mission; no `seeded_demo_*` calls; golden readiness labels |

**Specific hazards**

- Showing Completed mission as startable.  
- Cross-user leakage if `student_id` ≠ authenticated user (IDOR).  
- Caching opaque docs that override SQL.

---

## P2 — Recommendation alignment + demote demo

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — RecommendationService vs Planning disagreement must be resolved in projection, not by changing algorithms |
| **Educational risk** | High if alignment wrong — student reads one “next” and studies another |
| **Rollback** | Disable Recommendation bridge slice |
| **Verification** | AC-2: `mission_aligned=true` whenever mission exists; property test topic equality; seed-path unreachable |

**Specific hazards**

- Silently changing RecommendationService priority rules (forbidden).  
- Re-enabling seed “to make Home look full”.

---

## P3 — Write-path Start / Resume

| Dimension | Assessment |
|---|---|
| **Technical risk** | High — double-start, status races, session id map, multi-worker resume without durable store |
| **Educational risk** | High — wrong mission started; progress attributed incorrectly |
| **Rollback** | Disable write flag; fail closed Start; sole runtime off if needed |
| **Verification** | Start flips SQL status; idempotent re-POST; ownership 403; resume only for In Progress; AC-1/4/5/6 |

**Specific hazards**

- Creating Experience-only session when SQL start fails (split brain).  
- Auto-start Pending on GET causing unintended study starts.  
- Revision begin bypassing Planning.

---

## P4 — Complete + Evidence parity

| Dimension | Assessment |
|---|---|
| **Technical risk** | High–Critical — outcome mapping incomplete vs legacy forms; Evidence reject handling |
| **Educational risk** | **Critical** — mastery inflation/deflation; Evidence bypass via orchestrator; invalid exam readiness |
| **Rollback** | Disable EvidenceParity; block Experience complete; audit TopicProgress |
| **Verification** | Same outcome payload → same TopicProgress delta as legacy; Evidence reject paths; no dual writers; AC-7/8 |

**Specific hazards**

- UX complete without educational complete (allowed only transitional).  
- Writing TopicProgress without Evidence Authority.  
- Completing another user’s mission.

---

## P5 — Journey / History / Revision reads

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — query cost, empty-state UX |
| **Educational risk** | Medium — misleading journey % if coverage formula diverges from ReadinessService |
| **Rollback** | Port flags off → empty authentic |
| **Verification** | No demo seeds; Revision begin uses MissionLifecycleBridge; journey numbers match Readiness within tolerance |

---

## P6 — Durable store hardening

| Dimension | Assessment |
|---|---|
| **Technical risk** | High in multi-worker without it; Medium with migration of empty durable docs |
| **Educational risk** | Medium — students appear “new” if durable empty while SQL has history (mitigate: Bridge always reads SQL for educational fields) |
| **Rollback** | Durable flag off |
| **Verification** | Kill worker mid-session → resume surface correct; educational fields still from SQL |

---

## P7 — Internal Alpha Bridge gate

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — false confidence if checklist incomplete |
| **Educational risk** | Critical if Bridge Complete declared with AC gaps then sole runtime enabled |
| **Rollback** | Keep last good phase flags; do not enable sole runtime |
| **Verification** | Full AC-1…AC-10 scorecard; rollback drill; sign-off recorded |

---

## Cross-cutting risks

| Risk | Severity | Mitigation |
|---|---|---|
| Treating `SOLE_RUNTIME` as Bridge Complete | Critical | Explicit gate in ops runbooks; evidence_gates messaging |
| Big-bang deploy P1–P4 | High | Phase release train |
| Changing Planning/Recommendation algorithms “while bridging” | High | Bridge translates only; behaviour change = separate milestone |
| Schema “quick fix” migrations | Medium | Forbidden in Bridge programme |
| MissionEngine* accidentally injected as authority | High | Composition: engines unset; Bridge adapters only |
| Multi-tenant IDOR via student_id param | High | Always bind to `current_user.id` |

---

## Residual risks after Bridge Complete

| Residual | Acceptance |
|---|---|
| Dual “next” producers still exist in code | Accepted if projection aligns |
| Legacy UI still available when sole runtime off | Accepted |
| Activity content may be thinner than legacy session UI | Accepted until content parity programme |
| V2 engines still unwired | Accepted; future ADR |

---

## Stop condition

Risk analysis complete for all migration steps. **No production code.**
