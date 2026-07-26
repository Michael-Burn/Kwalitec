# MS-003 — Adaptive Explainability

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Contracts:** `ADAPTIVE_INTERFACE_SPECIFICATION.md`  
**Principles:** DP-005 Explainability, DP-009 Evidence Before Opinion, DP-010 Human-Centred Intelligence

---

## 1. Purpose

Every adaptive recommendation / decision shown as guidance must answer six questions. If it cannot, it is **not ready** to display as guidance (DP-005).

| # | Question | Contract field |
|---|---|---|
| 1 | Why? | `why` |
| 2 | Which evidence? | `evidence_refs` |
| 3 | Which topics? | `topic_refs` |
| 4 | Which rule or model? | `rule_or_model` |
| 5 | Confidence? | `confidence` |
| 6 | Alternatives considered? | `alternatives` |

---

## 2. `ExplanationBundle` contract

```
ExplanationBundle {
  why: {
    summary,                 # plain language, student-safe
    reason_codes[]           # stable machine codes
  },
  evidence_refs: [
    { kind, id, observed_at?, note? }
  ],
  topic_refs: [
    { topic_code, title, role }   # role: primary | alternative | supporting | weak | due
  ],
  rule_or_model: {
    rule_or_model_id,        # registered deterministic id
    version,
    description              # short human label
  },
  confidence: {
    score,                   # 0..1 mirrors outputs.confidence_score
    band,                    # low | medium | high
    rationale                # what raised/lowered confidence
  },
  alternatives: {
    items: [
      { topic_code, title, rank, reason_codes[], why_not_selected }
    ],
    rationale                # how selection among alternatives worked
  },
  limitations: {
    codes[],                 # e.g. sparse_evidence, stale_readiness, no_mission
    summary                  # honest bounds — what this decision does NOT claim
  },
  mission_note: {
    mission_aligned,
    summary                  # e.g. "Tonight’s session follows your mission; adaptive advice agrees / differs as alternative"
  } | null
}
```

### Completeness rule

For UX-bound decisions, **all six question groups** must be present as objects (arrays may be empty only with explicit `limitations` explaining paucity — e.g. new learner with zero attempts).

`EXPLAINABILITY_INCOMPLETE` if any required group missing or `why.summary` empty.

---

## 3. Evidence refs

| `kind` | `id` | Notes |
|---|---|---|
| `attempt` | AttemptId | Preferred for practice-grounded claims |
| `mission` | MissionId | Session context |
| `topic_progress` | topic_code (+ user scope) | Mastery/coverage signal |
| `readiness` | aggregate label / as_of | Not a substitute for attempts |
| `recommendation` | dated snapshot id / fingerprint | Composition with RecommendationService |
| `study_plan` | plan id | Goals context |

**Forbidden:** Citing evidence the student does not own; inventing attempt ids; treating absence of evidence as proof of mastery (DP-009).

Empty `evidence_refs` allowed **only** with `limitations.codes` including `sparse_evidence` (or equivalent) and reduced confidence.

---

## 4. Rule / model registry (design)

Every decision cites a registered `rule_or_model_id`.

| Example id (illustrative) | Intent |
|---|---|
| `curriculum.next_incomplete_leaf` | Syllabus-forward next topic |
| `adaptive.weak_topic_priority` | Weak-topic revision ordering |
| `adaptive.spacing.due_window` | Revision spacing advice |
| `adaptive.workload.minutes_fit` | Workload balancing vs goals |
| `adaptive.intensity.from_attempts` | Intensity band from recent attempts |
| `compose.recommendation_service_v1` | Composition with existing RecommendationService snapshot |

Registry is documentation + code constants in a later implementation milestone — **not** a schema change. Versions bump when material behaviour changes (determinism / replay).

**Forbidden in educational core:** Opaque LLM-only model ids without deterministic rule grounding.

---

## 5. Confidence design

| Band | Typical meaning | UX guidance |
|---|---|---|
| `high` | Rich recent evidence + stable progress + curriculum-clear candidate | Assertive but still explainable |
| `medium` | Partial evidence or mild conflict among signals | Balanced language |
| `low` | Sparse / stale / conflicting inputs | Hedge; prefer organisational director tone over diagnostic certainty |

Confidence must never be displayed without `rationale`. Inflating confidence without evidence is an explainability failure (see Risk Analysis).

---

## 6. Alternatives design

At least **one** alternative should be present when multiple curriculum-legal candidates exist. If only one candidate exists, `alternatives.items` may be empty with `rationale` stating singleton candidate set.

Each alternative requires `why_not_selected` (codes + short text). Silent single-choice theatre is forbidden when peers were scored.

---

## 7. Mapping to existing explainability services

| Layer | Role |
|---|---|
| Adaptive Engine | Produces structured ExplanationBundle (facts + codes + refs) |
| `EducationalExplainabilityService` | May render plain-language narratives from codes / recommendation categories (**templates unchanged in spirit**; may accept new codes later) |
| Experience ExplanationService / explanation card | Displays summary; detail may expand refs |

Engine **owns structured truth of the decision explanation**; narrative polish may reuse existing services without inventing educational causation.

---

## 8. Relationship to MS-002 TraceRef

| MS-002 TraceRef | MS-003 ExplanationBundle |
|---|---|
| what / why / evidence / recommendation delta for **past events** | why / evidence / topics / rule / confidence / alternatives for **future decisions** |

They are complementary:

- Journey/History: “What happened?”  
- Adaptive Engine: “What should happen next, and why?”

A later Outcome linkage may attach `decision_id` onto subsequent Journey events’ recommendation fields when reconstructable — without fabricating deltas.

---

## 9. Student-facing honesty (product constraint)

Aligned with EP-004 evidence: students distrust certainty without inspectability.

Therefore:

1. Prefer **inspectable working** over coach theatre.  
2. `limitations.summary` is mandatory when confidence is low or evidence sparse.  
3. Do not claim exam-mark prediction or content tutoring authority in adaptive explanations.  
4. When mission differs from raw Engine preference, say so (`mission_note`).

---

## 10. Acceptance checks (explainability)

| ID | Check |
|---|---|
| E-1 | Six questions populated on every UX-bound AdaptiveDecisionRecord |
| E-2 | `rule_or_model_id` always from registry |
| E-3 | Sparse evidence ⇒ low/medium confidence + limitations codes |
| E-4 | Alternatives include why_not_selected when items non-empty |
| E-5 | Incomplete explanation never shown as guidance (fallback or error) |
| E-6 | Golden fixtures document expected ExplanationBundle for ≥3 decision kinds |
