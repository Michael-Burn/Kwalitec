# MS-003 — Adaptive Decision Pipeline

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Related:** `ADAPTIVE_DATA_FLOW.md`, `ADAPTIVE_INTERFACE_SPECIFICATION.md`

---

## 1. Purpose

Define the complete decision flow from authoritative Runtime A state to Experience, with an explicit **no educational writes** boundary inside the Adaptive Engine.

---

## 2. End-to-end pipeline

```
Runtime A
   ↓  (authoritative educational state — facts)
Evidence
   ↓  (accepted attempts + progress signals + mission/readiness context)
Adaptive Engine
   ↓  (Adaptive Decision Record — advice only)
Recommendation
   ↓  (projection / narrative for surfaces — algorithms unchanged unless later ADR)
Experience
   ↓  (Home / Revision / explanation — existing UI)
(Student action → Runtime A write paths only — outside Engine)
```

### Pipeline invariant

| Stage | May read educational state? | May write educational state? |
|---|---|---|
| Runtime A services (authorised workflows) | Yes | Yes (Evidence Before Completion, Planning, plan wizard, …) |
| Evidence / snapshot assembly | Yes | **No** (read projection only) |
| Adaptive Engine | Yes (snapshot) | **No** |
| Recommendation projection | Yes | **No** (recompute narrative / map DTO only) |
| Experience presentation | Yes (DTOs) | **No** educational writes |
| Student Start / Complete / Plan edit | — | Yes, via Runtime A only |

---

## 3. Stages (detailed)

### Stage 0 — Trigger

| Trigger | Example | Notes |
|---|---|---|
| Home load | `get_todays_recommendation` | Primary Experience path |
| Revision load | Revision options / priorities | Lifecycle stage Revision |
| Shadow cron / dual-run | Shadow compare job | No UX change |
| Explicit refresh | Adaptive port refresh | Optional |

Triggers **request a decision**; they do not authorise educational mutation.

### Stage 1 — Runtime A authority check

1. Resolve `student_id` ownership.  
2. Confirm active StudyPlan (or document `NO_ACTIVE_PLAN`).  
3. Load lifecycle stage (`LearningLifecycleService`).  
4. Load today’s Mission if any (`MissionService`) — required for alignment policy.

**Failure:** `FORBIDDEN` / `NO_ACTIVE_PLAN` / `UNAVAILABLE` → Experience empty authentic or prior Recommendation Bridge behaviour per flag policy.

### Stage 2 — Evidence & input snapshot

Assemble `AdaptiveInputSnapshot` (see parent §5.2):

| Block | Source |
|---|---|
| Evidence | Accepted `StudyAttempt` / Evidence Authority read metadata |
| Topic Progress | TopicProgress rows (read) |
| Study Attempts | Bounded attempt history |
| Mission History | Missions (bounded) |
| Readiness | `ReadinessService` aggregates only |
| Curriculum | `CurriculumService` ordered leaves for active syllabus |
| Recommendations | `RecommendationService.generate_*` **read** snapshot (algorithms unchanged) |
| Student Goals | StudyPlan exam window, minutes, preferences |

**Stale-evidence policy:** each block carries `observed_at` / freshness; Engine records staleness in explanation confidence (see Risk Analysis).

### Stage 3 — Adaptive Engine decision

Logical steps (design — not implementation):

1. **Normalize** inputs onto curriculum spine (topic codes).  
2. **Detect stage policy** (Learning vs Revision).  
3. **Score candidates** (next topics / revision set) using deterministic rules/models registered by `rule_or_model_id`.  
4. **Apply constraints** (goals, workload, spacing, mission alignment).  
5. **Select primary + alternatives**.  
6. **Compute confidence**.  
7. **Build ExplanationBundle** (mandatory).  
8. Emit **AdaptiveDecisionRecord**.

**Forbidden in Stage 3:**

- `generate_today_mission` / mission create  
- TopicProgress updates  
- StudyAttempt inserts  
- Evidence acceptance  
- Plan field writes  
- Journey/History timeline fabrication as authority  

### Stage 4 — Recommendation projection

Map AdaptiveDecisionRecord → Experience AdaptiveDecisionPort / recommendation DTO:

| Condition | Projection rule |
|---|---|
| Mission exists | Primary label / topic **equals** mission topic (`mission_aligned=true`); Engine `next_topic` if different → alternative or advisory facet |
| No mission | Engine primary may populate recommendation; CTA still disabled per MS-001 when no plan/mission |
| Engine unavailable | Fall back to Recommendation Read Bridge (MS-001) — algorithms unchanged |
| Shadow mode | Experience continues prior path; Engine record telemetry only |

**Do not change RecommendationService algorithms** in MS-003 architecture implementation plan until a later ADR. Composition options:

- **A (preferred initially):** Engine wraps / enriches RecommendationService snapshot with confidence, alternatives, evidence refs.  
- **B (later):** RecommendationService accepts Engine outputs as additional **inputs** without rewriting existing rule bodies.  
- **C (explicit ADR only):** Engine becomes primary narrative producer.

### Stage 5 — Experience render

Existing Home recommendation card, explanation card, Revision options consume DTOs. **No UI redesign** in this milestone.

### Stage 6 — Student outcome (outside Engine)

Student acts (Start / practice / Complete). Writes flow through MS-001 bridges → Runtime A.  
Later outcomes link back for traceability (`ADAPTIVE_TRACEABILITY.md`) via `decision_id` + timestamps — **observational**, not Engine writes.

---

## 4. Sequence — Home recommendation (Adaptive Engine on)

```
UI (Home)
  → Experience (HomeService / AdaptiveDecisionPort)
    → AdaptiveEngineAdapter.decide(student_id, as_of)
      → assemble AdaptiveInputSnapshot (Runtime A reads)
      → Adaptive Engine compute
      → AdaptiveDecisionRecord + ExplanationBundle
    → project to recommendation DTO (mission alignment)
  → UI renders recommendation + explanation
```

### Sequence — Start Session (unchanged authority)

```
UI Start CTA
  → Mission Start Bridge (MS-001)
    → Planning / Mission Runtime A
  → SQL Mission (study identity)
```

Adaptive Engine is **not** on the Start write path.

### Sequence — Shadow mode

```
UI load (prior Recommendation Bridge path)
  ∥  AdaptiveEngineAdapter.decide (shadow)
       → telemetry SHADOW_COMPARE
       → discard for UX
```

---

## 5. Decision kinds

| Kind | Typical stage | Primary output |
|---|---|---|
| `NEXT_FOCUS` | Learning | `next_topic` |
| `REVISION_SET` | Revision | `revision_priority` |
| `INTENSITY` | Either | `study_intensity` |
| `WORKLOAD` | Either | `workload_balancing` |
| `SPACING` | Revision / review | `revision_spacing` |
| `COMPOSITE` | Home | Bundle of the above with one primary |

Each kind shares the same explainability contract.

---

## 6. Determinism

Given identical `AdaptiveInputSnapshot` (including `as_of` and registered model versions), the Engine must produce the same material outputs (primary topic, ranked alternatives, confidence band, rule_or_model_ids) — DP-012.

Non-determinism (random exploration, generative LLM cores) is **forbidden** in the educational decision centre. Assistive narrative phrasing may vary only if it does not change material conclusions; prefer fixed templates from `EducationalExplainabilityService`.

---

## 7. Failure & degradation

| Condition | Behaviour |
|---|---|
| No plan | Empty decision / `NO_ACTIVE_PLAN`; no fabricated next topic |
| Sparse evidence | Decision allowed with **low confidence** + explicit evidence paucity in explanation |
| Readiness unavailable | Omit readiness-dependent facets; lower confidence; never invent readiness |
| RecommendationService failure | Mission-only alignment if mission exists (`fallback_used`); else empty |
| Engine exception | Flag path falls back to Recommendation Bridge; telemetry FAILURE |

---

## 8. Acceptance checks (pipeline)

| ID | Check |
|---|---|
| P-1 | Engine stage issues zero educational writes in call graph |
| P-2 | Mission-aligned projection when mission exists |
| P-3 | Shadow mode never changes Experience DTO |
| P-4 | Same snapshot → same material decision (fixture replay) |
| P-5 | ExplanationBundle present on every successful decision |
