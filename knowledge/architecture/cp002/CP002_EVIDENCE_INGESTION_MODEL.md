# CP-002 — Evidence Ingestion Model

**Programme:** CP-002 — Capability Programme  
**Version:** 1.0  
**Status:** Active — evidence ingestion & qualification architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP002_LEARNING_FEEDBACK_ARCHITECTURE.md`  
**Constraint:** Conceptual model only — no collectors, schema, or emitters modified by this programme.

---

## 1. Purpose

Define how Learning Feedback Loop signals are **ingested**, **classified**, and **qualified** before they may become learning proposals.

**Rule:** Raw observation is not learning. Only qualified evidence with educational meaning may enter proposal stages.

---

## 2. Signal sources (input classes)

| Class | Source authority | Nature | Default claim boundary |
|-------|------------------|--------|------------------------|
| **A — Observational** | EP-003.4 `LearningFeedbackEvent` | Immutable observed behaviour | `preference_journal` / `plan_interaction` / `observed_behaviour` / `study_habit_signal` |
| **B — Decision memory** | CP-001 DecisionRecord (+ ILE-002 baseline) | Guidance freeze + student choice + outcome links | `organisation` → `learning_signal` when linked |
| **C — Outcome packs** | OM-001 filed evidence packs | Measured educational outcomes | Pack-declared boundary |
| **D — Reflection** | SI-C5 / CP-001 ReflectionAttachment | Optional elevated self-report | Elevated privacy; never coerced |
| **E — Sensei review** | ILE-005 educational review states | Internal governance assessment | Not student-facing ranking input |

Sources may join on `decision_id`, `recommendation_id`, `mission_id`, `attempt_id`, or pack `metric_ids[]`. Orphan vanity events without join keys remain Class A only and cannot drive LU-POL.

---

## 3. Ingestion envelope (conceptual)

Every ingested signal becomes a **FeedbackSignal** (design entity):

| Field | Meaning |
|-------|---------|
| `signal_id` | Stable opaque id |
| `learner_id?` | Present for learner-scoped signals; absent for aggregate packs |
| `source_class` | A…E |
| `source_ref` | Pointer to originating event / record / pack |
| `educational_meaning_code` | **Required** EF-* (Architecture §8) |
| `observed_at` | Event time |
| `ingested_at` | Ingestion time |
| `claim_boundary` | Evidence Model tag |
| `om_metric_ids[]` | Optional catalogue links |
| `si_capability_tags[]` | SI-C* tags |
| `join_keys` | decision / recommendation / mission / attempt ids |
| `payload_digest` | Hash or structured summary — no forbidden inference keys |
| `qualification_status` | See §5 |
| `limitations[]` | Mandatory when qualified or rejected |

**Invariant:** `educational_meaning_code` is mandatory. Signals without EF-* fail ingestion.

---

## 4. Educational meaning assignment

### 4.1 Mapping from known event types (normative defaults)

| Known source signal | Default EF-* | Notes |
|---------------------|--------------|-------|
| recommendation_accepted / Journal accept | EF-ACCEPT | Preference only — not mastery |
| recommendation_dismissed / Journal reject | EF-REJECT | Lawful agency |
| Journal defer | EF-DEFER | Not failure |
| plan_completed / mission complete link | EF-FOLLOW | Behavioural follow-through |
| OM-REC-08 / OM-LRN-* pack rows | EF-LEARN | Requires pack decision Supports |
| readiness band vs later performance | EF-READY | Calibration substrate |
| Optional reflection “did this help?” | EF-REFLECT | Optional; skip is lawful |
| study_consistency_observed | EF-HABIT | Habit ≠ learning quality |
| recovery_applied / revision_adhered|deferred | EF-RECOVER | Plan interaction |
| OM-EXP sample / empty-evidence flags | EF-EXPLAIN | Explainability honesty |
| ILE-005 Evidence insufficient | EF-INSUFF | Explicit humility |
| Contradictory accept+learn-negative | EF-CONFLICT | Forces human review |

### 4.2 Forbidden meanings

Ingestion **must reject** attempts to encode as EF-LEARN (or any learning claim) from:

- Tip accept alone  
- Streak length alone  
- Session duration alone  
- UI chrome clicks  
- Founder anecdote without pack  

These may remain EF-ACCEPT / EF-HABIT / EF-FOLLOW with limitations, or be discarded as non-educational.

---

## 5. Evidence qualification rules

Qualification upgrades a FeedbackSignal from raw to **QualifiedEvidence** eligible for proposals.

### 5.1 Qualification statuses

| Status | Meaning | May enter proposals? |
|--------|---------|----------------------|
| `raw` | Ingested; meaning assigned; not yet reviewed | LU-OBS aggregates only |
| `qualified` | Passed §5.2 rules | Yes — class-limited |
| `insufficient` | Explicitly too thin (EF-INSUFF or C0) | No LU-POL / LU-TWN mastery-adjacent |
| `conflicted` | EF-CONFLICT or unresolved contradiction | Human checkpoint required |
| `rejected` | Failed validation / forbidden inference | No |
| `superseded` | Replaced by stronger pack evidence | Historical only |

### 5.2 Qualification checklist (all must pass for `qualified`)

1. **Meaning present** — valid EF-*  
2. **Source lawful** — source_class authorised for this EF-*  
3. **Claim boundary consistent** — boundary ≤ what the signal can support  
4. **No forbidden inference keys** — mirrors EP-003.4 `FORBIDDEN_INFERENCE_KEYS` (+ decision keys `next_action`, `plan_slots`, `mastery_delta` invented from clicks)  
5. **Join integrity** — learner-scoped signals owned; no cross-learner leakage  
6. **Flag honesty** — if source required a feature flag, recorded flag state at observation  
7. **Limitations declared** — at least one limitation string when sample thin or self-report  
8. **Confidence class assigned** — C0–C4 per OM-001 / Measurement Standard posture  
9. **For EF-LEARN / LU-POL candidates** — OM pack id present OR explicit pre-registered trial metric  

### 5.3 Confidence class (ingestion-facing)

| Class | Meaning for loop | Typical use |
|-------|------------------|-------------|
| **C0** | Exploratory / anecdotal | Never LU-POL |
| **C1** | Sparse observational | LU-OBS; LU-CAL humility only |
| **C2** | Reproducible operational aggregates | LU-CAL; LU-TWN behaviour |
| **C3** | Reviewed pack Supports | LU-POL candidate eligible |
| **C4** | Independent / trial-grade | LU-EXP promote eligible |

Detail on how classes update product confidence: `CP002_CONFIDENCE_CALIBRATION.md`.

---

## 6. Qualification → update class eligibility

| Qualification | Max update class without extra gate | Notes |
|---------------|-------------------------------------|-------|
| `raw` | LU-OBS | Buffer / analytics |
| `qualified` + C0–C1 | LU-OBS, LU-CAL (disclose-down only) | No stronger certainty |
| `qualified` + C2 | LU-CAL, LU-TWN (behaviour) | Twin Constitution still binds |
| `qualified` + C3 | LU-POL *candidate* | Still requires Architecture §5 checkpoint |
| `qualified` + C4 | LU-EXP path | SI-C10 + Independent Review |
| `conflicted` / `insufficient` | None behavioural | Human review or STOP |

---

## 7. Aggregation rules

| Rule | Meaning |
|------|---------|
| **Deterministic windows** | Aggregates declare window, n, eligibility (OM pack schema) |
| **No silent cohort mixing** | Flag-ON and flag-OFF populations separated |
| **Curriculum scoped** | Topic refs via CurriculumService ids; V1/V2 both valid |
| **Refuse vanity denominators** | Do not define “success rate” as accepts / impressions alone for educational claims |
| **Append-only raw store** | Corrections create new qualified rows; never mutate history |

---

## 8. Privacy and elevation

| Signal class | Posture |
|--------------|---------|
| Class A observational | Behavioural; student-scoped; fail-open emitters unchanged by this design |
| Class B journal | CP-001 privacy model; rationale elevated if free text |
| Class D reflection | Highest care; optional; never required for ranking eligibility |
| Class E Sensei review | Internal governance; not exported to student chronology as tips |

Erasure / retention follow CP-001 Privacy Model and account policy; CP-002 does not invent a parallel privacy regime.

---

## 9. Validation failures (normative rejects)

| Failure | Action |
|---------|--------|
| Missing EF-* | Reject ingestion |
| Forbidden inference key in payload | Reject |
| Cross-learner join | Reject + security review |
| EF-LEARN without pack/trial warrant | Downgrade to EF-FOLLOW or reject |
| Rewriting ExplanationSnapshot | Reject (append-only) |
| Auto-proposal for LU-POL from C0–C2 | Reject proposal creation |

---

## 10. Relationship to EP-003.4 / CP-001 / OM-001

```
EP-003.4 events ──┐
CP-001 records  ──┼──► FeedbackSignal ──► QualifiedEvidence ──► LearningProposal
OM-001 packs    ──┤         ▲
Reflection opt  ──┘         │
                     EF-* + qualification rules (this document)
```

EP-003.4 remains record-only at emission. CP-002 defines how those records (and richer journal/outcome joins) become *qualified* educational evidence for governed learning — without granting EP-003.4 adaptation authority.

---

## 11. Non-goals

- No durable store implementation  
- No change to emitter schemas  
- No automatic qualification bots without future ADR  
- No student UI for qualification status  

---

**End of CP-002 Evidence Ingestion Model**
