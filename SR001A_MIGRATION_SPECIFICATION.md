# SR-001A — Student Runtime Migration Specification

**Programme:** SR-001A · Student Runtime Migration Specification  
**Date:** 2026-07-30  
**Nature:** Implementation planning only — **no application code modified**  
**Authority:** Binding migration blueprint for every programme that implements SR-001  
**Predecessor:** SR-001 (Student Runtime Recomposition)  
**Supporting audits:** SLJ-001 · MISSION-001 · RR-002.3 · RI-001 / RI-002  
**Constraint:** Do not implement SR-001. Do not modify application architecture in this programme. Plan only.

---

## Executive Summary

SR-001 defines **what** the Student Runtime must become: one enrolment → mission → session → evidence → twin → tomorrow pipeline under seven constitutional singularities.

SR-001A defines **how** that recomposition is executed without destabilising production:

1. **Phased release**, not a single big-bang rewrite.  
2. **Feature flags** for every student-visible behavioural cutover.  
3. **Compose before polish** — bind Session + Evidence + Twin before Home craft.  
4. **Adapters first** — wrap dual writers; delete only after parity gates.  
5. **Independently deployable phases** — each phase ships, measures, and can roll back without reverting prior phases’ educational truth.

The migration is ordered into **eight independently deployable phases** (P0–P7), mapped to SR-001 programme intents (MISSION-002 → SR-002 → LXP/REF → EV-001 → SDT-004 → SR-003 → SR-004 → continuity). Deployment preference is **phased release with feature flags and subject-scoped incremental rollout**. A single monorelease of the full pipeline is **rejected**.

**This document is the roadmap all subsequent development programmes must follow.** Programme names may be adjusted by the Board; **dependency order and cutover gates must not**.

---

## Implementation Phases

### Phase taxonomy

| Phase | Deployable unit | SR-001 programme map | Student-visible? | Flag required? |
|---|---|---|---|---|
| **P0** | Mission briefing trust | MISSION-002 | Yes (presentation) | Soft (can ship behind presentation flag) |
| **P1** | Session spine binding | SR-002 + SR-002a | Yes (Primary CTA) | **Hard** |
| **P2** | Session product completion | LXP-003 | Yes (in-session) | Hard for production path |
| **P3** | Session educational substance | LXP-004 + LXP-005 + REF-001 | Yes | Hard |
| **P4** | Evidence Before Completion | EV-001 | Yes (completion gate) | **Hard** |
| **P5** | Twin activation | SDT-004 | Mostly indirect | Hard |
| **P6** | Progress singularity + curriculum adapter | SR-003 + SR-003b | Partial | Hard |
| **P7** | Legacy retirement + continuity | SR-004 + SLJ-003 + DX-005 exec | Yes | Hard for deletions |

Each phase below is **independently deployable**: it may ship to production with its own flag(s), tests, exit criteria, and rollback, provided its **hard dependencies** (Dependency Matrix) are already green.

---

### P0 — Mission briefing & selection coherence

#### Objectives

- One topic identity across mission title, why-now, curriculum position, and supporting evidence.
- No `node-*` leakage into student-facing chrome.
- CertifiedMissionEngine selection aligned with progress current topic and Home explanation (MISSION-001 defects closed).
- Students must not Start Session against a broken brief.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Selection | `app/application/curriculum_intelligence/` (CertifiedMissionEngine and related scorers) |
| Runtime mission | `app/application/educational_runtime_engine/service.py`, `dto.py` |
| Progress / explanation | `app/domain/educational_runtime_engine/progress.py`; journey explanation builders under educational experience |
| Presentation | `app/presentation/student/educational_view_models.py`, `view_models.py`, `services/student_home_service.py` |
| Experience projection | `app/application/educational_experience/` |
| Tests | `tests/` covering mission generation, Home why-now, node-id sanitisation |

#### Modules affected

- `curriculum_intelligence` (selection AUTHORITY)  
- `educational_runtime_engine` (mission instantiation)  
- `educational_experience` / Student Home VMs (presentation)  
- **Not** LearningSessionRuntime, Evidence, Twin writers

#### Dependencies

- **Hard:** SR-001 accepted; published CS1 package healthy (post–RCV-002).  
- **Soft:** none from later SR phases.  
- **Blocks:** P1 student trust — do not enable Start Session Primary until P0 exit criteria pass (sequencing law).

#### Exit criteria

- Mission topic ≡ progress current topic ≡ Home why-now topic for empty-progress and mid-progress fixtures.  
- Zero `node-` substrings in Home mission title, why-now, and LO labels on the production path.  
- Regression suite for MISSION-001 reproduction cases is green.  
- Gate **G-Progress** *presentation half* satisfied for published path (full engine merge remains P6).

#### Rollback strategy

- Revert presentation/selection PR; no schema change expected.  
- If interim dual-selector flag used: disable flag → prior Runtime C briefing behaviour restored.  
- No Twin/progress event rewrite required.

---

### P1 — Bind execution spine (Home → Session)

#### Objectives

- Published-curriculum Home Primary becomes **Start / Resume Study Session** into `/session/*`.  
- LearningSessionRuntime elevated as session **AUTHORITY**; Session Experience remains HTTP **ADAPTER**.  
- Mission **Accepted** ≡ session start; **Deferred** preserved (ILE-004).  
- Mark-complete is **not** the sole Primary; pilot confirm (if retained) is flag-gated, non-default, non-Twin-grade.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Home CTA | `app/presentation/student/educational_view_models.py` (`can_start_session`, `complete_runtime_c`), `services/student_home_service.py`, Home templates |
| Routes | `app/presentation/student/routes.py`, `app/presentation/session/` |
| Session binding | `app/application/session_experience/` (facade, ports — especially `session_runtime_port.py`, `mission_port.py`) |
| Session AUTHORITY | `app/application/learning_session/` (`runtime.py`, lifecycle, persistence adapter **new or extended**) |
| Runtime complete path | `app/application/educational_runtime_engine/service.py` (`complete_mission` must not be Home Primary) |
| Enrol / coexistence | `app/application/platform_integration/`, `educational_runtime_engine/coexistence.py` (read-only for P1; no retirement yet) |
| Feature flags | `app/application/config/v2_flags.py` (or successor SR flag module) |
| Bridge | `app/infrastructure/adapters/educational_runtime_bridge/` |

#### Modules affected

- Student Home (presentation AUTHORITY)  
- Session Experience (ADAPTER)  
- LearningSessionRuntime (AUTHORITY — elevate + wire)  
- EducationalRuntimeEngine (mission instance must expose session handle)  
- **New logical:** Student Runtime Coordinator (compose-only; may start as thin application service)

#### Dependencies

- **Hard:** P0 exit criteria (briefing trust).  
- **Hard:** Persistence story for LearningSessionRuntime sessions (in-phase or immediate pre-phase deliverable — SR-001 risk R4).  
- **Soft:** LXP substance (P2/P3) — spine may ship with thin activities behind “substance incomplete” honesty, but production default Primary should wait until P2 at least begins (see Deployment Strategy).

#### Exit criteria

- Gate **G-Session:** ≥95% of enrolled published-curriculum test students reach `/session/*` from Home Primary.  
- `can_start_session=True` on published path when flag ON; `session_control != complete_runtime_c` as default Primary.  
- Mark-complete (if present) only behind explicit pilot flag; labelled non-product.  
- LearningSessionRuntime owns phase transitions for bound sessions; Session Experience does not invent a second FSM.

#### Rollback strategy

- Disable **SR session-primary** feature flag → restore PR-001B Mark-complete Primary.  
- In-flight LearningSessionRuntime rows remain readable; do not delete.  
- Do **not** dual-write TOPIC_COMPLETED from both Mark-complete and session complete while flag flips (see Risk Register R-W1).

---

### P2 — Session product completion (LXP-003)

#### Objectives

- Plan checklist, pause/resume, finish review (Yes / Partially / No) on production session path.  
- Honest completion UX before evidence authority (P4) hard-gates Twin.  
- Session lifecycle visible and recoverable across browser sessions.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Session UX | `app/presentation/session/` templates + routes |
| Session services | `app/application/session_experience/` (`completion_service.py`, `session_service.py`, progress) |
| Runtime phases | `app/application/learning_session/` (`lifecycle_manager.py`, `completion_evaluator.py`, policies) |
| Defaults | `app/infrastructure/session/defaults.py` (still present; not yet deleted) |

#### Modules affected

- LearningSessionRuntime completion policies  
- Session Experience completion / progress projections  
- Student session presentation

#### Dependencies

- **Hard:** P1 spine live (flag may still be limited cohort).  
- **Soft:** P0 (assumed done).

#### Exit criteria

- Pause/resume restores same LearningSessionRuntime session.  
- Finish review records Yes/Partially/No before mission complete call.  
- No silent auto-complete without student finish review on default path.

#### Rollback strategy

- Feature flag off → prior session completion UX (or Home Mark-complete if P1 also rolled back).  
- Completed sessions remain; incomplete sessions stay resumable under old UX only if adapters preserve IDs.

---

### P3 — Educational substance (Read / Practice / Reflect)

#### Objectives

- Replace placeholder “Core methods” and three generic free-text defaults on production path.  
- Package/EI-derived Read and Practice activities.  
- Structured reflection; Decision Journal when memory-grade (REF-001).  
- Continuous in-session Read → Practice → Reflect.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Activity ports | `app/application/session_experience/ports/activity_engine_port.py` and adapters |
| Defaults retirement | `app/infrastructure/session/defaults.py` (production path stop using) |
| Curriculum artefacts | Educational Artefact Deriver / package activity projections |
| Reflection | `app/application/learning_session/reflection_manager.py`; Decision Journal packages |
| Presentation | session activity templates under `app/presentation/session/` |

#### Modules affected

- Session activity engines / ports  
- LearningSessionRuntime planner & scheduler  
- Decision Journal (memory-grade only)  
- Curriculum intelligence artefact consumers

#### Dependencies

- **Hard:** P1.  
- **Hard:** P2 finish-review contract (so substance feeds an honest completion).  
- **Soft:** EV-001 (P4) may run in parallel for wiring design but must not claim Twin updates yet.

#### Exit criteria

- Gate precursor to **R2:** placeholder defaults absent from production path when substance flag ON.  
- Read and Practice items resolve to syllabus-bound refs for CS1 certified package.  
- Reflection path available; skip allowed; no Twin scoring from reflection alone.

#### Rollback strategy

- Substance flag OFF → fall back to prior activity set (including defaults if still present) **only** for non-production/pilot cohorts; production should prefer “session unavailable” honesty over fake Core methods once R2 starts.  
- Journal rows retained; no cascade delete.

---

### P4 — Evidence Before Completion (EV-001)

#### Objectives

- Session complete blocked unless EducationalEvidenceAuthority accepts **or** explicit Partial/No recorded.  
- Coverage (`TOPIC_COMPLETED`) advances only under Evidence contract.  
- Mark-complete must not invent understanding-grade evidence.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Evidence AUTHORITY | `app/services/educational_evidence_authority.py` |
| Session evidence | `app/application/learning_session/evidence_collector.py`; VP-001 / learning_evidence bridges |
| Runtime complete | `app/application/educational_runtime_engine/service.py` (`complete_mission`) |
| Experience complete | `app/application/educational_experience/service.py` |
| Student routes | `app/presentation/student/routes.py` (confirm/complete handlers) |
| Legacy writer wrap | `app/services/study_session_service.py` (compatibility only) |

#### Modules affected

- EducationalEvidenceAuthority  
- LearningSessionRuntime evidence collector  
- EducationalRuntimeEngine completion  
- StudySessionService (wrap — not new authority)

#### Dependencies

- **Hard:** P1 + P2 (session exists and has finish review).  
- **Recommended before P5:** P3 substance so evidence is educationally meaningful.  
- **Constitutional:** Twin must not update before this gate (P5 depends on P4).

#### Exit criteria

- Gate **G-Evidence**.  
- Automated tests: complete without evidence rejected; Partial/No recorded without Twin-grade mastery claim.  
- Home Mark-complete (if flag ON) cannot emit Twin-grade or unscoped TOPIC_COMPLETED without evidence adapter.

#### Rollback strategy

- Evidence-gate flag OFF → prior completion writers restored **only** with explicit Board residual (coverage-without-evidence risk). Prefer keeping gate ON and rolling back P5 Twin instead.  
- Do not delete evidence rows on rollback.

---

### P5 — Twin activation (SDT-004)

#### Objectives

- Twin birth/initialisation for published-curriculum enrolments.  
- Twin updates **only after** Evidence Authority success on daily loop.  
- Learner Lifecycle Orchestrator becomes the sole observation path for that loop.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Twin packages | `app/application/student_digital_twin/`, `app/domain/student_digital_twin/` |
| Lifecycle | `app/application/learner_lifecycle/` |
| Session twin port | `app/application/session_experience/ports/student_twin_port.py` |
| Enrol hooks | EducationalRuntimeEngine enrol / platform_integration (Twin birth) |
| Calibration parity | Runtime A calibration twin init patterns (reference only) |

#### Modules affected

- Student Digital Twin  
- Learner Lifecycle  
- Session Experience twin port  
- Enrolment adapters (birth timing)

#### Dependencies

- **Hard:** P4 (Evidence Before Completion).  
- **Hard:** P1 session path producing evidence commits.  
- **Soft:** P3 (richer evidence quality).

#### Exit criteria

- Gate **G-Twin:** Twin Active or Initialised after first lawful session evidence on published path.  
- No Twin write from Mark-complete alone.  
- Observation-only: Twin does not teach or select missions directly.

#### Rollback strategy

- Twin-update flag OFF → stop new Twin writes; retain existing Twin state.  
- Session + Evidence + Progress may continue.  
- Do not fabricate Twin from coverage events while flag OFF.

---

### P6 — Progress singularity & curriculum source adapter

#### Objectives

- One Progress Engine: mission topic ≡ position ≡ why-now (engine-level, not only presentation).  
- JSON-bundled curricula feed the **same** Student Runtime pipeline via Curriculum Source Adapter.  
- RuntimeCoexistencePolicy shrinks toward subject cutover registry (not dual OS).  
- Prefer single write + dual read projection over two writers.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Progress | `app/domain/educational_runtime_engine/progress.py`; TopicProgress / journey projections |
| Educational state | `app/application/educational_state/` |
| Coexistence | `app/application/educational_runtime_engine/coexistence.py` |
| Enrol bridge | `app/application/platform_integration/` (FounderStudentEnrolmentBridge) |
| Study plans | `app/services/` StudyPlanService (wrap) |
| Mission merge | `app/application/mission_engine_v2/` (lifecycle semantics merge only) |
| Coordinator | Student Runtime Coordinator application package (**new or extended**) |

#### Modules affected

- Progress AUTHORITY  
- Curriculum Source Adapter (new/extended)  
- Coexistence policy  
- Mission lifecycle composition (ERE + ILE-004 + ME v2 semantics)  
- EducationalStateService (sole read model — must not hide dual writes)

#### Dependencies

- **Hard:** P0 (selector coherence) + P1 + P4 (lawful completion events).  
- **Soft:** P5 (Twin may inform tomorrow composition but Progress singularity does not require Twin inference theatre).

#### Exit criteria

- Gate **G-Progress** fully.  
- JSON subject smoke path uses same Mission → Session → Evidence pipeline under adapter.  
- No silent dual write of progress for the same enrolment.  
- Coexistence no longer encodes “two student products” for cut-over subjects.

#### Rollback strategy

- Per-subject cutover registry revert → prior coexistence routing for that subject.  
- Event store retained; do not recompute history destructively.  
- Dual-read projections may remain temporarily if single-write rolls back carefully.

---

### P7 — Legacy retirement & continuity craft

#### Objectives

- Retire default Mark-complete Primary (R1), placeholder defaults (R2), Unified Journey as alternate day OS (R3), StudySessionService as student writer (R4), SQL Mission parallel lifecycle (R5), coexistence dual-OS semantics (R6), legacy Contained shells (R7), RI temporary recommendation hosts as scheduled (R8).  
- Tomorrow continuity (SLJ-003) and Home craft (DX-005 execution) **only after** educational truth is real.

#### Files affected (expected)

| Area | Paths |
|---|---|
| Legacy UX | `app/dashboard/`, `app/mission/`, `app/analytics/` (templates/routes already redirect — deletion) |
| Consolidation | `app/presentation/consolidation.py` |
| Unified Journey | `app/application/unified_journey/` (chrome merge then retire flag) |
| Legacy services | `app/services/study_session_service.py`, MissionService SQL path |
| Home polish | `app/presentation/student/` templates + DX-005 artefacts |
| Continuity | Student Home tomorrow / missed-day UX |

#### Modules affected

- Presentation consolidation  
- Legacy blueprints  
- Unified Journey  
- Compatibility recommendation hosts (RI lineage)  
- Student Home craft (last)

#### Dependencies

- **Hard:** Gates G-Session, G-Evidence, G-Twin, G-Progress, G-Single-CTA.  
- **Hard:** P3 for R2; P4/P5 for intelligence honesty; P6 for R6.  
- **Sequencing law:** Do not polish Home before spine + substance + evidence.

#### Exit criteria

- Gates **G-Single-CTA**, **G-Retire-A-shell**, **G-Retire-coexistence**.  
- Legacy templates deletable without breaking sole-runtime redirects.  
- Continuity: student returning next day sees next Mission brief (non-empty Primary).

#### Rollback strategy

- Deletions are **last**; prefer flag-disable of new chrome before hard delete.  
- Template deletion requires prior release that already redirects; rollback = restore templates from git tag.  
- Never restore Mark-complete as **designed** product Primary (constitutional); emergency accessibility mode only with Board waiver.

---

## Dependency Matrix

### Hard dependencies (must exist before phase begins)

```
P0  ──►  P1  ──►  P2  ──►  P3
              │         │
              │         └──►  P4  ──►  P5
              │                │
              └────────────────┴──►  P6  ──►  P7
```

| Phase | Must be complete before start | May overlap / parallelise |
|---|---|---|
| P0 | SR-001 accepted; published package healthy | Founder ops, non-student work |
| P1 | P0 | Design of P2/P3; persistence spike for LSR |
| P2 | P1 | P3 design; P4 contract design |
| P3 | P1; P2 finish-review contract | P4 implementation behind flag |
| P4 | P1 + P2 | P3 (recommended), P5 design |
| P5 | P4 | P6 design |
| P6 | P0 + P1 + P4 | P5 (soft) |
| P7 | G-Session, G-Evidence, G-Twin, G-Progress, G-Single-CTA precursors | Continuity after gates; never before spine |

### Architectural dependency detail

| Consumer | Requires | Forbidden until |
|---|---|---|
| Home Start Session Primary | Mission brief coherence (P0); session handle from runtime | — |
| LearningSessionRuntime as AUTHORITY | Persistence adapter; Session Experience port bind | Claiming sole session without HTTP bind |
| Evidence gate | Session finish review producing candidate evidence | Twin writes |
| Twin update | Evidence Authority success | Mark-complete-only path |
| Progress TOPIC_COMPLETED | Evidence contract (P4) | Dual writers |
| Curriculum Source Adapter cutover | Same pipeline as published path | Dual behavioural OS |
| Legacy deletion | All G-* gates | Any open dual-write |
| Home DX polish | Pipeline true (P1–P5) | Twin theatre without evidence |

### Cutover gate ownership

| Gate | Owning phase | Blocks |
|---|---|---|
| G-Session | P1 | R1 Mark-complete retirement; CR1 “loop complete” claims |
| G-Evidence | P4 | P5 Twin; understanding claims |
| G-Twin | P5 | Intelligence product claims; P7 Twin theatre |
| G-Progress | P0 (presentation) + P6 (engine) | Trust / why-now consistency |
| G-Single-CTA | P1 behavioural + P7 cleanup | Mark-complete as default |
| G-Retire-A-shell | P7 | Template deletion |
| G-Retire-coexistence | P6→P7 | Dual OS semantics removal |

---

## Migration Order

### Authorised sequence (binding)

```
SR-001 (blueprint — done)
  → SR-001A (this specification — planning only)
  → P0  MISSION-002
  → P1  SR-002 / SR-002a
  → P2  LXP-003
  → P3  LXP-004 / LXP-005 / REF-001
  → P4  EV-001
  → P5  SDT-004
  → P6  SR-003 / SR-003b
  → P7  SR-004 / SLJ-003 / DX-005 execution
```

### Order laws

1. **Do not** enable production Start Session Primary before P0.  
2. **Do not** activate Twin writes before P4.  
3. **Do not** delete legacy shells before G-Retire-* gates.  
4. **Do not** polish Home (DX-005 execution) before P1–P5 educational truth.  
5. Board may rename programmes; **may not** reorder hard dependencies without written residual risk.

### Per-release checklist (every phase)

1. Tests green (phase Testing Strategy).  
2. Feature flag default OFF in production initially.  
3. Dogfood / cohort ON.  
4. Gate metrics measured.  
5. Rollback drill documented.  
6. Only then widen rollout / flip default.

---

## Testing Strategy

### Cross-cutting requirements

- Prefer **deterministic** fixtures (empty progress, mid-progress, deferred mission, pause/resume).  
- Cover **published CS1** path as primary; JSON adapter path as secondary from P6.  
- No test may treat Mark-complete as the designed happy path after P1 flag-default ON.  
- Architecture tests: presentation must not call Twin/progress math directly.

---

### P0 — Mission briefing

| Layer | Required coverage |
|---|---|
| **Unit** | CertifiedMissionEngine scoring with prerequisites; title sanitisation (no node-id); why_now selector preference |
| **Integration** | enrol → generate_daily_mission → EducationalExperience projection → Home VM; MISSION-001 reproduction fixtures |
| **Regression** | RCV-002 Begin Learning still enrols; progress derive unchanged for empty stream |
| **Acceptance** | Manual: Home shows one topic across title / why-now / position; no node IDs |

### P1 — Session spine

| Layer | Required coverage |
|---|---|
| **Unit** | Mission accept → session create; Deferred path; flag matrix (session primary ON/OFF) |
| **Integration** | Home Primary → `/session/*` → LearningSessionRuntime snapshot; Runtime C enrolment session handle |
| **Regression** | Flag OFF restores Mark-complete; Runtime A `/session/*` not broken; sole-runtime redirects intact |
| **Acceptance** | G-Session metric ≥95% on test cohort; Primary CTA copy = Start/Resume Session |

### P2 — Session completion product

| Layer | Required coverage |
|---|---|
| **Unit** | Pause/resume state machine; Yes/Partially/No finish review DTOs |
| **Integration** | Multi-request resume; completion evaluator + Experience complete handoff |
| **Regression** | Incomplete sessions do not emit TOPIC_COMPLETED |
| **Acceptance** | Student can pause, return, finish with explicit review |

### P3 — Substance

| Layer | Required coverage |
|---|---|
| **Unit** | Activity port resolves package artefacts; defaults not selected when substance ON |
| **Integration** | Read → Practice → Reflect continuous session; Journal write when memory-grade |
| **Regression** | Reflection alone does not update Twin mastery |
| **Acceptance** | No “Core methods” on production CS1 session |

### P4 — Evidence

| Layer | Required coverage |
|---|---|
| **Unit** | Evidence Authority accept/reject; Partial/No recording |
| **Integration** | Session complete → evidence → only then runtime `complete_mission` / TOPIC_COMPLETED |
| **Regression** | Mark-complete pilot cannot bypass Evidence for Twin-grade claims |
| **Acceptance** | G-Evidence; blocked complete without evidence |

### P5 — Twin

| Layer | Required coverage |
|---|---|
| **Unit** | Twin birth on published enrol; update-after-evidence only |
| **Integration** | Evidence success → lifecycle orchestrator → Twin Active/Initialised |
| **Regression** | Coverage event alone does not mutate Twin when gate ON |
| **Acceptance** | G-Twin |

### P6 — Progress & adapter

| Layer | Required coverage |
|---|---|
| **Unit** | Single progress derive; adapter maps JSON curriculum into same DTOs |
| **Integration** | Mission topic ≡ progress ≡ why-now after completion events; JSON subject smoke pipeline |
| **Regression** | No dual write for same enrolment; coexistence cutover registry behaviour |
| **Acceptance** | G-Progress; subject cutover reversible |

### P7 — Retirement & continuity

| Layer | Required coverage |
|---|---|
| **Unit** | Redirect map still covers deleted routes; flag removals |
| **Integration** | Full pipeline Brief → Session → Evidence → Twin → Complete → Tomorrow |
| **Regression** | Legacy URL matrix; RI compatibility hosts as scheduled |
| **Acceptance** | G-Single-CTA, G-Retire-A-shell, G-Retire-coexistence; next-day brief present |

### Continuous regression (every phase)

- `pytest` suites for: educational_runtime_engine, learning_session, session_experience, student presentation, evidence authority, twin.  
- Sole-runtime consolidation tests.  
- Begin Learning / RCV published package smoke.  
- ruff on touched packages.

---

## Deployment Strategy

### Decision

| Option | Verdict |
|---|---|
| Single release of entire SR-001 pipeline | **Rejected** — blast radius across Home, Session, Evidence, Twin, Progress, routing |
| Phased release | **Required** — P0→P7 as independently deployable units |
| Feature flags | **Required** for every student-visible behavioural cutover (especially P1, P4, P5, P7) |
| Incremental rollout | **Required** — cohort → subject → all published enrolments |

### Recommended model

```
Develop phase N behind flag (default OFF)
  → Deploy code (safe dark)
  → Enable for founder/dogfood
  → Enable for limited enrolled cohort
  → Measure gates
  → Default ON for published subjects
  → Only then start phase N+1 default expansion
```

### Flag sketch (names illustrative; implement in config module)

| Flag | Controls | Default prod (initial) |
|---|---|---|
| `SR_MISSION_BRIEF_COHERENCE` | P0 presentation/selection | OFF → ON after P0 accept |
| `SR_SESSION_PRIMARY` | P1 Home Start Session | OFF |
| `SR_PILOT_MARK_COMPLETE` | Emergency/accessibility confirm | OFF (never default ON after P1) |
| `SR_SESSION_SUBSTANCE` | P3 package activities | OFF |
| `SR_EVIDENCE_GATE` | P4 | OFF |
| `SR_TWIN_DAILY_LOOP` | P5 | OFF |
| `SR_PROGRESS_SINGULARITY` | P6 | OFF |
| `SR_CURRICULUM_ADAPTER_JSON` | P6 JSON path | OFF per subject |
| `SR_LEGACY_SHELL_DELETE` | P7 hard delete readiness | OFF until gates |

### Rollout dimensions

1. **Cohort** — staff / dogfood users first.  
2. **Subject** — CS1 published first; JSON subjects only via adapter after P6.  
3. **Geography/environment** — staging full pipeline before production default ON.  
4. **Write path** — enable read/projection before enabling new writers when uncertain.

### Database / migration posture

- Prefer **additive** Alembic revisions (new session persistence tables, twin birth columns) over destructive rewrites.  
- No drop of progress event history.  
- Dual-write windows discouraged; if unavoidable, time-box with explicit programme and metrics.  
- Backfills are separate deployable steps with their own rollback (restore from backup / stop writer).

### What must not ship together in one unflagged release

- P1 Primary cutover + P4 evidence gate + P5 Twin + P7 deletions.  
- Mission Engine v2 UI rewrite + lifecycle merge (merge semantics only in P6).  
- Home DX polish + first Session bind.

---

## Rollback Plan

### Principles

1. **Flag-first rollback** — disable behavioural flags before reverting code when possible.  
2. **Preserve educational records** — sessions, evidence, Twin observations, progress events are not deleted on rollback.  
3. **No Twin fabrication** during rollback.  
4. **Constitutional floor** — do not re-declare Mark-complete as the designed product Primary; emergency mode only.  
5. **Phase independence** — rolling back P5 must not require rolling back P1 if Evidence still holds.

### Phase rollback matrix

| Phase | Primary rollback | Data impact | Cascades |
|---|---|---|---|
| P0 | Revert PR / disable brief flag | None | Delay P1 enable |
| P1 | `SR_SESSION_PRIMARY=OFF` | LSR rows retained | P2–P5 cohort loses new Primary |
| P2 | Completion UX flag OFF | Reviews retained | Finish-review optional again |
| P3 | Substance flag OFF | Activities / journal retained | Placeholders only if Board accepts honesty risk |
| P4 | Evidence flag OFF (**discouraged**) | Evidence retained | Prefer keep ON; pause P5 |
| P5 | Twin flag OFF | Twin state retained; stop writes | Progress/session continue |
| P6 | Per-subject registry revert | Events retained | Subject returns to prior routing |
| P7 | Restore templates from tag; keep redirects | N/A | Do not restore dual OS |

### Emergency procedure

1. Disable student-visible SR flags (`SESSION_PRIMARY`, `TWIN_DAILY_LOOP`, substance).  
2. Confirm Begin Learning + Home still render.  
3. If progress corruption suspected: stop writers; Founder ops inspect event stream; do not auto-repair with Mark-complete.  
4. File residual risk; Board decides whether emergency confirm mode is allowed.

---

## Risk Register

### Cross-cutting

| ID | Area | Risk | Sev | Likely | Mitigation |
|---|---|---|---|---|---|
| R-A1 | Architecture | Treating sole-runtime chrome as One Runtime | H | H | Measure G-Session/G-Evidence/G-Twin, not enrolment alone |
| R-A2 | Architecture | Scope creep into Mission Engine v2 UI rewrite | M | M | P6 merges lifecycle semantics only |
| R-A3 | Architecture | Unified Journey becomes second session FSM | M | M | Journey contributes VMs only |
| R-W1 | Runtime | Dual writers (Mark-complete + session complete) | H | H | Single write authority; flag mutex; tests |
| R-W2 | Runtime | Silent dual progress projections hide dual write | H | M | EducationalStateService audit in P6 |
| R-F1 | Product | Enable Primary before substance | H | M | Cohort-limited P1; P2/P3 before default ON |
| R-C1 | Commercial | CR1 claims before G-Session | H | M | Gate commercial claims on pipeline |

### Database

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-D1 | LearningSessionRuntime without durable persistence | H | Persistence adapter mandatory in/before P1 |
| R-D2 | Destructive migration of progress events | H | Additive only; no history rewrite |
| R-D3 | Twin schema birth race on enrol | M | Idempotent Twin init; enrol retry safe |
| R-D4 | Orphan session rows after rollback | L | Retain; cleanup programme later |

### Routing

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-R1 | `/session/*` unreachable from Runtime C Home | H | P1 integration + G-Session |
| R-R2 | Legacy `/missions/*/session*` confusion | M | Keep redirects; no new features |
| R-R3 | Premature deletion of Contained shells | H | G-Retire-A-shell before delete |
| R-R4 | Open redirects / auth gaps on new session start | H | Existing login_required + ownership checks on session bind |

### Runtime (Student Runtime / A–C coexistence)

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-RT1 | Coexistence continues as dual product | H | P6 cutover registry; G-Retire-coexistence |
| R-RT2 | JSON subjects regress during published-first work | M | Curriculum Source Adapter; subject flags |
| R-RT3 | Student Runtime Coordinator becomes god-object | M | Compose-only; domain authorities keep math |
| R-RT4 | complete_mission still Home Primary under flag bugs | H | Flag tests; CTA assertions |

### Student Home

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-H1 | Mark-complete remains sole Primary | H | P1 + G-Single-CTA |
| R-H2 | Dual-topic why-now persists | H | P0 then P6 |
| R-H3 | Polishing Home before truth | M | P7 sequencing law |
| R-H4 | Latent/uncertified panels on L0 | M | Retire per SR-001 disposition |

### Mission Engine

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-M1 | Selection vs explanation diverge (MISSION-001) | H | P0 hard before P1 default |
| R-M2 | Accept/Deferred semantics lost | M | SR-002a in P1 |
| R-M3 | Confirm-without-accept remains | H | Lifecycle: Accepted = session start |
| R-M4 | ME v2 merge pulls scheduler UI rewrite | M | Semantics-only merge checklist |

### LearningSessionRuntime

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-L1 | Elevate without HTTP bind (still orphaned) | H | P1 exit requires `/session/*` bind |
| R-L2 | Session Experience remains parallel FSM | H | Port merge plan; authority tests |
| R-L3 | Placeholder defaults in production | H | P3 + R2 |
| R-L4 | Persistence adapter incomplete | H | Block P1 default ON |

### Evidence

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-E1 | Coverage treated as understanding | H | P4 G-Evidence |
| R-E2 | Twin update without evidence | H | P5 hard-depends P4 |
| R-E3 | StudySessionService remains covert writer | M | Wrap then R4 in P7 |
| R-E4 | Partial/No not recorded | M | P2 + P4 acceptance |

### Twin

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-T1 | Twin birth missing on published enrol | H | P5 enrol hooks |
| R-T2 | Assumption-driven Twin from Mark-complete | H | Forbid; tests |
| R-T3 | Twin “teaches” / selects missions | M | Observation-only reviews |
| R-T4 | Activating Twin before evidence adequacy | H | EV-001 before SDT-004 |

---

## Success Criteria

### Programme (SR-001A) success

| Criterion | Met when |
|---|---|
| Complete roadmap | Phases P0–P7 independently deployable with objectives, files, modules, dependencies, exit criteria, rollback |
| Dependency clarity | Matrix states hard prerequisites and forbidden parallelism |
| Risk coverage | Database, routing, runtime, Home, Mission, LSR, Evidence, Twin addressed |
| Testing blueprint | Unit / integration / regression / acceptance per phase |
| Deployment choice | Phased + flags + incremental rollout mandated; single release rejected |
| No code changed | Application tree untouched by SR-001A |

### Migration success (post-implementation programmes)

| Criterion | Gate / evidence |
|---|---|
| One execution path | Brief → Session → Read → Practice → Reflect → Evidence → Twin → Complete → Tomorrow |
| G-Session | ≥95% published test enrolments Start Session from Home |
| G-Evidence | Complete blocked without Evidence or explicit Partial/No |
| G-Twin | Twin Active/Initialised after first lawful evidence |
| G-Progress | Mission ≡ position ≡ why-now |
| G-Single-CTA | Mark-complete not default Primary |
| G-Retire-* | Legacy shells and dual-OS coexistence removable |
| No architectural regression | Layering preserved; V1/V2 curricula loadable; no second student OS |

---

## Final Recommendation

**Execute SR-001 as a phased, flag-gated migration (P0→P7), not a monorelease.**

1. **Start with P0 (MISSION-002)** — students must not enter Session on incoherent briefs.  
2. **Bind the spine next (P1)** behind `SR_SESSION_PRIMARY`, with LearningSessionRuntime persistence solved before default ON.  
3. **Fill substance (P2–P3)** before declaring the Study Loop commercially ready.  
4. **Wire Evidence then Twin (P4→P5)** — never reverse.  
5. **Collapse dual paths (P6)** with per-subject cutover, then **retire legacy (P7)** and only then polish Home continuity.

**Rejected:** single release; polishing Home first; Twin without Evidence; deleting Contained shells before G-Retire gates; leaving Mark-complete as the designed Primary.

**Authorised next action:** schedule **MISSION-002 (P0)** implementation programme under this specification. Do not begin P1 default production cutover until P0 exit criteria pass.

**SR-001A does not implement the Student Runtime.** It is the migration law subsequent programmes must obey.

---

## Appendix A — Traceability to SR-001

| SR-001 element | SR-001A location |
|---|---|
| Phase 0 Constitution & briefing | P0 |
| Phase 1 Bind execution spine | P1 |
| Phase 2 Educational substance | P2 + P3 |
| Phase 3 Intelligence substrate | P4 + P5 + P6 (progress) |
| Phase 4 Collapse dual paths | P6 + P7 |
| Phase 5 Continuity & craft | P7 (after gates) |
| Cutover gates G-* | Dependency Matrix + Success Criteria |
| Retirement waves R1–R8 | P1 / P3 / P7 mappings |
| Risks R1–R10 | Risk Register (expanded) |

## Appendix B — Document control

| Field | Value |
|---|---|
| Status | **Accepted as migration specification** (implementation not started) |
| Supersedes | Informal “big bang One Runtime” delivery plans |
| Does not supersede | SR-001 constitutional singularities; Educational Constitution; Product Blueprint |
| Application code modified | **None** |
| Next authorised action | Implement P0 (MISSION-002) per this blueprint |

**End of SR-001A.**
