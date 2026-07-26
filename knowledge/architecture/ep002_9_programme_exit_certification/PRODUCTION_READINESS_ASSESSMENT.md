# EP-002.9 — Production Readiness Assessment

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26

Legend: **O** · **E** · **C** · **R**

---

## 1. Recommendation (mandatory)

# Ready for Controlled Pilot

**Not** Ready for Limited Production.  
**Not** Ready for General Availability.  
**Not** “Not Ready” for architecture / non-production gated activation.

---

## 2. Assessment dimensions

### 2.1 Staging evidence

| Criterion | Status | Evidence |
|---|---|---|
| Controlled non-prod soak (Twin + Authority) | **Pass (harness)** | EP-002.3: 450 requests; 0 exceptions; rollback ok |
| Controlled cutover benches (Insights / Readiness / Daily Plan) | **Pass (harness)** | EP-002.5–7: ~50 attempts each; fallbacks exercised; 0 ownership violations |
| Presentation regression suite | **Pass** | EP-002.8: 22 presentation + 66 cutover tests |
| Archived live staging soak with real learner traffic for EP-002.5–8 | **Missing** | Explicitly deferred across EP-002.5–8; assigned to exit — **not supplied as live pack** |

**C:** Architecture and harness evidence are strong; **live staging evidence pack is incomplete**. That blocks Limited Production / GA, not Controlled Pilot.

### 2.2 Rollback

| Criterion | Status | Evidence |
|---|---|---|
| Per-surface cutover OFF restores legacy | **Pass** | Rollback plans EP-002.5–8 |
| Twin OFF global kill switch | **Pass** | `KWALITEC_DIGITAL_TWIN=0` |
| Authority OFF restores ExperienceTwinAdapter | **Pass** | EP-002.3 rollback verifier |
| No schema / data reverse migration required | **Pass** | Migration impact None across EP-002 |
| Production hard-ineligibility of HTTP cutovers | **Pass** | `_PRODUCTION_ENVS` in cutover modules |

**C:** Rollback posture is **strong**.

### 2.3 Latency

| Criterion | Status | Evidence |
|---|---|---|
| Shared CLS DI reduces nested assemble | **Pass (design)** | EP-002.2 |
| Bench latencies as production SLOs | **Fail / N/A** | Milestones explicitly forbid treating stub latencies as SLOs |
| Live Foundation P95 in target environment | **Missing** | Required before Limited Production |

**C:** Latency is **conditionally acceptable for Controlled Pilot** with monitoring; **not certified for production SLO commitments**.

### 2.4 Fail-open

| Criterion | Status | Evidence |
|---|---|---|
| Twin OFF → `build_*` None / legacy authority | **Pass** | Service contracts + tests |
| Twin exceptions / limitations → legacy cutover fallback | **Pass** | Cutover eligibility + fallback reasons |
| Defaults OFF in production | **Pass** | `v2_flags.py` |
| Presentation facade delegates legacy to EIP-003 | **Pass** | EP-002.8 |

**C:** Fail-open is **certified**.

### 2.5 Observability

| Criterion | Status | Evidence |
|---|---|---|
| `build_*` invocation / outcome / limitation / latency telemetry | **Pass** | EP-002.1 |
| Dual-run comparison logs (non-prod) | **Pass** | EP-002.4 (+ readiness / daily-plan dual-run) |
| Cutover served / fallback counters | **Pass (process-local)** | EP-002.5–7 health modules |
| Durable ops dashboard / long-retention metrics | **Weak** | Process-local health; logs are durable channel |

**C:** Observability is **sufficient for Controlled Pilot**, **weak for GA**.

### 2.6 Operational monitoring

| Criterion | Status | Evidence |
|---|---|---|
| Twin shadow health / rollback tooling | **Present** | MS-004 T6 |
| Consumer-chain soak health aggregator | **Present** | EP-002.3 |
| Named on-call runbook for EP-002 cutover incidents | **Partial** | Rollback plans exist; no dedicated production runbook pack in this milestone |
| Alerting thresholds on Foundation P95 / fallback rate | **Missing** | Successor ops |

**C:** Monitoring tooling exists; production alerting discipline is incomplete.

### 2.7 Feature flag governance

| Criterion | Status | Evidence |
|---|---|---|
| Safe defaults | **Pass** | All related flags OFF |
| Twin AND-gate on cutovers | **Pass** | `v2_flags.py` |
| Production hard gate | **Pass** | Cutover modules |
| Documented in `.env.example` | **Pass** | Flag comments present |
| Retirement path defined | **Directional** | Feature Flag Audit §5 |

**C:** Flag governance is **certified for Controlled Pilot**.

---

## 3. Mode readiness matrix

| Mode | Ready? |
|---|---|
| Ship code with all Twin / Cutover flags OFF | **Yes** |
| Non-prod Twin ON for observation / dual-run | **Yes** |
| Non-prod gated HTTP cutover (Controlled Pilot) | **Yes**, with monitoring owner + rollback drill |
| Production Authority ON | **No** |
| Production HTTP cutover (Limited Production) | **No** — missing live staging pack + P95 + alerting |
| General Availability | **No** |
| Twin Ready (T7) | **No** — see Twin Readiness Assessment |

---

## 4. Evidence summary supporting the recommendation

**Why Controlled Pilot (not Not Ready):**

- Constitutional ownership certified  
- Sequenced dual-run → cutover implemented  
- Fail-open + production hard-ineligibility  
- Rollback drills and harness soaks green  
- Presentation consolidated for Runtime A  

**Why not Limited Production / GA:**

- No archived live staging soak pack for EP-002.5–8 real traffic  
- No certified live Foundation P95 / production SLOs  
- Process-local metrics / incomplete production alerting  
- Daily Plan display/persistence tension unresolved for broad exposure  
- Explicit programme non-claim of public launch readiness  

---

## 5. Controlled Pilot entry checklist

Before enabling any cutover flag in a shared staging / pilot environment:

- [ ] Twin ON only in non-production `APP_ENV`  
- [ ] One surface at a time (prefer Insights → Readiness → Daily Plan)  
- [ ] Rollback owner named; Twin kill switch rehearsed  
- [ ] Capture fallback rate, limitation codes, Foundation latency samples  
- [ ] Confirm collectors still call pure legacy readiness getters  
- [ ] Confirm MissionOptimizer remains unwired  
- [ ] Do not enable production cutover eligibility in code without a new certification  

---

## 6. Overall verdict

**O:** EP-002 delivered a safe, flag-gated student intelligence surface architecture.  
**E:** Sections 2–4.  
**C:** **Ready for Controlled Pilot.**  
**R:** Keep production Twin / Authority / Cutover OFF until a successor production go/no-go closes `TD-OPS-STAGING` and latency/alerting gaps.
