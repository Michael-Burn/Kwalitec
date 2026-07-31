# SR-002 — Student Runtime Session Spine Binding

**Programme:** SR-002 · SR-001A Phase P1  
**Date:** 2026-07-30  
**Nature:** P1 implementation — Home → Study Session execution spine  
**Authority:** SR-001 + SR-001A  
**Predecessor:** MISSION-002 (P0)  

---

## Executive Summary

SR-002 binds Student Home to the Study Session for published-curriculum students. When `SR_SESSION_PRIMARY` is ON, Home Primary becomes **Start Study Session** / **Resume Study Session**, Mission Accepted becomes synonymous with starting a LearningSessionRuntime session, and the student lands on the canonical `/session/*` experience.

LearningSessionRuntime is elevated as session **AUTHORITY**; Session Experience remains an HTTP **ADAPTER**. Educational substance (Read / Practice / Reflect), Evidence Before Completion, and Twin updates are intentionally out of scope — the spine ships with honest `substance: incomplete` markers.

When `SR_SESSION_PRIMARY` is OFF (default for phased rollout), Runtime C **Mark mission complete** is restored for rollback. Mark-complete is never the designed product Primary when the session spine is enabled.

---

## Architecture Changes

```
Student Home (presentation AUTHORITY)
        ↓  Start / Resume Study Session  (SR_SESSION_PRIMARY=ON)
Student Runtime Coordinator (compose-only)
        ↓  Mission Accepted ≡ session start
LearningSessionRuntime (session AUTHORITY)
        ↓  SessionHandle + phase machine
LearningSessionPersistenceAdapter (opaque docs)
        ↓
Session Experience /session/* (HTTP ADAPTER)
```

| Concern | Owner |
|---|---|
| Home Primary CTA | `educational_view_models` + `StudentHomeService` |
| Composition | `StudentRuntimeCoordinator` |
| Session lifecycle | `LearningSessionRuntime` |
| Persistence | `LearningSessionPersistenceAdapter` via `SessionDocumentStore` |
| HTTP workspace | Session Experience `/session/*` |
| Mission Accepted / Deferred | `EducationalRuntimeEngineService.accept_mission` / `defer_mission` |

---

## Files Created

- `app/application/student_runtime/__init__.py`
- `app/application/student_runtime/coordinator.py`
- `app/application/student_runtime/dto.py`
- `app/application/student_runtime/exceptions.py`
- `app/infrastructure/adapters/learning_session/__init__.py`
- `app/infrastructure/adapters/learning_session/persistence.py`
- `app/infrastructure/adapters/learning_session/runtime_engine.py`
- `tests/test_sr002_session_spine.py`
- `SR002_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

### Feature flags

- `app/application/config/v2_flags.py` — `SR_SESSION_PRIMARY` (default OFF), `SR_PILOT_MARK_COMPLETE` (default OFF)

### Mission lifecycle (SR-002a)

- `app/domain/educational_runtime_engine/state.py` — `ACCEPTED`, `DEFERRED` statuses + transitions
- `app/domain/educational_runtime_engine/events.py` — `MISSION_ACCEPTED`, `MISSION_DEFERRED`
- `app/application/educational_runtime_engine/service.py` — `get_mission_instance`, `accept_mission`, `defer_mission`; open-mission query includes accepted/deferred

### Home / session binding

- `app/presentation/student/educational_view_models.py` — Start/Resume Study Session Primary when flag ON
- `app/presentation/student/services/student_home_service.py` — resume label; Mark-complete labelled rollback/pilot
- `app/presentation/student/views.py` — Runtime C path through Student Runtime Coordinator
- `app/presentation/student/routes.py` — Mark-complete gated; defer mirrors mission Deferred; start errors for spine
- `app/infrastructure/session/composition.py` — inject `LearningSessionRuntimeEngine` when flag ON

### Tests

- `tests/domain/educational_runtime_engine/test_lifecycle.py`
- `tests/test_dx006b_student_home.py` — Resume Study Session copy
- `tests/certification/test_pr001b_student_pilot.py` — Home OS clarity assertions aligned to mission panel

---

## Session Lifecycle

```
Mission GENERATED
  → Accept (Home Start Study Session)
      → LearningSessionRuntime create → prepare → start (ACTIVE)
      → persist SessionHandle
      → provision Session Experience overview
      → redirect /session/<id>/*
  → Resume (open binding)
      → resume PAUSED if needed → /session/<id>/*
  → Defer (ILE-004)
      → Mission DEFERRED (no session; no TOPIC_COMPLETED)
```

Mission completion and `TOPIC_COMPLETED` remain on the existing complete path (pilot / rollback only while P1 is live). Session complete does **not** advance syllabus coverage in P1 (Evidence gate is P4).

---

## Routing Changes

| Route | Behaviour |
|---|---|
| `POST /student/session/start` | Runtime C + flag ON → Coordinator accept/start → `/session/*` |
| `GET /session/<id>/*` | Unchanged HTTP adapter; LSR engine bound when flag ON |
| `POST /student/mission/complete` | Blocked when `SR_SESSION_PRIMARY` ON and pilot OFF; rollback path when flag OFF |
| `POST /student/commitment/defer` | Still records commitment deferral; also `defer_mission` when flag ON |

---

## Persistence Strategy

- **No Alembic migration** in P1.
- Opaque documents in `SessionDocumentStore` (in-memory by default; durable when `ENABLE_DURABLE_STORE` is ON via existing aggregate repos).
- Namespaces: `lsr.handle`, `lsr.open`, `lsr.mission`.
- Rollback retains rows; flag OFF restores Mark-complete Primary without deleting sessions (SR-001A R-D1 / R-D4).

---

## Feature Flags

| Flag | Env | Default | Role |
|---|---|---|---|
| `SR_SESSION_PRIMARY` | `SR_SESSION_PRIMARY` | **OFF** | Home Start/Resume Study Session spine |
| `SR_PILOT_MARK_COMPLETE` | `SR_PILOT_MARK_COMPLETE` | **OFF** | Emergency Mark-complete when spine ON (never product default) |
| `SR_MISSION_BRIEF_COHERENCE` | (unchanged) | ON | P0 briefing trust |

**Rollback:** set `SR_SESSION_PRIMARY=0` → Mark-complete Primary restored.

---

## Tests Added

| Layer | Coverage |
|---|---|
| **Unit** | Flag matrix; accept → LSR session; idempotent resume; flag-off block; Deferred → re-accept; accept does not emit TOPIC_COMPLETED |
| **Integration** | Home Primary Start Study Session; overview provision; HTTP start → `/session/*` |
| **Regression** | Flag OFF restores Mark-complete; complete route blocked when spine ON; Runtime A session routes intact |
| **Acceptance** | G-Session precursor: published student Home → start → `/session/*` → resume path |

**Command:**

```bash
python3 -m pytest \
  tests/test_sr002_session_spine.py \
  tests/domain/educational_runtime_engine/test_lifecycle.py \
  tests/certification/test_pr001b_student_pilot.py \
  tests/test_dx006b_student_home.py \
  -q
```

**Result:** **44 passed** (2026-07-30). Ruff clean on touched packages.

---

## Evidence

- `tests/test_sr002_session_spine.py` — 15 P1-focused cases
- Home HTML with flag ON: Primary `Start Study Session`, `session_control=start`, no `complete_runtime_c`
- Flag OFF: `complete_runtime_c` / Mark mission complete restored
- Mission status `accepted` after start; `MISSION_ACCEPTED` event with `session_id` payload
- Session overview authority `learning_session_runtime`

---

## P1 Exit Criteria

| Criterion | Status |
|---|---|
| Home Primary = Start / Resume Study Session when flag ON | **Met** |
| Primary launches LearningSessionRuntime via `/session/*` | **Met** |
| Mission Accepted ≡ session start | **Met** |
| LearningSessionRuntime sole session execution authority for bound sessions | **Met** |
| Session Experience HTTP adapter only | **Met** |
| Mark-complete only for rollback (flag OFF) / pilot (explicit) | **Met** |
| Deferred preserved (ILE-004) | **Met** |
| No educational substance / Evidence / Twin | **Honoured (out of scope)** |

Gate **G-Session** (≥95% cohort reach `/session/*`) is instrumentable; automated acceptance covers the path. Production default remains flag **OFF** until dogfood / cohort rollout per SR-001A.

---

## Architecture Compliance

- **Layering preserved:** routes thin; coordinator composes; LSR owns phase math; Session Experience does not invent a second FSM.
- **Curriculum V1/V2:** unchanged loadability; published path is the P1 bind surface.
- **No Twin / Evidence / Progress redesign.** Accept does not emit `TOPIC_COMPLETED`.
- **No schema / Alembic migrations.**

---

## Technical Debt

- Session overview/activity still uses placeholder activity counts until P2/P3 substance.
- Coordinator and Session composition both wrap the same `SessionDocumentStore`; a shared DI factory would reduce adapter duplication.
- `get_journey` open-mission query updated for ACCEPTED/DEFERRED; other call sites that assume only `generated` should be audited in P6.

---

## Known Limitations

- Substance incomplete by design (P2/P3).
- Session complete does not complete the Runtime C mission or update Twin (P4/P5).
- Flag default OFF — production students still see Mark-complete until rollout enablement.
- JSON Runtime A start path unchanged (Curriculum Source Adapter is P6).

---

## Recommendation for P2 Readiness

**P1 exit criteria are satisfied. P2 (LXP-003 — Session product completion) may proceed** behind the live spine for dogfood cohorts, subject to:

1. Keep `SR_SESSION_PRIMARY` cohort-limited until pause/resume + finish review (Yes/Partially/No) ship.
2. Do not enable Twin or Evidence gates before P4.
3. Do not polish Home craft (DX-005 execution) before P1–P5 educational truth.

**Authorised next programme:** LXP-003 (P2) — plan checklist, pause/resume product UX, finish review on the `/session/*` path bound in SR-002.

**SR-002 does not implement educational substance.** It establishes the single execution spine for the Student Runtime.
