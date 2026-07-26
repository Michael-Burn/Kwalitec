# MS-004 — Digital Twin Traceability

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Related:** MS-002 `JOURNEY_TRACEABILITY_MATRIX.md` (past events); MS-003 `ADAPTIVE_TRACEABILITY.md` (decisions)

---

## 1. Purpose

Link the Twin synthesis chain:

```
Runtime A Evidence  →  Twin Update  →  Profile Facet Claim  →  Experience Projection  →  (optional) Adaptive Input
```

Traceability answers: *which authoritative facts produced which Twin claim, what the student was shown, and whether Adaptive consumed the snapshot* — without Twin writing outcomes or owning Adaptive decisions.

---

## 2. Chain definitions

| Stage | Artefact | Authority |
|---|---|---|
| **Evidence** | StudyAttempts, TopicProgress, Missions, Readiness aggregates, StudyPlan goals, Curriculum position | Runtime A |
| **Twin Update** | `LearnerProfileSnapshot` at `as_of` + `twin_version` | Twin synthesis (derived) |
| **Profile Facet Claim** | A student-visible insight / readiness / summary statement | Twin Authority (flagged) |
| **Experience Projection** | Opaque TwinPort DTO | Projection |
| **Adaptive Input** (optional) | Twin attachment on AdaptiveInputBundle | Adaptive consumes; Twin does not decide |
| **Student Outcome** (downstream) | Later Mission / Attempt / Progress | Runtime A only |

---

## 3. Traceability matrix

| Link | What is recorded | Required fields | Forbidden |
|---|---|---|---|
| Evidence → Twin Update | Input refs that materially shaped the snapshot | `field_provenance`, evidence refs, `runtime_a_snapshot_id` | Invented refs; non-owned evidence |
| Twin Update → Facet Claim | Which facet + claim id + explanation | `claim_id`, facet name, `TwinExplanationBundle` | Claims without evidence/limitations |
| Facet Claim → Experience | What was shown | `claim_id`, port method, `twin_snapshot_ref` | Demo seeds under Authority; unexplained certainty |
| Twin → Adaptive Input | Whether Twin was attached | `twin_snapshot_ref`, Adaptive `decision_id` / input fingerprint | Claiming Twin caused Adaptive decision alone |
| Full chain | Alpha / research audit | Fixture: evidence → snapshot → DTO → optional adaptive attach → later SQL outcome | Fabricating Twin history; Twin writing outcomes |

---

## 4. `TwinTraceRef` contract

Every material Twin projection item carries:

| Field | Meaning |
|---|---|
| `twin_snapshot_ref` | Fingerprint of LearnerProfileSnapshot material serialize |
| `claim_id` | Stable id for the surfaced claim (hash of snapshot_ref + claim kind + topic?) |
| `as_of` | Snapshot clock |
| `twin_version` | Synthesis version |
| `evidence_refs[]` | Authoritative Runtime A refs |
| `what` | Student-safe what-this-claim-is |
| `why` | Pointer into TwinExplanationBundle / reason codes |
| `authority` | `digital_twin_synthesis` |
| `runtime_a_alignment` | `aligned` \| `pass_through` \| `derived` \| `conflict_runtime_a_wins` |

---

## 5. Observational TwinTrace (future implementation shape)

| Field | Source |
|---|---|
| `twin_snapshot_ref` | Assembler fingerprint |
| `correlation_id` | Lifecycle bind (may share with Adaptive when attached) |
| `feature_flag_state` | Twin Engine / Shadow / Authority / Adaptive-input |
| `runtime_a_snapshot_id` | Hash of Runtime A inputs considered |
| `trigger` | Lifecycle trigger enum |
| `gate_result` | Twin explainability gate canonical dict |
| `authority_status` | `shadow_only` \| `twin_authority` \| `gate_ineligible` \| `experience_fallback` \| `failed` |
| `adaptive_attach_status` | `attached` \| `skipped` \| `unavailable` \| `flag_off` |
| `executed_at` | Observational wall-clock (not material) |

### Reconstruction workflow

```
Evidence
    ↓
LearnerProfileSnapshot
    ↓
Facet Claim + Explanation
    ↓
Explainability Gate
    ↓
Experience Projection (or Shadow Only)
    ↓
Optional Adaptive Attachment
```

Reconstruction must be deterministic for a stored TwinTrace.

---

## 6. Conflict and alignment rules

| Situation | Trace requirement |
|---|---|
| Twin pass-through TopicProgress | `runtime_a_alignment=pass_through` |
| Twin structural aggregate (counts) | `derived` + evidence refs for contributing missions/attempts |
| Twin estimate deferred | `limitations` + no student-facing numeric claim |
| Twin estimate would contradict TopicProgress | **Do not surface estimate as fact**; emit `conflict_runtime_a_wins`; Runtime A value shown |

---

## 7. Relationship to Journey / Adaptive traces

| System | Past / Future | Twin role |
|---|---|---|
| Journey / History TraceRef | What happened | Twin must cite same Mission/Attempt ids when referring to sessions |
| Adaptive DecisionTrace | What was advised | Twin attachment appears as input lineage stage — Twin does not create Adaptive decision_id |
| TwinTrace | What the profile claimed | Distinct artefact; may share `correlation_id` when Adaptive attach in same lifecycle |

---

## 8. Telemetry

| Event | When |
|---|---|
| `TWIN_TRACE_CREATED` | TwinTrace recorded |
| `TWIN_TRACE_FAILED` | Trace error |
| `TWIN_TRACE_RECONSTRUCTED` | Lineage rebuilt |

---

## 9. Acceptance (architecture)

| ID | Criterion |
|---|---|
| TT-1 | Evidence → Twin → Claim → Projection chain defined |
| TT-2 | Runtime A conflict rule traced |
| TT-3 | Adaptive consume-only attach traced |
| TT-4 | No Twin write of student outcomes |
