# MS-003 — Adaptive Traceability Matrix

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001 / 007  
**Status:** **A5 Observational Traceability — Implemented**  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Contracts:** `ADAPTIVE_INTERFACE_SPECIFICATION.md`, `ADAPTIVE_EXPLAINABILITY.md`  
**Related:** MS-002 `JOURNEY_TRACEABILITY_MATRIX.md` (past events)  
**Package:** `app/infrastructure/adapters/adaptive_engine/traceability.py`

---

## 1. Purpose

Link the adaptive intelligence chain:

```
Evidence  →  Adaptive Decision  →  Recommendation  →  Student Outcome
```

Traceability answers: *which facts produced which advice, what the student was shown, and what authorised Runtime A outcome followed* — without the Adaptive Engine writing outcomes.

**A5 delivers observational DecisionTrace + lineage reconstruction.** Outcome soak / durable audit store remain optional (ADR-MS003-002).

---

## 2. Chain definitions

| Stage | Artefact | Authority |
|---|---|---|
| **Evidence** | Accepted StudyAttempts, TopicProgress signals, Mission history, Readiness aggregates, Curriculum position, Goals | Runtime A |
| **Adaptive Decision** | `AdaptiveDecisionRecord` / `DecisionTrace.decision_id` | Adaptive Engine (advice only) |
| **Recommendation** | Experience / Recommendation projection DTO shown to student | Projection (Adaptive Engine and/or RecommendationService composition) |
| **Student Outcome** | Subsequent Mission completion, attempts, progress/readiness changes | Runtime A write paths (MS-001) |

---

## 3. Traceability matrix

| Link | What is recorded | Required fields | Forbidden |
|---|---|---|---|
| Evidence → Decision | Input refs that materially influenced the decision | `explanation.evidence_refs`, `topic_refs`, `input_fingerprint`, authority tags | Invented refs; citing non-owned evidence |
| Decision → Recommendation | What was shown vs raw Engine outputs | `decision_id`, `mission_aligned`, primary label, alternatives surfaced | Showing unexplained decisions; contradicting mission primary when mission exists |
| Recommendation → Outcome | Observational linkage after student action | `decision_id` + time window + outcome refs (mission/attempt ids) | Claiming Engine caused mastery; writing outcome from Engine |
| Full chain | End-to-end audit for Alpha / research | Fixture: evidence set → decision → DTO → later SQL outcome | Fabricating recommendation history |

---

## 4. A5 DecisionTrace (implemented)

Every adaptive shadow or cutover execution records a `DecisionTrace` (in-memory + telemetry; no educational tables; no student-facing history).

| Field | Source |
|---|---|
| `decision_id` | `AdaptiveOutputBundle.decision_id` (or minted `a5-…` on failure) |
| `correlation_id` | Bound `CorrelationContext` for the decision lifecycle |
| `engine_version` | Executor / adapter version |
| `feature_flag_state` | Engine / Shadow / Authority snapshot |
| `runtime_a_snapshot_id` | `snap-<sha25616(AdaptiveInputBundle.serialize())>` |
| `input_bundle_ref` / `output_bundle_ref` | Fingerprints of frozen bundles |
| `explainability_gate_result` | Gate canonical dict when gate ran |
| `authority_status` | `shadow_only` / `adaptive_engine` / `gate_ineligible` / `recommendation_fallback` / `failed` |
| `executed_at` | Observational ISO timestamp |

### Correlation rules

1. Explicit `correlation_id` argument wins.  
2. Else reuse current `CorrelationContext`.  
3. Else mint a new id and bind it for the lifecycle.  
4. Related adaptive + trace events for one execution share the same correlation id.

### Reconstruction workflow

```
Evidence
    ↓
AdaptiveInputBundle
    ↓
AdaptiveOutputBundle
    ↓
Explainability Result
    ↓
Routing Decision
    ↓
Recommendation Delivered (or Shadow Only)
```

`TraceabilityService.reconstruct_lineage(decision_id)` is deterministic for a stored trace.

### Telemetry

| Event | When |
|---|---|
| `ADAPTIVE_TRACE_CREATED` | Successful DecisionTrace recorded |
| `ADAPTIVE_TRACE_FAILED` | Trace recorded with error / reconstruction miss |
| `ADAPTIVE_TRACE_RECONSTRUCTED` | Lineage reconstructed from stored DecisionTrace |

---

## 5. Per decision-kind expectations

| Decision kind | Evidence typically required | Recommendation surface | Outcome signals (read) |
|---|---|---|---|
| `NEXT_FOCUS` | TopicProgress + curriculum position (+ optional attempts) | Home primary (mission-aligned) | Mission topic studied; attempt accepted |
| `REVISION_SET` | Weak/due topics + attempts + lifecycle Revision | Revision priorities / alternatives | Revision missions / review attempts |
| `INTENSITY` | Recent attempts volume/outcomes | Advice facet / explanation | Session minutes / completion depth |
| `WORKLOAD` | Goals minutes + recent mission load + readiness backlog | Advice facet | Actual minutes vs suggested |
| `SPACING` | Last-studied + review schedule signals | Revision spacing advice | Time-to-next attempt on topic |
| `COMPOSITE` | Union of above (sparse OK with limitations) | Home composite card | Any of the above |

---

## 6. Outcome linkage policy (no schema mandate)

Without new tables, Outcome linkage may use:

1. **Telemetry join:** `decision_id` on `ADAPTIVE_ENGINE_SUCCESS` / `ADAPTIVE_TRACE_CREATED` + subsequent mission/attempt telemetry within window.  
2. **Recompute window:** Store `input_fingerprint` + `as_of`; reconstruct decision in tests; compare to later Mission dates.  
3. **Optional later audit store (ADR-MS003-002):** Persist AdaptiveDecisionRecord DTOs — **not** educational SoT; append-only advice log.

| State | When |
|---|---|
| `outcome_linked: true` | Mission/attempt after decision within policy window with matching student |
| `outcome_linked: false` | No subsequent study activity |
| `outcome_linked: null` + `unavailable` | Cannot reconstruct without inventing |

**Forbidden:** Fabricating outcomes or back-writing Journey timeline from Adaptive decisions.

---

## 7. Worked example (illustrative)

```
Evidence:
  - topic_progress CM2-core-methods mastery low
  - attempts [a101, a102] incorrect-heavy on same topic
  - readiness backlog high on weak set
  - curriculum next incomplete leaf = CM2-core-methods
  - mission today = CM2-core-methods (exists)

Adaptive Decision (decision_id=d789):
  next_topic = CM2-core-methods
  confidence = medium
  rule_or_model = adaptive.weak_topic_priority@1 + curriculum alignment
  alternatives = [other weak topic X] why_not_selected=mission_alignment

DecisionTrace (A5):
  correlation_id=c456
  runtime_a_snapshot_id=snap-…
  lineage: evidence → input → output → gate → routing → delivered|shadow_only

Recommendation shown:
  primary = mission title (mission_aligned=true)
  explanation includes evidence_refs a101,a102 + topic_progress
  decision_id=d789

Student Outcome (later, Runtime A):
  Mission completed; attempt a103 accepted; TopicProgress updated via Evidence Authority
  Trace link: d789 → mission_id → a103 (observational)
```

---

## 8. Relationship to Journey recommendation deltas

MS-002 TraceRef recommendation fields describe **past** recommendation change around events.  
MS-003 attaches **future** decision identity. When a SessionCompleted occurs after a shown decision:

- Prefer `recommendation.changed` from reconstructable prior/next labels (MS-002 rules).  
- Optionally include `prior_decision_id` when audit/telemetry available.  
- If unknown → `unavailable` — never invent.

---

## 9. Acceptance checks (traceability)

| ID | Check |
|---|---|
| AT-1 | Every UX decision has `decision_id` and non-empty why/evidence/topic/rule/confidence/alternatives groups |
| AT-2 | Evidence refs on decision ⊆ student’s Runtime A artefacts |
| AT-3 | Recommendation primary obeys mission alignment when mission exists |
| AT-4 | Outcome linkage never performed by Engine write; observational only |
| AT-5 | Golden chain fixture documents Evidence → Decision → Recommendation → Outcome for ≥1 learner |
| AT-6 | No cross-student ids in any link |
| AT-A5-1 | Every adaptive execution produces a complete DecisionTrace (A5) |
| AT-A5-2 | Lineage reconstruction is deterministic (A5) |
| AT-A5-3 | Correlation IDs remain consistent across a decision lifecycle (A5) |
