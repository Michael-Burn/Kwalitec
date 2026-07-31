# LXP-003 — Study Session Product Completion

**Programme:** LXP-003 · SR-001A Phase P2  
**Date:** 2026-07-30  
**Nature:** P2 implementation — complete, recoverable Study Session product workflow  
**Authority:** SR-001 + SR-001A  
**Predecessor:** SR-002 (P1 Session Spine Binding)  

---

## Executive Summary

LXP-003 completes the Study Session **product** experience on the LearningSessionRuntime spine. Students can pause and resume the same session, recover progress after refresh or navigation, enter an explicit Finish Review (Yes / Partially / No), and close the session without silent auto-complete.

Educational substance (Read / Practice / Reflect), Evidence Before Completion, Twin updates, and mission / topic completion are intentionally out of scope. Session close records a finish review and marks the LearningSessionRuntime session complete only — `mission_completed=False` and `progress_advanced=False`.

Flag: `SR_SESSION_COMPLETION_PRODUCT` (default **OFF**). When ON with `SR_SESSION_PRIMARY`, Finish Review is required before session close.

---

## Architecture Changes

```
Student Home (P1 spine)
        ↓
/session/*  Session Experience (HTTP ADAPTER)
        ↓  pause / resume / finish review / progress
SessionRuntimeAdapter
        ↓
LearningSessionRuntimeEngine (opaque)
        ↓
LearningSessionRuntime (session AUTHORITY)
        ↓  READY_TO_FINISH + FinishReview
LearningSessionPersistenceAdapter (handle + progress docs)
```

| Concern | Owner |
|---|---|
| Lifecycle transitions | `LearningSessionRuntime` / `LifecycleManager` |
| Finish Review authority | `FinishReview` DTO + `complete_session(require_finish_review=True)` |
| Persistence / recovery | `LearningSessionPersistenceAdapter` (`lsr.handle`, `lsr.progress`) |
| HTTP workflow | Session Experience `/session/*` |
| Product flag | `SR_SESSION_COMPLETION_PRODUCT` |

---

## Files Created

- `app/application/learning_session/dto/finish_review.py`
- `tests/test_lxp003_session_product.py`
- `LXP003_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

### LearningSessionRuntime (AUTHORITY)

- `app/application/learning_session/runtime_phase.py` — `READY_TO_FINISH` phase + `REQUEST_FINISH` event; product lifecycle labels
- `app/application/learning_session/lifecycle_manager.py` — `request_finish`; resume from ready-to-finish; complete from ready-to-finish
- `app/application/learning_session/runtime.py` — `request_finish`, `record_finish_review`, finish-review-gated `complete_session`
- `app/application/learning_session/policies/completion_policy.py` — optional finish-review requirement; rejects silent completion
- `app/application/learning_session/completion_evaluator.py` — pass-through finish review evaluation
- `app/application/learning_session/exceptions.py` — `FinishReviewRequired`
- `app/application/learning_session/dto/__init__.py` — export Finish Review types

### Persistence / opaque engine

- `app/infrastructure/adapters/learning_session/persistence.py` — finish review + checklist + active surface progress docs
- `app/infrastructure/adapters/learning_session/runtime_engine.py` — pause / resume / request finish / checklist / surface / gated complete

### Session Experience (ADAPTER)

- `app/application/session_experience/ports/session_runtime_port.py` — pause / resume / request_finish / checklist / surface / finish kwargs
- `app/application/session_experience/session_service.py` — pause / resume / checklist; recovery of persisted surface
- `app/application/session_experience/completion_service.py` — Finish Review gate; never completes missions
- `app/application/session_experience/facade.py` — public pause / resume / request_finish / checklist / finish kwargs
- `app/infrastructure/session/runtime_adapter.py` — port method implementations

### Presentation / flags

- `app/application/config/v2_flags.py` — `SR_SESSION_COMPLETION_PRODUCT`
- `app/presentation/session/forms.py` — Pause / Resume / Checklist / FinishReview forms
- `app/presentation/session/routes.py` — pause / resume / checklist / finish_start / finish review POST
- `app/presentation/session/views.py` — pause / resume / checklist / request_finish / finish kwargs
- `app/presentation/session/messages.py` — pause / ready-to-finish / finish-review copy
- `app/presentation/session/dto/study_session.py` — pause / checklist / finish-review page fields
- `app/presentation/session/services/study_session_service.py` — P2 primary kinds and Finish Review UX
- `app/templates/session/partials/session_body.html` — Finish Review radios, Pause, checklist
- `app/templates/session/base.html` — product-language comment hygiene
- `tests/application/session_experience/helpers.py` — fake port signatures for P2

---

## Session State Machine

Product lifecycle (student-visible):

```
Created → Started → In Progress → Paused → Resumed
  → Ready to Finish → Completed
```

RuntimePhase mapping:

| Product label | RuntimePhase | Domain SessionState |
|---|---|---|
| Created | `planned` / `ready` | `not_started` |
| Started / In Progress | `active` | `active` |
| Paused | `paused` | `paused` |
| Resumed | `active` | `active` |
| Ready to Finish | `ready_to_finish` | `active` or `paused` (unchanged until close) |
| Completed | `completed` | `completed` |

Lawful P2 transitions added:

- `ACTIVE|PAUSED + REQUEST_FINISH → READY_TO_FINISH`
- `READY_TO_FINISH + RESUME → ACTIVE` (cancel finish review)
- `READY_TO_FINISH + COMPLETE → COMPLETED` (requires Finish Review when flag ON)

Silent `ACTIVE → COMPLETED` remains lawful only when `SR_SESSION_COMPLETION_PRODUCT` is OFF (rollback).

---

## Persistence Behaviour

Additive opaque documents via `SessionDocumentStore` (no Alembic):

| Namespace | Purpose |
|---|---|
| `lsr.handle` | SessionHandle + phase + finish_review |
| `lsr.open` | Per-student open session pointer |
| `lsr.mission` | Mission → session pointer |
| `lsr.progress` | active_surface, checklist ticks, paused flag |

Progress and handle survive browser refresh and navigation when the durable store is enabled (or process memory in tests).

---

## Recovery Strategy

1. Pause persists `paused` phase + current surface.
2. Home Resume (P1) or `POST /session/<id>/resume` restores ACTIVE and returns to the saved surface.
3. `open_session` rehydrates workspace from persisted progress when status is in-progress / paused / ready-to-finish.
4. Multiple reload cycles keep the same `session_id` and phase.
5. Quiet Exit under the product flag posts Pause (safe leave) rather than abandoning the sitting.

---

## Finish Review UX

When `SR_SESSION_COMPLETION_PRODUCT=1`:

1. Student reaches Ready to Finish (`POST /session/<id>/finish/start` or reflection primary).
2. Summary surface presents **Did you complete today's planned study?** with Yes / Partially / No (+ optional notes).
3. `POST /session/<id>/complete` (or `/finish`) requires a verdict.
4. Session is marked completed; **mission is not completed**; no TOPIC_COMPLETED.
5. Without a verdict, completion is rejected (`finish_review_required`).

Educational meaning of the review: today's planned activity was engaged (Yes), partially engaged (Partially), or not (No). It does **not** claim mastery, Twin change, or evidence authority (P4).

---

## Tests Added

`tests/test_lxp003_session_product.py`

| Layer | Coverage |
|---|---|
| **Unit** | FinishReview DTO; READY_TO_FINISH transitions; pause/resume; silent-complete blocked; flag matrix |
| **Integration** | Persistence pause/resume same session_id; checklist survival; finish review persisted; silent complete rejected |
| **Regression** | Session complete does not emit TOPIC_COMPLETED / mission_completed |
| **Acceptance** | Pause → multi-refresh → resume → ready_to_finish → blocked silent complete → explicit No review; flag-off rollback path |

Also updated `tests/application/session_experience/helpers.py` for new port signatures.

### Tests Executed

```bash
python3 -m pytest tests/test_lxp003_session_product.py \
  tests/presentation/session/ \
  tests/application/session_experience/test_services.py \
  tests/application/learning_session/test_lifecycle.py -q
# 438 passed
```

---

## Evidence

- Pause/resume restores the same LearningSessionRuntime `session_id` (integration tests).
- Finish review Yes/Partially/No recorded on binding before close.
- Silent complete rejected when product flag / `require_finish_review` is ON.
- `mission_completed=False` and `progress_advanced=False` on opaque complete.
- Flag OFF restores prior complete-without-review behaviour (rollback).

---

## P2 Exit Criteria

| Criterion | Status |
|---|---|
| Pause/resume restores same LearningSessionRuntime session | **Met** |
| Finish review records Yes/Partially/No before mission complete call | **Met** (and mission complete is still not called) |
| No silent auto-complete without finish review on default product path | **Met** when `SR_SESSION_COMPLETION_PRODUCT=ON` |
| Session progress survives refresh / navigation | **Met** via `lsr.progress` + handle persistence |
| Mission completion NOT triggered | **Met** (deferred to P4) |

---

## Migration Impact

None. Additive opaque documents only; no Alembic revisions.

---

## Architecture Compliance

- LearningSessionRuntime remains session AUTHORITY.
- Session Experience remains HTTP ADAPTER (opaque ports only).
- Curriculum V1/V2 traversal untouched.
- No evidence pipeline, Twin writes, or Progress Engine changes.
- Substance remains marked `incomplete` pending P3.

---

## Technical Debt

- Plan checklist UI is wired but overview page does not yet project checklist items from opaque overview into `StudySessionPage.checklist` (engine stores them; presentation helper returns empty pending a thin overview VM pass).
- In-process SessionExperienceRegistry still holds workspace; recovery prefers persisted `lsr.progress` on re-open.
- Client timer remains browser-local (IAHF-001); server elapsed seconds field exists but is not yet driven by the EOS timer JS.

---

## Known Limitations

- No educational Read / Practice / Reflect substance (P3).
- No Evidence Before Completion gate (P4).
- No Twin activation (P5).
- Finish Review does not advance study progress or complete Runtime C missions.
- Product flag defaults OFF for phased rollout.

---

## Recommendation for P3 Readiness

P2 exit criteria are satisfied for the session **product** shell. P3 (LXP-004 / LXP-005 / REF-001) may begin behind `SR_SESSION_SUBSTANCE` once:

1. Dogfood cohort enables `SR_SESSION_PRIMARY` + `SR_SESSION_COMPLETION_PRODUCT`.
2. Pause / resume / finish-review acceptance is confirmed on published CS1 path.
3. Package/EI activity ports are ready to replace placeholder substance without inventing a second session FSM.

Do **not** enable Evidence Before Completion (P4) until P2 finish-review contract is stable in the enabled cohort.
