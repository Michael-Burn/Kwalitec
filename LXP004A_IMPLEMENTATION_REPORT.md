# LXP-004A — Educational Session Substance

**Programme:** LXP-004A · SR-001A Phase P3 Foundation  
**Date:** 2026-07-30  
**Nature:** P3 foundation — continuous Read → Practice → Reflect educational flow  
**Authority:** SR-001 + SR-001A  
**Predecessor:** LXP-003 (P2 Session Product Completion)  

---

## Executive Summary

LXP-004A transforms the completed Study Session product shell into a structured learning experience. Every session follows one continuous educational sequence:

Learning Objectives → Reading → Worked Examples (when available) → Practice → Reflection → Ready to Finish

Package/mission-derived activities replace placeholder “Core methods” free-text defaults on the production path when `SR_SESSION_SUBSTANCE` is ON. LearningSessionRuntime remains the sole session AUTHORITY; Session Experience stays the HTTP ADAPTER.

Evidence Before Completion, Twin updates, mission completion, and progress advancement remain out of scope (P4+).

Flag: `SR_SESSION_SUBSTANCE` (default **OFF**).

---

## Educational Flow

```
Overview — Learning Objectives
        ↓
Begin Session
        ↓
Reading Activity
        ↓
Worked Example (when package/mission facts support it)
        ↓
Practice Activity (one or more)
        ↓
Reflection (skip allowed; no Twin scoring)
        ↓
Ready to Finish (Finish Review from LXP-003)
```

Student-visible stages (`EducationalStage`):

| Stage | Surface | Role |
|---|---|---|
| `learning_objectives` | Overview | Present syllabus-bound objectives |
| `read` | Activity | Package-derived reading |
| `worked_example` | Activity | Method walkthrough when available |
| `practice` | Activity | Syllabus-bound practice prompts |
| `reflection` | Reflection | Structured close; skip allowed |
| `ready_to_finish` | Summary | Finish Review (P2) |

Transitions are continuous: each activity CTA names the next stage (e.g. “Continue to Worked Example”, “Continue to Practice”, “Continue to Reflection”). Students never encounter three disconnected generic free-text prompts.

---

## Activity Architecture

```
Published package / mission facts
        ↓
EducationalSubstancePlanner
        ↓  EducationalSessionSubstance
PackageActivityEngine (opaque *_opaque)
        ↓
SessionActivityAdapter (ActivityEnginePort)
        ↓
Session Experience ActivityService
        ↓
Study Session presentation (typed stage labels)
```

| Concern | Owner |
|---|---|
| Educational stage law | `educational_flow.py` |
| Package → activity sequence | `EducationalSubstancePlanner` |
| Opaque activity engine | `PackageActivityEngine` |
| Session FSM / finish | `LearningSessionRuntime` |
| HTTP workflow | Session Experience `/session/*` |
| Product flag | `SR_SESSION_SUBSTANCE` |

Substance resolution order:

1. Published artefacts via `EducationalEngineFoundationService` (curriculum identity + topic).
2. Honest mission-facts fallback (task descriptions, quality rationale, objective ids).
3. Never invent “Core methods” when the substance flag is ON.

---

## Files Created

- `app/application/learning_session/educational_flow.py`
- `app/application/learning_session/substance_planner.py`
- `app/infrastructure/adapters/learning_session/package_activity_engine.py`
- `tests/test_lxp004a_session_substance.py`
- `LXP004A_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

### Flags / composition

- `app/application/config/v2_flags.py` — `SR_SESSION_SUBSTANCE`
- `app/infrastructure/session/composition.py` — inject `PackageActivityEngine` when flag ON; skip demo Core-methods seed on substance path

### LearningSessionRuntime spine

- `app/application/student_runtime/coordinator.py` — plan substance, provision sequence + LO-rich overview, pass real objectives into LSR create
- `app/infrastructure/adapters/learning_session/runtime_engine.py` — substance-aware overview / reflection / response / completion opaque projections
- `app/infrastructure/adapters/learning_session/__init__.py` — export package engine

### Session Experience ADAPTER

- `app/infrastructure/session/activity_adapter.py` — preserve package substance (no Core-methods overwrite)
- `app/application/session_experience/activity_service.py` — project `activity_type` / `stage_label`
- `app/application/session_experience/session_service.py` — attach learning objectives from overview opaque
- `app/application/session_experience/dto/activity_snapshot.py` — typed stage fields
- `app/application/session_experience/dto/overview_snapshot.py` — `learning_objectives`
- `app/application/session_experience/_snapshots.py` — map new fields
- `app/domain/session_experience/activity_projection.py` — typed stage fields

### Presentation

- `app/presentation/session/view_models.py` — LO + stage labels on VMs
- `app/presentation/session/dto/study_session.py` — substance page fields
- `app/presentation/session/services/study_session_service.py` — stage-aware task/content copy
- `app/templates/session/partials/session_body.html` — LO list, multiline reading body, stage meta

---

## Runtime Integration

LearningSessionRuntime remains sole session AUTHORITY:

1. Coordinator accepts mission → creates/prepares/starts LSR handle.
2. When substance ON, planner builds `EducationalSessionSubstance` from package/mission facts.
3. Package activity sequence is provisioned into the shared `SessionDocumentStore` (`activity.sequence`, substance=`package`).
4. Overview opaque reports `substance: package`, learning objectives, and educational flow tags.
5. Activity port serves Read → Example → Practice continuously under the same `session_id`.
6. Reflection and Finish Review remain LSR-owned; complete still sets `mission_completed=False` and `progress_advanced=False`.
7. Response recording marks `evidence_emitted=False` and `twin_updated=False` (P4/P5 deferred).

---

## Tests Added

`tests/test_lxp004a_session_substance.py`

| Layer | Coverage |
|---|---|
| **Unit** | Educational flow order; substance planner Read/Example/Practice; flag matrix; package engine sequence without Core methods |
| **Integration** | Overview + reflection substance projections; checklist-stage sync path; continuous adapter advance |
| **Regression** | Reflection note does not write Journal/Twin; session complete does not complete mission / advance progress |
| **Acceptance** | Published-path style provision shows package substance and no “Core methods” |

### Tests Executed

```bash
python3 -m pytest tests/test_lxp004a_session_substance.py \
  tests/test_lxp003_session_product.py \
  tests/presentation/student/test_cq004_session_substance.py \
  tests/application/session_experience/test_services.py \
  tests/test_sr002_session_spine.py -q
# 69 passed

python3 -m ruff check <LXP-004A touched modules>
# All checks passed
```

---

## Educational Examples

**Topic:** Cash flows (syllabus-bound)

1. **Learning objectives (Overview)**  
   - Explain operating cash flow components  
   - Classify investing and financing flows  

2. **Reading**  
   Topic + objective list + educational rationale as study material. Student notes one idea that stood out.

3. **Worked example**  
   Method steps: restate objective → identify syllabus idea → apply to one concrete case → check against objective wording.

4. **Practice**  
   “Apply 1.1.1: Explain operating cash flow components. Explain your approach in a few sentences.”

5. **Reflection**  
   “After reading, examples, and practice on Cash flows, what still feels unclear — and what will you try next?” (skip allowed)

6. **Ready to Finish**  
   Finish Review Yes / Partially / No (LXP-003) — does not claim mastery.

---

## P3 Exit Criteria

| Criterion | Status |
|---|---|
| Placeholder “Core methods” absent from production path when substance flag ON | **Met** |
| Read and Practice items resolve to syllabus-bound refs (package or mission facts) | **Met** |
| Continuous in-session Read → Practice → Reflect | **Met** |
| Learning objectives presented on Overview | **Met** |
| Worked examples included when package/mission facts support them | **Met** |
| Reflection path available; skip allowed; no Twin scoring from reflection alone | **Met** |
| LearningSessionRuntime remains sole session AUTHORITY | **Met** |
| Evidence / Twin / mission completion / progress advancement NOT implemented | **Met** (deferred) |

---

## Migration Impact

None. Additive opaque documents only (`activity.sequence` substance payload); no Alembic revisions.

---

## Architecture Compliance

- LearningSessionRuntime remains session AUTHORITY.
- Session Experience remains HTTP ADAPTER (opaque ports only).
- Curriculum V1/V2 traversal untouched.
- No Evidence Authority writes, Twin updates, or Progress Engine changes.
- Substance content is syllabus-bound derivation / mission facts — not black-box LLM generation.

---

## Technical Debt

- Full CKG `ReadingReference` / `WorkedExample` / `PracticeExercise` entity bodies are not yet projected; substance uses derived package objectives, mission tasks, and educational rationale. Richer EI item banks remain a LXP-005 follow-up.
- Decision Journal memory-grade write (REF-001) is stubbed honest (`journal_written=False`) — foundation reflection only.
- Overview checklist auto-tick is best-effort on stage submit; presentation checklist projection from overview metadata remains thin (noted in LXP-003).

---

## Known Limitations

- Flag defaults OFF for phased rollout.
- When package authority cannot resolve and mission facts are empty, substance planning returns None (honest) rather than inventing Core methods.
- No Evidence Before Completion gate (P4).
- No Twin activation (P5).
- No adaptive intelligence inside the session.

---

## Recommendation for P4 Readiness

P3 foundation exit criteria are satisfied for educational substance behind `SR_SESSION_SUBSTANCE`. P4 (EV-001 Evidence Before Completion) may begin once:

1. Dogfood cohort enables `SR_SESSION_PRIMARY` + `SR_SESSION_COMPLETION_PRODUCT` + `SR_SESSION_SUBSTANCE`.
2. Continuous Read → Practice → Reflect acceptance is confirmed on published CS1 sessions (no Core methods).
3. Finish Review contract from P2 remains stable so evidence can gate completion without inventing a second FSM.

Do **not** enable Twin activation (P5) until Evidence Before Completion accepts or explicit Partial/No is recorded.

Optional P3 polish before default-ON substance: wire CKG reading/practice entities (LXP-005 depth) and memory-grade Decision Journal (REF-001).
