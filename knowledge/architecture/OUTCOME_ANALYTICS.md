# MS-006 — Outcome Analytics

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Companions:** `EVIDENCE_MODEL.md`, `EXPERIMENT_FRAMEWORK.md`, `POLICY_EVALUATION.md`  
**Related:** EP-004 SP4 / SP8; `EVIDENCE_BACKLOG.md` success metrics (educational, not UI)

---

## 1. Purpose

Define **analytics responsibilities** for observational educational outcomes: what is measured, who consumes it, how metrics are typed by claim boundary, and which anti-patterns are forbidden.

Analytics here are **governance- and research-facing**, not student coaching surfaces.

---

## 2. Responsibility split

| Actor | Owns | Does not own |
|---|---|---|
| **Runtime A** | Authoritative event facts | Aggregate narrative dashboards |
| **Evidence Platform analytics** | Outcome definitions, aggregates, exports, claim-boundary enforcement | Educational writes; student Home widgets as authority |
| **Upstream engines** | Their own shadow health telemetry | Cross-layer outcome causation claims |
| **Product / research** | Interpreting analytics under governance | Upgrading metrics into exam-mark promises |
| **Experience** | Presentation of educational serving | Authoring outcome definitions |

---

## 3. Metric families

### 3.1 Organisation metrics (`claim_boundary = organisation`)

| Family | Examples (logical) | Notes |
|---|---|---|
| Start / continue | Single-path start rate, resume success | EP-004 Cluster A sensitivity |
| Session loop | Same-night completion, abandon rate | Director loop health |
| Recovery | Post-abandon resume within window | Must not imply mastery recovery |
| Routing reliability | Authority path consistency, fallback rate | Ops + trust |

### 3.2 Learning-signal metrics (`learning_signal`)

| Family | Examples | Notes |
|---|---|---|
| Honesty ritual | Practice outcome logged rate | Valued in EP-004; not depth proof |
| Attempt logging | Attempts per session, incomplete close rate | Behavioural signal |
| Explanation completeness | Gate pass rates (ops) | Inspectability infrastructure |

### 3.3 Learning-depth metrics (`learning_depth`)

| Family | Examples | Notes |
|---|---|---|
| Pre-registered constructs | Within-topic attempt pattern change under protocol | High bar; limitations mandatory |
| Twin-linked observational | Only as supporting, never sole | Twin is interpretation |

**Default:** Prefer organisation + learning-signal as primaries until depth programme is governed.

### 3.4 Transfer metrics (`transfer`)

| Family | Status |
|---|---|
| Exam marks / pass rates | **Deferred** — registry may mark `not_in_programme` |
| Technique under timed conditions | Out of current product evidence scope |

### 3.5 Trust / ops metrics (`trust_inspectability` or ops)

| Family | Examples | Notes |
|---|---|---|
| Overclaim incidents | Empty evidence + strong language (if instrumented) | Qualitative linkage careful |
| Gate failures | Explainability incomplete rates | Adaptive / Strategy / Evidence gates |
| Shadow stability | Determinism / drift monitors | Per-engine + cross-layer |
| Latency | p95 Home stack with flags | Guardrail |

---

## 4. Analytics artefacts

### 4.1 `MetricSeries`

| Field | Meaning |
|---|---|
| `metric_id` | Maps to outcome definition or derived |
| `claim_boundary` | Required |
| `grain` | night / student / cohort / system |
| `points[]` | `{ t, value, n, uncertainty? }` |
| `filters` | Exam, flags, arm, eligibility |
| `limitations[]` | |

### 4.2 `ScorecardSlice`

Governance-facing slice (e.g. weekly ops), not student UI.

| Field | Meaning |
|---|---|
| `slice_id` | |
| `period` | |
| `organisation_block` | Metrics + deltas |
| `learning_signal_block` | Separate block |
| `learning_depth_block` | Optional; default empty / deferred |
| `guardrails_block` | |
| `narrative_constraints` | Forbidden phrases / required caveats |

### 4.3 `AnalyticsExport`

| Field | Meaning |
|---|---|
| `export_id` | |
| `audience` | `governance` \| `research` \| `engineering_ops` |
| `contents_ref` | Fingerprint of included series / evaluations |
| `redaction_level` | |
| `created_at` | |

**Forbidden audience:** `student_coaching` as Evidence Platform analytics product in this milestone.

---

## 5. Aggregation rules

| Rule | Binding |
|---|---|
| Student scope | Aggregates never leak other students’ identifiers |
| Flag dimensions | Always dimension by relevant Authority / Shadow flags when interpreting serve metrics |
| Exposure | Arm metrics require exposure verification |
| Empty authentic | Prefer showing empty / low N over imputed “healthy” composites |
| Determinism | Same freeze → same series serialize |

---

## 6. Anti-patterns (forbidden)

| Anti-pattern | Why |
|---|---|
| **Mastery theatre** | Composite readiness from thin logs presented as learning proof |
| **SP8 collapse** | Session completion labelled “learning improved” |
| **Causation invention** | Delivery→outcome `ambiguous` upgraded to causal win |
| **Authority laundering** | Analytics PASS used to flip Adaptive/Strategy Authority |
| **Coach feed** | Pushing evaluation confidence into student Coach copy |
| **Cross-engine blame** | Attributing Runtime A gaps to Twin/Adaptive without refs |
| **Demo inflation** | Seeded learners in promote-grade scorecards |
| **Exam promise** | Transfer metrics as product claims without programme |

---

## 7. Consumers & use cases

| Consumer | Legitimate use |
|---|---|
| Architecture / programme governance | Keep / revise / roll back policies |
| Engineering ops | Shadow soak health, latency, gate rates |
| Product strategy | Map metrics to EP-004 themes without upgrading confidence |
| Blind-review / research follow-ups | Link `RESEARCH_EVENT` ids carefully |
| Adaptive / Strategy owners | Observe outcomes of their policies — consume reports, don’t take write orders from analytics |

---

## 8. Feature flags (analytics, design)

| Flag | Role | Default |
|---|---|---|
| `ENABLE_OUTCOME_ANALYTICS` | Allow aggregate export / scorecard assembly | OFF |
| `ENABLE_EVIDENCE_SHADOW` | Required practical prerequisite for meaningful series | OFF |
| `ENABLE_EVIDENCE_PLATFORM` | Master | OFF |

Analytics OFF must not affect educational serving.

---

## 9. Relationship to existing product artefacts

| Existing | Relationship |
|---|---|
| EP-004 weekly scorecard / feedback register | Qualitative / programme; may later **link** metric ids — not replaced |
| Evidence Backlog success metrics | Educational acceptance language; analytics may operationalise **some** as registered outcomes after governance |
| Engine shadow telemetry | Inputs / dimensions; not substitutes for Runtime A outcomes |

---

## 10. Non-goals

- Student-facing analytics dashboards as SoT  
- Real-time personalisation from aggregates  
- Replacing curriculum / Planning authority with cohort trends  
- Implementing BI pipelines in this directive  

---

## 11. Acceptance hooks

Architecture PASS requires analytics responsibilities to:

- Remain observational  
- Enforce claim boundaries  
- Separate organisation from learning-depth reporting  
- Avoid becoming educational authority
