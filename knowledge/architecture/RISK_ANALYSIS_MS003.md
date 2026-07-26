# MS-003 — Risk Analysis (Adaptive Learning Engine)

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Migration:** `MIGRATION_PLAN_MS003.md`  
**Related:** MS-001 `RISK_ANALYSIS.md`; MS-002 `RISK_ANALYSIS_MS002.md`

---

## 1. Risk rating scale

| Level | Meaning |
|---|---|
| **Low** | Contained; flag rollback sufficient |
| **Medium** | Trust or performance impact; needs soak / ADR |
| **High** | Educational integrity or student-trust risk if shipped wrong |
| **Critical** | Could falsely declare Adaptive Engine Ready / corrupt educational authority |

---

## 2. Required risk themes

### 2.1 Feedback loops

| Dimension | Assessment |
|---|---|
| **Description** | Adaptive advice influences what students study → new evidence → next advice. Can amplify early errors or thrash topics. |
| **Technical risk** | Medium — observable via decision_id → outcome telemetry |
| **Educational risk** | **High** — self-reinforcing weak-topic fixation or avoidance |
| **Mitigation** | Curriculum primacy constraints; mission alignment; spacing rules; thrash monitors (same topic flip-flops); human-centred copy (DP-010); never Engine-write mastery |
| **Verification** | Shadow compare; Alpha thrash metrics; fixture sequences |
| **Rollback** | Disable Engine flag |

### 2.2 Over-adaptation

| Dimension | Assessment |
|---|---|
| **Description** | Engine reacts too aggressively to sparse/noisy attempts; nightly plan feels unstable. |
| **Technical risk** | Medium |
| **Educational risk** | **High** — destroys “workflow director” trust (EP-004) |
| **Mitigation** | Confidence bands; minimum evidence thresholds; hysteresis / cooldown on primary topic changes; prefer organisational stability when confidence low |
| **Verification** | Golden sparse-evidence fixtures expect low confidence + stable curriculum-next behaviour |
| **Rollback** | Flag off; or tighten thresholds via config behind flag |

### 2.3 Stale evidence

| Dimension | Assessment |
|---|---|
| **Description** | Snapshot uses outdated progress/readiness; advice contradicts recent session not yet reflected. |
| **Technical risk** | Medium |
| **Educational risk** | **High** (DP-008 Trust) |
| **Mitigation** | `observed_at` on input blocks; freshness windows; lower confidence when stale; prefer mission/today’s session as alignment anchor; avoid caching decisions across completion without invalidation |
| **Verification** | Tests: complete session then decide ⇒ snapshot includes new attempt or explicit stale limitation |
| **Rollback** | Disable cache; flag off |

### 2.4 Explainability failures

| Dimension | Assessment |
|---|---|
| **Description** | Guidance shown without six-question bundle; or narrative invents causation. |
| **Technical risk** | Low–Medium |
| **Educational risk** | **High** — EP-004 epistemic distrust |
| **Mitigation** | `EXPLAINABILITY_INCOMPLETE` blocks UX; fallback to Recommendation Bridge; structured refs only; limitations mandatory when sparse |
| **Verification** | E-1…E-6; contract tests |
| **Rollback** | Engine UX flag off |

### 2.5 Educational bias

| Dimension | Assessment |
|---|---|
| **Description** | Systematic favouring of certain topics, stages, or attempt patterns that disadvantage cohorts (e.g. late starters, revision-only, V1 vs V2 syllabus shapes). |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | Curriculum spine as candidate universe (DP-011); no private taxonomy; V1/V2 fixtures; avoid engagement heuristics as mastery proxies; document known limitations; monitor primary-topic distribution in Alpha |
| **Verification** | Cross-syllabus golden fixtures; bias review checklist before Ready |
| **Rollback** | Flag off; rule version pin |

### 2.6 Performance

| Dimension | Assessment |
|---|---|
| **Description** | Assembling history + scoring on Home load increases latency / DB load. |
| **Technical risk** | **Medium–High** |
| **Educational risk** | Low directly; Medium if timeouts cause empty/wrong fallback churn |
| **Mitigation** | Hard caps on attempts/missions; parallel reads; shadow async; latency telemetry budgets; fallback on timeout |
| **Verification** | Load tests on History-sized users; Home p95 budget |
| **Rollback** | Flag off; reduce caps |

---

## 3. Phase risks

### A0 — Contracts / ADRs

| Dimension | Assessment |
|---|---|
| Technical | Low |
| Educational | Low |
| Rollback | N/A |

### A1 — Input assembler

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — query shapes, V1/V2 traversal |
| **Educational risk** | High if assembler invents readiness/progress |
| **Mitigation** | Pass-through ReadinessService; forbid local formulas |
| **Rollback** | Unused / flag off |

### A2 — Shadow engine

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — dual compute cost |
| **Educational risk** | Low (no UX) unless shadow path accidentally wired |
| **Mitigation** | Hard separation; tests that UX DTO unchanged |
| **Rollback** | Shadow flag off |

### A3 — Explainability gate

| Dimension | Assessment |
|---|---|
| **Technical risk** | Low |
| **Educational risk** | Medium if gate bypassed |
| **Mitigation** | Single projection chokepoint |
| **Rollback** | Keep Engine off |

### A4 — Port cutover

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — composition wiring |
| **Educational risk** | **High** — contradiction with mission / RecommendationService |
| **Mitigation** | Mission alignment invariant; fallback; no algorithm rewrite |
| **Rollback** | `ENABLE_ADAPTIVE_ENGINE` off |

### A5 — Outcome linkage

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium |
| **Educational risk** | High if linkage fabricates causation |
| **Mitigation** | Observational only; `unavailable` policy |
| **Rollback** | Disable linkage |

### A6 — Soak

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium → **Mitigated for observational soak** (Directive 008) |
| **Educational risk** | Medium — silent drift (monitors emit telemetry; no auto-correction) |
| **Mitigation** | `ShadowSoakOrchestrator` + comparison / determinism / drift monitors; explainability + trace rates; rollback verifier |
| **Rollback** | Flags off (`KWALITEC_ADAPTIVE_ENGINE` / `KWALITEC_ADAPTIVE_AUTHORITY`) — verified automated |

### A7 — Ready gate

| Dimension | Assessment |
|---|---|
| **Technical risk** | Medium — false confidence |
| **Educational risk** | **Critical** if Ready declared with AE gaps then Planning/sole-runtime follow-on |
| **Mitigation** | Explicit Ready definition; separate Planning ADR; block sole-runtime coupling |
| **Rollback** | Hold Ready; disable Engine |

---

## 4. Cross-cutting risks

| Risk | Severity | Mitigation |
|---|---|---|
| Engine accidentally calls AdaptiveLearning **write** APIs | **Critical** | Architecture tests forbidding write imports; code review gate |
| Treating AdaptiveDecisionRecord as TopicProgress SoT | **Critical** | Authority tags; DP-004; documentation |
| Changing RecommendationService algorithms “while here” | High | Explicit non-goal; PR scope checks |
| Re-enabling `seeded_demo_adaptive` under Engine flag | High | Alpha checklist; composition audit |
| LLM / opaque generative core in decision centre | High | DP-012; registry allows deterministic ids only |
| Privacy: over-retention of decision logs | Medium | ADR-MS003-002 retention; no secrets in telemetry |

---

## 5. Residual risks after Adaptive Engine Ready

| Residual | Notes |
|---|---|
| Feedback loops remain inherent to adaptive products | Monitored, not eliminated |
| Sparse new learners always low-confidence | Honest emptiness preferred |
| Without durable decision audit store, long-horizon “why was I shown X last month?” limited | ADR-MS003-002 optional follow-up |
| Planning still independent of Engine | Intentional; dual-next policy remains |

---

## 6. Go / no-go inputs for Ready

Declare **Adaptive Engine Ready** only if:

1. AE-1…AE-10 green.  
2. No open Critical risks.  
3. Feedback-loop / over-adaptation / explainability monitors in place.  
4. Rollback drill succeeded.  
5. Product accepts residual risks in §5.

Do **not** couple Ready to sole-runtime or Planning algorithm changes.
