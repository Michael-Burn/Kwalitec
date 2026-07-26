# MS-004 — Digital Twin Data Model

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Constraint:** No schema changes — logical model over existing Runtime A SQL + curriculum JSON

---

## 1. Purpose

Define the **logical** data model for the Student Digital Twin: what a Learner Profile Snapshot contains, how fields map to Runtime A sources, and which fields are facts vs derived estimates.

Physical persistence for Twin Ready remains **recomputation from Runtime A** (no Alembic). Optional durable Twin tables require ADR-MS004-002 and are out of Twin Ready.

---

## 2. Physical sources (unchanged)

| Entity / service | Twin use |
|---|---|
| `User` | Identity ownership (`student_id`) |
| `StudyPlan` | Goals, exam sitting labels, plan window, revision fields |
| `Mission` (+ `MissionTask`) | Session lineage for Behaviour / Performance structure |
| `StudyAttempt` | Primary Learning Evidence references |
| `TopicProgress` | Knowledge / coverage factual slots (pass-through) |
| Curriculum via `CurriculumService` | Topic identity / order (V1 flat / V2 hierarchical) |
| `ReadinessService` | Readiness aggregates (pass-through; Twin does not invent formula) |
| `LearningLifecycleService` | Learning vs Revision stage |
| Recommendation / Adaptive decision refs (optional) | Preference / response structural refs — not Twin-owned decisions |

**Not authoritative:** `ExperienceProjectionStore` Twin docs, `seeded_demo_*`, unwired V2 Twin engine persistence, AdaptiveOutputBundle (advice only).

---

## 3. Aggregate: `LearnerProfileSnapshot`

Immutable logical aggregate representing the Twin at a point in time.

| Field | Type | Meaning |
|---|---|---|
| `twin_id` | string | Stable projection id (`twin-<student_id>` or versioned hash) |
| `student_id` | StudentId | Ownership scope |
| `as_of` | datetime | Decision / snapshot clock (not wall-clock drift in material fields) |
| `twin_version` | string | Twin synthesis version (rules + facet schema) |
| `authority` | `"digital_twin_synthesis"` | Constant when Twin-produced |
| `freshness` | FreshnessBlock | See §6 |
| `identity` | IdentityFacet | Who the learner is relative to syllabus / sitting |
| `goals` | GoalsFacet | Pass ambition, hours, dates (from plan) |
| `knowledge` | KnowledgeFacet | Structural mastery slots + evidence refs |
| `memory` | MemoryFacet | Structural retention / revision refs |
| `behaviour` | BehaviourFacet | Consistency / adherence structure + session refs |
| `performance` | PerformanceFacet | Assessment / session outcome structural summaries |
| `predictions` | PredictionFacet | Stored / packaged prediction + readiness snapshot slots |
| `confidence` | ConfidenceFacet | Calibration slots (separable from mastery) |
| `field_provenance` | map[string → Provenance] | Per material field / facet block |
| `limitations` | LimitationsBlock | Honest bounds |
| `trace` | TwinTraceRef | See `DIGITAL_TWIN_TRACEABILITY.md` |

**Immutability:** updates produce a **new** snapshot; prior snapshots may be frozen for audit / Adaptive `as_of`.

---

## 4. Facets

### 4.1 `IdentityFacet`

| Field | Source rule | Kind |
|---|---|---|
| `student_id` | Authenticated user | Fact |
| `curriculum_id` / syllabus label | Active StudyPlan / curriculum binding | Fact |
| `exam_label` / sitting | StudyPlan | Fact |
| `lifecycle_stage` | LearningLifecycleService | Derived (Runtime A service) |

### 4.2 `GoalsFacet`

| Field | Source rule | Kind |
|---|---|---|
| `target_exam_date` | StudyPlan | Fact |
| `planned_weekly_hours` / preferred minutes | StudyPlan / mission prefs if available | Fact |
| `ambition_label` | Plan fields when present; else unavailable | Fact / unavailable |

### 4.3 `KnowledgeFacet`

| Field | Source rule | Kind |
|---|---|---|
| `topics[]` | Curriculum order × TopicProgress | Fact structure |
| `topics[].topic_code` / `title` | CurriculumService | Fact |
| `topics[].progress_status` | TopicProgress | Fact (pass-through) |
| `topics[].evidence_refs[]` | StudyAttempt ids for topic | Fact refs |
| `topics[].mastery_belief` | **Deferred** — null / unavailable until ADR-MS004-004 | Estimate (forbidden without ADR) |
| `coverage_summary` | Readiness / plan coverage pass-through | Fact / Runtime A derived |
| `last_evidence_at` | Max attempt / progress timestamp | Fact |

**Ban:** Twin inventing TopicProgress statuses or mastery beliefs that contradict SQL.

### 4.4 `MemoryFacet`

| Field | Source rule | Kind |
|---|---|---|
| `revision_refs[]` | Revision-stage missions / weak-topic activity refs | Fact refs |
| `topics_due_structure[]` | Structural slots from last-seen evidence timestamps — **no forgetting-curve scores without ADR** | Structure / estimate-gated |
| `last_revised_at` | Latest revision-linked mission/attempt | Fact |

### 4.5 `BehaviourFacet`

| Field | Source rule | Kind |
|---|---|---|
| `session_refs[]` | Completed / missed / abandoned Missions | Fact refs |
| `completion_counts` | Counts from Mission statuses | Fact aggregates |
| `adherence_structure` | Planned vs completed day patterns (structural) | Derived structure |
| `consistency_metric` | **Deferred** numeric scoring without ADR | Estimate-gated |
| `preference_refs[]` | Optional recommendation accept/dismiss if available | Fact refs / unavailable |

Governing principle: **Behaviour is not learning; activity is not readiness.**

### 4.6 `PerformanceFacet`

| Field | Source rule | Kind |
|---|---|---|
| `attempt_outcome_summaries[]` | StudyAttempt outcome labels (student-safe) | Fact aggregates |
| `assessment_refs[]` | Assessment-shaped missions/attempts when present | Fact refs |
| `velocity_structure` | Coverage gain vs time invested (structural) | Derived structure |
| Ban | Raw answer keys, full event logs in Experience DTOs | — |

### 4.7 `PredictionFacet`

| Field | Source rule | Kind |
|---|---|---|
| `readiness_snapshot` | ReadinessService at `as_of` | Runtime A derived (pass-through) |
| `pass_probability` | **Deferred** — unavailable unless ADR | Estimate-gated |
| `completion_forecast` | **Deferred** | Estimate-gated |
| `snapshot_label` | Human-safe readiness narrative from Runtime A labels | Projection |

### 4.8 `ConfidenceFacet`

| Field | Source rule | Kind |
|---|---|---|
| `calibration_slots[]` | Structural place for confidence-vs-performance | Structure |
| `self_report_refs[]` | If collected; else unavailable | Fact refs / unavailable |

Confidence is **separable** from Knowledge mastery (do not collapse).

---

## 5. Supporting types

### 5.1 `Provenance`

| Field | Meaning |
|---|---|
| `source_service` | Runtime A service / authority |
| `source_entity` | e.g. `StudyAttempt`, `TopicProgress`, `Mission` |
| `collected_at` | Equals snapshot `as_of` (decision clock) |
| `availability` | `available` \| `unavailable` |
| `unavailable_reason` | Required when unavailable |
| `kind` | `fact` \| `runtime_a_derived` \| `twin_derived` |

**Missing vs empty:**

| Situation | Contract |
|---|---|
| Collector succeeded; no rows (new learner) | `available` + empty payload (honest emptiness) |
| No plan / collector failure | `unavailable` + reason; **never estimate** |

### 5.2 `FreshnessBlock`

| Field | Meaning |
|---|---|
| `latest_evidence_at` | Max Runtime A evidence timestamp considered |
| `snapshot_as_of` | Twin `as_of` |
| `is_stale` | True when beyond freshness window |
| `stale_reason` | Documented when stale |

### 5.3 `LimitationsBlock`

| Field | Meaning |
|---|---|
| `codes[]` | e.g. `sparse_evidence`, `no_active_plan`, `stale_snapshot`, `estimate_deferred` |
| `summary` | Student-safe honest bounds |

### 5.4 `EvidenceRef` (shared with Adaptive / Journey patterns)

| Field | Meaning |
|---|---|
| `kind` | `attempt` \| `mission` \| `topic_progress` \| `study_plan` \| `readiness` \| … |
| `id` | Canonical id |
| `observed_at` | Optional |
| `note` | Optional student-safe |

**Forbidden:** Citing non-owned evidence; inventing attempt ids; treating absence as mastery.

---

## 6. Experience projection mapping

Map into existing opaque `StudentTwinPort` shapes without UI redesign:

| Port method | Snapshot source |
|---|---|
| `get_learner_summary` | Identity + Goals + Knowledge coverage_summary + lifecycle |
| `get_readiness_summary` | PredictionFacet.readiness_snapshot (+ confidence limitations) |
| `get_learning_insights` | Behaviour / Performance / Knowledge structural insights with TraceRef |

When Authority ON and no active plan: return documented empty / null contracts (`NO_ACTIVE_PLAN`), never seeded demo readiness (~0.58 theatre).

---

## 7. Adaptive Engine attachment (optional)

When `ENABLE_DIGITAL_TWIN_ADAPTIVE_INPUT` is ON, Adaptive Assembler may attach:

| Attachment | Notes |
|---|---|
| `twin_snapshot_ref` | Fingerprint / `twin_id` + `as_of` |
| `behaviour` structural fields | Consume-only |
| `memory` structural fields | Consume-only |
| `predictions.readiness_snapshot` | Prefer same ReadinessService values already collected — Twin must not diverge |

Adaptive must still collect primary Runtime A inputs. Twin attachment failure → proceed without Twin + limitation code.

---

## 8. Identity mapping

| Twin concept | Canonical identity |
|---|---|
| Student | `User.id` / authenticated student_id |
| Topic | Curriculum topic_code (ADR-003 / ADR-004) |
| Session lineage | SQL `Mission.id` |
| Evidence | SQL `StudyAttempt.id` |
| Progress | TopicProgress scoped to user + topic_code |
| Twin snapshot | Deterministic hash of (`student_id`, `as_of`, `twin_version`, material serialize) optional |

---

## 9. Forbidden model elements (MS-004 Ready)

| Forbidden | Why |
|---|---|
| New Alembic tables for Twin | Out of Ready without ADR-MS004-002 |
| Twin-owned mastery write fields that replace TopicProgress | Dual truth |
| Embedding Adaptive decisions as Twin facts | Advice ≠ profile fact |
| Raw `events` / answer payloads in Experience Twin DTOs | Privacy + DP-006 |
| Cross-student cohort fields on student Twin | Governance |

---

## 10. Determinism

Identical Runtime A state + identical `as_of` + identical `twin_version` → identical `LearnerProfileSnapshot.serialize()` (material fields).  
Wall-clock latency telemetry is observational only and must not enter material fields.
