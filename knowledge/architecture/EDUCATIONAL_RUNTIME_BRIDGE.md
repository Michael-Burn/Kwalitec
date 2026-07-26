# MS-001 Engineering Directive 002 / 003 / 004 / 005 / 006 / 007 — Educational Runtime Bridge

**Milestone:** MS-001 — Foundational Trust  
**Directives:** Engineering Directive 002 (Architecture Design); Engineering Directive 003 (Mission Read Adapter); Engineering Directive 004 (Mission Start Bridge); Engineering Directive 005 (Mission Resume Bridge); Engineering Directive 006 (Session Completion Bridge); Engineering Directive 007 (Recommendation Read Bridge)  
**Status:** Architecture Design complete; **Mission Read Adapter — Implemented**; **Mission Start Bridge — Implemented**; **Mission Resume Bridge — Implemented**; **Session Completion Bridge — Implemented**; **Recommendation Read Bridge — Implemented**  
**Companions:** `BRIDGE_INTERFACE_SPECIFICATION.md`, `BRIDGE_SEQUENCE_DIAGRAM.md`, `MIGRATION_PLAN.md`, `ROLLBACK_PLAN.md`, `RISK_ANALYSIS.md`, `TEST_STRATEGY.md`  
**Prior investigation:** `SOURCE_OF_TRUTH_ANALYSIS.md`, `NAVIGATION_AUDIT.md`, `SERVICE_DEPENDENCY_MAP.md`, `REFACTORING_RECOMMENDATIONS.md`

---

## Implementation status (Directives 003 / 004 / 005 / 006 / 007)

| Component | Status | Notes |
|---|---|---|
| **Mission Read Adapter** (`PlanningBridge` read) | **Implemented** | `app/infrastructure/adapters/educational_runtime_bridge/` |
| **Mission Start Bridge** (ensure today + start) | **Implemented** | Same package; write-path translator |
| **Mission Resume Bridge** (active session continuity) | **Implemented** | Same package; continuity translator |
| **Session Completion Bridge** (Evidence Before Completion) | **Implemented** | Same package; completion + evidence translator |
| **Recommendation Adapter** (`RecommendationBridge` read) | **Implemented** | Same package; educational intelligence read translator |
| Journey / History / Revision bridges | Journey **Implemented** (MS-002 J1); History / Revision not started | — |

### Bridge Coverage

| Bridge | Status |
|---|---|
| Mission Read | **Implemented** |
| Mission Start | **Implemented** |
| Mission Resume | **Implemented** |
| Session Completion | **Implemented** |
| Recommendation | **Implemented** |
| Journey | **Implemented** |
| History | Not started |

### Mission Read Adapter — implementation notes

- **Flag:** `KWALITEC_MISSION_READ_BRIDGE` (alias: `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_MISSION_READ_BRIDGE` (default **off**).
- **Path:** Experience `MissionPort.get_todays_session` → `ExperienceMissionAdapter` → `MissionReadAdapter` → `MissionService.get_today_mission` → SQL `Mission`.
- **Translator only:** maps Mission (+ optional lifecycle / preferred minutes) to opaque `todays_session`; does **not** call `generate_today_mission`, start, complete, or invent topics.
- **No demo fallback:** when the bridge is on and Runtime A has no mission, returns the documented empty contract (`BridgeResult` with `NO_ACTIVE_PLAN` / `OUTSIDE_PLAN_WINDOW` / `NOT_FOUND`); never `seeded_demo_mission`.
- **Rollback:** disable the flag — prior Experience / seed behaviour restored immediately.
- **Telemetry (observational):** `MISSION_BRIDGE_REQUESTED`, `MISSION_BRIDGE_SUCCESS`, `MISSION_BRIDGE_FAILURE`, `MISSION_BRIDGE_LATENCY`.
- **Tests:** `tests/infrastructure/adapters/educational_runtime_bridge/` (unit, integration, contract).

### Mission Start Bridge — implementation notes

- **Flag:** `KWALITEC_MISSION_START_BRIDGE` (also enabled by umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_MISSION_START_BRIDGE` (default **off**).
- **Path:** Experience `MissionPort.start_session` → `ExperienceMissionAdapter` → `MissionStartAdapter` → `PlanningService.generate_today_mission` (ensure) + `StudySessionService.start_session` → SQL `Mission`.
- **Translator only:** does not choose topics, calculate recommendations, or create fallback / demo sessions.
- **No demo educational state:** when the bridge is on, Start never uses `seeded_demo_mission` / opaque invent; absence / ownership / completed-state map to documented `BridgeResult` codes (`NO_ACTIVE_PLAN`, `FORBIDDEN`, `INVALID_STATE`, …).
- **Rollback:** disable the flag — prior Experience opaque start restored immediately.
- **Telemetry (observational):** `MISSION_START_BRIDGE_REQUESTED`, `MISSION_START_BRIDGE_SUCCESS`, `MISSION_START_BRIDGE_FAILURE`, `MISSION_START_BRIDGE_LATENCY`.
- **Tests:** unit, integration, contract, and behavioural parity vs legacy Planning + StudySession start.

### Mission Resume Bridge — implementation notes

- **Flag:** `KWALITEC_MISSION_RESUME_BRIDGE` (also enabled by umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_MISSION_RESUME_BRIDGE` (default **off**).
- **Path:** Experience `resume_session` / `get_session_status` → `ExperienceMissionAdapter` → `MissionResumeAdapter` → `StudySessionService.get_owned_mission` (or `MissionService.get_today_mission` to locate) → SQL `Mission`.
- **Translator only:** locates an existing **In Progress** session, validates continuity, and projects canonical educational state. Does **not** generate missions, call `start_session`, or invent educational state.
- **Lifecycle invariants preserved:** student identity, mission identity, session identity, learning/progress state (tasks + status), educational continuity. If any invariant cannot be preserved → documented `BridgeResult` failure (`FORBIDDEN`, `INVALID_STATE`, `NOT_FOUND`, …). **Never** silently creates a replacement session.
- **No demo educational state:** when the bridge is on, Resume never uses `seeded_demo_mission`; Pending / Completed map to `INVALID_STATE`.
- **Rollback:** disable the flag — prior Experience opaque / store resume restored immediately.
- **Telemetry (observational):** `MISSION_RESUME_BRIDGE_REQUESTED`, `MISSION_RESUME_BRIDGE_SUCCESS`, `MISSION_RESUME_BRIDGE_FAILURE`, `MISSION_RESUME_BRIDGE_LATENCY`.
- **Tests:** unit, integration, contract, and behavioural parity vs legacy StudySession ownership + In Progress continuity.

### Session Completion Bridge — implementation notes

- **Flag:** `KWALITEC_SESSION_COMPLETION_BRIDGE` (also enabled by umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_SESSION_COMPLETION_BRIDGE` (default **off**).
- **Path:** Experience `complete_session` → `ExperienceMissionAdapter` → `SessionCompletionAdapter` → `StudySessionService` / `LearningService` / `MissionService` → Evidence Authority → SQL `Mission` (+ `StudyAttempt`).
- **Evidence Before Completion (binding):** Validate session → Commit educational evidence → Mark session complete → Return canonical educational state. If evidence cannot be committed: session remains **In Progress**, completion fails cleanly (`EVIDENCE_REJECTED` / `INVALID_STATE`), and no partial educational completion is recorded.
- **Translator only:** does not generate recommendations, alter learning algorithms, invent completion state, or bypass evidence recording.
- **Lifecycle invariants preserved:** student identity, mission identity, session identity, learning/progress state, evidence integrity.
- **No demo educational state:** when the bridge is on, Completion never uses `seeded_demo_mission`; Pending / already-Completed map to `INVALID_STATE`.
- **Learning-loop guard:** when the completion bridge is wired, the post-start learning loop does **not** auto-complete the SQL session (would violate Evidence Before Completion).
- **Rollback:** disable the flag — prior Experience opaque complete restored immediately.
- **Telemetry (observational):** `SESSION_COMPLETION_BRIDGE_REQUESTED`, `SESSION_COMPLETION_BRIDGE_SUCCESS`, `SESSION_COMPLETION_BRIDGE_FAILURE`, `SESSION_COMPLETION_BRIDGE_LATENCY`.
- **Tests:** unit, integration, contract, behavioural parity vs legacy finish, and failure-path tests proving evidence failures leave the session active.

### Recommendation Read Bridge — implementation notes

- **Flag:** `KWALITEC_RECOMMENDATION_BRIDGE` (also enabled by umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_RECOMMENDATION_BRIDGE` (default **off**).
- **Path:** Experience `AdaptiveDecisionPort.get_todays_recommendation` → `ExperienceAdaptiveAdapter` → `RecommendationAdapter` → `RecommendationService.generate_recommendations` (+ `MissionService.get_today_mission` for alignment) → Learning State / Evidence-backed progress → SQL.
- **Translator only:** retrieves canonical Runtime A recommendations and projects DTOs; does **not** calculate recommendations in the adapter, alter learning state, modify evidence, call `record_decision`, or cache authoritative educational state.
- **Mission alignment (dual-“next” rule §5.3):** when a SQL Mission exists, primary `topic_title` / `recommendation_label` equal the mission title (`mission_aligned=true`); `RecommendationService` narrative supplies explanation / alternatives without contradicting the mission topic. Curriculum traversal remains V1/V2 compatible ([ADR-003](ADR-003-curriculum-v1-v2.md)).
- **No demo educational state:** when the bridge is on, Recommendation never uses `seeded_demo_adaptive`; empty Runtime A → documented empty contract (`NOT_FOUND`); RecommendationService failure with mission → mission-only label (`fallback_used=true`).
- **Rollback:** disable the flag — prior Experience opaque / seed adaptive behaviour restored immediately.
- **Telemetry (observational):** `RECOMMENDATION_BRIDGE_REQUESTED`, `RECOMMENDATION_BRIDGE_SUCCESS`, `RECOMMENDATION_BRIDGE_FAILURE`, `RECOMMENDATION_BRIDGE_LATENCY`.
- **Tests:** unit, integration, contract, and behavioural parity vs legacy `RecommendationService` (+ mission alignment).

---

## 1. Purpose

Design an **Educational Runtime Bridge** so the Experience application (Student Home, Session, Journey, Revision, History, Profile) consumes **one authoritative educational runtime** without changing educational behaviour.

Directive 002 documented architecture only. Directive 003 implements the first bridge component (Mission Read). Directive 004 implements the first write-path component (Mission Start). Directive 005 implements the continuity component (Mission Resume). Directive 006 implements Session Completion with Evidence Before Completion. Directive 007 implements the first educational intelligence bridge (Recommendation Read).

---

## 2. Problem statement

Kwalitec currently runs two independent educational runtimes:

| Runtime | Surface | Educational truth |
|---|---|---|
| **Runtime A — Legacy SQL** | Dashboard, Missions, Analytics | `StudyPlan` + `Mission` + `TopicProgress` via `PlanningService`, `StudySessionService`, Evidence Authority |
| **Runtime B — Experience** | Student Home, Session shell | Opaque projections (`seeded_demo_*` by default); ports do not read SQL educational records |

`KWALITEC_V2_SOLE_RUNTIME` switches **chrome and entry routes** only. It does not unify educational state.

This violates the Product / Educational Constitution principle that every educational decision must originate from **one** authoritative runtime.

---

## 3. Architectural decision (summary)

**Decision:** The Bridge makes **Runtime A (legacy SQL educational services)** the authoritative educational core for Experience consumption.

**Rationale:**

1. Investigation (`SOURCE_OF_TRUTH_ANALYSIS.md`) established legacy SQL as the closest ground truth for real learning.
2. Experience facades already refuse educational ownership (projection-only) — the correct seam for bridging.
3. Wiring Experience → SQL preserves deterministic planning, Evidence-gated mastery, and CurriculumService traversal without a data migration.
4. Unwired packages (`MissionEngine*`, underfed `AdaptiveDecisionEngine`) are **not** promoted to authority in this directive.

**Non-decision (deferred):** Replacing SQL services with V2 domain engines as sole writers. That is a later programme after Bridge Complete and evidence parity.

**ADR:** See §12 (Architecture Decision Record).

---

## 4. Bridge placement

```
Templates / JS
      ↓
Presentation (student / session blueprints)
      ↓
Application facades (StudentExperienceService, SessionExperienceService, …)
      ↓
Experience Ports (MissionPort, AdaptiveDecisionPort, TwinPort, JourneyPort, …)
      ↓
╔══════════════════════════════════════════╗
║  EDUCATIONAL RUNTIME BRIDGE (new seam)   ║
║  Bridging adapters + DTO projection      ║
╚══════════════════════════════════════════╝
      ↓
Canonical Educational Services (Runtime A)
      ↓
SQL models / Curriculum Engine / Evidence Authority
```

**Invariants:**

- Experience facades **never** import `app/services/*` directly.
- Legacy services **never** import Experience facades.
- Bridge adapters own translation, ownership checks, fallbacks, and telemetry.
- Educational law (topic selection, mastery updates, evidence gates) remains inside Runtime A services.

---

## 5. Canonical educational services

### 5.1 Authority matrix

| Service / component | Role | Bridge status | Rationale |
|---|---|---|---|
| **`CurriculumService`** (+ Curriculum Engine JSON) | Topic order, leaf traversal, official structure | **Authoritative — retained** | ADR-004; both V1/V2 curricula must remain traversable |
| **`StudyPlanService`** | Active plan, wizard persistence, week scaffolding | **Authoritative — retained** | Plan is prerequisite for mission generation |
| **`PlanningService`** | Creates today’s Mission (topic + tasks) | **Authoritative for “what to study today” (mission)** | Sole producer of SQL Mission topic under legacy path |
| **`MissionService`** | Mission / MissionTask CRUD and status | **Authoritative for mission records** | SQL `missions` is session of record for study identity |
| **`StudySessionService`** | Start / finish / practice outcome / feedback | **Authoritative for session write lifecycle** | Evidence-gated completion path lives here |
| **`LearningLifecycleService`** | Learning vs Revision stage | **Authoritative for lifecycle stage** | Gates Planning + Recommendation behaviour |
| **`RecommendationService`** (`app/services`) | Explainable “next” card / narrative | **Authoritative for recommendation narrative** (policy: see §5.3) | Deterministic, explainable; already SQL-backed |
| **`ReadinessService`** | Coverage, backlog, readiness aggregates | **Authoritative for readiness aggregates** | Twin projections must derive from this (or TopicProgress via Adaptive) |
| **`AdaptiveLearningService`** | Mastery, weak topics, review schedule | **Authoritative for mastery / TopicProgress updates** | Paired with Evidence Authority |
| **`EducationalEvidenceAuthority`** | Gates mastery writes | **Authoritative integrity gate — retained** | Non-negotiable for educational integrity |
| **`EducationalExplainabilityService`** | Narratives for UI | **Retained** as explanation source for bridged Adaptive/Home | Experience ExplanationService may wrap outputs |
| **`EducationalContinuityService`** | History protection across plan changes | **Retained** | Continuity across plan edits |

### 5.2 Deprecated for educational authority (presentation / demo / unwired)

| Component | Status | Notes |
|---|---|---|
| **`seeded_demo_*` projections** | **Deprecated for non-demo paths** | Allowed only behind explicit demo/seed flags for empty-state demos; never authority under Bridge |
| **`ExperienceProjectionStore` as educational SoT** | **Demoted to cache / UX projection** | May hold bridged DTOs; must not invent topics or mastery |
| **`MissionOpaqueBridge` / empty `MissionOpaqueBridge.start_opaque` defaults** | **Transitional only** | Replaced by SQL-backed Mission bridge; fabricated `"Core methods"` topics forbidden when bridged |
| **`app/application/mission_engine*`** | **Not authoritative** | Built but unwired; archive or wire in a later ADR — not Bridge authority |
| **`AdaptiveDecisionEngine` (default wiring)** | **Not authoritative until SQL-fed** | May later consume Twin derived from SQL; until then RecommendationService + Planning own “next” |
| **`LearningOrchestrator` independent evidence store** | **Not authoritative for mastery** | May emit events; mastery writes go through Evidence Authority |
| **`SessionWorkspace` as educational SoT** | **UX resume only** | Authoritative for linear step resume; not for mission topic or mastery |
| **Flask `session` / browser localStorage** | **Not educational SoT** | Timer UX only on legacy |

### 5.3 Dual “next” policy (explicit product rule for Bridge)

Legacy already has two producers:

1. **Mission topic** — `PlanningService.generate_today_mission`
2. **Recommendation card** — `RecommendationService.generate_today_recommendation`

**Bridge rule (Foundational Trust):**

| Concern | Authority |
|---|---|
| **What the student studies when they Start Session** | `PlanningService` → SQL `Mission` |
| **What Home shows as recommendation label / explanation** | Prefer **alignment**: Adaptive/Home recommendation **projects the same mission topic** (and Planning/Lifecycle stage). `RecommendationService` may supply secondary narrative / alternatives, but must not contradict the active mission topic when a mission exists. |
| **When no mission exists** (no plan / outside window) | Home CTA disabled; recommendation may explain “create/activate plan” — no fabricated mission |

This collapses the product-visible contradiction without deleting `RecommendationService`.

---

## 6. Experience consumption map

For every Experience page: **current data source → future (bridged) data source**.

### 6.1 Student Home (`student.home`)

| Concern | Current | Future (Bridge) |
|---|---|---|
| Today’s session / CTA | `seeded_demo_mission` → MissionPort | **Planning + Mission bridge** → MissionPort (`get_todays_session`) — **Mission Read Adapter implemented** |
| Primary recommendation | `seeded_demo_adaptive` → AdaptiveDecisionPort | **Recommendation Read Bridge** → AdaptiveDecisionPort (`get_todays_recommendation`) — **Implemented** (mission-aligned + RecommendationService narrative) |
| Readiness | Demo Twin readiness labels | **ReadinessService / TopicProgress → TwinPort** |
| Journey snippet | `seeded_demo_journey` | **Twin + Lifecycle + StudyPlan → JourneyPort** |
| History snippet | Twin/History opaque | **StudyAttempt / Mission history + Readiness progression → History projection** |
| Explanation | Demo explanation blobs | **EducationalExplainabilityService** (or Planning label helpers via public API) |

### 6.2 Journey (`student.journey`)

| Concern | Current | Future |
|---|---|---|
| Progress / milestones | `seeded_demo_journey` | StudyPlan coverage + TopicProgress + Lifecycle stage via Journey bridge |

### 6.3 Revision (`student.revision`)

| Concern | Current | Future |
|---|---|---|
| Revision options | Demo adaptive / journey | `LearningLifecycleService` (Revision stage) + `AdaptiveLearningService` weak topics + Planning revision templates |
| Begin CTA | Same start path as Home (demo mission) | Same **Start Session bridge** as Home (SQL Mission) |

### 6.4 History (`student.history`)

| Concern | Current | Future |
|---|---|---|
| Activity / readiness progression | Opaque / demo | Mission completion history, StudyAttempt, ReadinessService time series |

### 6.5 Profile (`student.profile`)

| Concern | Current | Future |
|---|---|---|
| Preferences / identity | Mostly user/settings | Unchanged (identity); exam/plan summary from **StudyPlanService** |

### 6.6 Session Overview / Activity / Reflection / Summary / Complete

| Concern | Current | Future |
|---|---|---|
| Session identity | Opaque `session_id` / `experience_session_id` | Bridge maps to SQL `Mission.id` (+ stable experience session id for UI) |
| Objective / topics | Demo mission doc | Mission + MissionTask from SQL |
| Begin / advance | SessionWorkspace + Activity port (demo activity) | Workspace remains UX; **Start** via Mission Start Bridge → SQL Mission; activity content from bridged mission tasks / LearningService where available |
| Complete / mastery | Opaque complete; **no TopicProgress write by default** | **Session Completion Bridge** → `StudySessionService` + Evidence Authority (Evidence Before Completion) |
| Resume surface | `SessionWorkspace.active_surface` | Unchanged as UX resume; must load only if Mission ownership valid |

### 6.7 Shared / indirect surfaces (not Experience pages, but Bridge-affected)

| Surface | Current | Future |
|---|---|---|
| Root `/` under `SOLE_RUNTIME` | Chrome → Home (demo truth) | Chrome → Home (**bridged truth**) |
| Study Plan / Calibration | Runtime A (correct) | Unchanged; Bridge reads resulting plan |
| Legacy Dashboard / Missions | Runtime A | Remain until sole-runtime retirement; under Bridge they stay SQL-authoritative |

---

## 7. Bridge interface catalogue (index)

Full contracts: `BRIDGE_INTERFACE_SPECIFICATION.md`.

| Interface | Owns | Maps Runtime A | Implementation |
|---|---|---|---|
| `PlanningBridge` (read) | Today’s mission projection | `MissionService` (+ plan/lifecycle reads) | **`MissionReadAdapter` — Implemented** |
| `PlanningBridge` (ensure) | ensure-today generate | `PlanningService` | **`MissionStartAdapter` (ensure leg) — Implemented** |
| `MissionLifecycleBridge` | Start / status / complete | `StudySessionService`, `MissionService` | **Start via `MissionStartAdapter` — Implemented**; **Resume via `MissionResumeAdapter` — Implemented**; **Complete via `SessionCompletionAdapter` — Implemented** |
| `RecommendationBridge` | Home recommendation DTO | Mission alignment + `RecommendationService` | **`RecommendationAdapter` — Implemented** |
| `LearningStateBridge` | Twin / readiness / lifecycle labels | `ReadinessService`, `TopicProgress`, `LearningLifecycleService` | Not started |
| `JourneyBridge` | Journey snapshot | StudyPlan + TopicProgress + Lifecycle | **Implemented** (MS-002 J1) |
| `HistoryBridge` | History snapshot | Missions / attempts / readiness progression | **Implemented** (MS-002 J2) |
| `EvidenceParityBridge` | Practice outcome → mastery | `StudySessionService` + Evidence Authority | **Embedded in `SessionCompletionAdapter` (Evidence Before Completion) — Implemented** |

Ports remain Experience-facing (`MissionPort`, etc.). Bridges implement or back those ports.

---

## 8. Sequence flows (index)

Full diagrams: `BRIDGE_SEQUENCE_DIAGRAM.md`.

1. Start Study — **Mission Start Bridge implemented**  
2. Resume Study — **Mission Resume Bridge implemented**  
3. Load Dashboard (Student Home) — **mission read leg implemented**  
4. Complete Session — **Session Completion Bridge implemented** (Evidence Before Completion)  
5. Recommendation Request — **Recommendation Read Bridge implemented**

Layer order in every diagram: **UI → Experience Layer → Bridge → Educational Services → Database**.

---

## 9. Migration strategy (index)

Full plan: `MIGRATION_PLAN.md`. Rollback: `ROLLBACK_PLAN.md`.

Principles:

- Incremental, independently releasable phases  
- Each phase has rollback  
- No big-bang  
- No schema changes in Bridge phases (reuse existing SQL)  
- No UI redesign (projection shape may enrich; templates keep structure)

**P1 partial:** Mission Read Adapter delivers the Mission half of P1 read-path under `ENABLE_MISSION_READ_BRIDGE`.  
**P2 partial (Directive 007):** Recommendation Read Bridge delivers mission-aligned recommendation projection under `ENABLE_RECOMMENDATION_BRIDGE`.  
**P3 partial (Directive 004 / 005):** Mission Start Bridge + Mission Resume Bridge deliver Start and Resume under `ENABLE_MISSION_START_BRIDGE` / `ENABLE_MISSION_RESUME_BRIDGE`.  
**P4 partial (Directive 006):** Session Completion Bridge delivers Complete + Evidence Before Completion under `ENABLE_SESSION_COMPLETION_BRIDGE`.
---

## 10. Acceptance criteria (measurable)

Bridge is **not complete** until all of the following are true under the Bridge feature flag in Internal Alpha:

| ID | Criterion | Measurement |
|---|---|---|
| AC-1 | Every study entry point returns identical educational state for the same user/date/plan | Home CTA mission topic == SQL `Mission` topic from `PlanningService.generate_today_mission` / `get_today_mission` |
| AC-2 | Every recommendation on Experience originates from one runtime policy | Adaptive/Home recommendation topic equals active mission topic when mission exists; no `seeded_demo_adaptive` authority |
| AC-3 | No Experience page consumes `seeded_demo_*` when Bridge + non-demo flags are set | Composition path never calls `seeded_demo_*` for authenticated learners |
| AC-4 | Session ownership is singular | Experience session maps 1:1 to owned SQL `Mission`; foreign mission → 403/404 |
| AC-5 | Planning ownership is singular | Only `PlanningService` creates/selects today’s mission topic |
| AC-6 | Mission ownership is singular | Only SQL `Mission` (+ MissionService) is mission SoT; opaque docs are projections |
| AC-7 | Complete Session updates mastery only through Evidence Authority | Completing canonical session writes the same evidence-gated path as legacy finish (or explicitly no-op with telemetry if outcome deferred) |
| AC-8 | Educational behaviour unchanged vs legacy for same inputs | Golden fixtures: same plan + TopicProgress → same mission topic and readiness labels (within agreed projection formatting) |
| AC-9 | Each migration phase independently releasable with rollback | Phase checklist + rollback drill documented and dry-run |
| AC-10 | `SOLE_RUNTIME` may remain off; when on, Home must satisfy AC-1–AC-3 | Gate test in Internal Alpha |

**Directive 003 slice:** With `ENABLE_MISSION_READ_BRIDGE` on, Home/MissionPort read satisfies AC-6 for today’s session projection and does not use `seeded_demo_mission` on that path.

**Directive 004 slice:** With `ENABLE_MISSION_START_BRIDGE` on, Home/MissionPort start satisfies AC-5 / AC-6 for session initiation (Planning ensure + StudySession start) and does not use demo educational state on that path.

**Directive 005 slice:** With `ENABLE_MISSION_RESUME_BRIDGE` on, Experience resume / `get_session_status` satisfies AC-4 / AC-6 for session continuity (owned In Progress SQL Mission) and does not create replacement or demo sessions.

**Directive 007 slice:** With `ENABLE_RECOMMENDATION_BRIDGE` on, AdaptiveDecisionPort / Home recommendation satisfies AC-2 for recommendation projection (Runtime A RecommendationService + mission alignment; no `seeded_demo_adaptive` authority on that path). Curriculum V1/V2 coexistence preserved ([ADR-003](ADR-003-curriculum-v1-v2.md)).

---

## 11. Definition of “Bridge Complete”

**Bridge Complete** means:

1. Experience ports for Mission, Adaptive (recommendation), Twin (learning state), Journey, and History are backed by Bridge adapters to Runtime A.  
2. `seeded_demo_*` is not used for educational projections in Bridge-enabled, non-demo environments.  
3. Start, Resume, Load Home, Complete, and Recommendation flows match the sequence diagrams and pass contract + regression suites in `TEST_STRATEGY.md`.  
4. Acceptance criteria AC-1 through AC-10 are met.  
5. Rollback for the final Bridge phase is verified.  
6. No educational behaviour change vs legacy for golden learners (AC-8).

**Bridge Complete does not require:**

- Deleting legacy Dashboard/Mission UI  
- Enabling `SOLE_RUNTIME` by default in production  
- Schema migrations  
- Wiring or deleting `MissionEngine*`  
- Replacing `RecommendationService` with `AdaptiveDecisionEngine`

Those are post-Bridge programme items.

---

## 12. Architecture Decision Record

### ADR-MS001-002: Educational Runtime Bridge — SQL services as authority

**Status:** Accepted (architecture); Mission Read + Mission Start + Mission Resume + Session Completion + Recommendation Read slices shipping behind flags
**Date:** 2026-07-25  
**Context:** Dual educational runtimes; SOLE_RUNTIME switches chrome only; Experience defaults to demo projections.

**Decision:** Introduce bridging adapters so Experience ports consume Runtime A (`PlanningService`, `MissionService`, `StudySessionService`, `RecommendationService`, `ReadinessService`, `AdaptiveLearningService`, `LearningLifecycleService`, `StudyPlanService`, Curriculum + Evidence Authority) without Experience owning educational law.

**Consequences:**

- Positive: Single educational truth; sole-runtime cutover becomes safe; preserves determinism and Evidence integrity.  
- Negative: Temporary dual persistence (SQL + projection cache); adapter complexity; must carefully align dual “next” producers.  
- Neutral: V2 engines remain candidates for a later authority migration under a new ADR.

**Alternatives rejected:**

1. **Promote Experience opaque stores as SoT** — loses Evidence/TopicProgress; educational regression.  
2. **Big-bang cutover to MissionEngine*** — unwired, unproven vs SQL behaviour; violates “no behaviour change”.  
3. **Keep dual truth until engines ready** — blocks Foundational Trust and invalidates sole-runtime claims.

---

## 13. Recommended implementation order

See `MIGRATION_PLAN.md` phases. Condensed:

1. Freeze contracts + golden educational fixtures (tests only)  
2. Read-path bridges (Home / Twin / Recommendation alignment) — **Mission Read done**; **Recommendation Read done**
3. Gate off `seeded_demo_*` when Bridge on  
4. Write-path Start / Resume — **Mission Start done**; **Mission Resume done**  
5. Complete + Evidence parity  
6. Journey / History / Revision projections  
7. Durable projection/workspace hardening for multi-worker  
8. Internal Alpha validation gate  
9. (Post-Bridge) Sole-runtime proof; legacy UI retirement

---

## 14. Estimated complexity

| Workstream | Complexity | Notes |
|---|---|---|
| Architecture (Directive 002) | Done | Docs only |
| Mission Read Adapter (Directive 003) | Done | Flag-gated translator |
| Mission Start Bridge (Directive 004) | Done | Flag-gated write translator |
| Mission Resume Bridge (Directive 005) | Done | Flag-gated continuity translator |
| Remaining read-path bridges + flags | **M** | Twin remaining; Recommendation done |
| Write-path resume | Done | Directive 005 |
| Evidence parity on complete | Done (Directive 006) | Session Completion Bridge; further Activity outcome parity may remain |
| Journey/History/Revision read bridges | **M** | Parallelizable after Twin |
| Durable store hardening | **M** | Required before multi-instance sole runtime |
| **Overall to Bridge Complete** | **L–XL** | Dominated by Evidence parity |

---

## 15. Critical blockers

| Blocker | Why it blocks Bridge Complete |
|---|---|
| **No product-locked dual-“next” rule** | Without §5.3, Home may still disagree with Start Session |
| **Evidence parity design for Session Activity** | Canonical activity may not yet capture practice outcomes equivalent to legacy finish forms |
| **In-memory SessionWorkspace / projections in multi-worker** | Resume and ownership break across instances |
| **Demo seed default (`SEED_DEMO_LEARNERS`)** | Must be gated; otherwise AC-3 fails |
| **SOLE_RUNTIME treated as “done” before Bridge** | Critical product risk (fabricated study) — operational, not technical |
| **Import-cycle fragility Planning ↔ StudyPlan** | Bridge tests must not force unsafe import reordering without a small extraction (post-architecture) |

---

## 16. Constraints (binding for implementers)

- No schema changes for Bridge.  
- No UI redesign for Bridge.  
- Preserve Curriculum V1/V2 loadability and traversal.  
- Preserve Evidence Authority as mastery gate.  
- Mission Read Adapter must not implement Resume / Recommendation / writes.
- Mission Start Bridge must not implement Resume / Complete / Recommendation.
- Mission Resume Bridge must not implement Start / Complete / Recommendation / generate.
- Session Completion Bridge must not implement Recommendation / Journey / History / Adaptive bridges.
- Recommendation Read Bridge must not implement writes, Adaptive recalculation, Journey, or History bridges.

---

## 17. Document map

| Document | Contents |
|---|---|
| This file | Authority, consumption map, ADR, acceptance, Bridge Complete, Mission Read / Start / Resume / Completion / Recommendation status |
| `BRIDGE_INTERFACE_SPECIFICATION.md` | Inputs, outputs, failures, fallbacks, telemetry, ownership |
| `BRIDGE_SEQUENCE_DIAGRAM.md` | Mermaid sequences for five flows |
| `MIGRATION_PLAN.md` | Phased releasable migration |
| `ROLLBACK_PLAN.md` | Per-phase and emergency rollback |
| `RISK_ANALYSIS.md` | Technical + educational risk per step |
| `TEST_STRATEGY.md` | Unit → E2E + Internal Alpha |

---

## Stop condition (Directive 007)

Recommendation Read Bridge complete, tests green, this document updated. **Do not begin Journey or History bridges** without architecture review.
