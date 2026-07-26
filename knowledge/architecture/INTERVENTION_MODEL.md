# MS-005 — Intervention Model

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Related:** `STRATEGY_PIPELINE.md`, `STRATEGY_EXPLAINABILITY.md`, `STRATEGY_INTERFACE_SPECIFICATION.md`

---

## 1. Purpose

Define the **logical intervention vocabulary**, lifecycle, and planning models used by the Learning Strategy Engine.

Interventions are **orchestration artefacts**. They structure Adaptive recommendations + Twin factors + Runtime A constraints into actionable plans. They are **not** educational facts, Twin claims, or Adaptive rankings.

**No schema changes.** All types are logical DTOs for a future implementation milestone.

---

## 2. Core types

```
Intervention {
  intervention_id,              # digest-stable within StrategyDecisionRecord
  kind,                         # see §3
  priority_band,                # critical | high | medium | low | advisory
  status,                       # lifecycle state — see §4
  topic_refs[],                 # curriculum topic codes involved
  minutes_budget,               # suggested minutes (nullable)
  adaptive_decision_ref,        # Adaptive decision_id consumed (required when Adaptive available)
  twin_snapshot_ref,            # Twin snapshot fingerprint (nullable if Twin unavailable)
  runtime_a_refs[],             # EvidenceRef / MissionId / AttemptId / StudyPlan id
  educational_principle_ids[],  # ≥1 registered principle
  explanation_ref,              # StrategyExplanationBundle id / embedded
  limitations[]                 # honest bounds codes
}
```

```
InterventionPlan {
  plan_id,
  student_id,
  as_of,
  strategy_decision_id,
  primary_intervention,         # exactly one primary for UX director tone
  supporting_interventions[],   # ordered; may be empty
  mission_alignment: {
    mission_id?,
    mission_aligned,            # bool
    summary
  },
  input_fingerprint,
  engine_version,
  serialize()
}
```

```
StrategyDecisionRecord {
  decision_id,
  student_id,
  as_of,
  intervention_plan,
  explanation,                  # StrategyExplanationBundle
  confidence: { score?, band, rationale },
  authority_status,             # shadow_only | strategy_engine | gate_ineligible | fallback | failed
  feature_flag_state,
  serialize()
}
```

---

## 3. Intervention kinds

| Kind | Purpose | Typical triggers |
|---|---|---|
| `STUDY_PLAN` | Multi-horizon study structure advice | Exam proximity, sparse coverage, Adaptive next_topic set |
| `SESSION_PLAN` | Tonight’s completable session shell | Home load / Start-adjacent advice |
| `REVISION_PLAN` | Structured revision windows / topic set | Lifecycle Revision; Adaptive revision_priority |
| `RECOVERY_PLAN` | Restart after failure / interruption | Abandoned mission, failed attempts, Twin persistence dips |
| `FATIGUE_MANAGEMENT` | Break / intensity / stop advice | Twin cognitive load + recent attempt density |
| `CONFIDENCE_INTERVENTION` | Calibration / honesty guardrail | Twin confidence trend vs Runtime A performance divergence |
| `CONTINUE` | Affirm Adaptive CONTINUE / mission continuation | Stable learning stage, mission in progress |
| `BREAK` | Explicit rest intervention | Fatigue critical; diminishing returns |
| `ASSESS` | Suggest performance check structure (not invent scores) | Confidence / evidence gap — structure only |

**Phase-1 Strategy Ready (design target):** `SESSION_PLAN`, `REVISION_PLAN`, `RECOVERY_PLAN`, `FATIGUE_MANAGEMENT`, `CONFIDENCE_INTERVENTION`, plus optional `STUDY_PLAN` advice.  
`CONTINUE` / `BREAK` / `ASSESS` remain vocabulary for extensibility without redesign.

---

## 4. Intervention lifecycle

```
PROPOSED
   ↓  (StrategyExecutor emits InterventionPlan)
EXPLAINED
   ↓  (StrategyExplanationBundle complete)
GATED
   ↓  (Explainability Gate PASS | FAIL)
   ├─ FAIL → SHADOW_ONLY / INELIGIBLE (never student guidance)
   └─ PASS →
        ├─ Shadow flag only → OBSERVED (discard for UX)
        └─ Authority ON → SERVED
              ↓
         ACCEPTED | DEFERRED | DISMISSED   (Experience / student action signals — observational)
              ↓
         OUTCOME_LINKED                   (subsequent Runtime A evidence — observational)
```

| State | Meaning | May write educational SoT? |
|---|---|---|
| `PROPOSED` | Computed intervention structure | No |
| `EXPLAINED` | Explanation attached | No |
| `GATED` | Gate evaluated | No |
| `OBSERVED` | Shadow telemetry only | No |
| `SERVED` | Shown via Experience port | No |
| `ACCEPTED` / `DEFERRED` / `DISMISSED` | Observational UX signal (optional later) | No |
| `OUTCOME_LINKED` | Linked to later Mission/Attempt refs | No (Runtime A owns outcomes) |

**Invariant:** Lifecycle never authorises Runtime A mutation. Student Start / Complete remain Runtime A write paths.

---

## 5. Study planning model

**Purpose:** Advise a multi-session / multi-day study structure without owning `StudyPlan` SQL.

```
StudyPlanAdvice {
  horizon: { days | sessions },
  focus_topics[],               # from Adaptive primary + alternatives (order preserved)
  daily_minutes_band,           # from goals + Adaptive workload_balancing
  stage_policy,                 # Learning | Revision
  checkpoints[],                # structural checkpoints (e.g. practice-close ritual nights)
  twin_factors_used[],
  limitations[]
}
```

| Rule | Binding |
|---|---|
| Topic order | Must preserve Adaptive ranking; Strategy may group/window but **not** re-rank |
| Goals | Minutes / exam date from Runtime A StudyPlan only |
| Coverage claims | Cite Runtime A TopicProgress / Readiness — never invent mastery |
| Twin role | Rhythm / consistency / load modulate **density and spacing**, not topic identity |

---

## 6. Session planning model

**Purpose:** Tonight’s completable session shell (EP-004 director + checklist value).

```
SessionPlanAdvice {
  primary_topic,                # MUST equal mission topic when mission exists
  advisory_topic?,              # Adaptive primary if differs (labelled advisory)
  phases: [
    { name, minutes, intent }   # e.g. open, study_materials, practice_close
  ],
  total_minutes,
  close_ritual,                 # performance honesty / Practice Outcome structure
  materials_note,               # bring-your-own materials — no content generation
  twin_factors_used[],
  adaptive_decision_ref,
  educational_principle_ids[]   # must include ep.director.nightly_topic and/or ep.session.completable_shell
}
```

### Session phase vocabulary (design)

| Phase | Intent |
|---|---|
| `orient` | Confirm tonight’s topic + why |
| `study_materials` | External CMP / notes / papers (product boundary) |
| `practice_close` | Forced performance confession structure |
| `log_outcome` | Point to Runtime A completion / attempt path |

**Forbidden:** Generating actuarial content; replacing textbooks; inventing mark conversion.

---

## 7. Revision planning model

**Purpose:** Structure Adaptive `revision_priority` into windows and topic sets.

```
RevisionPlanAdvice {
  windows: [
    { window_id, due_band, topics[], suggested_minutes, rationale_codes[] }
  ],
  primary_revision_topic,
  spacing_note,                 # from Adaptive revision_spacing when present
  twin_revision_behaviour_ref?,
  adaptive_decision_ref,
  limitations[]
}
```

| Rule | Binding |
|---|---|
| Topic selection | Adaptive revision_priority is source of topic identity |
| Spacing | May project Adaptive spacing advice; must not invent retention curves without registered rule |
| Twin | Revision behaviour facet modulates urgency band language, not topic invention |

---

## 8. Recovery planning model

**Purpose:** Restart that still counts — without shame theatre or fabricated diagnosis (EP-004 secondary).

```
RecoveryPlanAdvice {
  trigger: {
    kind,                       # abandoned_mission | failed_attempt | long_gap | interrupted_session
    runtime_a_refs[]
  },
  restart_topic,                # mission-aligned when mission exists; else Adaptive primary
  steps: [
    { order, action_code, summary }
  ],
  what_still_counts,            # honest: what Runtime A already recorded
  what_does_not_count,          # honesty guard: incomplete ≠ mastery
  twin_persistence_ref?,
  educational_principle_ids[]   # ep.recovery.restart_that_counts; ep.honesty.completion_neq_mastery
}
```

**Forbidden:** Motivational pep-talk copy as the intervention body; inventing “you’re behind” without Runtime A refs; claiming Strategy healed mastery.

---

## 9. Fatigue management

**Purpose:** Protect educational value when load signals show diminishing returns.

```
FatigueIntervention {
  severity_band,                # low | medium | high | critical
  recommended_action,           # reduce_intensity | insert_break | stop_for_tonight | shorten_session
  minutes_adjustment?,
  twin_cognitive_load_ref,
  runtime_a_activity_refs[],    # recent attempts / session density
  adaptive_intensity_ref?,      # if Adaptive study_intensity present
  educational_principle_ids[]   # ep.fatigue.diminishing_returns
}
```

| Signal source | Use |
|---|---|
| Twin Cognitive Load Indicators | Primary interpretive fatigue signal |
| Runtime A recent attempt density / session length | Authoritative activity evidence |
| Adaptive study_intensity / workload_balancing | Recommendation constraint — Strategy may tighten, not invent |

**Critical fatigue:** Prefer `BREAK` / `stop_for_tonight` as primary intervention; Adaptive topic advice becomes deferred supporting.

---

## 10. Confidence intervention

**Purpose:** Calibrate confidence to Runtime A performance evidence (anti-false-confidence for resitters).

```
ConfidenceIntervention {
  divergence_band,              # none | mild | material | severe
  twin_confidence_trend_ref,
  runtime_a_performance_refs[], # attempts / scores / TopicProgress — facts only
  recommended_action,           # affirm_cautious | request_practice_close | reduce_certainty_copy | assess_structure
  honesty_guard_copy_codes[],   # machine codes for Experience tone — not free-form pep
  educational_principle_ids[]   # ep.confidence.calibrate_to_evidence; ep.honesty.completion_neq_mastery
}
```

| Rule | Binding |
|---|---|
| Divergence | Twin confidence **vs** Runtime A performance — never Twin vs Adaptive alone as “truth” |
| No invented scores | Strategy cites attempt / progress refs; does not compute new mastery |
| Tone | Inspectable calibration, not motivational theatre |

---

## 11. Composition rules (primary selection)

Strategy selects **exactly one primary intervention** per `InterventionPlan`:

| Condition | Primary kind |
|---|---|
| Fatigue `critical` | `FATIGUE_MANAGEMENT` / `BREAK` |
| Recovery trigger active + not fatigue-critical | `RECOVERY_PLAN` |
| Lifecycle Revision + Adaptive revision focus | `REVISION_PLAN` |
| Confidence divergence `material`+ and no recovery/fatigue primary | `CONFIDENCE_INTERVENTION` (may be supporting if session primary wins) |
| Default learning night | `SESSION_PLAN` |

Supporting interventions may include study-plan advice and confidence/fatigue advisories when not primary.

**Adaptive primary topic** always appears in session/revision structure (as primary or advisory). Strategy never invents a competing primary topic identity.

---

## 12. Empty / unavailable authenticity

| Situation | Contract |
|---|---|
| No Adaptive | `limitations` includes `adaptive_unavailable`; prefer empty authentic or RecommendationService-shaped topic pass-through — **never invent ranking** |
| No Twin | Twin refs `unavailable`; fatigue/confidence interventions limited or omitted with codes |
| No mission + Learning stage | Session plan may use Adaptive primary as primary topic |
| New learner / sparse evidence | `sparse_evidence` limitation; organisational director tone over diagnostic certainty |

---

## 13. Immutability

Once emitted inside a `StrategyDecisionRecord`, Intervention and InterventionPlan objects are **immutable**. Updates require a new decision with a new `as_of` / input fingerprint.
