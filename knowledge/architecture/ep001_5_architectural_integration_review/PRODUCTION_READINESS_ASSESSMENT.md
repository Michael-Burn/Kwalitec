# EP-001.5 — Production Readiness Assessment

**Milestone:** EP-001.5  
**Date:** 2026-07-26

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Rollout readiness

| Criterion | Status | Evidence |
|---|---|---|
| Default-safe (no UX change) | **Pass** | Twin flags default OFF |
| Additive DI when Twin ON | **Pass** | Composition builds Twin stack only if flag ON |
| Unit coverage for EP-001 packages | **Pass** | 32 unit tests passed (foundation + planner + readiness + insight) |
| HTTP cutover | **Not ready** | Routes still call legacy APIs |
| Experience Authority cutover | **Not ready (optional)** | Authority default OFF; fallback exists |
| MS-004 Twin Ready (T7) declaration | **Not claimed** | EP-001.1 explicitly deferred |

**C:** EP-001 is **ready to enable in shadow / API-only mode**, not ready as sole UX authority.

---

## 2. Rollback readiness

| Criterion | Status | Evidence |
|---|---|---|
| Instant flag OFF removes Twin DI | **Pass** | Composition + service fail-open |
| Experience TwinPort preserved on Twin OFF | **Pass** | `TwinRollbackVerifier` expectations |
| Adaptive flags independent of Twin | **Pass** | Rollback verifier asserts independence |
| No schema migration to reverse | **Pass** | No Alembic across EP-001.1–4 |
| Authority OFF restores ExperienceTwinAdapter | **Pass** | Composition routing |

**C:** Rollback posture is **strong** for flag-based deployment.

---

## 3. Backwards compatibility

| Criterion | Status | Evidence |
|---|---|---|
| Legacy mission generation unchanged when Twin OFF | **Pass** | `generate_today_mission` |
| Legacy readiness getters unchanged | **Pass** | Explicit EP-001.3 invariant |
| Legacy recommendations unchanged | **Pass** | `generate_recommendations` untouched as formula |
| V1/V2 curriculum traversal | **Pass** | Completion reports; no curriculum edits |
| Collector recursion safety | **Pass** | Intelligence path does not wrap getters |

**C:** Backwards compatibility is a **first-class design property** of EP-001.

---

## 4. Observability

| Capability | Status | Evidence |
|---|---|---|
| Twin Shadow validator + monitors | **Present** | `shadow.py`, `shadow_monitors.py`, `shadow_health.py` |
| Twin rollback telemetry | **Present** | `shadow_telemetry.py`, `shadow_rollback.py` |
| Production metrics on EP-001.2–4 `build_*` | **Weak** | No HTTP callers; limited live signal |
| Provenance on CanonicalLearnerState | **Present** | Foundation blocks carry evidence_refs / availability |
| Limitation codes on partial insights | **Present** | Insight contracts |

**C:** MS-004 Twin observability is solid; **EP-001 consumer-chain live observability is thin** until surfaces call `build_*`.

**R:** Add structured logging / shadow counters for `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` before UX cutover.

---

## 5. Operational risk

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Premature Authority ON exposes Foundation bugs in Experience UX | Medium | High | Keep Authority OFF; soak first |
| Premature HTTP cutover without Twin ON | Low | High | Cutover must require Twin ON |
| Nested assemble cost under load | Medium | Medium | Share Foundation instance; cache as_of snapshot |
| Operator confusion from multi-Twin docs | Medium | Medium | Quarantine narrative (TD-ARCH-01) |
| Demo-seed theatre vs Runtime A honesty | Medium if Authority ON with fallback failure | High | Authority fallback + disallow demo when Authority ON |

**C:** Operational risk is **low under current defaults**, **elevated if flags flipped without soak**.

---

## 6. Overall production readiness verdict

| Mode | Ready? |
|---|---|
| Ship code with Twin OFF (current) | **Yes** |
| Enable Twin ON for shadow / Adaptive TwinInput / API availability | **Conditionally yes** (with monitoring) |
| Enable Twin Authority for Experience | **Not yet** without soak |
| Replace dashboard legacy APIs with EP-001 `build_*` | **Not yet** |
| Declare EP-001 product-complete for students | **No** |

**R:** Treat EP-001 as an **architecturally ready foundation** and a **flag-gated pre-cutover stack**, not as a finished student-facing delivery.
