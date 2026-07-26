# EP-002.9 — Risk Register

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Sources:** Programme brief R1–R10; EP-002.1–8 residual risks; MS-004 readiness critical risks

Likelihood / Impact: Low · Medium · High  
Status: **Mitigated** · **Accepted** · **Open** · **Watch**

---

## 1. Programme-level risks (updated)

| ID | Risk | L | I | Status | Notes |
|---|---|---|---|---|---|
| R1 | Premature HTTP cutover to unproven `build_*` | Low | High | **Mitigated** | Dual-run → gated cutover; production hard-ineligible; defaults OFF |
| R2 | Premature Authority ON in production | Medium | High | **Watch** | Non-prod soak done; production Authority still OFF; T7 not claimed |
| R3 | Operator confusion across Twin stacks | Low | Medium | **Mitigated** | Quarantine note binding |
| R4 | Nested Foundation assemble cost | Low | Medium | **Mitigated** | Shared CLS DI; live Foundation P95 still needed in staging |
| R5 | Insight vs EIP-003 divergence confuses students | Low | Medium | **Mitigated** (Runtime A) | Presentation facade; residual tone difference accepted |
| R6 | MissionOptimizer orphan inconsistency | Low | Medium | **Mitigated** | Quarantined; hard-delete deferred |
| R7 | Collector recursion via readiness intelligence | Low | High | **Mitigated** | Legacy getters retained; architecture tests |
| R8 | Programme ID collision with Analytics EP-002 | Medium | Low | **Accepted** | Full titles / separate directories |
| R9 | Scope creep into Twin facets / Strategy / Adaptive authority | Low | High | **Mitigated** | Non-objectives held across milestones |
| R10 | Treating EP-002 as Twin Ready (T7) | Low | High | **Mitigated** | Explicit non-claim in every milestone + this exit |

---

## 2. Residual operational / product risks

| ID | Risk | L | I | Status | Mitigation / disposition |
|---|---|---|---|---|---|
| RX-01 | Controlled benches mistaken for live staging soak | Medium | High | **Open** | EP-002.9 production readiness requires staging pack before Limited Production |
| RX-02 | Process-local metrics lost on restart | Medium | Medium | **Accepted** (near-term) | Logs as durable channel; durable sink planned |
| RX-03 | Daily Plan display ≠ ORM session topic | Medium | Medium | **Accepted** | Documented `TD-DP-01`; student messaging honesty |
| RX-04 | EI Stage A + Insight dual visibility | Low | Medium | **Accepted** | Mutual exclusion; `TD-CO-02` |
| RX-05 | Experience `/student` narrator divergence under SOLE_RUNTIME | Medium | Medium | **Open** | Out of EP-002; successor guidance |
| RX-06 | Twin latency / nested cost under real collectors | Medium | Medium | **Watch** | Measure Foundation P95 in staging before expanding pilot |
| RX-07 | Heuristic alignment thresholds misread as hard failures | Medium | Low | **Accepted** | Alignment reports; non-blocking where designed |
| RX-08 | Accidental production env mislabel enabling cutover | Low | High | **Mitigated** | Hard-ineligibility + defaults OFF + kill switch |
| RX-09 | Demo-seed theatre if Authority ON without policy | Medium | High | **Watch** | Authority OFF; T7 checklist includes demo-seed eradication |
| RX-10 | Educational effectiveness assumed from architecture | Low | High | **Mitigated** | Explicit non-claim; product measurement programmes |

---

## 3. Critical risk posture

| Class | Open Critical? |
|---|---|
| Observational Twin / Consumer Chain under defaults OFF | **No** |
| Production Twin Authority / Experience cutover | Premature enablement — **mitigated by OFF + review hold** |
| Production HTTP cutover | Premature enablement — **mitigated by OFF + hard-ineligibility** |

---

## 4. Risk acceptance for programme exit

EP-002 exit **accepts**:

- Controlled-bench evidence (not live staging pack) as sufficient for *architecture* completion  
- Process-local health metrics as interim ops posture  
- Display/persistence tension for Daily Plan cutover  
- EI Stage A and Experience narrator residuals as out-of-programme  

EP-002 exit **does not accept**:

- Twin Ready (T7) declaration  
- Production GA without staging evidence and explicit go/no-go  
- Removal of fail-open or production hard gates without successor certification  

---

## 5. Verdict

Overall residual programme risk under production defaults: **Low**.  
Overall residual risk if flags flipped without staging pack: **High**.

**R:** Keep production OFF; run Controlled Pilot only with staging monitoring and documented rollback owner.
