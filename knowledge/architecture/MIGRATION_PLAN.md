# MS-001 — Educational Runtime Bridge Migration Plan

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`  
**Rollback:** `ROLLBACK_PLAN.md`  
**Risks:** `RISK_ANALYSIS.md`

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Rollbackable** — each phase has a documented rollback (see `ROLLBACK_PLAN.md`).  
3. **No big-bang** — never flip Bridge + Sole Runtime + Evidence parity together.  
4. **No schema changes** — reuse existing SQL tables.  
5. **No UI redesign** — projections feed existing templates.  
6. **No educational behaviour change** — golden fixtures must match legacy outputs.  
7. **Flag-gated** — Bridge off by default until phase exit criteria pass.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? |
|---|---|---|---|
| P0 | Contracts & golden fixtures | Yes (tests/docs) | No |
| P1 | Read-path Mission + Learning State | Yes | No |
| P2 | Recommendation alignment + demote demo seed | Yes | No |
| P3 | Write-path Start / Resume | Yes | Mission status only |
| P4 | Complete + Evidence parity | Yes | Mastery path |
| P5 | Journey / History / Revision read bridges | Yes | No |
| P6 | Durable store hardening | Yes | No (ops) |
| P7 | Internal Alpha Bridge gate | Yes (ops) | As prior |
| — | **Bridge Complete** | — | AC-1…AC-10 |
| P8+ | Post-Bridge (sole runtime proof, legacy UI) | Later programme | — |

---

## P0 — Contracts & golden fixtures

### Scope

- Freeze interface contracts (`BRIDGE_INTERFACE_SPECIFICATION.md`).  
- Capture golden educational fixtures from Runtime A for representative learners (plan + TopicProgress → mission topic, readiness labels, recommendation titles).  
- Add **failing or skipped** contract test scaffolds only if milestone allows test-only files; otherwise document fixture tables in `TEST_STRATEGY.md` (this directive prefers docs-only — implement tests in later engineering milestones).

### Exit criteria

- Fixture set agreed (min: empty plan, active learning plan, revision-stage plan, completed mission).  
- Dual-“next” policy (§5.3 parent doc) signed by product.

### Rollback

N/A (docs/tests only).

---

## P1 — Read-path Mission + Learning State

### Scope

- Bridge-backed `MissionPort.get_todays_session` → Planning/Mission.  
- Bridge-backed Twin/LearningState reads → Readiness + Lifecycle + TopicProgress.  
- Feature flag: Bridge read on; writes still opaque/no-op for start if not P3.  
- Home shows real mission topic when plan exists; CTA may still be limited until P3.

### Exit criteria

- Home `todays_session.topic_*` matches SQL mission for golden users.  
- No `seeded_demo_mission` / `seeded_demo_twin` when Bridge read flag on.  
- Legacy Dashboard unchanged.

### Rollback

Disable Bridge read flag → prior Experience adapters.

---

## P2 — Recommendation alignment + demote demo seed

### Scope

- `RecommendationBridge` behind AdaptiveDecisionPort.  
- Enforce mission-aligned primary recommendation when mission exists.  
- When Bridge on: composition must not call `seeded_demo_*` for authenticated learners.  
- Keep `SEED_DEMO_LEARNERS` for explicit demo/empty marketing paths only if still required — default off under Bridge Alpha.

### Exit criteria

- AC-2 and AC-3 satisfied in Alpha with Bridge on.  
- Recommendation ≠ fabricated “Continue today's learning session” demo when mission exists.

### Rollback

Disable Recommendation bridge slice; optionally re-enable seed only in non-Alpha.

---

## P3 — Write-path Start / Resume

### Scope

- `MissionLifecycleBridge.start_session` → `StudySessionService.start_session`.  
- Session id mapping MissionId ↔ ExperienceSessionId.  
- Resume validates SQL ownership before SessionWorkspace redirect.  
- Home CTA starts real mission.

### Exit criteria

- AC-1, AC-4, AC-5, AC-6 for start/resume.  
- Starting from Home flips SQL Mission to In Progress.  
- Double-start safe (idempotent).

### Rollback

Disable write bridge; Start returns to opaque-only **or** disable Start CTA (prefer fail closed). Prefer: Bridge read remains; write flag off → Start disabled with message rather than demo write.

---

## P4 — Complete Session + Evidence parity

### Scope

- Complete path calls `StudySessionService` finish/outcome + Evidence Authority.  
- Define outcome payload mapping from Session Activity (may be minimal first: mission complete + duration).  
- Transitional `educational_complete=false` **not** allowed past phase exit.

### Exit criteria

- AC-7, AC-8 for completion.  
- TopicProgress updates match legacy finish for equivalent outcomes.  
- No second mastery writer (orchestrator).

### Rollback

Disable EvidenceParity write; block Complete or route to legacy finish temporarily (product choice). See `ROLLBACK_PLAN.md`.

---

## P5 — Journey / History / Revision read bridges

### Scope

- JourneyBridge, HistoryBridge, Revision options from Lifecycle + AdaptiveLearning weak topics.  
- Revision begin uses same Start bridge as Home.

### Exit criteria

- No page under Experience uses demo seeds with Bridge on.  
- Revision begin == Home start educationally.

### Rollback

Per-port flag off → empty authentic snapshots (not demo).

---

## P6 — Durable store hardening

### Scope

- Enable durable SessionWorkspace / projection cache for multi-worker Alpha/prod.  
- Verify resume across process restart.  
- Projections remain **cache**, SQL remains SoT.

### Exit criteria

- Resume works after worker recycle.  
- No educational drift vs SQL after restart.

### Rollback

Disable durable store flag; accept single-worker Alpha only.

---

## P7 — Internal Alpha Bridge gate

### Scope

- Run Internal Alpha checklist from `TEST_STRATEGY.md`.  
- Scorecard: AC-1…AC-10.  
- Declare **Bridge Complete** when met.  
- **Do not** enable production `SOLE_RUNTIME` solely because Bridge shipped — separate go/no-go.

### Exit criteria

- Bridge Complete definition in parent doc satisfied.  
- Rollback drill executed once.

---

## P8+ — Post-Bridge (out of Bridge Complete)

Not required for Directive 002 acceptance:

1. Sole-runtime production proof with bridged Home.  
2. Retarget calibration/onboarding/welcome to `student.home`.  
3. Legacy mission UI retirement.  
4. Archive or wire `MissionEngine*`.  
5. Optional later ADR: engines become writers after data migration.

---

## Release train rules

| Rule | Detail |
|---|---|
| One phase per deploy preferred | Especially P3 and P4 |
| Soak | ≥ 1 Alpha soak between P3 and P4 |
| Monitoring | `bridge.fallback`, evidence reject rate, start failure rate |
| Dual-run | Keep `SOLE_RUNTIME` off until Bridge Complete + ops go/no-go |

---

## Dependency graph

```
P0 → P1 → P2 → P3 → P4 → P7 → Bridge Complete
         ↘ P5 (after P1; can parallel P3)
P3 → P6 (before multi-worker sole runtime; can parallel P4/P5)
```

---

## Stop condition

Migration plan documented. Implementation occurs in later engineering milestones, not Directive 002.
