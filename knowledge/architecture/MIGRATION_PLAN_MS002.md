# MS-002 — Migration Plan (Educational Journey / History)

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Risks:** `RISK_ANALYSIS_MS002.md`  
**Related:** MS-001 `MIGRATION_PLAN.md` phase **P5** (refined here)

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Reversible** — feature-flag rollback per phase.  
3. **No big-bang** — never flip Journey + History + Sole Runtime + demo-off together.  
4. **No schema changes.**  
5. **No UI redesign.**  
6. **Read-only** — Journey/History bridges never write educational state.  
7. **Empty authentic over demo** when bridge flags are on.  
8. **Depends on MS-001** — Mission identity and Recommendation alignment already bridged improve Journey/History fidelity; Journey Bridge can still ship after Mission Read at minimum.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? |
|---|---|---|---|
| J0 | Contracts, fixtures, ADRs | Yes (docs/tests) | No |
| J1 | JourneyAdapter core projection | Yes | No |
| J2 | Journey timeline + traceability | Yes | No |
| J3 | HistoryAdapter list projection | Yes | No |
| J4 | History pagination / filters / readiness series | Yes | No |
| J5 | Inspect Evidence + Recommendation Change | Yes | No |
| J6 | Home cards + demo gate + dual-run soak | Yes | No |
| J7 | Internal Alpha — Journey Bridge Complete | Yes (ops) | No |
| — | **Journey Bridge Complete** | — | JC-1…JC-10 |

Revision options bridge remains MS-001 P5 companion (optional parallel; not required for Journey Bridge Complete unless product expands definition).

---

## J0 — Contracts, fixtures, ADRs

### Scope

- Accept MS-002 architecture docs.  
- Accept ADR-MS002-001 (and draft 002/003).  
- Capture golden learners: empty plan, learning mid-plan, revision stage, multi-mission history.  
- Document expected Journey progress ratios vs ReadinessService and History session lists vs SQL Missions.

### Exit criteria

- ADRs accepted for authority.  
- Fixture table agreed.  

### Rollback

N/A (docs only).

---

## J1 — JourneyAdapter core projection

### Scope

- `JourneyBridge.project_journey` behind `ENABLE_JOURNEY_BRIDGE`.  
- Progress + topics + active mission + empty authentic.  
- Wire `LearningJourneyPort` composition when flag on.  
- **Do not** yet require full timeline / recommendation delta.

### Exit criteria

- Journey page topic order matches CurriculumService × TopicProgress for golden users.  
- Progress ratio matches ReadinessService within tolerance.  
- No `seeded_demo_journey` when flag on.  
- Legacy surfaces unchanged.

### Rollback

Disable `ENABLE_JOURNEY_BRIDGE` → prior Experience journey adapter. Prefer empty authentic in Alpha if seed re-enable is undesirable.

---

## J2 — Journey timeline + traceability

### Scope

- Timeline events from Missions / Attempts / Lifecycle / Progress milestones.  
- Attach `TraceRef` (What / Why / Evidence / Recommendation state).  
- Recommendation focus aligned with Recommendation Read Bridge when available.

### Exit criteria

- Traceability checks T-1…T-5 pass on golden fixtures.  
- Telemetry `JOURNEY_BRIDGE_*` visible.

### Rollback

Flag off; or feature-slice flag for timeline only if split.

---

## J3 — HistoryAdapter list projection

### Scope

- `HistoryBridge.project_history` behind `ENABLE_HISTORY_BRIDGE`.  
- Completed sessions + minutes + mastered topics + revision labels.  
- Replace Twin demo insights path for HistoryService when flag on.

### Exit criteria

- History session list matches owned completed Missions for golden users.  
- No fabricated Twin sessions when flag on.  
- Raw event keys never appear.

### Rollback

Disable `ENABLE_HISTORY_BRIDGE`.

---

## J4 — Pagination, filters, readiness progression

### Scope

- `limit` / `offset` (or cursor), date/topic/stage filters, hard max.  
- Readiness progression per ADR-MS002-002 (derived policy).  

### Exit criteria

- Pagination stable (no dup/skip under concurrent inserts beyond documented cursor rules).  
- Readiness series empty or derived — never demo curves.  
- Query budgets acceptable in Alpha.

### Rollback

Disable progression slice or whole History flag.

---

## J5 — Inspect Evidence + Recommendation Change

### Scope

- `get_evidence_summary` (read-only).  
- `get_recommendation_change` with honest `unavailable`.  

### Exit criteria

- Ownership failures → FORBIDDEN/NOT_FOUND.  
- No evidence re-commit on inspect.  
- Recommendation delta never fabricated.

### Rollback

Disable detail endpoints / flag slice; list projections remain.

---

## J6 — Home cards + demo gate + dual-run

### Scope

- Home journey/history cards consume same bridges (snippet limits).  
- Confirm composition never calls journey/history demo seeds when both flags on.  
- Dual-run: compare Bridge vs legacy Analytics / readiness for soak cohort.

### Exit criteria

- Single SoT for cards and pages.  
- Dual-run mismatches within tolerance or documented.  

### Rollback

Per-flag off; cards fall back independently.

---

## J7 — Internal Alpha gate — Journey Bridge Complete

### Scope

- Scorecard JC-1…JC-10 + traceability T-1…T-6.  
- Rollback drill (disable Journey, disable History, disable both).  
- Declare **Journey Bridge Complete** when met.

### Exit criteria

- Definition in parent §16 satisfied.  
- Do **not** enable production `SOLE_RUNTIME` solely because Journey Bridge shipped.

### Rollback

Keep last good flags; do not advance sole-runtime go/no-go.

---

## Dependency graph

```text
J0 → J1 → J2
J0 → J3 → J4 → J5
J2 + J5 → J6 → J7
```

- J1 and J3 may proceed in parallel after J0.  
- J5 should follow J2 or J3 enough that event ids exist.  
- MS-001 Mission Read / Recommendation Read **recommended before J2** for coherent recommendation_focus; not a hard blocker for J1.

---

## Release train rules

| Rule | Detail |
|---|---|
| One major phase per deploy preferred | Especially J3→J4 query cost |
| Soak | ≥ 1 Alpha soak between J4 and J7 |
| Monitoring | Bridge latency, fallback rate, empty vs non-empty ratio, ownership denials |
| Flags default off | Until phase exit criteria pass |

---

## Relationship to MS-001 P5

MS-001 P5 bundled Journey / History / Revision. MS-002 **splits Journey/History** into J0–J7 with explicit continuity/traceability acceptance. Revision options remain tracked under MS-001 P5 / future directive unless pulled into J7 by product decision.

---

## Stop condition

Migration design only. Do not implement phases under this directive.
