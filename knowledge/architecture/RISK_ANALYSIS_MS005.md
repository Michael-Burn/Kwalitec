# MS-005 — Risk Analysis (Learning Strategy & Intervention Engine)

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Migration:** `MIGRATION_PLAN_MS005.md`  
**Related:** MS-001 `RISK_ANALYSIS.md`; MS-003 `RISK_ANALYSIS_MS003.md`; MS-004 `RISK_ANALYSIS_MS004.md`

---

## 1. Risk rating scale

| Level | Meaning |
|---|---|
| **Low** | Contained; flag rollback sufficient |
| **Medium** | Trust or performance impact; needs soak / ADR |
| **High** | Educational integrity or student-trust risk if shipped wrong |
| **Critical** | Could falsely declare Strategy Ready / corrupt educational authority |

---

## 2. Required risk themes

### 2.1 Strategy replaces Runtime A (authority inversion)

| Dimension | Assessment |
|---|---|
| **Description** | Teams treat InterventionPlan as educational SoT; Strategy “plans” overwrite Missions, Progress, or Evidence. |
| **Technical risk** | **Critical** |
| **Educational risk** | **Critical** |
| **Mitigation** | ADR-MS005-001; Strategy read-only; no Planning/mission writes; Runtime A wins fact conflicts; architecture gates |
| **Verification** | Static write guards; integration mutation checks |
| **Rollback** | Disable all Strategy flags |

### 2.2 Strategy re-ranks Adaptive (recommendation seizure)

| Dimension | Assessment |
|---|---|
| **Description** | Strategy silently changes Adaptive primary topic / revision order and presents it as Adaptive consumption. |
| **Technical risk** | High |
| **Educational risk** | **High** — authority polyphony; DP-005 / ADR-005 spirit |
| **Mitigation** | Consume-only Adaptive attachment; preserve alternative order; mission alignment policy; contract tests forbid re-rank |
| **Verification** | Golden: Adaptive primary appears as primary or explicit advisory; never silently replaced |
| **Rollback** | Authority OFF |

### 2.3 Strategy owns Twin / feedback loops

| Dimension | Assessment |
|---|---|
| **Description** | Strategy writes Twin facets or treats Strategy interventions as Twin “truth,” creating self-reinforcing loops. |
| **Technical risk** | High |
| **Educational risk** | **High** |
| **Mitigation** | Twin consume-only; Twin updates only from Runtime A; separate flags |
| **Verification** | Tests: Strategy output does not change Twin snapshot without new Runtime A evidence |
| **Rollback** | Disable Strategy / Twin flags as needed |

### 2.4 Over-orchestration / pedagogical invention

| Dimension | Assessment |
|---|---|
| **Description** | Strategy invents teaching content, mark conversion, or diagnostic certainty beyond director + structure. |
| **Technical risk** | Medium |
| **Educational risk** | **High** (EP-004 product boundary) |
| **Mitigation** | Intervention model forbids content generation; principle registry; materials_note = bring-your-own; honesty principles |
| **Verification** | Contract tests ban content payloads; review copy codes |
| **Rollback** | Authority OFF |

### 2.5 Fatigue / confidence false positives

| Dimension | Assessment |
|---|---|
| **Description** | Fatigue stop-advice or confidence calibration fires on thin Twin signals, blocking useful study or shaming students. |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | Require Runtime A activity refs for fatigue/confidence; severity bands; limitations; prefer supporting over primary when evidence sparse; no pep-talk / shame copy |
| **Verification** | Sparse Twin fixtures → limited interventions + limitations codes |
| **Rollback** | Authority OFF; disable specific builders if flagged |

### 2.6 Mission conflict / dual-next regression

| Dimension | Assessment |
|---|---|
| **Description** | Session intervention primary topic differs from SQL Mission; Start Session contradicts Home director. |
| **Technical risk** | High |
| **Educational risk** | **High** (EP-004 Cluster A trust) |
| **Mitigation** | Mission alignment mandatory; Adaptive differing topic advisory-only; Planning Start unchanged |
| **Verification** | Mission fixtures: topic_code equality under Authority |
| **Rollback** | Authority OFF |

### 2.7 Explainability failures / hidden reasoning

| Dimension | Assessment |
|---|---|
| **Description** | Interventions served without five mandatory explanation questions; Adaptive/Twin lineage omitted. |
| **Technical risk** | Low–Medium |
| **Educational risk** | **High** (DP-005, DP-009) |
| **Mitigation** | Strategy Explainability Gate; fallback over unexplained guidance |
| **Verification** | Gate unit tests; ST/SE acceptance checks |
| **Rollback** | Authority OFF |

### 2.8 Demo / theatrical interventions under Authority

| Dimension | Assessment |
|---|---|
| **Description** | Seeded recovery stories, fake fatigue, or motivational theatre appear when Strategy Authority ON. |
| **Technical risk** | Medium |
| **Educational risk** | **High** (EP-004 epistemic distrust) |
| **Mitigation** | Empty authentic contracts; ban demo markers under Authority; Alpha checklist |
| **Verification** | Contract tests forbid demo markers |
| **Rollback** | Authority OFF |

### 2.9 Stale inputs / continuity contradiction

| Dimension | Assessment |
|---|---|
| **Description** | Strategy uses stale Twin/Adaptive/Runtime A snapshot; Home contradicts Journey/History after completion. |
| **Technical risk** | Medium |
| **Educational risk** | **High** |
| **Mitigation** | `as_of` snapshot discipline; `stale_snapshot` limitations; prefer post-evidence recompute triggers later |
| **Verification** | Complete session → new orchestrate includes new attempt refs or stale flag |
| **Rollback** | Flag off; force re-orchestrate |

### 2.10 Flag / poly-authority complexity

| Dimension | Assessment |
|---|---|
| **Description** | Twin + Adaptive + Strategy Authority combinations produce unpredictable Experience routing. |
| **Technical risk** | High |
| **Educational risk** | Medium–High |
| **Mitigation** | Migration principle: no simultaneous multi-authority flip; documented precedence; soak matrices |
| **Verification** | Composition matrix tests for flag combinations |
| **Rollback** | Disable Strategy Authority first (narrowest), then Adaptive/Twin as needed |

### 2.11 Privacy / governance leakage

| Dimension | Assessment |
|---|---|
| **Description** | Strategy DTOs or telemetry include raw answers, cross-student data, or secrets. |
| **Technical risk** | Medium |
| **Educational risk** | Medium (trust); **High** compliance |
| **Mitigation** | Refs not payloads; student scope; minimal telemetry |
| **Verification** | Contract tests on DTO shape; security review before Authority |
| **Rollback** | Flag off |

### 2.12 Performance / latency stacking

| Dimension | Assessment |
|---|---|
| **Description** | Strategy path stacks Twin assemble + Adaptive decide + Strategy orchestrate on Home load → latency regression. |
| **Technical risk** | Medium |
| **Educational risk** | Low–Medium (abandonment) |
| **Mitigation** | Consume precomputed Twin/Adaptive snapshots when available; shadow latency budgets; fail open to prior path |
| **Verification** | Soak latency metrics; p95 budgets |
| **Rollback** | Authority OFF |

### 2.13 Premature Strategy Ready declaration

| Dimension | Assessment |
|---|---|
| **Description** | Ready declared after docs or partial S0–S2 without soak / gate / fallback proof. |
| **Technical risk** | Medium |
| **Educational risk** | **Critical** programme risk |
| **Mitigation** | Migration Ready checklist; architecture review stop condition; no implementation in this directive |
| **Verification** | Readiness report required before S7 go-live |
| **Rollback** | N/A — do not declare Ready |

---

## 3. Risk by migration phase

| Phase | Top risks | Residual after mitigations |
|---|---|---|
| Docs / review | Premature implementation | Low if stop condition held |
| S0 | Contract drift vs Adaptive/Twin | Low |
| S1 | Estimating unavailable inputs | Medium → Low with provenance rules |
| S2 | Re-ranking Adaptive; content invention | High → Medium with tests |
| S3 | Gate bypass | Medium → Low |
| S4–S6 | False confidence from shadow agreement | Medium |
| S7 | Mission conflict; poly-authority; demo theatre | High → Medium with checklist |

---

## 4. Educational risk summary

| Harm | How Strategy could cause it | Primary control |
|---|---|---|
| False mastery narrative | Confidence/recovery copy overclaims | Honesty principles + Runtime A refs |
| Topic dithering returns | Mission/Adaptive conflict | Mission alignment |
| Study blocked wrongly | Over-aggressive fatigue | Severity bands + evidence refs |
| Distrust of “AI director” | Hidden reasoning / theatre | Explainability Gate + empty authentic |
| Authority confusion | Strategy presented as fact/ranking owner | ADR-MS005-001 + UX authority labels |

---

## 5. Go / No-Go signals (pre-Authority)

| Signal | Go | No-Go |
|---|---|---|
| Determinism | Replay stable on golden fixtures | Non-deterministic decision ids |
| Mission alignment | 100% on mission fixtures | Any contradictory primary topic |
| Adaptive preservation | Primary preserved or explicit advisory | Silent re-rank |
| Gate | Incomplete never served | Bypass observed |
| Fallback | Instant prior path on kill switch | Partial / sticky Authority |
| Twin/Adaptive writes | Zero from Strategy path | Any mutation |
| Latency | Within agreed Home budget | Persistent regression |
| Demo markers | Absent under Authority | Present |

---

## 6. Residual risks after Strategy Ready (expected)

1. Multi-flag operational complexity remains — requires runbooks.  
2. Fatigue/confidence interventions remain judgement-sensitive — keep supporting-first bias when sparse.  
3. Strategy-as-sole-director (replacing Adaptive port UX) remains undecided — ADR-MS005-003.  
4. Trace retention / durable audit store undecided — ADR-MS005-002.  
5. EP-004 secondary demands (deep within-topic coaching) remain out of scope — product boundary.

---

## 7. Acceptance for architecture review

| Criterion | Risk posture |
|---|---|
| Responsibilities distinct | Mitigated by ADR + dependency law |
| Runtime A authoritative | Critical risk mitigated by read-only design |
| Twin interpretive | High loop risk mitigated by consume-only |
| Adaptive recommendation-only | High seizure risk mitigated by no re-rank rule |
| Strategy orchestration-only | Over-orchestration mitigated by intervention model + principles |
| No implementation artefacts | This directive docs-only — **PASS if no code landed** |
