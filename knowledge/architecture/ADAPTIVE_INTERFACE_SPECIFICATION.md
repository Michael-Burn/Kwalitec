# MS-003 — Adaptive Interface Specification

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001 / 002  
**Status:** Architecture Design; **A0 Contracts — Implemented** (`app/infrastructure/adapters/adaptive_engine/`)  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Extends:** MS-001 `BRIDGE_INTERFACE_SPECIFICATION.md` (Recommendation / AdaptiveDecisionPort); MS-002 TraceRef patterns

---

## 0. Conventions

### Layers

| Layer | Responsibility |
|---|---|
| Experience Port / Facade | `AdaptiveDecisionPort`, HomeService, EducationalStateService |
| Adaptive Engine Adapter | Assembles snapshot; invokes Engine; projects DTOs; telemetry; flags |
| Adaptive Learning Engine | Pure decision computation + ExplanationBundle |
| Educational Services | Authoritative Runtime A **read** APIs |
| Database / Curriculum | Existing SQLAlchemy models / Curriculum JSON |

### Shared types (logical)

| Type | Meaning |
|---|---|
| `StudentId` | Authenticated user id |
| `TopicCode` | Curriculum topic identifier |
| `DecisionId` | Stable id for AdaptiveDecisionRecord |
| `MissionId` | SQL Mission.id (stringified) |
| `AttemptId` | StudyAttempt.id (stringified) |
| `OpaqueDict` | Projection document safe for Experience |
| `BridgeResult[T]` | `{ ok, value?, error_code?, message?, fallback_used }` |
| `ExplanationBundle` | See `ADAPTIVE_EXPLAINABILITY.md` |
| `AdaptiveInputSnapshot` | See parent architecture §5.2 |
| `AdaptiveDecisionRecord` | See §2 |

### Shared failure codes

Reuse MS-001 / MS-002 codes where applicable:

| Code | Meaning |
|---|---|
| `UNAVAILABLE` | Downstream service or DB unreachable |
| `NO_ACTIVE_PLAN` | No active StudyPlan |
| `NOT_FOUND` | Insufficient context for a decision kind |
| `FORBIDDEN` | Ownership failure |
| `INVALID_STATE` | Malformed request / illegal as_of |
| `EXPLAINABILITY_INCOMPLETE` | Decision computed but explanation missing required fields — **must not ship to UX as guidance** |
| `BEHAVIOUR_MISMATCH` | Parity / golden check (tests only) |

### Shared read-only rule

Adaptive Engine Adapter / Engine **must not**:

- Call Planning ensure/generate  
- Start / resume / complete sessions  
- Write TopicProgress or StudyAttempt  
- Accept evidence  
- Mutate StudyPlan  
- Emit demo seeds when Adaptive Engine flags are on  
- Change RecommendationService algorithm bodies  

---

## 1. `AdaptiveEngineBridge` (adapter)

**Purpose:** Experience AdaptiveDecisionPort backed by Adaptive Learning Engine.  
**Backs:** `AdaptiveDecisionPort.get_todays_recommendation` / `decide` (and Revision priority reads as designed).  
**Ownership:** Infrastructure adapter.  
**Educational owners (read):** Evidence / Attempt reads, TopicProgress, MissionService, ReadinessService, CurriculumService, RecommendationService, StudyPlanService, LearningLifecycleService, AdaptiveLearningService **read APIs**.

### 1.1 `decide`

**Inputs**

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | Current user |
| `as_of` | datetime | No | Defaults to server now |
| `decision_kinds` | list[str] | No | Default `["COMPOSITE"]` |
| `include_explanation` | bool | No | Default **true** (required true for UX guidance) |
| `shadow` | bool | No | Force shadow semantics for this call |

**Outputs** (`BridgeResult[AdaptiveDecisionRecord]`)

Success value: §2 record.  
On `EXPLAINABILITY_INCOMPLETE`: `ok=false` (or ok with `fallback_used` to Recommendation Bridge — product policy: **prefer fallback over unexplained guidance**).

### 1.2 `get_todays_recommendation` (Experience-shaped)

Projects AdaptiveDecisionRecord into existing recommendation OpaqueDict shape used by Home (compatible with Recommendation Bridge fields):

```
{
  topic_title,
  recommendation_label,
  category,
  explanation_summary,      # from ExplanationBundle.why.summary
  alternatives,             # from record.alternatives
  confidence_score,
  confidence_band,
  mission_aligned,
  decision_id,
  authority: "adaptive_engine",
  explanation,              # full ExplanationBundle or compact
  fallback_used,
  rule_or_model_ids
}
```

**Mission alignment:** If today’s Mission exists, `topic_title` / `recommendation_label` **equal** mission title; `mission_aligned=true`. Engine primary differing topic appears under `alternatives` or `advisory_next_topic`, never as contradictory primary.

### 1.3 `compare_shadow` (ops / dual-run)

**Inputs:** `student_id`, `as_of`  
**Outputs:** Engine record + Recommendation Bridge snapshot + diff summary (topics, categories, confidence).  
**No UX mutation.**

---

## 2. `AdaptiveDecisionRecord`

```
{
  decision_id,                 # DecisionId
  student_id,
  as_of,
  decision_kind,               # NEXT_FOCUS | REVISION_SET | … | COMPOSITE
  outputs: {
    next_topic: { topic_code, title } | null,
    revision_priority: [ { topic_code, title, rank, due_hint } ],
    confidence_score,          # 0..1
    confidence_band,           # low | medium | high
    study_intensity,           # enum/band | null
    workload_balancing: { suggested_minutes, rationale_code } | null,
    revision_spacing: [ { topic_code, suggested_interval_days } ] | null,
    alternatives: [
      { topic_code, title, rank, score, reason_codes[] }
    ]
  },
  mission_context: {
    mission_id | null,
    mission_topic_code | null,
    mission_aligned: bool
  },
  explanation: ExplanationBundle,   # mandatory for UX
  input_fingerprint,           # hash of AdaptiveInputSnapshot material fields
  model_versions: { rule_or_model_id: version },
  authority: "adaptive_engine",
  created_at
}
```

### Null / empty policy

| Situation | Policy |
|---|---|
| No candidates | `next_topic=null`; explanation states paucity; confidence low |
| No revision stage | `revision_priority=[]` with `not_applicable` reason in explanation |
| Missing readiness | workload facets null; confidence reduced; never fabricate |

**Forbidden:** Inventing topic titles not in CurriculumService; inventing attempt ids.

---

## 3. `AdaptiveInputSnapshot` (assembler contract)

Documented in parent §5.2. Adapter-owned assembly; Engine treats as immutable input.

Minimum required for `COMPOSITE` when plan exists:

- `curriculum_context` (non-empty ordered leaves or explicit empty syllabus error)  
- `lifecycle_stage`  
- `student_goals` (may be sparse)  
- At least one of: topic_progress, mission_history, recommendation_snapshot  

Evidence may be empty for new learners — decision must explain evidence paucity.

---

## 4. Port mapping

| Experience concern | Current (typical) | MS-003 Adaptive Engine |
|---|---|---|
| `AdaptiveDecisionPort.get_todays_recommendation` | Recommendation Bridge / seed | `AdaptiveEngineBridge.get_todays_recommendation` when flag on |
| Revision priorities | Demo / AdaptiveLearning weak topics via other paths | `decide(kinds=["REVISION_SET"])` |
| Explanation card | EducationalExplainabilityService / demo | `ExplanationBundle` (+ ExplainabilityService phrasing templates) |

---

## 5. Telemetry hooks

| Event | Payload (non-PII) |
|---|---|
| `ADAPTIVE_ENGINE_REQUESTED` | student_id scope, decision_kinds |
| `ADAPTIVE_ENGINE_SUCCESS` | decision_id, confidence_band, latency_ms |
| `ADAPTIVE_ENGINE_FAILURE` | error_code |
| `ADAPTIVE_ENGINE_SHADOW_COMPARE` | match_primary_topic bool, category_diff |
| `adaptive.explainability_complete` | bool |

---

## 6. Feature-flag behaviour

| Flag state | `decide` / port behaviour |
|---|---|
| Engine off, shadow off | Prior Recommendation Bridge / Experience path |
| Shadow on, Engine off | Prior UX + background compare |
| Engine on | Port uses Engine; fallback to Recommendation Bridge on failure |
| Engine on + incomplete explanation | Do not show unexplained guidance; fallback |

---

## 7. Acceptance checks (interfaces)

| ID | Check |
|---|---|
| I-1 | Successful UX-bound decide always includes ExplanationBundle with six questions answered |
| I-2 | Mission alignment fields correct when mission present |
| I-3 | Adapter module imports no educational write entrypoints (architecture test) |
| I-4 | OpaqueDict remains ORM-free |
| I-5 | Shadow compare does not alter AdaptiveDecisionPort UX result |
