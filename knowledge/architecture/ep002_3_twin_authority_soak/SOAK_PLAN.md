# EP-002.3 — Soak Plan

**Milestone:** EP-002.3 — Twin & Authority Non-Production Soak  
**Environment:** Non-production only (`APP_ENV` ≠ production; pytest / local / staging)  
**Production flags:** Remain Twin OFF / Authority OFF

---

## 1. Objectives

1. Twin-enabled non-prod runs of all three `build_*` APIs.  
2. Authority-enabled non-prod Experience TwinPort routing validation.  
3. Capture operational evidence via EP-002.1–2 telemetry.  
4. Validate rollback to pre-soak state.  
5. Confirm readiness for EP-002.4 HTTP dual-run planning — **not** cutover.

---

## 2. Flag matrix (cells to execute)

| Cell | Twin | Authority | Expected routing / behaviour |
|---|---|---|---|
| A | OFF | OFF | `build_*` → `None` / unavailable; TwinPort = ExperienceTwinAdapter |
| B | OFF | ON (env) | Authority **resolved OFF** (requires Twin); same as A |
| C | ON | OFF | `build_*` exercise Foundation path; TwinPort = ExperienceTwinAdapter |
| D | ON | ON | `build_*` + TwinPort = Foundation Authority (fail-open to ExperienceTwinAdapter) |
| E | Rollback | Twin OFF then Authority OFF | Composition matches pre-soak (cell A) |

---

## 3. Workload profile

| Dimension | Plan |
|---|---|
| APIs | `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` |
| Mode | Controlled soak orchestrator with injectable Foundations / stubs for unit; composition factory for Authority matrix |
| Iterations | ≥ 30 insight compositions (or equivalent nested chain) + ≥ 30 planner / readiness samples under Twin ON |
| Nested compose | Prefer Insight with planner + readiness ON to exercise EP-002.2 share-hit |
| Authority | Composition builds for cells A–D; smoke `get_learner_summary` under D with fail-open case |

Realistic non-prod means: same call paths as production services would use when Twin is ON, without HTTP route changes.

---

## 4. Metrics to capture

| Metric | Source |
|---|---|
| Request count / outcome histogram | `ConsumerChainTelemetry` completed / failed |
| Latency avg / p95 | Completed `duration_ms` |
| Foundation assemble count | `foundation_assemble` where `assembled=True` |
| Share-hit rate | Injected / (assembled + injected) |
| Limitation-code frequency | Completed `limitation_codes` |
| Exception rate | Failed observations / total |
| Twin / Authority flag state | Snapshot fields on each emit |
| TwinPort adapter id | Composition `twin` type / ADAPTER_ID |
| Rollback success | Soak rollback verifier |
| Ownership violations | Static checks: no Runtime A writes from soak modules |

---

## 5. Execution sequence

```
1. Baseline (cell A) — Twin OFF, Authority OFF
2. Twin soak (cell C) — Twin ON, Authority OFF; exercise build_*
3. Authority soak (cell D) — Twin ON, Authority ON; verify TwinPort + fail-open
4. Invalid Authority env (cell B) — confirm flag AND behaviour
5. Rollback drill (cell E) — Twin OFF → Authority OFF; verify pre-soak
6. Aggregate health snapshot + write completion metrics
```

---

## 6. Observability

- Reuse `ConsumerChainTelemetry` (no second framework).  
- Emit soak-level events: requested / completed / failed / health / rollback / matrix cell.  
- All events mark `influences_student=False`.

---

## 7. Stop conditions

| Condition | Action |
|---|---|
| Ownership violation detected | Fail soak; do not recommend EP-002.4 |
| Rollback verifier `ok=False` | Fail soak |
| Unexpected exception rate above threshold in harness | Triage; document in Risks |
| Production defaults flipped | Immediate remediation — out of scope to enable |

---

## 8. Deliverables from execution

- Soak execution evidence (tests + health snapshot)  
- Performance / Foundation metrics  
- Authority matrix results  
- Rollback validation  
- Feature flag matrix confirmation  
- Recommendation for EP-002.4
