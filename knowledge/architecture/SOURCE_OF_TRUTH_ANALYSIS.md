# MS-001 — Source of Truth Analysis

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)  
**Verdict:** There is **no single source of truth** across the live student journey today. The legacy SQL stack is internally coherent; the canonical Experience stack is architecturally clean but **not bridged** to that SQL truth under default flags.

---

## 1. Ownership matrix

| Concept | Authoritative store (legacy) | Authoritative store (canonical) | Single SoT? | Duplication |
|---|---|---|---|---|
| **Active study session** | `Mission.status` ∈ {Pending, In Progress, Completed} (`app/models/mission.py`) | `ExperienceProjectionStore` `todays_session` + `SessionWorkspace` (`ACTIVE`/`PAUSED`/`CLOSED`, `active_surface`) | **No** | Three+ independent representations; no FK between them |
| **Current mission** | SQL `missions` row scoped by `user_id`, `mission_date`, `study_plan_id` | Opaque `mission_id` strings (demo `"m1"` or UUID-like) in projection docs | **No** | Unrelated ID spaces |
| **Today’s recommendation** | Computed: `RecommendationService.generate_today_recommendation` (and independently mission topic via `PlanningService`) | Opaque Adaptive projection / `AdaptiveDecisionPort.get_todays_recommendation` (demo-seeded) | **No** | Legacy already has **two** independent “next” computations; canonical is a third |
| **Progress** | `TopicProgress` (+ `StudyAttempt`), evidence-gated updates via `EducationalEvidenceAuthority` / `AdaptiveLearningService` | Twin/Journey opaque projections (demo-seeded; not reading TopicProgress by default) | **Partial** (legacy only) | Canonical surfaces do not share TopicProgress |
| **Learning state (lifecycle)** | `LearningLifecycleService.resolve` over syllabus-leaf completion + plan fields (`revision_*` on StudyPlan) | Not the same service; Twin readiness labels in opaque docs | **No** across stacks | Legacy lifecycle is SoT for legacy UI only |
| **Navigation state** | Implicit: URL + Mission.status; sidebar from `SOLE_RUNTIME` | `SessionWorkspace.active_surface` + student surface from route; sidebar from flag | **No** | Flag chooses tree; workspace chooses session step — orthogonal |

---

## 2. Detailed ownership

### 2.1 Active study session

**Legacy writes**

- `StudySessionService.start_session` / `finish_session`
- `MissionService.update_mission_status` / `complete_mission` / `mark_task_complete` (may flip to In Progress)

**Canonical writes**

- `ExperienceMissionAdapter.start_session` / `complete_session`
- `SessionExperienceService` / runtime adapter mutating `SessionWorkspace`
- Optional Learning Orchestrator mission adapter (separate in-memory aggregate) on learning-loop hooks

**Flask session:** does not hold active session pointer.  
**Browser storage:** legacy timer keys only (`study_session.js`).

### 2.2 Current mission

**Legacy SoT:** `Mission` ORM + `MissionService.get_today_mission(..., study_plan_id=…)`.

**Canonical SoT (as wired):** opaque document field `todays_session.mission_id`, provisioned by `seeded_demo_mission` / start_session — **does not load SQL Mission** when `mission_engine` is `None` (default `build_default_opaque_engines` leaves real mission engine unset).

### 2.3 Today’s recommendation

| Producer | Consumer | Selects today’s Mission topic? |
|---|---|---|
| `PlanningService.generate_today_mission` | Mission hub, dashboard mission card | **Yes** (creates Mission) |
| `RecommendationService.generate_*` | Dashboard recommendation widget | **No** |
| EI Educational Orchestrator (flagged) | Dashboard card when enabled | Overlay / suppress legacy rec card |
| `AdaptiveDecisionPort` + demo adaptive seed | Student Home / Revision | Drives Home CTA copy; demo by default |
| `AdaptiveDecisionEngine` (Phase I) | Only if injected with real inputs | Present in codebase; not fed real DB twin/journey in default composition |

### 2.4 Progress / learning state

**Legacy SoT for mastery:** `TopicProgress` updated through Evidence Authority after practice outcome capture.

**Canonical:** `learner_summary` / `readiness_summary` / journey progress from Twin/Journey ports — default demo values (`readiness ~0.58`, fabricated topics).

**Learning lifecycle stage (Learning vs Revision):** `LearningLifecycleService` — shared by legacy dashboard/mission/recommendation/planning. Not consumed by Student Experience Home by default.

### 2.5 Navigation state

| Concern | Owner |
|---|---|
| Which product shell (legacy vs OS) | `KWALITEC_V2_SOLE_RUNTIME` |
| Which student surface (Home/Journey/…) | URL / `ExperienceSurface` |
| Which session step | `SessionWorkspace.active_surface` |
| Wizard progress | Flask `session["wizard_data"]` |

---

## 3. Duplication catalogue

1. **Dual presentation stacks** for the same product intent (“start studying”).  
2. **Dual “next” engines on legacy:** Planning (mission) vs Recommendation (card).  
3. **Dual topic sequencing algorithms:** `get_next_incomplete_topic` (daily) vs Kahn topological `_resolve_curriculum_sequence` (week-plan scaffolding).  
4. **Triple adaptive/decision systems:** `AdaptiveLearningService` (legacy mastery), `RecommendationService` (rules), `AdaptiveDecisionEngine` (V2 domain, unwired inputs).  
5. **Mission engines V1/V2 packages** under `app/application/mission_engine*` — built but **not imported** by live routes/composition (dead from request path).  
6. **Multiple persistence planes:** SQL educational tables vs opaque V2 aggregate JSON vs in-memory session docs vs orchestrator evidence store.  
7. **Topic label formatting** private on `PlanningService`, reached from Recommendation and LearningLifecycle (coupling duplicate).

---

## 4. Flag impact on truth

| Flag | Default | Effect on SoT |
|---|---|---|
| `KWALITEC_V2_SOLE_RUNTIME` | false | Switches **presentation** entry; does not merge data stores |
| `KWALITEC_V2_DURABLE_STORE` / `ENABLE_DURABLE_STORE` | false | Opaque docs survive process if on; still not SQL Mission |
| `KWALITEC_V2_INJECT_ENGINES` / `INJECT_PHASE_I_ENGINES` | false | Empty engines dict when false; when true still no real twin/mission/journey engine instances |
| `SEED_DEMO_LEARNERS` | true | Fabricated Home/Session content on ensure_learner |

---

## 5. Answers required by MS-001

| Question | Answer |
|---|---|
| Is there a single source of truth? | **No.** |
| Closest ground truth for real learning? | Legacy SQL: `StudyPlan` + `Mission` + `TopicProgress` + Evidence Authority, driven by `PlanningService` / `StudySessionService` / `AdaptiveLearningService`. |
| What Home shows under sole runtime today (default wiring)? | Demo-seeded opaque projections unless bridging adapters are added and engines injected with real data. |
| Where duplication hurts most? | Sole-runtime cutover without a bridge: students leave real missions for fabricated “Core methods” sessions. |

---

## 6. Implications for Foundational Trust

Foundational Trust (MS-001) cannot be claimed for navigation until **one** of the following is true and verified:

1. Canonical ports read/write the legacy SQL educational records (bridge adapters), or  
2. Canonical engines become the sole writers and legacy shells are retired **after** data migration, or  
3. Sole runtime remains off until (1) or (2) ships.

This document records the as-built state only; it does not prescribe the product choice.
