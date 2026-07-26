# MS-002 — Risk Analysis (Educational Journey / History)

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Migration:** `MIGRATION_PLAN_MS002.md`  
**Related:** MS-001 `RISK_ANALYSIS.md` (P5 refined)

---

## 1. Risk rating scale

| Level | Meaning |
|---|---|
| **Low** | Contained; flag rollback sufficient |
| **Medium** | Trust or performance impact; needs soak / ADR |
| **High** | Educational integrity risk if shipped wrong |
| **Critical** | Could falsely declare continuity / sole-runtime readiness |

---

## 2. Phase risks

### J0 — Contracts / ADRs

| Dimension | Assessment |
|---|---|
| Technical | Low |
| Educational | Low |
| Rollback | N/A |
| Verification | ADR acceptance recorded |

---

### J1 — JourneyAdapter core

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — composition wiring, Curriculum V1/V2 traversal |
| **Educational risk** | **High** — divergent progress % vs ReadinessService destroys trust |
| **Rollback** | `ENABLE_JOURNEY_BRIDGE` off |
| **Verification** | Golden ratio tolerance; topic order parity; no demo seed |
| **Mitigation** | Adapter calls ReadinessService; forbids local formula |

---

### J2 — Timeline + traceability

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — event_id stability, volume |
| **Educational risk** | Medium — over-claiming recommendation causation |
| **Rollback** | Flag / timeline slice off |
| **Verification** | Traceability T-1…T-5; honest `unavailable` |
| **Mitigation** | Matrix §3 states mandatory; no fabricated deltas |

---

### J3 — HistoryAdapter list

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — Mission/Attempt query shapes |
| **Educational risk** | High if Twin demo still mixed when flag on |
| **Rollback** | `ENABLE_HISTORY_BRIDGE` off |
| **Verification** | Session list == completed Missions; strip raw events |
| **Mitigation** | Single insights source behind flag; Alpha checklist |

---

### J4 — Pagination / readiness series

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium–High — query cost, pagination cursors |
| **Educational risk** | High if readiness series fabricated or misleadingly smooth |
| **Rollback** | Disable series or History flag |
| **Verification** | ADR-MS002-002 policy; load tests; empty-ok |
| **Mitigation** | Hard max limit; derived-only series; prefer empty over fake |

---

### J5 — Inspect Evidence / Recommendation Change

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium |
| **Educational risk** | **High** — inspect must not re-write evidence; deltas must not invent |
| **Rollback** | Detail slice off |
| **Verification** | FORBIDDEN paths; no mastery writes in call graph; unavailable policy |
| **Mitigation** | Read-only service APIs; architecture tests forbidding write imports |

---

### J6 — Home cards + demo gate

| Dimension | Assessment |
|---|---|
| **Technical risk** | Low–Medium |
| **Educational risk** | Medium — dual SoT if cards still seeded |
| **Rollback** | Per-flag |
| **Verification** | Cards and pages same authority tags |
| **Mitigation** | Shared Bridge methods; composition audit |

---

### J7 — Journey Bridge Complete gate

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — false confidence |
| **Educational risk** | **Critical** if Complete declared with JC gaps then sole-runtime enabled |
| **Rollback** | Hold flags; block sole-runtime go/no-go |
| **Verification** | Full JC + T scorecard; rollback drill |
| **Mitigation** | Explicit Complete definition; separate sole-runtime decision |

---

## 3. Cross-cutting risks

| Risk | Severity | Mitigation |
|---|---|---|
| Progress formula drift from Analytics / Readiness | High | Single ReadinessService API; contract tests |
| No recommendation audit table | Medium | ADR-MS002-003; `unavailable` allowed |
| Plan edit appears to wipe Journey | High | ContinuityService awareness; show owned history across plans |
| Partial flag matrix (Journey on, History off) confuses Alpha | Medium | Document matrix; Complete requires both |
| Performance regression on History | Medium | Pagination, indexes already on user_id/date (ops verify), soak |
| Experience still runs educational math in facades | High | Facades format only; CI import rules |
| Confusion with V2 LearningJourneyEngine | Medium | ADR-MS002-001 rejects as SoT for this programme |
| MS-001 Recommendation bridge off while Journey shows focus | Medium | Degrade focus to mission topic only or empty; no demo |

---

## 4. Educational integrity threats (explicit)

1. **Fabricated journey %** — student believes more progress than TopicProgress supports.  
2. **Fabricated history sessions** — false accomplishment narrative.  
3. **Invented recommendation deltas** — false explainability.  
4. **Evidence inspect that mutates mastery** — violates Evidence Before Completion / read-only law.  
5. **Cross-user leakage** — timeline without ownership checks.

Any of the above is a **ship blocker** for Journey Bridge Complete.

---

## 5. Rollback summary

| Phase | Primary rollback |
|---|---|
| J1–J2 | `ENABLE_JOURNEY_BRIDGE=false` |
| J3–J5 | `ENABLE_HISTORY_BRIDGE=false` (or detail slice) |
| J6 | Per-flag; verify seeds not reintroduced unexpectedly |
| J7 | Freeze flags; do not promote sole-runtime |

Emergency: disable umbrella Educational Runtime Bridge if composition couples flags unsafely — document actual coupling during implementation.

---

## 6. Residual risks after Journey Bridge Complete

- Historical readiness fidelity limited without time-travel tables (accepted under ADR-MS002-002).  
- Recommendation history may remain partially `unavailable`.  
- Revision options bridge may still be demo until MS-001 P5 Revision slice.  
- Legacy Analytics UI may still exist alongside History (dual presentation, single educational SoT if Bridge on).

---

## Stop condition

Risk register for architecture only. Update during implementation milestones with measured incidents.
