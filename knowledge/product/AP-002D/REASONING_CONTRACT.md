# AP-002D — Reasoning Contract

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`INTEGRATION_SPECIFICATION.md`](INTEGRATION_SPECIFICATION.md), [`EVIDENCE_BOUNDARY.md`](EVIDENCE_BOUNDARY.md), `StudentReasoningService`

---

## 1. Purpose

Specify exactly what `StudentReasoningService` receives from assessment evidence ingress, what it returns, how errors behave, and how versions interact.

This contract freezes the **integration surface**. Rule internals may evolve; the authority and I/O shape must not silently change.

---

## 2. Who calls Reasoning

| Caller | Allowed? | Role |
|---|---|---|
| Assessment Pipeline (AP-001) after observation append | **Yes** (primary for assessment) | Orchestrates ingress → reason |
| Founder / manual Twin paths | Yes (existing) | Diagnostic / ops |
| Assessment Engine delivery / packaging services | **No** | Producers only |
| Mission Engine | **No** (may trigger pipeline refresh indirectly) | Consumer of decisions |
| Tutor | **No** | Explains only |

---

## 3. What StudentReasoningService receives

### 3.1 Required inputs

| Input | Type / source | Meaning |
|---|---|---|
| `twin` | `StudentDigitalTwin` aggregate | Prior belief + append-only observations including new assessment facts |
| `triggered_by` | `str` | Provenance of the run; assessment path uses `assessment_pipeline:<event_type>` |
| `observation_ids` | `tuple[str, …]` | Ids included in this reasoning cycle (defaults to all Twin observations if omitted — assessment path **should** pass the relevant set explicitly when practical) |
| `persist` | `bool` | Whether inferences and Graph projections are persisted |

### 3.2 Assessment evidence available to Reasoning (via Twin observations)

Reasoning does **not** receive an `EvidenceBundle` object as a Twin write. It receives **observations** whose metadata lawfully carries assessment evidence dimensions exported across the boundary.

| Field family | Source | Notes |
|---|---|---|
| Observation kind | Mapped from Engine / AP-001 | Prefer existing `ObservationKind` values |
| `curriculum_entity_id` / `kind` | Opaque syllabus refs | Resolved only via Curriculum Retrieval |
| `evidence_reference` | Bundle / result / event id | Audit pointer |
| `provenance` | Engine session + pipeline | Must include Engine session id where available |
| Metadata: correctness / partial | Evidence dimensions | Facts, not mastery |
| Metadata: confidence | Self-report | Soft alone |
| Metadata: response_time_ms | Timing | Soft alone |
| Metadata: hints_used / retries | Scaffolding | Affects strength interpretation |
| Metadata: misconception_tags | Tagged errors | Gap specificity input |
| Metadata: evidence_strength | Bundle band | Quality gate for high-mastery language — **not** mastery |
| Metadata: packaging_version | `PACKAGING_VERSION` | Contract version for rules |
| Metadata: instrument / intent | Session context | diagnostic / checkpoint / … |

### 3.3 Explicitly not received as authority

| Not an input authority | Why |
|---|---|
| Precomputed mastery percentages from Assessment | Would bypass Reasoning |
| Tutor prose | Not evidence |
| Mission priority overrides | Scheduling ≠ belief |
| Graph “mastery rows” as SoT | Graph projects; Twin owns |
| LLM free-text judgments in core path | Forbidden by invariants |

### 3.4 Curriculum evidence

During the run, Reasoning obtains curriculum excerpts **only** through Curriculum Retrieval (approved profiles). Assessment must not inject ad-hoc syllabus scrapes.

---

## 4. What StudentReasoningService returns

Operationally, `reason(...)` returns the **updated Twin** after applying the engine result. Educationally, the authoritative inference payload is `ReasoningResult`:

| Output | Meaning |
|---|---|
| `run_id` | Stable id for this reasoning cycle |
| `twin_id` / `triggered_by` / `observation_ids` | Trace linkage |
| `mastery` | Updated mastery map (inference) |
| `confidence` | Confidence state (inference) |
| `learning_state` | Learning-state snapshot (inference) |
| `gaps` | Knowledge gaps (inference) |
| `recommendations` | Actionable educational recommendations (decisions) |
| `decisions` | Educational decisions produced by rules |
| `explanations` | Deterministic explanation artefacts |
| `executions` | Rule execution audit |
| `curriculum_evidence` | Retrieval bundle used |
| `summary` | Human-readable run summary |
| `engine_version` | Reasoning engine version |
| `created_at` | Run timestamp |

Side effects when `persist=True` (existing lawful behaviour):

1. Twin inference fields replaced via persistence.
2. Reasoning history / timeline updated.
3. Learning Graph projections refreshed from Twin.

Assessment packaging does not receive these outputs as a write-back channel.

---

## 5. Error behaviour

| Condition | Expected behaviour |
|---|---|
| Twin missing | Fail before reasoning (pipeline / Twin service error); do not invent a Twin |
| Invalid / rejected evidence at packaging | Bundle not exported; no observation append for invalid package (see [`ERROR_HANDLING.md`](ERROR_HANDLING.md)) |
| Duplicate evidence / duplicate observation id | Idempotent skip or reject at ingress; do not double-infer the same fact |
| Partial bundle (some items invalid) | Prefer fail-closed for the package **or** export only validated subset with explicit partial flag — implementation must choose one and test it; default recommendation: **fail-closed at packaging**, optional later “partial export” behind explicit contract |
| Unknown concept / missing LO | Observation may still append with opaque/empty refs; Reasoning must not fabricate curriculum claims — gaps/recommendations remain honest / deferred |
| Reasoning rule failure | Preserve prior Twin inferences; record failed run / error path; do not apply partial corrupt mastery |
| Persistence failure after compute | Transactional rollback expectations: no half-applied inference + Graph projection |

Soft signals never “error into” high mastery. Absence of strong evidence is **honesty**, not failure.

---

## 6. Versioning expectations

| Version | Owner | Expectation |
|---|---|---|
| `PACKAGING_VERSION` (e.g. `AP-002C.1`) | Assessment packaging | Bump when Evidence Bundle schema / strength factors change |
| AP-001 pipeline engine version | Assessment Pipeline | Bump when event → observation mapping changes |
| Educational Reasoning `ENGINE_VERSION` | Reasoning | Bump when rule semantics change |
| Twin schema / ObservationKind | Twin programme | Additive kinds only via coordinated milestone |

**Compatibility rules:**

1. Reasoning must tolerate unknown metadata keys (ignore safely).
2. Reasoning must not require future packaging fields for baseline runs.
3. Breaking packaging fields require coordinated Reasoning readiness **before** student-visible cutover.
4. Same versions + same inputs → same outputs (determinism).

---

## 7. Determinism contract

Given identical:

- Twin prior inferences and observation set
- Curriculum retrieval results
- Graph relationship structure
- Engine / packaging / pipeline versions

then `StudentReasoningService.reason` must reproduce the same educational decisions and explanations (ordering of equivalent sets may be normalised as today).

No hidden randomness. No LLM in the educational decision core.

---

## 8. Minimal call sequence (normative)

```
1. Validate & package EvidenceBundle (Assessment)
2. Export DTO across Evidence Boundary
3. Map → AssessmentEvent(s) (AP-001)
4. Append Observation(s) via ObservationService
5. StudentReasoningService.reason(
       twin,
       triggered_by="assessment_pipeline:<event_type>",
       observation_ids=<ids for this cycle>,
       persist=True,
   )
6. Graph projection refresh (inside / after reason as today)
7. Optional mission refresh (consumer only)
```

Steps 1–2 must never jump to Twin inference writes.
