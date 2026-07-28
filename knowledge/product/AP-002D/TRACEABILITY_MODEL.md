# AP-002D — Traceability Model

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`EXPLAINABILITY_REQUIREMENTS.md`](EXPLAINABILITY_REQUIREMENTS.md), MS-004 Digital Twin Traceability

---

## 1. Purpose

Design end-to-end traceability so every step from assessment fact to Tutor narration is reconstructable.

```
Observation
    ↓
Evidence
    ↓
Inference
    ↓
Twin Update
    ↓
Mission
    ↓
Tutor
```

---

## 2. Identity chain

| Step | Primary identifiers |
|---|---|
| Engine Observation | `ObservationId`, `SessionId`, `QuestionId`, `ResultId` |
| Evidence Item / Bundle | `EvidenceItemId`, `EvidenceBundleId`, `PACKAGING_VERSION`, refs to observation ids |
| AP-001 Event | `event_id`, `twin_id`, `event_type`, metadata links to session/bundle |
| Twin Observation | `observation_id`, `evidence_reference`, `provenance` |
| Reasoning | `run_id` / `reasoning_id`, `triggered_by`, `observation_ids`, `ENGINE_VERSION` |
| Twin Update | Twin `updated_at`, inference snapshot ids (e.g. learning-state snapshot) |
| Mission | `mission_id`, activity ids, reason codes citing Twin decisions / reasoning |
| Tutor | Conversation turn refs to mission / feedback / reasoning ids (session-scoped) |

All links must be durable strings suitable for Founder audit — not ephemeral UI-only ids.

---

## 3. Reconstructability requirements

Given any Twin inference change attributed to assessment, an auditor must reconstruct:

1. Which Engine session and items produced the facts  
2. Which Evidence Bundle / items packaged those facts  
3. Which AP-001 event(s) crossed the boundary  
4. Which Twin observation ids were appended  
5. Which Reasoning run applied which rules  
6. Which Twin fields changed  
7. Whether Mission refreshed and which activities cited the new decisions  
8. What Tutor narrated (explanation of decisions, not a new score)

If any link is missing, the chain is incomplete and must not be claimed “fully traced”.

---

## 4. Provenance conventions

| Field | Convention |
|---|---|
| `provenance` (Twin observation) | Include `assessment_pipeline:…` and Engine `session_id` |
| `evidence_reference` | Bundle id and/or Assessment Result / event id |
| `triggered_by` | `assessment_pipeline:<event_type>` for assessment ingress |
| Metadata | Carry `packaging_version`, `evidence_strength`, instrument/intent, misconception tags |
| Reasoning steps | Record rule codes and observation id subsets used |

---

## 5. Persistence expectations

| Store | Holds |
|---|---|
| Assessment Engine persistence | Sessions, responses, packaged bundles |
| AP-001 persistence | Events, pipeline results, learning feedback (metadata only — not Twin mastery SoT) |
| Twin persistence | Observations + inferences + reasoning history |
| Graph persistence | Relationships + projections (not mastery SoT) |
| Mission persistence | Plans/activities + explainable reason codes |
| Tutor | Session memory — not long-term belief |

Cross-store joins use the identity chain above.

---

## 6. Failure of traceability

If packaging succeeds but pipeline emission fails: Engine retains bundle; Twin unchanged; retry export idempotently.  
If observations append but Reasoning fails: facts remain; inferences unchanged; retry Reasoning with same observation ids.  
Never “heal” gaps by writing mastery without a reasoning run id.

---

## 7. Founder / research use

Traceability supports:

- “Did this assessment reduce Twin uncertainty?”  
- Instrument quality (misconception yield, thin-band rate)  
- Pipeline health (events without reasoning)

Founder analytics (AP-002F) consume this chain; they do not become educational authority.
