# MS-005 — Strategy Explainability

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Contracts:** `STRATEGY_INTERFACE_SPECIFICATION.md`, `INTERVENTION_MODEL.md`  
**Principles:** DP-005 Explainability, DP-009 Evidence Before Opinion, DP-010 Human-Centred Intelligence

---

## 1. Purpose

Every intervention shown as guidance must explain:

1. **Why it exists**  
2. **Contributing Runtime A evidence**  
3. **Twin factors considered**  
4. **Adaptive recommendation consumed**  
5. **Educational principle applied**  

No hidden reasoning. If these cannot be answered, the intervention is **not ready** to display as guidance.

---

## 2. Five mandatory questions

| # | Question | Contract field |
|---|---|---|
| 1 | Why does this intervention exist? | `why` |
| 2 | Which Runtime A evidence contributed? | `runtime_a_evidence_refs` |
| 3 | Which Twin factors were considered? | `twin_factors` |
| 4 | Which Adaptive recommendation was consumed? | `adaptive_consumed` |
| 5 | Which educational principle applied? | `educational_principles` |

Additional Adaptive-style fields (confidence, alternatives, limitations, mission note) remain required for UX-bound records.

---

## 3. `StrategyExplanationBundle` contract

```
StrategyExplanationBundle {
  why: {
    summary,                 # plain language, student-safe
    reason_codes[]           # stable machine codes
  },

  runtime_a_evidence_refs: [
    { kind, id, observed_at?, note? }
  ],

  twin_factors: {
    snapshot_ref?,           # Twin snapshot fingerprint
    factors_considered: [
      { facet_id, availability, role, note? }
      # role: primary_driver | modulator | ignored_unavailable | supporting
    ],
    summary                  # what Twin changed about structure (not topic invention)
  },

  adaptive_consumed: {
    decision_id?,            # Adaptive decision_id when available
    primary_topic?,
    recommendation_summary?,
    alternatives_preserved[],# Adaptive alternatives order preserved
    availability,            # available | unavailable
    unavailable_reason?      # required when unavailable
  },

  educational_principles: [
    {
      principle_id,          # registered id — see §6
      version,
      description,           # short human label
      how_applied            # how this intervention instantiates the principle
    }
  ],

  confidence: {
    score?,                  # optional 0..1
    band,                    # low | medium | high
    rationale
  },

  alternatives: {
    items: [
      { intervention_kind, rank, reason_codes[], why_not_selected }
    ],
    rationale
  },

  limitations: {
    codes[],                 # sparse_evidence | twin_unavailable | adaptive_unavailable | stale_snapshot | …
    summary
  },

  mission_note: {
    mission_aligned,
    summary
  } | null
}
```

### Completeness rule

For UX-bound interventions, **all five mandatory question groups** must be present as objects.

| Required | Empty allowed when |
|---|---|
| `why.summary` | Never empty for UX |
| `runtime_a_evidence_refs` | Only with `sparse_evidence` (or equivalent) + reduced confidence |
| `twin_factors` | Object always present; factors may be empty if Twin unavailable with explicit availability |
| `adaptive_consumed` | Object always present; `availability=unavailable` + reason when Adaptive missing |
| `educational_principles` | ≥1 principle with non-empty `principle_id` + `how_applied` |

`STRATEGY_EXPLAINABILITY_INCOMPLETE` if any required group missing or rules violated.

---

## 4. Runtime A evidence refs

| `kind` | `id` | Notes |
|---|---|---|
| `attempt` | AttemptId | Preferred for performance / recovery / confidence calibration |
| `mission` | MissionId | Session / alignment context |
| `topic_progress` | topic_code (+ user scope) | Coverage / mastery **signal** — not Strategy-invented |
| `readiness` | aggregate label / as_of | Not a substitute for attempts |
| `study_plan` | plan id | Goals / minutes / exam window |
| `recommendation` | dated snapshot fingerprint | When Adaptive unavailable and RecommendationService used |

**Forbidden:** Citing evidence the student does not own; inventing attempt ids; treating absence as mastery (DP-009).

---

## 5. Twin factors

| Facet id (align Twin) | Typical Strategy role |
|---|---|
| `learning_rhythm` | Study/session density modulator |
| `consistency` | Recovery / streak honesty |
| `persistence` | Recovery planning |
| `revision_behaviour` | Revision plan urgency language |
| `confidence_trend` | Confidence intervention driver |
| `session_habits` | Session phase fit |
| `cognitive_load` | Fatigue management driver |

**Rules:**

- Twin factors **modulate structure** (minutes, phases, fatigue, recovery tone) — they do **not** invent primary topic identity.  
- Unavailable facets must appear with `availability=unavailable` — never estimated.  
- Strategy must not claim Twin facts as Runtime A evidence.

---

## 6. Adaptive consumption

| Field | Rule |
|---|---|
| `decision_id` | Required when Adaptive available |
| Primary topic | Must match Adaptive primary **or** be explicitly mission-aligned with Adaptive in alternatives/advisory |
| Alternatives | Preserve Adaptive order when listed |
| Unavailable | Document reason; Strategy must not fabricate AdaptiveDecisionRecord |

**Forbidden:** Hidden re-ranking presented as Adaptive consumption; citing Adaptive without `decision_id` when Adaptive Authority path was available.

---

## 7. Educational principle registry (design)

Every intervention cites ≥1 registered `principle_id`.

| Principle id | Intent | Typical kinds |
|---|---|---|
| `ep.director.nightly_topic` | Defensible tonight direction | `SESSION_PLAN` |
| `ep.session.completable_shell` | Reduce evening planning load | `SESSION_PLAN` |
| `ep.honesty.completion_neq_mastery` | Coverage ≠ understanding | `CONFIDENCE_INTERVENTION`, `RECOVERY_PLAN`, close ritual |
| `ep.recovery.restart_that_counts` | Restart without pep-talk theatre | `RECOVERY_PLAN` |
| `ep.fatigue.diminishing_returns` | Protect load / stop advice | `FATIGUE_MANAGEMENT`, `BREAK` |
| `ep.confidence.calibrate_to_evidence` | Confidence vs performance | `CONFIDENCE_INTERVENTION` |
| `ep.inspectability.why_tonight` | Student-verifiable rationale | All UX-bound |
| `ep.revision.spacing_structure` | Structure Adaptive revision advice | `REVISION_PLAN` |
| `ep.study.horizon_structure` | Multi-day structure without plan ownership | `STUDY_PLAN` |

Registry is documentation + future code constants — **not** a schema change. Versions bump when material meaning changes.

**Forbidden in educational core:** Opaque LLM-only principle ids without deterministic grounding.

---

## 8. Confidence design

| Band | Typical meaning | UX guidance |
|---|---|---|
| `high` | Runtime A + Adaptive + Twin available; mission-aligned; rich evidence | Assertive but explainable |
| `medium` | Partial Twin or mild Adaptive/mission tension | Balanced language |
| `low` | Sparse evidence / Adaptive unavailable / Twin unavailable | Organisational director tone; hedge diagnostic claims |

Strategy confidence is about **orchestration completeness**, not a copy of Adaptive confidence alone. Both may be shown; both need rationale.

---

## 9. Explainability Gate

| Check | Rule |
|---|---|
| Why present | Non-empty `why.summary` + reason_codes |
| Runtime A refs | ≥1 evidence ref **or** explicit `sparse_evidence` limitation |
| Twin factors object | Present; unavailable documented |
| Adaptive consumed object | Present; unavailable documented |
| Principles | ≥1 with `how_applied` |
| Confidence | Band + rationale |
| Alternatives | Object present (may be empty with rationale) |
| Limitations | Object present |

| Outcome | Behaviour |
|---|---|
| **PASS** | Eligible for Authority delivery |
| **FAIL** | `STRATEGY_EXPLAINABILITY_INCOMPLETE`; shadow-only; no UX guidance; no mutation |

Gate does not “fix” explanations — fail open to prior Experience path under Authority.

---

## 10. Student-safe language rules

| Do | Do not |
|---|---|
| Cite inspectable topics, missions, attempts | Invent causation (“the AI decided”) |
| Say what Twin suggested about load / habits | Present Twin estimates as exam readiness |
| Say which Adaptive recommendation was used | Hide Adaptive primary when Strategy structures around mission |
| Name the educational principle in plain words | Pep-talk / shame / false certainty |
| State limitations honestly | Demo-seeded theatre under Authority |

---

## 11. Relationship to Adaptive / Twin explainability

| Layer | Explanation answers |
|---|---|
| Adaptive ExplanationBundle | Why this **recommendation** |
| Twin Facet/SnapshotExplanation | Why this **interpretation** |
| StrategyExplanationBundle | Why this **intervention structure** |

Strategy explanations **cite** Adaptive and Twin artefacts; they do not replace them. Experience may surface a compact Strategy why with expandable Adaptive/Twin lineage.
