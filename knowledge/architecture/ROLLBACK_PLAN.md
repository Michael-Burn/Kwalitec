# MS-001 — Educational Runtime Bridge Rollback Plan

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`  
**Companion:** `MIGRATION_PLAN.md`

---

## Goals

- Every migration phase can be reversed without schema rollback.  
- Prefer **flag disable** over code revert for operational emergencies.  
- Never roll back into a state that serves `seeded_demo_*` as authority under sole runtime without an explicit product decision.  
- Protect learner data: SQL Mission / TopicProgress writes already committed are **not** deleted on rollback.

---

## Global emergency rollback

### Trigger

- Spike in `bridge.fallback` or start failures  
- Evidence reject storm / mastery corruption suspicion  
- Home topic ≠ mission topic for > threshold of Alpha users  
- Support: “fabricated content” reports under Bridge on

### Actions (ordered)

1. **Disable Bridge write flags** (P3/P4) — stop SQL mutations from Experience.  
2. **Disable Bridge read flags** if projections wrong — Experience may show empty authentic state.  
3. **Ensure `SOLE_RUNTIME` off** if chrome forces Experience and Bridge is unsafe — students return to legacy Dashboard/Missions (Runtime A).  
4. **Do not** re-enable `SEED_DEMO_LEARNERS` in Alpha/prod as a “fix” unless product explicitly accepts demo authority.  
5. Capture diagnostics: adapter health, last `bridge.call` errors, affected `user_id`s.  
6. Communicate Alpha operators: study via legacy Missions until Bridge re-enabled.

### Data handling

| Data | On rollback |
|---|---|
| SQL Mission In Progress / Completed | **Keep** |
| TopicProgress / StudyAttempt | **Keep** (investigate if corrupt) |
| Opaque projection docs | Ignore / expire; SQL is SoT |
| SessionWorkspace | Drop / ignore |

---

## Per-phase rollback

### P0 — Contracts & fixtures

| Item | Action |
|---|---|
| Rollback | Revert docs/tests only |
| Data | None |
| Verification | N/A |

### P1 — Read-path Mission + Learning State

| Item | Action |
|---|---|
| Rollback | Set Bridge read flag **off** |
| Behaviour | Prior Experience adapters (may be demo if seed on) |
| Verification | Home loads; no Bridge telemetry; legacy path unaffected |
| Risk note | If sole runtime on + seed on, demo returns — prefer also unset sole runtime |

### P2 — Recommendation + demote demo

| Item | Action |
|---|---|
| Rollback | Disable Recommendation bridge; optionally restore prior Adaptive adapter |
| Seed | Only re-enable seed in non-production if needed for demos |
| Verification | Adaptive port returns; mission read bridge may stay on |

### P3 — Write-path Start / Resume

| Item | Action |
|---|---|
| Rollback | Disable write bridge flag |
| Prefer | Keep read bridge; **disable Start CTA** or fail closed rather than opaque start |
| Alternate | Full Bridge off + sole runtime off → legacy start |
| Data | Missions already In Progress remain; resume via legacy Missions |
| Verification | No new Experience starts mutate SQL; legacy start works |

### P4 — Complete + Evidence parity

| Item | Action |
|---|---|
| Rollback | Disable EvidenceParity / complete write flag |
| Prefer | Block Experience Complete **or** redirect operators to legacy finish for in-flight missions |
| Data | Do not auto-revert TopicProgress; manual remediation if bad writes detected |
| Verification | No Evidence writes from Experience; legacy finish path healthy |
| Drill | Required once before declaring Bridge Complete |

### P5 — Journey / History / Revision

| Item | Action |
|---|---|
| Rollback | Per-port flags off → empty authentic snapshots |
| Verification | Pages render empty states; no demo seed |

### P6 — Durable store

| Item | Action |
|---|---|
| Rollback | Disable durable store; single-worker Alpha |
| Data | Durable docs retained harmlessly; memory store resumes |
| Verification | App boots; sessions work on one instance |

### P7 — Alpha gate

| Item | Action |
|---|---|
| Rollback | Declare Bridge incomplete; keep flags at last known good phase |
| Verification | Scorecard re-run after fix |

---

## Rollback decision matrix

| Symptom | Immediate action |
|---|---|
| Wrong topic on Home (read) | Disable P1/P2 read or fix adapter; sole runtime off if needed |
| Start creates duplicate / wrong mission | Disable P3 write |
| Complete updates wrong mastery | Disable P4; freeze Alpha study; audit TopicProgress |
| Resume 403 / missing across workers | Disable multi-worker or enable durable (ops); not educational rollback |
| Demo content under Bridge | Confirm seed gated; treat as AC-3 failure — disable Bridge or seed |

---

## Communication template (Alpha)

> Educational Runtime Bridge has been rolled back to phase **Pn**.  
> Please use **legacy Missions** for study until further notice (`SOLE_RUNTIME` unset).  
> Existing progress in your study plan is preserved.

---

## Stop condition

Rollback plan complete. No production changes under Directive 002.
