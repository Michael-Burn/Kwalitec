# MS-003 — Adaptive Data Flow

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Related:** `ADAPTIVE_DECISION_PIPELINE.md`, `ADAPTIVE_INTERFACE_SPECIFICATION.md`

---

## 1. Purpose

Document how data moves into and out of the Adaptive Learning Engine — **read paths only** into the Engine; **advice DTOs only** out.

---

## 2. Data flow diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ RUNTIME A (authoritative educational facts)                     │
│                                                                 │
│  Curriculum JSON ──► CurriculumService                          │
│  StudyPlan ────────► StudyPlanService / Goals                   │
│  Mission ──────────► MissionService                             │
│  StudyAttempt ─────► Evidence Authority (accept) + session svc  │
│  TopicProgress ────► AdaptiveLearningService (write elsewhere)  │
│  Aggregates ───────► ReadinessService                           │
│  Narrative rules ──► RecommendationService (unchanged algos)    │
│  Stage ────────────► LearningLifecycleService                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │ READ snapshots only
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ ADAPTIVE INPUT ASSEMBLER (infrastructure / adapter)             │
│  AdaptiveInputSnapshot { evidence, progress, attempts,          │
│    missions, readiness, curriculum, recommendations, goals }    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ ADAPTIVE LEARNING ENGINE                                        │
│  pure decision computation                                      │
│  FORBIDDEN: SQL educational writes                              │
└───────────────────────────────┬─────────────────────────────────┘
                                │ AdaptiveDecisionRecord
                                │ + ExplanationBundle
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ RECOMMENDATION / EXPERIENCE PROJECTION                          │
│  AdaptiveDecisionPort DTO · mission alignment · explanation     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ EXPERIENCE UI (existing templates — no redesign)                │
│  Home recommendation · explanation · Revision                   │
└─────────────────────────────────────────────────────────────────┘

Student action (Start / Complete / Plan edit)
  ──► MS-001 bridges / Runtime A WRITE paths
  ──► NEW evidence / progress / missions
  ──► next AdaptiveInputSnapshot (later request)
```

**Closed loop note:** Outcomes re-enter as **inputs** on a later request. That is a **product feedback loop** (see `RISK_ANALYSIS_MS003.md`). The Engine still never writes; Runtime A authorised workflows do.

---

## 3. Per-input flow

| Input | Origin store / API | Assembler transform | Engine use |
|---|---|---|---|
| Evidence | StudyAttempt + acceptance metadata | Summarise accepted/rejected; link mission ids | Ground mastery claims; confidence |
| Topic Progress | TopicProgress | Map topic_code → mastery/coverage/last_seen | Candidate scoring; weak-topic set |
| Study Attempts | StudyAttempt | Bound by recency/count; strip PII-irrelevant fields | Intensity, spacing, confidence |
| Mission History | Mission | Bound list; status + topic + date | Continuity; avoid thrashing; alignment |
| Readiness | ReadinessService | Pass-through aggregates | Workload / backlog signals |
| Curriculum | CurriculumService | Ordered leaves for active plan syllabus | Candidate universe; DP-011 |
| Recommendations | RecommendationService | Snapshot categories/labels/explanations | Composition / shadow compare |
| Student Goals | StudyPlan + prefs | Exam date, minutes, stage flags | Constraints on intensity/workload |

### Ownership tag on every block

```
authority: "readiness_service" | "recommendation_service" | "mission_service" | …
observed_at: <timestamp>
```

Assembler must not recompute readiness with a private formula.

---

## 4. Per-output flow

| Output | Produced by Engine | Leaves system as | Downstream write? |
|---|---|---|---|
| next_topic | Yes | AdaptiveDecisionRecord / recommendation DTO | No (advice) |
| revision_priority | Yes | Revision DTO facets | No |
| confidence_score | Yes | DTO + telemetry | No |
| study_intensity | Yes | Optional advice facet | No |
| workload_balancing | Yes | Optional advice facet | No |
| revision_spacing | Yes | Optional advice facet | No |
| alternatives | Yes | Explanation / DTO | No |
| explanation | Yes | ExplanationBundle | No |
| decision_id | Yes | Trace + telemetry | Optional audit DTO store later (ADR-MS003-002) — still not educational SoT |

---

## 5. Optional continuity reads

| Source | Flow | Constraint |
|---|---|---|
| JourneyBridge projection | May supply timeline context | Read-only; prefer primary SQL services for scoring |
| HistoryBridge projection | May supply session narrative | Read-only; do not treat demo Twin as authority |

When Journey/History flags are off, Engine must still function from primary Runtime A services.

---

## 6. Caching (design policy)

| Cache | Allowed? | Rules |
|---|---|---|
| Short-lived AdaptiveDecisionRecord in Experience projection store | Yes | Tagged `authority=adaptive_engine`; TTL; never invent if miss |
| Durable educational facts in Engine | **No** | Facts stay in Runtime A |
| Demo seed adaptive documents | **No** when `ENABLE_ADAPTIVE_ENGINE` on | Empty authentic / Recommendation Bridge fallback |

---

## 7. Boundary violations (forbidden flows)

```
Adaptive Engine ──✗──► TopicProgress.write
Adaptive Engine ──✗──► StudyAttempt.insert
Adaptive Engine ──✗──► Mission.create / ensure
Adaptive Engine ──✗──► Evidence.accept
Adaptive Engine ──✗──► StudyPlan.mutate
Adaptive Engine ──✗──► Journey/History invent events
Experience ──────✗──► treat AdaptiveDecisionRecord as mastery fact
```

---

## 8. Volume & performance (design)

| Concern | Guidance |
|---|---|
| Attempt / mission history bounds | Hard caps (e.g. last N missions / M days) — exact N in implementation ADR |
| Curriculum traversal | Use CurriculumService helpers; do not load full unrelated syllabi |
| Home path latency | Prefer parallel reads; budget comparable to Recommendation Bridge |
| Shadow mode | Async or sampled if latency risk; never block Start |

Full risk: `RISK_ANALYSIS_MS003.md` § performance.

---

## 9. Acceptance checks (data flow)

| ID | Check |
|---|---|
| DF-1 | Every AdaptiveInputSnapshot block carries authority tag |
| DF-2 | Engine outputs never appear as SQL educational writes in the same request |
| DF-3 | Mission topic remains Start authority; Adaptive next_topic does not create missions |
| DF-4 | When Engine flag on, `seeded_demo_adaptive` is not authority |
